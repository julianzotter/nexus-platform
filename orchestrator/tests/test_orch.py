import json, pytest
from nexus_orch.core import Orchestrator, load_config, write_lesson, search_lessons, ROOT
from nexus_orch.providers import MockProvider, ProviderError

def mk(tmp_path, **over):
    cfg = load_config()
    prov = {n: MockProvider(n, answer=f"A-{n}") for n in cfg["providers"]}
    prov.update(over)
    return Orchestrator(cfg, prov, root=tmp_path)

def test_primary(tmp_path):
    r = mk(tmp_path).run("research", "Q")
    assert r["provider"] == "perplexity"

def test_fallback(tmp_path):
    r = mk(tmp_path, perplexity=MockProvider("perplexity", fail=True)).run("research", "Q")
    assert r["provider"] == "gemini" and r["errors"]

def test_privacy_gate(tmp_path):
    assert mk(tmp_path).run("research", "VERTRAULICH Statik")["provider"] == "local"

def test_privacy_no_cloud_fallback(tmp_path):
    with pytest.raises(ProviderError):
        mk(tmp_path, local=MockProvider("local", fail=True)).run("research", "VERTRAULICH x")

def test_unknown_task(tmp_path):
    with pytest.raises(KeyError):
        mk(tmp_path).run("xyz", "Q")

def test_council_dissent(tmp_path):
    r = mk(tmp_path).council("engineering_decision", "Q")
    assert r["consensus"] is False and r["synthesis"]

def test_council_consensus(tmp_path):
    cfg = load_config()
    o = Orchestrator(cfg, {n: MockProvider(n, answer="Same") for n in cfg["providers"]}, root=tmp_path)
    assert o.council("engineering_decision", "Q")["consensus"] is True

def test_lessons(tmp_path):
    with pytest.raises(ValueError):
        write_lesson({"agent": "x"}, root=tmp_path)
    write_lesson({"agent": "claude", "context": "EC5", "condition": "wenn kmod fehlt", "pattern": "NKL pruefen", "evidence": "s1"}, root=tmp_path)
    assert len(search_lessons("kmod", root=tmp_path)) == 1

def test_registry_routes_valid():
    cfg = load_config(); reg = json.loads((ROOT / "registry/workflow-registry.json").read_text())
    assert all(w["route"] in cfg["routes"] for w in reg["workflows"])
    assert all(set(r["fallback"] + [r["primary"]]) <= set(cfg["providers"]) for r in cfg["routes"].values())

def test_ocr_route(tmp_path):
    assert mk(tmp_path).run("ocr", "https://x/plan.jpg")["provider"] == "vision"

def test_ocr_fallback(tmp_path):
    assert mk(tmp_path, vision=MockProvider("vision", fail=True)).run("ocr", "https://x/p.jpg")["provider"] == "gemini"

def test_ocr_confidential_local(tmp_path):
    assert mk(tmp_path).run("ocr", "VERTRAULICH C:/scan.png")["provider"] == "local"

def test_cli_clean_error(monkeypatch, capsys):
    from nexus_orch import cli
    for k in ("PERPLEXITY_API_KEY", "GEMINI_API_KEY", "OPENAI_API_KEY"):
        monkeypatch.delenv(k, raising=False)
    assert cli.main(["run", "research", "Q"]) == 2
    out = json.loads(capsys.readouterr().out)
    assert out["ok"] is False and "PERPLEXITY_API_KEY" in out["missing_keys"]

def test_http_error_detail(monkeypatch):
    import io, urllib.error, urllib.request
    from nexus_orch import providers
    def boom(*a, **k):
        raise urllib.error.HTTPError("http://localhost:11434/v1/chat/completions", 404, "Not Found", {}, io.BytesIO(b'{"error":"model \'qwen2.5:7b\' not found"}'))
    monkeypatch.setattr(urllib.request, "urlopen", boom)
    with pytest.raises(ProviderError) as e:
        providers._post("http://localhost:11434/v1/chat/completions", {}, {})
    assert "not found" in str(e.value) and "ollama pull" in str(e.value)

def test_ollama_num_ctx(monkeypatch):
    from nexus_orch import providers
    seen = {}
    def fake(url, h, body, timeout=120):
        seen.update(url=url, body=body); return {"message": {"content": "OK"}}
    monkeypatch.setattr(providers, "_post", fake)
    cfg = load_config()["providers"]["local"]
    r = providers.Provider("local", cfg).complete("Q")
    assert r["text"] == "OK" and seen["url"].endswith("/api/chat") and seen["body"]["options"]["num_ctx"] == 16384
