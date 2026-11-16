"""Offline tests for the no-network seed catalog contract."""

from __future__ import annotations

import copy
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_seed import create_sqlite, validate  # noqa: E402


class SeedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.seed = json.loads((ROOT / "seed/nexus_aec_top20_seed_v1.json").read_text("utf-8"))

    def test_complete_seed(self) -> None:
        self.assertEqual(validate(self.seed), [])

    def test_url_cannot_claim_other_host(self) -> None:
        modified = copy.deepcopy(self.seed)
        modified["sources"][0]["url"] = "https://untrusted.example/"
        self.assertIn("host/URL mismatch: DATAHOLZ", validate(modified))

    def test_broken_relation_is_rejected(self) -> None:
        modified = copy.deepcopy(self.seed)
        modified["links"][0]["to"] = "NONEXISTENT"
        self.assertTrue(any(x.startswith("broken edge") for x in validate(modified)))

    def test_sqlite_round_trip_and_no_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            db = Path(temp) / "discovery.sqlite"
            create_sqlite(self.seed, db)
            with sqlite3.connect(db) as conn:
                self.assertEqual(conn.execute("SELECT count(*) FROM sources").fetchone()[0], 20)
                self.assertEqual(conn.execute("SELECT count(*) FROM links").fetchone()[0], 9)
                self.assertEqual(conn.execute("PRAGMA integrity_check").fetchone()[0], "ok")
            with self.assertRaises(FileExistsError):
                create_sqlite(self.seed, db)


if __name__ == "__main__":
    unittest.main()
