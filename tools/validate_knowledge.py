#!/usr/bin/env python3
"""Validate knowledge items (registry/knowledge/**/*.json) against the schema and sign-off binding rules."""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import jsonschema

SCHEMA = Path(__file__).resolve().parents[1] / "schemas" / "knowledge-item.schema.json"


def _is_aware_timestamp(value: Any) -> bool:
    """ISO 8601 with explicit timezone; independent of optional format-checker plugins."""
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).tzinfo is not None
    except (ValueError, TypeError):
        return False


def validate_item(item: Any, schema: dict) -> list[str]:
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    errors = [e.message for e in validator.iter_errors(item)]
    if errors or not isinstance(item, dict):
        return errors
    signoff = item.get("signoff")
    if isinstance(signoff, dict):
        if signoff.get("result_version") != item.get("version"):
            errors.append("signoff.result_version does not match item version (sign-off is stale)")
        if not _is_aware_timestamp(signoff.get("decided_at")):
            errors.append("signoff.decided_at must be an ISO 8601 timestamp with timezone")
    return errors


def knowledge_files(directory: Path) -> list[Path]:
    """All *.json files below the directory, including subfolders, in a stable order."""
    if not directory.is_dir():
        return []
    return sorted(path for path in directory.rglob("*.json") if path.is_file())


def validate_dir(directory: Path) -> list[str]:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors: list[str] = []
    for path in knowledge_files(directory):
        label = path.relative_to(directory).as_posix()
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{label}: unreadable: {exc}")
            continue
        errors += [f"{label}: {m}" for m in validate_item(item, schema)]
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", type=Path, default=Path("registry/knowledge"))
    parser.add_argument("--allow-empty", action="store_true",
                        help="Allow an unpopulated inventory; still report NO_DATA, never PASS")
    args = parser.parse_args()
    if not args.dir.exists() or (args.dir.is_dir() and not knowledge_files(args.dir)):
        print("Knowledge validation: NO_DATA (no knowledge items evaluated)")
        return 0 if args.allow_empty else 2
    if not args.dir.is_dir():
        print("Knowledge validation: FAIL (input path is not a directory)")
        return 1
    errors = validate_dir(args.dir)
    if errors:
        print("Knowledge validation: FAIL")
        for e in errors:
            print(f"- {e}")
        return 1
    print("Knowledge validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
