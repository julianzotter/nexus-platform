---
name: cad-statik-pipeline
description: CAD/BIM-Daten (DXF, DWG, IFC, RFEM-CSV, JSON, SQLite, RF5, RF6) deterministisch in ein neutrales Statikmodell (NSM) überführen, formatübergreifend vergleichen und als RFEM-5-Modell anlegen. Verwenden bei DXF/IFC→RFEM, Formatgleichheit prüfen, Systemlinien aus Plänen, RF6-Inventar ohne API, Modell als SQLite/CSV/JSON, Querschnitts-/Material-Zuordnung. Für reine RFEM-5-COM-Bedienung den Skill rfem5-com nutzen.
---

# CAD-Statik-Pipeline (NSM)

Stand 17.11.2026 · ID06 · geprüft mit Python 3.12, ezdxf 1.4.4, ifcopenshell 0.8.5, RFEM 5.29.01 (über Skill `rfem5-com`)

## Dateien (Pfad = Ordner dieser SKILL.md)

| Datei | Zweck |
|---|---|
| `references/HANDBUCH_CAD_STATIK_PIPELINE.md` | **zuerst lesen**: Formate, Eigenheiten, Rezepte, Achsen, Testsammlung, öffentliche Testdaten |
| `scripts/pipeline.py` | Kommandozeile: `inspect`, `convert`, `compare [--2d]`, `learn-map`, `rf5-active` |
| `scripts/formats.py` | Leser/Schreiber: DXF (RFEM-Export + generisch + Umriss-Modus), IFC (SAV + physisch), RF5 (COM), RF6 (Inventar), RFEM-CSV, DWG (Konverter) |
| `scripts/nsm.py` | neutrales Modell, JSON/CSV/SQLite, `validate()`, `fingerprint()` |
| `scripts/testkorpus.py` · `references/testkorpus.json` | Testsammlung K01–K08 mit Prüfsummen und Ergebnissen |
| `templates/` | Pratt-Fachwerk als NSM-JSON, CSV, SQLite, DXF; `mapping_vorlage.json` |
| `tests/test_offline.py` | 8 Offline-Tests (ohne RFEM) |

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
- **Plan-DXF** enthält oft Umrisse: Umriss-Modus (Rechteck → Mittellinie, Quadrat → Stützenpunkt), Vergleich mit `--2d`.
- Befunde nie unterdrücken (`validate()`, `extra.hinweise`, Schreib-Befunde); Zuordnungen von Querschnitt/Material sind G2-Entscheidungen.
- Kundendaten (z. B. `D:\RFEM\EIS_*`) bleiben lokal, nie in Git.
