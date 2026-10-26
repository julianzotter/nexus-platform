---
name: WEGWEISER-NEXUS-ENTRY-POINTS
version: 0.2.0
status: REVIEW
timestamp: '2026-10-26T16:48:23+01:00'
agent_id: ID03
executor_instance: /root
executor: OpenAI Codex
owner_id: ID01
ticket_id: WO-20261026-NEXUS-REPAIR-01
run_id: DOCSYNC-20261026T164823+0100
artifact_id: '0072'
gate: PENDING (Human Gate ID01)
development_status: PROPOSED
evidence_status: SOURCE_BACKED_DOCUMENT
canonical_source: Google Drive / LLM-LOCAL-SSOT
source_scope: sichtbarer Chat und explizit gelesene Quellen; keine vollständige Rückerfassung
  aller Accounts
source_refs:
- https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view
- https://docs.google.com/document/d/1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg/edit
- https://docs.google.com/document/d/1Ig0YFqbWji6B5-oOFcxuVpHb5GEBk0HlbJVz51rf9ho/edit
- https://drive.google.com/file/d/1y7jmHlyxq7Ja2xA2FM6MJapOjIkIMlqZ/view
- https://drive.google.com/file/d/1KeHVM_VC9nGHZTVyJd_5vBE6xBCG9KwX/view
supersedes:
  version: '0.1'
  drive_id: 1u1lqlQ0zn2HcauvEPc63mk8Kvu3sNC74
  content_hash_sha256: d1b2e45830a79a55049b5c4fb17bb939773428ebbb560ba5cf44ac43dfd944df
hash_scope: body_utf8_after_closing_frontmatter_lf
content_hash_sha256: f27f65058a04cb5ce6828a4a0412712104fa3b17ff5c6747a8598dfe4826d86c
hash: f27f65058a04cb5ce6828a4a0412712104fa3b17ff5c6747a8598dfe4826d86c
---
# 00_WEGWEISER_NEXUS-ENTRY-POINTS — Anker-Datei für alle Agenten (ID02–ID08)

`Historischer Ausgangsstand: PROPOSED vom 29.09.2026; aktuelle Korrektur unten. Kein neuer Governance-Kanon.`
`CANONICAL SOURCE = 00_NEXUS_MANIFEST__CURRENT__2026-09-28 + 00_NEXUS_BASELINE_INSTRUCTIONS__CURRENT__2026-09-28 (MUST-142). Diese Datei ist Wegweiser, kein Register (MUST-22/24).`

## 1. Bootstrap-Reihenfolge (MUST-143)
1. Manifest → 2. Baseline → 3. Ticket-Registry/WORK → 4. Ledger → 5. Templates → 6. Domänen-Wegweiser.
Kein Agent gilt als "wach", weil Drive aktualisiert wurde (MUST-96/159). Vor Arbeit: `CLAIM <ticket_id> <ID>` + executor/model/runtime angeben (MUST-150).

## 2. Kanonische Einstiegspunkte (Drive-ID = Identität)
| # | Artefakt | Drive-ID | Ort | Status |
|:--:|:--|:--|:--|:--:|
| E1 | 00_NEXUS_MANIFEST__CURRENT__2026-09-28 (gdoc) | 1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg | LLM-LOCAL-SSOT | CANON |
| E2 | 00_NEXUS_BASELINE_INSTRUCTIONS__CURRENT__2026-09-28 (gdoc) | 1Ig0YFqbWji6B5-oOFcxuVpHb5GEBk0HlbJVz51rf9ho | LLM-LOCAL-SSOT | CANON |
| E3 | NEXUS_CONTROL_PLANE__TICKET_REGISTRY (Sheet) | 1o1ZCZUgsCGTDOwdbJ7EbUCKOKJng1LcJLFnrRiPjYTE | LLM-LOCAL-SSOT/WORK | CANON |
| E4 | 00_ID_LEDGER.csv (aktuellen Inhalt lesen; ID-Vergabe nur im Ledger) | 1Uvb89wWOpte3iXWKm3qrg42dEwBb7nuG | LLM-LOCAL-SSOT | CANON |
| E5 | 00_DECISION_REGISTRY.jsonl v0.1 | siehe Ledger-Nachtrag | LLM-LOCAL-SSOT | PROPOSED |
| E6 | GROUNDING_PROMPT_SYSTEM_INVENTORY_v0.1 (gdoc) | 1M-lJu5DhT8wU_cQwEHO6-gb60vsNfKcE8_wneTkDQZQ | LLM-LOCAL-SSOT | REVIEWED |
| E7 | 26_09_28_0028_WHITEPAPER_NEXUS-AI-AEC-KES_MANIFEST+IMPL+USER-MANUAL_v1.0.md | 1N-HUl4Bq8DffMMF1FqLxPmjpTRV-lahl | LLM-LOCAL-SSOT | PROPOSED |
| E8 | Semantic-MVP Pilot-Input (Registry, 25–50 Ressourcen, MUST-154) | 1_N-J3pSAcHtr5sv0jGFmyWHpYQYz4TJj | – | CANON-INPUT |

## 3. Ordner (Top-10; vollständige 20er-Liste → `20_ORDNERPFADEN_UND_WEGWEISER.md`, Drive-ID 1gKxjfq99vzOyL0Lfqf5W83v74jem9DSE)
| Ordner | Drive-ID | Zweck |
|:--|:--|:--|
| _developement | 1OIyJI6rljIi8zNsT-iwg47NsuguoZqTB | Entwicklungs-Root |
| _developement/LLM-LOCAL-SSOT | 1j3FLJkWpQv6xGA_KO0D9sMyA11f0vxBV | Governance, Registries, Reports (mit Präfix) |
| _developement/LLM-LOCAL-SSOT/WORK | 1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP | WorkOrders, Tickets, Run-Outputs (ohne Präfix) |
| _developement/MCP-ACCESS-TOOLS | 1fRa7rQvKi-BkhVIzjXPcY_u8iIJ4Vn5J | Runtime-/Tool-Kandidaten |
| _INDEX.MASTER | 1oWX4JbZlJkUZJWwgSA_KxuFJRemvZoxK | globale Discovery (MUST-22), Tree-Snapshots |
| _INDEX | 1okgsbzTD2QuHZqPGYTrzmf_NESmkkaqD | Index-/Workflow-Bestand, _PENDING, ARCHIVE_HTML_DASHBOARDS |
| _INDEX/00_ARTEFAKTE-BIBLIOTHEK | 1jXreTO8oEDblDcTCXAEHVWvioMFJPMXz | Master-Templates (diese Datei) |
| _INDEX/00 TREE-LISTS_INDEX-LISTS | 1X33b5oMAWOywd-1SeEO6lxJYOEJ9XL6A | Alt-Indexlisten/Trees (Reuse vor Neuanlage, MUST-23) |
| _INDEX_LNK | 1GcIKgilIzIh8TZsD0y9p0MMfjd5hW7SR | Benchmarks HOLZ/BETON/SEILSTATIK, Bookmarks |
| AI-PYTHON-PARSE | 1nbSlOQkCQ7Yhro3RxtIXW3QLP5yj9nBc | Parser-Quellen/-Derivate |

## 4. Master-Templates (Ledger 0013–0019, 0026; alle REFERENCE_ONLY/DRAFT)
| ID | Template | Drive-ID |
|:--:|:--|:--|
| 0013 | NEXUS_01_KNOWLEDGE-OBJECT.schema_v0.1.json | 1cEAdd5SMOSsilPyhTDMyBA5TLZSW42cL |
| 0014 | NEXUS_02_ONTOLOGY-SIGNALS-RELATIONS_v0.1.yaml | 1SUjIs0DcjuKgppl7bQVyX2uulX9pQgFn |
| 0015 | NEXUS_03_SKILLS-AGENTS_v0.1.yaml | 1qIFHpk58-KOycbLyIiCbbArDdCpwLiRx |
| 0016 | NEXUS_04_WORKORDER-GATES_v0.1.yaml | 12m60hMCcZWrA12pWt18t9RzJPUOpjHdE |
| 0017 | NEXUS_05_MCP-SERVER-TOOLS_v0.1.json | 13Bu5Sh1tFhjIry_3Ctz5fE59pESOdJYK |
| 0018 | NEXUS_06_CURATOR-AGENT-INSTALL_v0.1.md | 1iz3FjXrLL4zl0NL_AwRgRGWUfRNvsbUw |
| 0019 | CHAT-CODE-HUMAN_KOLLABORATION_v1.1.md (RACI) | 1tWkgj3HteoFUHQHG8_N6U_n1SWxl9vJC |
| 0026 | NEXUS_07_INGESTION-LAYERS-ANKER-SIGNAL-FAMILIE_v0.1.md | 1OWv9m3nCVQs0cwBwO4BIavZ1eXT5h2NM |

## 5. Weitere Wegweiser (verlinkt, nicht dupliziert)
- `00_WEGWEISER_NORMEN_PARSER_INDEX_REUSE__2026-09-29.md` — Normen/Parser/Masterindex-Suchkette; Kopie im SSOT-Root: 1LcigDxoDAS1v4Mb6EhufOa9i9SaZZDxl
- `20_ORDNERPFADEN_UND_WEGWEISER.md` — 20 priorisierte Ordnerpfade: 1gKxjfq99vzOyL0Lfqf5W83v74jem9DSE
- Offene WorkOrders (Ledger): 0022 REGISTRY-CONSOLIDATION, 0023 SEMANTIC-LINKER, 0027 NEXUS-LINT-VALIDATOR (alle DRAFT, WORK)

## 6. Regeln in Kurzform
- Registry vor Semantik; Locator-Pflicht; Zahlen nur aus Solvern (MUST-32/73/155).
- Move-only im Drive; Nachfolger nennt SUPERSEDES; Historie bleibt (MUST-131/132).
- Reporting-Syntax am Ende jeder Antwort: STATUS/CHANGED/TESTS/SOURCE_STATUS/RISKS_GAPS/NEXT/QA_STATUS/LOG.
- Bei Widerspruch zwischen Wegweiser und Kanon gewinnt der Kanon (MUST-144); dann diese Datei als STALE markieren.


## 7. Aktualisierung aus Dokumentationsauftrag 26.10.2026
Dieser Wegweiser bleibt ein Verzeichnis vorhandener Quellen. Aktuelle AGB v002 (23.10) samt Vorrang-/Benennungsänderung lesen: https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view. _FRONTMATTER ist weiterhin ENTWURF. Ältere Bootstrapverweise sind mit späteren datierten ID01-Adoptionen abzugleichen.
Aktuelles Ledger: https://drive.google.com/file/d/1Uvb89wWOpte3iXWKm3qrg42dEwBb7nuG/view. Alte E4-ID verweist auf historischen Stand und wurde korrigiert; keine alten Ledgerdateien gelöscht.
AIM v0.3.2: https://drive.google.com/file/d/1y7jmHlyxq7Ja2xA2FM6MJapOjIkIMlqZ/view.
Aktuelle Reparaturcheckliste: https://drive.google.com/file/d/1KeHVM_VC9nGHZTVyJd_5vBE6xBCG9KwX/view.
Technikachsenentscheidung: https://drive.google.com/file/d/1prAgbIXHIOac8uJOoPClMFbke9I_DaM-/view; Ledger0059. Handbuch, Anpassungsauftrag, Review und Austauschpaket sind über neue Ledgerzeilen0063ff und den Lieferkatalog dieses Laufs auffindbar.
GitHub-Austauschziel: https://github.com/julianzotter/nexus-platform; Snapshots/PR aus diesem Lauf, keine globale bidirektionale Synchronisierung. Aktuelle Lieferung zusätzlich im WORK-Laufbericht verlinkt. Keine Empfänger-ACKs aus Ablage ableiten.
## Historie v0.2.0
2026-10-26T16:48:23+01:00: OpenAI Codex /root korrigiert Ledgerpointer, verlinkt AGB/AIM/WO/Technikachse und die neue Dokumentationslieferung. Ursprüngliche Bytes werden im historischen Sicherungspaket erhalten.

## Konkrete Lieferverweise dieses Laufs
- NEXUS-BETRIEBSHANDBUCH v0.2.0: https://drive.google.com/file/d/1Xo4gL6N_OWcnnde70baStp0ATNVwu5Wo/view?usp=drivesdk
- WO-PERPLEXITY-AIM-ANPASSUNG v1.0.0: https://drive.google.com/file/d/1tSxNz_htFwI9UC6fAmqmVajaLzvBAwkF/view?usp=drivesdk
- REVIEW-CHAT-KONSOLIDIERUNG v1.0.0: https://drive.google.com/file/d/1J0x-AiudvMZJ5OhJlFsfNACRgK-Bp_K0/view?usp=drivesdk
- STATUS-NEXUS-UMSETZUNG v1.0.0: https://drive.google.com/file/d/1XVnG4FevBpQGX2GEDPqeBwrLc41wrweZ/view?usp=drivesdk
- WO-NEXUS-REPAIR-SPEEDTEAM v1.0.2: https://drive.google.com/file/d/1KeHVM_VC9nGHZTVyJd_5vBE6xBCG9KwX/view?usp=drivesdk
- MUSTER-MARKDOWN-HISTORY v0.1.0: https://drive.google.com/file/d/1uD9baHyHk5_ad9V3KYFOUepZ-ZSAczjW/view?usp=drivesdk
- LIEFERKATALOG-NEXUS-DOKUMENTATION v1.0.0: https://drive.google.com/file/d/1_CmvceBYi0b2DtHhMGa7cLDNSkcpo27E/view?usp=drivesdk
- RUNLOG-NEXUS-DOKUMENTATION v1.0.0: https://drive.google.com/file/d/1hpNsnLiqx2I7PqbZf_6lw6jvA1JEjdwQ/view?usp=drivesdk
- WEGWEISER-NEXUS-ENTRY-POINTS v0.2.0: https://drive.google.com/file/d/1u1lqlQ0zn2HcauvEPc63mk8Kvu3sNC74/view?usp=drivesdk
- Vorstandsarchiv: https://drive.google.com/file/d/1Rs_vnD1dt_lxtRs7Jkep5lGF0lTv93WV/view?usp=drivesdk
- GitHub-Snapshotbranch: https://github.com/julianzotter/nexus-platform/tree/docs/nexus-manual-audit-20261026-164823
