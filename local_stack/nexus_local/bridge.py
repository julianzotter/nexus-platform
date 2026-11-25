"""One-way file bridges (OneDrive <-> Google Drive mount <-> git mirror) with a hash ledger.

Rules
- Never deletes or moves source files. Never deletes destination files.
- A changed destination is never overwritten: the new source version is written next to it
  as <name>.CONFLICT-<UTC>-<rule><ext>, and an incident is recorded.
- New destination files are published create-only (never replace a file that appeared meanwhile).
- A source update of a file this engine published is written side by side as
  <name>.UPDATE-<sha12>-<rule><ext> (default). Only with allow_replace_own_copy=true (ID01 opt-in)
  is the own copy replaced, after archiving the previous bytes in <dst>/.nexus_versions/.
- Bytes are read once into a private snapshot, hashed and re-checked before publication.
- dry_run plans only: no destination writes, no baseline changes.
- Partial files: a file is copied only after size+mtime were stable for `settle_seconds`.
- Cloud placeholders (online-only / recall-on-access) and Google native shortcuts are skipped,
  so a scan never triggers mass downloads.
- Loop protection: identical destination hash -> skip; rule graph cycles are rejected.
- State lives in SQLite under the local runtime dir (never inside a cloud-synced folder).
"""
from __future__ import annotations

import fnmatch
import logging
import os
import shutil
import sqlite3
import stat
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from .util import IS_WINDOWS, SECRET_PATTERNS, DestinationExists, atomic_write_bytes, iso, long_path, now_utc, sha256_bytes, sha256_file

log = logging.getLogger("nexus_local.bridge")

FILE_ATTRIBUTE_OFFLINE = 0x1000
FILE_ATTRIBUTE_RECALL_ON_OPEN = 0x40000
FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS = 0x400000
FILE_ATTRIBUTE_REPARSE_POINT = 0x400
PLACEHOLDER_MASK = FILE_ATTRIBUTE_OFFLINE | FILE_ATTRIBUTE_RECALL_ON_OPEN | FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS

DEFAULT_EXCLUDE_DIRS = (".git", "__pycache__", ".pytest_cache", ".nexus_versions", "node_modules",
                        ".venv", "venv", ".tmp.drivedownload", ".tmp.driveupload", "$RECYCLE.BIN")
DEFAULT_EXCLUDE_FILES = ("~$*", "*.tmp", ".~nexus-*", "desktop.ini", "Thumbs.db", ".DS_Store",
                         "*.gdoc", "*.gsheet", "*.gslides", "*.gform", "*.gmap", "*.gdraw", "*.gsite",
                         "*.lnk", "*.partial", "*.crdownload", "*.CONFLICT-*") + SECRET_PATTERNS


class BridgeConfigError(ValueError):
    pass


_RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}
MAX_PATH_CHARS = 400
MAX_FAILURES = 5


def unsafe_rel(rel: str) -> str | None:
    """Return a reason if a relative path must not be published (fail closed)."""
    if os.path.isabs(rel) or rel.startswith(("\\", "/")) or ":" in rel:
        return "ABSOLUTE_OR_ADS_PATH"
    for part in rel.replace("\\", "/").split("/"):
        if part in ("", ".", ".."):
            return "TRAVERSAL"
        if part.endswith((" ", ".")):
            return "TRAILING_DOT_OR_SPACE"
        if part.split(".")[0].upper() in _RESERVED:
            return "RESERVED_DEVICE_NAME"
        if any(ord(c) < 32 or c in '<>"|?*' for c in part):
            return "INVALID_CHARACTER"
    return None


@dataclass
class Rule:
    name: str
    src: Path
    dst: Path
    mode: str = "mirror"               # mirror = new + changed ; inbox = new only
    include: tuple[str, ...] = ("*",)
    exclude: tuple[str, ...] = ()
    exclude_dirs: tuple[str, ...] = ()
    max_bytes: int = 50 * 1024 * 1024
    max_files_per_cycle: int = 500
    settle_seconds: float = 20.0
    keep_versions: bool = True
    allow_replace_own_copy: bool = False   # ID01 opt-in; default: updates are published side by side
    enabled: bool = True

    @classmethod
    def from_dict(cls, d: dict, expand) -> "Rule":
        if d.get("mode", "mirror") not in ("mirror", "inbox"):
            raise BridgeConfigError(f"INVALID_MODE {d.get('mode')}")
        src, dst = expand(d["src"]), expand(d["dst"])
        if not src or not dst:
            raise BridgeConfigError(f"RULE_PATH_MISSING {d.get('name')}")
        return cls(name=d["name"], src=src, dst=dst, mode=d.get("mode", "mirror"),
                   include=tuple(d.get("include", ["*"])), exclude=tuple(d.get("exclude", [])),
                   exclude_dirs=tuple(d.get("exclude_dirs", [])),
                   max_bytes=int(d.get("max_bytes", 50 * 1024 * 1024)),
                   max_files_per_cycle=int(d.get("max_files_per_cycle", 500)),
                   settle_seconds=float(d.get("settle_seconds", 20)),
                   keep_versions=bool(d.get("keep_versions", True)),
                   allow_replace_own_copy=bool(d.get("allow_replace_own_copy", False)),
                   enabled=bool(d.get("enabled", True)))


def _norm(p: Path) -> str:
    return os.path.normcase(os.path.abspath(str(p)))


def _inside(child: Path, parent: Path) -> bool:
    c, p = _norm(child), _norm(parent)
    return c == p or c.startswith(p.rstrip("\\/") + os.sep)


def validate_rules(rules: Iterable[Rule]) -> None:
    rules = [r for r in rules if r.enabled]
    names = [r.name for r in rules]
    if len(names) != len(set(names)):
        raise BridgeConfigError("DUPLICATE_RULE_NAME")
    for r in rules:
        if _inside(r.dst, r.src) or _inside(r.src, r.dst):
            raise BridgeConfigError(f"RULE_SELF_NESTED {r.name}")
    for a in rules:  # a writes into b's source and b writes back into a's source -> loop
        for b in rules:
            if a is not b and _inside(a.dst, b.src) and _inside(b.dst, a.src):
                raise BridgeConfigError(f"RULE_CYCLE {a.name}<->{b.name}")


class Ledger:
    """SQLite hash ledger. One connection guarded by a lock (thread-safe)."""

    def __init__(self, db_path: Path):
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()
        self.db = sqlite3.connect(str(db_path), check_same_thread=False, timeout=30)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.execute("PRAGMA busy_timeout=30000")
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS files(rule TEXT, rel TEXT, src_size INTEGER, src_mtime_ns INTEGER,
                src_sha TEXT, dst_sha TEXT, synced_at TEXT, PRIMARY KEY(rule, rel));
            CREATE TABLE IF NOT EXISTS pending(rule TEXT, rel TEXT, size INTEGER, mtime_ns INTEGER,
                first_seen REAL, PRIMARY KEY(rule, rel));
            CREATE TABLE IF NOT EXISTS journal(rule TEXT, rel TEXT, dst TEXT, sha TEXT, state TEXT,
                at TEXT, PRIMARY KEY(rule, rel, sha));
            CREATE TABLE IF NOT EXISTS failures(rule TEXT, rel TEXT, n INTEGER, last TEXT, PRIMARY KEY(rule, rel));
            CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT, rule TEXT,
                kind TEXT, rel TEXT, detail TEXT);
        """)
        self.db.commit()

    def get(self, rule: str, rel: str):
        with self.lock:
            return self.db.execute("SELECT src_size, src_mtime_ns, src_sha, dst_sha FROM files WHERE rule=? AND rel=?",
                                   (rule, rel)).fetchone()

    def put(self, rule: str, rel: str, size: int, mtime_ns: int, src_sha: str, dst_sha: str) -> None:
        with self.lock:
            self.db.execute("INSERT OR REPLACE INTO files VALUES(?,?,?,?,?,?,?)",
                            (rule, rel, size, mtime_ns, src_sha, dst_sha, iso()))
            self.db.execute("DELETE FROM pending WHERE rule=? AND rel=?", (rule, rel))  # ledger row only
            self.db.commit()

    def pending(self, rule: str, rel: str, size: int, mtime_ns: int) -> float:
        """Return seconds the (size, mtime) pair has been stable."""
        with self.lock:
            row = self.db.execute("SELECT size, mtime_ns, first_seen FROM pending WHERE rule=? AND rel=?",
                                  (rule, rel)).fetchone()
            now = time.time()
            if row and row[0] == size and row[1] == mtime_ns:
                return now - row[2]
            self.db.execute("INSERT OR REPLACE INTO pending VALUES(?,?,?,?,?)", (rule, rel, size, mtime_ns, now))
            self.db.commit()
            return 0.0

    def journal(self, rule: str, rel: str, dst: str, sha: str, state: str) -> None:
        with self.lock:
            self.db.execute("INSERT OR REPLACE INTO journal VALUES(?,?,?,?,?,?)", (rule, rel, dst, sha, state, iso()))
            self.db.commit()

    def open_journal(self) -> list[tuple]:
        with self.lock:
            return self.db.execute("SELECT rule, rel, dst, sha FROM journal WHERE state='PREPARED'").fetchall()

    def fail(self, rule: str, rel: str, reset: bool = False) -> int:
        with self.lock:
            if reset:
                self.db.execute("DELETE FROM failures WHERE rule=? AND rel=?", (rule, rel))  # counter row only
                self.db.commit()
                return 0
            self.db.execute("INSERT INTO failures VALUES(?,?,1,?) ON CONFLICT(rule, rel) DO UPDATE SET n=n+1, last=?",
                            (rule, rel, iso(), iso()))
            self.db.commit()
            return self.db.execute("SELECT n FROM failures WHERE rule=? AND rel=?", (rule, rel)).fetchone()[0]

    def failures(self, rule: str, rel: str) -> int:
        with self.lock:
            row = self.db.execute("SELECT n FROM failures WHERE rule=? AND rel=?", (rule, rel)).fetchone()
        return row[0] if row else 0

    def event(self, rule: str, kind: str, rel: str, detail: str = "") -> None:
        with self.lock:
            self.db.execute("INSERT INTO events(at, rule, kind, rel, detail) VALUES(?,?,?,?,?)",
                            (iso(), rule, kind, rel, detail[:500]))
            self.db.commit()

    def recent_events(self, limit: int = 50) -> list[dict]:
        with self.lock:
            rows = self.db.execute("SELECT at, rule, kind, rel, detail FROM events ORDER BY id DESC LIMIT ?",
                                   (limit,)).fetchall()
        return [dict(zip(("at", "rule", "kind", "rel", "detail"), r)) for r in rows]

    def counts(self) -> dict:
        with self.lock:
            rows = self.db.execute("SELECT rule, kind, COUNT(*) FROM events GROUP BY rule, kind").fetchall()
        out: dict = {}
        for rule, kind, n in rows:
            out.setdefault(rule, {})[kind] = n
        return out

    def close(self) -> None:
        with self.lock:
            self.db.close()


@dataclass
class CycleResult:
    rule: str
    scanned: int = 0
    copied: int = 0
    unchanged: int = 0
    waiting: int = 0
    conflicts: int = 0
    skipped_placeholder: int = 0
    skipped_other: int = 0
    errors: int = 0
    blocked: str | None = None
    started: str = field(default_factory=iso)
    finished: str | None = None


def is_placeholder(st: os.stat_result) -> bool:
    attrs = getattr(st, "st_file_attributes", 0) or 0
    return bool(attrs & PLACEHOLDER_MASK)


class BridgeEngine:
    def __init__(self, rules: list[Rule], ledger: Ledger, dry_run: bool = False):
        validate_rules(rules)
        self.rules, self.ledger, self.dry_run = rules, ledger, dry_run
        self.last: dict[str, CycleResult] = {}
        self.reconcile()

    def reconcile(self) -> None:
        """After a crash: PREPARED journal rows are resolved by destination readback, never replayed blindly."""
        for rule, rel, dst, sha in self.ledger.open_journal():
            p = Path(long_path(Path(dst)))
            ok = p.is_file() and sha256_file(p) == sha
            self.ledger.journal(rule, rel, dst, sha, "PUBLISHED" if ok else "ABANDONED")
            self.ledger.event(rule, "reconciled", rel, "PUBLISHED" if ok else "ABANDONED_REQUEUE")

    # -------------------------------------------------------------- filters
    @staticmethod
    def _match(name: str, patterns: Iterable[str]) -> bool:
        low = name.lower()
        return any(fnmatch.fnmatch(low, p.lower()) for p in patterns)

    def _walk(self, rule: Rule):
        ex_dirs = DEFAULT_EXCLUDE_DIRS + rule.exclude_dirs
        for root, dirs, files in os.walk(long_path(rule.src)):
            keep = []
            for d in dirs:
                if self._match(d, ex_dirs) or d.startswith(".~nexus"):
                    continue
                try:
                    dst_ = os.lstat(os.path.join(root, d))
                except OSError:
                    continue
                if stat.S_ISLNK(dst_.st_mode) or (getattr(dst_, "st_file_attributes", 0) & FILE_ATTRIBUTE_REPARSE_POINT
                                                  and not getattr(dst_, "st_file_attributes", 0) & PLACEHOLDER_MASK
                                                  and self._is_junction(os.path.join(root, d))):
                    continue  # never follow symlinks/junctions out of the root
                keep.append(d)
            dirs[:] = keep
            for fn in files:
                yield Path(root) / fn

    @staticmethod
    def _is_junction(path: str) -> bool:
        try:
            return os.path.isjunction(path) or os.path.islink(path)
        except AttributeError:  # Python < 3.12
            return os.path.islink(path)

    # -------------------------------------------------------------- cycle
    def run_cycle(self, rule: Rule) -> CycleResult:
        res = CycleResult(rule.name)
        if not rule.enabled:
            res.blocked = "DISABLED"
        elif not rule.src.is_dir():
            res.blocked = "SOURCE_NOT_MOUNTED"
        elif not rule.dst.parent.is_dir():
            res.blocked = "DEST_ROOT_NOT_MOUNTED"
        elif not self.dry_run:
            try:
                rule.dst.mkdir(exist_ok=True)
            except OSError as exc:
                res.blocked = f"DEST_UNAVAILABLE {exc}"
        if res.blocked:
            res.finished = iso()
            self.last[rule.name] = res
            return res
        budget = rule.max_files_per_cycle
        src_root = Path(long_path(rule.src))
        for path in self._walk(rule):
            if budget <= 0:
                break
            name = path.name
            if self._match(name, DEFAULT_EXCLUDE_FILES + rule.exclude) or not self._match(name, rule.include):
                continue
            res.scanned += 1
            try:
                st = os.lstat(path)  # never follow symlinks
            except OSError:
                res.errors += 1
                continue
            if not stat.S_ISREG(st.st_mode):
                continue
            if is_placeholder(st):
                res.skipped_placeholder += 1
                continue
            if st.st_size > rule.max_bytes:
                res.skipped_other += 1
                continue
            rel = os.path.relpath(str(path), str(src_root))
            key = os.path.normcase(rel)
            reason = unsafe_rel(rel) or (None if len(str(rule.dst / rel)) + 80 < MAX_PATH_CHARS else "PATH_TOO_LONG")
            if reason:
                res.skipped_other += 1
                if self.ledger.failures(rule.name, key) == 0:
                    self.ledger.fail(rule.name, key)
                    self.ledger.event(rule.name, "unsupported_path", rel, reason)
                continue
            if self.ledger.failures(rule.name, key) >= MAX_FAILURES:
                res.skipped_other += 1  # quarantined until ID01 resets (see README)
                continue
            row = self.ledger.get(rule.name, key)
            if row and row[0] == st.st_size and row[1] == st.st_mtime_ns:
                res.unchanged += 1
                continue
            if self.ledger.pending(rule.name, key, st.st_size, st.st_mtime_ns) < rule.settle_seconds:
                res.waiting += 1
                continue
            try:
                outcome = self._sync_one(rule, path, rel, key, st, row)
            except OSError as exc:
                res.errors += 1
                n = self.ledger.fail(rule.name, key)
                self.ledger.event(rule.name, "quarantined" if n >= MAX_FAILURES else "error", rel,
                                  f"{type(exc).__name__}: {exc}"[:300])
                log.warning("bridge %s error %s: %s", rule.name, rel, exc)
                continue
            budget -= outcome != "unchanged"
            setattr(res, outcome, getattr(res, outcome) + 1)
        res.finished = iso()
        self.last[rule.name] = res
        return res

    def run_all(self) -> list[CycleResult]:
        return [self.run_cycle(r) for r in self.rules]

    # -------------------------------------------------------------- one file
    def _dst_path_safe(self, rule: Rule, rel: str) -> bool:
        """No symlink/junction between the rule's destination root and the target file."""
        p = rule.dst
        for part in Path(rel).parts:
            if os.path.lexists(long_path(p)) and (os.path.islink(long_path(p)) or self._is_junction(long_path(p))):
                return False
            p = p / part
        return not (os.path.lexists(long_path(p)) and os.path.islink(long_path(p)))

    def _sync_one(self, rule: Rule, path: Path, rel: str, key: str, st: os.stat_result, row) -> str:
        # 1) private snapshot: read bytes ONCE (bounded), hash them, re-stat; publish exactly these bytes
        with open(long_path(path), "rb") as f:
            data = f.read(rule.max_bytes + 1)
            fst = os.fstat(f.fileno())
        if len(data) > rule.max_bytes:
            return "skipped_other"
        st2 = os.lstat(path)
        if len(data) != st.st_size or (fst.st_size, fst.st_mtime_ns) != (st.st_size, st.st_mtime_ns) \
                or (st2.st_size, st2.st_mtime_ns) != (st.st_size, st.st_mtime_ns):
            return "waiting"  # changed while reading -> next cycle
        src_sha = sha256_bytes(data)
        if not self._dst_path_safe(rule, rel):
            self.ledger.event(rule.name, "unsupported_path", rel, "DEST_LINK_IN_PATH")
            return "skipped_other"
        dst = rule.dst / rel
        dst_exists = os.path.lexists(long_path(dst))
        dst_sha = sha256_file(Path(long_path(dst))) if dst_exists else None
        owned = row[3] if row else None            # last bytes THIS engine published (protected baseline)
        if dst_sha == src_sha:
            if not self.dry_run:
                self.ledger.put(rule.name, key, st.st_size, st.st_mtime_ns, src_sha, dst_sha)
            return "unchanged"
        if self.dry_run:  # plan only: no target writes, no baseline change
            kind = "dry_run_conflict" if dst_exists and (rule.mode == "inbox" or owned != dst_sha) else "dry_run_copy"
            self.ledger.event(rule.name, kind, rel, src_sha[:12])
            return "conflicts" if kind == "dry_run_conflict" else "copied"
        if dst_exists:
            external = rule.mode == "inbox" or owned is None or owned != dst_sha
            if external or not rule.allow_replace_own_copy:
                tag = "CONFLICT" if external else "UPDATE"
                side = dst.with_name(f"{dst.stem}.{tag}-{src_sha[:12]}-{rule.name}{dst.suffix}")
                if not os.path.lexists(long_path(side)):
                    try:
                        self._publish(side, data, st, replace=False)
                    except DestinationExists:
                        pass
                # baseline keeps the OWNED hash (never adopt an external edit as ours)
                self.ledger.put(rule.name, key, st.st_size, st.st_mtime_ns, src_sha, owned)
                self.ledger.event(rule.name, "conflict" if external else "update_side_by_side", rel, side.name)
                return "conflicts" if external else "copied"
            if rule.keep_versions:  # explicit ID01 opt-in: archive previous own bytes, then replace
                vdir = dst.parent / ".nexus_versions"
                vdir.mkdir(exist_ok=True)
                shutil.copy2(long_path(dst), long_path(vdir / f"{dst.stem}.{(owned or 'x')[:12]}{dst.suffix}"))
        self.ledger.journal(rule.name, key, str(dst), src_sha, "PREPARED")
        try:
            new_sha = self._publish(dst, data, st, replace=dst_exists)
        except DestinationExists:  # appeared between check and publish -> conflict handling next cycle
            self.ledger.journal(rule.name, key, str(dst), src_sha, "ABANDONED")
            self.ledger.event(rule.name, "conflict", rel, "DEST_APPEARED_DURING_PUBLISH")
            return "conflicts"
        self.ledger.journal(rule.name, key, str(dst), src_sha, "PUBLISHED")
        self.ledger.put(rule.name, key, st.st_size, st.st_mtime_ns, src_sha, new_sha)
        self.ledger.fail(rule.name, key, reset=True)
        self.ledger.event(rule.name, "copied", rel, src_sha[:12])
        return "copied"

    @staticmethod
    def _publish(dst: Path, data: bytes, st: os.stat_result, replace: bool = False) -> str:
        digest = atomic_write_bytes(dst, data, create_only=not replace)
        try:
            os.utime(long_path(dst), ns=(st.st_atime_ns, st.st_mtime_ns))
        except OSError:
            pass
        return digest

    def status(self) -> dict:
        return {"rules": [{"name": r.name, "src": str(r.src), "dst": str(r.dst), "mode": r.mode,
                           "enabled": r.enabled, "last": (self.last.get(r.name).__dict__ if r.name in self.last else None)}
                          for r in self.rules],
                "event_counts": self.ledger.counts(), "dry_run": self.dry_run}
