---
name: PLAN_REPORT-LEDGER-RENUMMERIERUNG
version: 0.1.0
status: ENTWURF
timestamp: 2026-11-25T15:10:00+01:00
agent_id: ID06
executor: Claude (claude.ai cloud session, gh REST)
scope: Planung, keine Umbenennung ausgefuehrt
---

# Plan: Umbenennung LEDGER-PENDING / UNREGISTERED / ID-UNVERIFIED

## TL;DR
- Regel: `YY_MM_DD_HHMM_ID##_THEMA_###` (governance/current/_AGBS.md Z. 58; AGENTS.md Punkt 4).
- Artefaktnummer `###` **nur aus dem ID-Ledger**, nie aus Dateinamen ableiten (_AGBS.md Z. 58, AGENTS.md Punkt 4).
- Befund: Im Repo existiert **kein** maschinenlesbarer ID-Ledger (gesucht: `registry/`, `governance/`). Ohne Ledger keine Nummernvergabe moeglich -> **Blocker B1**.
- Bestand (Stand HEAD 169d247, `python tools/naming_gate.py --all --plan`): Tabelle unten. Gesamtinventar: 153 Kandidaten, 101 nicht konform (Altbestand, nicht CI-gesperrt).
- CI-Gate wirkt nur auf **neu hinzugefuegte/umbenannte** Dateien eines PR; Altbestand bleibt bis zur Umbenennung sichtbar, aber nicht blockierend.

## Schritte
1. **B1 Ledger anlegen (ID01-Entscheid):** `registry/report-ledger.jsonl` (eine Zeile je Artefakt: `nr`, `id`, `thema`, `path`, `sha256`, `registered_at`). Eigentuemer: ID03 (Chief Orchestrator), Freigabe ID01.
2. **Rollen-ID belegen** fuer `ID-UNVERIFIED`: Quelle = Frontmatter `agent_id`, sonst PR-Branch/Commit. Hinweise unten sind **unbelegt** und brauchen ID01-Bestaetigung.
3. **Nummern ziehen:** je Datei eine Ledger-Zeile, Nummer aus Ledger-Zaehler.
4. **Umbenennen per `git mv`** in einem PR; Verweise (`grep -rl <altname>`) im selben PR nachziehen; Drive-Spiegel ueber Sync.
5. **Gate verschaerfen:** danach `naming_gate.py --strict` im CI (LEDGER-PENDING zaehlt dann als Verstoss).

## Hinweise zur Rollen-ID (unbelegt, aus Merge-Branch)
| Datei (Kurz) | Branch / PR | Kandidat |
|---|---|---|
| USECASES/.../26_11_25_0246_ID-UNVERIFIED_P205_FT-* (2) | perplexity/26-11-25-p205-bestandsanalyse, PR #133 | ID05 (Perplexity) |
| reports/26_11_25_0010_ID-UNVERIFIED_PROTOKOLL_CHAT-ARCHGATE-P205 | perplexity/26-11-25-protokoll-archgate-p205, PR #131 | ID05 |
| reports/26_11_23_0845_ID-UNVERIFIED_ROADMAP_DROPZONE-AI-STACK | claude/report-dropzone-ai-stack-roadmap, PR #108 | ID06 (Claude) |
| docs/operations/review/2026-10-27/*ID-UNVERIFIED* (6) | review/nexus-manual-status-20261027-1517, PR #44 | offen |
| docs/dossiers/.../26_10_26_18_40_ID-UNVERIFIED_* | docs/current-state-governance-20261025, PR #40 | offen (zusaetzlich HH_MM) |
| docs/integration-review/26_10_19_16_42_ID-UNVERIFIED_* | codex/repo-integration-20261019, PR #34 | ID06 lt. Matrix-Regel "OpenAI Codex" (offen) |

## Bestand (generiert)
Treffer: 55

| # | Datei | Urteil | Erforderlich |
|---|---|---|---|
| 1 | `USECASES/P205_EISTEICHE/FT_TRAEGER_MATRIX/26_11_25_0246_ID-UNVERIFIED_P205_FT-BESTANDSANALYSE_LEDGER-PENDING.md` | Verstoss | Rollen-ID aus Frontmatter/Commit belegen (ID01); Artefaktnummer ### aus ID-Ledger |
| 2 | `USECASES/P205_EISTEICHE/FT_TRAEGER_MATRIX/26_11_25_0246_ID-UNVERIFIED_P205_FT-REF-REKONSTRUKTION_LEDGER-PENDING.md` | Verstoss | Rollen-ID aus Frontmatter/Commit belegen (ID01); Artefaktnummer ### aus ID-Ledger |
| 3 | `WORK/26_11_23_2045_ID05_PROTOKOLL_CHAT-BASELINE-EVAL_UNREGISTERED.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 4 | `WORK/26_11_24_2344_ID05_WO-SYSTEM-EVAL-OPTIMIERUNG_UNREGISTERED.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 5 | `WORK/P205_FT/2026-11-23_ID02/26_11_23_1104_ID02_P205_FT-MOE-ROUTER_v1.0_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 6 | `WORK/P205_FT/2026-11-23_ID02/26_11_23_1104_ID02_P205_FT-PEER-REVIEW_v1.2_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 7 | `WORK/P205_FT/2026-11-23_ID02/26_11_23_1104_ID02_P205_FT-TRUE-RUN-WORKFLOW_v1.0_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 8 | `WORK/P205_FT/2026-11-23_ID02/26_11_23_1320_ID02_P205_FT-MULTIAGENT-WORKORDERS_v1.0_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 9 | `WORK/P205_FT/2026-11-23_ID02/26_11_23_1410_ID02_P205_FT-POWERSHELL-E2E-HANDOFF_v1.1_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 10 | `WORK/REPORTS/26_11_11_1200_ID02_PEER-REVIEW_CONTROL-TOWER_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 11 | `WORK/REPORTS/26_11_11_1316_ID02_STATUSREPORT_ID02-PRIVATE-ROLLOUT_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 12 | `WORK/REPORTS/26_11_11_1333_ID02_SCHEDULER-EVIDENCE_LEDGER-PENDING.json` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 13 | `WORK/REPORTS/26_11_11_1334_ID02_SCHEDULER-IMPLEMENTIERUNG_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 14 | `WORK/REPORTS/26_11_17_1928_ID06_REINSCHRIFT_RFEM-CAD-PYTHON-PIPELINE_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 15 | `WORK/REPORTS/26_11_19_1444_ID02_STATUS-NEXUS-HANDBUCH-UND-SYNC_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 16 | `WORK/REPORTS/26_11_20_0901_ID02_NEXUS-KNOWLEDGE-IMPLEMENTIERUNGSPLAN_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 17 | `WORK/REPORTS/26_11_23_0830_ID02_AT-STRUCTURAL-STANDARDS-WATCH-BGLD-OIB-RL6_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 18 | `WORK/REPORTS/26_11_23_1410_ID02_NEXUS-P205-PANEL-REPAIR_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 19 | `WORK/REPORTS/26_11_24_2118_ID06_REVIEW_ID02-WO122-UEBERGABE_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 20 | `WORK/REPORTS/26_11_24_ID03_NEXUS-3PASS-SYSTEMCHECK-ROLE-MATRIX_LEDGER-PENDING.md` | Verstoss | Rollen-ID aus Frontmatter/Commit belegen (ID01); Artefaktnummer ### aus ID-Ledger |
| 21 | `backups/work/26_11_24_1108_NEXUS_GRILL_WORKORDER_DESIGN_UNREGISTERED.md` | Verstoss | Rollen-ID aus Frontmatter/Commit belegen (ID01); Artefaktnummer ### aus ID-Ledger |
| 22 | `backups/work/26_11_24_1108_NEXUS_GRILL_WORKORDER_IMPLEMENT_UNREGISTERED.md` | Verstoss | Rollen-ID aus Frontmatter/Commit belegen (ID01); Artefaktnummer ### aus ID-Ledger |
| 23 | `backups/work/26_11_24_1108_NEXUS_GRILL_WORKORDER_REVIEW_UNREGISTERED.md` | Verstoss | Rollen-ID aus Frontmatter/Commit belegen (ID01); Artefaktnummer ### aus ID-Ledger |
| 24 | `backups/work/26_11_24_1108_NEXUS_GRILL_WORKORDER_SYNC_UNREGISTERED.md` | Verstoss | Rollen-ID aus Frontmatter/Commit belegen (ID01); Artefaktnummer ### aus ID-Ledger |
| 25 | `docs/dossiers/2026-10-26-system-design-signalmatrix-v1.0.0/26_10_26_18_40_ID-UNVERIFIED_DOSSIER-LIEFERLOG_v1.0.0.md` | Verstoss | Rollen-ID aus Frontmatter/Commit belegen (ID01); HH_MM -> HHMM |
| 26 | `docs/handbooks/26_11_19_1445_ID02_DEEPSEEK-HARNESS-NEXUS-AI-BENUTZERHANDBUCH-IMPLEMENTIERUNGSGUIDE_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 27 | `docs/handbooks/26_11_19_1445_ID02_DEEPSEEK-HARNESS-NEXUS-AI-BESTANDSANALYSE_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 28 | `docs/implementation-plans/26_11_20_0903_ID02_NEXUS-KNOWLEDGE-SYSTEM_IMPLEMENTIERUNGSPLAN_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 29 | `docs/implementation-plans/evidence/2026-11-20/26_11_20_0905_ID02_NEXUS-KNOWLEDGE-PLAN_RUNLOG_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 30 | `docs/implementation-plans/evidence/2026-11-20/26_11_20_0905_ID02_NEXUS-KNOWLEDGE-PLAN_STATUS-REGISTRATION_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 31 | `docs/integration-review/26_10_19_16_42_ID-UNVERIFIED_REPO-INTEGRATION_v1.0.0.md` | Verstoss | Rollen-ID aus Frontmatter/Commit belegen (ID01); HH_MM -> HHMM |
| 32 | `docs/operations/2026-11-10/26_11_10_1601_ROLE-UNVERIFIED_CLAUDE-INTERCONNECTIVITY_DECISIONS_UNREGISTERED.md` | Verstoss | Rollen-ID aus Frontmatter/Commit belegen (ID01); Artefaktnummer ### aus ID-Ledger |
| 33 | `docs/operations/review/2026-10-27/26_10_27_1517_ID-UNVERIFIED_NEXUS-EVIDENCE-MANIFEST_UNREGISTERED.json` | Verstoss | Rollen-ID aus Frontmatter/Commit belegen (ID01); Artefaktnummer ### aus ID-Ledger |
| 34 | `docs/operations/review/2026-10-27/26_10_27_1517_ID-UNVERIFIED_NEXUS-PEER-REVIEW-WORKORDER_UNREGISTERED.md` | Verstoss | Rollen-ID aus Frontmatter/Commit belegen (ID01); Artefaktnummer ### aus ID-Ledger |
| 35 | `docs/operations/review/2026-10-27/26_10_27_1517_ID-UNVERIFIED_NEXUS-SYSTEMSTATUS-EVALUATION_UNREGISTERED.md` | Verstoss | Rollen-ID aus Frontmatter/Commit belegen (ID01); Artefaktnummer ### aus ID-Ledger |
| 36 | `docs/operations/review/2026-10-27/26_10_27_1517_ID-UNVERIFIED_NEXUS-USERMANUAL-IMPLEMENTATIONGUIDE_UNREGISTERED.md` | Verstoss | Rollen-ID aus Frontmatter/Commit belegen (ID01); Artefaktnummer ### aus ID-Ledger |
| 37 | `docs/operations/review/2026-10-27/26_10_27_1517_ID-UNVERIFIED_NEXUS-USERMANUAL-IMPLEMENTATIONGUIDE_UNREGISTERED.pdf` | Verstoss | Rollen-ID aus Frontmatter/Commit belegen (ID01); Artefaktnummer ### aus ID-Ledger |
| 38 | `docs/operations/review/2026-10-27/26_10_27_1544_ID-UNVERIFIED_NEXUS-DELIVERY-RUNLOG_UNREGISTERED.md` | Verstoss | Rollen-ID aus Frontmatter/Commit belegen (ID01); Artefaktnummer ### aus ID-Ledger |
| 39 | `docs/reports/2026-11-16_admin-debug/26_11_16_2308_ID02_NEXUS-ADMIN-DEBUG_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 40 | `docs/reports/2026-11-16_admin-debug/26_11_16_2335_ID02_OAUTH-REGISTRY-REPAIR_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 41 | `governance/roles-v1.1/26_11_11_1316_ID02_WORKORDER_ID02-PRIVATE-ROLLOUT_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 42 | `knowledge/W100_CIRCULAR_HOUSING/26_11_12_1931_ID02_W100-CHAT-ERGEBNISSE_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 43 | `reports/26_11_10_1601_ID06_STATUSMATRIX_SKILLS-SYNC_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 44 | `reports/26_11_23_0845_ID-UNVERIFIED_ROADMAP_DROPZONE-AI-STACK_LEDGER-PENDING.md` | Verstoss | Rollen-ID aus Frontmatter/Commit belegen (ID01); Artefaktnummer ### aus ID-Ledger |
| 45 | `reports/26_11_24_1111_NEXUS_GRILL_PHASE2_TEST_REPORT_UNREGISTERED.md` | Verstoss | Rollen-ID aus Frontmatter/Commit belegen (ID01); Artefaktnummer ### aus ID-Ledger |
| 46 | `reports/26_11_25_0010_ID-UNVERIFIED_PROTOKOLL_CHAT-ARCHGATE-P205_LEDGER-PENDING.md` | Verstoss | Rollen-ID aus Frontmatter/Commit belegen (ID01); Artefaktnummer ### aus ID-Ledger |
| 47 | `reports/claude-ergo/26_11_10_1601_ID06_CHAT-EXPORT-d96056dc_UNREGISTERED.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 48 | `reports/claude-ergo/26_11_10_1602_ID06_WO-0-REUSE-CHECK+PROFILE-DRAFT_UNREGISTERED.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 49 | `reports/system-evaluation/26_11_24_2351_ID05_WORKORDER_SYSTEMEVAL_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 50 | `reports/system-evaluation/26_11_24_2354_ID05_HISTORY_SYSTEMEVAL_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 51 | `reports/system-evaluation/26_11_24_2354_ID05_STATUS_SYSTEMEVAL_FEEDBACK_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 52 | `reports/system-evaluation/26_11_25_0001_ID05_WORKORDER_SYSTEMEVAL_ARCHITEKTUR_NACHTRAG_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 53 | `reports/system-evaluation/26_11_25_0015_ID05_STATUS_WORKORDER_SYNC_DATENPUNKT_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 54 | `usecases/P205-EISTEICHE-BT-WEST/26_11_23_1810_ID06_STATUS-QUICKTASK-MATRIX+REFLIST+ROADMAP_P205-FT-CAD_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
| 55 | `usecases/P205-EISTEICHE-BT-WEST/26_11_23_1820_ID06_ARBEITSPLAN_P205-FT-CAD-INTEGRATION_LEDGER-PENDING.md` | Nummer offen | Artefaktnummer ### aus ID-Ledger |
