import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from assert_operational_evidence import assess


class EvidenceGateTest(unittest.TestCase):
    def test_monitor_requires_every_check_and_identity(self):
        r = {"status": "PASS", "commit": "a" * 40, "run_id": "123",
             "checks": {"registry": {"status": "PASS"}}}
        self.assertTrue(assess("monitor", r)[0])
        r["checks"]["coverage"] = {"status": "INCOMPLETE"}
        self.assertFalse(assess("monitor", r)[0])
        r["checks"]["coverage"] = {"status": "PASS"}
        r["run_id"] = "LOCAL"
        self.assertFalse(assess("monitor", r)[0])

    def test_poll_requires_real_operation(self):
        self.assertFalse(assess("drive-poll", {"status": "BLOCKED"})[0])
        self.assertFalse(assess("drive-poll", {"status": "INITIALIZED"})[0])
        self.assertFalse(assess("drive-poll", {"status": "OK"})[0])
        self.assertTrue(assess("drive-poll", {"status": "OK", "change_count": 0})[0])

    def test_cli_missing_or_initialized_checkpoint_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            report = root / "status.json"
            state = root / "state.json"
            report.write_text(json.dumps({"status": "OK", "change_count": 0}))
            command = [sys.executable, str(ROOT / "tools/assert_operational_evidence.py"),
                       "drive-poll", str(report), "--checkpoint", str(state)]
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)
            state.write_text(json.dumps({"page_token": "t0", "initialized": True}))
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)
            state.write_text(json.dumps({"page_token": "t1", "initialized": False}))
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)


if __name__ == "__main__":
    unittest.main()
