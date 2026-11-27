#!/usr/bin/env python3
"""CI gate for the report file rule YY_MM_DD_HHMM_ID##_THEMA_### (_AGBS.md, AGENTS.md item 4).

Reuses name_check() from local_stack/nexus_local/naming.py and adds a role-ID check against
registry/roles/role_capability_matrix.json (NEXUS-ROLES-v1.2; ID93 and unknown IDs fail).

Usage:
  python tools/naming_gate.py --base origin/main        # gate: files added/renamed since base
  python tools/naming_gate.py --all [--plan OUT.md]      # inventory of the whole tree (report only)
  python tools/naming_gate.py --strict ...               # LEDGER-PENDING/UNREGISTERED also fail

Artifact numbers come only from the ID ledger (_AGBS.md); this tool never proposes numbers.
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "registry" / "roles" / "role_capability_matrix.json"
NAMING = ROOT / "local_stack" / "nexus_local" / "naming.py"
DATE_PREFIX = re.compile(r"^(\d\d_\d\d_\d\d_|\d{4}-\d\d-\d\d[_ ])")
REPORT_DIRS = ("WORK/", "reports/", "docs/reports/")
EXEMPT = {"README.md", "Folder.md", "LICENSE"}
PASS = {"konform", "Steuerdatei", "ueberholt"}
OPEN = {"Nummer offen"}


def _naming():
    spec = importlib.util.spec_from_file_location("nexus_naming", NAMING)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def valid_ids() -> set[str]:
    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    return {r["id"] for r in data["roles"] if r["status"] != "INACTIVE"}


def is_candidate(path: str) -> bool:
    """Report-like files the rule applies to: date-prefixed names or .md/.json in report folders."""
    name = path.rsplit("/", 1)[-1]
    if name in EXEMPT or name.startswith("_") or name.startswith("."):
        return False
    if DATE_PREFIX.match(name):
        return True
    return path.startswith(REPORT_DIRS) and name.endswith((".md", ".json"))


def judge(path: str, ids: set[str], check=None) -> tuple[str, str]:
    """Verdict for one path: (verdict, reason). Adds role-ID validation to name_check."""
    check = check or _naming().name_check
    name = path.rsplit("/", 1)[-1]
    verdict, reason = check(name)
    m = re.match(r"^\d\d_\d\d_\d\d_\d{4}_(ID\d\d)_", name)
    if m and m.group(1) not in ids and verdict in PASS | OPEN:
        return "Verstoss", f"Rollen-ID {m.group(1)} nicht in NEXUS-ROLES-v1.2 (aktiv)"
    return verdict, reason


def new_names(name_status: str) -> list[str]:
    """Added files, and renamed files whose file name changed. A pure folder move
    (e.g. into archive/) keeps the reviewed historical name and is not a new artifact."""
    paths = []
    for line in name_status.splitlines():
        parts = line.split("\t")
        if parts[0] == "A":
            paths.append(parts[1])
        elif parts[0].startswith("R") and parts[1].rsplit("/", 1)[-1] != parts[2].rsplit("/", 1)[-1]:
            paths.append(parts[2])
    return paths


def added_since(base: str) -> list[str]:
    cmd = ["git", "-c", "core.quotepath=off", "diff", "--name-status", "--find-renames", "--diff-filter=AR", f"{base}...HEAD"]
    out = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return new_names(out)


def tracked() -> list[str]:
    out = subprocess.run(["git", "-c", "core.quotepath=off", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return out.splitlines()


def evaluate(paths: list[str], strict: bool) -> tuple[list[tuple[str, str, str]], int]:
    ids, check = valid_ids(), _naming().name_check
    rows = [(p, *judge(p, ids, check)) for p in paths if is_candidate(p)]
    ok = PASS if strict else PASS | OPEN
    return rows, sum(1 for r in rows if r[1] not in ok)


def fix_hint(path: str) -> str:
    """Required change for an open/unverified name; never invents an ID or artifact number."""
    name = path.rsplit("/", 1)[-1]
    todo = []
    if "ID-UNVERIFIED" in name or not re.search(r"_\d{4}_ID\d\d_", name):
        todo.append("Rollen-ID aus Frontmatter/Commit belegen (ID01)")
    if re.search(r"_(LEDGER-PENDING|UNREGISTERED)(\.[A-Za-z0-9]+)?$", name):
        todo.append("Artefaktnummer ### aus ID-Ledger")
    if re.match(r"^\d\d_\d\d_\d\d_\d\d_\d\d_", name):
        todo.append("HH_MM -> HHMM")
    return "; ".join(todo) or "pruefen"


def plan(rows: list[tuple[str, str, str]]) -> str:
    """Markdown renumbering plan for files with open number or unverified role ID."""
    hits = [r for r in rows if "LEDGER-PENDING" in r[0] or "UNREGISTERED" in r[0] or "ID-UNVERIFIED" in r[0]]
    lines = ["| # | Datei | Urteil | Erforderlich |", "|---|---|---|---|"]
    lines += [f"| {i} | `{p}` | {v} | {fix_hint(p)} |" for i, (p, v, _) in enumerate(sorted(hits), 1)]
    return f"Treffer: {len(hits)}\n\n" + "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    strict = "--strict" in argv
    if "--base" in argv:
        rows, bad = evaluate(added_since(argv[argv.index("--base") + 1]), strict)
    else:
        rows, bad = evaluate(tracked(), strict)
    for p, v, why in rows:
        if v not in PASS:
            print(f"{v:13} {p}" + (f"  ({why})" if why else ""))
    if "--plan" in argv:
        Path(argv[argv.index("--plan") + 1]).write_text(plan(rows), encoding="utf-8")
    print(f"naming_gate: {len(rows)} geprueft, {bad} Verstoesse" + (" (strict)" if strict else ""))
    return 1 if bad and "--base" in argv else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
