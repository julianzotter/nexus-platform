import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import json
import tempfile

from knowledge_health import assess_item, build_report

NOW = datetime(2026, 10, 18, tzinfo=timezone.utc)
FID = "0123456789abcdef"


def item(**kw):
    base = {"id": "k", "version": "1.0", "source_file_id": FID, "engineering_result": True,
            "signoff": {"result_version": "1.0", "decided_at": "2026-10-01T00:00:00Z"}}
    base.update(kw)
    return base


class HealthTests(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(assess_item(item(signoff={"result_version": "1.0", "decided_at": "2026-10-01T00:00:00Z", "approver_type": "human"}), {FID}, NOW, 180)["state"], "OK")

    def test_llm_signoff_is_draft_not_ok(self):
        s = {"result_version": "1.0", "decided_at": "2026-10-01T00:00:00Z", "approver_type": "llm"}
        self.assertEqual(assess_item(item(signoff=s), {FID}, NOW, 180)["state"], "DRAFT")

    def test_missing_approver_type_is_draft(self):
        self.assertEqual(assess_item(item(), {FID}, NOW, 180)["state"], "DRAFT")

    def test_non_engineering_without_signoff_is_draft(self):
        self.assertEqual(assess_item(item(engineering_result=False, signoff=None), {FID}, NOW, 180)["state"], "DRAFT")

    def test_unreadable_date_never_ok(self):
        s = {"result_version": "1.0", "decided_at": "not-a-date", "approver_type": "human"}
        self.assertNotEqual(assess_item(item(signoff=s), {FID}, NOW, 180)["state"], "OK")

    def test_broken_link(self):
        self.assertEqual(assess_item(item(), set(), NOW, 180)["state"], "BROKEN")

    def test_missing_signoff(self):
        self.assertEqual(assess_item(item(signoff=None), {FID}, NOW, 180)["state"], "BROKEN")

    def test_stale_version(self):
        s = {"result_version": "0.9", "decided_at": "2026-10-01T00:00:00Z"}
        self.assertEqual(assess_item(item(signoff=s), {FID}, NOW, 180)["state"], "STALE")

    def test_unreadable_knowledge_file_is_broken(self):
        with tempfile.TemporaryDirectory() as d:
            kd = Path(d) / "k"; kd.mkdir()
            (kd / "bad.json").write_text("{not json", encoding="utf-8")
            r = build_report(kd, Path(d) / "none.jsonl", Path(d) / "none.json", NOW, 180)
            self.assertEqual(r["counts"], {"BROKEN": 1})

    def test_empty_inventory_is_explicit_no_data(self):
        with tempfile.TemporaryDirectory() as d:
            r = build_report(Path(d) / "missing", Path(d) / "none.jsonl", Path(d) / "none.json", NOW, 180)
            self.assertEqual(r["status"], "NO_DATA")
            self.assertEqual(r["healthy_percent"], "INCOMPLETE")
            self.assertEqual(r["items"], 0)

    def test_stale_age(self):
        s = {"result_version": "1.0", "decided_at": "2025-01-01T00:00:00Z"}
        self.assertEqual(assess_item(item(signoff=s), {FID}, NOW, 180)["state"], "STALE")
