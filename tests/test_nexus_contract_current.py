"""Current-source receipt and adopted filename contract regression tests."""
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "mcp_bridge"))
from nexus_contract import load_governance, report_filename


class CurrentContractTests(unittest.TestCase):
    def test_current_folder_source_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            work = root / "WORK"
            work.mkdir()
            overrides = {key: f"{key}.md" for key in ("agbs", "folder", "manifest", "baseline")}
            for relative in overrides.values():
                (root / relative).write_text("fixture policy", encoding="utf-8")
            result = load_governance(work, overrides)
            self.assertEqual(result["policies"]["folder"]["configured_source_id"],
                             "1nDjF78dq3l8PGpXsauzBz1bzHescDSwv")
            self.assertFalse(result["authority_verified"])

    def test_adopted_actor_position_and_vienna_boundary(self):
        moment = datetime(2026, 11, 16, 23, 30, tzinfo=timezone.utc)
        self.assertEqual(report_filename("STATUS.md", "0212", "ID02", moment),
                         "26_11_17_0030_ID02_STATUS_0212.md")

    def test_legacy_alias_normalized_without_rewriting_history(self):
        moment = datetime(2026, 7, 1, 22, 30, tzinfo=timezone.utc)
        self.assertEqual(report_filename("STATUS.md", "0212", "ID-03", moment),
                         "26_07_02_0030_ID03_STATUS_0212.md")


if __name__ == "__main__":
    unittest.main()
