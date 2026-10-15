"""Offline contract and regression tests; never access production data."""
import sqlite3
import tempfile
import unittest
from pathlib import Path
from hybrid_gateway import AtlasSchemaError, invoke, open_atlas


class GatewayTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = str(Path(self.tmp.name) / 'atlas.sqlite')
        with sqlite3.connect(self.db) as conn:
            conn.execute('CREATE TABLE files (file_name TEXT, source_system TEXT, source_class TEXT, scan_status TEXT, sha256 TEXT)')
            conn.execute("INSERT INTO files VALUES ('SiloDesign.md','GDRIVE','REGISTRY','HASHED','abc')")

    def tearDown(self):
        self.tmp.cleanup()

    def test_health(self):
        self.assertEqual(invoke('atlas.health', self.db)['file_locations'], 1)

    def test_lookup(self):
        row = invoke('atlas.lookup', self.db, 'Silo')['results'][0]
        self.assertEqual(row['file_name'], 'SiloDesign.md')
        self.assertNotIn('abs_path', row)

    def test_allowlist(self):
        with self.assertRaises(ValueError):
            invoke('shell.execute', self.db)

    def test_missing_database_not_created(self):
        path = str(Path(self.tmp.name) / 'missing.sqlite')
        with self.assertRaises(FileNotFoundError):
            invoke('atlas.health', path)
        self.assertFalse(Path(path).exists())

    def test_invalid_parameters(self):
        for limit in (0, 101, True, '4'):
            with self.assertRaises(ValueError):
                invoke('atlas.lookup', self.db, 'Silo', limit)
        with self.assertRaises(ValueError):
            invoke('atlas.lookup', self.db, '')

    def test_uri_special_characters(self):
        for filename in ('atlas#snapshot.sqlite', 'atlas%20.sqlite', 'atlas?query.sqlite', 'atlas space.sqlite'):
            target = Path(self.tmp.name) / filename
            target.write_bytes(Path(self.db).read_bytes())
            self.assertEqual(invoke('atlas.health', str(target))['file_locations'], 1)

    def test_missing_table_rejected(self):
        path = Path(self.tmp.name) / 'wrong.sqlite'
        with sqlite3.connect(path) as db:
            db.execute('CREATE TABLE not_files (x TEXT)')
        with self.assertRaisesRegex(AtlasSchemaError, "required table 'files'"):
            invoke('atlas.health', str(path))

    def test_missing_column_rejected(self):
        path = Path(self.tmp.name) / 'wrongcols.sqlite'
        with sqlite3.connect(path) as db:
            db.execute('CREATE TABLE files (file_name TEXT)')
        with self.assertRaisesRegex(AtlasSchemaError, 'missing files columns'):
            invoke('atlas.health', str(path))

    def test_write_blocked(self):
        with open_atlas(self.db) as db:
            with self.assertRaises(sqlite3.OperationalError):
                db.execute("INSERT INTO files (file_name) VALUES ('unauthorized')")
        self.assertEqual(invoke('atlas.health', self.db)['file_locations'], 1)

    def test_literal_search_wildcards(self):
        self.assertEqual(invoke('atlas.lookup', self.db, '%')['results'], [])
        self.assertEqual(invoke('atlas.lookup', self.db, '_')['results'], [])


if __name__ == '__main__':
    unittest.main()
