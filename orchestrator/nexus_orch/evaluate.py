"""nexus eval: Evaluierungsbogen + aktuelles Kontextpaket an alle verfuegbaren Modelle, Berichte speichern, auswerten.

Bewusste Ausnahme vom Privacy-Gate: gesendet wird ausschliesslich Repo-Inhalt (Code/Doku, keine Projektdaten).
Der Bogen wird gegen Marker geprueft; enthaelt ein Repo-File echte Projektdaten, gehoert es nicht ins Repo.
"""
import datetime as dt, json, pathlib, re, runpy, subprocess, sys

REPO = pathlib.Path(__file__).resolve().parents[2]
EVAL = REPO / "evaluation"
BOGEN = EVAL / "NEXUS_EVAL_BOGEN_v1.0.md"
PACK_FILES = [
    "README.md", "orchestrator/README.md", "orchestrator/pyproject.toml",
    "orchestrator/config/routing.json", "orchestrator/config/sync_targets.json",
    "orchestrator/registry/workflow-registry.json",
    "orchestrator/nexus_orch/core.py", "orchestrator/nexus_orch/providers.py",
    "orchestrator/nexus_orch/cli.py", "orchestrator/nexus_orch/evaluate.py",
    "orchestrator/tests/test_orch.py", "orchestrator/setup.ps1",
    "orchestrator/sync_nexus.ps1", "orchestrator/sync_nexus_rclone.ps1", "orchestrator/install_autosync.ps1",
]
LANG = {".py": "python", ".json": "json", ".ps1": "powershell", ".toml": "toml", ".md": "markdown"}
CLOUD = ["perplexity", "claude", "gpt", "gemini"]

def commit(repo=REPO):
    try:
        return subprocess.run(["git", "-C", str(repo), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip() or "unbekannt"
    except OSError:
        return "unbekannt"

def build_pack(repo=REPO):
    """Kontextpaket zum aktuellen Stand: Dateibaum + Kerndateien mit Zeilennummern."""
    repo = pathlib.Path(repo)
    skip = {".git", "__pycache__", ".pytest_cache", "node_modules", ".venv", "venv"}
    tree = [f"{p.stat().st_size:>9}  {p.relative_to(repo).as_posix()}" for p in sorted(repo.rglob("*"))
            if p.is_file() and not (set(p.relative_to(repo).parts) & skip) and "egg-info" not in str(p)]
    out = [f"## 6 Kontextpaket (automatisch erzeugt, Commit {commit(repo)}, {dt.date.today()})", "", "### Dateibaum", "```", *tree, "```"]
    for rel in PACK_FILES:
        f = repo / rel
        if not f.exists():
            continue
        lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        out += ["", f"### FILE: {rel}", "~~~~" + LANG.get(f.suffix, "text"), *[f"{i:4} {l}" for i, l in enumerate(lines, 1)], "~~~~"]
    return "\n".join(out)

def build_prompt(repo=REPO):
    text = (pathlib.Path(repo) / "evaluation/NEXUS_EVAL_BOGEN_v1.0.md").read_text(encoding="utf-8")
    head = re.split(r"(?m)^## 6 Kontextpaket", text)[0]  # Anweisung + Kriterien + Format, ohne altes Paket
    return head.rstrip() + "\n\n" + build_pack(repo)

def run(orch, models=None, outdir=None, repo=REPO):
    outdir = pathlib.Path(outdir or pathlib.Path(repo) / "evaluation/berichte"); outdir.mkdir(parents=True, exist_ok=True)
    prompt, stamp = build_prompt(repo), dt.date.today().strftime("%y%m%d")
    system = "Du bist unabhaengige Pruefinstanz. Befolge den Evaluierungsbogen exakt, inklusive JSON-Block am Ende. Deutsch."
    done, skipped, failed = [], [], []
    for name in models or CLOUD:
        p = orch.providers.get(name)
        if p is None or not p.available():
            skipped.append(name); continue
        p.cfg = {**p.cfg, "timeout": 900, "max_tokens": max(p.cfg.get("max_tokens", 4096), 8192)}
        try:
            r = p.complete(prompt, system, 0.0)
        except Exception as e:  # ProviderError oder unerwartete Antwort
            failed.append(f"{name}: {e}"); continue
        f = outdir / f"EVAL_{name}_{stamp}.md"
        body = r["text"]
        if r.get("citations"):
            body += "\n\n## Quellen (Provider)\n" + "\n".join(f"- {c}" for c in r["citations"])
        f.write_text(f"<!-- model={r.get('model')} commit={commit(repo)} -->\n" + body, encoding="utf-8")
        done.append(f.name)
    summary = aggregate(outdir) if done or list(outdir.glob("EVAL_*.md")) else None
    return {"commit": commit(repo), "berichte": done, "uebersprungen_ohne_key": skipped, "fehler": failed,
            "auswertung": summary, "prompt_zeichen": len(prompt)}

def aggregate(outdir):
    script = EVAL / "nexus_eval_auswertung.py"
    if not script.exists():
        return None
    argv = sys.argv
    try:
        sys.argv = [str(script), str(outdir)]
        runpy.run_path(str(script), run_name="__main__")
    except SystemExit as e:
        return f"keine Auswertung: {e}"
    finally:
        sys.argv = argv
    return str(pathlib.Path(outdir) / "NEXUS_EVAL_AUSWERTUNG.md")
