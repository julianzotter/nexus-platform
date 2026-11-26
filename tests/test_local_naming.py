"""Tests for local_stack/nexus_local/naming.py (moved from tools/nexus-tower, archived 2026-11-26)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "local_stack"))

from nexus_local import naming  # noqa: E402


@pytest.mark.parametrize("name,verdict", [
    ("26_11_10_1605_ID06_ANALYSIS_X_0187.md", "konform"),
    ("26_11_10_1754_ID06_SCRIPT_X-v0.1.0_LEDGER-PENDING.py", "Nummer offen"),
    ("26_11_10_1748_ID03_STATUSREPORT_CHECK.md", "Abweichung"),
    ("26_11_10_0086_SOFTWARE_OLD_v0.1.0.py", "Verstoss"),
    ("26_11_10_18_02_ID-UNVERIFIED_CPLM_UNREGISTERED.md", "Verstoss"),
    ("26_11_10_ID06_SKILL_X.md", "Verstoss"),
    ("26_11_10_1720_WO-X_v0.2.md", "Verstoss"),
    ("NEXUS_X.md", "Verstoss"),
    ("_AGBS.md", "Steuerdatei"),
    ("NEXUS_OLD_UEBERHOLT.md", "ueberholt"),
])
def test_name_check(name: str, verdict: str) -> None:
    assert naming.name_check(name)[0] == verdict


def test_report_and_gate(tmp_path: Path) -> None:
    (tmp_path / "26_11_10_1748_ID03_STATUSREPORT_CHECK.md").write_text(
        "---\nstatus: ABWEICHUNG\nproblems:\n- A\n- B\n---\nbody\n", encoding="utf-8")
    (tmp_path / "26_11_10_0086_SOFTWARE_OLD_v0.1.0.py").write_text("x", encoding="utf-8")
    files, total = naming.list_files(tmp_path)
    assert total == 2 and len(files) == 2
    report = naming.naming_report(tmp_path)
    assert report["counts"] == {"Abweichung": 1, "Verstoss": 1}
    gate = naming.read_gate(tmp_path)
    assert gate["status"] == "ABWEICHUNG" and gate["problems"] == "A, B"


def test_empty_folder(tmp_path: Path) -> None:
    assert naming.read_gate(tmp_path) == {}
    assert naming.naming_report(tmp_path)["problems"] == []
