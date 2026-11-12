"""python -m nexus_orch.cli {status|run|council|lesson|lessons|registry}"""
import argparse, json, pathlib, sys
from .core import Orchestrator, write_lesson, search_lessons, ROOT
from .providers import ProviderError

def main(argv=None):
    ap = argparse.ArgumentParser(prog="nexus")
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("status")
    p = sp.add_parser("deepseek-auth", help="Explicit read-only DeepSeek model/auth probe")
    p.add_argument("--execute", action="store_true")
    for c in ("run", "council"):
        p = sp.add_parser(c); p.add_argument("task"); p.add_argument("prompt"); p.add_argument("--system", default="")
    p = sp.add_parser("lesson"); [p.add_argument(f"--{k}", required=True) for k in ("agent", "context", "condition", "pattern", "evidence")]
    p = sp.add_parser("lessons"); p.add_argument("query", nargs="?", default="")
    sp.add_parser("registry")
    p = sp.add_parser("eval", help="Evaluierung an alle Modelle mit Key senden, Berichte + Auswertung schreiben")
    p.add_argument("--models", default="", help="z.B. perplexity,claude (Standard: alle Cloud-Modelle mit Key)")
    p.add_argument("--dry-run", action="store_true", help="nur Prompt bauen und Groesse/Modelle anzeigen")
    sp.add_parser("eval-summary", help="vorhandene Berichte in evaluation/berichte auswerten")
    a = ap.parse_args(argv)
    o = Orchestrator()
    if a.cmd == "deepseek-auth":
        if not a.execute:
            r = {"status": "NOT_RUN", "endpoint": "GET https://api.deepseek.com/models"}
        else:
            from .deepseek import models_probe
            r = models_probe()
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r["status"] in ("NOT_RUN", "AUTHENTICATED") else 2
    if a.cmd == "status":
        r = {"provider_status_scope": "credential_resolution_only_not_authentication", "providers": {n: p.available() for n, p in o.providers.items()},
             "routes": {k: o.chain(k) for k in o.cfg["routes"]}}
    elif a.cmd in ("run", "council"):
        try:
            r = (o.run if a.cmd == "run" else o.council)(a.task, a.prompt, a.system)
        except (ProviderError, KeyError) as e:
            missing = [p.cfg["env_key"] for p in o.providers.values() if p.cfg.get("env_key") and not p.available()]
            print(json.dumps({"ok": False, "error": str(e).strip("'\""), "missing_keys": missing,
                              "hint": "Keys setzen: .\\setup.ps1, danach neues PowerShell-Fenster; lokal: Ollama starten"},
                             ensure_ascii=False, indent=2))
            return 2
    elif a.cmd == "lesson":
        r = write_lesson({k: getattr(a, k) for k in ("agent", "context", "condition", "pattern", "evidence")})
    elif a.cmd == "lessons":
        r = search_lessons(a.query)
    elif a.cmd == "eval":
        from . import evaluate as ev
        models = [m for m in a.models.split(",") if m] or None
        if a.dry_run:
            pr = ev.build_prompt()
            r = {"commit": ev.commit(), "prompt_zeichen": len(pr), "ca_tokens": len(pr) // 4,
                 "modelle": {n: o.providers[n].available() for n in (models or ev.CLOUD)}}
        else:
            r = ev.run(o, models)
    elif a.cmd == "eval-summary":
        from . import evaluate as ev
        r = {"auswertung": ev.aggregate(ev.EVAL / "berichte")}
    else:
        r = json.loads((ROOT / "registry/workflow-registry.json").read_text(encoding="utf-8"))
    print(json.dumps(r, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    sys.exit(main())
