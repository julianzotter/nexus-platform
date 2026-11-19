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
    p = sp.add_parser("eval", help="Evaluierung an alle Modelle mit Key senden, Berichte + Auswertung schreiben")
    p.add_argument("--models", default="", help="z.B. perplexity,claude (Standard: alle Cloud-Modelle mit Key)")
    p.add_argument("--dry-run", action="store_true", help="nur Prompt bauen und Groesse/Modelle anzeigen")
    sp.add_parser("eval-summary", help="vorhandene Berichte in evaluation/berichte auswerten")
    p = sp.add_parser("rfem-preflight", help="Read-only connection/identity diagnostics")
    p.add_argument("--target", choices=("rfem5", "rfem6"), required=True)
    p.add_argument("--type-library", type=pathlib.Path)
    p.add_argument("--expected-model", type=pathlib.Path)
    p.add_argument("--port", type=int, default=9000)
    p = sp.add_parser("geometry-plan", help="DSH proposal -> schema validation -> dry-run only")
    p.add_argument("--prompt-file", type=pathlib.Path, required=True)
    p.add_argument("--out", type=pathlib.Path, required=True)
    p = sp.add_parser("geometry", help="Deterministic frame JSON; no solver")
    p.add_argument("--spec", type=pathlib.Path, required=True)
    p.add_argument("--out", type=pathlib.Path, required=True)
    p.add_argument("--target", choices=("dry-run", "sdk-check", "rfem6-new", "rfem5-empty"), default="dry-run")
    p.add_argument("--type-library", type=pathlib.Path)
    p.add_argument("--expected-model", type=pathlib.Path)
    p.add_argument("--port", type=int, default=9000)
    a = ap.parse_args(argv)
    if a.cmd == "rfem-preflight":
        try:
            if a.target == "rfem5":
                from .rfem5 import preflight
                if a.type_library is None or a.expected_model is None:
                    raise ValueError("RFEM5 requires type library and expected model")
                r = preflight(a.type_library, a.expected_model)
            else:
                from .rfem6 import preflight
                r = preflight(a.port)
        except Exception as error:
            print(json.dumps({"status": "PREFLIGHT_BLOCKED", "error_type": type(error).__name__}))
            return 2
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0
    if a.cmd == "geometry-plan":
        from .geometry_plan import plan
        try:
            r = plan(a.prompt_file, a.out)
        except (ProviderError, ValueError, OSError) as error:
            print(json.dumps({"status": "PLAN_REJECTED_OR_BLOCKED", "error_type": type(error).__name__}))
            return 2
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0
    if a.cmd == "geometry":
        from .geometry_run import load_spec, run
        try:
            r = run(load_spec(a.spec), a.out, target=a.target,
                    type_library=a.type_library, expected_model=a.expected_model, port=a.port)
        except (ValueError, OSError) as error:
            print(json.dumps({"status": "INPUT_REJECTED", "error_type": type(error).__name__}))
            return 2
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 2 if r["status"] == "FAILED_OR_BLOCKED" else 0
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
