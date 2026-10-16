#!/usr/bin/env python3
"""Generate registry/catalog-draft.yaml (Status = DRAFT) from the measured coverage report."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


def render_catalog(coverage: dict[str, Any], coverage_name: str) -> str:
    lines = [
        "Status: DRAFT",
        f"coverage_formula: {coverage['formula']}",
        f"coverage_report: {coverage_name}",
        "sources:",
    ]
    for name, source in coverage["sources"].items():
        lines.append(f"  - name: {name}")
        lines.append(f"    status: {source['status']}")
        if source["status"] == "INCOMPLETE":
            lines.append(f"    reason: {source.get('reason') or 'unknown'}")
        else:
            lines.append(f"    coverage_percent: {source['coverage_percent']}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coverage", type=Path, default=Path("registry/coverage-per-source.json"))
    parser.add_argument("--output", type=Path, default=Path("registry/catalog-draft.yaml"))
    args = parser.parse_args()
    coverage = json.loads(args.coverage.read_text(encoding="utf-8"))
    content = render_catalog(coverage, args.coverage.name)
    tmp = args.output.with_suffix(args.output.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    os.replace(tmp, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
