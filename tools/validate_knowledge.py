#!/usr/bin/env python3
"""Validate knowledge items (registry/knowledge/*.json) against the schema and sign-off binding rules."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import jsonschema

SCHEMA = Path(__file__).resolve().parents[1] / "schemas" / "knowledge-item.schema.json"


def validate_item(item: Any, schema: dict) -> list[str]:
    errors = [e.message for e in jsonschema.Draft202012Validator(schema).iter_errors(item)]
    if errors or not isinstance(item, dict):
        return errors
    signoff = item.get("signoff")
    if isinstance(signoff, dict) and signoff.get("result_version") != item.get("version"):
        errors.append("signoff.result_version does not match item version (sign-off is stale)")
    return errors


def validate_dir(directory: Path) -> list[str]:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors: list[str] = []
    for path in sorted(directory.glob("*.json")) if directory.is_dir() else []:
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.name}: unreadable: {exc}")
            continue
        errors += [f"{path.name}: {m}" for m in validate_item(item, schema)]
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", type=Path, default=Path("registry/knowledge"))
    errors = validate_dir(parser.parse_args().dir)
    if errors:
        print("Knowledge validation: FAIL")
        for e in errors:
            print(f"- {e}")
        return 1
    print("Knowledge validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
