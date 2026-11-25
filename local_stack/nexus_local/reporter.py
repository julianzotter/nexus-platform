"""Status reports (WORK) and the single overwritable heartbeat (LLM-HISTORY-LOG), per _AGBS v007.2.

Evidence states written into every report (review G03/R02):
- LOCAL_WRITTEN_READBACK_OK : bytes written to the local Drive-for-desktop folder and re-read (SHA-256).
- DRIVE_SYNC_UNVERIFIED     : upload to drive.google.com is NOT verified by this process.
- REGISTRATION_PENDING      : no ledger number; the designated ledger writer registers later.
"""
from __future__ import annotations

import time
from pathlib import Path

from .util import DestinationExists, atomic_write_text, iso, load_json, atomic_write_json, now_vienna

INCIDENT_WINDOW_S = 3600
STARTUP_MIN_GAP_S = 6 * 3600


def report_name(agent: str, topic: str, when=None, suffix: str = "") -> str:
    t = when or now_vienna()
    return f"{t:%y_%m_%d_%H%M}_{agent}_{topic}_LEDGER-PENDING{suffix}.md"


class Reporter:
    def __init__(self, sup, cfg: dict, expand):
        rc = cfg.get("reporter", {})
        self.sup, self.cfg = sup, cfg
        self.agent = cfg.get("agent_id", "ID08")
        self.publish = bool(rc.get("publish_to_work", False))   # review G03/R02: provider writes only by ID01 opt-in
        local = Path(cfg["_runtime"]) / "reports"
        if self.publish:
            self.report_dir = expand(rc.get("report_dir")) or expand(cfg.get("paths", {}).get("work"))
            self.history = expand(cfg.get("paths", {}).get("history_log"))
        else:
            self.report_dir = local
            self.history = local / "heartbeat"
            self.history.mkdir(parents=True, exist_ok=True)
        self.daily_hour = int(rc.get("daily_hour", 18))
        self.state_path = Path(cfg["_runtime"]) / "state" / "reporter.json"
        self.state = load_json(self.state_path, {}) or {}
        self.last_incident_mono = 0.0

    def _save(self) -> None:
        atomic_write_json(self.state_path, self.state)

    # ------------------------------------------------------------- content
    def render(self, kind: str, reason: str) -> str:
        st = self.sup.status()
        bridges = self.sup.bridge_engine.status() if getattr(self.sup, "bridge_engine", None) else None
        rows = "\n".join(f"| {t['name']} | {t['kind']} | {t['status']} | {t['restarts']} | {t['last_ok'] or '-'} | "
                         f"{(t['last_error'] or '').replace('|', '/')[:120]} |" for t in st["tasks"])
        problems = [t for t in st["tasks"] if t["status"] in ("FAILED", "CIRCUIT_OPEN", "BLOCKED", "BACKOFF")]
        brows = ""
        if bridges:
            for r in bridges["rules"]:
                l = r.get("last") or {}
                brows += (f"| {r['name']} | {r['mode']} | {'AUS' if not r['enabled'] else l.get('blocked') or 'OK'} | "
                          f"{l.get('copied', '-')} | {l.get('conflicts', '-')} | {l.get('skipped_placeholder', '-')} |\n")
        return f"""---
name: "{report_name(self.agent, 'LOCALSTACK-STATUS')[:-3]}"
version: "{st['version']}"
status: "{'PROBLEME' if problems else 'OK'}_{kind.upper()}"
date: "{iso()}"
role_id: "{self.agent}"
executor: "{self.cfg.get('executor')}"
boot_id: "{st['boot_id']}"
evidence: "{'LOCAL_WRITTEN_READBACK_OK / DRIVE_SYNC_UNVERIFIED' if self.publish else 'LOCAL_STAGED (nicht in WORK veroeffentlicht)'}"
registration_status: "REGISTRATION_PENDING"
release: false
---

# NEXUS Local Stack – Statusbericht ({kind})

Anlass: {reason}

## Tasks

| Task | Typ | Status | Restarts | Letzter OK | Letzter Fehler |
|---|---|---|---|---|---|
{rows}

## Brücken

| Regel | Modus | Status | Kopiert | Konflikte | Platzhalter |
|---|---|---|---|---|---|
{brows or '| - | - | nicht konfiguriert | - | - | - |\n'}
## Probleme

{chr(10).join(f'- {t["name"]}: {t["status"]} {t["last_error"] or ""}' for t in problems) or '- keine'}

## Offene Fragen / Nachweisstand

- Cloud-Upload dieses Berichts: DRIVE_SYNC_UNVERIFIED (Drive for desktop).
- Registrierung: REGISTRATION_PENDING (Ledger-Schreiber laut _AGBS §6).
- Freigabe: keine; Statusprojektion des lokalen Supervisors.
"""

    def write_report(self, kind: str, reason: str) -> dict:
        if not self.report_dir or not self.report_dir.is_dir():
            return {"status": "BLOCKED", "reason": "REPORT_DIR_NOT_MOUNTED"}
        text = self.render(kind, reason)
        for n in range(1, 10):
            path = self.report_dir / report_name(self.agent, "LOCALSTACK-STATUS", suffix="" if n == 1 else f"-{n}")
            try:
                digest = atomic_write_text_create(path, text)
                return {"status": "LOCAL_WRITTEN_READBACK_OK" if self.publish else "LOCAL_STAGED",
                        "file": path.name, "sha256": digest}
            except DestinationExists:
                continue
        return {"status": "BLOCKED", "reason": "NAME_COLLISION"}

    def heartbeat(self) -> dict:
        if not self.history or not self.history.is_dir():
            return {"status": "BLOCKED", "reason": "HISTORY_LOG_NOT_MOUNTED"}
        st = self.sup.status()
        ok = sum(t["status"] in ("RUNNING", "EXTERNAL") for t in st["tasks"])
        path = self.history / f"_HEARTBEAT_{self.agent}_NEXUS-LOCALSTACK.md"  # the ONE allowed overwrite (_AGBS §5)
        digest = atomic_write_text(path, f"# Heartbeat {self.agent} NEXUS-LOCALSTACK\n\n- at: {iso()}\n- boot_id: {st['boot_id']}\n"
                                         f"- tasks_ok: {ok}/{len(st['tasks'])}\n- evidence: process progress only, not provider receipt\n")
        return {"status": "LOCAL_WRITTEN_READBACK_OK", "sha256": digest}

    # ------------------------------------------------------------- schedule
    def tick(self) -> dict:
        out = {"heartbeat": self.heartbeat()}
        now = time.time()
        if self.state.get("boot_id") != self.sup.boot_id:
            self.state["boot_id"] = self.sup.boot_id
            if now - self.state.get("last_startup_report", 0) > STARTUP_MIN_GAP_S:
                out["startup"] = self.write_report("start", "Supervisor-Start")
                if out["startup"].get("status", "").startswith("LOCAL_"):
                    self.state["last_startup_report"] = now
        t = now_vienna()
        slot = t.strftime("%Y-%m-%d")
        if "startup" in out and t.hour >= self.daily_hour:
            self.state["last_daily"] = slot  # start report of today's slot replaces the daily one
        if t.hour >= self.daily_hour and self.state.get("last_daily") != slot:
            out["daily"] = self.write_report("taeglich", f"Tagesbericht {slot}")
            if out["daily"].get("status", "").startswith("LOCAL_"):
                self.state["last_daily"] = slot
        bad = [x["name"] for x in self.sup.status()["tasks"] if x["status"] == "CIRCUIT_OPEN"]
        if bad and time.monotonic() - self.last_incident_mono > INCIDENT_WINDOW_S and bad != self.state.get("last_incident"):
            out["incident"] = self.write_report("incident", "CIRCUIT_OPEN: " + ", ".join(bad))
            self.last_incident_mono = time.monotonic()
            self.state["last_incident"] = bad
        self._save()
        return out


def atomic_write_text_create(path: Path, text: str) -> str:
    from .util import atomic_write_bytes
    return atomic_write_bytes(path, text.encode("utf-8"), create_only=True)
