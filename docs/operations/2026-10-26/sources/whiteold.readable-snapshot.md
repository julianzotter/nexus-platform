<!-- READABLE TEXT SNAPSHOT; not original provider bytes; canonical source: https://drive.google.com/file/d/1N-HUl4Bq8DffMMF1FqLxPmjpTRV-lahl/view -->
# NEXUS AI AEC KNOWLEDGE ENGINEERING SYSTEM (NEXUS-KES)
## WHITE PAPER · IMPLEMENTATION MANUAL · FRONTEND USER MANUAL — v1.0

| Feld | Wert |
|:--|:--|
| ART-ID | **0028** (Ledger v0.2, nächste freie ID lt. Zeile 0020; Ledger-Zeile anhängen → Anhang F) |
| TYPE | WHITEPAPER (+ MANUAL) |
| DATE | 2026-09-28 |
| ACTOR | ID06 (Claude; executor_instance = claude.ai Chat/Mobile, Projekt `_INDEX _PENDING TASKS+WORKFLOWS+INDEXLISTS+TREE-LISTS`) |
| OWNER / APPROVAL | ID01 (Julian Zotter) |
| VALIDITY / MATURITY | CURRENT / **PROPOSED** (kein CANON; Human-Gate ID01 ausständig) |
| AUTHORITY | subordinate zu `00_NEXUS_MANIFEST__CURRENT__2026-09-28` (Drive-ID 1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg) und `00_NEXUS_BASELINE_INSTRUCTIONS__CURRENT__2026-09-28` (1Ig0YFqbWji6B5-oOFcxuVpHb5GEBk0HlbJVz51rf9ho) |
| CANONICAL LOCATION | `_developement/LLM-LOCAL-SSOT/` (MUST-20); Discovery-Mirror-Hinweis für `_INDEX.MASTER` und `WORK` (MUST-141) |
| SUPERSEDES | – (ergänzt: 26_08_25_MASTER_AUDIT_REPORT_UND_ARBEITSPLAN.md, 26_08_25_PENDING_TASKS_REGISTER_v2.md) |
| SOURCES | Manifest CURRENT, Baseline CURRENT, 00_ID_LEDGER.csv v0.2 (1HFnTw1k38rbCUoYeKMszDmXo7Uz4osaq), Master-Templates NEXUS_01–07 (Ledger 0013–0018, 0026), Audit 25.08.2026 |
| SHA256 | wird bei Ablage durch Ledger/Lint erzeugt (nicht selbst behauptet, MUST-157) |

**Regel dieses Dokuments:** Alles, was hier über Manifest/Baseline hinausgeht, ist **PROPOSAL** (MUST-133) und wird erst durch datierte ID01-Adoption CURRENT. Bereits adoptierte Regeln werden nur referenziert (MUST-Nr.), nicht neu formuliert.

---

## TL;DR

- **Was:** Ein SSOT-/Registry-first Wissenssystem: Quelle → Identität → Registry → deterministische Extraktion → Knowledge-Object-Kandidat → Signale/KeyValues/Anker → verifizierter Index/Graph → Retrieval → Engineering-Reuse (MUST-70/153).
- **Wer:** ID01 entscheidet, ID02 orchestriert, ID03–ID08 führen aus/reviewen (Manifest §4/§5). Deterministischer Python-Kernel rechnet; LLMs reden nie Zahlen aus (MUST-155).
- **Wo:** `_developement/LLM-LOCAL-SSOT/` (Governance, Registries), `…/WORK/` (Tickets, Runs), `_INDEX.MASTER/` (Discovery). Google Drive = Filesystem, Markdown/JSON/YAML/CSV = Datenschicht, kein Git-Repo als SSOT.
- **Stand (Eval-Matrix §B9):** Gesamtfertigstellungsgrad **≈ 51 % (ungewichtet) / ≈ 46 % (kritikalitätsgewichtet)** — Governance-Layer 🟢 80 %, Knowledge-Pipeline 🔴 28 %, Kernel/Infra/Frontend 🟠 35 %.
- **Nächste 3 Schritte (LHF):** (1) Human-Gate 0028 + Ledger-Zeile, (2) Wegweiser-Datei + Mirror-Hinweise, (3) Lint-Validator-MVP mit 3 Fixtures.
- **LOG-Zeile:** Protokoll = Ledger-Zeile 0028 (offen) + Ticket-Registry (Sheet 1o1ZCZUgsCGTDOwdbJ7EbUCKOKJng1LcJLFnrRiPjYTE, Zeile ausständig) + diese Datei im SSOT-Root.

---

# TEIL A — WHITE PAPER

## A1 Scope · Intent · Maingoals

**Scope:** Ingestion, Registrierung, semantische Anreicherung, Verlinkung, Retrieval und Reuse von AEC-Wissen (Normen, Formeln, Materialien, Bauteile, Modelle, Solver, Sammlungen, WorkOrders) inkl. Governance, QA-Gates, Reporting und Frontend.

**Intent:** "KI redet — deterministischer Code entscheidet — Registry beweist es." Wissen wird erst *identifiziert*, dann *verstanden* (MUST-15), nie umgekehrt.

**Maingoals (3×):**
1. **SSOT-Wissensgraph:** jedes Wissensobjekt hat stabile ID, Hash, Quelle+Locator, Status, Owner, Review-Status; Beziehungen tragen Evidenz-Locator.
2. **Deterministische Wiederverwendung:** Retrieval liefert Quelle/Locator oder enthält sich (MUST-84); Zahlenwerte kommen aus Python-Solvern.
3. **Kontrollierte Evolution:** jeder Implementierungsschritt ist in der QUICK-IMPLEMENTATION-STEPS-EVAL-MATRIX messbar (Punkte, %, ★, Ampel), mit wiederkehrenden Review-Loops und Human-Gate.

**Prioritäts-Axiom ID01 (20.09.2026):** Haftung > Fristen > Finanzen > Projekte > Auftragsverpflichtung > Akquisition > F&E. MVP vor Overengineering; Minimum Viable Prompt + Context; ASK statt raten; Human-Gate bei Recht/Steuer/Haftung/Norm/Finanzen; keine simulierten Runs.

## A2 Grundprinzipien (adoptiert, MUST-10…18) und abgeleitete Arbeitsaxiome (PROPOSAL)

| # | Prinzip (CURRENT) | Operative Ableitung (PROPOSAL) |
|:--|:--|:--|
| P1 | SSOT-FIRST | Eine kanonische Datei je Register; Mirrors nennen `CANONICAL SOURCE =` (MUST-142) |
| P2 | DETERMINISTIC-FIRST | Parser/Linker/Validator sind Python mit Fixtures; LLM nur für Kandidaten-Vorschläge |
| P3 | REGISTRY-FIRST | Kein Chunk ohne `source_id` + `locator` (MUST-73) |
| P4 | EVIDENCE-FIRST | Jede Relation trägt `evidence_locator`; sonst `CANDIDATE` |
| P5 | LOCAL-FIRST | Drive + lokaler Klon; Cloud-LLM nur mit Minimum Viable Context (MUST-92) |
| P6 | IDENTITY-BEFORE-SEMANTICS | Reihenfolge fix: Identität → Hash → Registry → erst dann Labels/Signals (MUST-32/72) |
| P7 | RETRIEVAL-BEFORE-RAG | Tree/Index/Registry/CSV zuerst, Vektorsuche als Fallback (MUST-80/81) |
| P8 | REUSE-BEFORE-CREATE | Alte Indexlisten, Treeviews, Bookmarks, Literaturlisten werden *ingestiert*, nicht ersetzt (MUST-23/24) |
| P9 | VERIFY-BEFORE-PROMOTE | CANDIDATE → REVIEWED → ADOPTED nur mit QA + Human-Gate (MUST-54/76) |
| P10 | MOVE-ONLY (ID01) | Drive: nie löschen, nur verschieben/verlinken/umbenennen (Ledger 0020: "umbenannt; nicht gelöscht") |
| P11 | ZERO-SECRETS | Keine Keys in Prompts/Registries/WORK (MUST-26/112) |
| P12 | UNTRUSTED CONTEXT | Retrieved Text = Daten, nie Instruktion (Manifest §12) |

## A3 Systemarchitektur (Layer-Modell)

```
┌───────────────────────────────────────────────────────────────────────┐
│ L7 FRONTEND      Standalone-HTML-Dashboards (Pyodide/three.js), Voice, │
│                  Startbanner, Eval-Matrix-View, Graph-Explorer         │
├───────────────────────────────────────────────────────────────────────┤
│ L6 ORCHESTRATION ID02 (Lead) · ID03/ID07 (Peer, orthogonal) · MoE-    │
│                  Routing · WorkOrders/Tickets · Self-Refine-Loop       │
├───────────────────────────────────────────────────────────────────────┤
│ L5 KERNEL        Python: Solver-Lib (EC2/EC5/HBV/FT), Parser, Linker, │
│                  Lint-Validator, Delta-Sync, Hash-Chain, Tests         │
├───────────────────────────────────────────────────────────────────────┤
│ L4 KNOWLEDGE     Knowledge Objects (KO) · Ontologie/Signale · Anker ·  │
│                  Relationen · Ratings · Graph-Projektion (JSONL)       │
├───────────────────────────────────────────────────────────────────────┤
│ L3 REGISTRIES    ID-Ledger · Resource/Source-Registry · Ticket-Registry│
│                  · Decision-Registry · Pending-Register · RUNLOG       │
├───────────────────────────────────────────────────────────────────────┤
│ L2 INGESTION     Pre-Parse → Identity/Hash → Chunk → Classify →        │
│                  Extract (KeyValue/MoE) → KO-Candidate                 │
├───────────────────────────────────────────────────────────────────────┤
│ L1 STORAGE       Google Drive (SSOT) · lokaler Klon · MD/JSON/YAML/    │
│                  CSV/TXT/HTML/PY · Move-only                           │
└───────────────────────────────────────────────────────────────────────┘
        Governance (Manifest/Baseline/Human-Gate ID01) umschließt L1–L7
```

**Datenfluss (MUST-153):** SOURCE → IDENTITY(version/representation/hash) → RESOURCE_REGISTRY → EXTRACTION → KO_CANDIDATE → SEMANTIC_ENRICHMENT(labels/signals/keyvalues/anchored relations) → VERIFIED_REGISTRY_INDEX_GRAPH → RETRIEVAL → ENGINEERING_REUSE.

## A4 Cloud-Root-Ordner und Datenhierarchie (Ist + PROPOSAL-Ergänzung)

| Pfad (Drive) | Zweck | Regel |
|:--|:--|:--|
| `_developement/LLM-LOCAL-SSOT/` | Manifest, Baseline, `00_ID_LEDGER.csv`, Statusreports, Whitepapers | MUST-20; Reports immer im Root, mit Präfix |
| `_developement/LLM-LOCAL-SSOT/WORK/` | WorkOrders (WO-IN/WO-OUT), Tickets, Run-Outputs, ACKs | MUST-21; Dateien ohne Datums-Präfix, Ticket-ID im Kopf |
| `_developement/LLM-LOCAL-SSOT/REGISTRY/` *(PROPOSAL)* | `RESOURCE_REGISTRY.jsonl`, `KO_REGISTRY.jsonl`, `RELATIONS.jsonl`, `DECISION_REGISTRY.jsonl` | append-only, SHA-256-Kette |
| `_developement/MCP-ACCESS-TOOLS/` | Connector-/Tool-Definitionen (NEXUS_05) | keine Secrets |
| `_INDEX/_INDEX.MASTER` | globaler Wegweiser (Low-Tech, beliebig duplizierbar) | MUST-22; kein Chunking/Embedding |
| `_INDEX/00_ARTEFAKTE-BIBLIOTHEK/` | Master-Templates NEXUS_01–07, RACI-Template, Wegweiser-Datei | Master hier, Kopie im Arbeitsordner |
| `_INDEX/_PENDING/` | Pending-Register, Audit-Reports, Arbeitspläne | additiv, DONE wandert in Historie |
| `_INDEX/ARCHIVE_HTML_DASHBOARDS/` | v1.1–v3.0 + SHA-256-Manifest | nur kopieren |
| `_INDEX/INDEX-LNK/` | Tree-Listings, Benchmarks (HOLZ/BETON/SEILSTATIK), Bookmarks | Discovery-Quelle für P8 |

**Hierarchie-Regel:** max. 3 Ebenen unter dem Root; Trennung nach Dateityp, nicht nach Projekt (Ausnahme: Projektordner der ZT GmbH bleiben unberührt).

## A5 Datei- und Ordnersyntax

**Verbindlich (ID01 20.09.2026, bewahrt durch MUST-33):**
`YY_MM_DD_<ID-LF-NR>_<CONTENT-TYPE>_<TITLE>[_vX.Y].<ext>`

- Regex (PROPOSAL für Lint): `^\d{2}_\d{2}_\d{2}_\d{4}_[A-Z][A-Z-]*_[A-Za-z0-9+\-.]+(_v\d+\.\d+)?\.(md|json|jsonl|yaml|csv|txt|html|py)$`
- `<ID-LF-NR>` = globale fortlaufende 4-stellige Nummer aus `00_ID_LEDGER.csv` (**nie** `max(filename)+1`, MUST-152); EXT-xx für extern verwaltete Google-native Dateien.
- `CONTENT-TYPE` (Enum, PROPOSAL erweitert): `STATUSREPORT | WORKORDER | TEMPLATE | RULEUPDATE | ACK | LEDGER | WHITEPAPER | MANUAL | DECISION | EVAL | RUNLOG | REGISTRY | SCHEMA | FIXTURE`
- Ausnahmen: WORK-Dateien ohne Datums-Präfix; Google-native Dokumente mit `__CURRENT__YYYY-MM-DD`.
- Timestamps im Inhalt: ISO 8601 mit Zeitzone (`2026-09-28T13:18:44+02:00`).
- POSIX-safe: keine Leerzeichen, keine Umlaute im Dateinamen; `+` erlaubt.

## A6 Rollen-IDs (Referenz — einzige Quelle: Manifest §4, NEXUS-ROLES-v1.0)

ID01 Human/Entscheidung · ID02 ChatGPT Orchestrator · ID03 ChatGPT Peer/QA · ID04 Gemini Evidence/Log · ID05 Perplexity Research · ID06 Claude Coding/Implementation (Codex-Runtime möglich, ohne eigene ID) · ID07 DeepSeek Auditor/Falsifikation · ID08 Ollama lokal · ID09/ID10 inaktiv. **Vor Ausführung erfassen:** executor_instance, provider, model_id/version, runtime, tool-/filesystem-scope (MUST-150).

## A7 Knowledge-Object-Schema (KO) — JSON-Template (PROPOSAL, kompatibel zu NEXUS_01 v0.1 + MUST-66)

```json
{
  "ko_id": "KO-000001",
  "uuid": "urn:uuid:<uuid4>",
  "ko_type": "SOURCE|CLAUSE|FORMULA|MATERIAL|COMPONENT|MODEL|SOLVER|COLLECTION|WORKORDER",
  "title": "EC5-1-1 §6.1.2 Zug parallel zur Faser",
  "domain": "TIMBER|CONCRETE|HBV|STEEL|GEOTECH|LCA|GOVERNANCE|AI-OS",
  "usecases": ["ULS-DESIGN", "HBV-GAMMA-METHOD"],
  "labels": ["EC5", "ULS", "TENSION"],
  "keywords": ["ft,0,d", "kmod", "gamma_M"],
  "keyvalues": {"gamma_M": 1.3, "unit": "-", "source_locator": "EC5-1-1 Tab.2.3"},
  "signals": {"slot1": "#EC5", "slot2": "#ULS", "slot3": "#TIMBER", "slot4": "#FORMULA", "slot5": "#MATURITY-ADOPTED"},
  "anchors": ["EC5-1-1#6.1.2", "ONORM-B-1995-1-1#NA"],
  "relations": [
    {"rel": "DERIVED_FROM", "target": "KO-000010", "evidence_locator": "EC5-1-1 Eq.(6.1)", "status": "CONFIRMED|CANDIDATE"}
  ],
  "source": {"source_id": "SRC-000123", "source_uri": "drive://<id>", "representation": "pdf", "version": "2019-06", "hash_sha256": "<64hex>", "locator": "p.41 §6.1.2", "authority_level": "PRIMARY|SECONDARY", "access": "PUBLIC|INTERNAL"},
  "standard": {"standard_id": "EN 1995-1-1", "edition": "2004+A2:2014", "national_annex": "ÖNORM B 1995-1-1:2019", "clause": "6.1.2", "validity_date": "2019-06-01"},
  "status": {"validity": "CURRENT|HISTORICAL|REFERENCE_ONLY", "maturity": "DRAFT|CANDIDATE|REVIEWED|ADOPTED", "review_status": "UNREVIEWED|PEER_OK|HUMAN_GATE_OK", "verification_status": "VERIFIED|UNVERIFIED|ASSUMPTION"},
  "rating": {"quality": 0, "evidence_level": 0, "signal_energy": 0.0, "scale": "0-5 / 0-5 / 0.0-1.0"},
  "owner_id": "ID06", "created_at": "2026-09-28T00:00:00+02:00", "modified_at": "2026-09-28T00:00:00+02:00",
  "run_id": "RUN-2026-09-28-0001", "ticket_id": "T-0000",
  "links": ["drive://<id>", "https://…"],
  "notes": ""
}
```

**Regeln:** `ko_id`, `uuid`, `source.hash_sha256`, `source.locator` sind Pflicht vor jeder Anreicherung (MUST-32). Keyword-Ähnlichkeit erzeugt nur `CANDIDATE`-Relationen (MUST-155). Zahlen in `keyvalues` tragen `unit` + `source_locator`.

## A8 Ontologie · Signalmatrix · Familien (PROPOSAL, Basis NEXUS_02/07)

- **Achsen:** DOMAIN × VALUE × SIGNAL × CAPABILITY × MATURITY × EVIDENCE (ID01 24.09.).
- **5 Hashtag-Slots je Signal, gleichgewichtet** (ID01 19.09.): Slot1 Norm/Quelle · Slot2 Nachweis/Use-Case · Slot3 Domain/Material · Slot4 KO-Typ · Slot5 Reifegrad/Evidenz.
- **Familien:** KO-Gruppen mit gemeinsamem Anker (z. B. Familie `EC5-1-1#6` = alle ULS-Nachweise Kap. 6). Familien-Anker sind Navigations-Knoten, keine Wissensobjekte.
- **Signal-Energie** `E = Σ(slot_hits × w_slot) × evidence_level / 25` ∈ [0,1] — dient nur der Ranking-Reihenfolge, nie der Autorität (MUST-83).
- **Relations-Enum:** `DERIVED_FROM | DEPENDS_ON | SUPERSEDES | CONFLICTS_WITH | PART_OF | VALIDATED_BY | USED_IN | SAME_AS(candidate)`.

## A9 Registries (Ist-Stand + Zielschema)

| Registry | Format | Ist | Schlüssel | Regel |
|:--|:--|:--:|:--|:--|
| `00_ID_LEDGER.csv` v0.2 | CSV | ✅ CANON | ID | append-only; Spalten ID,DATE,TYPE,TITLE,DRIVE_ID,FOLDER,SHA256,VALIDITY,MATURITY,SUPERSEDES,CANON,ACTOR,NAME_SCHEMA_OK,NOTE |
| Ticket-Registry (Sheet) | GSheet | ✅ CANON | TICKET_ID | Status-SSOT für Tickets (MUST-152) |
| `SOURCE_REGISTRY.csv` (120 Quellen) | CSV | ✅ | source_id | Pilot-Input nach Feldmapping (MUST-154) |
| `RESOURCE_REGISTRY.jsonl` | JSONL | 🔴 | source_id, hash | Identität vor Semantik; Pilot 25–50 Ressourcen |
| `KO_REGISTRY.jsonl` | JSONL | 🔴 | ko_id | Schema A7 |
| `RELATIONS.jsonl` | JSONL | 🔴 | (src,rel,tgt) | evidence_locator Pflicht |
| `DECISION_REGISTRY.jsonl` | JSONL | 🔴 | decision_id | Felder: decision_id, date, decided_by(ID01), scope, statement, supersedes, evidence_uri, status |
| `PENDING_TASKS_REGISTER` | MD | ✅ v2 (Stand 25.08., **stale**) | BIZ/SYS/DEV-# | Lifecycle §6 des Registers |
| `RUNLOG` | MD/JSONL | ✅ historisch | run_id | nur Evidenz, keine Koordination (MUST-152) |

## A10 Ingestion-Pipeline (Stufen, Ein-/Ausgabe, Gate)

| Stufe | Modul | IN | OUT | Gate |
|:--|:--|:--|:--|:--|
| 0 Discovery | `nexus_discover` (read-only Scanner) | Drive-Tree, Alt-Indexlisten, Bookmarks, Literaturlisten | `DISCOVERY.jsonl` (path, mime, size, mtime, DUPLICATE_CANDIDATE) | G0 keine Schreibrechte (MUST-157) |
| 1 Pre-Parse | `nexus_preparse` | Datei | Text/Struktur, Encoding, Seiten, Tabellen | G1 Syntax valide |
| 2 Identity | `nexus_identity` | Pre-Parse-Output | source_id, representation, version, SHA-256 | G2 Hash aus Bytes (MUST-150) |
| 3 Registry | `nexus_registry` | Identity | Zeile in RESOURCE_REGISTRY.jsonl | G3 keine Duplikat-Identität |
| 4 Chunk | `nexus_chunk` | Text + locator | Chunks mit source_id+locator | G4 kein Chunk ohne Locator (MUST-73) |
| 5 Classify | `nexus_classify` (LLM-Kandidat + Regel-Check) | Chunk | domain, ko_type, labels, 5 Signal-Slots | G5 Regel-Whitelist |
| 6 Extract | `nexus_extract` (KeyValue/MoE-Experten) | Chunk | keyvalues{unit, locator}, Formeln | G6 Einheiten-Check |
| 7 KO-Candidate | `nexus_ko` | Extract | KO-JSON (A7) `maturity=CANDIDATE` | G7 Schema-valid |
| 8 Link | `nexus_link` | KO-Set | RELATIONS.jsonl (CANDIDATE) | G8 evidence_locator oder CANDIDATE |
| 9 Rate | `nexus_rate` | KO + Relationen | rating{quality, evidence_level, signal_energy} | G9 deterministisch, reproduzierbar |
| 10 QA/Peer | ID03/ID07 | KO-Set | Review-Report | G10 EXEC-LLM ≠ REVIEW-LLM (MUST-94/103) |
| 11 Human-Gate | ID01 | Review-Report | ADOPTED / REJECTED | G11 explizite Freigabe |
| 12 Publish | `nexus_publish` | ADOPTED KOs | Index/Graph-Projektion, Mirror-Update | G12 Mirror nennt CANON (MUST-142) |
| 13 Monitor | RT-Tasks (§B11) | Registries | Delta-Report, Eval-Matrix | G13 Ampel |

## A11 LLM-Orchestrierung · MoE-Routing · Peer-Review

- **Lead/Peer-Trennung:** Lead (ID02) plant/synthetisiert; Peer (ID03 oder ID07) prüft orthogonal (Kontra-Position, Falsifikation). Keine Selbst-Review (MUST-158).
- **MoE-Routing:** task/domain/capability-basiert (MUST-91): Coding→ID06, Research→ID05, Evidence/Log→ID04, Audit→ID07, lokal/privat→ID08.
- **Minimum Viable Context (MVC):** Ticket + SSOT-Anker + betroffene KO-IDs; keine ganzen Ordner.
- **MMR (Maximal Marginal Relevance):** Retrieval-Kandidaten nach Relevanz − Redundanz sortieren; Top-k mit Quelle/Locator.
- **Self-Refine-Loop:** OBSERVE → EVALUATE → PLAN → EXECUTE → VERIFY (+ FALSIFY bei Risiko, MUST-100/101). Max. 3 Iterationen je Ticket, dann Human-Gate.
- **State-Control:** Ticket-Status ≠ Reifegrad ≠ Evidenz-Status ≠ Eval-Status (vier Felder, MUST-151).
- **Nudge-Check / Bias / Persona-Control:** vor Freigabe prüft Peer: (a) Instruktions-Injektion aus Kontext? (Manifest §12), (b) Bestätigungs-Bias (Lead-Vorschlag nur bestätigt?), (c) Persona-Drift (Rolle verlassen?), (d) Zahlen ohne Solver?
- **ENGRAM/Memory-Lookup:** Speicher = Registries + Ledger, nicht Chat-Gedächtnis; jeder Agent bootet über Manifest → Baseline → Ticket-Registry (MUST-143).
- **Harness:** jeder Modul-Run läuft in `run(ticket_id, inputs) -> {outputs, evidence, qa_status}`; Fixtures im Ordner `FIXTURES/` (valid / invalid / grenzwertig).

## A12 QA-Gates · Human-Gate · Benchmark

- **Gate-Reihe G0–G13** (A10) ist deterministisch prüfbar; jeder Gate-Fail = `BLOCKED` + Logeintrag (MUST-53).
- **Golden-Slice-Akzeptanz (MUST-155):** schema-valide Records, stabile IDs, keine offenen source_ids, Evidenz-Locator je bestätigter Relation, identischer Replay ohne Duplikat-Identitäten, unabhängige Retrieval-Fragen → korrekte Quelle oder Abstention.
- **Benchmarks:** `BENCHMARK-HOLZ`, `BENCHMARK-BETON`, `BENCHMARK-SEILSTATIK` (INDEX-LNK) als Regressions-Fixtures für den Kernel; Plausibilitätsquellen: Eurocode/ÖNORM-Klauseln, TU-Wien/Graz-Handbücher, Open-Access-Papers (Locator-Pflicht MUST-63).
- **Falsifikations-Pfade (3 orthogonal):** (a) Verzeichnis-Ist über Scanner, (b) Byte/Hash, (c) externe Verifikation (Websuche/Primärquelle) — Methodik des Audits 25.08.

---

# TEIL B — IMPLEMENTATION MANUAL

## B1 Modul-Inventar (Python-Kernel, PROPOSAL)

| Modul | Funktion (≤50 Zeilen/Funktion, Type Hints) | IN → OUT | Status |
|:--|:--|:--|:--:|
| `nexus_discover.py` | read-only Drive/Local-Scan, DUPLICATE_CANDIDATE | Tree → DISCOVERY.jsonl | 🟠 (nexus_drive_index v2.0 existiert, Mapping offen) |
| `nexus_preparse.py` | PDF/MD/HTML/CSV/TXT → Text+Struktur | Datei → PREPARSE.json | 🔴 |
| `nexus_identity.py` | SHA-256, version, representation | PREPARSE → IDENTITY.json | 🟠 (Hash-Chain aus drive_index) |
| `nexus_registry.py` | append-only JSONL + Hash-Kette, ID-Vergabe aus Ledger | IDENTITY → RESOURCE_REGISTRY.jsonl | 🔴 |
| `nexus_chunk.py` | Chunking mit Locator | Text → CHUNKS.jsonl | 🔴 |
| `nexus_classify.py` | Regel-Whitelist + LLM-Kandidat | Chunk → labels/signals | 🔴 |
| `nexus_extract.py` | KeyValue/Formel-Extraktion, Einheiten-Check | Chunk → keyvalues | 🔴 |
| `nexus_link.py` | Relationen-Kandidaten + Evidenz-Locator (WO 0023) | KO-Set → RELATIONS.jsonl | 🔴 DRAFT |
| `nexus_lint.py` | Namensschema, Ledger-Konsistenz, Schema-Validierung (WO 0027) | Ordner → LINT_REPORT.md | 🔴 DRAFT |
| `nexus_delta_sync.py` | WORK ↔ _INDEX ↔ REGISTRY Delta (move-only) | Registries → DELTA_REPORT.md | 🔴 |
| `nexus_eval.py` | Eval-Matrix-Berechnung (§B8), Ampel | STEPS.yaml → EVAL_MATRIX.md | 🔴 |
| `get_secret.py` | keepassxc-cli / env → Virtual Key (LiteLLM) | service → key (nie geloggt) | 🔴 |
| `solvers/*` | EC2/EC5/HBV/FT deterministisch | JSON-Input → JSON-Output + Gleichgewichtscheck | 🟠 (Solver-Lib vorhanden) |

## B2 Schnittstellen-Verträge (fix definierte Übergabeformate)

**WO-IN (Ticket, MUST-41):** `TICKET_ID | CREATED_AT | OWNER_ID | PRIORITY | STATUS | SOURCE/SSOT_ANCHOR | OBJECTIVE | INPUTS | CONSTRAINTS | TASK | EXPECTED_OUTPUT | ACCEPTANCE_CRITERIA | DEPENDENCIES | RISKS | NEXT_ACTION`

**WO-OUT / Reporting-Syntax (Ende jeder Antwort, ID01 20.09. + MUST-45):**
```
STATUS: DONE|BLOCKED|REVIEW_REQUIRED|FAILED
CHANGED: <Artefakte mit Drive-ID/Pfad>
TESTS: <Fixture-Ergebnisse oder "keine">
SOURCE_STATUS: VERIFIED|UNVERIFIED|ASSUMPTION je Kernaussage
RISKS_GAPS: <…>
NEXT: <nächste Aktion + Owner-ID>
QA_STATUS: <Peer/Human-Gate>
LOG: <wo protokolliert / "PROTOKOLL FEHLT">
```

**Modul-IO (jede Python-Funktion):**
```python
def run(ticket_id: str, inputs: dict, cfg: dict) -> dict:
    """returns {"outputs": {...}, "evidence": [locator, ...],
               "qa_status": "PASS|FAIL|SKIP", "run_id": str, "hash_in": str, "hash_out": str}"""
```

**RUNLOG-Zeile (JSONL, MUST-51):**
`{"run_id","ticket_id","agent_id","executor_instance","model_id","started_at","completed_at","status","inputs","artifacts","qa_status","next_action"}`

**DECISION-Zeile (JSONL):**
`{"decision_id":"D-0001","date":"2026-09-20","decided_by":"ID01","scope":"NAMING","statement":"YY_MM_DD_<ID>_<TYPE>_<TITLE>.md","supersedes":null,"evidence_uri":"chat/ledger","status":"ADOPTED"}`

**config.yaml (PROPOSAL):** `drive_root`, `ssot_root`, `work_dir`, `registry_dir`, `index_master`, `ledger_path`, `secret_backend: keepassxc|env`, `llm_gateway: litellm`, `models: {lead, peer, coder, auditor}`, `chunk: {size, overlap}`, `gates: {g0..g13: true}`, `eval_weights: {spec:0.20, impl:0.30, test:0.20, integ:0.15, doc:0.15}`.

## B3 Reporting-, Logfile- und Statusbericht-Regeln

1. Jeder substantielle Run → RUNLOG-Zeile + Ticket-Registry-Update (MUST-50).
2. Statusberichte im SSOT-Root mit Präfix und ART-ID; Struktur: Kopfblock (wie Seite 1 dieses Dokuments) → TL;DR → Befund → Eval-Matrix → NEXT → LOG-Zeile.
3. Verifiziert / Annahme / Vorschlag / offen / Fehler sind sprachlich getrennt (MUST-52/62).
4. **LOG-Zeile ist Pflicht** in jeder Arbeitsanweisung/Antwort; fehlt ein Protokoll: `LOG: PROTOKOLL FEHLT`.
5. Kein Mailversand, keine Drive-Löschung, keine Secrets, keine simulierten Runs.

## B4 Artefakt-Archivierungspflicht

- Jede Version bleibt erhalten; Nachfolger nennt `SUPERSEDES` (MUST-131/132).
- Ersetzte Datei: Umbenennung mit `_SUPERSEDED_YYYY-MM-DD`, Verschiebung in `ARCHIVE_*`, Ledger-Note (Vorbild: Ledger 0020).
- HTML-Dashboards: je Version eigener Ordner + SHA-256-Manifest (Ist seit 25.08.).
- Chat-Handoffs an andere LLMs: `.md` mit Timestamp im SSOT-Root; WORK-Antworten ohne Präfix.

## B5 Delta-Synchronisierung WORK ↔ _INDEX ↔ REGISTRY (Algorithmus, PROPOSAL)

1. `discover(WORK)`, `discover(_INDEX)`, `read(REGISTRY, LEDGER)` → drei Mengen (path, hash, id).
2. Klassifiziere: `NEW` (Hash unbekannt) · `MOVED` (Hash bekannt, Pfad neu) · `MODIFIED` (id bekannt, Hash neu) · `ORPHAN` (Registry-Eintrag ohne Datei) · `DUPLICATE_CANDIDATE` (Titel+Größe gleich, Hash offen).
3. Ausgabe `DELTA_REPORT.md` (Tabelle je Klasse) — **keine automatische Schreibaktion**; Move/Register nur nach ID01-Freigabe oder Ticket.
4. Nach Freigabe: Ledger-Append, Registry-Append, Mirror-Update mit `CANONICAL SOURCE =`.

## B6 Implementierungsphasen (chronologisch)

| Phase | Inhalt | Owner | Akzeptanz |
|:--|:--|:--|:--|
| P0 Governance | Manifest, Baseline, Rollen, Ledger, Ticket-Registry | ID01/ID02 | ✅ CURRENT 28.09. |
| P1 Discovery/Index | Alt-Indexlisten, Trees, Bookmarks ingestieren; Wegweiser; Mirrors | ID06/ID04 | Wegweiser + DISCOVERY.jsonl vorhanden |
| P2 Registry-Pilot | 25–50 Ressourcen, Feldmapping, Lint | ID06, Review ID07 | MUST-155 erfüllt |
| P3 Semantic MVP | Chunk/Classify/Extract/Link auf Pilot | ID06/ID03 | Golden Slice PASS |
| P4 Kernel-Kopplung | Solver-Lib ↔ KO-KeyValues, Benchmarks | ID06/ID07 | Regressionstests PASS |
| P5 Secret+Gateway | KeePassXC + LiteLLM, get_secret | ID06 | kein Klartext-Key im Drive |
| P6 Frontend | Wrapper-Dashboard (Graph, Eval-Matrix, Startbanner) | ID06 | Standalone-HTML läuft offline |
| P7 Betrieb | RT-Tasks, Monitoring, Refinement | ID02/ID01 | Eval-Matrix ≥ 80 % 🟢 |

## B7 Bewertungsschema QUICK-IMPLEMENTATION-STEPS-EVAL-MATRIX (eigenes Punkte-/Gewichtungsschema)

| Kriterium | Gewicht | 0 | 3 | 5 |
|:--|:--:|:--|:--|:--|
| K1 SPEZIFIKATION | 0.20 | keine | Schema/Template vorhanden | adoptiert, eindeutig |
| K2 IMPLEMENTIERUNG | 0.30 | nichts | MVP läuft | vollständig, robust |
| K3 TEST/EVIDENZ | 0.20 | keine | Fixtures teilweise | Golden Slice / Replay PASS |
| K4 INTEGRATION | 0.15 | isoliert | mit 1 Nachbarmodul | End-to-End verkettet |
| K5 DOKU/LOG | 0.15 | keine | Report vorhanden | Ledger+Ticket+Report konsistent |

- **%-Completion** = Σ(w·p)/5 · 100.
- **★-Rating:** ≥95 ★★★★★ · 80–94 ★★★★☆ · 60–79 ★★★☆☆ · 40–59 ★★☆☆☆ · 20–39 ★☆☆☆☆ · <20 ☆☆☆☆☆.
- **Ampel:** ≥70 🟢 · 35–69 🟠 · <35 🔴 · BLOCKED ⚫.
- **Gesamt:** ungewichtetes Mittel **und** kritikalitätsgewichtet (Knowledge-Pipeline ×2, da Kernpfad).

## B8 QUICK-IMPLEMENTATION-STEPS-EVAL-MATRIX (Stand 2026-09-28, Evidenz: Ledger v0.2 / Manifest / Audit 25.08.)

| # | Step | Evidenz | K1 | K2 | K3 | K4 | K5 | % | ★ | Ampel |
|:--:|:--|:--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| S01 | Manifest CURRENT adoptiert | EXT-01 CANON | 5 | 5 | 4 | 5 | 5 | 96 | ★★★★★ | 🟢 |
| S02 | Baseline Instructions CURRENT | EXT-02 CANON | 5 | 5 | 4 | 5 | 5 | 96 | ★★★★★ | 🟢 |
| S03 | Rollenregister ROLES-v1.0 + ACK ID06 | 0025 DONE | 5 | 5 | 4 | 4 | 5 | 93 | ★★★★☆ | 🟢 |
| S04 | ID-Ledger v0.2 (append-only) | 0020 CANON | 5 | 5 | 3 | 4 | 4 | 86 | ★★★★☆ | 🟢 |
| S05 | Ticket-Registry (Sheet) | EXT-03 CANON | 5 | 4 | 3 | 4 | 4 | 80 | ★★★★☆ | 🟢 |
| S06 | _INDEX/_PENDING-Audit, Archiv + SHA-256, SOURCE_REGISTRY 120 | Audit 25.08. | 5 | 5 | 4 | 4 | 5 | 93 | ★★★★☆ | 🟢 |
| S07 | PENDING-Register v2 | 25.08. (**stale**) | 5 | 5 | 4 | 4 | 5 | 93 | ★★★★☆ | 🟢 |
| S08 | Master-Templates NEXUS_01–07 | 0013–0018, 0026 DRAFT | 4 | 3 | 1 | 2 | 4 | 56 | ★★☆☆☆ | 🟠 |
| S09 | Wegweiser/Anker + Mirrors (MUST-141/142) | Entscheid 25.09., Umsetzung UNVERIFIED | 4 | 2 | 1 | 2 | 2 | 44 | ★★☆☆☆ | 🟠 |
| S10 | Dieses Whitepaper/Manual 0028 | PROPOSED | 5 | 4 | 0 | 2 | 5 | 65 | ★★★☆☆ | 🟠 |
| S11 | Resource-Registry-Pilot 25–50 + WO 0022 | MUST-154, DRAFT | 4 | 2 | 1 | 2 | 3 | 47 | ★★☆☆☆ | 🟠 |
| S12 | Semantic-Linker WO 0023 | DRAFT | 4 | 1 | 0 | 1 | 3 | 34 | ★☆☆☆☆ | 🔴 |
| S13 | Lint-Validator WO 0027 | DRAFT | 4 | 1 | 0 | 1 | 3 | 34 | ★☆☆☆☆ | 🔴 |
| S14 | Pre-Parser / deterministische Extraktion | kein Artefakt | 3 | 1 | 0 | 0 | 2 | 24 | ★☆☆☆☆ | 🔴 |
| S15 | KO-Candidate + Signals/KeyValues/MoE-Extraktion | Template only | 3 | 1 | 0 | 0 | 2 | 24 | ★☆☆☆☆ | 🔴 |
| S16 | Verified Registry/Index/Graph-Projektion | kein Artefakt | 3 | 0 | 0 | 0 | 2 | 18 | ☆☆☆☆☆ | 🔴 |
| S17 | Retrieval index-first + RAG-Fallback | Regel vorhanden | 3 | 1 | 0 | 0 | 2 | 24 | ★☆☆☆☆ | 🔴 |
| S18 | Golden-Slice-Akzeptanz + Replay-Tests | MUST-155 | 4 | 0 | 0 | 0 | 2 | 22 | ★☆☆☆☆ | 🔴 |
| S19 | Python-Kernel (Solver-Lib EC2/EC5) ↔ KO | Solver vorhanden | 4 | 3 | 3 | 1 | 2 | 55 | ★★☆☆☆ | 🟠 |
| S20 | Secret-Framework KeePassXC + LiteLLM | Phase B 0 % | 4 | 0 | 0 | 0 | 2 | 22 | ★☆☆☆☆ | 🔴 |
| S21 | Drive-Automation / Delta-Sync (move-only) | Phase C, F6 | 3 | 1 | 0 | 0 | 1 | 21 | ★☆☆☆☆ | 🔴 |
| S22 | Frontend Wrapper-Dashboard (three.js Graph) | Dashboards v1–v3 | 3 | 2 | 1 | 1 | 2 | 37 | ★☆☆☆☆ | 🟠 |
| S23 | AEC-Voice-Stack v2.5 (Phase D) | 10 % | 3 | 1 | 0 | 0 | 2 | 24 | ★☆☆☆☆ | 🔴 |
| S24 | Wiederkehrende Eval-/Monitoring-Tasks | definiert §B11 | 4 | 0 | 0 | 0 | 3 | 25 | ★☆☆☆☆ | 🔴 |
| S25 | Drive-Hygiene Move-only-Plan P1–P7 | 0012 CANDIDATE | 4 | 3 | 2 | 2 | 4 | 60 | ★★★☆☆ | 🟠 |

## B9 OVERALL-BEWERTUNG · GESAMTFERTIGSTELLUNGSGRAD

| Layer | Steps | Ø % | Ampel |
|:--|:--|:--:|:--:|
| Governance / Registries | S01–S10 | **80 %** | 🟢 |
| Knowledge-Pipeline (Kernpfad) | S11–S18 | **28 %** | 🔴 |
| Kernel / Infra / Frontend / Betrieb | S19–S25 | **35 %** | 🟠 |
| **GESAMT ungewichtet** | S01–S25 | **≈ 51 %** | 🟠 |
| **GESAMT kritikalitätsgewichtet** (Pipeline ×2) | – | **≈ 46 %** | 🟠 |

**Overall-Rating: ★★☆☆☆ (46–51 %) · 🟠** — Governance ist belastbar; der Wissens-Kernpfad (Registry → KO → Graph → Retrieval) ist spezifiziert, aber nicht implementiert. Engpass = S11–S16.

## B10 NEXT STEPS — Low-Hanging-Fruit · Low-Compute · Small+Fast · High-Quality

| # | Schritt | Owner | Aufwand | Effekt |
|:--:|:--|:--:|:--:|:--|
| N1 | Human-Gate 0028 (ADOPT/MODIFY/REJECT) + Ledger-Zeile anhängen (Anhang F) | ID01 / ID06 | 5 min | S10 → 🟢 |
| N2 | `00_WEGWEISER_NEXUS.md` in 00_ARTEFAKTE-BIBLIOTHEK + `CANONICAL SOURCE =`-Hinweis in WORK und _INDEX.MASTER | ID06 | 10 min | S09 → 🟢 |
| N3 | `DECISION_REGISTRY.jsonl` anlegen, 6 Altbeschlüsse nachtragen (Namensschema 20.09., Prio-Axiom 20.09., Slot-Gewichte 19.09., Rollen 26./28.09., Ledger v0.2 28.09., Wegweiser 25.09.) | ID06, Readback ID04 | 15 min | Registry-Layer komplett |
| N4 | Lint-Validator MVP (WO 0027): 3 Fixtures valid/invalid/grenzwertig, 1 Run Claude Code, Review ID07 | ID06 → ID07 | 1 Run | S13 → 🟠, Basis für S11 |
| N5 | Feldmapping-Tabelle `SOURCE_REGISTRY.csv` → KO-Schema A7 (nur Tabelle, kein Code) für Pilot-Input 1_N-J3pSAcHtr5sv0jGFmyWHpYQYz4TJj | ID06 | 20 min | S11 entblockt |
| N6 | DEV-4 QA-Audit als `.md` + B1 `api_keys_inventory_TEMPLATE.csv` (maskiert) | ID06 | 15 min | Altlasten Phase B/C |
| N7 | PENDING-Register v3: BIZ/SYS-Status seit 25.08. verifizieren (Lifecycle-Regel) | ID02 | 20 min | S07 stale → aktuell |
| N8 | RT-Tasks (§B11) als Kalender-Reminder anlegen (Drive weckt keine LLMs, MUST-96) | ID01 | 5 min | S24 → 🟠 |

## B11 Wiederkehrende Aufgaben (Recurring Tasks — Monitoring & laufende Bewertung)

| RT | Rhythmus | Aufgabe | Owner | Output / Ablage |
|:--|:--|:--|:--:|:--|
| RT-1 | täglich (Werktag) | Startbanner Top-10 + Ticket-Registry-Delta (OPEN/BLOCKED) | ID02 | Chat-Banner; Sheet |
| RT-2 | wöchentlich Mo | **QUICK-EVAL-MATRIX-Update** (§B8) + OVERALL + NEXT | ID06 | `YY_MM_DD_<ID>_EVAL_NEXUS-STEPS-MATRIX.md` im SSOT-Root |
| RT-3 | wöchentlich | Peer-Review-Stichprobe: 1 DONE-Ticket falsifizieren | ID07 | Review-Report in WORK |
| RT-4 | 14-tägig | Delta-Sync WORK ↔ _INDEX ↔ REGISTRY (read-only) | ID06/ID04 | `DELTA_REPORT.md` |
| RT-5 | monatlich | Governance-Readback (Manifest/Baseline/Decision-Registry), Mirror-Staleness | ID01 | Adoption-Vermerk |
| RT-6 | quartalsweise | Key-Rotation/Secret-Inventur (ohne Werte), Backup-Test .kdbx | ID01/ID06 | `api_keys_inventory.csv` (maskiert) |
| RT-7 | je Release | Benchmark-Regression HOLZ/BETON/SEIL gegen Solver-Lib | ID06 → ID07 | Testreport |

Trigger: menschlicher Aufruf oder Kalender/Watcher — nie "Drive-Update = Agent wach" (MUST-159).

---

# TEIL C — FRONTEND USER MANUAL (für ID01 und Gäste)

## C1 Einstieg (< 5 min)

1. Öffne `_developement/LLM-LOCAL-SSOT/` → lies `00_NEXUS_MANIFEST__CURRENT__…` und `…BASELINE…` (Bootstrap-Reihenfolge MUST-143).
2. Öffne Ticket-Registry (Sheet) → Startbanner = Top-10 OPEN/BLOCKED nach Prio-Axiom.
3. Neue Arbeit nur über Ticket (WO-IN, §B2). Für externe LLMs: 1–2 bestehende WOs in `WORK/` als Syntaxvorlage lesen, dann im selben Muster anlegen.

## C2 Standard-Workflows

| Ziel | Schritte | Ergebnis |
|:--|:--|:--|
| Quelle einbringen | Datei in `WORK/IN/` → `CLAIM <ticket> ID06` → Pipeline Stufen 0–7 → KO-CANDIDATE | KO-JSON + Registry-Zeile |
| Wissen finden | Stichwort → `_INDEX.MASTER` / Tree → Registry-Lookup → erst dann RAG | Quelle + Locator (oder Abstention) |
| Bemessung | Ticket mit Input-JSON → Solver (`solvers/*`) → Gleichgewicht ΣV=0/ΣM=0 + Einheiten-Check → Report | Zahlen nur aus Kernel |
| Review/Freigabe | Peer-Report lesen → ADOPT / MODIFY / REJECT → Ledger/Registry-Status | `maturity=ADOPTED` |
| Aufräumen | Delta-Report prüfen → Move-only-Freigabe → Mirror-Update | nichts gelöscht |
| Status | RT-2 Eval-Matrix öffnen → Ampeln, OVERALL, NEXT | Entscheidungsgrundlage |

## C3 Kommandos (Chat-Konventionen, PROPOSAL)

`/status` Eval-Matrix + Banner · `/wo new` WO-IN-Template · `CLAIM <ticket> <ID>` (MUST-42) · `/report <ticket>` WO-OUT-Syntax · `/find <keyword>` index-first · `/delta` Delta-Report · `/promote <ko_id>` Human-Gate-Vorlage · `/eval` Matrix neu berechnen · `/log` letzte RUNLOG-Zeilen. Sprachmodus: keine URLs vorlesen, Listen ins Textfenster.

## C4 Dashboards (Standalone-HTML, offline, Pyodide/three.js)

- **Control Tower:** Ticket-Status, Ampeln, Eval-Matrix (liest `EVAL_MATRIX.json`).
- **Graph-Explorer:** KO-Knoten, Relationen, Familien-Anker; Farbe = Reifegrad, Größe = Signal-Energie; Klick → Quelle/Locator.
- **AEC-Voice v2.5:** Sprach-Trigger → Tool-Call → Python-Kernel (nur nach D1-Test).
- Regel: Dashboards lesen JSON aus dem Drive-Klon; sie schreiben nie in Registries.

## C5 FAQ / Fehlerbilder

| Symptom | Ursache | Abhilfe |
|:--|:--|:--|
| Zwei Dateien mit gleicher ID | ID aus Dateiname statt Ledger | Ledger ist Quelle; Datei umbenennen, Ledger-Note |
| KO ohne Locator | Gate G4 umgangen | Chunk verwerfen, Pre-Parse wiederholen |
| Agent meldet DONE ohne Test | MUST-54 verletzt | Status → REVIEW_REQUIRED |
| Zahl aus LLM statt Solver | MUST-155 | ablehnen, Solver-Ticket |
| Mirror widerspricht Kanon | Staleness | Kanon gewinnt, Mirror markieren (MUST-144) |
| Externer Agent reagiert nicht | Drive weckt nicht (MUST-96) | manuell anstoßen, ACK erst bei echter Antwort |

---

# ANHANG

## Anhang A — Regel-/Keyword-Kanon (fortgesetzte, konsolidierte Liste)

| Gruppe | Elemente | Bezug |
|:--|:--|:--|
| K-A Struktur | Ordner-Hierarchie, `_INDEX.MASTER`, `_PENDING`, `WORK`, `REGISTRY`, `ARCHIVE_*`, Move-only | A4, MUST-20–25 |
| K-B Identität | Dateisyntax, Timestamp ISO, ART-ID/Ledger, UUID, SHA-256, Representation, Version, EXT-ID | A5, MUST-30–34, 150 |
| K-C Rollen | ID01–ID10, executor_instance, provider, model_id, runtime, capability-check, RACI | A6, MUST-90–96 |
| K-D Wissensobjekt | KO-Typ, Domain, Use-Case, Labels, Keywords, KeyValues+Units, Anker, Familien, Relationen+Evidenz-Locator, Rating, Signal-Energie | A7/A8, MUST-66/72 |
| K-E Registries | ID-Ledger, Resource/Source, KO, Relations, Decision, Ticket, Pending, RUNLOG; append-only; Hash-Kette | A9, MUST-70–76, 152 |
| K-F Pipeline | Discovery, Pre-Parse, Identity, Chunking, Classification, KeyValue/MoE-Extraction, Linking, Rating, Publish, Monitor | A10 |
| K-G Retrieval | Tree/Index/Registry first, Vektor-Fallback, MMR, Provenienz, Abstention | MUST-80–84 |
| K-H Orchestrierung | Lead/Peer, MoE-Routing, MVC, MVP, Self-Refine (OEPEV+F), State-Control (4 Statusfelder), Nudge-/Bias-/Persona-Check, Engram/Bootstrap, Harness/Fixtures | A11, MUST-100–105 |
| K-I QA | Gates G0–G13, Golden Slice, Replay, Benchmarks HOLZ/BETON/SEIL, Falsifikation 3-Pfad, Human-Gate, Independent Reviewer | A12, MUST-155/158 |
| K-J Reporting | WO-IN/WO-OUT-Syntax, RUNLOG-Zeile, Statusreport-Struktur, LOG-Zeile, Verifiziert/Annahme-Trennung | B2/B3, MUST-50–55 |
| K-K Archiv | SUPERSEDES, `_SUPERSEDED_` Umbenennung, Versionsordner, Hash-Manifest, Historie erhalten | B4, MUST-131/132 |
| K-L Sicherheit | Zero-Secrets, KeePassXC+LiteLLM Virtual Keys, Least Privilege, Public/Internal-Provenienz, Untrusted Context | MUST-26, 112, 120–123, Manifest §12 |
| K-M Kernel | Solver EC2/EC5/HBV/FT, Einheiten-Check, Gleichgewicht, Plausibilität, Normkonformität, Type Hints, ≤50 Zeilen/Funktion | B1, Engineering-Konventionen |
| K-N Frontend | Standalone-HTML, Startbanner, Eval-Matrix-View, Graph-Explorer, Voice, read-only auf Registries | C4 |
| K-O Betrieb | RT-1…RT-7, Delta-Sync, Staleness, Key-Rotation, Backup, kontinuierliche Verbesserung | B5, B11 |

## Anhang B — Glossar (Auszug)

SSOT Single Source of Truth · KO Knowledge Object · KES Knowledge Engineering System · MVC Minimum Viable Context · MVP Minimum Viable Product/Prompt · MMR Maximal Marginal Relevance · MoE Mixture of Experts · OEPEV Observe-Evaluate-Plan-Execute-Verify · Golden Slice reproduzierbarer Referenz-Datensatz · Locator kleinste zitierbare Fundstelle · Human-Gate ID01-Freigabe · Move-only nie löschen · LHF Low-Hanging Fruit.

## Anhang C — Einheiten- und Spaltenstandard (Kernel ↔ KO)

SI konsequent: Länge m/mm, Kraft kN, Moment kNm, Spannung N/mm², Fläche m²/mm², Dichte kg/m³. Spalten in CSV/JSON: `snake_case`, Einheit als eigene Spalte `unit`, nie im Wert. Norm-Referenz: `standard_id | edition | national_annex | clause | table/equation | validity_date` (MUST-65).

## Anhang D — Fixture-Minimalsatz je Modul

`valid_01` (erwartet PASS) · `invalid_01` (erwartet FAIL mit Fehlercode) · `edge_01` (Grenzwert: leere Datei, Umlaut im Namen, doppelter Hash). Replay-Regel: identischer Input → identischer Output-Hash.

## Anhang E — Bezüge zu Altregistern (additiv, nichts ersetzt)

- `26_08_25_MASTER_AUDIT_REPORT_UND_ARBEITSPLAN.md`: Phasen B/C/D → hier S20/S21/S23; Gap-Matrix G1–G8 → S20, RT-6.
- `26_08_25_PENDING_TASKS_REGISTER_v2.md`: DEV-4…DEV-10 → N6, S20–S21; BIZ/SYS-Track unverändert, Verifikation → N7.

## Anhang F — Ledger-Zeile (zum Anhängen an `00_ID_LEDGER.csv`, nur nach ID01-Freigabe)

```
0028,2026-09-28,WHITEPAPER,NEXUS-AI-AEC-KES_MANIFEST+IMPL+USER-MANUAL_v1.0,<DRIVE_ID>,LLM-LOCAL-SSOT,<SHA256>,CURRENT,PROPOSED,,false,ID06,1,Whitepaper+Impl-Manual+User-Manual; Eval-Matrix 25 Steps; ID01-Freigabe offen
```

---

```
STATUS: REVIEW_REQUIRED
CHANGED: 26_09_28_0028_WHITEPAPER_NEXUS-AI-AEC-KES_MANIFEST+IMPL+USER-MANUAL_v1.0.md (SSOT-Root)
TESTS: keine (Dokument; Eval-Matrix rechnerisch geprüft: Σ/25 = 50.9 %)
SOURCE_STATUS: Manifest/Baseline/Ledger VERIFIED (Byte-Zugriff 28.09.); S09/S16/S17/S21 Ist-Stand UNVERIFIED (kein Artefakt gefunden)
RISKS_GAPS: PROPOSAL-Anteile (Registry-Ordner, Enum-Erweiterung, Kommandos, Signal-Energie-Formel) nicht adoptiert; PENDING-Register stale seit 25.08.
NEXT: N1 Human-Gate ID01 → N2 Wegweiser → N4 Lint-MVP
QA_STATUS: kein Peer-Review (ID03/ID07 ausständig)
LOG: Ledger-Zeile 0028 OFFEN; Ticket-Registry-Zeile OFFEN; Datei im SSOT-Root abgelegt
```
