---
workflow_id: NEXUS-TRUE-RUN-P205-FT
version: "1.0"
created_vienna: 2026-11-23T11:04:26+01:00
author_role: ID02
registration_status: REGISTRATION_PENDING
technical_release: false
---
# NEXUS True-Run Workflow · P205 FT-Träger

## 1. Grundvertrag

- Vor jedem Run: aktuelle `_AGBS.md`, freigegebene Baseline, Manifest, Ticket- und Rollenregister lesen. Fehlt eine Pflichtquelle: `BOOTSTRAP_BLOCKED`.
- LLMs analysieren, routen und prüfen Evidenz. Nachweisrelevante Berechnungen stammen ausschließlich aus Excel Desktop, RFEM oder einem validierten deterministischen Solver.
- Keine persistierte private Chain-of-Thought. Auditfähiger Ersatz: `Source Record → Evidence Record → Decision Record → Calculation Record → QA Record → Human Approval Record`.
- Jeder Agent schreibt nur in seinen Run-/ID-Outbox-Pfad. Gemeinsame SQLite-DB und kanonische Berichte haben genau einen Writer.
- Keine Überschreibung: neues Artefakt, Hash und Vorgängerreferenz.

## 2. Benennung und Isolation

`YY_MM_DD_HHMMSS_IDxx_P205_FT_<Semantischer-Titel>_RUN-Rxx_vNNN.ext`

`WORK/P205_FT/RUNS/<run_id>/<agent_id>/`

Pflichtfelder: `run_id`, `agent_id`, `created_utc`, `created_vienna`, `status`, `source_ids`, `source_sha256`, `parent_run_id`, `evidence_class`, `technical_release=false`.

## 3. Tokenbudget

`C` ist das tatsächlich gemeldete Kontextlimit; unbekannt bleibt `null`.

| Anteil | Zweck |
|---:|---|
| 8 % | System-, Rollen- und Sicherheitsregeln |
| 12 % | Governance, Manifest, Run-Contract |
| 50 % | gehashte Primärquellen/Evidence Pack |
| 15 % | strukturierter Output |
| 15 % | Reserve für Fehler, Metadaten und Retry |

- Quellen > `0,50 × C` werden nach Domäne/Blattgruppe geteilt, niemals still gekürzt.
- Jeder Teil-Run ist mit vollständigem Input-Contract ohne Chat-Historie reproduzierbar.
- Nach zwei fehlgeschlagenen Runs: `ESCALATE_ID02`; keine automatische Scope-Ausweitung.
- Nicht exponierte Token-/Kostenwerte bleiben `null`, `telemetry_status=NOT_EXPOSED`.

## 4. Input-/Output-Contract

```yaml
objective: atomic and testable
scope_in: []
scope_out: []
governance_sources: []
technical_sources:
  - source_id: null
    version: null
    sha256: null
    locator: null
required_tools: []
calculation_authority: NONE|EXCEL|RFEM|PYTHON
acceptance_tests: []
stop_conditions: []
token_budget:
  context_limit: null
  source_max: null
  output_max: null
```

Pflichtausgaben: `run_manifest.json`, `evidence_records.ndjson`, `findings.ndjson`, `decision_records.ndjson`, `blockers.ndjson`, `artifact_manifest.json`, `qa_report.md`; bei Rechenläufen zusätzlich `calculation_record.json`, Maschinenlog und Testergebnis.

## 5. True-Run-Kette

| Run | Inhalt | Owner | Gate |
|---|---|---|---|
| R00 | Governance-/Baseline-/Rollen-Bootstrap | ID02 | G0 |
| R01 | Quellen, Versionen, Hashes, Dubletten | ID04 | G1 |
| R02 | Workbook, Formeln, Cache, Links, Excel-E2E | ID06 → ID07 | G2 |
| R03 | Geometrie-/Bauteil-/Planreferenzen | ID04 → ID03 | G1 |
| R04 | Designschnittkräfte und RFEM-Zuordnung | ID04 → ID03 | G2 |
| R05 | Widerstände, Normparameter, Nachweislogik | Solver → ID03 | G2 |
| R06 | alle Auslastungen >105 % unabhängig prüfen | ID03 → ID07 | G3 |
| R07 | Zeichnungs-/Ausschreibungsrestpunkte | ID02 → ID03 | G3 |
| R08 | MoE-Synthese und Konfliktbericht | ID02 | G3 |
| R09 | unabhängiger Reproduzierbarkeitslauf | ID07 | G3 |
| R10 | technische Entscheidung/Freigabe | ID01 | G4 |
| R11 | Registry, Ledger, GitHub/Drive, Readback | ID02 → ID03 | G5 |

G0 Pflichtquellen aktuell; G1 Quelle/Version/Locator/Hash; G2 deterministischer, reproduzierbarer Rechenlauf; G3 unabhängiger Review; G4 explizites ID01-Approval; G5 Upload-/Commit-ID, Hash und Readback stimmen.

## 6. Parallelbetrieb

- Reviewer erhalten dasselbe unveränderliche Evidence Pack und sehen die anderen Ergebnisse erst nach eigener Abgabe.
- Agenten schreiben NDJSON-Outboxen; ein Ledger-Writer validiert Schema, Hash und Dubletten und importiert transaktional.
- ID01 ist alleinige technische Freigabeinstanz; ID02 orchestriert; ID03–ID08 nur gemäß Rollenregister.
- Kimi, Qwen, Gemma, Meta AI und andere unregistrierte Modelle: `UNASSIGNED` bis Rollenregister und Ticket vorliegen.

## 7. Power-Panel-Ereignis

```json
{
  "run_id": "P205-FT-R02-YYYYMMDDThhmmssZ",
  "agent_id": "ID06",
  "seq": 1,
  "timestamp_utc": "YYYY-MM-DDThh:mm:ssZ",
  "state": "ACTIVE_ACK",
  "folder": "WORK/P205_FT/RUNS/.../ID06",
  "written_artifacts": [],
  "blocker": null,
  "next_action": "Excel Desktop E2E",
  "emitter": "AGENT_ACK"
}
```

Ein Chat-LLM kann keine garantierten 10-/30-Sekunden-Herzschläge liefern. Der lokale Watchdog darf Prozessliveness melden, aber niemals fachlichen Fortschritt simulieren.
