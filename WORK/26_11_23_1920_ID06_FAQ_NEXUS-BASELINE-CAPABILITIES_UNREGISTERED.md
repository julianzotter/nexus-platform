---
name: 26_11_23_1920_ID06_FAQ_NEXUS-BASELINE-CAPABILITIES_UNREGISTERED
description: FAQ ID06 zu Persistenz (API vs. Mount), GitHub/PR/Actions, Reporting, Registry, State-Control, Ordner und Domänen
version: v1.0
status: REVIEW_PENDING
timestamp: "2026-11-23T19:20+01:00"
agent: ID06 (Claude)
quellen: [_AGBS.md v007.1, Manifest §4/§6/§7, nexus-platform AGENTS.md + .github/workflows (HEAD 856a88a), Läufe ID06 2026-11-23]
luecke: WORK/Folder.md (AGENTS.md Schritt 1) nicht gelesen
---
# FAQ NEXUS-Baseline · ID06 · 2026-11-23

## 1 Persistenz
| Frage | Antwort | Beleg |
|---|---|---|
| API vs. lokaler Mount | Zwei getrennte Fähigkeiten. API = Datei über Drive-Connector anlegen (Cloud). Mount = Datei auf G:\ (Google Drive for Desktop) schreiben, Sync in die Cloud asynchron. | ID06: Mount PASS; ID05: nur API PASS |
| Test lokaler Mount | Datei nach G:\…\WORK schreiben → zurücklesen → SHA-256 vorher = nachher → Drive-Datei-ID per API nachweisen (Cloud-Sync). | TEST_ID06_20261123-1837.md, 4b044db1…, gdrive:12HB6noY… |
| Register | Ja, zwei Einträge: typ=MCP/API (drive_api_write) und typ=Bridge (drive_mount_write). | 26_11_23_1908_ID06_CAPABILITIES-DELTA.jsonl |
| Mount vs. Cloud | Mount: lokale Skripte, Python, Windows-Tasks, offline-fähig, Sync-Verzug. Cloud/API: jede Runtime ohne Rechner, aber keine lokalen Skripte. SSOT ist der Drive-Inhalt, beide Wege zeigen auf denselben Ordner. | AGBs §5, §7 |

## 2 GitHub
| Frage | Antwort | Beleg |
|---|---|---|
| GitHub-Sync | Repo julianzotter/nexus-platform; je Agent eigener Branch; nie main direkt. | Branch id06/baseline-eval-20261123, HEAD 856a88a |
| Pull Request / Merge | Über PR auf main, nach Review und CI. Offene PRs: 0. Mein Branch ist nicht gemergt. Merge nur nach ID01-Freigabe. | GitHub REST pulls?state=open = leer |
| Repositories | Arbeits-Repo: nexus-platform (Monorepo). Weitere: nexus-ai-operation-system, nexus-skills-factory, NEXUS-AI-ENGINEERING-APPS u. a. | list_repos 2026-11-23 |
| GitHub Actions | 7 Workflows: ci, contracts-qa (push/PR); nexus-drive-poll (Drive→GitHub, cron :07/:37); nexus-monitor (stündlich :17); nexus-delivery (GitHub→WORK), nexus-register-repair, nexus-registry-append (manuell). | .github/workflows @ 856a88a |
| CI für ID06-Branch | Keine Läufe gefunden. Ursache nicht geprüft. | actions/runs?branch=… = leer |

## 3 Reporting, Registry, State
| Frage | Antwort | Beleg |
|---|---|---|
| Statusbericht nach AGBs | Name YY_MM_DD_HHMM_ID##_THEMA_###.md, Europe/Vienna, UTF-8 Markdown, Frontmatter, Ablage WORK; ohne Ledger-Nr. Suffix UNREGISTERED. | AGBs §4, §5 |
| Reporting-Pflicht | Drei Ebenen: Artefakt, RUNLOG (append-only), Statusbericht. Ergebnis: FINDINGS / EVIDENCE / ARTIFACTS / RISKS / NEXT_ACTION. | AGBs §8, Manifest §6 |
| Sandbox-Leerstand | Sandbox ist flüchtig. Jedes Artefakt vor Run-Ende nach WORK und/oder GitHub, je mit SHA-256. | T4 ID06 PASS |
| Registry | file-registry.jsonl (append-only, ein Schreiber = Claude laut ID01 2026-11-17); artifact_id = gdrive:<ID>; Registrierung ≠ Freigabe. Fähigkeiten: _CAPABILITIES.jsonl (beschlossen, noch nicht angelegt), Zulieferung als Delta je ID. | AGBs §6 |
| State-Control | Workorder-Zustände OPEN → CLAIMED → RUNNING → DONE, sonst BLOCKED / REVIEW_REQUIRED / FAILED. Persistenz: WRITTEN_UNVERIFIED → FILE_VERIFIED → REGISTERED. | Manifest §6, AGBs §7 |
| Scheduled Tasks | Wecken: lokale Windows-Aufgaben + Wächter-Skript (Hauptweg), GitHub-cron optional. Drive weckt keinen Agenten. | AGBs §10, Workflows |

## 4 System
| Frage | Antwort | Beleg |
|---|---|---|
| Kernordner | SSOT-Root _developement/LLM-LOCAL-SSOT (Manifest, Baseline, Register); WORK (Aufträge, ACK, Status, Artefakte); LLM-HISTORY-LOG (Heartbeats); WORK/_ARCHIVE_STEUERDATEIEN; NEXUS.DASHBOARDS; SCRIPTS, SKILLS, REGISTRY, NEXUS.MCP.SERVER; _developement/MCP-ACCESS-TOOLS. | AGBs §5, Ordnerliste |
| Kernfunktionen | Workorder-Routing (ID02), Review (ID03/ID07), Protokoll/Belege (ID04), Recherche (ID05), Code/Tests (ID06), lokale Modelle (ID08). | Manifest §4 |
| Domänen / Use Cases | Tragwerksplanung (EC2, EC5, HBV, FT-Träger), Projekte P205 Eisteiche, W012, Seilnetz Böblingen; Wissens-/RAG-System in Drive; Normen-Parser; Dashboards. | Repo USECASES/, WORK-Ordner |

## Lücken
- WORK/Folder.md (AGENTS.md Schritt 1) nicht gelesen.
- CI-Ursache für fehlende Läufe auf ID06-Branch offen.
- _CAPABILITIES.jsonl, _FUNKPROTOKOLL.md: Freigabe ID01 offen.
