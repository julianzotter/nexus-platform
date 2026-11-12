import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from scheduler_runtime import inspect_runtime, inspect_workflow, WORKFLOWS
import monitor_repo as monitor

NOW = datetime(2026, 11, 11, 12, 30, tzinfo=timezone.utc)
SPEC = WORKFLOWS[0]
META = {"id": 42, "state": "active", "path": ".github/workflows/nexus-monitor.yml"}


def runs() -> list[dict]:
    return [{"id": 100 + i, "workflow_id": 42, "run_attempt": 1,
             "event": "schedule", "head_branch": "main", "head_sha": "a" * 40,
             "created_at": (NOW - timedelta(minutes=10 + 60 * i)).isoformat(),
             "status": "completed", "conclusion": "success",
             "html_url": f"https://github.com/owner/repo/actions/runs/{100+i}"}
            for i in range(3)]


def inspect(items: list[dict], meta: dict | None = None) -> dict:
    api = Mock(side_effect=[meta or META, {"workflow_runs": items}])
    return inspect_workflow("owner/repo", SPEC, api, NOW)


class RuntimeTests(unittest.TestCase):
    def test_success_keeps_concrete_run_and_commit_identity(self):
        result = inspect(runs())
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["runs"][0]["id"], 100)
        self.assertEqual(result["runs"][0]["head_sha"], "a" * 40)

    def test_disabled_workflow_is_failure_without_run_query(self):
        api = Mock(return_value={**META, "state": "disabled_inactivity"})
        result = inspect_workflow("owner/repo", SPEC, api, NOW)
        self.assertEqual(result["reason"], "WORKFLOW_NOT_ACTIVE")
        self.assertEqual(api.call_count, 1)

    def test_empty_or_short_history_does_not_pass(self):
        for count, status in [(0, "NO_DATA"), (1, "INCOMPLETE"), (2, "INCOMPLETE")]:
            with self.subTest(count=count):
                self.assertEqual(inspect(runs()[:count])["status"], status)

    def test_foreign_evidence_fails_closed(self):
        for field, value in [("event", "workflow_dispatch"), ("head_branch", "feature"),
                             ("workflow_id", 99), ("head_sha", "UNKNOWN"), ("id", True),
                             ("created_at", "2026-11-11T12:00:00"),
                             ("created_at", "2027-01-01T00:00:00Z"), ("status", "unknown")]:
            with self.subTest(field=field, value=value):
                data = runs()
                data[0][field] = value
                self.assertEqual(inspect(data)["status"], "ERROR")

    def test_duplicate_id_is_not_three_runs(self):
        data = runs()
        data[1]["id"] = data[0]["id"]
        self.assertEqual(inspect(data)["status"], "ERROR")

    def test_successful_retry_does_not_prove_original_schedule_success(self):
        data = runs()
        data[0]["run_attempt"] = 2
        self.assertEqual(inspect(data)["reason"], "RETRY_NOT_INITIAL_TRIGGER_SUCCESS")

    def test_failed_cancelled_skipped_and_unknown_conclusions(self):
        for conclusion in ["failure", "cancelled", "skipped", None, "neutral", "timed_out"]:
            with self.subTest(conclusion=conclusion):
                data = runs()
                data[1]["conclusion"] = conclusion
                self.assertEqual(inspect(data)["reason"], "RECENT_RUN_NOT_SUCCESSFUL")

    def test_stale_history_and_gap_fail(self):
        data = runs()
        for run in data:
            run["created_at"] = (NOW - timedelta(hours=5)).isoformat()
        self.assertEqual(inspect(data)["reason"], "STALE")
        data = runs()
        data[2]["created_at"] = (NOW - timedelta(hours=5)).isoformat()
        self.assertEqual(inspect(data)["reason"], "OBSERVED_RUN_GAP")

    def test_current_run_does_not_hide_three_prior_successes(self):
        data = runs()
        pending = {**data[0], "id": 999, "status": "in_progress", "conclusion": None,
                   "created_at": NOW.isoformat()}
        self.assertEqual(inspect([pending] + data)["status"], "PASS")

    def test_stuck_run_and_stale_completed_run_fail(self):
        data = runs()
        data[2]["status"] = "in_progress"
        self.assertEqual(inspect(data)["reason"], "OVERDUE_RUN")
        pending = {**data[0], "id": 999, "status": "queued", "conclusion": None}
        for index, run in enumerate(data):
            run.update(status="completed", created_at=(NOW - timedelta(minutes=100+60*index)).isoformat())
        self.assertEqual(inspect([pending]+data)["reason"], "LAST_COMPLETED_RUN_STALE")

    def test_sort_order_is_timestamp_not_api_order(self):
        self.assertEqual(inspect(list(reversed(runs())))["runs"][0]["id"], 100)

    def test_invalid_payload_and_api_error_never_expose_error_text(self):
        for payload in [None, {}, {"workflow_runs": None}, {"workflow_runs": [None]}]:
            api = Mock(side_effect=[META, payload])
            self.assertEqual(inspect_workflow("owner/repo", SPEC, api, NOW)["status"], "ERROR")
        api = Mock(side_effect=RuntimeError("secret=NEVER_EMIT"))
        result = inspect_runtime("owner/repo", api, NOW)
        self.assertEqual(result["status"], "ERROR")
        self.assertNotIn("NEVER_EMIT", json.dumps(result))

    def test_metadata_pass_is_never_end_to_end_proof_and_queries_are_bounded(self):
        def response(endpoint: str) -> dict:
            filename = endpoint.split("/workflows/")[1].split("/")[0]
            if "/runs?" not in endpoint:
                return {**META, "path": f".github/workflows/{filename}"}
            self.assertIn("per_page=100&page=1", endpoint)
            data = runs()
            for i, run in enumerate(data):
                run["event"] = "workflow_run" if filename == "nexus-delivery.yml" else "schedule"
                run["created_at"] = (NOW-timedelta(minutes=10+30*i)).isoformat()
            return {"workflow_runs": data}
        api = Mock(side_effect=response)
        result = inspect_runtime("owner/repo", api, NOW)
        self.assertEqual(api.call_count, 6)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["end_to_end"], "UNVERIFIED")

    def test_invalid_repo_does_not_call_api(self):
        api = Mock()
        self.assertEqual(inspect_runtime("owner/repo?token=x", api, NOW)["status"], "ERROR")
        api.assert_not_called()

    def test_monitor_report_preserves_failure_without_self_deadlock(self):
        with tempfile.TemporaryDirectory() as directory:
            args = ["monitor", "--repository", "owner/repo", "--report-dir", directory]
            runtime = {"status": "FAIL", "end_to_end": "UNVERIFIED", "workflows": []}
            with patch.object(sys, "argv", args), patch.object(monitor, "validation_checks", return_value={
                "registry": {"status": "PASS"}}), patch.object(monitor, "inspect_prs", return_value={
                "status": "PASS"}), patch.object(monitor, "inspect_runtime", return_value=runtime) as api:
                self.assertEqual(monitor.main(), 0)
                api.assert_called_once()
            report = json.loads((Path(directory)/"report.json").read_text())
            self.assertEqual(report["scheduler_runtime"]["status"], "FAIL")
            self.assertIn("end-to-end: **UNVERIFIED**", (Path(directory)/"report.md").read_text())

    def test_runtime_api_does_not_paginate_or_leak_stderr(self):
        with patch.object(monitor, "command", return_value={"exit_code": 0, "stdout": "{}"}) as command:
            self.assertEqual(monitor.github_runtime_json("repos/o/r"), {})
            command.assert_called_once_with(["gh", "api", "repos/o/r"])
        with patch.object(monitor, "command", return_value={"exit_code": 1, "stderr": "SECRET"}):
            with self.assertRaisesRegex(RuntimeError, "^Runtime metadata unavailable$"):
                monitor.github_runtime_json("repos/o/r")


if __name__ == "__main__":
    unittest.main()
