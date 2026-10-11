#!/usr/bin/env python3
"""Validate inventory registry structure and measured coverage calculations."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from coverage_stats import COUNT_FIELDS, SOURCE_NAMES

REQUIRED_FIELDS = {"id", "root", "path", "name", "ext", "size", "mtime", "sha256", "status"}
VALID_STATUSES = {"FOUND", "SKIPPED", "ERROR", "INCOMPLETE"}


def validate_registry(registry_path: Path, coverage_path: Path) -> list[str]:
    errors: list[str] = []
    records: list[dict[str, Any]] = []
    try:
        with registry_path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    errors.append(f"line {line_number}: blank JSONL lines are not allowed")
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    errors.append(f"line {line_number}: invalid JSON: {exc.msg}")
                    continue
                if not isinstance(record, dict):
                    errors.append(f"line {line_number}: record must be a JSON object")
                    continue
                records.append(record)
                missing = REQUIRED_FIELDS - record.keys()
                if missing:
                    errors.append(f"line {line_number}: missing fields: {', '.join(sorted(missing))}")
                    continue
                if not isinstance(record["id"], str) or not re.fullmatch(r"[0-9a-f]{16}", record["id"]):
                    errors.append(f"line {line_number}: id must be 16 lowercase hexadecimal characters")
                elif isinstance(record["root"], str) and isinstance(record["path"], str):
                    expected_id = hashlib.sha256(f"{record['root']}/{record['path']}".encode("utf-8")).hexdigest()[:16]
                    if record["id"] != expected_id:
                        errors.append(f"line {line_number}: id does not match SHA-256(root/path)[:16]")
                if not isinstance(record["size"], int) or isinstance(record["size"], bool) or record["size"] < 0:
                    errors.append(f"line {line_number}: size must be a non-negative integer")
                if not isinstance(record["status"], str) or record["status"] not in VALID_STATUSES:
                    errors.append(f"line {line_number}: invalid status {record['status']!r}")
                if record["root"] not in SOURCE_NAMES:
                    errors.append(f"line {line_number}: unknown source root {record['root']!r}")
                digest = record["sha256"]
                if digest is not None and (not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest)):
                    errors.append(f"line {line_number}: sha256 must be null or 64 lowercase hexadecimal characters")
                try:
                    datetime.fromisoformat(record["mtime"].replace("Z", "+00:00"))
                except (AttributeError, TypeError, ValueError):
                    errors.append(f"line {line_number}: mtime must be an ISO 8601 timestamp")
                if not all(isinstance(record[field], str) for field in ("root", "path", "name", "ext", "mtime")):
                    errors.append(f"line {line_number}: root, path, name, ext, and mtime must be strings")
        ids = [record.get("id") for record in records if isinstance(record.get("id"), str)]
        if len(ids) != len(set(ids)):
            errors.append("registry contains duplicate ids")
    except OSError as exc:
        return [f"cannot read registry: {exc}"]

    try:
        coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return errors + [f"cannot read coverage report: {exc}"]
    if not isinstance(coverage, dict):
        return errors + ["coverage report must be an object"]
    if coverage.get("formula") != "indexed / accessible":
        errors.append("coverage formula must be 'indexed / accessible'")
    sources = coverage.get("sources")
    if not isinstance(sources, dict):
        return errors + ["coverage sources must be an object"]
    for name in SOURCE_NAMES:
        source = sources.get(name)
        if not isinstance(source, dict):
            errors.append(f"{name}: missing coverage entry")
            continue
        if source.get("status") == "INCOMPLETE":
            if not source.get("reason"):
                errors.append(f"{name}: INCOMPLETE source must include a reason")
            if any(source.get(field) is not None for field in (*COUNT_FIELDS, "coverage_percent")):
                errors.append(f"{name}: INCOMPLETE metrics must be null, not guessed")
        elif source.get("status") == "COMPLETE":
            values = [source.get(field) for field in COUNT_FIELDS]
            if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in values):
                errors.append(f"{name}: COMPLETE source counts must be non-negative integers")
                continue
            if not (
                source["indexed"] <= source["accessible"] <= source["discovered"]
                and source["skipped"] <= source["accessible"]
                and source["error"] <= source["discovered"]
            ):
                errors.append(f"{name}: source counts are inconsistent")
            expected = source["indexed"] / source["accessible"] * 100 if source["accessible"] else None
            actual = source.get("coverage_percent")
            if (expected is not None and (not isinstance(actual, (int, float)) or isinstance(actual, bool))) or actual != expected:
                errors.append(f"{name}: coverage_percent does not match indexed / accessible")
        else:
            errors.append(f"{name}: status must be COMPLETE or INCOMPLETE")

    total = coverage.get("total")
    if not isinstance(total, dict):
        errors.append("coverage total must be an object")
    elif any(source.get("status") == "INCOMPLETE" for source in sources.values()):
        if total.get("status") != "INCOMPLETE":
            errors.append("total must be INCOMPLETE when any source is INCOMPLETE")
        elif any(total.get(field) is not None for field in (*COUNT_FIELDS, "coverage_percent")):
            errors.append("INCOMPLETE total metrics must be null, not guessed")
    elif total.get("status") == "COMPLETE":
        values = [total.get(field) for field in COUNT_FIELDS]
        if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in values):
            errors.append("COMPLETE total counts must be non-negative integers")
        else:
            if not (
                total["indexed"] <= total["accessible"] <= total["discovered"]
                and total["skipped"] <= total["accessible"]
                and total["error"] <= total["discovered"]
            ):
                errors.append("total counts are inconsistent")
            expected = total["indexed"] / total["accessible"] * 100 if total["accessible"] else None
            actual = total.get("coverage_percent")
            if (expected is not None and (not isinstance(actual, (int, float)) or isinstance(actual, bool))) or actual != expected:
                errors.append("total coverage_percent does not match indexed / accessible")
    else:
        errors.append("total status must be COMPLETE or INCOMPLETE")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=Path("registry/file-registry.jsonl"))
    parser.add_argument("--coverage", type=Path, default=Path("registry/coverage-per-source.json"))
    args = parser.parse_args()
    errors = validate_registry(args.registry, args.coverage)
    if errors:
        print("Inventory validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Inventory validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
