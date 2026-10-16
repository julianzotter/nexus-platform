import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from generate_catalog import render_catalog

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None


def load(name):
    return json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))


class SchemaTests(unittest.TestCase):
    def test_catalog_matches_committed_draft(self):
        coverage = json.loads((ROOT / "registry/coverage-per-source.json").read_text(encoding="utf-8"))
        expected = (ROOT / "registry/catalog-draft.yaml").read_text(encoding="utf-8")
        self.assertEqual(render_catalog(coverage, "coverage-per-source.json"), expected)

    @unittest.skipIf(jsonschema is None, "jsonschema not installed")
    def test_registry_files_validate(self):
        coverage = json.loads((ROOT / "registry/coverage-per-source.json").read_text(encoding="utf-8"))
        jsonschema.validate(coverage, load("coverage.schema.json"))
        schema = load("file-record.schema.json")
        for line in (ROOT / "registry/file-registry.jsonl").read_text(encoding="utf-8").splitlines():
            if line.strip():
                jsonschema.validate(json.loads(line), schema)

    @unittest.skipIf(jsonschema is None, "jsonschema not installed")
    def test_schemas_are_valid_and_reject_guessed_metrics(self):
        for name in ("file-record", "coverage", "task", "evidence", "knowledge-item"):
            jsonschema.Draft202012Validator.check_schema(load(f"{name}.schema.json"))
        bad = {"formula": "indexed / accessible", "total": {
            "status": "INCOMPLETE", "reason": "x", "discovered": 5, "accessible": None,
            "indexed": None, "skipped": None, "error": None, "coverage_percent": None}, "sources": {}}
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(bad, load("coverage.schema.json"))


if __name__ == "__main__":
    unittest.main()
