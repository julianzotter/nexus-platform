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





class SnapshotScopeTests(unittest.TestCase):
    def test_manifest_verified_snapshot_is_archival_not_duplicate(self):
        import hashlib
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(root, "skills/live/SKILL.md", VALID)
            frozen = write(root, "skills/claude-ai/demo/SKILL.md", VALID)
            digest = hashlib.sha256(frozen.read_bytes()).hexdigest()
            write(root, "skills/claude-ai/MANIFEST.sha256", digest + "  ./demo/SKILL.md\n")
            report = si.build_report(root)
            self.assertEqual(report["duplicate_ids"], [])
            archive = next(r for r in report["packages"] if "claude-ai" in r["path"])
            self.assertEqual(archive["status"], "ARCHIVAL_SNAPSHOT")
            self.assertEqual(archive["raw_structure_status"], "INCOMPLETE")
            self.assertEqual(archive["sha256"], digest)

    def test_changed_or_unmanifested_snapshot_is_invalid(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(root, "skills/claude-ai/demo/SKILL.md", VALID)
            for manifest in [None, "0" * 64 + "  demo/SKILL.md\n"]:
                if manifest is not None:
                    write(root, "skills/claude-ai/MANIFEST.sha256", manifest)
                report = si.build_report(root)
                self.assertEqual(report["packages"][0]["status"], "INVALID")

    def test_duplicate_executable_candidates_remain_invalid(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(root, "skills/a/SKILL.md", VALID)
            write(root, "skills/b/SKILL.md", VALID)
            report = si.build_report(root)
            self.assertEqual(report["duplicate_ids"], ["demo-skill"])
            self.assertTrue(all(r["status"] == "INVALID" for r in report["packages"]))


class MixedScopeTests(unittest.TestCase):
    def test_live_duplicates_do_not_invalidate_verified_archive(self):
        import hashlib
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(root, "skills/a/SKILL.md", VALID)
            write(root, "skills/b/SKILL.md", VALID)
            frozen = write(root, "skills/claude-ai/demo/SKILL.md", VALID)
            write(root, "skills/claude-ai/MANIFEST.sha256",
                  hashlib.sha256(frozen.read_bytes()).hexdigest() + "  ./demo/SKILL.md\n")
            report = si.build_report(root)
            self.assertEqual(report["duplicate_ids"], ["demo-skill"])
            archive = next(r for r in report["packages"] if "claude-ai" in r["path"])
            self.assertEqual(archive["status"], "ARCHIVAL_SNAPSHOT")
            self.assertNotIn("DUPLICATE_ID", archive["issues"])


if __name__ == "__main__":
    unittest.main()
