import json
import sys
import tempfile
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from validate_knowledge import SCHEMA, knowledge_files, validate_dir, validate_item

SCHEMA_DOC = json.loads(SCHEMA.read_text(encoding="utf-8"))
RELATION = json.loads((ROOT / "schemas" / "relation.schema.json").read_text(encoding="utf-8"))
NORM = {"standard": "EN 1992-1-1", "edition": "2011", "clause": "6.2.2"}
SIGNOFF = {"reviewer": "ID-01", "decision": "APPROVED", "decided_at": "2026-10-18T12:00:00Z", "result_version": "1.0"}
LEGACY = {
    "id": "KO-LEGACY-1", "kind": "workflow", "title": "t", "source_file_id": "a48a8748013ade84",
    "version": "1.0.0", "status": "DRAFT", "engineering_result": False,
    "source_url": "https://example.invalid/x", "source_revision": "0" * 40, "source_sha256": "f" * 64,
    "observations": {"runner": "ubuntu-24.04"}, "validation_scope": "configuration only",
}


def item(**kw):
    base = {"id": "k1", "kind": "solver", "title": "t", "source_file_id": "0123456789abcdef",
            "version": "1.0", "status": "VALID", "engineering_result": True, "norm": NORM, "signoff": SIGNOFF}
    base.update(kw)
    return {k: v for k, v in base.items() if v is not None}


class ItemContractTests(unittest.TestCase):
    def test_schema_is_valid(self):
        jsonschema.Draft202012Validator.check_schema(SCHEMA_DOC)
        jsonschema.Draft202012Validator.check_schema(RELATION)

    def test_legacy_item_stays_valid(self):
        self.assertEqual(validate_item(LEGACY, SCHEMA_DOC), [])

    def test_extended_fields_are_checked(self):
        self.assertTrue(validate_item({**LEGACY, "content_hash_sha256": "xyz"}, SCHEMA_DOC))
        self.assertTrue(validate_item({**LEGACY, "source_revision": "abc"}, SCHEMA_DOC))
        self.assertTrue(validate_item({**LEGACY, "labels": ["a", "a"]}, SCHEMA_DOC))

    def test_classification_never_guessed(self):
        unresolved = {"system": "Uniclass", "edition": None, "code": None, "uri": None, "mapping_status": "UNRESOLVED"}
        self.assertEqual(validate_item({**LEGACY, "classification": [unresolved]}, SCHEMA_DOC), [])
        self.assertTrue(validate_item({**LEGACY, "classification": [{**unresolved, "mapping_status": "RESOLVED"}]}, SCHEMA_DOC))

    def test_signoff_timestamp_needs_timezone(self):
        naive = {**SIGNOFF, "decided_at": "2026-10-18T12:00:00"}
        self.assertTrue(validate_item(item(signoff=naive), SCHEMA_DOC))
        self.assertTrue(validate_item(item(signoff={**SIGNOFF, "decided_at": "not-a-date"}), SCHEMA_DOC))

    def test_stale_signoff_still_rejected(self):
        self.assertTrue(validate_item(item(version="1.1"), SCHEMA_DOC))


class RecursiveReadTests(unittest.TestCase):
    def test_nested_files_are_validated(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "structural").mkdir()
            (root / "structural" / "bad.json").write_text(json.dumps(item(signoff=None)), encoding="utf-8")
            (root / "ok.json").write_text(json.dumps(LEGACY), encoding="utf-8")
            self.assertEqual([p.name for p in knowledge_files(root)], ["ok.json", "bad.json"])
            errors = validate_dir(root)
            self.assertTrue(errors and all(e.startswith("structural/bad.json") for e in errors))

    def test_missing_directory_has_no_files(self):
        self.assertEqual(knowledge_files(ROOT / "does-not-exist"), [])


class RelationContractTests(unittest.TestCase):
    BASE = {"relation_id": "R-1", "source_object_id": "KO-1", "target_object_id": "KO-2",
            "relation_type": "DEPENDS_ON", "source_anchor": "doc#clause-6.2.2", "evidence_ref": "EV-1",
            "derivation_method": "HUMAN", "validation_status": "UNVALIDATED"}

    def test_human_relation_valid(self):
        jsonschema.validate(self.BASE, RELATION)

    def test_semantic_relation_needs_confidence_and_model(self):
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate({**self.BASE, "derivation_method": "SEMANTIC"}, RELATION)
        jsonschema.validate({**self.BASE, "derivation_method": "SEMANTIC", "confidence": 0.8, "model_version": "m1"}, RELATION)

    def test_unknown_relation_type_and_missing_evidence_rejected(self):
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate({**self.BASE, "relation_type": "SIMILAR"}, RELATION)
        bad = dict(self.BASE)
        del bad["evidence_ref"]
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(bad, RELATION)


if __name__ == "__main__":
    unittest.main()
