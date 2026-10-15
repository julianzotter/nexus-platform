"""Offline safety and contract tests for hybrid gateway."""
import sqlite3
import tempfile
import unittest
from pathlib import Path
from hybrid_gateway import invoke

class GatewayTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = str(Path(self.tmp.name) / "atlas.sqlite")
        with sqlite3.connect(self.db) as db:
            db.execute("CREATE TABLE files (file_name TEXT,source_system TEXT,source_class TEXT,scan_status TEXT,sha256 TEXT)")
            db.execute("INSERT INTO files VALUES ('SiloDesign.md','GDRIVE','REGISTRY','HASHED','abc')")

    def tearDown(self):
        self.tmp.cleanup()

    def test_health(self):
        self.assertEqual(invoke("atlas.health", self.db)["file_locations"], 1)

    def test_lookup(self):
        result = invoke("atlas.lookup", self.db, "Silo")
        self.assertEqual(len(result["results"]), 1)
        self.assertNotIn("abs_path", result["results"][0])

    def test_allowlist(self):
        with self.assertRaises(ValueError):
            invoke("shell.execute", self.db)

    def test_missing_database_not_created(self):
        path = str(Path(self.tmp.name) / "missing.sqlite")
        with self.assertRaises(FileNotFoundError):
            invoke("atlas.health", path)
        self.assertFalse(Path(path).exists())

    def test_limit_and_empty_term(self):
        with self.assertRaises(ValueError):
            invoke("atlas.lookup", self.db, "Silo", 101)
        with self.assertRaises(ValueError):
            invoke("atlas.lookup", self.db, "")
if __name__ == "__main__":
    unittest.main()
