"""Build the task set from the config (keeps supervisor.py generic)."""
from __future__ import annotations

from pathlib import Path

from . import control_tower, git_mirror, gpt_to_skill, gpu, mcp_gateway
from .bridge import BridgeEngine, Ledger, Rule, validate_rules
from .reporter import Reporter
from .supervisor import ExternalMonitorTask, PeriodicTask, ProcessTask, ServerTask, http_json
from .util import expand


def ollama_probe(cfg: dict):
    base = cfg.get("ollama", {}).get("base_url", "http://127.0.0.1:11434")
    default = cfg.get("ollama", {}).get("default_model")

    def probe() -> dict:
        ver = http_json(base + "/api/version", 3).get("version")
        loaded = []
        for m in http_json(base + "/api/ps", 3).get("models", []):
            size, vram = m.get("size") or 0, m.get("size_vram") or 0
            share = "100% GPU" if size and vram >= size else (f"{round(100 * vram / size)}% GPU" if size else "?")
            loaded.append({"name": m.get("name"), "size_gb": round(size / 1e9, 2), "size_vram_gb": round(vram / 1e9, 2),
                           "context_length": m.get("context_length"), "gpu_share": share, "expires_at": m.get("expires_at")})
        return {"version": ver, "loaded": loaded, "default_model": default}
    return probe


def wire(sup) -> None:
    cfg = sup.cfg
    ports = cfg.get("ports", {})
    sup.add(ServerTask("control_tower", lambda: control_tower.build_server(sup, int(ports.get("control_tower", 8770))),
                       "Task-Manager-Dashboard 127.0.0.1:%s" % ports.get("control_tower", 8770)))
    mcp_cfg = cfg.get("mcp", {})
    sup.add(ServerTask("mcp_gateway", lambda: mcp_gateway.build_server(cfg, sup.token, int(ports.get("mcp_gateway", 8766)), sup),
                       "MCP Streamable HTTP 127.0.0.1:%s/mcp (read-only + local_llm)" % ports.get("mcp_gateway", 8766)),
            enabled=mcp_cfg.get("enabled", True))
    sup.add(ExternalMonitorTask("ollama", ollama_probe(cfg), "Ollama (nur Überwachung, wird nie gestoppt)"))
    gcfg = cfg.get("gpu", {})
    obase = cfg.get("ollama", {}).get("base_url", "http://127.0.0.1:11434")
    sup.add(ExternalMonitorTask("gpu", gpu.gpu_probe(cfg, ps=lambda: http_json(obase + "/api/ps", 3).get("models", [])),
                                "GPU-Telemetrie (nvidia-smi) + CPU-Offload-Warnung"), enabled=gcfg.get("enabled", True))
    sup.add(PeriodicTask("gpu_health", lambda: gpu.health_check(cfg, expand), float(gcfg.get("health_interval_s", 1800)),
                         "GPU-Gesundheitsprüfung: Treiber, Ollama-CUDA, VC++-Runtime, server.log"),
            enabled=gcfg.get("enabled", True))

    rules = [Rule.from_dict(r, expand) for r in cfg.get("bridges", [])]
    validate_rules(rules)
    sup.bridge_engine = BridgeEngine(rules, Ledger(Path(cfg["_runtime"]) / "state" / "bridge.sqlite"),
                                     dry_run=bool(cfg.get("bridge_dry_run", True)))
    sup.add(PeriodicTask("bridges", lambda: {r.rule: r.__dict__ for r in sup.bridge_engine.run_all()},
                         float(cfg.get("bridge_interval_s", 60)), "Datei-Brücken OneDrive · Drive · Git-Staging"),
            enabled=bool(rules))

    gm = cfg.get("git_mirror", {})
    sup.add(PeriodicTask("git_mirror", lambda: git_mirror.run_mirror(cfg, expand), float(gm.get("interval_s", 900)),
                         "EXPORT-APPROVED -> GitHub review/* (nie main, nie force)"), enabled=bool(gm.get("enabled")))

    gs = cfg.get("gpt_to_skill", {})
    sup.add(PeriodicTask("gpt_to_skill", lambda: gpt_to_skill.run(expand(gs.get("exports_dir")), expand(gs.get("staging_dir"))),
                         float(gs.get("interval_s", 600)), "Custom-GPT-Export -> SKILL.md (lokales Staging)"),
            enabled=bool(gs.get("enabled")))

    rep = Reporter(sup, cfg, expand)
    sup.add(PeriodicTask("reporter", rep.tick, float(cfg.get("reporter", {}).get("interval_s", 300)),
                         "Heartbeat LLM-HISTORY-LOG + Statusbericht WORK"), enabled=cfg.get("reporter", {}).get("enabled", True))

    for svc in cfg.get("processes", []):
        sup.add(ProcessTask(svc["name"], [str(expand(c)) if "%" in c else c for c in svc["cmd"]],
                            str(expand(svc.get("cwd"))) if svc.get("cwd") else None, svc.get("env", {}),
                            sup.log_dir, sup.job, svc.get("health_url"), svc.get("desc", "")),
                enabled=bool(svc.get("enabled", False)))
