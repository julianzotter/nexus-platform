# NEXUS AEC Contracts — v0.1.0

Projektneutrales, ausführbares Referenzpaket für Ports-and-Adapters, analytische
Tragwerksdaten, Capability-Prüfung und nachvollziehbare Ergebnisübergaben.

Status: **getestete Software-Referenzimplementierung; Spezifikationskandidat**.
Keine technische Freigabe, kein implementierter Fachnachweis, keine geprüfte
Herstellerintegration. Die Beispiele sind ausschließlich synthetische Software-Testdaten.

## Inhalt

| Artefakt | Zweck |
| --- | --- |
| `src/nexus/domain/contracts/` | Unveränderliche, typisierte und zur Laufzeit validierte Verträge |
| `src/nexus/domain/services/compatibility.py` | Konservative Prüfung vollständiger Analysezustände gegen alternative Capability-Profile |
| `src/nexus/domain/services/result_validation.py` | Modellbindung, vollständige Ergebniszuordnung und notwendiges Bewertungsgate |
| `src/nexus/domain/ports/` | `SolverPort`, analytischer `ExchangePort` |
| `src/nexus/adapters/json_codec.py` | Strikter JSON-Rundlauf mit Ablehnung unbekannter Felder |
| `src/nexus/adapters/fixture_solver.py` | Ausschließlich Wiedergabe vorgegebener Testwerte |
| `schemas/` | Sieben aus denselben Python-Typen erzeugte JSON-Schemata, Draft 2020-12 |
| `examples/` | Sieben vollständig ladbare, synthetische Beispieldateien |
| `tests/` | Vertrags-, Fehlerfall-, Rundlauf-, Ergebnis- und echte Import-Linter-Tests |
| `qa/` | Tatsächlich ausgeführte Prüfungen mit Logs, JUnit und Versionsangaben |
| `docs/` | Architektur, Vertragssemantik, Grenzen, Quellen und Cross-Chat-Handoff |

## Start

Im entpackten Paketverzeichnis, Python 3.11 oder höher:

```bash
python -m venv .venv
```

Umgebung aktivieren: Linux/macOS `source .venv/bin/activate`, Windows PowerShell
`.venv\Scripts\Activate.ps1`. Danach:

```bash
python -m pip install -e . -r requirements-qa.txt
python tools/export_schemas.py
python tools/create_examples.py
python tools/run_qa.py
python -m nexus.bootstrap.demo
```

Die Demo meldet explizit `fixture replay` und führt keine statische Berechnung aus.
Nach lokaler Installation der Entwicklungsabhängigkeiten benötigt die Testsuite
weder CAD-Programme noch Solver, Cloud-Zugang oder ein Netzwerk.

## Verbindlicher Umfang dieser Implementierung

- SI-Kanon: m, N, Pa, kg, s, K, rad; Momente Nm; Linienlasten N/m.
  JSON-Dezimalwerte werden als Dezimalstrings übertragen, nie als Float.
- Knoten, Stäbe, linear-elastisch-isotrope Materialien, Querschnitte,
  starre Lager mit sechs Freiheitsgraden und expliziten Achsen.
- Typisierte Knotenkräfte/-momente, konstante Stablasten, gleichmäßige
  Temperaturänderung und Stabvorspannung; explizite Lastfälle und Analysezustände.
- Initialzustände bilden einen azyklischen Graphen. Formfindungsziele sind von
  Material-/Geometriereferenzzuständen getrennt und einem Zustand zugeordnet.
- `AnalysisResults` bindet jeden Skalar an Zustand, Objekt, gegebenenfalls
  Stabstation, Achsensystem, Vorzeichenkonvention und Einheit.
- `CheckResult` ist ein Evidenz-/Befundvertrag; er implementiert keinen EC-/AISC-Nachweis.

**Repräsentierbarkeit ist kein Solverfähigkeitsnachweis.** Die enthaltenen
Capability-Angaben gehören ausschließlich zum Fixture-Adapter. Reale Adapter für
RFEM, SOFiSTiK, BricsCAD, FreeCAD, PyNite, IFC, DXF oder Excel sind nicht enthalten.

## Lesen und weiterarbeiten

1. [Architektur und Entscheidungen](docs/ARCHITECTURE.md)
2. [Vertragssemantik und Systemgrenzen](docs/CONTRACT_SPEC.md)
3. [QA und Abnahmekriterien](docs/QA.md)
4. [Cross-Chat-Handoff](docs/CROSS_CHAT_HANDOFF.md)
5. [Quellen](docs/SOURCES.md)

Die führenden Definitionen liegen in Python. Schemata werden daraus regeneriert,
nicht unabhängig editiert. JSON Schema prüft Struktur; die Domain prüft zusätzlich
Referenzen, Einheitenzuordnung und weitere semantische Invarianten.

`MANIFEST.sha256` enthält die Prüfsummen aller ausgelieferten Dateien außer sich
selbst. Der lokale Hashprofilname `nexus-c14n/0.1` behauptet keine Kompatibilität
mit RFC 8785/JCS und keine Bedeutungsgleichheit verschieden sortierter Modelle.
