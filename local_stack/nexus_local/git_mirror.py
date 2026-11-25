"""Git review-snapshot mirror (disabled by default; review G01/J01-J03).

Only files that ID01 placed into an EXPORT-APPROVED folder are published, as a snapshot commit on a
dedicated review branch of a dedicated private clone. Never main, never force, no rebase/merge/reset,
no `git add -A`: literal paths only. Credential prompts are disabled (non-interactive, AUTH_BLOCKED).
Pushing is not approval: a human opens/reviews the PR.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

from .bridge import DEFAULT_EXCLUDE_FILES, unsafe_rel
from .util import iso, sha256_bytes, sha256_file

BRANCH_RE = re.compile(r"^review/[a-z0-9][a-z0-9._-]{0,60}$")


class MirrorBlocked(RuntimeError):
    pass


def git_env() -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_ASKPASS") and k != "SSH_ASKPASS"}
    env.update({"GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "never", "GIT_ASKPASS": "", "SSH_ASKPASS": "",
                "GIT_EDITOR": "true", "GIT_CONFIG_NOSYSTEM": "1", "GIT_LFS_SKIP_SMUDGE": "1"})
    return env


def git(repo: Path, *args: str, timeout: int = 120) -> str:
    cmd = ["git", "-C", str(repo), "-c", "core.autocrlf=false", "-c", f"core.hooksPath={repo / '.git' / 'nexus-no-hooks'}",
           "-c", "credential.interactive=never", *args]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=git_env(), stdin=subprocess.DEVNULL)
    if r.returncode != 0:
        err = (r.stderr or "").lower()
        if "authentication" in err or "could not read username" in err or "403" in err or "terminal prompts disabled" in err:
            raise MirrorBlocked("AUTH_BLOCKED (ID01: git credential onboarding in foreground)")
        raise MirrorBlocked(f"GIT_FAILED {' '.join(args[:2])}: {(r.stderr or r.stdout).strip()[:300]}")
    return r.stdout.strip()


def run_mirror(cfg: dict, expand) -> dict:
    gm = cfg.get("git_mirror", {})
    if not gm.get("enabled"):
        return {"status": "DISABLED"}
    clone, approved = expand(gm["clone_dir"]), expand(gm["approved_dir"])
    branch, remote_url = gm.get("branch", "review/local-export"), gm["remote_url"]
    subdir = gm.get("repo_subdir", "local_exports")
    if not BRANCH_RE.match(branch):
        raise MirrorBlocked("BRANCH_NOT_ALLOWED (must be review/...)")
    if not approved or not approved.is_dir():
        return {"status": "BLOCKED", "reason": "APPROVED_DIR_MISSING"}
    if not (clone / ".git").is_dir():
        raise MirrorBlocked("CLONE_MISSING (Install-NexusLocal.ps1 -SetupMirror)")
    if git(clone, "remote", "get-url", "origin") != remote_url:
        raise MirrorBlocked("ORIGIN_MISMATCH")
    if git(clone, "status", "--porcelain"):
        raise MirrorBlocked("CLONE_DIRTY (manual inspection required, nothing reset)")
    git(clone, "fetch", "--no-tags", "origin", f"+refs/heads/{gm.get('base', 'main')}:refs/remotes/origin/{gm.get('base', 'main')}")
    remote_head = subprocess.run(["git", "-C", str(clone), "ls-remote", "--heads", "origin", branch], capture_output=True,
                                 text=True, timeout=60, env=git_env(), stdin=subprocess.DEVNULL).stdout.split()
    if remote_head:
        git(clone, "fetch", "--no-tags", "origin", f"refs/heads/{branch}:refs/remotes/origin/{branch}")
        base = f"origin/{branch}"
    else:
        base = f"origin/{gm.get('base', 'main')}"
    git(clone, "checkout", "-q", "-B", branch, base)
    if git(clone, "rev-parse", "--abbrev-ref", "HEAD") != branch:
        raise MirrorBlocked("WRONG_BRANCH_AFTER_CHECKOUT")
    staged: list[dict] = []
    for p in sorted(approved.rglob("*")):
        if not p.is_file() or p.is_symlink():
            continue
        rel = p.relative_to(approved).as_posix()
        import fnmatch
        if unsafe_rel(rel) or any(fnmatch.fnmatch(p.name.lower(), x.lower()) for x in DEFAULT_EXCLUDE_FILES):
            continue
        dest = clone / subdir / rel
        src_sha = sha256_file(p)
        if dest.is_file() and sha256_file(dest) == src_sha:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, dest)
        staged.append({"rel": f"{subdir}/{rel}", "sha256": src_sha})
    if not staged:
        return {"status": "NOTHING_TO_PUBLISH", "branch": branch, "head": git(clone, "rev-parse", "HEAD")}
    for s in staged:
        git(clone, "add", "--", s["rel"])
    names = set(git(clone, "diff", "--cached", "--name-only").splitlines())
    if names != {s["rel"] for s in staged}:
        raise MirrorBlocked("UNEXPECTED_STAGED_PATHS")
    for s in staged:  # staged blob must equal source bytes (no filters/CRLF transforms)
        blob = subprocess.run(["git", "-C", str(clone), "cat-file", "blob", f":{s['rel']}"], capture_output=True,
                              timeout=30, env=git_env(), stdin=subprocess.DEVNULL).stdout
        if sha256_bytes(blob) != s["sha256"]:
            raise MirrorBlocked(f"BLOB_HASH_MISMATCH {s['rel']}")
    git(clone, "commit", "-q", "--no-verify", "-m", f"local export snapshot {iso()} ({len(staged)} files)\n\n"
        "Source: EXPORT-APPROVED folder (ID01). Review snapshot only, not an approval.")
    head = git(clone, "rev-parse", "HEAD")
    out = subprocess.run(["git", "-C", str(clone), "push", "--porcelain", "origin", f"HEAD:refs/heads/{branch}"],
                         capture_output=True, text=True, timeout=180, env=git_env(), stdin=subprocess.DEVNULL)
    if out.returncode != 0:
        status = "NON_FAST_FORWARD_BLOCKED" if "rejected" in (out.stdout + out.stderr) else "PUSH_FAILED"
        return {"status": status, "local_head": head, "detail": (out.stderr or out.stdout)[-300:]}
    remote = subprocess.run(["git", "-C", str(clone), "ls-remote", "origin", f"refs/heads/{branch}"], capture_output=True,
                            text=True, timeout=60, env=git_env(), stdin=subprocess.DEVNULL).stdout.split()
    verified = bool(remote) and remote[0] == head
    return {"status": "PUSHED_REVIEW_PENDING" if verified else "PUSHED_UNVERIFIED", "branch": branch,
            "head": head, "files": staged}
