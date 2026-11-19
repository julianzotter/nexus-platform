"""Read-only DeepSeek Harness / NEXUS Windows preflight.

No DSH configuration, credential, database, MCP or repository writes are made.
An optional JSON report is written only to an explicitly supplied output path.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import sqlite3
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def check(name: str, status: str, evidence: str) -> dict[str, str]:
    return {"check": name, "status": status, "evidence": evidence}


def path_check(name: str, path: Path) -> dict[str, str]:
    status = "PASS" if path.exists() else "BLOCKED"
    return check(name, status, "exists" if path.exists() else "missing")


def profile_inventory(home: Path) -> dict[str, str]:
    profiles = home / "profiles"
    if not profiles.is_dir():
        return check("dsh_profiles", "BLOCKED", "profiles directory missing")
    patches = sorted(profiles.glob("*/cordis.patch.yml"))
    fingerprints = [
        {"profile": p.parent.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
        for p in patches
    ]
    return check("dsh_profiles", "PASS" if patches else "WARN", json.dumps(fingerprints))


def ollama_tags() -> dict[str, str]:
    try:
        with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=4) as reply:
            data = json.load(reply)
        models = data.get("models", [])
        if not isinstance(models, list):
            raise ValueError("models is not an array")
        return check("ollama_endpoint", "PASS", f"models_count={len(models)}")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return check("ollama_endpoint", "BLOCKED", type(exc).__name__)


def ollama_smoke(model: str) -> dict[str, str]:
    payload = json.dumps({
        "model": model,
        "prompt": "Antworte mit einem kurzen OK.",
        "stream": False,
        "options": {"num_predict": 12},
    }).encode("utf-8")
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate", data=payload,
        headers={"Content-Type": "application/json"}, method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=65) as reply:
            result = json.load(reply)
        ok = isinstance(result.get("response"), str) and bool(result["response"].strip())
        return check("ollama_inference", "PASS" if ok else "BLOCKED", "nonempty_text" if ok else "empty_text")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return check("ollama_inference", "BLOCKED", type(exc).__name__)


def sqlite_readonly(path: Path) -> dict[str, str]:
    if not path.is_file():
        return check("sqlite_readonly", "BLOCKED", "database missing")
    try:
        with sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True, timeout=3) as db:
            db.execute("PRAGMA query_only=ON")
            db.execute("SELECT name FROM sqlite_master LIMIT 1").fetchall()
        return check("sqlite_readonly", "PASS", "mode=ro; query_only=ON; metadata SELECT")
    except sqlite3.Error as exc:
        return check("sqlite_readonly", "BLOCKED", type(exc).__name__)


def github_readonly() -> dict[str, str]:
    if not shutil.which("gh"):
        return check("github_cli", "BLOCKED", "gh executable missing")
    try:
        result = subprocess.run(
            ["gh", "api", "repos/julianzotter/nexus-platform", "--jq", ".full_name"],
            capture_output=True, text=True, timeout=15, check=False,
        )
        ok = result.returncode == 0 and result.stdout.strip() == "julianzotter/nexus-platform"
        return check("github_cli", "PASS" if ok else "BLOCKED", "private_repo_read" if ok else "read_failed")
    except (OSError, subprocess.TimeoutExpired) as exc:
        return check("github_cli", "BLOCKED", type(exc).__name__)


def run(args: argparse.Namespace) -> dict[str, Any]:
    home = Path(args.dsh_home or os.environ.get("DSH_HOME") or Path.home() / ".dsh")
    checks = [
        check("windows_host", "PASS" if platform.system() == "Windows" else "BLOCKED", platform.system()),
        check("dsh_executable", "PASS" if shutil.which("dsh") else "BLOCKED", "found" if shutil.which("dsh") else "not_on_PATH"),
        path_check("dsh_home", home),
        profile_inventory(home),
        path_check("nexus_repo", Path(args.repo)),
        path_check("drive_work", Path(args.work)),
        ollama_tags(),
    ]
    if args.sqlite:
        checks.append(sqlite_readonly(Path(args.sqlite)))
    if args.ollama_model:
        checks.append(ollama_smoke(args.ollama_model))
    if args.check_github:
        checks.append(github_readonly())
    checks.append(check("dsh_mcp_session_log_plugins", "NOT_RUN", "requires live DSH UI and isolated synthetic session"))
    return {
        "schema": "nexus.dsh.preflight.v1",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "READ_ONLY_PRECHECK",
        "checks": checks,
        "overall": "BLOCKED" if any(c["status"] == "BLOCKED" for c in checks) else "PARTIAL",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dsh-home", help="Actual Harness home; defaults to DSH_HOME or ~/.dsh")
    parser.add_argument("--repo", default=str(Path.home() / "nexus-platform"))
    parser.add_argument("--work", default=r"G:\Meine Ablage\_developement\LLM-LOCAL-SSOT\WORK")
    parser.add_argument("--sqlite", help="Optional real SQLite file; read-only metadata SELECT")
    parser.add_argument("--ollama-model", help="Explicit installed model for local synthetic inference")
    parser.add_argument("--check-github", action="store_true", help="GitHub CLI read-only private repository check")
    parser.add_argument("--output", type=Path, help="Optional sanitized JSON evidence path")
    args = parser.parse_args()
    result = run(args)
    output = json.dumps(result, ensure_ascii=False, indent=2)
    print(output)
    if args.output:
        if not args.output.parent.is_dir():
            parser.error("--output parent directory must already exist")
        if args.output.exists():
            parser.error("--output must not overwrite an existing report")
        args.output.write_text(output + "\n", encoding="utf-8")
    return 0 if result["overall"] != "BLOCKED" else 2


if __name__ == "__main__":
    sys.exit(main())
