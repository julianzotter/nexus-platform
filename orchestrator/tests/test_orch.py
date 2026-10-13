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
