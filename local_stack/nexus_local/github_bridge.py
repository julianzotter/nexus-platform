"""GitHub -> Drive WORK inbox bridge (github_to_work). Disabled by default, dry-run by default.

Reads committed files under <prefix> of origin/<branch> from an existing local clone WITHOUT touching
its working tree: only `git fetch` (remote-tracking ref) + `git ls-tree` + `git cat-file blob`.
Writes create-only into WORK\\_INBOX_GITHUB; a changed upstream file becomes a side file
<stem>.UPDATE-<blob12>-github_to_work<ext>; nothing is ever overwritten or deleted.
Every written file is recorded in _MANIFEST_GITHUB.json with commit SHA + blob SHA + SHA-256.
Uses the existing local git credential (non-interactive); no cloud credential is added.
"""
from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

from .bridge import DEFAULT_EXCLUDE_FILES, unsafe_rel
from .git_mirror import MirrorBlocked, git, git_env
from .util import DestinationExists, atomic_write_bytes, iso, long_path, sha256_bytes, sha256_file

RULE = "github_to_work"
MANIFEST = "_MANIFEST_GITHUB.json"
BRANCH_OK = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{0,80}$")
PREFIX_OK = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/ -]{0,120}/$")


def _norm_url(u: str) -> str:
    u = u.strip().rstrip("/")
    return u[:-4].lower() if u.lower().endswith(".git") else u.lower()


def _blob(repo: Path, sha: str) -> bytes:
    r = subprocess.run(["git", "-C", str(repo), "cat-file", "blob", sha], capture_output=True, timeout=60,
                       env=git_env(), stdin=subprocess.DEVNULL)
    if r.returncode != 0:
        raise MirrorBlocked(f"CAT_FILE_FAILED {sha[:12]}")
    return r.stdout


def git_blob_sha(path: Path) -> str:
    data = Path(long_path(path)).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def list_tree(repo: Path, commit: str, prefix: str) -> list[dict]:
    """[{mode, sha, size, path}] for regular blobs under prefix (symlinks/submodules skipped)."""
    out = subprocess.run(["git", "-C", str(repo), "ls-tree", "-r", "-z", "--long", commit, "--", prefix],
                         capture_output=True, timeout=60, env=git_env(), stdin=subprocess.DEVNULL)
    if out.returncode != 0:
        raise MirrorBlocked(f"LS_TREE_FAILED {out.stderr.decode('utf-8', 'replace')[:200]}")
    items = []
    for rec in out.stdout.decode("utf-8", "replace").split("\0"):
        if not rec:
            continue
        meta, path = rec.split("\t", 1)
        mode, typ, sha, size = meta.split()
        if typ != "blob" or mode not in ("100644", "100755"):
            continue
        items.append({"mode": mode, "sha": sha, "size": int(size), "path": path})
    return items


def run(cfg: dict, expand) -> dict:
    g = cfg.get("github_to_work", {})
    if not g.get("enabled"):
        return {"status": "DISABLED"}
    repo, dst = expand(g["repo_dir"]), expand(g["dst"])
    branch, prefix = g.get("branch", "main"), g.get("prefix", "reports/")
    dry = bool(g.get("dry_run", cfg.get("bridge_dry_run", True)))
    include = g.get("include", ["*"])
    max_files, max_bytes = int(g.get("max_files_per_cycle", 100)), int(g.get("max_bytes", 50_000_000))
    if not BRANCH_OK.match(branch) or ".." in branch:
        raise MirrorBlocked("BRANCH_INVALID")
    if not PREFIX_OK.match(prefix) or ".." in prefix:
        raise MirrorBlocked("PREFIX_INVALID (relative folder ending with /)")
    gm_branch = cfg.get("git_mirror", {}).get("branch")
    if gm_branch and branch == gm_branch:
        raise MirrorBlocked("LOOP_BLOCKED (branch == git_mirror.branch)")
    if not (repo / ".git").exists():
        return {"status": "BLOCKED", "reason": f"REPO_MISSING {repo}"}
    if not dst.parent.is_dir():  # WORK root must exist (Drive mounted); inbox folder itself may be created
        return {"status": "BLOCKED", "reason": f"WORK_ROOT_MISSING {dst.parent}"}
    want = g.get("remote_url")
    if want and _norm_url(git(repo, "remote", "get-url", "origin")) != _norm_url(want):
        raise MirrorBlocked("ORIGIN_MISMATCH")

    git(repo, "fetch", "--no-tags", "origin", f"+refs/heads/{branch}:refs/remotes/origin/{branch}", timeout=180)
    commit = git(repo, "rev-parse", f"refs/remotes/origin/{branch}^{{commit}}")
    man_path = dst / MANIFEST
    manifest = {"rule": RULE, "repo": want or "", "branch": branch, "prefix": prefix, "files": {}}
    if man_path.is_file():
        try:
            manifest = json.loads(man_path.read_text("utf-8"))
        except (OSError, ValueError):
            pass
    files = manifest.setdefault("files", {})
    res = {"status": "OK", "dry_run": dry, "commit": commit, "copied": 0, "updates": 0, "unchanged": 0,
           "skipped": 0, "planned": [], "finished": None}
    if not dry:
        dst.mkdir(exist_ok=True)
    budget = max_files
    for it in list_tree(repo, commit, prefix):
        rel = it["path"][len(prefix):]
        name = rel.rsplit("/", 1)[-1]
        if (unsafe_rel(rel) or it["size"] > max_bytes
                or any(fnmatch.fnmatch(name.lower(), x.lower()) for x in DEFAULT_EXCLUDE_FILES)
                or not any(fnmatch.fnmatch(name.lower(), x.lower()) for x in include)):
            res["skipped"] += 1
            continue
        prev = files.get(rel)
        if prev and prev.get("blob") == it["sha"]:
            res["unchanged"] += 1
            continue
        if budget <= 0:
            break
        target = dst / Path(rel)
        if os.path.isfile(long_path(target)) and git_blob_sha(target) == it["sha"]:
            if not dry:  # identical bytes already present (e.g. manifest lost) -> adopt, no write
                files[rel] = {"commit": commit, "blob": it["sha"], "sha256": sha256_file(target),
                              "size": it["size"], "written_as": rel, "at": iso(), "adopted": True}
            res["unchanged"] += 1
            continue
        if os.path.lexists(long_path(target)):
            stem, ext = os.path.splitext(target.name)
            target = target.with_name(f"{stem}.UPDATE-{it['sha'][:12]}-{RULE}{ext}")
            kind = "updates"
        else:
            kind = "copied"
        if os.path.lexists(long_path(target)):  # side file already written for this blob
            res["unchanged"] += 1
            continue
        budget -= 1
        if dry:
            res["planned"].append({"rel": rel, "as": target.name, "blob": it["sha"][:12]})
            res[kind] += 1
            continue
        data = _blob(repo, it["sha"])
        digest = sha256_bytes(data)
        try:
            atomic_write_bytes(target, data, create_only=True)
        except DestinationExists:
            res["unchanged"] += 1
            continue
        if sha256_file(target) != digest:
            raise MirrorBlocked(f"READBACK_MISMATCH {rel}")
        files[rel] = {"commit": commit, "blob": it["sha"], "sha256": digest, "size": len(data),
                      "written_as": target.relative_to(dst).as_posix(), "at": iso()}
        res[kind] += 1
    res["planned"] = res["planned"][:50]
    if not dry and (res["copied"] or res["updates"] or any(v.get("adopted") for v in files.values())):
        manifest.update({"last_commit": commit, "updated": iso()})
        atomic_write_bytes(man_path, json.dumps(manifest, indent=1, ensure_ascii=False).encode("utf-8"))
    res["finished"] = iso()
    return res
