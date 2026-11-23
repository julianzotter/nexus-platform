# QA und Geltungsbereich

Maßgeblicher maschinenlesbarer Nachweis: `qa/report.json`, vollständige
Einzeltests: `qa/pytest.xml`, Werkzeugausgaben: `qa/*.log`.

Die Prüfungen werden tatsächlich mit Python ausgeführt. Die abgenommene Eigenschaft
ist das dokumentierte Softwareverhalten dieses Pakets in der beobachteten Umgebung.
Es handelt sich nicht um einen numerischen, normativen oder projektspezifischen Nachweis.

## Ausgeführte Prüfgruppen

| Gruppe | Geprüftes Verhalten |
| --- | --- |
| Contracts | Tatsächliche Literal-/Typprüfung; endliche Decimal-Werte; unveränderliche verschachtelte Daten; Referenz-/ID-Prüfung; Frames; Referenzzustände; Analysegraph |
| Capabilities | Knotenlastfälle; Eigengewicht ohne explizite Last; Zustände ohne Last; gemeinsam erforderliche Lastarten; alternative Profile; doppelte Profile; gedrehte Lager |
| Results | Modellhash/-identität; vollständige Zustands-/Objekt-/Stationszuordnung; Einheiten/Achsen; Duplikate; Partial-/Fehlergate; eindeutige Fixture-Kennzeichnung |
| Serialization | Sieben generierte Schemata; vollständige synthetische Fixtures; Rundlauf; unbekannte Felder; doppelte JSON-Schlüssel; Float-/NaN-Ablehnung; Schema- und Domain-Prüfebenen |
| Hashing | Decimal-Repräsentationen; negative Null; Revisionsbindung; bedeutungserhaltende JSON-Formatierung; bewusst reihenfolgeabhängiger Inhaltssnapshot |
| Checks | Getrennte Norm-/NA-Ausgaben; vollständige Evidenzreferenzen; not_evaluated-Beispiel |
| Architecture | Echter Import-Linter: sauberes Paket sowie isoliert injizierte verbotene Importkanten; zusätzlicher statischer Importzyklentest |
| Typprüfung | `mypy --strict` für den gesamten Produktionsquellcode; Protocol-Verwendung durch die Application |
| Smoke | Python-Kompilierung und Fixture-Replay-Demo |

## Fixture-only

`examples/results_fixture.json` enthält bewusst vorgegebene Nullwerte, keine
berechneten Tragwerksantworten. Sie belegen ausschließlich Zuordnung und
Transport. Dass sie nicht zum belasteten Modell passen müssen, ist gerade der
Grund, `execution_kind=fixture_only` stets vom Bemessungsgate auszuschließen.
Der Adapter kann keine echten Solverfähigkeiten behaupten und führt keine
Calculate-/COM-/gRPC-Aufrufe aus.

`require_design_ready` prüft notwendige Bedingungen: kein Fixture und keine
teilweisen/fehlgeschlagenen Ergebnisse. Es ist kein ausreichendes
Ingenieurfreigabegate. Gleichgewicht, Modellstabilität, Netzkonvergenz,
Bemessungsregel und unabhängige Referenzwerte sind zusätzlich erforderlich.

## Reproduzieren

```bash
python -m pip install -e . -r requirements-qa.txt
python tools/export_schemas.py
python tools/create_examples.py
python tools/run_qa.py
```

Direkter Linter-Aufruf nach Installation: `lint-imports --no-cache`.
Die Architekturtests führen dasselbe installierte CLI-Entrypoint-Verhalten aus
und prüfen zusätzlich den Fehler-Exitcode. Ein bloßes Python-Aufrufen einer
Funktion ohne Weitergabe ihres Rückgabecodes ist kein belastbares CI-Gate.

Die mitgelieferte GitHub-Actions-Datei ist vorbereitet, aber hier nicht auf GitHub
ausgeführt. Lokal beobachtete Python-/Plattform-/Paketversionen stehen im Report.
Die optionale CI-Matrix 3.11/3.12 ist kein Nachweis beider Laufzeitumgebungen.

## Offene Abnahmen

- Unabhängiges Review der Vertragssemantik und des Codes.
- Tests in weiteren Zielumgebungen, insbesondere Windows und gewählter Python-Version.
- Echte Herstelleradapter mit eigener Capability-/Lizenz-/Versionsprüfung.
- Numerische Referenzfälle einschließlich nichtlinearer Fälle und Ergebnisvorzeichen.
- Fachregeln, Normausgaben/nationale Anhänge und menschliche technische Freigabe.
- Vollständiger Dependency-Lock mit Hashes für eine spätere Produktionslieferung;
  `requirements-qa.txt` pinnt hier die direkt verwendeten QA-Werkzeuge.
