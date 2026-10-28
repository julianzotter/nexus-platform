#!/usr/bin/env python3
"""NEXUS Agent Communication Bus (ACB) v0.2 — file-based, hash-chained message bus.

WO-20261027-ID02-ACB-002 + ID01-Entscheide 2026-10-27 (WO-Namensschema, Ledger-ID je Nachricht). Root: 00_WORKFLOW_PATTERN_REGISTRY/20_RUNTIME/COMMUNICATION/
Commands: send | inbox | verify | ack | ledger-verify
Rules: fail closed; never delete (move-only); every write is read back and hash-compared.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ACB_VERSION = "0.2.0"
NAMING_SCHEMA = "YY_MM_DD_<ID>_<TYPE>_<TITLE>_vX.Y.Z.md"  # ID01-Entscheid 2026-10-27 (WO K5); <ID>=Rollen-ID ID##
MSG_SCHEMA_VERSION = "v0.1.0"
LEDGER_ID_RE = re.compile(r"^\d{4}$")
TZ = ZoneInfo("Europe/Vienna")
DEFAULT_ROOT = Path("00_WORKFLOW_PATTERN_REGISTRY/20_RUNTIME/COMMUNICATION")
SUBDIRS = ("ID02_TO_ID03", "ID03_TO_ID02", "PROCESSED", "FAILED")
LEDGER = "_ACB_LEDGER.jsonl"
ROLE_RE = re.compile(r"^ID\d{2}$")
GENESIS = "0" * 64


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def now_iso() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def resolve_root(root: str | None) -> Path:
    base = Path(root) if root else Path(os.environ.get("NEXUS_ACB_ROOT", DEFAULT_ROOT))
    return base.resolve()


def ensure_layout(root: Path) -> list[str]:
    """Create root + subfolders if missing. Returns list of created paths."""
    created: list[str] = []
    for sub in ("",) + SUBDIRS:
        p = root / sub
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)
            created.append(str(p))
    ledger = root / LEDGER
    if not ledger.exists():
        ledger.touch()
        created.append(str(ledger))
    return created


def last_ledger_hash(root: Path) -> str:
    ledger = root / LEDGER
    last = GENESIS
    if ledger.exists():
        for line in ledger.read_text(encoding="utf-8").splitlines():
            if line.strip():
                last = json.loads(line)["entry_hash"]
    return last


def ledger_append(root: Path, entry: dict) -> dict:
    """Append hash-chained ledger entry; returns the stored entry."""
    entry = dict(entry)
    entry["prev_hash"] = last_ledger_hash(root)
    entry["ts"] = now_iso()
    payload = json.dumps(entry, sort_keys=True, ensure_ascii=False)
    entry["entry_hash"] = sha256_bytes(payload.encode("utf-8"))
    with (root / LEDGER).open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, sort_keys=True, ensure_ascii=False) + "\n")
    return entry


def next_seq(root: Path) -> int:
    ledger = root / LEDGER
    n = 0
    if ledger.exists():
        for line in ledger.read_text(encoding="utf-8").splitlines():
            if line.strip() and json.loads(line).get("event") == "SEND":
                n += 1
    return n + 1


def split_frontmatter(text: str) -> tuple[dict, str]:
    """Parse minimal 'key: value' YAML frontmatter. Returns (meta, body)."""
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = text.index("\n---\n", 4)
    meta: dict = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip("'\"")
    return meta, text[end + 5:]


def build_message(sender: str, recipient: str, subject: str, body: str,
                  seq: int, reply_to: str | None, artifact_id: str) -> tuple[str, str]:
    """Return (filename, file_text). Name per NAMING_SCHEMA; TITLE=<THEMA>-<ledger_id>.

    body hash covers UTF-8 body after closing frontmatter LF. artifact_id = 00_ID_LEDGER ID (ID01: 1 ID je Nachricht).
    """
    ts = datetime.now(TZ)
    body_hash = sha256_bytes(body.encode("utf-8"))
    msg_id = f"ACB-{ts.strftime('%Y%m%dT%H%M%S')}-{sender}-{recipient}-{artifact_id}"
    theme = re.sub(r"[^A-Za-z0-9-]+", "-", subject).strip("-").upper()[:40]
    fname = f"{ts.strftime('%y_%m_%d')}_{sender}_ACB-MSG_{theme}-{artifact_id}_{MSG_SCHEMA_VERSION}.md"
    fm = [
        "---", f"msg_id: {msg_id}", f"acb_version: {ACB_VERSION}", f"artifact_id: '{artifact_id}'",
        f"acb_seq: {seq:04d}", f"from: {sender}",
        f"to: {recipient}", f"subject: {subject}", f"timestamp: '{ts.isoformat(timespec='seconds')}'",
        f"in_reply_to: {reply_to or 'null'}", "hash_scope: body_utf8_after_closing_frontmatter_lf",
        f"body_sha256: {body_hash}", "status: SENT", "---",
    ]
    return fname, "\n".join(fm) + "\n" + body


def cmd_send(a: argparse.Namespace) -> int:
    for r in (a.sender, a.recipient):
        if not ROLE_RE.match(r):
            return fail(f"invalid role id {r!r}; expected ID## (AGBS v003)")
    root = resolve_root(a.root)
    ensure_layout(root)
    outdir = root / f"{a.sender}_TO_{a.recipient}"
    outdir.mkdir(exist_ok=True)
    body = Path(a.body_file).read_text(encoding="utf-8") if a.body_file else a.body or ""
    if not body.strip():
        return fail("empty body")
    if not LEDGER_ID_RE.match(a.artifact_id):
        return fail("--artifact-id must be a 4-digit 00_ID_LEDGER id (ID01: one ledger id per message)")
    fname, text = build_message(a.sender, a.recipient, a.subject, body, next_seq(root), a.reply_to, a.artifact_id)
    target = outdir / fname
    if target.exists():
        return fail(f"target exists: {target}")
    data = text.encode("utf-8")
    target.write_bytes(data)
    readback = target.read_bytes()  # READBACK: bytes on disk == bytes intended
    if sha256_bytes(readback) != sha256_bytes(data):
        return fail(f"readback mismatch: {target}")
    meta, _ = split_frontmatter(readback.decode("utf-8"))
    entry = ledger_append(root, {"event": "SEND", "msg_id": meta["msg_id"], "artifact_id": a.artifact_id, "from": a.sender,
                                 "to": a.recipient, "path": str(target.relative_to(root)),
                                 "file_sha256": sha256_bytes(readback),
                                 "body_sha256": meta["body_sha256"], "readback": "PASS"})
    print(json.dumps({"status": "SENT", "path": str(target), "msg_id": meta["msg_id"],
                      "file_sha256": entry["file_sha256"], "entry_hash": entry["entry_hash"]}, indent=2))
    return 0


def verify_file(path: Path) -> dict:
    raw = path.read_bytes()
    meta, body = split_frontmatter(raw.decode("utf-8"))
    actual = sha256_bytes(body.encode("utf-8"))
    ok = actual == meta.get("body_sha256")
    return {"path": str(path), "msg_id": meta.get("msg_id"), "from": meta.get("from"),
            "to": meta.get("to"), "subject": meta.get("subject"), "in_reply_to": meta.get("in_reply_to"),
            "body_sha256_expected": meta.get("body_sha256"), "body_sha256_actual": actual,
            "file_sha256": sha256_bytes(raw), "hash_match": ok, "verdict": "PASS" if ok else "FAIL"}


def cmd_inbox(a: argparse.Namespace) -> int:
    root = resolve_root(a.root)
    items = []
    for d in sorted(root.glob(f"*_TO_{a.role}")):
        for f in sorted(d.glob("*.md")):
            items.append(verify_file(f))
    print(json.dumps({"role": a.role, "count": len(items), "messages": items}, indent=2))
    return 0


def cmd_verify(a: argparse.Namespace) -> int:
    res = verify_file(Path(a.path))
    print(json.dumps(res, indent=2))
    return 0 if res["hash_match"] else 2


def cmd_ack(a: argparse.Namespace) -> int:
    """Readback-ack by recipient: verify, then move to PROCESSED (or FAILED). Move-only."""
    root = resolve_root(a.root)
    src = Path(a.path).resolve()
    res = verify_file(src)
    if res["to"] != a.by:
        return fail(f"ack by {a.by} but message addressed to {res['to']}")
    dest_dir = root / ("PROCESSED" if res["hash_match"] else "FAILED")
    dest_dir.mkdir(exist_ok=True)
    dest = dest_dir / src.name
    if dest.exists():
        return fail(f"destination exists: {dest}")
    src.rename(dest)
    entry = ledger_append(root, {"event": "ACK" if res["hash_match"] else "ACK_FAILED",
                                 "msg_id": res["msg_id"], "by": a.by, "from_path": str(src.relative_to(root)),
                                 "to_path": str(dest.relative_to(root)), "file_sha256": res["file_sha256"],
                                 "readback": res["verdict"]})
    print(json.dumps({"status": entry["event"], "path": str(dest), "entry_hash": entry["entry_hash"]}, indent=2))
    return 0 if res["hash_match"] else 2


def cmd_ledger_verify(a: argparse.Namespace) -> int:
    root = resolve_root(a.root)
    prev, n = GENESIS, 0
    for line in (root / LEDGER).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        stored = e.pop("entry_hash")
        if e["prev_hash"] != prev:
            return fail(f"chain break at entry {n}: prev_hash mismatch")
        if sha256_bytes(json.dumps(e, sort_keys=True, ensure_ascii=False).encode("utf-8")) != stored:
            return fail(f"entry {n} hash mismatch")
        prev, n = stored, n + 1
    print(json.dumps({"ledger": str(root / LEDGER), "entries": n, "head": prev, "verdict": "PASS"}, indent=2))
    return 0


def cmd_init(a: argparse.Namespace) -> int:
    root = resolve_root(a.root)
    created = ensure_layout(root)
    print(json.dumps({"root": str(root), "created": created, "layout": list(SUBDIRS) + [LEDGER]}, indent=2))
    return 0


def fail(msg: str) -> int:
    print(json.dumps({"status": "FAIL", "error": msg}), file=sys.stderr)
    return 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="nexus", description="NEXUS ACB v0.1")
    p.add_argument("--root", help=f"ACB root (default: $NEXUS_ACB_ROOT or {DEFAULT_ROOT})")
    sub = p.add_subparsers(dest="group", required=True)
    m = sub.add_parser("message").add_subparsers(dest="cmd", required=True)
    s = m.add_parser("send"); s.add_argument("--from", dest="sender", required=True)
    s.add_argument("--to", dest="recipient", required=True); s.add_argument("--subject", required=True)
    s.add_argument("--body"); s.add_argument("--body-file"); s.add_argument("--reply-to")
    s.add_argument("--artifact-id", required=True, help="4-digit 00_ID_LEDGER id for this message")
    s.set_defaults(fn=cmd_send)
    i = m.add_parser("inbox"); i.add_argument("--for", dest="role", required=True); i.set_defaults(fn=cmd_inbox)
    v = m.add_parser("verify"); v.add_argument("path"); v.set_defaults(fn=cmd_verify)
    k = m.add_parser("ack"); k.add_argument("path"); k.add_argument("--by", required=True); k.set_defaults(fn=cmd_ack)
    m.add_parser("ledger-verify").set_defaults(fn=cmd_ledger_verify)
    m.add_parser("init").set_defaults(fn=cmd_init)
    return p


def main(argv: list[str] | None = None) -> int:
    a = build_parser().parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
