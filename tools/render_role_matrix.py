"""Render registry/roles/role_capability_matrix.json as a Markdown table.

Usage: python tools/render_role_matrix.py [--check] [--panel CONTROL_DATA_JSON]
--check exits 1 if the committed Markdown or panel roles differ from the rendering.
--panel writes the generated roles into the "roles" key of a Control Panel
        control-data.json (schema 4.1.x) in place; other keys stay untouched.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "registry" / "roles" / "role_capability_matrix.json"
OUT = ROOT / "governance" / "ROLE-ID-CAPABILITY-MATRIX-v1.2.md"
PANEL_OUT = ROOT / "registry" / "roles" / "panel_roles.json"
COLS = ["drive_read", "drive_write", "github_read", "github_write", "merge"]
PANEL_STATUS = {"ACTIVE": "ACTIVE", "OPTIONAL": "AVAILABLE", "INACTIVE": "UNASSIGNED"}


def render(data: dict) -> str:
    a = data["role_authority"]
    lines = [
        f"# NEXUS Role-ID Capability Matrix ({data['role_register_version']})",
        "",
        f"Generated from `{SRC.relative_to(ROOT).as_posix()}` - do not edit by hand.",
        f"Status {data['status']} - as of {data['as_of']} - author {data['author']}.",
        f"Role authority: {a['source']} (`{a['repo_path']}`, Drive `{a['drive_id']}`).",
        "",
        data["note"],
        "",
        "| ID | Actor | Function | Status | " + " | ".join(COLS) + " | Evidence |",
        "|" + "---|" * (len(COLS) + 5),
    ]
    for r in data["roles"]:
        cells = [r["id"], r["actor"], r["function"], r["status"], *(r[c] for c in COLS), r["evidence"]]
        lines.append("| " + " | ".join(str(c).replace("|", "\\|") for c in cells) + " |")
    lines += ["", "Invalid IDs: " + ", ".join(f"{k} ({v})" for k, v in data["invalid_ids"].items()), "",
              "## Runtimes without role ID", ""]
    lines += [f"- {x['runtime']}: {x['rule']}" for x in data["runtimes_without_role_id"]]
    lines += ["", f"Superseded: {data['superseded']}", "", "## Legend", ""] + [f"- {k}: {v}" for k, v in data["legend"].items()]
    return "\n".join(lines) + "\n"


def panel_row(r: dict) -> list[str]:
    """One Control Panel row: [ID, Actor, Function, Capabilities, Status] (5 columns, app.js rolesView)."""
    caps = " · ".join(f"{c}={r[c]}" for c in COLS)
    actor = r["actor"]
    if r["id"] == "ID01":
        status = "OWNER"
    else:
        status = PANEL_STATUS.get(r["status"], "UNKNOWN")
    return [r["id"], actor, r["function"], caps, status]


def panel_roles(data: dict) -> list[list[str]]:
    """Panel 'roles' array derived from the matrix; invalid IDs and ID-less runtimes are listed last."""
    rows = [panel_row(r) for r in data["roles"]]
    rows += [[k, "INVALID", v, "no rights", "INVALID"] for k, v in data["invalid_ids"].items()]
    rows += [["—", x["runtime"], x["rule"], "no role ID", "UNASSIGNED"] for x in data["runtimes_without_role_id"]]
    return rows


def panel_json(data: dict) -> str:
    doc = {"generated_from": SRC.relative_to(ROOT).as_posix(), "matrix_version": data["version"],
           "role_register_version": data["role_register_version"], "as_of": data["as_of"],
           "columns": ["id", "actor", "function", "capabilities", "status"], "roles": panel_roles(data)}
    return json.dumps(doc, ensure_ascii=False, indent=2) + "\n"


def patch_panel(path: Path, data: dict) -> None:
    """Replace only control-data.json['roles'] with the generated rows."""
    cd = json.loads(path.read_text(encoding="utf-8"))
    cd["roles"] = panel_roles(data)
    path.write_text(json.dumps(cd, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def check(outputs: dict[Path, str]) -> int:
    stale = [p for p, text in outputs.items() if (p.read_text(encoding="utf-8") if p.exists() else "") != text]
    for p in stale:
        print(f"{p.relative_to(ROOT).as_posix()} is out of date; run tools/render_role_matrix.py")
    return 1 if stale else 0


def main(argv: list[str]) -> int:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    outputs = {OUT: render(data), PANEL_OUT: panel_json(data)}
    if "--check" in argv:
        return check(outputs)
    if "--panel" in argv:
        patch_panel(Path(argv[argv.index("--panel") + 1]), data)
        return 0
    for p, text in outputs.items():
        p.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
