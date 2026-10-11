#!/usr/bin/env python3
"""Mark byte-identical registry entries and write a deterministic report."""
from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def write_jsonl_atomic(records: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as stream:
        for record in records:
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    os.replace(temporary, path)


def write_text_atomic(content: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8", newline="\n")
    os.replace(temporary, path)


def mark_duplicates(records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], str]:
    ordered = sorted(records, key=lambda item: (item.get("root", ""), item.get("path", ""), item.get("id", "")))
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in ordered:
        record.pop("duplicate_of", None)
        record.pop("duplicate_group", None)
        digest = record.get("sha256")
        if record.get("status") == "FOUND" and isinstance(digest, str) and len(digest) == 64:
            groups[digest.lower()].append(record)

    duplicate_groups = [(digest, group) for digest, group in sorted(groups.items()) if len(group) > 1]
    report = [
        "# Duplicate candidates",
        "",
        "Groups are ordered by SHA-256; canonical records are ordered by root, path, and id.",
        "Candidates cover only indexed records; an empty result does not establish that unavailable sources contain no duplicates.",
        "",
    ]
    if not duplicate_groups:
        report.append("No duplicate candidates were found in the available registry records.")
    for digest, group in duplicate_groups:
        canonical = group[0]
        group_id = f"sha256:{digest}"
        report.extend((f"## {group_id}", "", f"Canonical: `{canonical.get('root')}/{canonical.get('path')}` (`{canonical.get('id')}`)", ""))
        for record in group:
            record["duplicate_group"] = group_id
            if record is not canonical:
                record["duplicate_of"] = canonical.get("id")
            report.append(f"- `{record.get('root')}/{record.get('path')}` (`{record.get('id')}`)")
        report.append("")
    return ordered, "\n".join(report).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=Path("registry/file-registry.jsonl"))
    parser.add_argument("--report", type=Path, default=Path("registry/duplicates-report.md"))
    args = parser.parse_args()
    records, report = mark_duplicates(read_jsonl(args.registry))
    report += (
        "\n## Reproducibility\n\n"
        f"Tool: detect_duplicates.py v1; Python {sys.version.split()[0]}\n\n"
        f"Command: `{shlex.join([sys.executable, *sys.argv])}`\n"
    )
    write_jsonl_atomic(records, args.registry)
    write_text_atomic(report, args.report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
