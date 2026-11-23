#!/usr/bin/env python3
"""Validate METAWISSEN HOLZBAU newsletter Markdown files (structure only, no content judgement).

Exit codes: 0 = all files PASS, 1 = at least one FAIL, 2 = NO_DATA (no files given/found).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

FRONTMATTER_KEYS = ("name", "description", "version", "status", "timestamp", "zeitraum")
SECTIONS = ("## TL;DR", "## QUICK-TOPIC-MATRIX", "## MELDUNGEN", "## TERMINE & FRISTEN",
            "## REFERENZEN", "## LOG")
TOPICS = ("NORM", "TECH", "PROJ", "OEKO", "EVENT", "PUBL", "MARKT")
REF_LINE = re.compile(r"^#(\d+), [^,]+, https?://\S+$")
ITEM_LINE = re.compile(r"^- #(\d+) \[(\w+)\] ")


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Return (frontmatter key/value pairs, body). Empty dict if no frontmatter block."""
    if not text.startswith("---\n"):
        return {}, text
    head, sep, body = text[4:].partition("\n---\n")
    if not sep:
        return {}, text
    pairs = (line.split(":", 1) for line in head.splitlines() if ":" in line)
    return {k.strip(): v.strip() for k, v in pairs}, body


def section(body: str, heading: str) -> str:
    """Return the text of one '## ' section, or '' if the heading is missing."""
    start = body.find(heading + "\n")
    if start < 0:
        return ""
    rest = body[start + len(heading) + 1:]
    end = rest.find("\n## ")
    return rest if end < 0 else rest[:end]


def validate_text(text: str) -> list[str]:
    """Return a list of findings; an empty list means PASS."""
    meta, body = split_frontmatter(text)
    errors = [f"frontmatter key missing: {k}" for k in FRONTMATTER_KEYS if not meta.get(k)]
    errors += [f"section missing: {s}" for s in SECTIONS if not section(body, s)]
    matrix = section(body, "## QUICK-TOPIC-MATRIX")
    errors += [f"matrix row missing: {t}" for t in TOPICS if f"| {t} |" not in matrix]
    refs: set[str] = set()
    for line in section(body, "## REFERENZEN").strip().splitlines():
        match = REF_LINE.match(line.strip())
        if match:
            refs.add(match.group(1))
        else:
            errors.append(f"reference line not '#NR, NAME, URL': {line.strip()[:60]}")
    for line in section(body, "## MELDUNGEN").splitlines():
        match = ITEM_LINE.match(line.strip())
        if not match:
            continue
        if match.group(2) not in TOPICS:
            errors.append(f"item #{match.group(1)}: unknown topic {match.group(2)}")
        if match.group(1) not in refs:
            errors.append(f"item #{match.group(1)}: no reference line")
    return errors


def main(argv: list[str]) -> int:
    files = [p for arg in argv for p in (sorted(Path(arg).rglob("*NEWSLETTER*.md"))
                                         if Path(arg).is_dir() else [Path(arg)])]
    if not files:
        print("NO_DATA: no newsletter files")
        return 2
    failed = 0
    for path in files:
        errors = validate_text(path.read_text(encoding="utf-8"))
        print(f"{'FAIL' if errors else 'PASS'} {path}")
        for error in errors:
            print(f"  - {error}")
        failed += bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
