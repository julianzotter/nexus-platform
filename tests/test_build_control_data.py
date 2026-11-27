"""Control Panel data build: deterministic, schema-valid, sourced from repo registries."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build_control_data as bcd  # noqa: E402


def head() -> str:
    return subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], check=True,
                          capture_output=True, text=True).stdout.strip()


def test_build_is_deterministic_and_complete(tmp_path: Path) -> None:
    commit = head()
    assert bcd.main(["--source-commit", commit, "--out", str(tmp_path / "a"), "--snapshot", "missing.json"]) == 0
    assert bcd.main(["--source-commit", commit, "--out", str(tmp_path / "b"), "--snapshot", "missing.json"]) == 0
    a = (tmp_path / "a/control-data.json").read_bytes()
    assert a == (tmp_path / "b/control-data.json").read_bytes()
    data = json.loads(a)
    registry = json.loads((ROOT / bcd.WORKFLOWS).read_text(encoding="utf-8"))
    matrix = json.loads((ROOT / bcd.ROLES).read_text(encoding="utf-8"))
    assert len(data["nexus"]["workflows"]["items"]) == len(registry["workflows"])
    assert [r[0] for r in data["roles"]] == [r["id"] for r in matrix["roles"]]
    assert data["nexus"]["monitor"]["status"] == "NO_DATA"  # never PASS without a snapshot
    assert (tmp_path / "a/index.html").exists()


def test_rejects_bad_commit(tmp_path: Path) -> None:
    assert bcd.main(["--source-commit", "abc", "--out", str(tmp_path)]) == 1


def test_report_classification() -> None:
    ids = {"0185"}
    assert bcd.classify_report("26_11_10_1555_ID06_STATUSREPORT_X_0185.md", ids)[2] == "REGISTERED"
    assert bcd.classify_report("26_10_27_1815_ID06_X_0127.md", ids)[2] == "NOT_IN_LEDGER"
    assert bcd.classify_report("26_11_25_0015_ID05_STATUS_X_LEDGER-PENDING.md", ids) == ("2026-11-25", "ID05", "LEDGER_PENDING")
    assert bcd.classify_report("26_11_24_ID03_X_LEDGER-PENDING.md", ids)[2] == "NAME_NONCONFORM"  # HHMM missing


def test_repo_stats_match_git(tmp_path: Path) -> None:
    commit = head()
    stats = bcd.build_repo_stats(ROOT, commit)
    files = subprocess.run(["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", commit], check=True,
                           capture_output=True, text=True).stdout.splitlines()
    commits = subprocess.run(["git", "-C", str(ROOT), "rev-list", "--count", commit], check=True,
                             capture_output=True, text=True).stdout.strip()
    assert stats["files"] == len(files)
    assert stats["commits"] == int(commits)
    assert stats == bcd.build_repo_stats(ROOT, commit)  # deterministic
    assert len(stats["commitsPerDay"]) <= 14
