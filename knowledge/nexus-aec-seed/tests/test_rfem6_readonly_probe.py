"""Exercise only the offline RFEM preflight path; no licensed API requests."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from rfem6_readonly_probe import inspect_sdk, read_application_info  # noqa: E402


class RFEMPreflightTests(unittest.TestCase):
    def test_offline_never_runs_solver(self) -> None:
        report = inspect_sdk()
        self.assertEqual(report["rfem_connection"], "NOT_RUN")
        self.assertEqual(report["calculations"], "NOT_RUN")
        self.assertFalse(report["model_changed"])

    def test_live_must_acknowledge_cost(self) -> None:
        with self.assertRaises(PermissionError):
            read_application_info(inspect_sdk(), acknowledged=False)


if __name__ == "__main__":
    unittest.main()
