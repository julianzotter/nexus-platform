"""Negative and positive tests for tools/skill_inventory.py."""
import tempfile
import unittest
from pathlib import Path

from tools import skill_inventory as si

VALID = "---\nname: demo-skill\ndescription: Does a demo.\n---\n# Demo\n"


def write(root: Path, rel: str, text: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


class ParseTests(unittest.TestCase):
    def test_valid_frontmatter(self):
        fields, err = si.parse_frontmatter(VALID)
        self.assertIsNone(err)
        self.assertEqual(fields["name"], "demo-skill")

    def test_crlf_frontmatter(self):
        fields, err = si.parse_frontmatter(VALID.replace("\n", "\r\n"))
        self.assertIsNone(err)
        self.assertEqual(fields["name"], "demo-skill")

    def test_missing_frontmatter(self):
        self.assertEqual(si.parse_frontmatter("# no fm")[1], "NO_FRONTMATTER")

    def test_unclosed_frontmatter(self):
        self.assertEqual(si.parse_frontmatter("---\nname: x\n")[1], "FRONTMATTER_NOT_CLOSED")

    def test_duplicate_key_rejected(self):
        text = "---\nname: a\nname: b\n---\n"
        self.assertEqual(si.parse_frontmatter(text)[1], "DUPLICATE_KEY:name")

    def test_nested_yaml_rejected(self):
        text = "---\nname: a\nmeta:\n  x: 1\n---\n"
        self.assertEqual(si.parse_frontmatter(text)[1], "FRONTMATTER_NOT_FLAT")


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_valid_package_is_incomplete_without_optional_fields(self):
        rec = si.inventory_skill(write(self.root, "skills/a/SKILL.md", VALID), self.root)
        self.assertEqual(rec["status"], "INCOMPLETE")
        self.assertEqual(rec["version"], "UNKNOWN")
        self.assertIn("UNKNOWN:owner", rec["issues"])

    def test_fully_declared_package_is_valid_structure(self):
        text = VALID.replace("---\n# Demo", "version: 1.0.0\nowner: julian\ntools: none\nruntime: any\n---\n# Demo")
        rec = si.inventory_skill(write(self.root, "skills/b/SKILL.md", text), self.root)
        self.assertEqual(rec["status"], "VALID_STRUCTURE")

    def test_crlf_inventory_preserves_raw_hash(self):
        import hashlib
        # write_bytes: text-mode write_text would turn "\r\n" into "\r\r\n" on Windows.
        raw = VALID.replace("\n", "\r\n").encode("utf-8")
        p = self.root / "skills/crlf/SKILL.md"
        p.parent.mkdir(parents=True)
        p.write_bytes(raw)
        rec = si.inventory_skill(p, self.root)
        self.assertEqual(rec["status"], "INCOMPLETE")
        self.assertEqual(rec["sha256"], hashlib.sha256(raw).hexdigest())

    def test_missing_name_is_invalid(self):
        text = "---\ndescription: only desc\n---\n"
        rec = si.inventory_skill(write(self.root, "skills/c/SKILL.md", text), self.root)
        self.assertEqual(rec["status"], "INVALID")
        self.assertIn("MISSING_REQUIRED:name", rec["issues"])

    def test_missing_description_is_invalid(self):
        text = "---\nname: only-name\n---\n"
        rec = si.inventory_skill(write(self.root, "skills/d/SKILL.md", text), self.root)
        self.assertEqual(rec["status"], "INVALID")

    def test_hash_matches_bytes(self):
        import hashlib
        p = write(self.root, "skills/e/SKILL.md", VALID)
        rec = si.inventory_skill(p, self.root)
        self.assertEqual(rec["sha256"], hashlib.sha256(p.read_bytes()).hexdigest())

    def test_duplicate_ids_marked_invalid(self):
        write(self.root, "skills/x/SKILL.md", VALID)
        write(self.root, "skills/y/SKILL.md", VALID)
        recs = [si.inventory_skill(p, self.root) for p in sorted(self.root.glob("skills/**/SKILL.md"))]
        self.assertEqual(si.find_duplicate_ids(recs), ["demo-skill"])

    def test_report_on_repository_runs(self):
        report = si.build_report()
        self.assertIn("counts", report)
        self.assertEqual(report["scope"], "structure_and_bytes_only")


if __name__ == "__main__":
    unittest.main()
