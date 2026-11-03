import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from coverage_stats import SOURCE_NAMES, calculate_coverage
from detect_duplicates import mark_duplicates
from validate_registry import validate_registry


class InventoryCompletenessTests(unittest.TestCase):
    def test_coverage_uses_indexed_over_accessible_and_marks_unavailable_sources(self):
        # This is a multi-source behaviour fixture, independent of active sources.
        available, unavailable = "available-fixture", "unavailable-fixture"
        records = [
            {"root": available, "status": "FOUND"},
            {"root": available, "status": "FOUND"},
            {"root": available, "status": "SKIPPED"},
            {"root": available, "status": "ERROR"},
        ]
        with patch("coverage_stats.SOURCE_NAMES", (available, unavailable)):
            stats = calculate_coverage(records, {unavailable: "not mounted"})
        source = stats["sources"][available]
        self.assertEqual((source["discovered"], source["accessible"], source["indexed"]), (4, 3, 2))
        self.assertAlmostEqual(source["coverage_percent"], 2 / 3 * 100)
        self.assertEqual(stats["total"]["status"], "INCOMPLETE")
        self.assertIsNone(stats["sources"][unavailable]["accessible"])

    def test_active_source_scope_does_not_invent_unavailable_sources(self):
        records = [{"root": name, "status": "FOUND"} for name in SOURCE_NAMES]
        stats = calculate_coverage(records, {})
        self.assertEqual(set(stats["sources"]), set(SOURCE_NAMES))
        self.assertEqual(stats["total"]["status"], "COMPLETE")
        self.assertEqual(stats["total"]["indexed"], len(records))
        self.assertEqual(stats["total"]["coverage_percent"], 100)

    def test_incomplete_evidence_overrides_complete_source_assertion(self):
        source = SOURCE_NAMES[0]
        for records, reasons in [
            ([{"root": source, "status": "FOUND"}], {source: "scan interrupted"}),
            ([{"root": source, "status": "INCOMPLETE"}], {}),
        ]:
            with self.subTest(records=records, reasons=reasons):
                stats = calculate_coverage(records, reasons, {source})
                for entry in (stats["sources"][source], stats["total"]):
                    self.assertEqual(entry["status"], "INCOMPLETE")
                    for metric in ("discovered", "accessible", "indexed", "skipped", "error", "coverage_percent"):
                        self.assertIsNone(entry[metric])

    def test_duplicate_marking_is_stable_and_uses_duplicate_fields(self):
        records = [
            {"id": "b", "root": "source", "path": "b", "status": "FOUND", "sha256": "a" * 64},
            {"id": "a", "root": "source", "path": "a", "status": "FOUND", "sha256": "a" * 64},
        ]
        marked, report = mark_duplicates(records)
        self.assertEqual(marked[0]["id"], "a")
        self.assertEqual(marked[0]["duplicate_group"], f"sha256:{'a' * 64}")
        self.assertNotIn("duplicate_of", marked[0])
        self.assertEqual(marked[1]["duplicate_of"], "a")
        self.assertNotIn("supersedes", report)

    def test_validation_accepts_incomplete_sources_without_fabricated_counts(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            registry = root / "registry.jsonl"
            registry.write_text("", encoding="utf-8")
            coverage = calculate_coverage([], {name: "source unavailable" for name in SOURCE_NAMES})
            coverage_path = root / "coverage.json"
            coverage_path.write_text(json.dumps(coverage), encoding="utf-8")
            self.assertEqual(validate_registry(registry, coverage_path), [])

    def test_validation_rejects_incorrect_coverage_formula(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            registry = root / "registry.jsonl"
            registry.write_text("", encoding="utf-8")
            coverage = calculate_coverage([], {name: "source unavailable" for name in SOURCE_NAMES})
            coverage["formula"] = "indexed / discovered"
            coverage_path = root / "coverage.json"
            coverage_path.write_text(json.dumps(coverage), encoding="utf-8")
            self.assertTrue(validate_registry(registry, coverage_path))

    def test_unmeasured_sources_are_not_assumed_empty_and_complete(self):
        stats = calculate_coverage([], {})
        self.assertTrue(all(source["status"] == "INCOMPLETE" for source in stats["sources"].values()))
        self.assertTrue(all(source["accessible"] is None for source in stats["sources"].values()))

    def test_validation_rejects_malformed_registry_records(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            registry = root / "registry.jsonl"
            registry.write_text(json.dumps({"id": "bad"}) + "\n", encoding="utf-8")
            coverage = calculate_coverage([], {name: "source unavailable" for name in SOURCE_NAMES})
            coverage_path = root / "coverage.json"
            coverage_path.write_text(json.dumps(coverage), encoding="utf-8")
            self.assertTrue(any("missing fields" in error for error in validate_registry(registry, coverage_path)))


if __name__ == "__main__":
    unittest.main()
