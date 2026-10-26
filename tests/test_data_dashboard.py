import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1] / "prototypes" / "data-dashboard"
sys.path.insert(0, str(HERE))
import build_data  # noqa: E402

HTML = (HERE / "index.html").read_text(encoding="utf-8")


def embedded() -> dict:
    return json.loads(re.search(r"window\.DASHBOARD_DATA = (.*?);/\*DATA:END\*/", HTML, re.S).group(1))


class DataDashboardTests(unittest.TestCase):
    def test_embedded_data_matches_rebuild_at_its_revision(self):
        data = embedded()
        self.assertEqual(data, build_data.build(data["revision"]))

    def test_embedded_revision_is_in_history(self):
        rev = embedded()["revision"]
        subprocess.run(["git", "merge-base", "--is-ancestor", rev, "HEAD"], cwd=build_data.ROOT, check=True)

    def test_rows_conform_to_declared_columns(self):
        for ds in embedded()["datasets"].values():
            keys = {c["key"] for c in ds["columns"]}
            self.assertTrue(ds["rows"])
            for row in ds["rows"]:
                self.assertEqual(set(row), keys)
                for c in ds["columns"]:
                    v = row[c["key"]]
                    if c["type"] == "number" and v is not None:
                        self.assertIsInstance(v, int)
                    if c["type"] == "date" and v is not None:
                        self.assertRegex(v, r"^\d{4}-\d{2}-\d{2}")

    def test_file_dates_present(self):
        rows = embedded()["datasets"]["dateien"]["rows"]
        self.assertTrue(all(r["geaendert"] for r in rows))

    def test_self_contained(self):
        self.assertIsNone(re.search(r"<(script|link|img)[^>]+(src|href)=\"https?:", HTML))
        self.assertNotIn("innerHTML", HTML)

    def test_embed_requires_markers(self):
        with self.assertRaises(ValueError):
            build_data.embed("<html></html>", {})


QUERIES = [
    ("dateien", "Wie viele Python-Dateien?", {"filters": [{"col": "typ", "op": "eq", "value": ".py"}], "count": True}),
    ("dateien", "Summe Zeilen im Ordner tests", {"filters": [{"col": "ordner", "op": "eq", "value": "tests"}], "stat": {"fn": "sum", "col": "zeilen"}}),
    ("dateien", "Dateien größer als 10 kb", {"filters": [{"col": "bytes", "op": "gt", "value": 10240}]}),
    ("dateien", "Gruppiere nach Ordner", {"groupBy": "ordner"}),
    ("dateien", "sortiere nach zeilen aufsteigend", {"sort": {"col": "zeilen", "dir": "asc"}}),
    ("dateien", "Die 5 größten Dateien", {"top": {"n": 5, "col": None}}),
    ("dateien", "Wechsle zu Commits", {"dataset": "commits"}),
    ("dateien", "exportiere als markdown", {"export": "md"}),
    ("commits", "Wie viele Commits seit 2026-10-18?", {"filters": [{"col": "datum", "op": "gte", "value": "2026-10-18"}], "count": True}),
    ("commits", "ohne Merge", {"filters": [{"col": "art", "op": "neq", "value": "Merge"}]}),
    ("commits", "Summe plus pro Autor", {"groupBy": "autor", "stat": {"fn": "sum", "col": "plus"}}),
    ("commits", "blabla", {"understood": False}),
]


@unittest.skipUnless(shutil.which("node"), "node not available")
class QueryGrammarTests(unittest.TestCase):
    def test_queries(self):
        nlq = re.search(r'<script id="nlq">(.*?)</script>', HTML, re.S).group(1)
        driver = """
const NLQ = require(process.argv[2]); const D = JSON.parse(require('fs').readFileSync(process.argv[3], 'utf8'));
const out = JSON.parse(require('fs').readFileSync(process.argv[4], 'utf8')).map(([k, q]) => {
  const cols = D.datasets[k].columns.map(c => ({...c}));
  for (const c of cols) if (c.type === 'category') c.values = [...new Set(D.datasets[k].rows.map(r => r[c.key]))];
  return NLQ.interpret(q, {columns: cols, datasets: Object.entries(D.datasets).map(([key, d]) => ({key, title: d.title}))});
});
console.log(JSON.stringify(out));"""
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            (t / "nlq.js").write_text(nlq, encoding="utf-8")
            (t / "driver.js").write_text(driver, encoding="utf-8")
            (t / "data.json").write_text(json.dumps(embedded()), encoding="utf-8")
            (t / "q.json").write_text(json.dumps([[k, q] for k, q, _ in QUERIES]), encoding="utf-8")
            res = subprocess.run(["node", str(t / "driver.js"), str(t / "nlq.js"), str(t / "data.json"), str(t / "q.json")],
                                 capture_output=True, text=True, check=True, encoding="utf-8")
        for (_, q, expected), got in zip(QUERIES, json.loads(res.stdout)):
            for key, value in expected.items():
                self.assertEqual(got.get(key), value, f"{q}: {key}")
            self.assertEqual(got["understood"], expected.get("understood", True), q)


if __name__ == "__main__":
    unittest.main()
