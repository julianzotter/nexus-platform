"""Tests for local_stack/nexus_local (Linux CI; Windows paths/Job Object are NOT_RUN here)."""
from __future__ import annotations

import json
import os
import socket
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "local_stack"))

from nexus_local import bridge, gpt_to_skill, mcp_gateway, reporter, util  # noqa: E402
from nexus_local.bridge import BridgeConfigError, BridgeEngine, Ledger, Rule, unsafe_rel, validate_rules  # noqa: E402
from nexus_local.winproc import AlreadyRunning, InstanceLock  # noqa: E402


# ------------------------------------------------------------------ helpers
def free_port() -> int:
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p


def make_engine(tmp: Path, mode="mirror", settle=0.0, **kw):
    src, dst = tmp / "src", tmp / "dstroot" / "dst"
    src.mkdir(parents=True); (tmp / "dstroot").mkdir()
    rule = Rule(name="r1", src=src, dst=dst, mode=mode, settle_seconds=settle, **kw)
    eng = BridgeEngine([rule], Ledger(tmp / "state" / "b.sqlite"))
    return eng, rule, src, dst


def cycle(eng, rule, n=2):
    res = None
    for _ in range(n):  # first pass registers pending, second copies (settle=0)
        res = eng.run_cycle(rule)
    return res


# ------------------------------------------------------------------ bridge
def test_copy_new_file_and_no_delete(tmp_path):
    eng, rule, src, dst = make_engine(tmp_path)
    (src / "a.md").write_text("hallo", encoding="utf-8")
    r = eng.run_cycle(rule)
    assert r.copied == 1 and (dst / "a.md").read_text() == "hallo"
    assert eng.run_cycle(rule).unchanged == 1
    (src / "a.md").unlink()  # source deletion must never propagate
    cycle(eng, rule)
    assert (dst / "a.md").exists()


def test_settle_waits_for_stable_file(tmp_path):
    eng, rule, src, dst = make_engine(tmp_path, settle=3600)
    (src / "b.md").write_text("x")
    r = cycle(eng, rule, 3)
    assert r.waiting == 1 and not (dst / "b.md").exists()


def test_external_dest_change_creates_conflict_copy(tmp_path):
    eng, rule, src, dst = make_engine(tmp_path)
    (src / "c.md").write_text("v1"); cycle(eng, rule)
    (dst / "c.md").write_text("edited in onedrive")       # someone edits the mirror
    time.sleep(0.01); (src / "c.md").write_text("v2-source"); cycle(eng, rule)
    assert (dst / "c.md").read_text() == "edited in onedrive"  # never overwritten
    conflicts = list(dst.glob("c.CONFLICT-*-r1.md"))
    assert len(conflicts) == 1 and conflicts[0].read_text() == "v2-source"
    cycle(eng, rule)  # deterministic name: no repeated conflict files
    assert len(list(dst.glob("c.CONFLICT-*"))) == 1


def test_own_copy_update_side_by_side_by_default(tmp_path):
    eng, rule, src, dst = make_engine(tmp_path)
    (src / "d.md").write_text("v1"); cycle(eng, rule)
    time.sleep(0.01); (src / "d.md").write_text("v2"); cycle(eng, rule)
    assert (dst / "d.md").read_text() == "v1"
    ups = list(dst.glob("d.UPDATE-*-r1.md"))
    assert len(ups) == 1 and ups[0].read_text() == "v2"


def test_own_copy_replace_opt_in_archives_previous(tmp_path):
    eng, rule, src, dst = make_engine(tmp_path, allow_replace_own_copy=True)
    (src / "d.md").write_text("v1"); cycle(eng, rule)
    time.sleep(0.01); (src / "d.md").write_text("v2"); cycle(eng, rule)
    assert (dst / "d.md").read_text() == "v2"
    versions = list((dst / ".nexus_versions").glob("d.*.md"))
    assert len(versions) == 1 and versions[0].read_text() == "v1"


def test_external_edit_never_adopted_as_baseline(tmp_path):
    eng, rule, src, dst = make_engine(tmp_path, allow_replace_own_copy=True)
    (src / "g.md").write_text("v1"); cycle(eng, rule)
    (dst / "g.md").write_text("external")
    time.sleep(0.01); (src / "g.md").write_text("v2"); cycle(eng, rule)
    time.sleep(0.01); (src / "g.md").write_text("v3"); cycle(eng, rule)
    assert (dst / "g.md").read_text() == "external"
    assert len(list(dst.glob("g.CONFLICT-*"))) == 2


def test_dry_run_writes_nothing(tmp_path):
    src, dst = tmp_path / "s", tmp_path / "root" / "d"
    src.mkdir(); (tmp_path / "root").mkdir(); (src / "a.md").write_text("x")
    rule = Rule(name="r", src=src, dst=dst, settle_seconds=0)
    eng = BridgeEngine([rule], Ledger(tmp_path / "st.sqlite"), dry_run=True)
    eng.run_cycle(rule); eng.run_cycle(rule)
    assert not dst.exists()
    assert any(e["kind"] == "dry_run_copy" for e in eng.ledger.recent_events())


@pytest.mark.skipif(os.name == "nt", reason="symlink creation needs privileges on Windows")
def test_symlinks_not_followed(tmp_path):
    eng, rule, src, dst = make_engine(tmp_path)
    secret = tmp_path / "outside.md"; secret.write_text("private")
    (src / "link.md").symlink_to(secret)
    (tmp_path / "outdir").mkdir(); (tmp_path / "outdir" / "x.md").write_text("p")
    (src / "linkdir").symlink_to(tmp_path / "outdir", target_is_directory=True)
    cycle(eng, rule)
    assert not dst.exists() or not any(dst.rglob("*.md"))


def test_inbox_never_overwrites(tmp_path):
    eng, rule, src, dst = make_engine(tmp_path, mode="inbox")
    dst.mkdir(); (dst / "e.md").write_text("existing")
    (src / "e.md").write_text("incoming"); cycle(eng, rule)
    assert (dst / "e.md").read_text() == "existing"
    assert len(list(dst.glob("e.CONFLICT-*"))) == 1


def test_identical_dest_is_noop(tmp_path):
    eng, rule, src, dst = make_engine(tmp_path)
    dst.mkdir(); (dst / "f.md").write_text("same"); (src / "f.md").write_text("same")
    r = cycle(eng, rule)
    assert r.unchanged >= 1 and not list(dst.glob("*.CONFLICT-*"))


def test_secrets_temp_and_shortcuts_skipped(tmp_path):
    eng, rule, src, dst = make_engine(tmp_path)
    for n in (".env", "x.key", "token.json", "~$doc.docx", "a.gdoc", ".~nexus-1.tmp", "credentials_x.json"):
        (src / n).write_text("s")
    cycle(eng, rule)
    assert not dst.exists() or not any(dst.iterdir())


def test_source_missing_blocks_and_dest_root_never_created(tmp_path):
    rule = Rule(name="r", src=tmp_path / "nope", dst=tmp_path / "x" / "y")
    eng = BridgeEngine([rule], Ledger(tmp_path / "s.sqlite"))
    assert eng.run_cycle(rule).blocked == "SOURCE_NOT_MOUNTED"
    (tmp_path / "nope").mkdir()
    assert eng.run_cycle(rule).blocked == "DEST_ROOT_NOT_MOUNTED" and not (tmp_path / "x").exists()


def test_rule_cycle_and_nesting_rejected(tmp_path):
    a, b = tmp_path / "A", tmp_path / "B"
    with pytest.raises(BridgeConfigError):
        validate_rules([Rule("x", a, b / "in"), Rule("y", b, a / "in")])
    with pytest.raises(BridgeConfigError):
        validate_rules([Rule("x", a, a / "sub")])
    validate_rules([Rule("x", a, b / "mirror"), Rule("y", tmp_path / "C", a / "_inbox")])  # one-way, no cycle


@pytest.mark.parametrize("rel,ok", [("a/b.md", True), ("../x", False), ("a/CON.txt", False), ("a/b.md:ads", False),
                                    ("x./y", False), ("a/ b ", False), ("/abs", False), ("a/b?.md", False)])
def test_unsafe_rel(rel, ok):
    assert (unsafe_rel(rel) is None) is ok


def test_crash_journal_reconciled(tmp_path):
    led = Ledger(tmp_path / "j.sqlite")
    target = tmp_path / "t.md"; target.write_text("abc")
    led.journal("r", "t.md", str(target), util.sha256_bytes(b"abc"), "PREPARED")
    led.journal("r", "u.md", str(tmp_path / "missing.md"), "0" * 64, "PREPARED")
    BridgeEngine([], led)
    states = dict(led.db.execute("SELECT rel, state FROM journal").fetchall())
    assert states == {"t.md": "PUBLISHED", "u.md": "ABANDONED"}


def test_create_only_never_replaces(tmp_path):
    p = tmp_path / "x.md"; p.write_text("orig")
    with pytest.raises(util.DestinationExists):
        util.atomic_write_bytes(p, b"new", create_only=True)
    assert p.read_text() == "orig" and not list(tmp_path.glob(".~nexus-*"))


def test_instance_lock_exclusive(tmp_path):
    a = InstanceLock(tmp_path / "l.lock").acquire()
    if os.name != "nt":
        import subprocess
        code = ("import sys;sys.path.insert(0,%r);from nexus_local.winproc import InstanceLock,AlreadyRunning\n"
                "try:\n InstanceLock(__import__('pathlib').Path(%r)).acquire();print('GOT')\n"
                "except AlreadyRunning:\n print('BUSY')") % (str(Path(bridge.__file__).parents[1]), str(tmp_path / "l.lock"))
        out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True).stdout.strip()
        assert out == "BUSY"
    a.release()


def test_vienna_fallback_dst():
    from datetime import datetime, timezone
    assert util._vienna_fallback(datetime(2026, 7, 1, 12, tzinfo=timezone.utc)).hour == 14
    assert util._vienna_fallback(datetime(2026, 11, 25, 12, tzinfo=timezone.utc)).hour == 13


# ------------------------------------------------------------------ servers
class FakeSup:
    def __init__(self, runtime: Path):
        self.boot_id = "test"
        self.token = "a" * 64
        self.cfg = {"links": {}}
        self.tasks = {}
        self.log_dir = runtime
        self.bridge_engine = None
        self.stopped = False

    def status(self):
        return {"service": "x", "version": "0", "boot_id": "test", "tasks": [], "job_object": False}

    def action(self, name, action):
        return {"error": "UNKNOWN_TASK"}

    def shutdown(self):
        self.stopped = True


def serve(server):
    t = threading.Thread(target=server.serve_forever, daemon=True); t.start()
    return server


def req(url, method="GET", headers=None, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    if data is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=5) as resp:
            return resp.status, dict(resp.headers), json.loads(resp.read() or b"null")
    except urllib.error.HTTPError as e:
        raw = e.read()
        return e.code, dict(e.headers), (json.loads(raw) if raw else None)


@pytest.fixture
def tower(tmp_path):
    from nexus_local import control_tower
    sup = FakeSup(tmp_path)
    port = free_port()
    srv = serve(control_tower.build_server(sup, port))
    yield sup, port
    srv.shutdown(); srv.server_close()


def test_tower_static_public_data_protected(tower):
    sup, port = tower
    base = f"http://127.0.0.1:{port}"
    code, hdr, _ = req(base + "/healthz")
    assert code == 200 and "default-src 'none'" in hdr["Content-Security-Policy"]
    assert req(base + "/api/status")[0] == 401
    assert req(base + "/api/status", headers={"Authorization": "Bearer " + "b" * 64})[0] == 401
    assert req(base + "/api/status", headers={"Authorization": "Bearer " + sup.token})[0] == 200
    with urllib.request.urlopen(base + "/") as r:
        html = r.read().decode()
    assert sup.token not in html


def test_tower_rejects_foreign_host_and_origin(tower):
    sup, port = tower
    s = socket.create_connection(("127.0.0.1", port))
    s.sendall(f"GET /healthz HTTP/1.1\r\nHost: evil.example:{port}\r\nConnection: close\r\n\r\n".encode())
    assert s.recv(100).startswith(b"HTTP/1.1 421"); s.close()
    code, _, _ = req(f"http://127.0.0.1:{port}/api/task", "POST",
                     {"Authorization": "Bearer " + sup.token, "Origin": "http://evil.example"}, {"name": "x", "action": "stop"})
    assert code == 403
    code, _, _ = req(f"http://127.0.0.1:{port}/api/task", "POST",
                     {"Authorization": "Bearer " + sup.token, "Sec-Fetch-Site": "cross-site"}, {"name": "x", "action": "stop"})
    assert code == 403


def test_tower_port_exclusive(tower):
    from nexus_local import control_tower
    sup, port = tower
    with pytest.raises(OSError):
        control_tower.build_server(sup, port)


@pytest.fixture
def mcp(tmp_path):
    work = tmp_path / "WORK"; work.mkdir()
    (work / "26_11_25_1200_ID05_TEST_LEDGER-PENDING.md").write_text("Bemessung Holzbalken EC5 Nachweis", encoding="utf-8")
    (work / ".env").write_text("SECRET=1")
    cfg = {"paths": {"work": str(work)}, "ollama": {"default_model": "m"}, "search": {}, "mcp": {"require_token": True}}
    port = free_port()
    srv = serve(mcp_gateway.build_server(cfg, "c" * 64, port))
    yield port, "c" * 64
    srv.shutdown(); srv.server_close()


def modern(port, tok, method, params=None, name=None, pv="2026-07-28", hdr_pv=None, mid=1):
    p = dict(params or {})
    p["_meta"] = {"io.modelcontextprotocol/protocolVersion": pv, "io.modelcontextprotocol/clientInfo": {"name": "t", "version": "1"}}
    h = {"Authorization": "Bearer " + tok, "MCP-Protocol-Version": hdr_pv or pv, "Mcp-Method": method,
         "Accept": "application/json, text/event-stream"}
    if name:
        h["Mcp-Name"] = name
    body = {"jsonrpc": "2.0", "method": method, "params": p}
    if mid is not None:
        body["id"] = mid
    return req(f"http://127.0.0.1:{port}/mcp", "POST", h, body)


def test_mcp_modern_discover_list_call(mcp):
    port, tok = mcp
    code, _, d = modern(port, tok, "server/discover")
    assert code == 200 and "2026-07-28" in d["result"]["supportedVersions"]
    code, _, l = modern(port, tok, "tools/list")
    names = {t["name"] for t in l["result"]["tools"]}
    assert {"work_list", "work_read", "work_search", "local_llm"} <= names and "web_search" not in names
    assert not any("write" in n or "submit" in n for n in names)
    code, _, r = modern(port, tok, "tools/call", {"name": "work_search", "arguments": {"query": "holzbalken"}}, "work_search")
    assert r["result"]["structuredContent"]["hits"][0]["path"].endswith("TEST_LEDGER-PENDING.md")
    code, _, r = modern(port, tok, "tools/call", {"name": "work_list", "arguments": {}}, "work_list")
    assert all(i["name"] != ".env" for i in r["result"]["structuredContent"]["items"])


def test_mcp_naming_and_gate_tools(mcp):
    """Tools moved from tools/nexus-tower (archived 2026-11-26)."""
    port, tok = mcp
    names = {t["name"] for t in modern(port, tok, "tools/list")[2]["result"]["tools"]}
    assert {"naming_check", "gate_status"} <= names
    r = modern(port, tok, "tools/call", {"name": "naming_check", "arguments": {}}, "naming_check")[2]
    assert r["result"]["structuredContent"]["counts"] == {"Nummer offen": 1}
    r = modern(port, tok, "tools/call", {"name": "gate_status", "arguments": {}}, "gate_status")[2]
    assert r["result"]["structuredContent"] == {}
    r = modern(port, tok, "tools/call", {"name": "naming_check", "arguments": {"subdir": "../x"}}, "naming_check")[2]
    assert r["result"]["isError"] is True


def test_mcp_modern_header_rules(mcp):
    port, tok = mcp
    assert modern(port, tok, "tools/list", hdr_pv="2025-11-25")[2]["error"]["code"] == -32020
    code, _, e = modern(port, tok, "tools/list", pv="1900-01-01")
    assert code == 400 and e["error"]["code"] == -32022 and "2026-07-28" in e["error"]["data"]["supported"]
    code, _, e = modern(port, tok, "tools/call", {"name": "work_list", "arguments": {}}, "other")
    assert code == 400 and e["error"]["code"] == -32020
    code, _, e = modern(port, tok, "nope/method")
    assert code == 404 and e["error"]["code"] == -32601
    assert modern(port, tok, "tools/list", mid=None)[0] == 202
    assert req(f"http://127.0.0.1:{port}/mcp")[0] == 405


def test_mcp_path_guards(mcp):
    port, tok = mcp
    for path in ("../x.md", ".env", "a:b.md", "CON.md"):
        _, _, r = modern(port, tok, "tools/call", {"name": "work_read", "arguments": {"path": path}}, "work_read")
        assert r["result"]["isError"]
    _, _, r = modern(port, tok, "tools/call", {"name": "work_read", "arguments": {"path": "x", "bogus": 1}}, "work_read")
    assert "UNKNOWN_ARGUMENT" in r["result"]["content"][0]["text"]


def test_mcp_legacy_session_flow_and_auth(mcp):
    port, tok = mcp
    url = f"http://127.0.0.1:{port}/mcp"
    assert req(url, "POST", {}, {"jsonrpc": "2.0", "id": 1, "method": "tools/list"})[0] == 401
    h = {"Authorization": "Bearer " + tok}
    code, hdr, init = req(url, "POST", h, {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                                            "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "x", "version": "1"}}})
    assert code == 200 and init["result"]["protocolVersion"] == "2025-06-18"
    sid = {k.lower(): v for k, v in hdr.items()}["mcp-session-id"]
    h2 = {**h, "Mcp-Session-Id": sid, "MCP-Protocol-Version": "2025-06-18"}
    assert req(url, "POST", h2, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})[2]["error"]["code"] == -32002
    assert req(url, "POST", h2, {"jsonrpc": "2.0", "method": "notifications/initialized"})[0] == 202
    assert len(req(url, "POST", h2, {"jsonrpc": "2.0", "id": 3, "method": "tools/list"})[2]["result"]["tools"]) >= 5
    assert req(url, "POST", {**h2, "Mcp-Session-Id": "f" * 32}, {"jsonrpc": "2.0", "id": 4, "method": "tools/list"})[0] == 404
    assert req(url, "POST", h, [{"jsonrpc": "2.0", "id": 5, "method": "ping"}])[0] == 400  # no batches


def test_mcp_body_limits(mcp):
    port, tok = mcp
    s = socket.create_connection(("127.0.0.1", port))
    s.sendall(f"POST /mcp HTTP/1.1\r\nHost: 127.0.0.1:{port}\r\nAuthorization: Bearer {tok}\r\n"
              f"Content-Type: application/json\r\nContent-Length: -5\r\nConnection: close\r\n\r\n".encode())
    assert s.recv(100).startswith(b"HTTP/1.1 411"); s.close()
    s = socket.create_connection(("127.0.0.1", port))
    s.sendall(f"POST /mcp HTTP/1.1\r\nHost: 127.0.0.1:{port}\r\nAuthorization: Bearer {tok}\r\n"
              f"Content-Type: application/json\r\nContent-Length: 999999999\r\nConnection: close\r\n\r\n".encode())
    assert s.recv(100).startswith(b"HTTP/1.1 413"); s.close()


# ------------------------------------------------------------------ gpt -> skill
def _gpt(tmp: Path, title="EC5 Holzbau-Bemessung", extra=None):
    d = tmp / "exports" / "ec5"; (d / "knowledge").mkdir(parents=True)
    meta = {"account": "GPT-PRIVATE", "gpt_id": "g-abc123XYZ", "title": title, "source_uri": "https://chatgpt.com/g/g-abc123XYZ",
            "source_sha256": "a" * 64, "capture_status": "CONFIG_CAPTURED", "actions": [{"name": "rfem"}], **(extra or {})}
    (d / "gpt.json").write_text(json.dumps(meta), encoding="utf-8")
    (d / "instructions.md").write_text("Du bist ein Holzbau-Statiker.\nRechne nach EN 1995-1-1.", encoding="utf-8")
    (d / "knowledge" / "kmod.csv").write_text("klasse;kmod\n1;0.6\n", encoding="utf-8")
    return tmp / "exports", tmp / "staging"


def test_gpt_to_skill_converts_and_is_idempotent(tmp_path):
    exp, stg = _gpt(tmp_path)
    assert gpt_to_skill.run(exp, stg)["converted"] == 1
    skill = next(stg.glob("*/SKILL.md")).read_text("utf-8")
    assert skill.startswith("---\nname: ec5-holzbau-bemessung-") and "MIGRATED_UNTESTED" in skill and "rfem" in skill
    man = json.loads(next(stg.glob("*/source-manifest.json")).read_text())
    assert man["conversion_status"] == "MIGRATED_UNTESTED" and man["approval"] == "PENDING_ID01"
    assert next(stg.glob("*/references/kmod.csv")).exists()
    assert gpt_to_skill.run(exp, stg)["unchanged"] == 1


def test_gpt_to_skill_rejects_unknown_fields(tmp_path):
    exp, stg = _gpt(tmp_path, extra={"api_key": "x"})
    assert gpt_to_skill.run(exp, stg)["rejected"] == 1


# ------------------------------------------------------------------ reporter
def test_report_name_format():
    from datetime import datetime, timezone
    n = reporter.report_name("ID08", "LOCALSTACK-STATUS", datetime(2026, 11, 25, 18, 5, tzinfo=timezone.utc))
    assert n == "26_11_25_1805_ID08_LOCALSTACK-STATUS_LEDGER-PENDING.md"


# ---------------------------------------------------------------- GPU tile + health check
from nexus_local import gpu  # noqa: E402

SMI_CSV = "NVIDIA GeForce RTX 3080, 591.44, 37, 6120, 10240, 61, 182.5, 320.00, 8.6\n"
SMI_HDR = "| NVIDIA-SMI 591.44   Driver Version: 591.44   CUDA Version: 13.1 |\n"


def fake_smi(args):
    return SMI_CSV if args else SMI_HDR


def test_gpu_parse_and_probe_offload_alert():
    g = gpu.parse_smi_csv(SMI_CSV)[0]
    assert g["name"] == "NVIDIA GeForce RTX 3080" and g["mem_total_mib"] == 10240 and g["compute_cap"] == "8.6"
    assert gpu.parse_cuda_max(SMI_HDR) == "13.1"
    ps = lambda: [{"name": "qwen3.5:9b", "size": 13_000_000_000, "size_vram": 7_540_000_000, "context_length": 262144},
                  {"name": "nexus-q35-9b-16k", "size": 5_800_000_000, "size_vram": 5_800_000_000}]
    r = gpu.gpu_probe({}, smi=fake_smi, ps=ps)()
    assert r["state"] == "WARN" and len(r["alerts"]) == 1 and "58% GPU" in r["alerts"][0]


def test_gpu_probe_temp_and_vram_alerts():
    hot = "RTX, 1, 99, 10000, 10240, 90, 300, 320, 8.6\n"
    r = gpu.gpu_probe({"gpu": {"temp_warn_c": 85}}, smi=lambda a: hot)()
    assert r["state"] == "WARN" and len(r["alerts"]) == 2


def test_gpu_probe_raises_without_gpu():
    with pytest.raises(RuntimeError):
        gpu.gpu_probe({}, smi=lambda a: "")()


def test_gpu_health_check_pass_and_fail(tmp_path):
    lib = tmp_path / "lib" / "ollama"
    (lib / "cuda_v12").mkdir(parents=True); (lib / "cuda_v13").mkdir()
    (lib / "cuda_v13" / "ggml-cuda.dll").write_bytes(b"x")
    log = tmp_path / "server.log"; log.write_text("level=INFO msg=ok\n")
    cfg = {"gpu": {"ollama_lib_dir": str(lib), "ollama_server_log": str(log), "vcredist_min": "14.40"}}
    r = gpu.health_check(cfg, util.expand, smi=fake_smi, vcredist=lambda: "14.51.36247.0")
    st = {c["id"]: c["status"] for c in r["checks"]}
    assert st == {"G01": "PASS", "G02": "PASS", "G03": "PASS", "G04": "PASS"} and r["state"] == "PASS"
    assert "CUDA max 13.1" in r["checks"][0]["detail"]
    log.write_text('msg="failure during llama-server GPU discovery" error=0xc0000005\n')
    r = gpu.health_check(cfg, util.expand, smi=fake_smi, vcredist=lambda: "14.16.27033.0")
    st = {c["id"]: c["status"] for c in r["checks"]}
    assert st["G03"] == "WARN" and st["G04"] == "FAIL" and r["state"] == "FAIL"


def test_gpu_health_check_missing_everything(tmp_path):
    def no_smi(args):
        raise FileNotFoundError("nvidia-smi nicht gefunden")
    cfg = {"gpu": {"ollama_lib_dir": str(tmp_path / "nope"), "ollama_server_log": str(tmp_path / "nolog")}}
    r = gpu.health_check(cfg, util.expand, smi=no_smi, vcredist=lambda: None)
    assert [c["id"] for c in r["checks"]] == ["G01", "G02", "G03", "G04"]
    assert r["checks"][3]["status"] == "NOT_RUN"


@pytest.mark.parametrize("hdr,ver", [("CUDA Version: 13.1", "13.1"), ("CUDA Version          : 13.2", "13.2"),
                                     ("| CUDA Driver Version: 13.0 |", "13.0"), ("no cuda here", None)])
def test_parse_cuda_max_variants(hdr, ver):
    assert gpu.parse_cuda_max(hdr) == ver
