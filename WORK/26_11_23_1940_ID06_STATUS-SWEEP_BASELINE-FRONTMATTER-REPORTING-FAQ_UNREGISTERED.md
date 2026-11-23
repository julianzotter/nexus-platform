---
name: STATUS-SWEEP_BASELINE-FRONTMATTER-REPORTING-FAQ
description: Ist-Stand aus Drive (WORK, LLM-HISTORY-LOG) und GitHub zu Basic-Instructions-Eval, Frontmatter, Reporting/Agentenkommunikation und FAQ
role: ID06
timestamp: "2026-11-23T19:45+01:00"
status: SNAPSHOT
quellen: [Drive-Suche WORK + LLM-HISTORY-LOG ab 2026-11-23 15:00 Uhr, GH REST branches/pulls/commits, Capability-WO gdrive:1y0DSTvkH_04avqI8TZKyaKOy05gWfZgx]
---
## 1 Basic-Instructions-Evaluation
| Punkt | Stand | Beleg |
|---|---|---|
| Kanonisches Ticket | WO-20261112-ID02-CAPABILITY-ACK; ID02 Selbst-ACK DONE, ID03-ID08 OPEN laut Ticket; ID03-Abschlussreceipt 18:29 UTC angehängt | Capability-WO |
| Tests belegt | ID06 T1-T4 PASS; ID03 T1a/T2/T3a PASS, T3b BLOCKED | WORK |
| Ohne eigenen Lauf | ID02 (nur Watch-Läufe heute), ID04 (FAQ ohne Tests), ID05 (nur API-Upload), ID07 (Chat-Export), ID08 | WORK, LLM-HISTORY-LOG |
| Basic Instructions | Baseline CURRENT 2026-09-28 unverändert; kein Update | BAS |
| Prüfvorlage | v3 (ID06, Entwurf, Mängel laut ID03), v3.1 (ID03, Vorschlag) | WORK |

## 2 Frontmatter-/Steuerdateien
| Datei | Stand |
|---|---|
| _AGBS.md | v007.1 + ID01-Ergänzung, geändert 2026-11-23 13:56 |
| _TROUBLESHOOTING.md | geändert 2026-11-23 15:15 |
| _CAPABILITIES.jsonl, _FUNKPROTOKOLL.md | beschlossen, nicht angelegt |
| _FRONT_LOG.md, _FRONTMATTER_v006-PROPOSAL | unverändert (Okt/Nov) |

## 3 Reporting und Agentenkommunikation
| Punkt | Stand |
|---|---|
| LLM-HISTORY-LOG heute | ID02 Watch-Läufe 11:53/14:06/17:12, ID02 Panel-JSON, ID03 RUNLOG; ID06 Startzeile fehlte → nachgeholt |
| ACK-Dateien WO-BASELINE-EVAL | ID06 vorhanden; ID03 als START_ACK in Capability-WO; übrige fehlen |
| Registerdeltas | Ledger 0212-0256 gemergt (0257); file-registry-Delta ID03 (4 Zeilen) offen |
| GitHub | Branches id03/… und id06/baseline-eval-20261123; 0 offene PRs; main zuletzt PR #117 (14:48 UTC); GitHub→WORK und Monitor failure |

## 4 FAQ
| Datei | Rolle | Bemerkung |
|---|---|---|
| 26_11_23_1923_ID03_NEXUS-BASELINE_FAQ-REVIEW | führend | mit v3.1 |
| 26_11_23_1926_ID06_FAQ-KONSOLIDIERT | ergänzend | 14 Widersprüche |
| 26_11_23_1920_ID05_FAQ_…KERNFUNKTIONEN | ergänzend | – |
| 26_11_23_FAQ NEXUS-AI Baseline und Kernfunktionen.md | DUPLIKAT | byte-gleich ID05-FAQ, sha256 92531141… |
| 26_11_23_ID04_FAQ.md | ergänzend | ohne Frontmatter, text/plain |
| 26_11_23_DeepSeek-NEXUS Baseline Evaluation.md | Chat-Export ID07 | ohne ID-Präfix |
| 26_11_23_1920_ID06_FAQ_…CAPABILITIES | überholt | durch 1926 ersetzt |
| 26_11_23_FAQ_Question+Answers.md | Sammeldatei ID01 | 29 KB |
| 26_11_23_NEXUS-AI-ENGINEERING-KNOWLEDGE-SYSTEM_FAQ_V1.0 (GDoc, anderer Ordner) | älter, 16:02 | nicht geprüft |

## 5 Offen
- #O1 → Basic Instructions → Update nach ID01-Freigabe v3.1
- #O2 → ACKs → ID02, ID04, ID05, ID07 fehlen
- #O3 → file-registry → ID03-Delta mergen
- #O4 → Duplikate → 1 FAQ, 1 Protokoll (bereits ALT)
- #O5 → OAuth → ID01
