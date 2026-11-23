---
name: _GAP
description: Steuerdatei – Register aller festgestellten, gemeldeten und nicht behobenen Lücken, Mängel und Inkonsistenzen (Baseline, Reporting, GitHub, FAQ, Frontmatter, Logs)
version: v0.1
status: PROPOSED (neue Steuerdatei, Freigabe ID01 offen)
owner_file: ID06
timestamp: "2026-11-23T19:50+01:00"
regel: append-only; neue Lücke = neue Zeile; Statuswechsel = neue Zeile mit gleicher GAP-ID, nie Zeile ändern
statuswerte: OPEN | IN_PROGRESS | BLOCKED | DECISION_ID01 | CLOSED
quellen: [MAN 1POfiQCW…, BAS 1CdwNHr6…, _AGBS.md v007.1, Folder.md 1nDjF78d…, WORK-Dateien 2026-11-23, GH nexus-platform REST]
---
| GAP | Bereich | Lücke / Mangel | Beleg | Owner | Status | Seit |
|---|---|---|---|---|---|---|
| G01 | GitHub | OAuth abgelaufen: "Drive to GitHub" und "GitHub to WORK" failure | Run 45198599526, Schritt "Check Drive credentials" | ID01 | DECISION_ID01 | 2026-11-16 |
| G02 | GitHub | Monitor fail-closed ("Assert operational monitor evidence") | Run 45198194995 | ID06 nach G01/G05 | BLOCKED | 2026-11-23 |
| G03 | Baseline | Basic Instructions nicht aktualisiert; v3.1 (ID03) nicht freigegeben | BAS Stand 2026-09-28 | ID01 | DECISION_ID01 | 2026-11-23 |
| G04 | Register | _CAPABILITIES.jsonl beschlossen, nicht angelegt; Konflikt AGB §6.1 (kein paralleles Register) und §9 | Sprachrunde, AGB | ID01 | DECISION_ID01 | 2026-11-23 |
| G05 | Register | file-registry.jsonl: ID03-Delta (4 Zeilen) ungemergt; Tagesartefakte ID06 unregistriert | Capability-WO 1y0DSTvk…, Abschnitt Registerdelta | ID06 | OPEN | 2026-11-23 |
| G06 | Ledger | WO-Merge Schritt 6: SHA256 für 0212-0235 fehlen | Report 26_11_23_1940_ID06_REPORT_LEDGER-MERGE | ID06 | OPEN | 2026-11-17 |
| G07 | Ledger | Zwei Dateien "00_ID_LEDGER.csv" im SSOT-Root (2127 B alt, 75843 B Master) → lokaler Konfliktname, Cloud-Umbenennung | Drive-Metadaten 1Qso4VQE… | ID01 (Move-Freigabe) | DECISION_ID01 | 2026-11-23 |
| G08 | Reporting | ACK zu WO-BASELINE-EVAL fehlt: ID02, ID04, ID05, ID07, ID08 | WORK-Suche | je ID | OPEN | 2026-11-23 |
| G09 | Baseline | T3b lokaler Mount nur bei ID06 belegt; ID03 BLOCKED, ID05 FAIL | Prüfmatrix | strukturell | OPEN | 2026-11-23 |
| G10 | Baseline | T5: zwei Rechenfälle (ID05 k_h=1,0 / ID06 k_h §3.3(3)); keine Normausgabe/NA; Sollwert vom selben Autor | FAQ ID06 W3, Review ID03 | ID01 + ID07 | DECISION_ID01 | 2026-11-23 |
| G11 | Baseline | T6 lokales RAG: kein Endpunkt, keine Golden-Frage | Review ID03 | ID01/ID06 | OPEN | 2026-11-23 |
| G12 | Review | ID06 lokaler Push/G:-Write ohne fremden Beleg; ID05 und ID06 gleiche Modellfamilie; ID03 nur intern geprüft | Review ID03 §5.2, ID05-Frontmatter | ID02/ID07 | OPEN | 2026-11-23 |
| G13 | Governance | AGB §9 "Claude-ID offen" ↔ MAN §4 ID06 = Claude | AGB, MAN | ID01 | DECISION_ID01 | 2026-11-17 |
| G14 | Governance | Ledger-Nummernvergabe: BAS §7 Nachtrag (ID03) ↔ AGB §6.6 (Claude) | BAS, AGB | ID01 | DECISION_ID01 | 2026-11-17 |
| G15 | Governance | Doppelter Startbeleg: LLM-HISTORY-LOG (AGB §2.3) ↔ START_ACK WORK (Ergänzung 2026-11-23) | AGB | ID01 | DECISION_ID01 | 2026-11-23 |
| G16 | Governance | Rollenregister-Links auf Google Doc statt MD (AGB §1: MD kanonisch) | BAS §17, RDM, AGENTS.md | ID02 | OPEN | 2026-11-17 |
| G17 | Governance | Baseline-Kopf enthält ID02-Rollenblock ↔ BAS §17 | BAS | ID02 | OPEN | 2026-11-11 |
| G18 | Governance | Folder.md sync_rule "kein bidirektionaler Sync" ↔ Workflows Drive↔GitHub | FLD, .github/workflows | ID01 | DECISION_ID01 | 2026-11-16 |
| G19 | Reporting | Vier Statusquellen ohne Führung: Ticket Registry, Folder.md, Kontrollpanel, WORK-Berichte | BAS MUST-152, FLD, AGB | ID01 | DECISION_ID01 | 2026-11-23 |
| G20 | FAQ | Fragmentiert: 7 Dateien in WORK + GDoc FAQ V1.0 + Zu-den-FAQs 07.08; FAQ-SSOT nicht festgelegt | Sweep 1940 | ID01 | DECISION_ID01 | 2026-11-23 |
| G21 | FAQ | Duplikat "26_11_23_FAQ NEXUS-AI Baseline und Kernfunktionen.md" = ID05-FAQ (sha256 92531141…) | Hash ID06 | ID01 (Move) | OPEN | 2026-11-23 |
| G22 | Frontmatter | Nicht AGB-konform: 26_11_23_ID04_FAQ.md (kein HHMM, kein Frontmatter, text/plain); DeepSeek-Export ohne ID; FAQ_Question+Answers ohne ID; IDNN-Protokoll id:NN, storage:sandbox_only | AGB §4 | Autoren | OPEN | 2026-11-23 |
| G23 | Provenienz | Texte als "ID 06" nicht von ID06 (Sprachrunde, DeepSeek); WORK anyone:writer, Herkunft nur über Dateiname | FLD problems, Sitzung | ID01 | OPEN | 2026-11-16 |
| G24 | Provenienz | Uploader der ID05-Datei technisch nicht authentifiziert | Review ID03 | ID05 | OPEN | 2026-11-23 |
| G25 | Baseline | ID06-v3-Entwurf fehlerhaft (NN, Mount abgeschwächt, T6 Doku, T5 Eigen-Soll) | Review ID03 | ID06 | CLOSED (ersetzt durch v3.1-Vorschlag) | 2026-11-23 |
| G26 | Reporting | ID06-Startzeile fehlte | LLM-HISTORY-LOG | ID06 | CLOSED 19:40 (nachgeholt, nicht rückdatiert) | 2026-11-23 |
| G27 | WORK | >2000 Dateien; ≥815 ID-UNVERIFIED, ≥346 UNREGISTERED; Bereinigungsplan ohne Freigabe | Inventar ID06 18:39 | ID01 | DECISION_ID01 | 2026-11-23 |
| G28 | Code-SSOT | Skripte in WORK, SCRIPTS, NEXUS.MCP.SERVER, MCP-ACCESS-TOOLS; P205-ps1 hashgleich doppelt | Review ID03 §5.3 | ID01 | DECISION_ID01 | 2026-11-23 |
| G29 | Runtime | device_bash: G: nicht mountbar (VM) | ID06 RUNLOG | – | OPEN (Workaround Bridge-Dateitools) | 2026-11-23 |
| G30 | GitHub | Branch id06/baseline-eval-20261123 ohne PR/Merge | GH REST | ID01 | DECISION_ID01 | 2026-11-23 |
| G31 | Reporting | Folder.md Stand 2026-11-16, Status-Projektion veraltet | FLD | Ledger-/Status-Schreiber | OPEN | 2026-11-16 |
| G32 | Reporting | Fremdbericht 19:45 mit falschen Aussagen: Branch "nicht sichtbar", Ledger-Merge "offen", Original/Duplikat vertauscht | GH REST (Branch HEAD 9b00a58), Ledger 0257 | Autor des Berichts | CLOSED (widerlegt, siehe Bericht 1950) | 2026-11-23 |
