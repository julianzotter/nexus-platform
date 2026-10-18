import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from validate_knowledge import SCHEMA, validate_item

SCHEMA_DOC = json.loads(SCHEMA.read_text(encoding="utf-8"))
NORM = {"standard": "EN 1992-1-1", "edition": "2011", "national_annex": "ÖNORM B 1992-1-1", "clause": "6.2.2"}
SIGNOFF = {"reviewer": "ID-01", "decision": "APPROVED", "decided_at": "2026-10-18T12:00:00Z", "result_version": "1.0"}


def item(**kw):
    base = {"id": "k1", "kind": "solver", "title": "t", "source_file_id": "0123456789abcdef",
            "version": "1.0", "status": "VALID", "engineering_result": True, "norm": NORM, "signoff": SIGNOFF}
    base.update(kw)
    return {k: v for k, v in base.items() if v is not None}


class KnowledgeTests(unittest.TestCase):
    def test_valid_signed_item(self):
        self.assertEqual(validate_item(item(), SCHEMA_DOC), [])

    def test_missing_signoff_rejected(self):
        self.assertTrue(validate_item(item(signoff=None), SCHEMA_DOC))

    def test_rejected_decision_not_valid(self):
        self.assertTrue(validate_item(item(signoff={**SIGNOFF, "decision": "REJECTED"}), SCHEMA_DOC))

    def test_stale_signoff_rejected(self):
        self.assertTrue(validate_item(item(version="1.1"), SCHEMA_DOC))

    def test_norm_clause_requires_norm(self):
        self.assertTrue(validate_item(item(kind="norm_clause", engineering_result=None, signoff=None, norm=None), SCHEMA_DOC))

    def test_draft_without_signoff_ok(self):
        self.assertEqual(validate_item(item(status="DRAFT", signoff=None), SCHEMA_DOC), [])


if __name__ == "__main__":
    unittest.main()
