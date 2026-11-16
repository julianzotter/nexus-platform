"""Unit and evidence gate regression tests; no engineering computations."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_knowledge import validate  # noqa: E402


BASE = {
    "record_id": "test-1", "evidence_status": "UNVERIFIED",
    "source": {"source_uri": "https://www.oib.or.at/", "locator": "section 1", "content_sha256": None},
    "scope": {"country": "AT", "binding_status": "DRAFT", "edition": "2027", "effective_date": None},
    "engineering_release": "NOT_RELEASED", "properties": [],
}


class KnowledgeGateTests(unittest.TestCase):
    def test_draft_never_becomes_binding(self) -> None:
        self.assertEqual(validate(BASE), [])
        self.assertTrue(validate({**BASE, "engineering_release": "ID01_APPROVED"}))

    def test_austrian_binding_needs_state(self) -> None:
        trial = {**BASE, "scope": {**BASE["scope"], "binding_status": "BINDING_VERIFIED"}}
        self.assertTrue(any("federal_state" in x for x in validate(trial)))

    def test_lca_declared_unit_required(self) -> None:
        field = {
            "name": "gwp", "unit": "kg CO2e", "stage": "A1-A3", "locator": "EPD tab 3",
            "dataset_version": "2026", "declared_unit": None, "verification": "UNVERIFIED",
        }
        self.assertTrue(any("declared unit" in x for x in validate({**BASE, "properties": [field]})))


if __name__ == "__main__":
    unittest.main()
