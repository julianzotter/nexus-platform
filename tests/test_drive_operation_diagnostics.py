import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import drive_auth_check
import drive_changes_poll as polling
from delivery_errors import DeliveryError

ENV = {"GOOGLE_ACCESS_TOKEN": "TEST_ONLY_TOKEN"}


class DriveOperationDiagnosticsTests(unittest.TestCase):
    def test_auth_refresh_error_identifies_operation_without_environment(self):
        with patch.object(drive_auth_check, "get_access_token", side_effect=DeliveryError("HTTP_400")):
            result = drive_auth_check.check_access(environ=ENV)
        self.assertEqual(result["operation"], "oauth.token_refresh")
        self.assertEqual(result["reason"], "HTTP_400")
        self.assertNotIn("TEST_ONLY_TOKEN", json.dumps(result))

    def test_work_metadata_error_identifies_operation(self):
        with patch.object(drive_auth_check, "get_access_token", return_value="TEST_ONLY_TOKEN"), patch.object(
                drive_auth_check.DriveClient, "call", side_effect=DeliveryError("HTTP_400")):
            result = drive_auth_check.check_access(require_write=True, environ=ENV)
        self.assertEqual(result["operation"], "drive.files.get_work_metadata")
        self.assertEqual(result["status"], "BLOCKED")
        self.assertNotIn("TEST_ONLY_TOKEN", json.dumps(result))

    def test_poll_auth_failure_preserves_checkpoint(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = root / "state.json"
            state.write_text('{"page_token":"cursor"}')
            with patch.object(polling, "get_access_token", side_effect=DeliveryError("HTTP_400")):
                result = self.run_poll(root)
            self.assertEqual(result["operation"], "oauth.token_refresh")
            self.assertEqual(state.read_text(), '{"page_token":"cursor"}')

    def test_poll_reports_exact_drive_operation_and_preserves_checkpoint(self):
        for checkpoint, failed_operation in [
            ({}, "drive.changes.getStartPageToken"),
            ({"page_token": "cursor"}, "drive.changes.list"),
        ]:
            with self.subTest(operation=failed_operation), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                state = root / "state.json"
                before = json.dumps(checkpoint)
                state.write_text(before)
                with patch.object(polling, "get_access_token", return_value="TEST_ONLY_TOKEN"), patch.object(
                        polling.DriveReader, "get", side_effect=DeliveryError("HTTP_400")):
                    result = self.run_poll(root)
                self.assertEqual(result["operation"], failed_operation)
                self.assertEqual(result["reason"], "HTTP_400")
                self.assertEqual(state.read_text(), before)
                self.assertNotIn("TEST_ONLY_TOKEN", json.dumps(result))

    def run_poll(self, root):
        args = ["poll", "--state", str(root / "state.json"), "--out", str(root / "out")]
        with patch.object(sys, "argv", args), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(polling.main(), 2)
        return json.loads((root / "out/status.json").read_text())
