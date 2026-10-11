#!/usr/bin/env python3
"""Calculate measured inventory coverage by source from registry JSONL."""
from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

SOURCE_NAMES = (
    "NEXUS-AI-AEC-ENGINEERIN-KNOWLEDGE-GRAPH",
    "julianzotter",
    "Obsidian-Vault",
    "Google Drive",
)
COUNT_FIELDS = ("discovered", "accessible", "indexed", "skipped", "error")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def calculate_coverage(
    records: list[dict[str, Any]],
    incomplete_sources: dict[str, str],
    complete_sources: set[str] | None = None,
) -> dict[str, Any]:
    by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_source[str(record["root"])].append(record)

    complete_sources = complete_sources or set()
    sources: dict[str, dict[str, Any]] = {}
    for source in SOURCE_NAMES:
        source_records = by_source.get(source, [])
        reason = incomplete_sources.get(source)
        if any(record.get("status") == "INCOMPLETE" for record in source_records):
            reason = reason or "One or more discovered files could not be accessed."
        if reason:
            sources[source] = {
                "status": "INCOMPLETE",
                **{field: None for field in COUNT_FIELDS},
                "coverage_percent": None,
                "reason": reason,
            }
            continue

        if not source_records and source not in complete_sources:
            sources[source] = {
                "status": "INCOMPLETE",
                **{field: None for field in COUNT_FIELDS},
                "coverage_percent": None,
                "reason": "Source accessibility was not supplied and no registry records are available.",
            }
            continue

        counts = {
            "discovered": len(source_records),
            "accessible": sum(record.get("status") in ("FOUND", "SKIPPED") for record in source_records),
            "indexed": sum(record.get("status") == "FOUND" for record in source_records),
            "skipped": sum(record.get("status") == "SKIPPED" for record in source_records),
            "error": sum(record.get("status") == "ERROR" for record in source_records),
        }
        coverage = (
            counts["indexed"] / counts["accessible"] * 100
            if counts["accessible"]
            else None
        )
        sources[source] = {
            "status": "COMPLETE",
            **counts,
            "coverage_percent": coverage,
        }

    if any(source["status"] == "INCOMPLETE" for source in sources.values()):
        total = {
            "status": "INCOMPLETE",
            **{field: None for field in COUNT_FIELDS},
            "coverage_percent": None,
        }
    else:
        total_counts = {field: sum(source[field] for source in sources.values()) for field in COUNT_FIELDS}
        total = {
            "status": "COMPLETE",
            **total_counts,
            "coverage_percent": (
                total_counts["indexed"] / total_counts["accessible"] * 100
                if total_counts["accessible"]
                else None
            ),
        }
    return {
        "formula": "indexed / accessible",
        "coverage_unit": "percent",
        "sources": sources,
        "total": total,
    }


def write_json_atomic(value: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def render_summary(stats: dict[str, Any], command: list[str]) -> str:
    lines = ["Inventory coverage (formula: indexed / accessible)"]
    for name, source in stats["sources"].items():
        if source["status"] == "INCOMPLETE":
            lines.append(f"{name}: INCOMPLETE — {source['reason']}")
        else:
            counts = ", ".join(f"{field}={source[field]}" for field in COUNT_FIELDS)
            coverage = source["coverage_percent"]
            shown_coverage = "UNDEFINED (accessible=0)" if coverage is None else f"{coverage:.1f}%"
            lines.append(f"{name}: {counts}, coverage={shown_coverage}")
    total = stats["total"]
    if total["status"] == "INCOMPLETE":
        lines.append("Total: INCOMPLETE (one or more sources are incomplete)")
    else:
        coverage = total["coverage_percent"]
        shown_coverage = "UNDEFINED (accessible=0)" if coverage is None else f"{coverage:.1f}%"
        lines.append(f"Total: indexed={total['indexed']} / accessible={total['accessible']}, coverage={shown_coverage}")
    lines.extend((
        "",
        "Reproducibility",
        f"Tool: coverage_stats.py v1; Python {sys.version.split()[0]}",
        f"Command: {shlex.join(command)}",
    ))
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=Path("registry/file-registry.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("registry/coverage-per-source.json"))
    parser.add_argument("--summary", type=Path, default=Path("registry/inventory-summary.txt"))
    parser.add_argument(
        "--incomplete",
        action="append",
        default=[],
        metavar="SOURCE=REASON",
        help="Mark a source INCOMPLETE because it could not be measured; repeat as needed.",
    )
    parser.add_argument(
        "--complete-source",
        action="append",
        default=[],
        choices=SOURCE_NAMES,
        help="Assert that a source was accessible even if it contains no files; repeat as needed.",
    )
    args = parser.parse_args()
    incomplete = {}
    for item in args.incomplete:
        source, separator, reason = item.partition("=")
        if not separator or source not in SOURCE_NAMES or not reason:
            parser.error(f"invalid --incomplete value: {item}")
        incomplete[source] = reason
    stats = calculate_coverage(read_jsonl(args.registry), incomplete, set(args.complete_source))
    write_json_atomic(stats, args.output)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.summary.with_suffix(args.summary.suffix + ".tmp")
    temporary.write_text(render_summary(stats, [sys.executable, *sys.argv]), encoding="utf-8")
    os.replace(temporary, args.summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
