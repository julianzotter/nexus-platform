---
schema: IOD.01/1.0
run_id: 2026-10-13__NEXUS-MULTI-LLM-ORCHESTRATOR__R001
type: lessons_learned
title: Lessons Learned
owner: ID-01-HUMAN (DI Julian Zotter)
agent: Perplexity Computer (Orchestrator)
created_ts: 2026-10-15T06:00:27+02:00
session: https://www.perplexity.ai/computer/tasks/a612993d-02b5-4dfb-92ac-9bc7428de58e
project: NEXUS-AI Multi-LLM System
---

# 02 Lessons Learned
Format: Bedingung → Muster → Evidenz (Status PROPOSED).

| ID | Bedingung | Muster | Evidenz |
|---|---|---|---|
| LL-01 | Drive-Datei soll aus der Perplexity-Sandbox angelegt werden | Sandbox-Uploads sind per Policy (`ask_required`) gesperrt, auch nach Freigabe und Re-Auth → Ablage über lokalen Sync (G:\ bzw. rclone), nicht wiederholt versuchen | 13.10., 4 Versuche, 403 |
| LL-02 | PowerShell-Skript aktualisiert sich selbst per `git pull` | Laufende Instanz nutzt alte Fassung → nach Skript-Änderung zweiten Lauf einplanen (oder Re-Exec nach Pull) | Sync 13:24 nur 2x OK, 13:26 3x OK |
| LL-03 | Befehle werden vom Owner kopiert | Nur reine Befehlszeilen liefern; Hinweis cmd vs. PowerShell (`PS` im Prompt) | cmd-Fehler 13:2x |
| LL-04 | Ollama antwortet 404 auf /v1/chat/completions | Modell fehlt oder Download unvollständig → `ollama list`; OpenAI-kompatibler Endpunkt ignoriert num_ctx → native `/api/chat` mit `options.num_ctx` | PR #9, #11 |
| LL-05 | Modell `gpt-5` mit temperature=0.0 | Wird mit HTTP 400 abgelehnt → Temperatur weglassen oder anderes Modell | Council-Befund Claude Fable 5.1, extern bestätigt |
| LL-06 | Privacy-Marker-Prüfung | Immer casefold über Prompt + Systemtext + Anhänge, mit Negativtests | Alle 3 Council-Modelle |
| LL-07 | Mehrere Sessions schreiben ins selbe Repo | Vor jedem neuen Artefakt `main` pullen und vorhandene Ordner prüfen (evaluation/ kam aus Parallel-Session) | 13.10., Commit 78ce229 |
| LL-08 | Notenstreuung zwischen LLM-Prüfern | Ursache meist Ankerauslegung → Median je Kriterium als Konsens, Spannweite >1 gezielt prüfen | Gesamt 1,8 bis 4,0 |
| LL-09 | Ablage von Session-Artefakten | IOD.01: Run-Ordner im fachlichen Zielbereich, nicht `_INDEX`; Ablageort vorher erfragen | Owner-Entscheidung 15.10. |
