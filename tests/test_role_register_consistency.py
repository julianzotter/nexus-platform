"""NEXUS-ROLES v1.2 consistency across governance files, AGENTS.md and the capability matrix."""
from __future__ import annotations

import hashlib
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
STALE = re.compile(r"ChatGPT Private\s*=\s*ID02|ID02\s*[—-]\s*ChatGPT Private")


class RoleRegisterConsistency(unittest.TestCase):
    def setUp(self) -> None:
        self.matrix = json.loads(MATRIX.read_text(encoding="utf-8"))

    def test_current_files_declare_v12(self) -> None:
        for name in ("00_NEXUS_MANIFEST__CURRENT__2026-09-28.md", "_FRONTMATTER.md", "_AGBS.md"):
            self.assertIn(VERSION, (GOV / name).read_text(encoding="utf-8"), name)
        self.assertIn(VERSION, (ROOT / "AGENTS.md").read_text(encoding="utf-8"))

    def test_no_stale_mapping_in_current_entrypoints(self) -> None:
        for path in [ROOT / "AGENTS.md", *GOV.glob("*.md")]:
            self.assertIsNone(STALE.search(path.read_text(encoding="utf-8")), path.name)

    def test_manifest_assigns_business_and_private(self) -> None:
        text = MANIFEST.read_text(encoding="utf-8")
        self.assertRegex(text, r"ID02 — ChatGPT Business")
        self.assertRegex(text, r"ID03 — ChatGPT Private")
        self.assertIn("ID93", text)

    def test_matrix_matches_manifest(self) -> None:
        roles = {r["id"]: r for r in self.matrix["roles"]}
        self.assertEqual(sorted(roles), [f"ID{n:02d}" for n in range(1, 11)])
        self.assertEqual(roles["ID02"]["actor"], "ChatGPT Business")
        self.assertEqual(roles["ID03"]["actor"], "ChatGPT Private")
        self.assertIn("Chief Orchestrator", roles["ID03"]["function"])
        self.assertIn("ID93", self.matrix["invalid_ids"])
        self.assertEqual(self.matrix["role_register_version"], VERSION)

    def test_matrix_pins_manifest_hash(self) -> None:
        digest = hashlib.sha256(MANIFEST.read_bytes()).hexdigest()
        self.assertEqual(self.matrix["role_authority"]["sha256"], digest,
                         "Manifest changed: re-derive the matrix and update role_authority.sha256")

    def test_capability_values_use_legend(self) -> None:
        allowed = set(self.matrix["legend"])
        for r in self.matrix["roles"]:
            for col in ("drive_read", "drive_write", "github_read", "github_write", "merge"):
                self.assertIn(r[col], allowed, f"{r['id']}.{col}")

    def test_markdown_rendering_is_current(self) -> None:
        res = subprocess.run([sys.executable, str(ROOT / "tools" / "render_role_matrix.py"), "--check"],
                             capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, res.stdout)


if __name__ == "__main__":
    unittest.main()
