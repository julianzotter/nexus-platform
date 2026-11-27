#!/usr/bin/env python3
"""Architecture gate: every HTML surface is declared once in registry/ui-surfaces.json.

Rules (fail closed, exit 1):
  R1 every declared path exists and is unique; ids unique (UI-##)
  R2 exactly one CANONICAL_DISPLAY = apps/control-panel/site, exactly one LOCAL_BACKEND
  R3 PROTOTYPE entries name owner and consolidation_target
  R4 every index.html under SCAN_ROOTS lies inside a declared path (no undeclared dashboard)

Usage: python tools/check_ui_surfaces.py [--root .]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = Path("registry/ui-surfaces.json")
CANONICAL = "apps/control-panel/site"
SCAN_ROOTS = ("apps", "prototypes", "local_stack", "docs/dashboards", "archive")
ROLES = {"CANONICAL_DISPLAY", "LOCAL_BACKEND", "PROTOTYPE", "REPORT_VIEW", "TOOL", "ARCHIVED"}
SKIP_PARTS = {"dist", "node_modules", "__pycache__"}  # build output is not a surface


def load(root: Path) -> list[dict[str, Any]]:
    return json.loads((root / REGISTRY).read_text(encoding="utf-8"))["surfaces"]


def declared_errors(root: Path, surfaces: list[dict[str, Any]]) -> list[str]:
    """R1-R3: registry consistency."""
    errors: list[str] = []
    ids = [s["id"] for s in surfaces]
    paths = [s["path"] for s in surfaces]
    for label, values in (("id", ids), ("path", paths)):
        dupes = sorted({v for v in values if values.count(v) > 1})
        if dupes:
            errors.append(f"R1 duplicate {label}: {', '.join(dupes)}")
    for s in surfaces:
        if not re.fullmatch(r"UI-\d\d", s["id"]):
            errors.append(f"R1 bad id: {s['id']}")
        if s["role"] not in ROLES:
            errors.append(f"R1 unknown role {s['role']} ({s['id']})")
        if not (root / s["path"]).is_dir():
            errors.append(f"R1 missing path: {s['path']} ({s['id']})")
        if s["role"] == "PROTOTYPE" and not (s.get("owner") and s.get("consolidation_target")):
            errors.append(f"R3 prototype without owner/consolidation_target: {s['id']}")
    canon = [s["path"] for s in surfaces if s["role"] == "CANONICAL_DISPLAY"]
    if canon != [CANONICAL]:
        errors.append(f"R2 CANONICAL_DISPLAY must be exactly [{CANONICAL}], got {canon}")
    if sum(s["role"] == "LOCAL_BACKEND" for s in surfaces) != 1:
        errors.append("R2 exactly one LOCAL_BACKEND required")
    return errors


def undeclared(root: Path, surfaces: list[dict[str, Any]]) -> list[str]:
    """R4: index.html files outside any declared surface path."""
    declared = [Path(s["path"]) for s in surfaces]
    found: list[str] = []
    for base in SCAN_ROOTS:
        for html in sorted((root / base).rglob("index.html")) if (root / base).is_dir() else []:
            rel = html.relative_to(root)
            if SKIP_PARTS & set(rel.parts):
                continue
            if not any(rel.is_relative_to(d) for d in declared):
                found.append(rel.parent.as_posix())
    return [f"R4 undeclared surface: {p} (add to {REGISTRY.as_posix()})" for p in found]


def check(root: Path) -> list[str]:
    surfaces = load(root)
    return declared_errors(root, surfaces) + undeclared(root, surfaces)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        errors = check(args.root)
    except (OSError, KeyError, ValueError) as exc:
        print(f"UI surface gate: FAIL ({type(exc).__name__}: {exc})")
        return 1
    for line in errors:
        print(line)
    print(f"UI surface gate: {'FAIL' if errors else 'PASS'} ({len(load(args.root))} surfaces)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
