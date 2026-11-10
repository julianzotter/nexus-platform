"""Tests for tools/nexus-counter/nexus_counter.py (single-writer artifact counter)."""
import importlib.util
import os
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "tools" / "nexus-counter" / "nexus_counter.py"
spec = importlib.util.spec_from_file_location("nexus_counter", SRC)
counter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(counter)

HEADER = "ID,DATE,TYPE,TITLE,DRIVE_ID,FOLDER,SHA256,VALIDITY,MATURITY,SUPERSEDES,CANON,ACTOR,NAME_SCHEMA_OK,NOTE\n"


def setup(tmp_path):
    work = tmp_path / "WORK"
    work.mkdir()
    ledger = tmp_path / "ledger.csv"
    ledger.write_text(HEADER + "0181,2026-11-10,X,b.md,,,,,,,,ID03,1,\nPENDING,2026-11-10,X,c.md,,,,,,,,ID06,0,\n", encoding="utf-8")
    log = tmp_path / "history.log"
    log.write_text("", encoding="utf-8")
    old = work / "26_11_10_1754_ID06_SCRIPT_X-v0.1.0_LEDGER-PENDING.py"
    new = work / "26_11_10_1805_ID07_HANDOFF_X_UNREGISTERED.md"
    old.write_text("a", encoding="utf-8")
    new.write_text("b", encoding="utf-8")
    os.utime(old, (1000, 1000))
    os.utime(new, (2000, 2000))
    (work / "26_11_10_1605_ID06_ANALYSIS_X_0187.md").write_text("d", encoding="utf-8")
    (work / "_AGBS.md").write_text("e", encoding="utf-8")
    return work, ledger, log


def test_dry_run_changes_nothing(tmp_path):
    work, ledger, log = setup(tmp_path)
    before = sorted(p.name for p in work.iterdir())
    assert counter.allocate(work, ledger, log, apply=False) == 2
    assert sorted(p.name for p in work.iterdir()) == before
    assert ledger.read_text(encoding="utf-8").count("\n") == 3
    assert log.read_text(encoding="utf-8") == ""


def test_apply_counts_past_numbers_in_file_names(tmp_path):
    work, ledger, log = setup(tmp_path)
    assert counter.allocate(work, ledger, log, apply=True) == 2
    names = sorted(p.name for p in work.iterdir())
    assert "26_11_10_1754_ID06_SCRIPT_X-v0.1.0_0188.py" in names   # oldest first, after 0187
    assert "26_11_10_1805_ID07_HANDOFF_X_0189.md" in names
    rows = ledger.read_text(encoding="utf-8").splitlines()
    assert rows[-2].startswith("0188,2026-11-10,SCRIPT,") and rows[-1].startswith("0189,2026-11-10,HANDOFF,")
    assert len(log.read_text(encoding="utf-8").splitlines()) == 2
    assert counter.allocate(work, ledger, log, apply=True) == 0   # second run: nothing left
