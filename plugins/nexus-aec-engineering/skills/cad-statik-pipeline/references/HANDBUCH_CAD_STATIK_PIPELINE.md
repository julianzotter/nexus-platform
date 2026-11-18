# Benutzerhandbuch – CAD-Statik-Pipeline (DXF/IFC/CSV/JSON/SQLite/RF5/RF6 ↔ RFEM)

| | |
|---|---|
| Version | 1.1 · 17.11.2026 · ID06 (Claude Code) – 1.1: Flächen + Lasten (IFC/RF5/SAF), SAF-Leser, DWG über GNU LibreDWG, Layerfilter, Teillasten, Lastvergleich, K09–K11 |
| Zweck | CAD- und BIM-Daten deterministisch in ein **neutrales Statikmodell (NSM)** überführen, gegeneinander prüfen und als RFEM-Modell anlegen – nachvollziehbar, mit Prüfsummen und Befunden |
| Prüfstatus | 12 Offline-Tests PASS · Testsammlung K01–K11 live geprüft (10 PASS, K10 erwartete Abweichung durch Quelldatenfehler), siehe Kap. 8 |
| Ablage | SSOT `G:\Meine Ablage\_developement\LLM-LOCAL-SSOT\NEXUS.CAD.SKILLS\cad-statik-pipeline\` · installiert `%USERPROFILE%\.claude\skills\cad-statik-pipeline\` |
| Abhängig | Python 3.12 · `ezdxf` · `ifcopenshell` · `numpy` · für RF5: Skill `rfem5-com` (comtypes, laufendes RFEM 5) |

## Inhalt
1. Prinzip · 2. Das neutrale Modell (NSM) · 3. Formate und Datendarstellungen · 4. Kommandos · 5. Rezepte · 6. Koordinaten und Einheiten · 7. Namenszuordnung Querschnitt/Material · 8. Testsammlung · 9. Öffentliche Testdaten · 10. Grenzen und Befunde · 11. Freigabestufen · 12. Lasten und Lastvergleich · 13. Datenqualitäts-Befunde

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
| `surfaces` | `id`, `nodes` (geordneter Außenrand), `thickness` [m], `material` | IFC: Kantenzug; RF5: verkettete Randlinien; nach RF5 als ebene Fläche mit konstanter Dicke |
| `loads` | `cases` [`id`, `name`, `category`, `self_weight`]; `items` [`case`, `kind` nodal/member/line/surface, `targets`, `dir` X/Y/Z/PX/PY/PZ/MX/MY/MZ, `value`, `dist` uniform/partial, `a`/`b` Teillast [m], `line_nodes`] | SI (N, Nm, N/m, N/m²); je Richtung ein Eintrag wie in RFEM; globales System der Quelle |
| `extra` | Inventare, Hinweise, RFEM-Bibliotheks-IDs | formatspezifisch |

`Model.validate()` meldet: doppelte Knotennummern, ungültige Koordinaten, Stäbe ohne Knoten, Nulllängen, Lager ohne Knoten, `INFO_FREIE_KNOTEN` (z. B. Flächenknoten).
`Model.fingerprint()` = SHA-256 über sortierte Knoten und Stäbe → Regressionsvergleich zwischen Läufen.

## 3. Formate und Datendarstellungen

| Format | Lesen | Schreiben | Technik | Was übertragen wird | Wichtige Eigenheit (geprüft) |
|---|---|---|---|---|---|
| **DXF – RFEM-Export** | ✓ | ✓ | ezdxf | Knoten, Stäbe, Querschnitt+Material aus Layername | Knoten = **Würfel aus 12 Kanten** (Kante 0,2 m) auf `DL_NODES`; nur vollständige Würfel zählen (sonst Scheinwürfel zwischen Nachbarn); Stäbe als LINE auf Layer `Querschnitt$Material`, `/` als `(SLASH)`; Koordinaten im **RFEM-Modellsystem** |
| **DXF – generisch** | ✓ | – | ezdxf | Linien/Polylinien = Stabachsen, Layer = Querschnitt | `$INSUNITS` wird in Meter umgerechnet; **Umriss-Modus:** Layer aus lauter Rechtecken → Mittellinie, Quadrate → Stützenpunkt; Zeichnungslayer (Bemaßung, Text, Schraffur, Achsen, `SECTION`) werden ignoriert |
| **DWG** | ✓ | – | **GNU LibreDWG 0.14** `dwg2dxf` (GPL-3, nur Test) → DXF | wie DXF | Konverter unter `C:\zotter_ai\tools\libredwg-0.14\extracted\` (oder Umgebungsvariable `NSM_DWG2DXF`); AC1032 geprüft; große Pläne mit `--layers` filtern |
| **SAF (Excel)** | ✓ | – | openpyxl | Knoten, Stäbe (inkl. Rippen), Flächen, Punktlager, Lastfälle, Punkt-/Linien-/Flächenlasten (global) | kN → N; Koordinatensystem „Global“/„Local“; Stäbe mit Zwischenknoten werden gemeldet |
| **IFC – Statikmodell (SAV)** | ✓ | – | ifcopenshell | `IfcStructuralPointConnection` → Knoten (ID aus Name), `IfcStructuralCurveMember` → Stäbe, `IfcStructuralSurfaceMember` → Flächen, `IfcBoundaryNodeCondition` → Lager, Profil/Material aus Relationen, **Lastgruppen (LOAD_CASE) mit Punkt-/Linien-/Flächeneinwirkungen**, freie Linien (`IfcStructuralCurveConnection`) für Linienlasten | RFEM-IFC: Rohkoordinaten im RFEM-System, Platzierungsmatrix = **Drehung 180° um X** → Weltkoordinaten Z nach oben; IFC2X3 kennt `IfcStructuralCurveAction` nicht (dort `IfcStructuralLinearAction`); Lastvektoren mit derselben Platzierungsdrehung transformiert; Kraft-/Längeneinheiten (z. B. lbf, inch) umgerechnet; IFC4 `IfcStructuralLoadConfiguration` → Teillast |
| **IFC – physisch** | ✓ | – | ifcopenshell + numpy | IfcBeam/IfcColumn/IfcMember → Achse | `Axis`-Darstellung bevorzugt; sonst **Achse aus Extrusionsquader** (Rechteck/Kreis, längste Kante) – als Näherung markiert |
| **RF5** | ✓ | ✓ | COM (Skill `rfem5-com`) | Knoten, Linien, Stäbe (Typ), Querschnitte, Materialien (inkl. Bibliotheks-TextID), Knotenlager, Flächen, **Lastfälle + Knoten-/Stab-/Linien-/Flächenlasten** (gleichmäßig, global/projiziert; Stab-Teillast als Trapez) | Lesen öffnet eine **Kopie** in `%TEMP%\NSM_SANDBOX` und schließt sie; Schreiben legt ein **neues** Modell an (nur `SANDBOX`), Achsdrehung automatisch |
| **RF6** | Inventar | – | ZIP + SQLite (ohne API) | Zählungen (Knoten, Linien, Stäbe, Flächen, Lager, Lastfälle), Versionsstempel | `.rf6` = ZIP mit `model.db` (SQLite, >3.000 Tabellen, Schema undokumentiert), XML, `preview.glb` – **nur** Inventar/Fingerabdruck; Geometrie über dlubal.api, IFC- oder SAF-Export |
| **RFEM-CSV-Tabellenexport** | ✓ | – | csv (cp1252) | `1.1 Knoten`, `1.2 Linien`, `1.3 Materialien`, `1.13 Querschnitte`, `1.17 Stäbe`, `1.7 Knotenlager` | 2 Kopfzeilen, leere Nummernzeilen werden gefiltert, Lager `+` = fest; Koordinaten auf 3 Nachkommastellen gerundet |
| **NSM-JSON** | ✓ | ✓ | json | alles | Austausch, Archiv, Agenten |
| **NSM-CSV** | ✓ | ✓ | csv (UTF-8, `;`) | Knoten, Stäbe, Lager + `meta.json` | Excel-tauglich |
| **NSM-SQLite** | ✓ | ✓ | sqlite3 | Tabellen + View `member_geometry` (inkl. Stablänge) | SQL-Abfragen, Dashboards, Agenten |

## 4. Kommandos (`scripts/pipeline.py`)

```bash
python pipeline.py inspect  <quelle> [--layers REGEX]                 # Zusammenfassung, Befunde, Fingerabdruck
python pipeline.py convert  <quelle> <ziel.json|ziel.sqlite|ziel.dxf|ordner/|ziel.rf5> [--map mapping.json] [--layers REGEX]
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

**G · DWG-Stützenplan → Stützenpunkte**
```bash
python pipeline.py convert plan.dwg stuetzen.nsm.json --layers "^0SP_S_"     # Umrisse ≤ 1,0 m → Punkte
```

**H · SAF → RF5 mit Lasten, Rückprüfung**
```bash
python pipeline.py convert modell.xlsx saf.nsm.json
python pipeline.py convert saf.nsm.json "D:\…\SANDBOX\saf.rf5" --map mapping.json
python pipeline.py convert "D:\…\SANDBOX\saf.rf5" rueck.nsm.json
python pipeline.py compare saf.nsm.json rueck.nsm.json                       # inkl. Lastvergleich je Lastfall
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
| K01 | EIS26 BETONBAU – DXF ↔ IFC ↔ RF5 (1.519 Knoten, 376 Stäbe, 245 Flächen) | **3× PASS**, max. 6 µm; IFC ↔ RF5 zusätzlich 8/8 Lastfälle gleich |
| K02 | IFC → NSM → neues RF5 **mit Flächen und Lasten** → Rücklesen | **PASS**: 245/245 Flächen, 8/8 Lastfälle (ΣF, Σp·n 0,0 %), 9 freie Linien |
| K03 | Böblingen 5e – RFEM-CSV ↔ RF5 (86 Knoten, 88 Stäbe, 35 Lager) | **PASS**, max. 0,49 mm (CSV-Rundung) |
| K04 | Plan-DXF (Umrisse, mm) ↔ IFC4 physisch – 6 Träger | **PASS (2D)** |
| K05 | Plan-DXF ↔ IFC4 physisch – 3 Stützen | **PASS (2D)** |
| K06 | RF6 ohne API – `04_Tensioned_beam.rf6`, `CTR001.rf6` | Inventar **PASS** |
| K07 | DWG AC1032 → DXF (LibreDWG 0.14) | **PASS** (0 Prüffehler, mm → m) |
| K08 | Synthetisches Pratt-Fachwerk | 12 Offline-Tests **PASS** |
| K09 | buildingSMART IFC4X3 (Zoll/lbf, Teillast) → RF5 → Rücklesen | **PASS** (−17.512,7 N/m auf 2,438–4,877 m = −42,7 kN) |
| K10 | SAF 2.2.0 Haus → RF5 → Rücklesen | Lasten 3/3, Flächen 11/11 gleich; **erwartete Abweichung**: Stab 45 mit Nulllänge, Knoten 84 koordinatengleich (Quelldatei) |
| K11 | DWG-Stützenplan, Layerfilter `^0SP_S_` | **PASS**: 113 Stützenpunkte |

K01, K02, K07, K11 sind Kundendaten: nur lokal (`D:\RFEM`, Ergebnisse in `D:\RFEM_SANDBOX_CAD`), nicht auf GitHub.

**Gefundene Fehlerquellen beim Aufbau (alle behoben, als Regel festgehalten):** Würfel dicht benachbarter Knoten berühren sich (Union-Find zieht zusammen) · Scheinwürfel aus 7/12 Kanten · Kantenlängen 0,20001 m durch Rundung · Achsumrechnung als Drehung statt Spiegelung · IFC2X3-Entitäten fehlen · Plan-DXF enthält Umrisse statt Systemlinien · Schnittmarkierungs-Layer.

## 9. Öffentliche Testdaten

**Geladen** am 17.11.2026 nach `D:\RFEM_SANDBOX_CAD\OEFFENTLICH\`, nur Testzweck:

| Datei | Quelle | Lizenz | SHA-256 (16) | Fall |
|---|---|---|---|---|
| `structural-curve-member.ifc` (15.275 B) | github.com/buildingSMART/IFC4.x-specification-models | laut Repo CC BY-ND 4.0 → unverändert verwenden | `9ccd7cc699cddf11` | K09 |
| `SAF_example_HOUSE_metric_ZYX_220.xlsx` (133.350 B) | github.com/StructuralAnalysisFormat/StructuralAnalysisFormat-Examples | keine formale Lizenz → nur intern | `5b0f8271edfcad66` | K10 |
| `libredwg-0.14-win64.zip` (12.084.779 B) | github.com/LibreDWG/libredwg, Release 0.14 | GPL-3 (externes Werkzeug), Signatur vorhanden, Schlüssel nicht importiert | `1ad7e15344d20b34` | K07, K11 |

**Weitere Kandidaten** (nicht geladen): IfcOpenShell/analysis-models (ohne Lizenz – nur intern), Frame3DD (GPL-3, Referenzausgaben), PyNite `Testing/` (MIT, Lehrbuchwerte), ezdxf `examples_dxf/` (MIT), Dlubal-Verifikationsbeispiele (proprietär). Lücke: kein frei lizenziertes IFC2X3-Statikmodell – eigener RFEM-Export (K01) ist dafür die beste Quelle.

## 10. Grenzen und Befunde

- Flächen: eben, konstante Dicke; **Öffnungen, gekrümmte Ränder, Flächen-Regionen** werden nicht übertragen.
- Lasten: nur **gleichmäßige** Kräfte im **globalen** System (auch projiziert) sowie Stab-Teillasten. Lokale Lastachsen, veränderliche bzw. hydrostatische Lasten (RFEM „Linear Z“), Temperatur, Vorspannung und Stabmomente werden **gemeldet, nicht übertragen**.
- Eigengewicht: RF5 → RF5 übernimmt den Schalter; aus IFC/SAF nicht ableitbar → in RFEM prüfen.
- Lager sind im RFEM-DXF nicht kodiert; Federlager werden nicht als „fest“ gewertet; SAF-Linien-/Flächenlager nicht übertragen.
- RF6: nur Inventar; Geometrie über die RFEM-6-API (derzeit gesperrt, siehe rfem5-com Kap. 16) oder über den IFC-Export.
- Achse aus Volumenkörper = Näherung; Umriss ≤ 1,0 m = Stützenpunkt (der Querschnittsname geht dabei verloren).

## 11. Freigabestufen (wie rfem5-com / rfem6-mcp-engineering)

| Stufe | Hier |
|---|---|
| G0 | `inspect`, `compare`, `convert` nach JSON/CSV/SQLite/DXF, RF5 lesen (Kopie), RF6-Inventar |
| G1 | – (Werte im Bestand ändern: Skill `rfem5-com`, Beispiel bsp03) |
| G2 | `convert … .rf5` = neues Modell mit Topologie, Querschnitts-/Materialzuordnung → **Entscheidung Tragwerksplaner** |
| G3/G4 | nie automatisch; `FINAL_RELEASE = HUMAN_SIGNOFF_REQUIRED` |

## 12. Lasten und Lastvergleich

`compare` ordnet Lastfälle über die Nummer im Namen zu (`LF3` ↔ `LC3`) und vergleicht je Lastfall zwei **geometrieunabhängige** Kennwerte (Toleranz 0,1 %):
- **ΣF** [kN] = Σ Knotenkräfte + Σ q·L (Stab-, Linien- und Teillasten),
- **Σp·n** [kN/m²] = Σ Flächenlast × Anzahl Zielflächen, unabhängig davon, wie die Flächenränder unterteilt sind.

Zwischen RFEM-System und Welt werden die Lastvektoren wie die Geometrie gedreht (y, z negiert). Unterschiedliche Randunterteilung (IFC teilt Ränder an jedem Knoten, RFEM speichert durchgehende Linien) wird bei der Flächenzuordnung über Knoten-Teilmengen berücksichtigt.

## 13. Datenqualitäts-Befunde (aus den Tests)

| Befund | Bedeutung | gefunden in |
|---|---|---|
| `DOPPELTE_KOORDINATEN:a=b` | zwei Knoten an derselben Stelle – RFEM fasst sie zusammen | SAF-Beispiel (Knoten 84) |
| `STAB_NULLLAENGE` | Anfangs- = Endknoten – wird beim Schreiben übersprungen | SAF-Beispiel (Stab 45) |
| „…-Last ohne Objekt“ | Last mit leerer Objektliste (Altlast nach gelöschten Objekten) – wird nicht übertragen; RFEM exportiert sie auch nicht nach IFC | EIS26-RF5: 1.458 Flächen-, 53 Stab-, 9 Knotenlasten |
| `FLAECHENDICKE_PLATZHALTER` | Quelle ohne Dicke | – |
| `LASTEN_NICHT_UEBERTRAGEN` | Lastart außerhalb des Umfangs (Kap. 10) | EIS26 LF12 Wasserdruck (Linear Z, lokal) |
