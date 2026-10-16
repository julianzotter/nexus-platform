# TASK-00004: INVENTAR — Agent D / Curator

**Status:** TOOLING_MERGED_SCAN_PENDING (Tooling gemergt in PR #2; realer Scan steht aus, alle Quellen `INCOMPLETE`)
**Owner:** ID-02 (Agent D / Curator)
**Implementation Support:** Coding Agent (nur Tooling, kein Rollenträger)
**Reviewer:** ID-01 (Human Gate)
**Start:** 2026-10-08

> **Regel: Evidenzmetriken werden nie vorab befüllt.** Alle Zahlen (Coverage, Duplikate, Dateianzahlen) stehen in dieser Spezifikation als Platzhalter `[MEASURED_AFTER_SCAN]` und werden ausschließlich aus dem tatsächlichen Scan erzeugt.

---

## Rollen

| Rolle | Verantwortung | Status |
|---|---|---|
| ID-02 / Agent D (Curator) | Task-Ownership, Datenqualität, Evidence-Kette, Signatur | OWNER |
| Coding Agent | Implementierung der deterministischen Skripte (Scan, Duplikate, Coverage, Katalog) | SUPPORT |
| ID-01 | Review, Approval, Merge-Entscheidung | HUMAN GATE |

*D owns the task; coding support implements tooling.*

## Governance

1. Spezifikation liegt auf `main`.
2. Die gesamte Inventar-Arbeit erfolgt ausschließlich auf `feature/TASK-00004-inventory`.
3. PR nach `main`, Review durch ID-01, Status `AWAITING_REVIEW`.
4. **Kein automatischer Merge.**

## Aufgabe

Quellen inventarisieren: Repos, Obsidian-Vault, Google Drive (soweit zugänglich).

**Wichtig:** Quellrepos bleiben read-only. Keine Änderungen an Quellen. Nur Metadaten erfassen.

## Input

- `julianzotter/julianzotter/tools/01_scan_registry.py` (atomarer Scanner)
- Quellen (Zugänglichkeit je Quelle im Report ausweisen):
  - `julianzotter/NEXUS-AI-AEC-ENGINEERIN-KNOWLEDGE-GRAPH`
  - `julianzotter/julianzotter`
  - Obsidian-Vault (lokal oder Drive)
  - Google Drive (falls Zugang vorhanden)

## Output

```
registry/
├─ file-registry.jsonl        # 1 Zeile = 1 Datei
├─ duplicates-report.md       # alle Duplikat-Kandidaten, deterministisch
├─ catalog-draft.yaml         # Status = DRAFT
├─ inventory-summary.txt      # Coverage je Quelle
└─ coverage-per-source.json   # maschinenlesbar
```

## Datensatz je Datei (file-registry.jsonl)

| Feld | Beschreibung |
|---|---|
| `id` | SHA-256(root + relpath)[:16], stabil |
| `root`, `path`, `name`, `ext` | Herkunft |
| `size`, `mtime` | Metadaten (mtime ISO 8601) |
| `sha256` | Hash über Bytes, `null` bei Datei > 500 MB |
| `status` | `FOUND` / `SKIPPED` / `ERROR` / `INCOMPLETE` (bei Zugriff verweigert) |
| `duplicate_of` | id der Referenzdatei bei gleichem SHA-256 |
| `duplicate_group` | Gruppen-ID bei mehreren Duplikaten |

`supersedes` wird **nicht** für Duplikate verwendet, nur für echte Versionsnachfolge.

## Coverage-Definition

**Explizite Formel (verbindlich):**

```
Coverage % = ( indexed / accessible ) × 100
```

**Definitionen:**
- `discovered`: Dateien auf Quelle laut Dateisystem sichtbar
- `accessible`: Dateien, die lesbar sind (keine Permission-Fehler, keine Locks)
- `indexed`: Dateien, die erfolgreich in `file-registry.jsonl` aufgenommen wurden
- `skipped`: Dateien, die per Ausschlussregel bewusst übersprungen (z.B. `__pycache__`)
- `error`: Dateien, die Fehler beim Lesen erzeugt haben
- `INCOMPLETE`: Quelle war nicht zugänglich (z.B. Google Drive offline, Obsidian-Pfad nicht gefunden)

**Beispiel:**
```
Quelle A: discovered=100, accessible=98, indexed=95, skipped=2, error=1
Coverage = 95 / 98 = 96.9 %

Quelle B: INCOMPLETE (kein Zugriff)
Coverage = INCOMPLETE
```

## Abnahmekriterien

- [ ] Coverage je Quelle ausgewiesen nach Formel: `indexed / accessible`
- [ ] Inaccessible Quellen als `INCOMPLETE` gekennzeichnet (nicht geraten)
- [ ] Gesamtquote indexed/accessible wird berichtet (Zielwert ≥ 90 %, Abweichungen begründet)
- [ ] Alle Duplikat-Kandidaten deterministisch gelistet (kein Mindestwert)
- [ ] Gleicher SHA-256 → `duplicate_of` bzw. `duplicate_group`
- [ ] Ausschlüsse: `__pycache__`, `.git`, `node_modules`, `$RECYCLE.BIN`, `System Volume Information`
- [ ] Credentials ausgeschlossen: `token.json`, `credentials.json`, `.env*`
- [ ] Atomares Schreiben (`.tmp` → `replace`)
- [ ] Rohdateien unverändert, read-only
- [ ] Alle Metriken stammen aus dem realen Lauf, nichts vorbefüllt
- [ ] Keine Metriken geraten (report `INCOMPLETE` bei Zugriff verweigert)
- [ ] Skript-Versionen und Aufrufparameter im Report dokumentiert (Reproduzierbarkeit)
- [ ] PR gegen `main`, Reviewer ID-01, Status `AWAITING_REVIEW`
- [ ] Nur Task-erforderliche Dateien in PR (keine unrelated changes)

## Coverage-Tabelle (Vorlage, wird vom Scan befüllt)

| Quelle | discovered | accessible | indexed | skipped | error | coverage |
|---|---|---|---|---|---|---|
| NEXUS-AI-AEC-ENGINEERIN-KNOWLEDGE-GRAPH | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] |
| julianzotter | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] |
| Obsidian-Vault | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] |
| Google Drive | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] |

Duplikat-Kandidaten gesamt: `[MEASURED_AFTER_SCAN]`

## Tooling (durch Coding Agent zu implementieren, deterministisch)

- `tools/01_scan_registry.py` (vorhanden, ggf. um Coverage-Zähler erweitern)
- `tools/generate_catalog.py` (vorhanden): erzeugt `catalog-draft.yaml` aus `coverage-per-source.json`
- `tools/detect_duplicates.py` (neu): Gruppierung nach SHA-256, Report und Felder
- `tools/coverage_stats.py` (neu): Zähler je Quelle nach Formel, JSON und TXT
- Katalog-Generator für `catalog-draft.yaml` (Status = DRAFT)
- Unit-Tests für alle neuen Skripte (Muster: `tests/test_scan_registry.py`)

## PR-Vorlage (Platzhalter bleiben, bis gemessen)

```markdown
## Task
- Agent: D (Curator, ID-02)
- Task: TASK-00004
- Support: Coding Agent (Tooling)

## Coverage (Formula: indexed / accessible)
Siehe registry/inventory-summary.txt: [MEASURED_AFTER_SCAN]

## Duplikate
Siehe registry/duplicates-report.md: [MEASURED_AFTER_SCAN]

## Reproduzierbarkeit
Skript-Versionen, Aufrufe, Datum: [FILLED_FROM_RUN]

## Status
AWAITING_REVIEW, Reviewer ID-01, kein automatischer Merge
```

## Dependencies

- Keine vorgelagerten Tasks
- Blockiert: TASK-00001 (Agent A / Reference), startet erst nach Merge durch ID-01

## Signatur (erst nach realem Lauf)

```
Agent: D (ID-02)
Datum: [FILLED_AT_SUBMISSION]
Evidence: [PR-LINK]
Status: AWAITING_REVIEW
```
