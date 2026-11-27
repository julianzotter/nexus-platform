#!/usr/bin/env python3
"""Build the Control Panel data file (control-data.json) from repository sources.

Deterministic: same commit + same inputs -> same bytes (no wall-clock fields).
Manual sections (projects, orders, architecture, moe, chatTasks, computerJobs,
navigation, reports) come from apps/control-panel/data/control-data.base.json.
Generated sections:
  roles  <- registry/roles/role_capability_matrix.json (replaces the manual list)
  nexus  <- orchestrator/registry/workflow-registry.json, skills/**/SKILL.md
            (tools/skill_inventory.py), governance/work-snapshot/00_ID_LEDGER.csv,
            registry/ui-surfaces.json, git ls-tree/log at the commit (repoStats),
            reports/monitor/nexus.snapshot.json (tools/export_dashboard.py, optional)
Never fabricates approval: a missing monitor snapshot is reported as NO_DATA.

Usage: python tools/build_control_data.py --source-commit "$GITHUB_SHA" [--out apps/control-panel/dist]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from collections import Counter
from pathlib import Path
from typing import Any

import jsonschema

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_inventory import build_report as build_skill_report  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PANEL = Path("apps/control-panel")
BASE = PANEL / "data/control-data.base.json"
SITE = PANEL / "site"
SCHEMA = Path("schemas/control-data.schema.json")
ROLES = Path("registry/roles/role_capability_matrix.json")
WORKFLOWS = Path("orchestrator/registry/workflow-registry.json")
LEDGER = Path("governance/work-snapshot/00_ID_LEDGER.csv")
SNAPSHOT = Path("reports/monitor/nexus.snapshot.json")
SURFACES = Path("registry/ui-surfaces.json")
REPORT_DIRS = (Path("reports"), Path("WORK/REPORTS"))
# Rule YY_MM_DD_HHMM_ID##_THEMA_### (governance/current/_AGBS.md, AGENTS.md item 4); ### from the ID ledger.
REPORT_NAME = re.compile(r"^(\d\d)_(\d\d)_(\d\d)_(\d{4})_(ID\d\d)_(.+?)_(\d{3,4}|LEDGER-PENDING|UNREGISTERED)\.[a-z0-9]+$")
SCHEMA_VERSION = "4.2.0"
LEDGER_LATEST = 15
# ANNAHME: Abbildung Matrix-Status -> Panel-Badge (Panel kennt OWNER/ACTIVE/AVAILABLE/UNASSIGNED).
ROLE_STATUS = {"ACTIVE": "ACTIVE", "OPTIONAL": "AVAILABLE", "INACTIVE": "UNASSIGNED"}
CAPS = (("drive_read", "Drive-R"), ("drive_write", "Drive-W"), ("github_read", "GH-R"),
        ("github_write", "GH-W"), ("merge", "Merge"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def commit_time(root: Path, commit: str) -> str:
    """Committer time of the source commit (UTC, Z) - deterministic asOf."""
    out = subprocess.run(["git", "-C", str(root), "show", "-s", "--format=%ct", commit],
                         check=True, capture_output=True, text=True).stdout.strip()
    return datetime.fromtimestamp(int(out), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_roles(matrix: dict[str, Any]) -> list[list[str]]:
    """Panel tuple: [id, actor, function, capabilities, badge]."""
    rows = []
    for role in matrix["roles"]:
        caps = " · ".join(f"{label} {role[key]}" for key, label in CAPS)
        badge = "OWNER" if role["id"] == "ID01" else ROLE_STATUS.get(role["status"], "UNKNOWN")
        rows.append([role["id"], role["actor"], role["function"], caps, badge])
    return rows


def build_workflows(registry: dict[str, Any]) -> dict[str, Any]:
    flows = [[w["id"], w["name"], w["route"], w["source"]] for w in registry["workflows"]]
    ids = [row[0] for row in flows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate workflow IDs")
    return {"version": registry["version"], "pipeline": registry["pipeline"],
            "ssot": registry["ssot"], "items": flows}


def build_skills(root: Path) -> dict[str, Any]:
    report = build_skill_report(root)
    items = [[p.get("id") or Path(p["path"]).parent.name, p["package_kind"], p["status"], p.get("version") or "UNKNOWN", p["path"]]
             for p in report["packages"]]
    return {"counts": report["counts"], "duplicateIds": report["duplicate_ids"],
            "scope": report["scope"], "items": items}


def build_ledger(path: Path) -> dict[str, Any]:
    rows = list(csv.DictReader(path.read_text(encoding="utf-8").splitlines()))
    ids = [r["ID"] for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate ledger IDs")
    numeric = [int(i) for i in ids if i.isdigit()]
    latest = sorted(rows, key=lambda r: (r["DATE"], r["ID"]))[-LEDGER_LATEST:][::-1]
    return {"entries": len(rows), "nextFreeId": f"{max(numeric) + 1:04d}" if numeric else "UNKNOWN",
            "lastDate": max(r["DATE"] for r in rows),
            "byValidity": dict(sorted(Counter(r["VALIDITY"] or "EMPTY" for r in rows).items())),
            "byMaturity": dict(sorted(Counter(r["MATURITY"] or "EMPTY" for r in rows).items())),
            "latest": [[r["ID"], r["DATE"], r["TYPE"], r["TITLE"], r["ACTOR"], r["MATURITY"]] for r in latest]}


def classify_report(name: str, ledger_ids: set[str]) -> tuple[str, str, str]:
    """-> (date, role, state); state in REGISTERED, NOT_IN_LEDGER, LEDGER_PENDING, UNREGISTERED, NAME_NONCONFORM."""
    m = REPORT_NAME.match(name)
    if not m:
        return "", "", "NAME_NONCONFORM"
    date, role, suffix = f"20{m[1]}-{m[2]}-{m[3]}", m[5], m[7]
    if suffix.isdigit():
        return date, role, "REGISTERED" if suffix.zfill(4) in ledger_ids else "NOT_IN_LEDGER"
    return date, role, suffix.replace("-", "_")


def build_report_files(root: Path, ledger_path: Path) -> dict[str, Any]:
    """Report files in reports/ and WORK/REPORTS checked against the naming rule and the ID ledger."""
    ledger_ids = {r["ID"] for r in csv.DictReader(ledger_path.read_text(encoding="utf-8").splitlines())}
    items = []
    for base in REPORT_DIRS:
        for path in sorted((root / base).rglob("*")):
            if path.is_file() and re.match(r"^\d\d_\d\d_\d\d_", path.name):
                date, role, state = classify_report(path.name, ledger_ids)
                items.append([path.name, date, role, state, path.relative_to(root).as_posix()])
    items.sort(key=lambda row: (row[1], row[0]), reverse=True)
    return {"rule": "YY_MM_DD_HHMM_ID##_THEMA_###", "entries": len(items),
            "byState": dict(sorted(Counter(row[3] for row in items).items())), "items": items}


def build_surfaces(registry: dict[str, Any]) -> dict[str, Any]:
    """UI surfaces (registry/ui-surfaces.json, gated by tools/check_ui_surfaces.py)."""
    items = [[s["id"], s["role"], s["title"], s["owner"], s["status"], s.get("consolidation_target") or "–", s["path"]]
             for s in registry["surfaces"]]
    return {"version": registry["version"], "rule": registry["rule"],
            "byRole": dict(sorted(Counter(i[1] for i in items).items())), "items": items}


def git_out(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), "-c", "core.quotepath=off", *args], check=True,
                          capture_output=True, text=True, encoding="utf-8").stdout


def build_repo_stats(root: Path, commit: str) -> dict[str, Any]:
    """Repository KPIs at the source commit (adopted from archived data dashboard, UI-05).

    Only git ls-tree / git log at a fixed commit -> deterministic.
    """
    folders: Counter[str] = Counter()
    types: Counter[str] = Counter()
    size = 0
    for line in git_out(root, "ls-tree", "-r", "-l", commit).splitlines():
        meta, path = line.split("\t", 1)
        _, kind, _, blob_size = meta.split()
        if kind != "blob":
            continue
        name = path.rsplit("/", 1)[-1]
        folders[path.split("/")[0] if "/" in path else "(root)"] += 1
        types["." + name.rsplit(".", 1)[1].lower() if "." in name.lstrip(".") else "(ohne)"] += 1
        size += int(blob_size)
    log = [row.split("\x1f") for row in git_out(root, "log", commit, "--format=%h\x1f%cI\x1f%P").splitlines()]
    days = Counter(row[1][:10] for row in log)
    last_days = sorted(days)[-14:]
    top = lambda c: [[k, v] for k, v in sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:8]]
    shallow = git_out(root, "rev-parse", "--is-shallow-repository").strip() == "true"
    return {"files": sum(folders.values()), "bytes": size, "commits": len(log), "shallow": shallow,
            "merges": sum(len(row[2].split()) > 1 for row in log), "firstCommit": min(days) if days else None,
            "byFolder": top(folders), "byType": top(types), "commitsPerDay": [[d, days[d]] for d in last_days]}


def build_monitor(path: Path, commit: str) -> dict[str, Any]:
    if not path.exists():
        return {"status": "NO_DATA", "detail": "Kein Snapshot (tools/export_dashboard.py) in diesem Lauf."}
    snap = json.loads(path.read_text(encoding="utf-8"))
    status = snap["monitor"]["status"] if snap.get("source_commit") == commit else "STALE_COMMIT"
    return {"status": status, "checks": snap["monitor"]["checks"], "observedAt": snap["observed_at"],
            "runId": snap["monitor"]["run_id"], "sourceCommit": snap["source_commit"],
            "nodes": len(snap.get("nodes", [])), "delivery": snap.get("delivery"),
            "consumerAck": snap.get("consumer_ack"), "humanAcceptance": snap.get("human_acceptance")}


def build(root: Path, commit: str, snapshot: Path) -> dict[str, Any]:
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("source commit must be 40 hex")
    data = json.loads((root / BASE).read_text(encoding="utf-8"))
    inputs = [BASE, ROLES, WORKFLOWS, LEDGER, SURFACES] + ([snapshot] if (root / snapshot).exists() else [])
    data["schemaVersion"] = SCHEMA_VERSION
    data["asOf"] = commit_time(root, commit)
    data["roles"] = build_roles(json.loads((root / ROLES).read_text(encoding="utf-8")))
    data["nexus"] = {
        "sourceCommit": commit, "repository": "julianzotter/nexus-platform",
        "inputs": [[p.as_posix(), sha256_file(root / p)] for p in inputs],
        "workflows": build_workflows(json.loads((root / WORKFLOWS).read_text(encoding="utf-8"))),
        "skills": build_skills(root), "ledger": build_ledger(root / LEDGER),
        "reportFiles": build_report_files(root, root / LEDGER),
        "repoStats": build_repo_stats(root, commit),
        "surfaces": build_surfaces(json.loads((root / SURFACES).read_text(encoding="utf-8"))),
        "monitor": build_monitor(root / snapshot, commit)}
    schema = json.loads((root / SCHEMA).read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(data)
    return data


def write_dist(root: Path, data: dict[str, Any], out: Path) -> Path:
    """Copy the static site and add control-data.json (+ .sha256) -> deployable dist/."""
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(root / SITE, out)
    raw = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    (out / "control-data.json").write_bytes(raw)
    (out / "control-data.json.sha256").write_text(hashlib.sha256(raw).hexdigest() + "\n", encoding="utf-8")
    return out / "control-data.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--snapshot", type=Path, default=SNAPSHOT)
    parser.add_argument("--out", type=Path, default=ROOT / PANEL / "dist")
    args = parser.parse_args(argv)
    try:
        data = build(args.root, args.source_commit, args.snapshot)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError, jsonschema.ValidationError) as exc:
        print(f"Control data build: FAIL ({type(exc).__name__}: {exc})")
        return 1
    path = write_dist(args.root, data, args.out)
    n = data["nexus"]
    print(f"Control data build: {path} · WF {len(n['workflows']['items'])} · skills {len(n['skills']['items'])}"
          f" · roles {len(data['roles'])} · ledger {n['ledger']['entries']} · monitor {n['monitor']['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
