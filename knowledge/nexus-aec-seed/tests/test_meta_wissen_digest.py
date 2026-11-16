from __future__ import annotations

import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from meta_wissen_digest import canonical_url, render_digest  # noqa: E402


class WeeklyDigestTests(unittest.TestCase):
    def test_no_claims_without_observations(self) -> None:
        as_of = datetime(2026, 11, 16, 8, 0, tzinfo=timezone.utc)
        result = render_digest([], as_of, 9)
        self.assertIn("observations_verified: 0", result)
        self.assertIn("No VERIFIED new observations", result)

    def test_dedup_and_unverified_filter(self) -> None:
        as_of = datetime(2026, 11, 16, 8, 0, tzinfo=timezone.utc)
        verified = {
            "publisher_id": "OIB", "topic": "OIB", "evidence_status": "VERIFIED",
            "source_uri": "https://www.oib.or.at/example/#section", "title": "Test version",
            "published_at": "2026-11-15T08:00:00+00:00", "finding": "Mock finding",
            "locator": "§1", "version_id": "vA",
        }
        unverified = {**verified, "evidence_status": "UNVERIFIED", "finding": "Do not include"}
        result = render_digest([verified, verified.copy(), unverified], as_of, 9)
        self.assertIn("observations_verified: 1", result)
        self.assertNotIn("Do not include", result)
        self.assertEqual(result.count("Mock finding"), 1)

    def test_requires_https(self) -> None:
        with self.assertRaises(ValueError):
            canonical_url("http://example.org")


if __name__ == "__main__":
    unittest.main()
