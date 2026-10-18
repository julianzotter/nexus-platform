import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from knowledge_health import assess_item

NOW = datetime(2026, 10, 18, tzinfo=timezone.utc)
FID = "0123456789abcdef"


def item(**kw):
    base = {"id": "k", "version": "1.0", "source_file_id": FID, "engineering_result": True,
            "signoff": {"result_version": "1.0", "decided_at": "2026-10-01T00:00:00Z"}}
    base.update(kw)
    return base


class HealthTests(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(assess_item(item(), {FID}, NOW, 180)["state"], "OK")

    def test_broken_link(self):
        self.assertEqual(assess_item(item(), set(), NOW, 180)["state"], "BROKEN")

    def test_missing_signoff(self):
        self.assertEqual(assess_item(item(signoff=None), {FID}, NOW, 180)["state"], "BROKEN")

    def test_stale_version(self):
        s = {"result_version": "0.9", "decided_at": "2026-10-01T00:00:00Z"}
        self.assertEqual(assess_item(item(signoff=s), {FID}, NOW, 180)["state"], "STALE")

    def test_stale_age(self):
        s = {"result_version": "1.0", "decided_at": "2025-01-01T00:00:00Z"}
        self.assertEqual(assess_item(item(signoff=s), {FID}, NOW, 180)["state"], "STALE")
