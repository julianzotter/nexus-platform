---
name: cad-statik-pipeline
description: CAD/BIM-Daten (DXF, DWG, IFC, SAF-Excel, RFEM-CSV, JSON, SQLite, RF5, RF6) deterministisch in ein neutrales Statikmodell (NSM) mit Flächen und Lasten überführen, formatübergreifend vergleichen (Geometrie + Lastsummen) und als RFEM-5-Modell anlegen. Verwenden bei DXF/DWG/IFC/SAF→RFEM, Lastübertragung, Formatgleichheit prüfen, Systemlinien aus Plänen, RF6-Inventar ohne API, Modell als SQLite/CSV/JSON, Querschnitts-/Material-Zuordnung. Für reine RFEM-5-COM-Bedienung den Skill rfem5-com nutzen.
---

# CAD-Statik-Pipeline (NSM)

Stand 17.11.2026 (v1.1) · ID06 · geprüft mit Python 3.12, ezdxf 1.4.4, ifcopenshell 0.8.5, openpyxl, GNU LibreDWG 0.14, RFEM 5.29.01 (über Skill `rfem5-com`)

## Dateien (Pfad = Ordner dieser SKILL.md)

| Datei | Zweck |
|---|---|
| `references/HANDBUCH_CAD_STATIK_PIPELINE.md` | **zuerst lesen**: Formate, Eigenheiten, Rezepte, Achsen, Testsammlung, öffentliche Testdaten |
| `scripts/pipeline.py` | Kommandozeile: `inspect`, `convert [--layers REGEX]`, `compare [--2d]` (inkl. Lastvergleich ΣF / Σp·n), `learn-map`, `rf5-active` |
| `scripts/formats.py` | Leser/Schreiber: DXF (RFEM-Export + generisch + Umriss-Modus + Layerfilter), IFC (SAV inkl. Lasten/freie Linien + physisch), SAF-Excel, RF5 (COM, inkl. Flächen + Lasten lesen/schreiben), RF6 (Inventar), RFEM-CSV, DWG (GNU LibreDWG) |
| `scripts/nsm.py` | neutrales Modell (Knoten, Stäbe, Lager, Flächen, Lasten), JSON/CSV/SQLite, `validate()`, `fingerprint()` |
| `scripts/testkorpus.py` · `references/testkorpus.json` | Testsammlung K01–K11 mit Prüfsummen und Ergebnissen (JSON nur lokal, enthält Kundenpfade) |
| `templates/` | Pratt-Fachwerk als NSM-JSON, CSV, SQLite, DXF; `mapping_vorlage.json` |
| `tests/test_offline.py` | 12 Offline-Tests (ohne RFEM) |

## Kernablauf
```bash
python scripts/pipeline.py convert <quelle> a.nsm.json      # jede Quelle → NSM
python scripts/pipeline.py compare a.nsm.json b.nsm.json     # PASS / ABWEICHUNG, nummerierungsunabhängig
python scripts/pipeline.py convert a.nsm.json "…\SANDBOX\neu.rf5" --map mapping.json   # G2, nur SANDBOX
```

## Regeln (aus Live-Tests abgeleitet)
- **Achsen:** RFEM-System (Z nach unten) ↔ Welt/IFC (Z nach oben) = **Drehung 180° um X** `(x,y,z)→(x,−y,−z)`, keine Spiegelung nur von z. `compare` erkennt das automatisch.
- **RFEM-DXF:** Knoten sind 12-Kanten-Würfel auf `DL_NODES`; nur vollständige Würfel zählen. Querschnitt/Material stehen im Layernamen `Querschnitt$Material`.
- **RFEM-IFC:** Knoten-ID aus dem Namen („Free node 12“); Profilnamen weichen von RFEM ab → `learn-map` nur aus PASS-Vergleich.
- **RF5** immer als Kopie lesen; schreiben nur in neue Modelle unter `SANDBOX`.
- **RF6** = ZIP + SQLite: nur Inventar, keine Geometrie aus der undokumentierten Datenbank.
- **Plan-DXF** enthält oft Umrisse: Umriss-Modus (Rechteck → Mittellinie, Umriss mit max. Seite ≤ 1,0 m → Stützenpunkt), Vergleich mit `--2d`.
- **DWG:** über GNU LibreDWG `dwg2dxf` (GPL-3, nur Test; Pfad `C:\zotter_ai\tools\libredwg-0.14\extracted\` oder `NSM_DWG2DXF`); große Pläne immer mit `--layers` filtern.
- **Lasten:** nur gleichmäßige globale Kräfte (Knoten/Stab/Linie/Fläche) und Stab-Teillasten werden übertragen; alles andere wird gemeldet. Lastvektoren drehen wie die Geometrie. Lastfälle werden über die Nummer zugeordnet; Vergleich über ΣF und Σp·n (0,1 %).
- **Flächen:** eben, konstante Dicke, geordneter Außenrand; Linienlasten aus IFC brauchen freie Linien (werden mitgeschrieben).
- **SAF-Excel:** nur Einträge im System „Global“; kN → N; Nulllängen-Stäbe und koordinatengleiche Knoten werden als Befund gemeldet (Beispiel K10).
- Befunde nie unterdrücken (`validate()`, `extra.hinweise`, Schreib-Befunde); Zuordnungen von Querschnitt/Material sind G2-Entscheidungen.
- Kundendaten (z. B. `D:\RFEM\EIS_*`) bleiben lokal, nie in Git.
