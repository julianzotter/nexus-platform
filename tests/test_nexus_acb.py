"""Tests for tools/nexus_acb.py (ACB v0.1). Local fixture roles only — no identity claims."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import nexus_acb as acb  # noqa: E402


def run(root: Path, *args: str) -> int:
    return acb.main(["--root", str(root), "message", *args])


def test_init_creates_layout(tmp_path: Path) -> None:
    assert run(tmp_path / "acb", "init") == 0
    for sub in acb.SUBDIRS:
        assert (tmp_path / "acb" / sub).is_dir()
    assert (tmp_path / "acb" / acb.LEDGER).exists()


def test_roundtrip_send_ack_reply(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = tmp_path / "acb"
    assert run(root, "send", "--from", "ID02", "--to", "ID03", "--subject", "PING", "--body", "hello\n", "--artifact-id", "0130") == 0
    sent = json.loads(capsys.readouterr().out)
    assert run(root, "inbox", "--for", "ID03") == 0
    inbox = json.loads(capsys.readouterr().out)
    assert inbox["count"] == 1 and inbox["messages"][0]["verdict"] == "PASS"
    assert run(root, "ack", sent["path"], "--by", "ID03") == 0
    assert (root / "PROCESSED" / Path(sent["path"]).name).exists()
    assert not Path(sent["path"]).exists()
    assert run(root, "send", "--from", "ID03", "--to", "ID02", "--subject", "PONG",
               "--body", "ack\n", "--reply-to", sent["msg_id"], "--artifact-id", "0131") == 0
    capsys.readouterr()
    assert run(root, "ledger-verify") == 0
    assert json.loads(capsys.readouterr().out)["entries"] == 3


def test_tampered_body_fails_verify_and_goes_to_failed(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = tmp_path / "acb"
    assert run(root, "send", "--from", "ID02", "--to", "ID03", "--subject", "X", "--body", "orig\n", "--artifact-id", "0132") == 0
    path = Path(json.loads(capsys.readouterr().out)["path"])
    path.write_text(path.read_text(encoding="utf-8").replace("orig", "tampered"), encoding="utf-8")
    assert run(root, "verify", str(path)) == 2
    capsys.readouterr()
    assert run(root, "ack", str(path), "--by", "ID03") == 2
    assert (root / "FAILED" / path.name).exists()


def test_invalid_role_and_wrong_ack_identity(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = tmp_path / "acb"
    assert run(root, "send", "--from", "ID-02", "--to", "ID03", "--subject", "X", "--body", "b", "--artifact-id", "0133") == 1
    assert run(root, "send", "--from", "ID02", "--to", "ID03", "--subject", "X", "--body", "b", "--artifact-id", "0133") == 0
    path = json.loads(capsys.readouterr().out)["path"]
    assert run(root, "ack", path, "--by", "ID06") == 1


def test_ledger_chain_break_detected(tmp_path: Path) -> None:
    root = tmp_path / "acb"
    assert run(root, "send", "--from", "ID02", "--to", "ID03", "--subject", "X", "--body", "b", "--artifact-id", "0134") == 0
    ledger = root / acb.LEDGER
    ledger.write_text(ledger.read_text(encoding="utf-8").replace('"readback": "PASS"', '"readback": "XX"'))
    assert run(root, "ledger-verify") == 1


def test_naming_schema_and_missing_artifact_id(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = tmp_path / "acb"
    assert run(root, "send", "--from", "ID02", "--to", "ID03", "--subject", "Ping Test", "--body", "b",
               "--artifact-id", "0140") == 0
    name = Path(json.loads(capsys.readouterr().out)["path"]).name
    assert name.endswith("_ID02_ACB-MSG_PING-TEST-0140_v0.1.0.md")
    assert run(root, "send", "--from", "ID02", "--to", "ID03", "--subject", "X", "--body", "b", "--artifact-id", "12") == 1
