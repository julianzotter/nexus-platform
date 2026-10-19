#!/usr/bin/env python3
"""Export a read-only, commit-bound dashboard snapshot; never fabricate approval."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import jsonschema
from validate_knowledge import validate_item

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "julianzotter/nexus-platform"
STATES = {"PASS", "NO_DATA", "INCOMPLETE", "CONFLICT", "UNKNOWN", "ERROR", "FAIL"}


def read_json(path: Path) -> tuple[Any, str]:
    raw = path.read_bytes()
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def project_monitor(report: dict, source_commit: str) -> dict:
    observed = report.get("observed_at", "")
    if not isinstance(observed, str) or not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:\d\d)", observed):
        raise ValueError("Invalid observation timestamp")
    if datetime.fromisoformat(observed.replace("Z", "+00:00")).tzinfo is None:
        raise ValueError("Observation timezone required")
    if report.get("schema_version") != "1.0.0":
        raise ValueError("Unsupported monitor schema")
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit) or report.get("commit") != source_commit:
        raise ValueError("Monitor and registry must use the same source commit")
    checks = report.get("checks")
    if not isinstance(checks, dict) or not {"registry", "knowledge", "coverage", "pull_requests"} <= checks.keys():
        raise ValueError("Missing required monitoring checks")
    states = {key: value["status"] for key, value in checks.items()}
    if any(state not in STATES for state in states.values()):
        raise ValueError("Unknown check state")
    expected = "ATTENTION" if set(states.values()) & {"FAIL", "ERROR", "CONFLICT", "UNKNOWN"} else (
        "INCOMPLETE" if set(states.values()) & {"NO_DATA", "INCOMPLETE"} else "PASS")
    if report.get("status") != expected:
        raise ValueError("Monitor status contradicts its checks")
    return {"status": expected, "checks": states,
            "run_id": str(report["run_id"]), "run_attempt": str(report["run_attempt"])}


def project_nodes(root: Path) -> list[dict]:
    schema, _ = read_json(root / "schemas/knowledge-item.schema.json")
    records = [json.loads(line) for line in (root / "registry/file-registry.jsonl").read_text().splitlines() if line.strip()]
    files = {record["id"]: record for record in records}
    if len(files) != len(records):
        raise ValueError("Duplicate file registry IDs")
    nodes, ids = [], set()
    for path in sorted((root / "registry/knowledge").glob("*.json")):
        item, digest = read_json(path)
        if validate_item(item, schema) or item["id"] in ids:
            raise ValueError(f"Invalid or duplicate knowledge item: {path.name}")
        source = files.get(item["source_file_id"])
        if source is None:
            raise ValueError(f"Unknown source_file_id: {path.name}")
        ids.add(item["id"])
        nodes.append({**{key: item[key] for key in ("id", "kind", "title", "source_file_id", "version", "status")},
                      "source_path": path.relative_to(root).as_posix(), "record_sha256": digest,
                      "source_sha256": source.get("sha256")})
    return nodes


def build_snapshot(root: Path, report_path: Path, source_commit: str) -> dict:
    report, digest = read_json(report_path)
    snapshot = {"schema_version": "nexus-integration/1", "repository": REPOSITORY,
                "source_commit": source_commit, "observed_at": report["observed_at"],
                "generated_at": datetime.now(timezone.utc).isoformat(), "report_sha256": digest,
                "monitor": project_monitor(report, source_commit), "nodes": project_nodes(root),
                "delivery": "NOT_OBSERVED", "consumer_ack": "NOT_OBSERVED", "human_acceptance": "NOT_OBSERVED"}
    schema, _ = read_json(root / "schemas/dashboard-snapshot.schema.json")
    jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(snapshot)
    return snapshot


def write_snapshot(snapshot: dict, output: Path) -> None:
    raw = (json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent, delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    try:
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    output.with_suffix(output.suffix + ".sha256").write_text(hashlib.sha256(raw).hexdigest() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--report", type=Path, default=ROOT / "reports/monitor/report.json")
    parser.add_argument("--output", type=Path, default=ROOT / "reports/monitor/nexus.snapshot.json")
    parser.add_argument("--source-commit", required=True, help="40-hex revision of report AND registry checkout")
    args = parser.parse_args()
    output = args.output.resolve()
    protected = [args.root / name for name in ("registry", "schemas", "tools")]
    if output == args.report.resolve() or any(output.is_relative_to(path.resolve()) for path in protected):
        parser.error("Output must not replace the input report or source files")
    # Never leave a prior successful snapshot at the requested output after a failed export.
    args.output.unlink(missing_ok=True)
    args.output.with_suffix(args.output.suffix + ".sha256").unlink(missing_ok=True)
    try:
        write_snapshot(build_snapshot(args.root, args.report, args.source_commit), args.output)
    except (OSError, ValueError, KeyError, TypeError, AttributeError, jsonschema.ValidationError):
        print("Dashboard export: FAIL (invalid input; no new snapshot)")
        return 1
    print(f"Dashboard export: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
