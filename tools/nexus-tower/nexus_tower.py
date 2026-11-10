#!/usr/bin/env python3
"""nexus_tower.py v0.2.0 | agent_id: ID06 | status: ENTWURF | NEXUS Control Tower, lokal und eigenstaendig

Eine Datei, nur Python-Standardbibliothek. Startet einen kleinen Webserver auf dem
eigenen PC (nur 127.0.0.1) und zeigt den Stand des WORK-Ordners im Browser.
Liest nur (Dateinamen, Aenderungszeit, Groesse, Kopf des letzten ID03-Berichts).
Schreibt nichts, loescht nichts, braucht kein Internet und keine Tokens.

Start:   Doppelklick auf nexus_tower_start.bat   (oder: python nexus_tower.py --work "<WORK>" --open)
Browser: http://localhost:8765   (als Lesezeichen speichern)
MCP:     http://localhost:8765/mcp   (lokaler MCP-Zugang, HTTP POST mit JSON-RPC, nur lesende Tools)
Ende:    Strg+C im Fenster
"""
from __future__ import annotations

import argparse
import json
import os
import re
import threading
import time
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

WORK = Path(".")
TOP_N = 300


def list_files() -> tuple[list[dict], int]:
    """Neueste Dateien direkt im WORK-Ordner (Name, Zeit in ms, Groesse) und Gesamtzahl."""
    rows = []
    with os.scandir(WORK) as it:
        for entry in it:
            try:
                if entry.is_file():
                    st = entry.stat()
                    rows.append({"name": entry.name, "mtime": int(st.st_mtime * 1000), "size": st.st_size})
            except OSError:
                continue
    rows.sort(key=lambda r: r["mtime"], reverse=True)
    return rows[:TOP_N], len(rows)


def read_gate(files: list[dict]) -> dict:
    """Kopfzeilen (Frontmatter) des neuesten ID03-Statusberichts."""
    hit = next((f for f in files if "ID03_STATUSREPORT" in f["name"]), None)
    if not hit:
        return {}
    try:
        head = (WORK / hit["name"]).read_text(encoding="utf-8", errors="replace")[:4000]
    except OSError:
        return {"title": hit["name"], "mtime": hit["mtime"], "status": "nicht lesbar"}
    lines = [ln.strip() for ln in head.splitlines()]
    out = {"title": hit["name"], "mtime": hit["mtime"]}
    for key in ("status", "problems", "open_questions", "tasks_open"):
        for i, ln in enumerate(lines):
            if ln.startswith(key + ":"):
                value = ln[len(key) + 1:].strip().strip("'\"")
                if not value:
                    items = []
                    for nxt in lines[i + 1:]:
                        if not nxt.startswith("- "):
                            break
                        items.append(nxt[2:])
                    value = ", ".join(items)
                out[key] = value
                break
    return out


def state() -> dict:
    files, total = list_files()
    return {"generated": int(time.time() * 1000), "work": str(WORK), "total": total,
            "files": files, "gate": read_gate(files)}


# ---------- Namenspruefung (AGB v005) und lokaler MCP-Zugang ----------

def name_check(title: str) -> tuple[str, str]:
    """Urteil und Grund fuer einen Dateinamen nach YY_MM_DD_HHMM_ID##_THEMA_###."""
    if title.startswith("_"):
        return "Steuerdatei", ""
    if re.search(r"_UEBERHOLT(\.[A-Za-z0-9]+)?$", title):
        return "ueberholt", ""
    if not re.match(r"^\d\d_\d\d_\d\d_", title):
        return "Verstoss", "kein Datumspraefix JJ_MM_TT"
    if re.match(r"^\d\d_\d\d_\d\d_\d\d_\d\d_", title):
        return "Verstoss", "Zeit als HH_MM statt HHMM"
    m = re.match(r"^\d\d_\d\d_\d\d_(\d\d)(\d\d)_", title)
    if not m:
        return "Verstoss", "kein HHMM nach dem Datum"
    if int(m.group(1)) > 23 or int(m.group(2)) > 59:
        return "Verstoss", "vier Ziffern nach dem Datum sind keine Uhrzeit"
    if not re.match(r"^\d\d_\d\d_\d\d_\d{4}_ID\d\d_", title):
        return "Verstoss", "keine Rollen-ID direkt nach HHMM"
    stem = re.sub(r"\.[A-Za-z0-9]+$", "", title)
    if re.search(r"_\d{3,4}$", stem):
        return "konform", ""
    if re.search(r"_(LEDGER-PENDING|UNREGISTERED)$", stem):
        return "Nummer offen", ""
    return "Abweichung", "Ende ohne Artefaktnummer oder LEDGER-PENDING"


def tool_work_state(args: dict) -> dict:
    limit = max(1, min(int(args.get("limit", 20)), TOP_N))
    files, total = list_files()
    return {"work": str(WORK), "total": total, "files": files[:limit]}


def tool_naming_check(args: dict) -> dict:
    files, _ = list_files()
    today = datetime.now().date()
    counts: dict[str, int] = {}
    problems = []
    for f in files:
        if datetime.fromtimestamp(f["mtime"] / 1000).date() != today:
            continue
        verdict, reason = name_check(f["name"])
        counts[verdict] = counts.get(verdict, 0) + 1
        if verdict in ("Verstoss", "Abweichung"):
            problems.append({"name": f["name"], "verdict": verdict, "reason": reason})
    return {"date": today.isoformat(), "counts": counts, "problems": problems}


def tool_gate_status(args: dict) -> dict:
    files, _ = list_files()
    return read_gate(files)


TOOLS = {
    "work_state": (tool_work_state, "Neueste Dateien im NEXUS-WORK-Ordner (Name, Aenderungszeit in ms, Groesse).",
                   {"type": "object", "properties": {"limit": {"type": "integer", "minimum": 1, "maximum": TOP_N}}}),
    "naming_check": (tool_naming_check, "Prueft die heute geaenderten Dateinamen gegen die AGB-v005-Dateiregel.",
                     {"type": "object", "properties": {}}),
    "gate_status": (tool_gate_status, "Kopfzeilen des neuesten ID03-Konsistenzberichts (Urteil, Probleme, offene Fragen).",
                    {"type": "object", "properties": {}}),
}
MCP_VERSIONS = ("2025-06-18", "2025-03-26", "2024-11-05")


def mcp_dispatch(msg: dict) -> dict | None:
    """Eine JSON-RPC-Nachricht beantworten. None = Notification ohne Antwort."""
    mid, method, params = msg.get("id"), msg.get("method", ""), msg.get("params") or {}
    if mid is None:
        return None
    def ok(result: dict) -> dict:
        return {"jsonrpc": "2.0", "id": mid, "result": result}
    if method == "initialize":
        want = params.get("protocolVersion")
        return ok({"protocolVersion": want if want in MCP_VERSIONS else MCP_VERSIONS[0],
                   "capabilities": {"tools": {}},
                   "serverInfo": {"name": "nexus-tower", "version": "0.2.0"}})
    if method == "ping":
        return ok({})
    if method == "tools/list":
        return ok({"tools": [{"name": n, "description": d, "inputSchema": sch} for n, (_, d, sch) in TOOLS.items()]})
    if method == "tools/call":
        entry = TOOLS.get(params.get("name", ""))
        if not entry:
            return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32602, "message": "unbekanntes Tool"}}
        try:
            data = entry[0](params.get("arguments") or {})
            return ok({"content": [{"type": "text", "text": json.dumps(data, ensure_ascii=False)}], "isError": False})
        except (OSError, ValueError) as exc:
            return ok({"content": [{"type": "text", "text": f"Fehler: {exc}"}], "isError": True})
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": "Methode nicht vorhanden"}}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, ctype: str, body: bytes) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # nur Lesen; andere Methoden gibt es nicht
        if self.path == "/api/state":
            try:
                body = json.dumps(state()).encode("utf-8")
                self._send(200, "application/json; charset=utf-8", body)
            except OSError as exc:
                self._send(500, "text/plain; charset=utf-8", f"WORK nicht lesbar: {exc}".encode("utf-8"))
        elif self.path in ("/", "/index.html"):
            self._send(200, "text/html; charset=utf-8", PAGE.encode("utf-8"))
        else:
            self._send(404, "text/plain; charset=utf-8", b"nicht gefunden")

    def _local_origin(self) -> bool:
        """Anfragen fremder Webseiten ablehnen (Schutz gegen DNS-Rebinding)."""
        origin = self.headers.get("Origin")
        return origin is None or re.match(r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$", origin) is not None

    def do_POST(self) -> None:  # nur /mcp; alle Tools lesen nur
        if self.path != "/mcp":
            self._send(404, "text/plain; charset=utf-8", b"nicht gefunden")
            return
        if not self._local_origin():
            self._send(403, "text/plain; charset=utf-8", b"Origin nicht erlaubt")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            msg = json.loads(self.rfile.read(min(length, 1_000_000)).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            body = json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "kein gueltiges JSON"}})
            self._send(400, "application/json; charset=utf-8", body.encode("utf-8"))
            return
        if isinstance(msg, list):
            answers = [a for a in (mcp_dispatch(m) for m in msg if isinstance(m, dict)) if a]
        else:
            answers = mcp_dispatch(msg) if isinstance(msg, dict) else None
        if not answers:
            self._send(202, "text/plain; charset=utf-8", b"")
            return
        self._send(200, "application/json; charset=utf-8", json.dumps(answers, ensure_ascii=False).encode("utf-8"))

    def log_message(self, fmt: str, *args) -> None:  # keine Zugriffsprotokolle im Fenster
        return


PAGE = r"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>NEXUS Control Tower (lokal)</title>
<style>
:root{--bg:#f6f5f1;--panel:#fff;--fg:#1c1b19;--muted:#6b6862;--line:#dedbd3;--ok:#1f7a4d;--bad:#b3261e}
@media (prefers-color-scheme:dark){:root{--bg:#191817;--panel:#232220;--fg:#eceae4;--muted:#a09c94;--line:#3a3835;--ok:#5fc48f;--bad:#f08b83}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,Segoe UI,sans-serif}
main{max-width:1200px;margin:0 auto;padding:20px;display:flex;flex-direction:column;gap:20px}
h1{font:400 28px Georgia,serif;margin:0 0 4px}h2{font-size:17px;margin:0 0 8px}
.muted{color:var(--muted)}.cap{font-size:12px;color:var(--muted)}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:14px;min-width:0}
.num{font:400 28px Georgia,serif;font-variant-numeric:tabular-nums}
.scroll{overflow-x:auto}table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}
th,td{text-align:left;padding:5px 8px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-size:12px;color:var(--muted);font-weight:600;white-space:nowrap}.nw{white-space:nowrap}
.ok{color:var(--ok)}.bad{color:var(--bad)}dl{display:grid;grid-template-columns:max-content 1fr;gap:4px 14px;margin:0}
dt{color:var(--muted);font-size:12px}dd{margin:0;overflow-wrap:anywhere}
#err{color:var(--bad);font-weight:600}
</style></head><body><main>
<div><h1>NEXUS Control Tower (lokal)</h1>
<p class="muted" style="margin:0">Letzte Änderung in WORK: <b id="s-last">—</b> durch <b id="s-agent">—</b>. Stand gelesen: <b id="s-read">—</b>. Liest alle 60 Sekunden neu. <span id="err"></span></p>
<p class="cap" id="s-work"></p></div>
<section class="card"><h2>Wo ist das Problem: letzte Konsistenzprüfung von ID03</h2>
<dl><dt>Urteil</dt><dd><b id="g-status">—</b></dd><dt>Abgelegt</dt><dd id="g-time">—</dd><dt>Probleme</dt><dd id="g-problems">—</dd>
<dt>Offene Fragen</dt><dd id="g-questions">—</dd><dt>Offene Aufgaben</dt><dd id="g-tasks">—</dd><dt>Bericht</dt><dd id="g-title">—</dd></dl>
<p class="cap">Aus dem Kopf des Berichts, wie ID03 ihn geschrieben hat. GitHub (Pull Requests, Actions) wird hier nicht live gelesen.</p></section>
<div class="tiles">
<div class="card"><div class="num" id="t-total">—</div><div class="cap">Dateien direkt in WORK</div></div>
<div class="card"><div class="num" id="t-today">—</div><div class="cap">heute geändert</div></div>
<div class="card"><div class="num" id="t-agents">—</div><div class="cap">Agenten mit ID im Namen heute aktiv</div></div>
<div class="card"><div class="num" id="t-viol">—</div><div class="cap">heutige Namen verstoßen gegen die AGB-v005-Dateiregel</div></div>
<div class="card"><div class="num" id="t-pend">—</div><div class="cap">heutige Dateien warten auf eine Ledger-Nummer</div></div>
</div>
<section><h2>Dateinamen gegen die AGB-v005-Regel (heute)</h2>
<p class="muted" id="n-lead" style="margin:0 0 8px"></p>
<div class="scroll"><table><thead><tr><th>Geändert</th><th>Agent</th><th>Urteil</th><th>Grund</th><th>Minuten Name/Schreibzeit</th><th>Datei</th></tr></thead><tbody id="tb-naming"></tbody></table></div>
<p class="cap">Regel: JJ_MM_TT_HHMM_ID##_THEMA_###. Ende LEDGER-PENDING oder UNREGISTERED zählt als „Nummer offen“. Steuerdateien mit Unterstrich und Namen mit _UEBERHOLT werden nicht geprüft. Es werden nur Namen geprüft, kein Frontmatter.</p></section>
<section><h2>Agenten: wer hat was wann geschrieben (heute)</h2>
<div class="scroll"><table><thead><tr><th>Agent</th><th>Rolle</th><th>Dateien heute</th><th>Letzte Änderung</th><th>Letzte Datei</th></tr></thead><tbody id="tb-agents"></tbody></table></div></section>
<section><h2>Neueste Dateien in WORK</h2>
<div class="scroll"><table><thead><tr><th>Geändert</th><th>Datei</th><th>Größe (Bytes)</th></tr></thead><tbody id="tb-files"></tbody></table></div></section>
</main><script>
const ROLES={ID01:'Julian (Mensch)',ID02:'ChatGPT Chief Orchestrator',ID03:'ChatGPT QA',ID04:'Gemini',ID05:'Perplexity',ID06:'Claude',ID07:'DeepSeek',ID08:'Ollama',ID10:'QA-Assistant'};
const $=(id)=>document.getElementById(id);
const pad=(n)=>String(n).padStart(2,'0');
const fmt=(ms)=>{if(!ms)return '—';const d=new Date(ms);return pad(d.getDate())+'.'+pad(d.getMonth()+1)+'. '+pad(d.getHours())+':'+pad(d.getMinutes());};
const isToday=(ms)=>new Date(ms).toDateString()===new Date().toDateString();
const agentOf=(t)=>{const m=/ID[-_ ]?(\d{2})(?!\d)/i.exec(t||'');return m?'ID'+m[1]:'ohne ID im Namen';};
function nameCheck(t){
  if(/^_/.test(t))return ['Steuerdatei','',null];
  if(/_UEBERHOLT(\.[A-Za-z0-9]+)?$/.test(t))return ['überholt','',null];
  const d=/^(\d\d)_(\d\d)_(\d\d)_/.exec(t);
  if(!d)return ['Verstoß','kein Datumspräfix JJ_MM_TT',null];
  if(/^\d\d_\d\d_\d\d_\d\d_\d\d_/.test(t))return ['Verstoß','Zeit als HH_MM statt HHMM',null];
  const h=/^\d\d_\d\d_\d\d_(\d\d)(\d\d)_/.exec(t);
  if(!h)return ['Verstoß','kein HHMM nach dem Datum',null];
  if(+h[1]>23||+h[2]>59)return ['Verstoß','vier Ziffern nach dem Datum sind keine Uhrzeit',null];
  const nm=new Date(2000+ +d[1],+d[2]-1,+d[3],+h[1],+h[2]).getTime();
  if(!/^\d\d_\d\d_\d\d_\d{4}_ID\d\d_/.test(t))return ['Verstoß','keine Rollen-ID direkt nach HHMM',nm];
  const stem=t.replace(/\.[A-Za-z0-9]+$/,'');
  if(/_\d{3,4}$/.test(stem))return ['konform','',nm];
  if(/_(LEDGER-PENDING|UNREGISTERED)$/.test(stem))return ['Nummer offen','',nm];
  return ['Abweichung','Ende ohne Artefaktnummer oder LEDGER-PENDING',nm];
}
function row(cells){const tr=document.createElement('tr');for(const c of cells){const td=document.createElement('td');td.textContent=c[0]==null?'':String(c[0]);if(c[1])td.className=c[1];tr.append(td);}return tr;}
function draw(s){
  const files=s.files||[],today=files.filter((f)=>isToday(f.mtime));
  $('s-work').textContent='Ordner: '+s.work+' · angezeigt werden die '+files.length+' neuesten Dateien';
  $('s-read').textContent=fmt(s.generated);
  $('s-last').textContent=files.length?fmt(files[0].mtime):'—';
  $('s-agent').textContent=files.length?agentOf(files[0].name):'—';
  const g=s.gate||{};
  $('g-status').textContent=g.status||'—';$('g-status').className=!g.status?'':(/^(OK|PASS|RELEASE)/i.test(g.status)?'ok':'bad');
  $('g-time').textContent=fmt(g.mtime);$('g-problems').textContent=g.problems||'—';$('g-questions').textContent=g.open_questions||'—';
  $('g-tasks').textContent=g.tasks_open||'—';$('g-title').textContent=g.title||'—';
  const checked=today.map((f)=>{const c=nameCheck(f.name);return {f,v:c[0],r:c[1],drift:c[2]==null?null:Math.round(Math.abs(f.mtime-c[2])/60000)};}).filter((x)=>x.v!=='Steuerdatei'&&x.v!=='überholt');
  const n=(v)=>checked.filter((x)=>x.v===v).length;
  $('t-total').textContent=s.total;$('t-today').textContent=today.length+(today.length===files.length&&s.total>files.length?'+':'');
  $('t-agents').textContent=new Set(today.map((f)=>agentOf(f.name)).filter((a)=>a!=='ohne ID im Namen')).size;
  $('t-viol').textContent=n('Verstoß');$('t-pend').textContent=n('Nummer offen');
  $('n-lead').textContent='Von '+checked.length+' geprüften Namen: '+n('konform')+' konform mit Nummer, '+n('Nummer offen')+' konform mit offener Nummer, '+n('Abweichung')+' mit falschem Ende, '+n('Verstoß')+' Verstöße.';
  $('tb-naming').replaceChildren(...checked.filter((x)=>x.v==='Verstoß'||x.v==='Abweichung').map((x)=>row([[fmt(x.f.mtime),'nw'],[agentOf(x.f.name),'nw'],[x.v,x.v==='Verstoß'?'bad nw':'nw'],[x.r],[x.drift==null?'':x.drift],[x.f.name]])));
  const by=new Map();
  for(const f of today){const a=agentOf(f.name);const r=by.get(a)||{a,n:0,last:0,title:''};r.n++;if(f.mtime>r.last){r.last=f.mtime;r.title=f.name;}by.set(a,r);}
  $('tb-agents').replaceChildren(...[...by.values()].sort((x,y)=>y.last-x.last).map((r)=>row([[r.a,'nw'],[ROLES[r.a]||''],[r.n],[fmt(r.last),'nw'],[r.title]])));
  $('tb-files').replaceChildren(...files.slice(0,40).map((f)=>row([[fmt(f.mtime),'nw'],[f.name],[f.size]])));
}
async function load(){
  try{const r=await fetch('/api/state',{cache:'no-store'});if(!r.ok)throw new Error(await r.text());draw(await r.json());$('err').textContent='';}
  catch(e){$('err').textContent='Fehler beim Lesen: '+e.message;}
}
load();setInterval(load,60000);
</script></body></html>
"""


def main() -> int:
    global WORK
    ap = argparse.ArgumentParser(description="NEXUS Control Tower, lokal")
    ap.add_argument("--work", required=True, help="Pfad zum WORK-Ordner")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--open", action="store_true", help="Browser nach dem Start oeffnen")
    args = ap.parse_args()
    WORK = Path(args.work)
    if not WORK.is_dir():
        print(f"WORK-Ordner nicht gefunden: {WORK}")
        return 2
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)  # nur vom eigenen PC erreichbar
    print(f"NEXUS Control Tower laeuft: http://localhost:{args.port}  (Ende mit Strg+C)")
    print(f"Lokaler MCP-Zugang:         http://localhost:{args.port}/mcp")
    if args.open:
        threading.Timer(1.0, webbrowser.open, args=(f"http://localhost:{args.port}",)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
