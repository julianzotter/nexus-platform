"""Tests for tools/naming_gate.py (CI gate for YY_MM_DD_HHMM_ID##_THEMA_###)."""
from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("naming_gate", ROOT / "tools" / "naming_gate.py")
ng = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ng)
IDS = ng.valid_ids()


def test_valid_ids_follow_roles_v12() -> None:
    assert {"ID01", "ID02", "ID03", "ID06"} <= IDS
    assert "ID93" not in IDS and "ID09" not in IDS and "ID10" not in IDS


def test_conforming_and_open_names() -> None:
    assert ng.judge("WORK/26_11_25_1405_ID06_STATUS_THEMA_014.md", IDS)[0] == "konform"
    assert ng.judge("WORK/26_11_25_1405_ID03_STATUS_LEDGER-PENDING.md", IDS)[0] == "Nummer offen"


def test_violations() -> None:
    assert ng.judge("reports/26_11_25_0010_ID-UNVERIFIED_X_LEDGER-PENDING.md", IDS)[0] == "Verstoss"
    verdict, reason = ng.judge("WORK/26_11_25_1405_ID93_STATUS_001.md", IDS)
    assert verdict == "Verstoss" and "ID93" in reason
    assert ng.judge("WORK/26_11_25_14_05_ID06_X_001.md", IDS)[0] == "Verstoss"
    assert ng.judge("WORK/2026-10-26_1445_PLAN_DRAFT.md", IDS)[0] == "Verstoss"


def test_candidates() -> None:
    assert ng.is_candidate("docs/x/26_11_25_1405_ID06_A_001.md")
    assert ng.is_candidate("WORK/REPORTS/notes.md")
    assert not ng.is_candidate("WORK/_AGBS.md")
    assert not ng.is_candidate("WORK/README.md")
    assert not ng.is_candidate("tools/naming_gate.py")


def test_strict_counts_open_numbers() -> None:
    paths = ["WORK/26_11_25_1405_ID03_STATUS_LEDGER-PENDING.md"]
    assert ng.evaluate(paths, strict=False)[1] == 0
    assert ng.evaluate(paths, strict=True)[1] == 1


def test_fix_hint_never_invents_numbers() -> None:
    hint = ng.fix_hint("reports/26_11_25_0010_ID-UNVERIFIED_X_LEDGER-PENDING.md")
    assert "Ledger" in hint and "Rollen-ID" in hint
    assert not re.search(r"\d{3}", hint)


def test_gate_passes_on_head_against_itself() -> None:
    res = subprocess.run([sys.executable, str(ROOT / "tools" / "naming_gate.py"), "--base", "HEAD"],
                         capture_output=True, text=True)
    assert res.returncode == 0, res.stdout


def test_folder_move_is_not_a_new_name() -> None:
    status = ("A\tWORK/REPORTS/new.md\n"
              "R100\tprototypes/x/26_11_25_1603_ID03_X_DRAFT.html\tarchive/prototypes/x/26_11_25_1603_ID03_X_DRAFT.html\n"
              "R095\treports/a.md\treports/b.md\n")
    assert ng.new_names(status) == ["WORK/REPORTS/new.md", "reports/b.md"]
