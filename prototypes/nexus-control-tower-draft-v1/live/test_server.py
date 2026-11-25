"""Tests for bounded NEXUS WORK and GitHub snapshot, no network required."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import server


class PanelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.files = [
            {"id": "abc", "name": "WO-20261125-PILOT.md",
             "modifiedTime": "2026-11-25T15:00:00Z"},
            {"id": "def", "name": "STATUSREPORT-NEXUS.md",
             "modifiedTime": "2026-11-25T15:04:00Z"},
        ]

    def test_metadata_not_ack(self) -> None:
        w, r = server.project_records(self.files)
        self.assertEqual(len(w), 1)
        self.assertEqual(len(r), 1)
        self.assertEqual(w[0]["ack"], "NOT_OBSERVED")

    def test_snapshot_source_time_not_check_time(self) -> None:
        result = server.build_snapshot(self.files, [])
        self.assertEqual(result["observedAt"], "2026-11-25T15:04:00Z")
        self.assertEqual(result["syncStatus"], "SOURCE_READ_OK")
        self.assertEqual(len(result["sourceRevision"]), 64)

    def test_repeat_is_idempotent_revision(self) -> None:
        a = server.build_snapshot(self.files, [])["sourceRevision"]
        b = server.build_snapshot(list(reversed(self.files)), [])["sourceRevision"]
        self.assertEqual(a, b)

    def test_missing_credentials_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with patch.dict("os.environ", {"GOOGLE_DRIVE_ACCESS_TOKEN": ""}):
                code, result = server.refresh(Path(tmp, "state.json"))
            self.assertEqual(code, 503)
            self.assertEqual(result["syncStatus"], "ERROR")
            self.assertFalse(Path(tmp, "state.json").exists())

    def test_last_good_retained_on_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "state.json")
            original = server.build_snapshot(self.files, [])
            server.save_atomic(path, original)
            with patch("server.drive_inventory", side_effect=RuntimeError("OAUTH_DENIED")):
                code, result = server.refresh(path)
            self.assertEqual(code, 200)
            self.assertEqual(result["syncStatus"], "STALE")
            self.assertEqual(result["sourceRevision"], original["sourceRevision"])
            self.assertEqual(json.loads(path.read_text()), original)

    def test_drive_pagination_fail_closed(self) -> None:
        response = {"files": self.files, "nextPageToken": "loop"}
        with patch("server.request_json", return_value=response):
            with self.assertRaisesRegex(RuntimeError, "DRIVE_PAGINATION_INCOMPLETE"):
                server.drive_inventory("dummy")

    def test_github_pr_pagination_fail_closed(self) -> None:
        with patch("server.request_json", return_value=[{}] * 100):
            with self.assertRaisesRegex(RuntimeError, "PAGINATION"):
                server.github_open_prs(None)


if __name__ == "__main__":
    unittest.main()
