"""python -m nexus_orch.cli {status|run|council|lesson|lessons|registry}"""
import argparse, json, pathlib, sys
from .core import Orchestrator, write_lesson, search_lessons, ROOT
from .providers import ProviderError

def main(argv=None):
    ap = argparse.ArgumentParser(prog="nexus")
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("status")
    for c in ("run", "council"):
        p = sp.add_parser(c); p.add_argument("task"); p.add_argument("prompt"); p.add_argument("--system", default="")
    p = sp.add_parser("lesson"); [p.add_argument(f"--{k}", required=True) for k in ("agent", "context", "condition", "pattern", "evidence")]
    p = sp.add_parser("lessons"); p.add_argument("query", nargs="?", default="")
    sp.add_parser("registry")
    a = ap.parse_args(argv)
    o = Orchestrator()
    if a.cmd == "status":
        r = {"providers": {n: p.available() for n, p in o.providers.items()},
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
    else:
        r = json.loads((ROOT / "registry/workflow-registry.json").read_text(encoding="utf-8"))
    print(json.dumps(r, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    sys.exit(main())
