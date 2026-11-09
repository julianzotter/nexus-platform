"""Read-only checks of the shipped projection and temporary isolated build tests."""
import hashlib
import json
import re
import shutil
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path

import build_knowledge as k


class KnowledgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temp.name) / "snapshot"
        cls.manifest = k.build(k.BASELINE, cls.output)
        cls.payload = json.loads((cls.output / "W012_Knowledge.json").read_text())

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    def test_integrity_and_baseline_preserved(self) -> None:
        with k.readonly(k.BASELINE) as base, k.readonly(self.output / "W012_Knowledge.sqlite") as db:
            self.assertEqual(db.execute("PRAGMA integrity_check").fetchone()[0], "ok")
            self.assertEqual(db.execute("PRAGMA foreign_key_check").fetchall(), [])
            for table in ("metadata", "sources", "records", "record_sources", "assemblies", "layers", "search_fts", "source_fts"):
                self.assertEqual([tuple(r) for r in base.execute("SELECT * FROM " + table)],
                                 [tuple(r) for r in db.execute("SELECT * FROM " + table)])

    def test_query_contract(self) -> None:
        with k.readonly(self.output / "W012_Knowledge.sqlite") as db:
            self.assertEqual(k.search(db, "PAR-01")[0]["id"], "PAR-01")
            self.assertIn("BTL-IW01h:L2", {r["id"] for r in k.search(db, "Gipskarton")})
            self.assertEqual(k.search(db, "Straße"), k.search(db, "Strasse"))
            self.assertEqual(k.search(db, '" OR * : ()'), k.search(db, "OR"))
            self.assertEqual(k.search(db, "---"), [])

    def test_snapshot_and_hashes(self) -> None:
        html = (self.output / "W012_Knowledge.html").read_text()
        embedded = json.loads(re.search(r'<script type="application/json" id="data">(.*?)</script>', html, re.S).group(1))
        self.assertEqual(embedded, self.payload)
        with k.readonly(self.output / "W012_Knowledge.sqlite") as db:
            self.assertEqual(json.loads(db.execute("SELECT value FROM knowledge_metadata WHERE key='snapshot_id'").fetchone()[0]), self.payload["snapshot_id"])
            self.assertEqual([dict(r) for r in db.execute("SELECT * FROM knowledge_documents ORDER BY id")], self.payload["documents"])
        for name, expected in self.manifest["files"].items():
            self.assertEqual(k.digest(self.output / name), expected)

    def test_extras_and_immutable_output(self) -> None:
        extras = Path(self.temp.name) / "extras"
        extras.mkdir(exist_ok=True)
        (extras / "note.md").write_text("# Ergänzung\nStraße Gipskarton", encoding="utf-8")
        (extras / "note.json").write_text('{"status":"APPROVED"}', encoding="utf-8")
        documents, inputs = k.extra_documents(extras)
        self.assertEqual(len(inputs), 2)
        self.assertTrue(all(d["status"] == "UNVERIFIED" for d in documents))
        with self.assertRaises(FileExistsError):
            k.build(k.BASELINE, self.output)

    def test_repeatable_identity(self) -> None:
        second = Path(self.temp.name) / "second"
        other = k.build(k.BASELINE, second)
        self.assertEqual(other["snapshot_id"], self.manifest["snapshot_id"])
        for filename in ("W012_Knowledge.json", "W012_Knowledge.html", "W012_Knowledge.sqlite"):
            self.assertEqual(k.digest(second / filename), k.digest(self.output / filename))

    def test_structured_expansion_and_duplicate_rejection(self) -> None:
        directory = Path(self.temp.name) / "structured"
        directory.mkdir(exist_ok=True)
        row = dict(id="EXT-001", title="Evidence", body="Original text", url="https://example.org/",
                   status="CONTENT_READ", source_kind="external", provider_id="123", approved_for_model=0)
        (directory / "rows.json").write_text(json.dumps([row, {**row, "id": "EXT-002"}]))
        documents, inputs = k.extra_documents(directory)
        self.assertEqual(len(documents), 2)
        self.assertEqual(documents[0]["status"], "CONTENT_READ")
        self.assertEqual(documents[0]["url"], row["url"])
        self.assertIn('"provider_id":"123"', documents[0]["body"])
        self.assertEqual(len(inputs), 1)
        k.prepare_documents(documents)
        with self.assertRaises(ValueError):
            k.prepare_documents([dict(row), {**row, "id": "ext-001"}])
        with self.assertRaises(ValueError):
            k.structured_documents([{**row, "body": {"wrong": "type"}}])

    def test_html_url_protocol_guard(self) -> None:
        function = re.search(r"function safeUrl\(value\).*?(?=function lookup)", k.HTML, re.S).group(0)
        script = function + "\nprocess.stdout.write(JSON.stringify(['https://example.org/','javascript:alert(1)','data:text/html,test','file:///tmp/a','http://example.org/','invalid'].map(safeUrl)));"
        result = subprocess.run([shutil.which("node"), "-e", script], capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout), ["https://example.org/", None, None, None, None, None])

    def test_actual_javascript_search_parity(self) -> None:
        node = shutil.which("node")
        self.assertIsNotNone(node, "Node is needed to validate actual HTML search parity")
        html = (self.output / "W012_Knowledge.html").read_text()
        normalizers = re.search(r"const normalize=.*?(?=const create=)", html, re.S).group(0)
        lookup = re.search(r"function lookup\(query\).*?(?=function render\(\))", html, re.S).group(0)
        queries = ["PAR-01", "Gipskarton", "Straße", "Strasse", "CLT 160", "IW01h", '" OR * : ()']
        script = "const data=JSON.parse(require('fs').readFileSync(0,'utf8'));\n" + normalizers + lookup
        script += "\nprocess.stdout.write(JSON.stringify(" + json.dumps(queries) + ".map(q=>lookup(q).map(d=>d.id))));"
        result = subprocess.run([node, "-e", script], input=k.canonical(self.payload), text=True,
                                capture_output=True, check=True)
        with k.readonly(self.output / "W012_Knowledge.sqlite") as db:
            self.assertEqual(json.loads(result.stdout),
                             [[d["id"] for d in k.search(db, query, 10000)] for query in queries])


if __name__ == "__main__":
    unittest.main()
