import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from export_dashboard import ROOT, build_snapshot, write_snapshot, main

COMMIT = "a" * 40


def fixture_report() -> dict:
    return {"schema_version": "1.0.0", "observed_at": "2026-10-19T10:00:00Z", "commit": COMMIT,
            "run_id": "TEST", "run_attempt": "1", "status": "INCOMPLETE", "checks": {
                "registry": {"status": "PASS", "stdout": "PRIVATE_DEBUG_NOT_EXPORTED"},
                "knowledge": {"status": "PASS"}, "coverage": {"status": "INCOMPLETE"},
                "pull_requests": {"status": "PASS"}}}


class DashboardExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for path in ["schemas/knowledge-item.schema.json", "schemas/dashboard-snapshot.schema.json"]:
            dest = self.root / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes((ROOT / path).read_bytes())
        (self.root / "registry/knowledge").mkdir(parents=True)
        (self.root / "registry/file-registry.jsonl").write_text(json.dumps({"id": "b" * 16, "sha256": "c" * 64}) + "\n")
        self.item = {"id": "KO-TEST", "kind": "workflow", "title": "Independent test fixture",
                     "source_file_id": "b" * 16, "version": "1.0.0", "status": "DRAFT"}
        self.item_path = self.root / "registry/knowledge/test.json"
        self.item_path.write_text(json.dumps(self.item))
        self.report = fixture_report()
        self.report_path = self.root / "report.json"

    def build(self):
        self.report_path.write_text(json.dumps(self.report))
        return build_snapshot(self.root, self.report_path, COMMIT)

    def test_preserves_incomplete_and_draft_without_creating_approval(self):
        result = self.build()
        self.assertEqual(result["monitor"]["status"], "INCOMPLETE")
        self.assertEqual(result["nodes"][0]["status"], "DRAFT")
        self.assertEqual(result["human_acceptance"], "NOT_OBSERVED")
        self.assertNotIn("PRIVATE_DEBUG_NOT_EXPORTED", json.dumps(result))
        self.assertEqual(result["nodes"][0]["record_sha256"], hashlib.sha256(self.item_path.read_bytes()).hexdigest())

    def test_export_digest_matches_exact_utf8_bytes(self):
        output = self.root / "out/nexus.snapshot.json"
        write_snapshot(self.build(), output)
        self.assertEqual(output.with_suffix(".json.sha256").read_text().strip(), hashlib.sha256(output.read_bytes()).hexdigest())

    def test_other_revision_is_rejected(self):
        self.report["commit"] = "d" * 40
        with self.assertRaises(ValueError): self.build()

    def test_incomplete_cannot_be_upgraded_to_pass(self):
        self.report["status"] = "PASS"
        with self.assertRaises(ValueError): self.build()

    def test_failure_is_preserved(self):
        self.report["checks"]["registry"]["status"] = "FAIL"
        self.report["status"] = "ATTENTION"
        self.assertEqual(self.build()["monitor"]["status"], "ATTENTION")

    def test_unknown_state_and_missing_checks_are_rejected(self):
        for checks in [{}, {**fixture_report()["checks"], "extra": {"status": "GREEN"}}]:
            with self.subTest(checks=checks):
                self.report["checks"] = checks
                with self.assertRaises(ValueError): self.build()

    def test_duplicate_node_ids_are_rejected(self):
        (self.item_path.parent / "duplicate.json").write_bytes(self.item_path.read_bytes())
        with self.assertRaises(ValueError): self.build()

    def test_unregistered_source_is_rejected(self):
        self.item["source_file_id"] = "e" * 16
        self.item_path.write_text(json.dumps(self.item))
        with self.assertRaises(ValueError): self.build()

    def test_no_knowledge_is_an_empty_array(self):
        self.item_path.unlink()
        self.assertEqual(self.build()["nodes"], [])

    def test_schema_rejects_invalid_timestamp(self):
        self.report["observed_at"] = "not a date"
        with self.assertRaises(ValueError): self.build()

    def test_cli_removes_old_snapshot_when_new_export_fails(self):
        output = self.root / "out.json"
        output.write_text("old snapshot")
        output.with_suffix(".json.sha256").write_text("old digest")
        with patch.object(sys, "argv", ["export", "--root", str(self.root), "--report", str(self.report_path),
                                       "--output", str(output), "--source-commit", COMMIT]):
            self.assertEqual(main(), 1)
        self.assertFalse(output.exists())
        self.assertFalse(output.with_suffix(".json.sha256").exists())

    def test_cli_cannot_delete_its_input(self):
        self.report_path.write_text("preserve me")
        with patch.object(sys, "argv", ["export", "--report", str(self.report_path),
                                       "--output", str(self.report_path), "--source-commit", COMMIT]):
            with self.assertRaises(SystemExit): main()
        self.assertEqual(self.report_path.read_text(), "preserve me")


if __name__ == "__main__":
    unittest.main()
