import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import monitor_repo as monitor


def detail(number: int, mergeable: bool | None) -> dict:
    return {"number": number, "mergeable": mergeable,
            "head": {"sha": "head"}, "base": {"sha": "base"}, "draft": False}


class MonitorTests(unittest.TestCase):
    def test_all_pages_and_conflicting_pr_are_reported(self):
        pages = [[{"number": 1}], [{"number": 2}]]
        with patch.object(monitor, "github_json", side_effect=[pages, [detail(1, True)], [detail(2, False)]]):
            report = monitor.inspect_prs("owner/repo")
        self.assertEqual(report["status"], "CONFLICT")
        self.assertEqual([item["number"] for item in report["items"]], [1, 2])

    def test_unknown_mergeability_is_retried_but_not_claimed_clean(self):
        responses = [[[{"number": 1}]]] + [[detail(1, None)]] * 3
        with patch.object(monitor, "github_json", side_effect=responses), patch.object(monitor.time, "sleep"):
            self.assertEqual(monitor.inspect_prs("owner/repo")["status"], "UNKNOWN")

    def test_mergeability_can_become_available_after_retry(self):
        responses = [[[{"number": 1}]], [detail(1, None)], [detail(1, True)]]
        with patch.object(monitor, "github_json", side_effect=responses), patch.object(monitor.time, "sleep"):
            self.assertEqual(monitor.inspect_prs("owner/repo")["status"], "PASS")

    def test_api_failure_does_not_look_like_no_open_prs(self):
        with patch.object(monitor, "github_json", side_effect=RuntimeError("denied")):
            self.assertEqual(monitor.inspect_prs("owner/repo")["status"], "ERROR")

    def test_empty_successful_pr_inventory_is_distinct_from_api_failure(self):
        with patch.object(monitor, "github_json", return_value=[[]]):
            self.assertEqual(monitor.inspect_prs("owner/repo"), {"status": "PASS", "items": []})

    def test_validation_failure_does_not_skip_knowledge_check(self):
        results = [{"exit_code": 1, "stdout": "FAIL", "stderr": ""},
                   {"exit_code": 2, "stdout": "NO_DATA", "stderr": ""}]
        with patch.object(monitor, "command", side_effect=results):
            checks = monitor.validation_checks()
        self.assertEqual(checks["registry"]["status"], "FAIL")
        self.assertEqual(checks["knowledge"]["status"], "NO_DATA")

    def test_no_data_and_unmeasured_coverage_do_not_become_overall_pass(self):
        self.assertEqual(monitor.overall_status({"knowledge": {"status": "NO_DATA"}}), "INCOMPLETE")
        self.assertEqual(monitor.overall_status({"coverage": {"status": "INCOMPLETE"}}), "INCOMPLETE")
        self.assertEqual(monitor.overall_status({"prs": {"status": "CONFLICT"}}), "ATTENTION")

    def test_failure_report_is_written_and_main_returns_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            args = ["monitor", "--repository", "owner/repo", "--report-dir", directory]
            with patch.object(sys, "argv", args), patch.object(monitor, "validation_checks", return_value={
                "registry": {"status": "FAIL"}}), patch.object(monitor, "inspect_prs", return_value={
                "status": "ERROR", "items": []}), patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": ""}):
                self.assertEqual(monitor.main(), 1)
            report = json.loads((Path(directory) / "report.json").read_text())
            self.assertEqual(report["status"], "ATTENTION")
            self.assertTrue((Path(directory) / "report.md").exists())

    def test_invalid_repository_never_executes_gh(self):
        with patch.object(monitor, "github_json") as api:
            self.assertEqual(monitor.inspect_prs("bad;command")["status"], "ERROR")
            api.assert_not_called()


if __name__ == "__main__":
    unittest.main()
