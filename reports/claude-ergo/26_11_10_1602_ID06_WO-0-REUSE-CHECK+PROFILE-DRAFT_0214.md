---
name: WO-0-REUSE-CHECK-CLAUDE-ERGO
description: Reuse check of the approved NEXUS bootstrap against the Claude personalisation plan, Claude profile text draft, skill-PR consolidation map, decisions for ID01
version: 0.1.0
status: ENTWURF
timestamp: 2026-11-10T16:02+01:00
agent_id: ID06
executor: Claude Fable 5.2, claude.ai cloud session
ticket_id: WO-20261031-NEXUS-BOOTSTRAP-PERSONAL-SETTINGS
run_id: WO-20261110-CLAUDE-ERGO/WO-0
source_refs: bootstrap v0.7.2 (gdrive:1evrg3zgwMsqxCiSkXnni5HOYjNRQvR5u); _AGBS.md v005 (gdrive:10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg); WORK Folder.md (gdrive:11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH); ticket registry export 2026-11-10; PRs 66-69
tasks_done: bootstrap + AGBS v005 read in full; diff written; profile text drafted; four parallel skill PRs mapped
tasks_open: Manifest, Baseline, _FRONTMATTER not read; profile text not saved in Claude; NEXUS start test in a fresh Claude chat; registry entries
problems: four Claude sessions produced four overlapping draft PRs; model-effort-router exists in three different versions
open_questions: decisions D1-D7 below
result: plan corrected - no new _SOUL.md / _GLOSSAR.md control files
---

# TL;DR
The approved bootstrap already defines what goes into Claude: one short start reference in the profile instructions, sources stay in Drive. Two planned files (`_SOUL.md`, `_GLOSSAR.md`) contradict it and are dropped as separate control files.

# 1 Diff: bootstrap v0.7.2 / AGBS v005 vs. Claude plan (WO-20261110-CLAUDE-ERGO)
| Topic | Bootstrap / AGBS say | Claude plan said | Result |
|---|---|---|---|
| Profile instructions | Paste the common start reference; no rule full text, no memory copy as authority | WO-1 "condensed block" | Keep WO-1, build it on the start reference (section 2) |
| `_SOUL.md` | No new control file; bundle into existing sources | WO-3 new file | Dropped as file. Role/style lines go into the profile text |
| `_GLOSSAR.md` | AGBS v005 no. 6: extend the existing glossary / shared understanding, no parallel register | WO-4 new file | Dropped as file. Terms are proposed as additions to the existing glossary (location not verified) |
| `_FRONTMATTER.md` | Exists, status ENTWURF | template inside nexus-settings-kit | Use the existing file; skill template must follow it (not compared yet) |
| Memory | Short stable preferences only | WO-2 cleanup | Keep WO-2; remove duplicates, no rule copies |
| File names | `YY_MM_DD_HHMM_ID##_THEMA_###.md`, Vienna time | earlier files used other patterns | This file follows AGBS; number UNREGISTERED |
| Registration | Entry in existing `file-registry.jsonl`, artifact_id = gdrive:<file id> | ledger delta with PENDING IDs | Registry entry open (353 kB file, connector cannot append): REGISTRATION_PENDING |
| Persistence wording | "saved" only with raw-byte readback + hash | size-only readback | Today's Claude uploads are WRITTEN_UNVERIFIED |
| Claude test | New chat, prompt "NEXUS-Starttest ..." | not planned | Added as acceptance test after D2 |
| Root path | Baseline (per ChatGPT, not read here) and Drive practice: `_developement` | conflict in memory | Recommend `_developement`; `_deployment` is a typo variant |

# 2 Claude profile instructions - draft v2 (ENTWURF, about 1300 characters)
```
ROLLE: AI-Engineering-Assistent fuer Tragwerksplanung (EC2/EC5, HBV, FT) und NEXUS (Rolle ID06).
STIL: Deutsch als Standard; Englisch auf Auftrag. TL;DR zuerst, Stichworte, Tabellen, keine Fuellwoerter.
FAKTEN: nichts raten. Quelle + Stand nennen. Ohne Beleg: "nicht beurteilbar - nicht dokumentiert". Teilpruefung als solche benennen.
STATIK: Formel vor Zahl, SI-Einheiten, Einheiten-Check, Gleichgewicht (Sum V, Sum M), Plausibilitaet, Norm mit Abschnitt. HBV: Gamma-Verfahren EC5 Anhang B; Kerven: diskrete Methode. Holz: kmod, gamma_M, NKL, kh, ksys pruefen.
CODE: Python mit Type Hints, Funktionen max. 50 Zeilen.
ARBEIT: Bestand vor Neubau. Ein Run = ein Hauptziel. Bei Unklarheit fertigstellen und Annahme nennen.
SICHER: nie loeschen (nur verschieben), keine E-Mails senden.
NEXUS: Bei NEXUS-Auftraegen die Steuerquellen im Drive lesen (_AGBS.md, Manifest, Baseline, WORK/Folder.md) und Quellenstand nennen. Ergebnisse nach WORK (_developement/LLM-LOCAL-SSOT/WORK), Dateiname YY_MM_DD_HHMM_ID06_THEMA_###.md, Readback, LOG-Zeile. Memory ist keine Regelautoritaet.
```
Not included on purpose: rule full texts, role register, Drive IDs, model numbers (bootstrap: no competing SSOT in settings). The line "STIL: Deutsch" depends on D1.

# 3 Skill PRs from four parallel Claude chats (all draft, all CI-tested separately)
| PR | Content | Overlap |
|---|---|---|
| 66 | 9 saved account skills (byte-identical), 3 proposed, manifest, CI integrity step | model-effort-router (version A) |
| 67 | model-effort-router (B), agent-team-plan, model-release-digest | model-effort-router |
| 68 | nexus-start, workspace-housekeeping, nexus-settings-kit; WORK 0182-0184, ledger delta 0182-0186 | none |
| 69 | daily-recall (differs from account copy), model-effort-router (C), agent-team-orchestrator | daily-recall, model-effort-router |

- `model-effort-router`: three different texts (A, B, C). The account holds one saved copy (sha 042c234a...), equal to none of the repo files byte for byte.
- `daily-recall`: PR 66 copy equals the account copy; PR 69 copy does not.
- Merging more than one of 66/67/69 unchanged gives duplicate skill IDs. PR 66 now carries a CI gate that fails on duplicate IDs.
- Ledger: only PR 68's chat allocated numbers (0182-0186). No collision found in the PR texts; other Drive files of today not checked.

# 4 Check of ChatGPT's recommendation
| Point | ChatGPT | ID06 view |
|---|---|---|
| Q1 language | German default | Agree as proposal; it reverses the stored "answer in English" rule, so ID01 must say it |
| Q2 root | `_developement/...` | Agree |
| Q3 morning recall | test on demand first | Agree; no new scheduled task until the 5 existing ones are fixed |
| PR 66 | keep draft, compare hashes, clear 21 vs 24 | Done: 9 of 9 saved skills identical; PR text corrected to 24; the 3 saved Fable skills differ from the PR drafts (frontmatter) |
| WO-0 | yes | Done (this file) |
| Export | yes | Done (turns 0-7) |
| Entry skills staged | nexus-start first | Agree |
| Ledger via ID03 | yes | Agree: one allocator; 0182-0186 already used by PR 68's delta |
| Missing in ChatGPT's list | - | Four parallel PRs need one consolidation decision (D3) |

# 5 Decisions for ID01 (recommendation first)
- D1 Language: A German default, English on request (recommended) | B English always | C follow the language of each message
- D2 Profile text: A paste draft v2 into Claude profile settings, then run the start test (recommended) | B revise first | C wait for Manifest/Baseline read
- D3 Skill PRs: A consolidate into PR 66 - one version per skill, 67-69 closed as superseded, nothing deleted (recommended) | B merge 68 now, consolidate 66/67/69 later | C keep all as drafts
- D4 `model-effort-router`: A keep the version saved in the account (recommended) | B version from PR 67 | C version from PR 69
- D5 Ledger: A ID03 merges delta 0182-0186 and assigns numbers to the PENDING rows (recommended) | B ID06 writes a new full ledger copy | C leave as deltas
- D6 Scheduled tasks #P1-#P4: A fix time zones and connectors now, decide the double briefing separately (recommended) | B fix all four | C leave
- D7 Memory cleanup (duplicates IOD.01, continuity principle): A do it after D1 (recommended) | B do not touch

# LOG
- Written to WORK and to nexus-platform `reports/claude-ergo/` (PR 66 branch). No settings, memory, skills or scheduled tasks changed. Nothing deleted, no mail sent.

STATUS: PARTIAL | CHANGED: 2 report files, CI step, PR 66 text | TESTS: skill inventory, sha256 manifest, CI | SOURCE_STATUS: bootstrap v0.7.2 and AGBS v005 read in full; Manifest, Baseline, _FRONTMATTER not read | RISKS_GAPS: registry entries, raw-byte readback, parallel sessions | NEXT: ID01 decides D1-D7
