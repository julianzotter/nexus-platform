---
name: DECISION-RECORD_WO-GOV-ACB-ENG-ID01-ENTSCHEIDE
type: DECISION-RECORD
version: 0.1.0
status: ENTWURF_REVIEW_SNAPSHOT
timestamp: '2026-10-27T18:25:00+01:00'
agent_id: ID06
artifact_id: '0129'
decided_by: ID01
decision_time: '2026-10-27T18:14+01:00'
refers_to: '0127 (Statusbericht), 0128 (Ledger-Append-Request)'
naming_schema: YY_MM_DD_<ID>_<TYPE>_<TITLE>_vX.Y.Z.md
hash_scope: body_utf8_after_closing_frontmatter_lf
---
# ID01-Entscheide (18:14) und Umsetzung
| # | Entscheid ID01 | Umsetzung ID06 | Status |
|---|---|---|---|
| 1 | K5: **WO-Schema** `YY_MM_DD_<ID>_<TYPE>_<TITLE>_vX.Y.Z.md` | ACB v0.2 erzeugt Namen so; `naming_rule` in agent_contracts.json; diese Datei erster Anwendungsfall | DONE (Snapshot) |
| 2 | ACB-Drive-Ort: **bestehender COMMUNICATION-Ordner** | gewählt: LLM-LOCAL-SSOT/nexus-llm-orchestrator/COMMUNICATION (10PrCkTgmAfoLkK1JXE-d1C1u9kXiQKjy); Subfolder angelegt: ID02_TO_ID03 1kaPKGr…, ID03_TO_ID02 1fHwYSB…, PROCESSED 12gpJR0…, FAILED 1nhzfGN… | DONE |
| 3 | **Ledger-ID je ACB-Nachricht** | `--artifact-id` (4-stellig) Pflicht; im Frontmatter + Dateiname (`…_ACB-MSG_<THEMA>-<ID>_v0.1.0.md`); 6/6 Tests PASS | DONE |
| 4 | **Solver-Import freigegeben** | Bestandsinventur Drive (Reuse vor Neubau) – siehe `wo03_solver_import` in agent_contracts.json; Import = eigene Runs (1 Solver/Run, Token-Regel) | GEPLANT |

# Annahmen (unklar → so entschieden)
- `<ID>` im WO-Schema = Rollen-ID `ID##` (konsistent mit ID01-Anordnung 27.10. „Rollen-ID nach Timestamp“); Ledger-Nr. im Frontmatter `artifact_id`. Falls `<ID>` = Ledger-Nr. gemeint: 1 Zeile in `build_message` ändern.
- Von den 3 COMMUNICATION-Ordnern (13.10.) wurde der unter LLM-LOCAL-SSOT gewählt (Dokument-SSoT, K4); die zwei anderen (unter `orchestrator` 1kv3HU7…, `nexus-llm-orchestrator` 1cHgJ7W…) bleiben unberührt → Duplikat-Hinweis P7.
- Ledger-IDs 0129 (dieser Record) und 0130–0134/0140 (nur Test-Fixtures, tmp, nicht persistiert) – reale Vergabe erfolgt durch ID03 beim Append.

# Offene Pflichtfolgen
- ID03: `_AGBS_v003.md` Snapshot + `_AGBS.md` v004 mit WO-Schema (AGBS-Änderungsregel); Ledger-Append 0127–0129.
- ID02/ID03: echter ACB-Roundtrip mit eigener Runtime (E2E-Nachweis).
- ID06: Solver-Import Run 1 = `boeb_seilnetz_v0.1.1.zip` oder `ref_hbv_gamma_EC5-AnhB_independent.py` (ID01 wählt Reihenfolge, sonst: Seilnetz zuerst – Haftung/Frist P205/26_001).

# REPORTING
STATUS: Entscheide 1–3 umgesetzt (Review-Snapshot); 4 geplant
CHANGED: tools/nexus_acb.py (v0.2.0), tests/test_nexus_acb.py (+1), development_cycle/agent_contracts.json, Drive 4 Subfolder, dieser Record
TESTS: pytest 6/6 PASS
SOURCE_STATUS: ID01-Chat 18:14; Drive-Metadaten der 3 COMMUNICATION-Ordner geprüft
RISKS_GAPS: AGBS v003 formal noch gültig bis v004; `<ID>`-Interpretation; keine echten Agent-Runtimes
NEXT: Ledger-Append (ID03) → AGBS v004 (ID03) → Solver-Import Run 1 (ID06)
