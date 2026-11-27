#!/usr/bin/env python3
"""NEXUS report ID ledger: registry/report-ledger.jsonl (single source for artifact numbers ###).

Rule (_AGBS.md, AGENTS.md item 4): YY_MM_DD_HHMM_ID##_THEMA_###; the number comes only from
this ledger, never from file names. Numbers are global, 4 digits, unique, never reused.

Usage:
  python tools/report_ledger.py check               # CI: schema, uniqueness, paths, unregistered numbers
  python tools/report_ledger.py next                # print next free number (read-only)
  python tools/report_ledger.py allocate --id ID06 --thema STATUSREPORT_X --path <repo path> [--by ID01]
      appends one ALLOCATED entry and prints the number; the caller then names the file with it.

Entries with status IMPORTED record numbers found in file names before the ledger existed
(2026-11-27, ID01 decision in the control-panel thread); they reserve the number, they do not
assign one.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "registry" / "report-ledger.jsonl"
MATRIX = ROOT / "registry" / "roles" / "role_capability_matrix.json"
KEYS = ["nr", "id", "thema", "path", "status", "registered_at", "registered_by", "source"]
STATUSES = {"IMPORTED", "ALLOCATED", "RETIRED"}
NUMBERED = re.compile(r"^\d\d_\d\d_\d\d_\d{4}_(ID\d\d)_(.+)_(\d{4})$")


def load(path: Path = LEDGER) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def role_ids() -> set[str]:
    return {r["id"] for r in json.loads(MATRIX.read_text(encoding="utf-8"))["roles"]}


def next_number(entries: list[dict]) -> str:
    return f"{max((int(e['nr']) for e in entries), default=0) + 1:04d}"


def numbered_files() -> dict[str, str]:
    """Repo paths whose names carry a 4-digit artifact number -> number."""
    out = subprocess.run(["git", "-c", "core.quotepath=off", "ls-files"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout.splitlines()
    found = {}
    for p in out:
        m = NUMBERED.match(re.sub(r"\.[A-Za-z0-9]+$", "", p.rsplit("/", 1)[-1]))
        if m:
            found[p] = m.group(3)
    return found


def entry_errors(i: int, e: dict, ids: set[str]) -> list[str]:
    errs = []
    if list(e) != KEYS:
        errs.append(f"line {i}: keys must be {KEYS}")
        return errs
    if not re.fullmatch(r"\d{4}", e["nr"]):
        errs.append(f"line {i}: nr {e['nr']!r} is not 4 digits")
    if e["id"] not in ids:
        errs.append(f"line {i}: role {e['id']} not in role_capability_matrix.json")
    if e["status"] not in STATUSES:
        errs.append(f"line {i}: status {e['status']!r}")
    if e["status"] != "RETIRED" and not (ROOT / e["path"]).exists():
        errs.append(f"line {i}: path missing {e['path']}")
    return errs


def check(entries: list[dict]) -> list[str]:
    ids, errs, seen = role_ids(), [], {}
    for i, e in enumerate(entries, 1):
        errs += entry_errors(i, e, ids)
        if e.get("nr") in seen:
            errs.append(f"line {i}: nr {e['nr']} already used on line {seen[e['nr']]}")
        seen.setdefault(e.get("nr"), i)
    by_nr = {e["nr"]: e for e in entries if "nr" in e}
    for path, nr in numbered_files().items():
        e = by_nr.get(nr)
        if e is None:
            errs.append(f"unregistered number {nr}: {path}")
        elif e["path"] != path:
            errs.append(f"number {nr} belongs to {e['path']}, also used by {path}")
    return errs


def allocate(role: str, thema: str, path: str, by: str) -> dict:
    entries = load()
    if role not in role_ids():
        raise SystemExit(f"unknown role {role}")
    e = dict(zip(KEYS, [next_number(entries), role, thema, path, "ALLOCATED",
                        datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), by, "report_ledger.py allocate"]))
    with LEDGER.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(e, ensure_ascii=False) + "\n")
    return e


def arg(argv: list[str], name: str, default: str | None = None) -> str:
    if name in argv:
        return argv[argv.index(name) + 1]
    if default is None:
        raise SystemExit(f"missing {name}")
    return default


def main(argv: list[str]) -> int:
    cmd = argv[0] if argv else "check"
    if cmd == "next":
        print(next_number(load()))
        return 0
    if cmd == "allocate":
        print(allocate(arg(argv, "--id"), arg(argv, "--thema"), arg(argv, "--path"), arg(argv, "--by", "ID01"))["nr"])
        return 0
    errs = check(load())
    print("\n".join(errs) if errs else f"report-ledger: {len(load())} entries, OK")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
