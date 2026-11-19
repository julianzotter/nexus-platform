"""Prevent duplicate weekly META_WISSEN source ownership in the seed catalog."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SchedulerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.seed = json.loads((ROOT / "seed/nexus_aec_top20_seed_v1.json").read_text("utf-8"))
        cls.contract = json.loads((ROOT / "config/meta_wissen_scheduler_contract_v1.json").read_text("utf-8"))

    def test_source_ownership_is_disjoint_and_seeded(self) -> None:
        known = {s["id"] for s in self.seed["sources"]}
        assigned: set[str] = set()
        for task in self.contract["automations"]:
            src = set(task["source_ids"])
            self.assertTrue(src <= known)
            self.assertFalse(assigned & src)
            assigned |= src
        self.assertEqual(len(assigned), 12)

    def test_both_schedulers_weekly_vienna(self) -> None:
        self.assertEqual(len(self.contract["automations"]), 2)
        for task in self.contract["automations"]:
            self.assertTrue(task["is_enabled"])
            self.assertIn("DTSTART;TZID=Europe/Vienna:", task["schedule"])
            self.assertIn("RRULE:FREQ=WEEKLY;BYDAY=MO", task["schedule"])


if __name__ == "__main__":
    unittest.main()
