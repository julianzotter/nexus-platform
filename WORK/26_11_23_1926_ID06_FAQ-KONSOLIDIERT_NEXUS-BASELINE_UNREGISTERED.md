---
name: 26_11_23_1926_ID06_FAQ-KONSOLIDIERT_NEXUS-BASELINE_UNREGISTERED
description: Konsolidierte FAQ (ID05 + ID06 + Scratch ID01) zu Persistenz, GitHub, Reporting, Registry, State-Control, Ordner, Domänen; mit Widerspruchsliste
version: v1.0
role: ID06
agent_name: Claude
runtime: claude.ai Cloud-Session + Desktop-Bridge (Gerät jul, win32)
manifest_ref: "NEXUS-ROLES-v1.1 §4"
timestamp: "2026-11-23T19:26+01:00"
status: PROPOSED
registration_status: REGISTRATION_PENDING
verification_status: REVIEW_PENDING (Review nicht durch ID06)
konsolidiert_aus:
  - 26_11_23_1920_ID05_FAQ_NEXUS-BASELINE-KERNFUNKTIONEN_UNREGISTERED.md (gdrive:1MRuCH59nfmfOue2wuSVGqr_4u7pGcl2q)
  - 26_11_23_1920_ID06_FAQ_NEXUS-BASELINE-CAPABILITIES_UNREGISTERED.md (gdrive:1D9TSvAG4S9pttv2fA5ee9JrGTUIGIqoM)
  - 26_11_23_FAQ_Question+Answers.md (gdrive:1dT_Q-yf3wzAyRwJF3uFBywUDbnGbisUV, byte-identisch mit ID06-FAQ, sha256 54de0354…)
quellen_gelesen: [MAN 1POfiQCW…, BAS 1CdwNHr6…, AGB _AGBS.md v007.1, RDM 1hZ9BHl6…, Folder.md 1nDjF78d…, AGENTS.md + .github/workflows @ e725ee0, GH REST actions/runs]
---
# FAQ NEXUS-Baseline (konsolidiert)

Status je Antwort: BELEGT = Quelle gelesen oder Test ausgeführt · INFERENZ = abgeleitet · OFFEN = Entscheidung ID01.
Kürzel: MAN Manifest · BAS Baseline · AGB _AGBS.md · RDM Control-Plane-README · FLD WORK/Folder.md · GH nexus-platform.

## A Persistenz
**Q1 API-Persistenz vs. lokaler Mount?**
Zwei unabhängige Fähigkeiten. API/MCP schreibt direkt in die Cloud, Beleg = Drive-Datei-ID. Mount = G:\ (Google Drive for Desktop) über eine Geräte-Bridge, Cloud-Sync durch den Desktop-Client. BELEGT: ID05 API PASS (1wjxj22S…), ID06 Mount PASS (12HB6noY…).

**Q2 Wie wird T3 "lokal gemountet" nachgewiesen?**
1 Schreiben über G:\…\WORK. 2 Lokaler Readback, SHA-256 gleich. 3 Datei per API finden, Datei-ID belegen. 4 Optional API-Rohbyte-Readback. Ergebnis FILE_VERIFIED, mit Registereintrag voll verifiziert (AGB §7). BELEGT: TEST_ID06_20261123-1837.md.

**Q3 Mount oder Cloud – was ist kanonisch?**
Kanonisch ist der Drive-Ordner `_developement/LLM-LOCAL-SSOT` (BAS MUST-20/21). G:\ ist eine lokale Sicht darauf. Mount = lokale Skripte, Solver, Windows-Tasks; Cloud = jede Runtime ohne Rechner. Als persistiert gilt eine Datei erst nach Cloud-Nachweis (INFERENZ aus AGB §7).

**Q4 Zwei getrennte Capability-Einträge?**
Ja. Ein Eintrag je Konnektor, Endpunkt und Ergebnis; Felder `id, konnektor, typ, endpunkt (ohne Secrets), ergebnis, beweis, zeitstempel`. Rechte je Lauf belegen, nie aus Labels ableiten (AGB §9, BAS MUST-123). Ablageform OFFEN (siehe W2).

**Q5 Sandbox-Leerstand (T4)?**
Sandbox ist flüchtig. Jede Datei, die nur dort liegt, vor Lauf-Ende nach WORK oder GitHub, je mit SHA-256. Arbeitskopien (Klone, Readbacks) dürfen bleiben, wenn gekennzeichnet. BELEGT: T4 ID06 PASS.

## B GitHub
**Q6 GitHub-Sync (T1)?**
Repo `julianzotter/nexus-platform` (privat, `main`). Eigener Branch je Agent, Commit, Push, Pull Request. Beweis: Commit-Hash, URL, SHA-256 Remote = Original. BELEGT: ID06 Branch `id06/baseline-eval-20261123`. ID05 schreibend NICHT GETESTET.

**Q7 Pull Request, Merge, Repositories?**
Kein Direkt-Commit auf `main` (MAN §10). Merge über PR nach CI und unabhängigem Review (AGB §10, BAS MUST-158), Freigabe ID01. Offene PRs: 0 (GH REST). ID06-Branch nicht gemergt, OFFEN. Weitere Repos: nexus-ai-operation-system, nexus-skills-factory, NEXUS-AI-ENGINEERING-APPS u. a.; Arbeits-Repo ist nexus-platform.

**Q8 GitHub Actions?**
| Workflow | Auslöser | Stand 2026-11-23 (GH REST) |
|---|---|---|
| CI | push, PR | success |
| contracts-qa | push, PR | nicht geprüft |
| NEXUS Drive to GitHub (drive-poll) | cron :07/:37, manuell | nicht geprüft |
| NEXUS Monitor | cron :17, push | failure (14:48 UTC) |
| NEXUS GitHub to WORK (delivery) | manuell / Folgelauf | failure, Run 45198599526 (14:50 UTC) |
| register-repair, registry-append | manuell | – |
Blocker: OAuth-Freigabe Google abgelaufen (laut ID05 `invalid_grant`, laut FLD `HTTP_400 Refresh-Token`). Erneuerung nur ID01 (AGB §8, FLD next_action). Auf dem ID06-Branch keine Läufe.

## C Reporting
**Q9 Statusbericht nach AGBs?**
Vorher `_AGBS.md` lesen und Version protokollieren (AGB §2). Name `YY_MM_DD_HHMM_ID##_THEMA_###.md`, Europe/Vienna, Nummer nur aus dem Ledger, sonst `UNREGISTERED` (AGB §4). UTF-8-Markdown, nie Google Doc (AGENTS.md). Ablage WORK (AGB §5, BAS MUST-21). Ergebnisfelder `FINDINGS | EVIDENCE/SOURCES | ARTIFACTS | RISKS | NEXT_ACTION | QA_STATUS` (BAS MUST-45).

**Q10 Reporting allgemein?**
1 Startbeleg (siehe W4). 2 Drei Ebenen je Vorgang: Artefakt, RUNLOG append-only, Statusbericht (AGB §8). 3 Fehler und Blocker immer melden (BAS MUST-53). 4 Publikation, Zustellung, ACK, Review, Release getrennt; ACK nur mit echter Antwort (AGB §10, BAS MUST-159). 5 Frontmatter mit Rolle, Executor, Provider, Modell, Runtime, Tool-Umfang, `capabilities_tested` (BAS MUST-150).

## D Architektur
**Q11 Kernfunktionen?**
Governance-Framework für deterministische, auditierbare Engineering- und Wissensarbeit (MAN §1). Prinzipien SSOT-, DETERMINISTIC-, REGISTRY-, EVIDENCE-, LOCAL-FIRST, IDENTITY-BEFORE-SEMANTICS, RETRIEVAL-BEFORE-RAG, REUSE-BEFORE-CREATE, VERIFY-BEFORE-PROMOTE (MAN §3). Führung: ID01 entscheidet → ID02 orchestriert → ID03–ID08 führen aus/prüfen → ID02 fasst zusammen → ID01 gibt frei (MAN §5). Rollen: ID02 ChatGPT Private, ID03 ChatGPT Assistant, ID04 Gemini, ID05 Perplexity, ID06 Claude, ID07 DeepSeek, ID08 Ollama (MAN §4). Zahlen rechnet ein Python-Solver (BAS MUST-155).

**Q12 Ordner?**
| Ordner | Funktion | Beleg |
|---|---|---|
| `_developement/LLM-LOCAL-SSOT/` | Manifest, Baseline, Register, Steuerdateien | BAS MUST-20, AGB §5 |
| `…/WORK/` (1HEcfQaf…) | Aufträge, ACKs, Statusberichte, Artefakte | BAS MUST-21 |
| `…/LLM-HISTORY-LOG/` (1uavEf5g…) | Heartbeats, Watch-Läufe, Startzeilen | AGB §5 |
| `WORK/_ARCHIVE_STEUERDATEIEN` | überholte Steuerdateien, nur verschieben | AGB §5 |
| `_INDEX.MASTER/` | einziger globaler Index | BAS MUST-22/24 |
| `NEXUS.DASHBOARDS` | Dashboards, Statusseiten | AGB §5 |
| `SCRIPTS`, `NEXUS.MCP.SERVER`, `_developement/MCP-ACCESS-TOOLS` | Code, Konnektoren; Code-SSOT OFFEN | Bestandsaufnahme ID06 |
| GH `nexus-platform` | ec5_core, rfem_parametric, contracts, registry, mcp_bridge, orchestrator, evaluation, USECASES, WORK, backups | GH |

**Q13 Domänen und Use Cases?**
Tragwerksplanung/AEC: Eurocode-Nachweise (EC2, EC5), parametrische Modellierung (RFEM), Python-Berechnung, quellengebundenes RAG in Drive, LLM-Orchestrierung. Use Cases mit Spuren in WORK/GH: P205 Eisteiche FT-Träger-Matrix, W012, Favoritenstraße 250, Seilnetz Böblingen, Semantic-MVP-Pilot 25–50 Ressourcen (BAS MUST-154), Normen-/Standards-Watch, Meta-Wissen Holzbau. Kein Produktionsstatus: PASS ist Testergebnis, keine Freigabe (MAN §8, BAS MUST-151).

## E Steuerung und Register
**Q14 State Control, Scheduled Tasks?**
Zustände: OPEN → CLAIMED → RUNNING → DONE, sonst BLOCKED / REVIEW_REQUIRED / FAILED (MAN §6, RDM, BAS MUST-43/44). Ticket-, Entwicklungs-, Evidenz- und Eval-Status sind getrennte Felder (BAS MUST-151). Drive weckt keinen Agenten (RDM, BAS MUST-96). Wecken: Windows-Aufgaben + Wächter-Skript als Hauptweg, GitHub-cron optional (AGB §10); GitHub-cron derzeit blockiert (Q8). Kontrollpanel beim Start öffnen (AGB, Ergänzung 2026-11-23).

**Q15 Registry?**
Ein Register `file-registry.jsonl`, append-only, kein paralleles Register (AGB §6.1). `artifact_id = gdrive:<Drive-ID>`, Startstatus REVIEW_PENDING; Registrierung ≠ Freigabe (AGB §6.3/6.4). Ein Ledger-Schreiber: Claude, Entscheid ID01 2026-11-17 (AGB §6.6). Keine IDs aus `max(filename)+1` (BAS MUST-152). Ticket-Koordination: Ticket Registry (BAS MUST-152). Rollen-IDs nur in MAN §4 (BAS §17).

## F Widersprüche
| # | Widerspruch | Quellen | Vorschlag / Owner |
|---|---|---|---|
| W1 | AGB §9: Claude-Kennung "offen" ↔ MAN §4: ID06 = Claude | AGB §9, MAN §4 | ID01: AGB-Text nachziehen |
| W2 | `_CAPABILITIES.jsonl` als eigenes Register ↔ "kein paralleles Register" ↔ AGB §9 "Capability-Matrix nur historisch, Rechte je Lauf belegen" | Sprachrunde, AGB §6.1, §9 | ID01: als Laufbeleg-Log mit Verweis auf file-registry beschließen oder als Spalte in file-registry |
| W3 | Zwei T5-Golden-Cases: ID05 (120/240, L 4,0, q 5,0, k_h = 1,0 fest, η 0,565) ↔ ID06 (120/360, L 5,0, q 6,0, k_h nach §3.3(3) 1,052, η 0,447). Gegenrechnung ID06: ID05-Fall mit k_h nach §3.3(3) = 1,096 ergibt η 0,516; k_h = 1,0 ist zulässig konservativ, aber nicht normexakt. | WO v3 (ID05), T5-Skript ID06 | ID01: einen Golden Case festlegen; Empfehlung k_h nach §3.3(3) |
| W4 | Zwei Startbelege: Zeile in LLM-HISTORY-LOG (AGB §2.3) ↔ START_ACK in WORK (Ergänzung 2026-11-23) | AGB | ID01: beide oder einen |
| W5 | Ledger-Nummern: ID03 vergibt sie für Watch-Berichte (BAS §7 Nachtrag 2026-11-08) ↔ ein Ledger-Schreiber Claude (AGB §6.6) | BAS §7, AGB §6.6 | ID01: Zuständigkeit je Ledger klären |
| W6 | Rollenregister-Link zeigt auf ein Google Doc (1o5ywhvaz0…) ↔ AGB §1: MD-Dateien kanonisch, Google Docs nur Archiv | BAS §17, RDM, AGENTS.md, AGB §1 | ID01: Links auf MD 1POfiQCW… umstellen |
| W7 | Baseline beginnt mit einem eingefügten ID02-Rollenblock ↔ BAS §17 "keine eigene Rollentabelle" | BAS Kopf, BAS §17 | ID02/ID01: Block in Fußnote/Verweis umwandeln |
| W8 | FLD `sync_rule`: "nur GitHub-Review-Snapshots, kein bidirektionaler Sync" ↔ Workflows Drive→GitHub und GitHub→WORK | FLD, .github/workflows | ID01: Sync-Regel oder Workflows angleichen |
| W9 | Vier Statusquellen: Ticket Registry (BAS MUST-152), Folder.md, Kontrollpanel, Statusberichte in WORK | BAS, FLD, AGB-Ergänzung | ID01: eine führende Quelle, Rest als Projektion |
| W10 | Unabhängigkeit: ID05 läuft laut eigenem Frontmatter auf "Claude Opus 5.5" ↔ ID06 ebenfalls Claude. Review ID05↔ID06 ist nicht modellunabhängig (MAN §4: zwei Rollenlabels belegen keine Unabhängigkeit) | ID05-FAQ Frontmatter, MAN §4 | Review-Matrix: ID06 nicht durch ID05 prüfen lassen, sondern durch ID02/ID03/ID07 |
| W11 | Duplikate ohne Rollen-ID im Namen: `26_11_23_FAQ_Question+Answers.md` = ID06-FAQ (sha256 54de0354…); `26_11_23_ID-PERPLEXITY_BASELINE-INSTRUCTION-EVALUATION.md` = ID05-Protokoll (b13372b3…) | AGB §4, BAS MUST-157 | DUPLICATE_CANDIDATE, nach Freigabe in Archiv verschieben |
| W12 | WORK ist "anyone: writer" ↔ Herkunft nur über Dateiname belegbar; Sprachtexte unter "ID 06" stammten nachweislich nicht von ID06 | FLD problems, Sitzung 2026-11-23 | Meldungen nur mit Datei- oder Hash-Beleg werten |
| W13 | WO v1 T3 "lokal gemountet" ↔ v2/v3 "Drive-Mount" bzw. "in WORK schreiben" | WO v1–v3 | v3.1: T3a API, T3b Mount getrennt |
| W14 | AGENTS.md Schritt 1: Folder.md vor jeder Aktion lesen ↔ ID06 hat es erst in diesem Lauf gelesen | AGENTS.md | ID06: Startroutine ergänzt |

## G Entscheidungen für ID01
- #E1 → Golden Case T5 (W3)
- #E2 → Capabilities-Ablage (W2)
- #E3 → Startbeleg (W4) und Ledger-Zuständigkeit (W5)
- #E4 → OAuth erneuern (Q8)
- #E5 → Duplikate archivieren (W11)

## LOG
- 2026-11-23 19:26 | ID06 | FAQ konsolidiert aus ID05-, ID06- und Scratch-FAQ; Quellen MAN, BAS, AGB, RDM, FLD, GH gelesen; GH-Läufe per REST geprüft; T5-Fälle nachgerechnet | R1 eingehalten
