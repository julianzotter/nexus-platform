# Benutzerhandbuch – CAD-Statik-Pipeline (DXF/IFC/CSV/JSON/SQLite/RF5/RF6 ↔ RFEM)

| | |
|---|---|
| Version | 1.0 · 17.11.2026 · ID06 (Claude Code) |
| Zweck | CAD- und BIM-Daten deterministisch in ein **neutrales Statikmodell (NSM)** überführen, gegeneinander prüfen und als RFEM-Modell anlegen – nachvollziehbar, mit Prüfsummen und Befunden |
| Prüfstatus | 8 Offline-Tests PASS · Testsammlung K01–K08 live geprüft (7 PASS, 1 erwartet blockiert), siehe Kap. 8 |
| Ablage | SSOT `G:\Meine Ablage\_developement\LLM-LOCAL-SSOT\NEXUS.CAD.SKILLS\cad-statik-pipeline\` · installiert `%USERPROFILE%\.claude\skills\cad-statik-pipeline\` |
| Abhängig | Python 3.12 · `ezdxf` · `ifcopenshell` · `numpy` · für RF5: Skill `rfem5-com` (comtypes, laufendes RFEM 5) |

## Inhalt
1. Prinzip · 2. Das neutrale Modell (NSM) · 3. Formate und Datendarstellungen · 4. Kommandos · 5. Rezepte · 6. Koordinaten und Einheiten · 7. Namenszuordnung Querschnitt/Material · 8. Testsammlung · 9. Öffentliche Testdaten · 10. Grenzen und Befunde · 11. Freigabestufen

---

## 1. Prinzip

```
 DXF ─┐                                   ┌─► JSON / CSV / SQLite (Austausch, Abfrage, Archiv)
 DWG ─┤ (Konverter)                        ├─► DXF (RFEM-kompatible Layer, Überlagerung)
 IFC ─┼─► Leser ─► NSM ─► validate() ─────┼─► RF5 (neues Modell über COM, nur SANDBOX, Stufe G2)
 CSV ─┤                     │              └─► compare(): Formatgleichheit / Regressionsprüfung
 RF5 ─┤ (COM, Kopie)        └─ fingerprint() (SHA-256 über Geometrie + Topologie)
 RF6 ─┘ (Inventar)
```

- **Ein Modell, viele Formate:** Jeder Leser liefert dasselbe NSM; jeder Schreiber nimmt ein NSM.
- **Deterministisch:** feste Toleranzen, sortierte Ausgabe, gleiche Eingabe → gleicher Fingerabdruck.
- **Keine stillen Korrekturen:** Unsicherheiten landen als Hinweis in `extra.hinweise`, Strukturfehler in `validate()`.
- **Originale bleiben unberührt:** RF5 wird immer als Kopie geöffnet; RF5 geschrieben wird nur in Ordner mit `SANDBOX`.

## 2. Das neutrale Modell (NSM v0.1)

Datei `scripts/nsm.py`, Beispiel `templates/beispiel_fachwerk.nsm.json`.

| Teil | Felder | Hinweis |
|---|---|---|
| `meta` | `schema`, `source`, `source_sha256`, `format`, `units` (m, N, Nm), `z_axis` (`up`/`down`/`unbekannt`), `created`, formatspezifisch | Herkunft immer mit Prüfsumme |
| `nodes` | `id`, `x`, `y`, `z` [m] | auf 1 µm gerundet |
| `members` | `id`, `n1`, `n2`, `section`, `material`, `type` (`beam`, `cable`, `truss` …) | Querschnitt/Material als Name der Quelle |
| `supports` | `node`, `fix` | `fix` = feste Freiheitsgrade: `x y z` (Verschiebung), `X Y Z` (Verdrehung) |
| `surfaces` | `id`, `nodes`, `thickness`, `material` | Flächen derzeit nur gelesen, nicht nach RF5 geschrieben |
| `extra` | Inventare, Hinweise, RFEM-Bibliotheks-IDs | formatspezifisch |

`Model.validate()` meldet: doppelte Knotennummern, ungültige Koordinaten, Stäbe ohne Knoten, Nulllängen, Lager ohne Knoten, `INFO_FREIE_KNOTEN` (z. B. Flächenknoten).
`Model.fingerprint()` = SHA-256 über sortierte Knoten und Stäbe → Regressionsvergleich zwischen Läufen.

## 3. Formate und Datendarstellungen

| Format | Lesen | Schreiben | Technik | Was übertragen wird | Wichtige Eigenheit (geprüft) |
|---|---|---|---|---|---|
| **DXF – RFEM-Export** | ✓ | ✓ | ezdxf | Knoten, Stäbe, Querschnitt+Material aus Layername | Knoten = **Würfel aus 12 Kanten** (Kante 0,2 m) auf `DL_NODES`; nur vollständige Würfel zählen (sonst Scheinwürfel zwischen Nachbarn); Stäbe als LINE auf Layer `Querschnitt$Material`, `/` als `(SLASH)`; Koordinaten im **RFEM-Modellsystem** |
| **DXF – generisch** | ✓ | – | ezdxf | Linien/Polylinien = Stabachsen, Layer = Querschnitt | `$INSUNITS` wird in Meter umgerechnet; **Umriss-Modus:** Layer aus lauter Rechtecken → Mittellinie, Quadrate → Stützenpunkt; Zeichnungslayer (Bemaßung, Text, Schraffur, Achsen, `SECTION`) werden ignoriert |
| **DWG** | (✓) | – | externer Konverter → DXF | wie DXF | Version wird erkannt (z. B. AC1032); Konverter: ODA File Converter (ohne Mitgliedschaft nur nicht-kommerziell) oder GNU LibreDWG `dwg2dxf` (GPL-3) – derzeit **nicht installiert** |
| **IFC – Statikmodell (SAV)** | ✓ | – | ifcopenshell | `IfcStructuralPointConnection` → Knoten (ID aus Name), `IfcStructuralCurveMember` → Stäbe, `IfcStructuralSurfaceMember` → Flächen, `IfcBoundaryNodeCondition` → Lager, Profil/Material aus Relationen, Lastzählung | RFEM-IFC: Rohkoordinaten im RFEM-System, Platzierungsmatrix = **Drehung 180° um X** → Weltkoordinaten Z nach oben; IFC2X3 kennt `IfcStructuralCurveAction` nicht (dort `IfcStructuralLinearAction`) |
| **IFC – physisch** | ✓ | – | ifcopenshell + numpy | IfcBeam/IfcColumn/IfcMember → Achse | `Axis`-Darstellung bevorzugt; sonst **Achse aus Extrusionsquader** (Rechteck/Kreis, längste Kante) – als Näherung markiert |
| **RF5** | ✓ | ✓ | COM (Skill `rfem5-com`) | Knoten, Linien, Stäbe (Typ), Querschnitte, Materialien (inkl. Bibliotheks-TextID), Knotenlager, Flächen | Lesen öffnet eine **Kopie** in `%TEMP%\NSM_SANDBOX` und schließt sie; Schreiben legt ein **neues** Modell an (nur `SANDBOX`), Achsdrehung automatisch |
| **RF6** | Inventar | – | ZIP + SQLite (ohne API) | Zählungen (Knoten, Linien, Stäbe, Flächen, Lager, Lastfälle), Versionsstempel | `.rf6` = ZIP mit `model.db` (SQLite, >3.000 Tabellen, Schema undokumentiert), XML, `preview.glb` – **nur** Inventar/Fingerabdruck; Geometrie über dlubal.api, IFC- oder SAF-Export |
| **RFEM-CSV-Tabellenexport** | ✓ | – | csv (cp1252) | `1.1 Knoten`, `1.2 Linien`, `1.3 Materialien`, `1.13 Querschnitte`, `1.17 Stäbe`, `1.7 Knotenlager` | 2 Kopfzeilen, leere Nummernzeilen werden gefiltert, Lager `+` = fest; Koordinaten auf 3 Nachkommastellen gerundet |
| **NSM-JSON** | ✓ | ✓ | json | alles | Austausch, Archiv, Agenten |
| **NSM-CSV** | ✓ | ✓ | csv (UTF-8, `;`) | Knoten, Stäbe, Lager + `meta.json` | Excel-tauglich |
| **NSM-SQLite** | ✓ | ✓ | sqlite3 | Tabellen + View `member_geometry` (inkl. Stablänge) | SQL-Abfragen, Dashboards, Agenten |

## 4. Kommandos (`scripts/pipeline.py`)

```bash
python pipeline.py inspect  <quelle>                                  # Zusammenfassung, Befunde, Fingerabdruck
python pipeline.py convert  <quelle> <ziel.json|ziel.sqlite|ziel.dxf|ordner/|ziel.rf5> [--map mapping.json]
python pipeline.py compare  <A> <B> [--tol 0.005] [--2d] [--report r.md] [--json r.json]
python pipeline.py learn-map <A-quelle> <B-rf5.nsm.json> <mapping.json>  # Namenszuordnung aus PASS-Paar ableiten
python pipeline.py rf5-active <ziel.json>                             # aktives RFEM-5-Modell (nur lesen)
python testkorpus.py                                                  # Manifest der Testsammlung erneuern
```

`compare` arbeitet **nummerierungsunabhängig**: Knoten über Koordinaten (Fangradius `--tol`), Stäbe über ihr Endknotenpaar. Unterschiedliche Achssysteme werden automatisch erkannt (Drehung 180° um X). `--2d` vergleicht Grundrisse (z ignoriert). Rückgabecode 0 = PASS, 2 = ABWEICHUNG.

## 5. Rezepte

**A · Statik-IFC gegen RFEM-Modell prüfen (Formatgleichheit)**
```bash
python pipeline.py convert modell.ifc a.nsm.json
python pipeline.py convert modell.rf5 b.nsm.json         # öffnet nur eine Kopie
python pipeline.py compare a.nsm.json b.nsm.json --report vergleich.md
```

**B · IFC/DXF → neues RFEM-5-Modell (Stufe G2)**
```bash
python pipeline.py learn-map a.nsm.json b.nsm.json mapping.json          # nur aus PASS-Paar, sonst templates/mapping_vorlage.json
python pipeline.py convert a.nsm.json "D:\…\SANDBOX\neu.rf5" --map mapping.json
python pipeline.py convert "D:\…\SANDBOX\neu.rf5" rueck.nsm.json
python pipeline.py compare a.nsm.json rueck.nsm.json                     # muss PASS sein
```
Befunde des Schreibers: `MATERIAL_PLATZHALTER`, `QUERSCHNITT_PLATZHALTER` (fehlende Zuordnung), `FLAECHEN_NICHT_UEBERTRAGEN`, `ACHSEN_GEDREHT`.

**C · Plan-DXF gegen 3D-Modell (Grundriss)**
```bash
python pipeline.py convert plan.dxf plan.nsm.json        # Umriss-Modus + mm→m automatisch
python pipeline.py compare plan.nsm.json modell.nsm.json --2d --tol 0.01
```

**D · Modell als SQLite für Abfragen**
```bash
python pipeline.py convert modell.rf5 modell.sqlite
sqlite3 modell.sqlite "SELECT section, COUNT(*), ROUND(SUM(length_m),2) FROM member_geometry GROUP BY section"
```

**E · RF6-Bestand inventarisieren (ohne API-Key)**
```bash
python pipeline.py inspect modell.rf6
```

**F · Als Python-Bibliothek**
```python
import sys; sys.path.insert(0, r"…\cad-statik-pipeline\scripts")
from formats import load, write_dxf; from pipeline import compare; import nsm
m = load(r"modell.ifc"); print(m.summary(), m.validate()); nsm.to_sqlite(m, "modell.sqlite")
```

## 6. Koordinaten und Einheiten

- **RFEM-Modellsystem:** globale Z-Achse meist **nach unten** (`GetGlobalZAxisOrientation()` = 0).
- **Welt/IFC/CAD:** Z nach oben. Umrechnung = **Drehung um 180° um die X-Achse**: `(x, y, z) → (x, −y, −z)`. Das ist eine Drehung (rechtshändig), **keine Spiegelung nur von z**. Im Projekt Böblingen entsprach das der Regel „y spiegeln, z = c − Z“.
- RFEM schreibt in **DXF** die Modellkoordinaten unverändert, in **IFC** Rohkoordinaten plus Platzierungsmatrix.
- Längen intern in m; DXF über `$INSUNITS`, IFC über `IfcSIUnit` (MILLI) bzw. `IfcConversionBasedUnit` umgerechnet.

## 7. Namenszuordnung Querschnitt/Material

Quellen benennen unterschiedlich (IFC `300X1100` / `D820`, RFEM `Rechteck 300/1100` / `Kreis 820`). RFEM-Materialien brauchen eine **Bibliotheks-TextID**.
- `learn-map` leitet die Zuordnung **nur aus einem PASS-Vergleich** ab (Mehrheitsentscheid je Name, Mehrdeutigkeiten werden gemeldet) und übernimmt die TextIDs aus dem RF5-Modell.
- Vorlage: `templates/mapping_vorlage.json` (`"*"` = Platzhalter).
- Jede Zuordnung ist eine **G2-Entscheidung** des Tragwerksplaners – Platzhalter erzeugen Befunde, nie stillschweigend „richtige“ Werte.

## 8. Testsammlung (live geprüft 17.11.2026)

Manifest: `references/testkorpus.json` (Quellen, SHA-256, Ergebnisse) – neu erzeugen mit `python scripts/testkorpus.py`.

| ID | Fall | Ergebnis |
|---|---|---|
| K01 | EIS26 BETONBAU – DXF ↔ IFC ↔ RF5 (1.519 Knoten, 376 Stäbe, 245 Flächen) | **3× PASS**, max. 6 µm |
| K02 | IFC → NSM → neues RF5 → Rücklesen (mit gelernter Zuordnung) | **PASS** gegen IFC und gegen Original-RF5, Querschnittsnamen identisch |
| K03 | Böblingen 5e – RFEM-CSV ↔ RF5 (86 Knoten, 88 Stäbe, 35 Lager) | **PASS**, max. 0,49 mm (CSV-Rundung) |
| K04 | Plan-DXF (Umrisse, mm) ↔ IFC4 physisch – 6 Träger | **PASS (2D)** |
| K05 | Plan-DXF ↔ IFC4 physisch – 3 Stützen | **PASS (2D)** |
| K06 | RF6 ohne API – `04_Tensioned_beam.rf6`, `CTR001.rf6` | Inventar **PASS** |
| K07 | DWG AC1032 | erwartet **BLOCKED** (kein Konverter) |
| K08 | Synthetisches Pratt-Fachwerk | 8 Offline-Tests **PASS** |

K01, K02, K07 sind Kundendaten: nur lokal (`D:\RFEM`, Ergebnisse in `D:\RFEM_SANDBOX_CAD`), nicht auf GitHub.

**Gefundene Fehlerquellen beim Aufbau (alle behoben, als Regel festgehalten):** Würfel dicht benachbarter Knoten berühren sich (Union-Find zieht zusammen) · Scheinwürfel aus 7/12 Kanten · Kantenlängen 0,20001 m durch Rundung · Achsumrechnung als Drehung statt Spiegelung · IFC2X3-Entitäten fehlen · Plan-DXF enthält Umrisse statt Systemlinien · Schnittmarkierungs-Layer.

## 9. Öffentliche Testdaten (recherchiert, nicht heruntergeladen)

| Rang | Quelle | Lizenz | Nutzen |
|---|---|---|---|
| 1 | buildingSMART IFC4.3 Sample Models – `structural-analysis-model/structural-curve-member` | CC BY-ND 4.0 | offizielles SAV-Beispiel mit Lasten und Referenzreaktionen (Einheiten Zoll/lbf) |
| 2 | IfcOpenShell/analysis-models (`portal_01`, `cantilever_01`, …) | keine Lizenz angegeben → nur intern | IFC4 + neutrales JSON je Modell |
| 3 | SAF – Structural Analysis Format (saf.guide, Beispiel-Repo) | „offenes Format“, keine formale Lizenz | RFEM 6 importiert/exportiert SAF – zweiter Eingangspfad |
| 4 | Frame3DD-Beispiele (Pratt-Fachwerk, Rahmen) | GPL-3 | Referenzausgaben vorhanden |
| 5 | PyNite `Testing/` | MIT | Lehrbuchwerte als Sollwerte |
| 6 | ezdxf `examples_dxf/` | MIT | Parser-Grenzfälle DXF R12–R2018 |
| 7 | GNU LibreDWG `dwg2dxf` | GPL-3 (externes Werkzeug) | DWG → DXF |
| – | Dlubal-Verifikationsbeispiele (VE 0079/0080/0039/0205/0106) | proprietär | RFEM-nah, siehe rfem5-com-Handbuch Kap. 14 |

Lücke: kein frei lizenziertes **IFC2X3-SAV**-Beispiel – eigener RFEM-Export (wie K01) ist dafür die beste Quelle. RFEM 6 importiert laut Dlubal IFC 2x3/4.0/4.3 (SAV → Knoten/Stäbe/Flächen); ob Lasten mitkommen, ist offen.

## 10. Grenzen und Befunde

- Flächen werden gelesen und gezählt, aber noch **nicht** nach RF5 geschrieben (Befund `FLAECHEN_NICHT_UEBERTRAGEN`).
- Lasten: nur gezählt (IFC), nicht übertragen.
- Lager im RFEM-DXF nicht kodiert; im generischen DXF nie.
- Federlager werden nicht als „fest“ gewertet (Hinweis).
- RF6: nur Inventar; Geometrie über RFEM-6-API, sobald der Zugang freigeschaltet ist (siehe rfem5-com-Handbuch Kap. 16).
- Achse aus Volumenkörper = Näherung (Exzentrizitäten/Systemlinien prüfen).

## 11. Freigabestufen (wie rfem5-com / rfem6-mcp-engineering)

| Stufe | Hier |
|---|---|
| G0 | `inspect`, `compare`, `convert` nach JSON/CSV/SQLite/DXF, RF5 lesen (Kopie), RF6-Inventar |
| G1 | – (Werte im Bestand ändern: Skill `rfem5-com`, Beispiel bsp03) |
| G2 | `convert … .rf5` = neues Modell mit Topologie, Querschnitts-/Materialzuordnung → **Entscheidung Tragwerksplaner** |
| G3/G4 | nie automatisch; `FINAL_RELEASE = HUMAN_SIGNOFF_REQUIRED` |
