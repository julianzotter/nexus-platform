"""Tests for tools/report_ledger.py and registry/report-ledger.jsonl."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("report_ledger", ROOT / "tools" / "report_ledger.py")
rl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rl)


def entry(nr: str, role: str = "ID06", path: str = "AGENTS.md", status: str = "ALLOCATED") -> dict:
    return dict(zip(rl.KEYS, [nr, role, "T", path, status, "2026-11-27T00:00:00Z", "ID01", "test"]))


def test_committed_ledger_is_valid() -> None:
    assert rl.check(rl.load()) == []


def test_every_numbered_file_is_registered() -> None:
    nrs = {e["nr"] for e in rl.load()}
    assert set(rl.numbered_files().values()) <= nrs


def test_next_number_is_max_plus_one() -> None:
    assert rl.next_number([]) == "0001"
    assert rl.next_number([entry("0009"), entry("0210")]) == "0211"


def test_entry_errors() -> None:
    ids = rl.role_ids()
    assert rl.entry_errors(1, entry("0001"), ids) == []
    assert rl.entry_errors(1, entry("01"), ids)
    assert rl.entry_errors(1, entry("0001", role="ID93"), ids)
    assert rl.entry_errors(1, entry("0001", path="does/not/exist.md"), ids)
    assert rl.entry_errors(1, entry("0001", path="gone.md", status="RETIRED"), ids) == []
    assert rl.entry_errors(1, entry("0001", status="GUESSED"), ids)


def test_duplicate_numbers_fail() -> None:
    errs = rl.check(rl.load() + [entry("0001")])
    assert any("already used" in e for e in errs)
