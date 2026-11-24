"""NEXUS-ROLES v1.2 consistency: governance entrypoints, Manifest §4 and the capability matrix."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOV = ROOT / "governance" / "current"
MANIFEST = GOV / "00_NEXUS_MANIFEST__CURRENT__2026-09-28.md"
MATRIX = ROOT / "registry" / "roles" / "role_capability_matrix.json"
VERSION = "NEXUS-ROLES-v1.2"
CAP_COLS = ("drive_read", "drive_write", "github_read", "github_write", "merge")
STALE = [
    re.compile(r"ChatGPT Private\s*\\?=\s*ID02"),
    re.compile(r"ID02\s*[—-]+\s*ChatGPT Private"),
    re.compile(r"ID03 bleibt ChatGPT Assistant / Peer Reviewer"),
]
HIST_HEADING = re.compile(r"HISTORICAL|SUPERSEDED|STALE|Originalinhalt", re.I)


def current_text(text: str) -> str:
    """Drop <details> blocks and Markdown sections whose heading marks them historical."""
    text = re.sub(r"<details>.*?</details>", "", text, flags=re.S)
    out, skip_level = [], 0
    for line in text.splitlines():
        m = re.match(r"^(#+)\s", line)
        if m:
            level = len(m.group(1))
            if skip_level and level <= skip_level:
                skip_level = 0
            if not skip_level and HIST_HEADING.search(line):
                skip_level = level
        if not skip_level:
            out.append(line)
    return "\n".join(out)


def manifest_section4() -> str:
    text = MANIFEST.read_text(encoding="utf-8")
    start = text.index("4\\. AUTHORITY AND ROLES") if "4\\. AUTHORITY" in text else text.index("4. AUTHORITY")
    return text[start:text.index("5\\. LEADERSHIP") if "5\\. LEADERSHIP" in text else text.index("5. LEADERSHIP")]


class RoleRegisterConsistency(unittest.TestCase):
    def setUp(self) -> None:
        self.matrix = json.loads(MATRIX.read_text(encoding="utf-8"))

    def test_entrypoints_declare_v12(self) -> None:
        for path in [ROOT / "AGENTS.md", MANIFEST]:
            self.assertIn(VERSION, path.read_text(encoding="utf-8"), path.name)

    def test_no_stale_mapping_outside_historical_sections(self) -> None:
        paths = [ROOT / "AGENTS.md", *sorted(GOV.glob("*.md"))]
        copilot = ROOT / ".github" / "copilot-instructions.md"
        if copilot.exists():
            paths.append(copilot)
        for path in paths:
            body = current_text(path.read_text(encoding="utf-8"))
            for pattern in STALE:
                self.assertIsNone(pattern.search(body), f"{path.name}: {pattern.pattern}")

    def test_every_role_key_appears_in_manifest_section4(self) -> None:
        sec = manifest_section4()
        for role in self.matrix["roles"]:
            self.assertRegex(sec, rf"{role['id']}\b[^\n]{{0,12}}{re.escape(role['manifest_key'])}", role["id"])
        self.assertIn("ID93", sec)

    def test_v12_assignments(self) -> None:
        roles = {r["id"]: r for r in self.matrix["roles"]}
        self.assertEqual(sorted(roles), [f"ID{n:02d}" for n in range(1, 11)])
        self.assertEqual(roles["ID02"]["actor"], "ChatGPT Business")
        self.assertEqual(roles["ID03"]["actor"], "ChatGPT Private")
        self.assertIn("Chief Orchestrator", roles["ID03"]["function"])
        self.assertIn("ID93", self.matrix["invalid_ids"])
        self.assertEqual(self.matrix["role_register_version"], VERSION)

    def test_capability_values_use_legend(self) -> None:
        allowed = set(self.matrix["legend"])
        for r in self.matrix["roles"]:
            for col in CAP_COLS:
                self.assertIn(r[col], allowed, f"{r['id']}.{col}")
            if "VERIFIED" in (r[c] for c in CAP_COLS):
                self.assertRegex(r["evidence"], r"20\d\d-\d\d-\d\d", f"{r['id']}: VERIFIED needs dated evidence")

    def test_markdown_rendering_is_current(self) -> None:
        res = subprocess.run([sys.executable, str(ROOT / "tools" / "render_role_matrix.py"), "--check"],
                             capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, res.stdout)


if __name__ == "__main__":
    unittest.main()
