"""Tests for tools/nexus-tower/nexus_tower.py (read-only local Control Tower)."""
import importlib.util
import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "tools" / "nexus-tower" / "nexus_tower.py"
spec = importlib.util.spec_from_file_location("nexus_tower", SRC)
tower = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tower)


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
def test_name_check(name, verdict):
    assert tower.name_check(name)[0] == verdict


@pytest.fixture()
def work(tmp_path, monkeypatch):
    (tmp_path / "26_11_10_1748_ID03_STATUSREPORT_CHECK.md").write_text(
        "---\nstatus: ABWEICHUNG\nproblems:\n- A\n- B\n---\nbody\n", encoding="utf-8")
    (tmp_path / "26_11_10_0086_SOFTWARE_OLD_v0.1.0.py").write_text("x", encoding="utf-8")
    monkeypatch.setattr(tower, "WORK", tmp_path)
    return tmp_path


def test_state_and_gate(work):
    state = tower.state()
    assert state["total"] == 2
    assert state["gate"]["status"] == "ABWEICHUNG"
    assert state["gate"]["problems"] == "A, B"


def test_mcp_dispatch(work):
    init = tower.mcp_dispatch({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                               "params": {"protocolVersion": "2025-06-18"}})
    assert init["result"]["protocolVersion"] == "2025-06-18"
    assert tower.mcp_dispatch({"jsonrpc": "2.0", "method": "notifications/initialized"}) is None
    names = [t["name"] for t in tower.mcp_dispatch({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})["result"]["tools"]]
    assert names == ["work_state", "naming_check", "gate_status"]
    call = tower.mcp_dispatch({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                               "params": {"name": "naming_check", "arguments": {}}})
    data = json.loads(call["result"]["content"][0]["text"])
    assert data["counts"]["Verstoss"] == 1
    assert tower.mcp_dispatch({"jsonrpc": "2.0", "id": 4, "method": "nope"})["error"]["code"] == -32601


def test_http_round_trip_and_origin_guard(work):
    server = ThreadingHTTPServer(("127.0.0.1", 0), tower.Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        assert json.load(urllib.request.urlopen(base + "/api/state"))["total"] == 2
        body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "ping"}).encode()
        ok = urllib.request.Request(base + "/mcp", data=body, headers={"Content-Type": "application/json"})
        assert json.load(urllib.request.urlopen(ok))["result"] == {}
        bad = urllib.request.Request(base + "/mcp", data=body, headers={"Origin": "https://evil.example"})
        with pytest.raises(urllib.error.HTTPError) as err:
            urllib.request.urlopen(bad)
        assert err.value.code == 403
    finally:
        server.shutdown()
