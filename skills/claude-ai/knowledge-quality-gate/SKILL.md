---
name: knowledge-quality-gate
description: "Prüft Knowledge Packages vor Registry, Retrieval oder Veröffentlichung auf Schema, Provenienz, Hash-Reproduzierbarkeit, Vollständigkeit, Duplikate, Lizenzkonformität und Regression gegen einen Gold-Datensatz. Ergebnis ist ein quality-report.json mit Status valid, warning, quarantine oder rejected."
version: '0.1.0'
status: PLANNED
timestamp: "2026-10-13"
priority: 3
depends_on:
- source-governance
- knowledge-ingestion
replaces:
- rag-eval-harness
- norm-chunk-validator
---

# knowledge-quality-gate

## Zweck
Letzte Schranke vor Registry, RAG und Veröffentlichung. Nur Pakete mit Status `valid` dürfen weiter. Berichte enthalten ausschließlich IDs, Hashes und Zähler, keine Dokumentinhalte.

## Inputs
| Input | Pflicht | Beschreibung |
|---|---|---|
| Knowledge Package | ja | Verzeichnis aus `knowledge-ingestion` |
| Governance-Entscheid | ja | gleicher Entscheid wie bei der Ingestion |
| `--target` | ja | beabsichtigtes Ziel (`local_processing`, `cloud`, `third_party`, `git`, `backup`) |
| Gold-Datensatz | nein | `tests/gold/<set>/` (siehe unten); ohne ihn wird Q07 übersprungen und im Bericht vermerkt |
| `--source` | nein | Originaldatei für Re-Ingest-Vergleich in Q03 |
| Schwellenwerte | ja | `config/quality-gates.yaml` |

## Checks
| ID | Prüfung | Fehlerfolge |
|---|---|---|
| Q01 Schema | `manifest`, `blocks`, `chunks` gegen Schemas (`docs/CONTRACTS.md`), Pflichtfelder, keine unbekannten Felder | `rejected` |
| Q02 Provenienz | jeder Chunk hat `source_hashes` und Anker; jeder referenzierte Blockhash existiert; Seiten-/Zeilenanker liegen im Dokumentbereich | `quarantine` |
| Q03 Hash-Reproduzierbarkeit | alle `block_hash`, `chunk_hash`, `root_hash` und Dateihashes neu berechnen; mit `--source` zusätzlich Re-Ingest und Vergleich | `quarantine` |
| Q04 Vollständigkeit | keine leeren Chunks; verwaiste Blöcke (in keinem Chunk) unter Schwelle; Seitenabdeckung gegenüber dem Manifest | `warning` oder `quarantine` je Schwelle |
| Q05 Duplikate | exakte Duplikate über `chunk_hash`; Beinahe-Duplikate über Shingle-Jaccard | exakt: `quarantine`; Beinahe: `warning` |
| Q06 Lizenz/Policy | Klassifikation im Paket gleich Entscheid; `--target` ist laut Entscheid erlaubt; bei `git`/`third_party` bei restricted/confidential nur Metadaten | `quarantine` |
| Q07 Regression | Gold-Abgleich (Match-Rate) und Retrieval-Recall@k gegenüber Schwellen | `warning` innerhalb der Marge, darunter `quarantine` |

## Statuslogik
1. Alle Checks laufen vollständig (kein Abbruch beim ersten Fehler), damit der Bericht alle Befunde zeigt.
2. Der schwerste Befund bestimmt den Status: `valid` < `warning` < `quarantine` < `rejected`.
3. Fehlende Provenienz, Policy-Verstoß oder nicht reproduzierbarer Hash führen **mindestens** zu `quarantine`.
4. `valid`: keine Warnung, keine Fehler. Nur `valid` wird in Registry oder RAG aufgenommen. `warning` benötigt eine dokumentierte menschliche Freigabe (`nexus release`).

## Quarantäne-Workflow
- Bei `quarantine`/`rejected` wird das Paket nach `data/quarantine/<pkg>/` verschoben (nicht gelöscht) und `quarantine.json` mit Grund und Check-IDs angelegt.
- Freigabe nur per `nexus release <pkg> --approved-by NAME --note TEXT` (Human Gate); die Freigabe wird protokolliert und im Paket vermerkt, ersetzt aber nie ein fehlgeschlagenes Q06.
- Quarantäne-Pakete werden nie in öffentliche Indizes, Git oder GitHub-Backups übernommen.

## Gold-Datensatz `tests/gold/<set>/`
```
gold_chunks.jsonl      # {doc_id, anchor, expected_text_hash | expected_text_snippet_hash}
retrieval.jsonl        # {query, expected_chunk_hashes: [...]}
negative.jsonl         # Fälle, die verworfen werden müssen (fehlende Provenienz, falsche Seite, Duplikat)
```
Gold-Daten enthalten nur Hashes und Fragen, keine lizenzierten Volltexte. Jeder Eintrag trägt `source_hash`.

## Output `quality-report.json`
```json
{
  "schema_version": "1.0",
  "package_root_hash": "<64 hex>",
  "decision_id": "gd-3f9a1c2e7b4d5a60",
  "target": "local_processing",
  "status": "quarantine",
  "checks": [
    {"check_id": "Q01", "name": "schema", "result": "pass", "severity": "blocker", "detail": "0 Fehler", "refs": []},
    {"check_id": "Q02", "name": "provenance", "result": "fail", "severity": "blocker", "detail": "3 Chunks ohne Anker", "refs": ["doc#c0004", "doc#c0005", "doc#c0009"]},
    {"check_id": "Q07", "name": "regression", "result": "skip", "severity": "minor", "detail": "kein Gold-Datensatz angegeben", "refs": []}
  ],
  "thresholds_sha256": "<64 hex>",
  "timestamp": "2026-10-13T12:00:00+02:00"
}
```
Schema: `docs/CONTRACTS.md` (`QualityReport`, `Check`). Erzeugt wird zusätzlich eine kurze Markdown-Zusammenfassung `quality-report.md` (Tabelle der Checks, ohne Inhalte).

## CLI
```
nexus validate <package-dir> --decision governance-decision.json --target <ziel>
               [--gold tests/gold/<set>] [--source <datei>] [--config config/quality-gates.yaml]
               [--no-move]
nexus release <pkg> --approved-by NAME --note TEXT
```

## Exit-Codes
| Code | Bedeutung |
|---|---|
| 0 | `valid` |
| 30 | `warning` |
| 31 | `quarantine` |
| 32 | `rejected` |
| 20 | Konfigurations- oder Eingabefehler |

CI wertet alles ungleich 0 als nicht bestanden, außer bei Negativfixtures, die absichtlich `quarantine` erwarten.

## Hard Gates
- Fehlende Provenienz, Policy-Verstoß oder abweichender Hash sperrt das Paket mindestens als `quarantine`.
- Nur `valid` gelangt in Registry oder RAG.
- Bericht ohne Dokumentinhalte (`report.include_content: false`).

## Tests
| # | Fall | Erwartung |
|---|---|---|
| G1 | Gültiges öffentliches Paket | `valid`, Exit 0 |
| G2 | Chunk ohne Anker | `quarantine` (Q02) |
| G3 | Ein Zeichen in `blocks.jsonl` geändert | `quarantine` (Q03) |
| G4 | Ungültiges Manifest (Pflichtfeld fehlt) | `rejected` (Q01) |
| G5 | Doppelter Chunk | `quarantine` (Q05 exakt) |
| G6 | Beinahe-Duplikat über Schwelle | `warning` (Q05) |
| G7 | Paket `restricted`, Ziel `third_party` | `quarantine` (Q06) |
| G8 | Match-Rate knapp unter Minimum (innerhalb Marge) | `warning` (Q07) |
| G9 | Match-Rate deutlich unter Minimum | `quarantine` (Q07) |
| G10 | `quarantine`-Paket wird ohne Freigabe in die Registry übernommen | Registry lehnt ab |
| G11 | Bericht enthält Textauszug | Test schlägt fehl (kein Inhalt erlaubt) |

## Abnahme
Policy-Verstoß, fehlende Provenienz und Hash-Abweichung blockieren die Freigabe in allen Testfällen; Negativfixtures landen zuverlässig in Quarantäne; nur `valid` kann die Registry erreichen.

## Offene Punkte
- Schwellenwerte außer den zwei aus dem Ursprungs-SKILL (Match-Rate 0,98; Recall@5 0,90) sind Startwerte und mit dem Gold-Datensatz zu kalibrieren.
- LLM-gestützte Validierung (Wächter-Prompt R1 bis R6, Delta-Loop) ist nicht Teil des MVP und folgt als Erweiterung dieses Skills.

## Log
- 2026-10-13: Vollständige Spezifikation erstellt (Status PLANNED).
