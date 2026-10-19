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

    def test_workflow_inventory_reports_declared_triggers_without_runtime_claim(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scheduled.yml").write_text(
                "name: Scheduled poll # main monitor\n"
                "on:\n"
                "    schedule:\n"
                "    - cron: '17 * * * *' # hourly\n"
                "    - {cron: \"7,37 * * * *\"}\n"
                "    - cron: 11 2 * * * # unquoted comment\n"
                "    workflow_dispatch: {}\n"
                "    push: {branches: [main]}\n"
                "permissions:\n"
                "  contents: read\n",
                encoding="utf-8")
            (root / "inline.yaml").write_text(
                "name: Inline poll\n"
                "\"on\": [push, pull_request] # PR and push\n",
                encoding="utf-8")
            (root / "scalar.yml").write_text("name: Scalar\non: push\n", encoding="utf-8")
            (root / "blankname.yaml").write_text(
                "name: # use file name\non: push\n", encoding="utf-8")
            (root / "flow.yaml").write_text(
                "name: Flow mapping\n"
                "on: {push: {tags: [v1, v2], branches: [main, dev]}, workflow_dispatch: {}}\n",
                encoding="utf-8")
            (root / "nested.yaml").write_text(
                "name: Nested sequence\n"
                "on:\n"
                "  push:\n"
                "    branches:\n"
                "      - main\n"
                "      - dev\n",
                encoding="utf-8")
            (root / "regular-schedule.yml").write_text(
                "name: Regular schedule\n"
                "on:\n"
                "  schedule:\n"
                "    - cron: '3 * * * *'\n"
                "  workflow_dispatch:\n",
                encoding="utf-8")
            report = monitor.inspect_workflow_configuration(root)
        self.assertEqual(report["state"], "OBSERVED")
        self.assertFalse(report["runtime_verified"])
        self.assertEqual(report["workflows"][0], {
            "file": "blankname.yaml", "name": "blankname", "events": ["push"], "schedules": [],
        })
        self.assertEqual(report["workflows"][1], {
            "file": "flow.yaml", "name": "Flow mapping",
            "events": ["push", "workflow_dispatch"], "schedules": [],
        })
        self.assertEqual(report["workflows"][2], {
            "file": "inline.yaml", "name": "Inline poll",
            "events": ["push", "pull_request"], "schedules": [],
        })
        self.assertEqual(report["workflows"][3], {
            "file": "nested.yaml", "name": "Nested sequence", "events": ["push"], "schedules": [],
        })
        self.assertEqual(report["workflows"][4], {
            "file": "regular-schedule.yml", "name": "Regular schedule",
            "events": ["schedule", "workflow_dispatch"], "schedules": ["3 * * * *"],
        })
        self.assertEqual(report["workflows"][5], {
            "file": "scalar.yml", "name": "Scalar", "events": ["push"], "schedules": [],
        })
        self.assertEqual(report["workflows"][6], {
            "file": "scheduled.yml", "name": "Scheduled poll",
            "events": ["schedule", "workflow_dispatch", "push"],
            "schedules": ["17 * * * *", "7,37 * * * *", "11 2 * * *"],
        })

    def test_workflow_inventory_distinguishes_no_files(self):
        with tempfile.TemporaryDirectory() as directory:
            report = monitor.inspect_workflow_configuration(Path(directory))
        self.assertEqual(report["state"], "NO_DATA")
        self.assertFalse(report["runtime_verified"])

    def test_workflow_inventory_reports_unreadable_files(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "unreadable.yaml"
            path.touch()
            with patch.object(monitor.Path, "read_text", side_effect=OSError):
                report = monitor.inspect_workflow_configuration(Path(directory))
        self.assertEqual(report["state"], "ERROR")
        self.assertEqual(report["unreadable_files"], [{"file": "unreadable.yaml", "reason": "UNREADABLE"}])

    def test_workflow_inventory_reports_non_utf8_files(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "invalid.yaml").write_bytes(b"\xff")
            report = monitor.inspect_workflow_configuration(Path(directory))
        self.assertEqual(report["state"], "ERROR")
        self.assertEqual(report["unreadable_files"], [{"file": "invalid.yaml", "reason": "UNREADABLE"}])

    def test_workflow_inventory_reports_partial_read_when_some_files_are_unreadable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "good.yml").write_text("name: Good\non: push\n", encoding="utf-8")
            (root / "bad.yml").write_bytes(b"\xff")
            report = monitor.inspect_workflow_configuration(root)
        self.assertEqual(report["state"], "PARTIAL")
        self.assertEqual(len(report["workflows"]), 1)
        self.assertEqual(report["unreadable_files"], [{"file": "bad.yml", "reason": "UNREADABLE"}])

    def test_report_explains_workflow_inventory_is_not_execution_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            monitor.write_report({
                "status": "INCOMPLETE",
                "checks": {},
                "commit": "abc",
                "observed_at": "2026-10-19T00:00:00+00:00",
                "automation_configuration": {
                    "workflows": [{"name": "Poll", "file": "poll.yml",
                                   "events": ["schedule"], "schedules": ["*/5 * * * *"]}]
                },
            }, Path(directory))
            text = (Path(directory) / "report.md").read_text(encoding="utf-8")
        self.assertIn("does not prove that a workflow ran", text)
        self.assertIn("`*/5 * * * *`", text)

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
