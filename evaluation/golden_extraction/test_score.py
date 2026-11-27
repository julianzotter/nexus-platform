import copy
import json
import tempfile
import unittest
from pathlib import Path

from score import load_rows, score


class ScoringTests(unittest.TestCase):
    def setUp(self):
        self.gold = {"A": {"case_id": "A", "label": "HOLD", "fields": {"v": None, "u": "m"}}}
        self.pred = copy.deepcopy(self.gold)

    def test_exact(self):
        self.assertEqual(score(self.gold, self.pred)["status"], "PASS")

    def test_null_zero(self):
        self.pred["A"]["fields"]["v"] = 0
        self.assertEqual(score(self.gold, self.pred)["status"], "FAIL")

    def test_absence_null(self):
        del self.pred["A"]["fields"]["v"]
        self.assertEqual(score(self.gold, self.pred)["exact_fields"], 1)

    def test_unit(self):
        self.pred["A"]["fields"]["u"] = "mm"
        self.assertEqual(score(self.gold, self.pred)["status"], "FAIL")

    def test_class(self):
        self.pred["A"]["label"] = "ALLOW"
        self.assertEqual(score(self.gold, self.pred)["macro_f1"], 0)

    def test_unexpected(self):
        self.pred["B"] = dict(self.pred["A"], case_id="B")
        self.assertEqual(score(self.gold, self.pred)["unexpected_cases"], ["B"])

    def test_missing_case(self):
        self.assertEqual(score(self.gold, {})["missing_cases"], ["A"])

    def test_extra_field(self):
        self.pred["A"]["fields"]["x"] = 2
        self.assertEqual(score(self.gold, self.pred)["extra_fields"], 1)

    def test_bad_input(self):
        row = json.dumps(self.gold["A"])
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "rows"
            for data in ("", row+"\n"+row, row.replace("null","NaN"), row.replace('"v": null','"v": 0, "v": null')):
                with self.subTest(data=data):
                    path.write_text(data, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        load_rows(path)


if __name__ == "__main__":
    unittest.main()
