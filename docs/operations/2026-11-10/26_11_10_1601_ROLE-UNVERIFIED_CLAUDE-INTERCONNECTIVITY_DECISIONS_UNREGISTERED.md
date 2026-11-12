---
name: CLAUDE-INTERCONNECTIVITY-DECISIONS
version: "0.1.0"
status: PROPOSED
timestamp: "2026-11-10T16:01:31+01:00"
ticket_id: WO-20261031-NEXUS-BOOTSTRAP-PERSONAL-SETTINGS
claude_ref: WO-20261110-CLAUDE-ERGO
owner_id: ID01
agent_id: null
executor: OpenAI Codex Work
executor_instance: /root
ledger_number: null
---

# Claude ↔ ChatGPT Work · Entscheidungsmatrix

Ticketstatus **OPEN**. Dieser Stand dokumentiert Empfehlungen. Ausführungsentscheidungen zu Claude, Scheduler und PR #66 liegen bei ID01. Rollen-ID und fortlaufende Ledgernummer des Berichts sind offen. Der kanonische Ablageort ist [NEXUS WORK](https://drive.google.com/drive/folders/1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP). GitHub hält den Review-Snapshot.

| Entscheidung | Empfehlung |
|---|---|
| Q1 · Sprache | Deutsch als Standard. Englisch auf ausdrücklichen Wunsch oder bei englischsprachigem Zielpublikum. Originalzitate unverändert. |
| Q2 · Root | `_developement/LLM-LOCAL-SSOT/WORK` gemäß CURRENT Baseline §4. `_deployment` als historischen Verweis dokumentieren. |
| Q3 · Morning Recall | Zuerst `NEXUS-START` auf Abruf testen. Optional werktags 08:15 Uhr Europe/Vienna. |
| Merge PR #66 | Draft belassen. Neu gespeicherte Skill-Fassungen gegen den PR-Head per SHA-256 abgleichen, Abweichung 21/24 Manifestdateien klären und Inventarbefunde prüfen. |
| GO WO-0 | Empfohlen. Bestehenden Bootstrap mit dem Claude-Entwurf abgleichen. Diff für Profil, `_SOUL.md` und `_GLOSSAR.md` vorlegen. |
| GO export | Empfohlen. Originalchat `d96056dc-1b5c-494f-ae27-1861be3cdc68`, Turns 0–7, als Markdown nach WORK exportieren. Sprecher, Turnnummern und Wortlaut erhalten. Fehlende Turns kennzeichnen. Drive-Link und Readback melden. |
| Drei Einstiegsskills | Nach Abgleich zuerst `nexus-start` speichern und testen, danach `workspace-housekeeping` und `nexus-settings-kit`. `daily-recall` bleibt der separate Abruf für Zufallsvorschläge. |

## Evidenz und offene Nachweise

- ID06 bestätigt den Originalchat „Claude-Ordnung und Skills-Setup“ vom 10.11.2026 und die gelesenen Turns 0–1. Turns 2–7 stehen aus. [Claude-Original](https://claude.ai/chat/d96056dc-1b5c-494f-ae27-1861be3cdc68)
- ChatGPT-Profil und Projekt #07a gespeichert und per Readback geprüft. Web-Starttest und Abruf der vier Projektquellen bestanden. Windows/RFEM separat abnehmen. [Abnahmechat](https://chatgpt.com/g/g-p-6988c630ecdc8191949541f7a137cbaf-07a-nexus-ai-aec-operation-system-dms-wms-kb/c/6af32ce1-dba8-83eb-95a4-210842fe2b7a)
- PR #66 enthält den Review-Snapshot von neun gespeicherten Claude-Skills. CI `test` war am geprüften Head erfolgreich. CodeRabbit übersprang den Draft. Die drei später laut ID06 gespeicherten Skills sind am selben Head in `_proposed/` dokumentiert. Bytegleichheit mit den im Konto gespeicherten Fassungen bleibt offen. [PR #66](https://github.com/julianzotter/nexus-platform/pull/66)
- Profiltext v2, Memory-Bereinigung, SOUL/GLOSSAR/CLAUDE.md, Projektkarte, Scheduled-Task-Fixes und Laufprotokoll bleiben laut Claude-Statusmatrix offen. Ledgerzuordnung über ID03 klären.

## Ablage und Prüfung

Manueller Snapshot mit Bytevergleich zwischen WORK und GitHub. Vorhandene Repository-CI deckt die PR-Prüfung ab. Eine zusätzliche Action ist für diese einmalige Ablage nicht erforderlich.

Quellen: [CURRENT Baseline](https://docs.google.com/document/d/1Ig0YFqbWji6B5-oOFcxuVpHb5GEBk0HlbJVz51rf9ho/edit) · [_AGBS.md v005](https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view) · [Ticketregister](https://docs.google.com/spreadsheets/d/1o1ZCZUgsCGTDOwdbJ7EbUCKOKJng1LcJLFnrRiPjYTE/edit#gid=1465731618&range=A20%3AK20)
