"""Render registry/roles/role_capability_matrix.json as a Markdown table.

Usage: python tools/render_role_matrix.py [--check]
--check exits 1 if the committed Markdown differs from the rendering.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "registry" / "roles" / "role_capability_matrix.json"
OUT = ROOT / "registry" / "roles" / "ROLE_CAPABILITY_MATRIX.md"
COLS = ["drive_read", "drive_write", "github_read", "github_write", "merge"]


def render(data: dict) -> str:
    a = data["role_authority"]
    lines = [
        f"# NEXUS Role-ID Capability Matrix ({data['role_register_version']})",
        "",
        f"Generated from `{SRC.relative_to(ROOT).as_posix()}` - do not edit by hand.",
        f"Status {data['status']} - as of {data['as_of']} - author {data['author']}.",
        f"Role authority: {a['source']} (Drive `{a['drive_id']}`, sha256 `{a['sha256'][:16]}`).",
        "",
        data["note"],
        "",
        "| ID | Actor | Function | Status | " + " | ".join(COLS) + " | Evidence |",
        "|" + "---|" * (len(COLS) + 5),
    ]
    for r in data["roles"]:
        caps = " | ".join(r[c] for c in COLS)
        lines.append(f"| {r['id']} | {r['actor']} | {r['function']} | {r['status']} | {caps} | {r['evidence']} |")
    lines += ["", "Invalid IDs: " + ", ".join(f"{k} ({v})" for k, v in data["invalid_ids"].items()), "",
              "## Runtimes without role ID", ""]
    lines += [f"- {x['runtime']}: {x['rule']}" for x in data["runtimes_without_role_id"]]
    lines += ["", "## Legend", ""] + [f"- {k}: {v}" for k, v in data["legend"].items()]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    text = render(json.loads(SRC.read_text(encoding="utf-8")))
    if "--check" in argv:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != text:
            print("ROLE_CAPABILITY_MATRIX.md is out of date; run tools/render_role_matrix.py")
            return 1
        return 0
    OUT.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
