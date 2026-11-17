# Benutzerhandbuch – RFEM 5 über die COM-Schnittstelle (RF-COM 5) mit Python

| | |
|---|---|
| Version | 1.2 · 17.11.2026 · ID06 (1.1: Pfade/Sicherung, Rechenverfahren, Benchmarks, Freigabestufen, GitHub-Quellen, Selbsttest · 1.2: Schnittstellen-Landkarte RF5/RF6 live, Integrationswege, Analyse Bestandsskripte, CAD-Pipeline, Architekturprinzipien, Ordner `references/` + `scripts/`) |
| Geltungsbereich | RFEM 5.29 (64 bit), RF-COM 5, Python 3.12 (64 bit), comtypes 1.4.16 |
| Autor | J. Zotter / Claude (Skill `rfem5-com`, NEXUS.CAD.SKILLS) |
| Prüfstatus | Verbindung, Lesen, Ändern, Rechnen, Ergebnisse: **im Projekt Seilstatik Böblingen live erprobt** (Sept.–Okt. 2026). API-Namen: **automatisch aus der Typbibliothek geprüft**. Beispiele 1–4: offline gegen Typbibliothek geprüft **und live in RFEM 5.29.01 erfolgreich ausgeführt (17.11.2026)** (Kap. 9) |
| Ablage | `G:\Meine Ablage\_developement\LLM-LOCAL-SSOT\NEXUS.CAD.SKILLS\rfem5-com\` (SSOT) · installiert unter `%USERPROFILE%\.claude\skills\rfem5-com\` |

---

## Inhalt

1. Was ist RF-COM?
2. Voraussetzungen und Einrichtung
3. Erste Verbindung (Schnelltest)
4. Objektmodell – wie die Schnittstelle aufgebaut ist
5. Grundregeln jedes Skripts
6. Rezepte (Lesen, Ändern, Anlegen, Lasten, Rechnen, Ergebnisse, Speichern)
7. Einheiten, Achsen, Vorzeichen
8. Fehlerbilder und Lösungen
9. Werkzeuge und Beispiele im Skill
10. Arbeitsregeln für prüffähige Statik
11. Grenzen der Schnittstelle
12. Pfade, Programmeinstellungen, Sicherung
13. Rechenverfahren (Algorithmen) in RFEM 5
14. Benchmark- und Verifikationsbeispiele
15. Quellen und weiterführende Links
16. Schnittstellen-Landkarte RFEM 5 / RFEM 6 (live geprüft)
17. Integrationswege mit Claude (Python lokal · Claude Code · MCP)
18. Analyse der Bestandsskripte und -dokumente
19. CAD-Datenpipeline DXF/IFC → RFEM (Skill `cad-statik-pipeline`)
20. Architekturprinzipien für deterministische Skript-Workflows
21. Glossar

---

## 1. Was ist RF-COM?

RF-COM ist die programmierbare Schnittstelle von RFEM 5. RFEM registriert sich als **COM-Server** (`RFEM5.Application`). Ein externes Programm – hier Python – kann damit:

- das laufende RFEM übernehmen oder RFEM starten,
- Modelle öffnen, anlegen, speichern,
- Modelldaten (Knoten, Linien, Stäbe, Lager, Querschnitte, Materialien …) lesen und schreiben,
- Lastfälle, Lasten und Kombinationen lesen und schreiben,
- rechnen und Ergebnisse (Schnittgrößen, Lagerkräfte, Verformungen …) auslesen.

```
Python-Skript ──comtypes──► Typbibliothek RFEM5_64.dll ──COM──► RFEM64.exe (GUI läuft mit)
```

**Wichtig:** Die RFEM-5-Schnittstelle ist ein *vtable*-Interface **ohne IDispatch**. Deshalb funktioniert `win32com.client.Dispatch(...)` (pywin32) **nicht** („Schnittstelle nicht unterstützt“). Python braucht **comtypes** plus die Typbibliothek.

RFEM 6 hat eine **andere** Schnittstelle (gRPC, Paket `dlubal.api`, API-Key) – siehe Kap. 11.

---

## 2. Voraussetzungen und Einrichtung

| # | Voraussetzung | Prüfen | Hinweis |
|---|---|---|---|
| 1 | RFEM 5.29 installiert, 64 bit | `C:\Program Files\Dlubal\RFEM 5.29\RFEM64.exe` | |
| 2 | **Lizenz mit RF-COM** | Ausgabe `com_licensed` von `rfem_connect.py` bzw. `app.IsComLicensed()` | Lesen geht teils ohne, Schreiben/Rechnen braucht RF-COM |
| 3 | Typbibliothek vorhanden | `C:\Program Files\Common Files\Dlubal\RFEM5_64.dll` | Abweichender Ort: Umgebungsvariable `RFEM5_TYPELIB` |
| 4 | COM-Server registriert | Registry `HKCR\RFEM5.Application` (CLSID `{5C397AC7-A317-4EE3-887C-0416236A44B1}`) | Fehlt er: als Admin `RFEM64.exe /RegServer` |
| 5 | Python **64 bit** | `python -c "import sys;print(sys.maxsize>2**32)"` → `True` | 32-bit-Python passt nicht zur 64-bit-Typbibliothek |
| 6 | comtypes | `pip install comtypes` | **Python nicht mit `-I` starten** – `-I` blendet die Benutzer-Pakete (dort liegt comtypes) aus |

Beim ersten `GetModule(...)` erzeugt comtypes einmalig Python-Wrapper unter `…\site-packages\comtypes\gen\` (`RFEM5.py` + `_5A027F61_…_0_5_7.py`). Nach einem RFEM-Update diesen Cache löschen, damit er neu erzeugt wird.

---

## 3. Erste Verbindung (Schnelltest)

1. RFEM 5 starten, Modell öffnen.
2. In der Eingabeaufforderung:

```bash
python "%USERPROFILE%\.claude\skills\rfem5-com\scripts\rfem_connect.py"
```

Erwartete Ausgabe (Beispiel):

```
RFEM 5.29.01.161059 | C:\Program Files\Dlubal\RFEM 5.29\ | COM-Lizenz: True
offene Modelle: 1
 [0] Modell | Kn 86 St 88 Fl 0 | LF 6 LK 12 RK 3 | Ergebnisse True | G:\…\Modell.rf5
```

Optionen: `--open <pfad.rf5>` (zusätzlich öffnen), `--guard SANDBOX` (nur Pfade mit diesem Text öffnen), `--start` (RFEM starten, falls keines läuft), `--json` (maschinenlesbar).

Der Kern in 8 Zeilen:

```python
import comtypes.client as cc
R = cc.GetModule(r"C:\Program Files\Common Files\Dlubal\RFEM5_64.dll")
app = cc.GetActiveObject(R.Application, interface=R.IApplication)   # an laufendes RFEM anhängen
app.LockLicense()                                                    # Pflicht vor jedem Zugriff
try:
    m = app.GetActiveModel()
    print(app.GetVersion(), m.GetPath(), m.GetModelData().GetNodeCount())
finally:
    app.UnlockLicense()                                              # IMMER – sonst bleibt RFEM gesperrt
```

---

## 4. Objektmodell – wie die Schnittstelle aufgebaut ist

```
IApplication                       app  (GetActiveObject / CreateObject)
 ├─ LockLicense · UnlockLicense · IsComLicensed · GetVersion · Show · Close
 ├─ GetActiveModel · GetModel(i) · GetModelCount · OpenModel(pfad) · CreateModel(name)
 └─ IModel                         m
     ├─ GetName · GetPath · Save(pfad) · Close · SetDescription · GetGlobalZAxisOrientation
     ├─ GetModelData() → IModelData   Knoten, Linien, Stäbe, Lager, Querschnitte … (Get…/Set…/Delete…)
     │    └─ GetNode(nr, AtNo) → INode   GetData / SetData (Einzelobjekt)
     ├─ GetLoads()     → ILoads       Lastfälle, LK, RK, SK
     │    └─ GetLoadCase(nr, AtNo) → ILoadCase   Knoten-/Stab-/Linien-/Flächenlasten
     ├─ GetCalculation() → ICalculation   Clean, Calculate, CalculateAll, Einstellungen
     │    └─ GetResultsInFeNodes(Typ, nr) / GetResultsInRasterPoints(Typ, nr) → IResults
     ├─ GetActiveView() → IView          ShowAll, Bildausschnitt, Zwischenablage
     └─ GetModule(name)                  Zusatzmodule (RF-STAHL, RF-BETON …, eigene TLBs)
```

Die vollständige Liste (114 Interfaces, 184 Strukturen, 116 Aufzählungen mit Hilfetexten) steht in **`API_REFERENZ_RFEM5.md`** – erzeugt mit `rfem5_api_inspect.py` direkt aus der Typbibliothek. Suchen ohne RFEM:

```bash
python rfem5_api_inspect.py --find NodalSupport
```

### 4.1 Drei Arten von Objekten

| Art | Beispiel | Verhalten in Python |
|---|---|---|
| **Interface** (`I…`) | `IModelData`, `INode`, `IResults` | hat Methoden; „Zeiger“ auf ein RFEM-Objekt |
| **Struktur** (Datensatz) | `Node`, `Member`, `NodalLoad`, `MemberForces` | ctypes-Struktur mit Feldern; `R.Node()` erzeugt eine leere; Felder per `obj.Feld` |
| **Aufzählung** (Enum) | `ItemAt`, `LoadingType`, `MemberType` | ganze Zahlen; Namen direkt als `R.AtNo`, `R.LoadCombinationType`, `R.Cable` |

### 4.2 Aus der Typbibliothek gelesen – häufig gebraucht

| Aufzählung | Werte |
|---|---|
| `ItemAt` | `AtIndex=0`, `AtNo=1` (fast immer **`R.AtNo`** = über Objektnummer) |
| `LoadingType` | `LoadCaseType=1`, `LoadCombinationType=2`, `ResultCombinationType=3`, `SuperCombinationType=4` |
| `MemberType` | `Beam=1`, `Rigid=2`, `Truss=4`, `TrussOnlyN=5`, `Tension=6`, `Compression=7`, `Cable=9`, `CableOnPulleys=10`, `Spring=17`, `NullMember=18` |
| `ModelObjectType` (für `DeleteObjects`) | `NodeObject=1`, `LineObject=2`, `MaterialObject=3`, `NodalSupportObject=8`, `CrossSectionObject=12`, `MemberHingeObject=13`, `MemberObject=16` |
| `LineType` | `PolylineType=1`, `SplineType=2`, `CircleType=3`, `ArcType=4` … |
| `ActionCategoryType` | `Permanent=1`, `Imposed=3`, `SnowIce=5`, `Wind=6`, `TemperatureNonFire=7` … |
| `MemberAxesType` | `GlobalAxes=1`, `LocalMemberAxes=2`, `LocalPrincipalAxes=3` |

---

## 5. Grundregeln jedes Skripts

1. **Lizenz-Klammer:** `LockLicense()` → Arbeit → `finally: UnlockLicense()`. Ohne Lock: Fehler *„Keine Lizenz für die Verwendung dieser Klasse vorhanden“* (`-2147221230`). Ohne Unlock: RFEM-Oberfläche bleibt gesperrt (dann RFEM über Task-Manager beenden). Im Skill erledigt das `with rfem_session() as (app, R):`.
2. **Änderungs-Klammer:** Schreiben nur zwischen `PrepareModification()` und `FinishModification()`; bei Fehler `CancelModification()`. Gilt für `IModelData`, `ILoads` und `ILoadCase` jeweils getrennt.
3. **Lesen → ändern → zurückschreiben:** Datensatz holen (`GetData()`), Felder ändern, `SetData()` – nie einen Datensatz „aus dem Nichts“ überschreiben, sonst gehen nicht gesetzte Felder verloren.
4. **Nummern-Listen sind Text:** `"1,2,5-8"` (z. B. `NodeList`, `DeleteObjects`). Bereiche mit Bindestrich beim Lesen selbst auflösen.
5. **`out`-Parameter sind Rückgabewerte:** `n = d.GetNodeCount()`; Arrays kommen als Tupel/Liste von Strukturen.
6. **Nur ein Client gleichzeitig.** Keine parallelen Skripte/KI-Sitzungen auf dieselbe RFEM-Instanz.
7. **Originale nie direkt öffnen** – nur hash-geprüfte Kopien (Kap. 10).

---

## 6. Rezepte

Alle Rezepte setzen voraus:

```python
import os, sys
sys.path.insert(0, os.path.expandvars(r"%USERPROFILE%\.claude\skills\rfem5-com\scripts"))
from rfem_connect import rfem_session, find_model, to_dict, sha256
```

### 6.1 Modell finden oder öffnen

```python
with rfem_session() as (app, R):
    m = app.GetActiveModel()                                   # aktives Fenster
    m = find_model(app, r"X:\SANDBOX\kopie.rf5") or app.OpenModel(r"X:\SANDBOX\kopie.rf5")
    for i in range(app.GetModelCount()):                       # alle offenen
        print(i, app.GetModel(i).GetPath())
```

Vor jeder Änderung prüfen, dass das **richtige** Modell aktiv ist (Pfad vergleichen) – im Projekt Böblingen hat genau diese Prüfung zweimal ein falsches aktives Modell abgefangen.

### 6.2 Modelldaten lesen

```python
d = m.GetModelData()
knoten = {n.No: (n.X, n.Y, n.Z) for n in d.GetNodes()}
linien = {l.No: l.NodeList for l in d.GetLines()}
seile  = [s.No for s in d.GetMembers() if int(s.Type) == R.Cable]       # MemberType Cable = 9
lager  = [(s.No, s.NodeList, s.SupportConstantZ) for s in d.GetNodalSupports()]
json_tauglich = to_dict(list(d.GetMembers()))                            # Struktur → dict
```

Fertig als Skript: `scripts\examples\bsp01_modell_lesen.py` (alles nach JSON).

### 6.3 Knoten ändern

```python
d.PrepareModification()
try:
    ni = d.GetNode(12, R.AtNo)
    nd = ni.GetData()
    nd.Z = nd.Z + 0.10; nd.Comment = "angehoben 10 cm"
    ni.SetData(nd)
    d.FinishModification()
except Exception:
    d.CancelModification(); raise
assert abs(d.GetNode(12, R.AtNo).GetData().Z - nd.Z) < 1e-9            # zurücklesen
```

### 6.4 Objekte anlegen und löschen

```python
def struct(name, **kw):
    s = getattr(R, name)()
    for k, v in kw.items(): setattr(s, k, v)
    return s

kn = d.GetLastObjectNo(R.NodeObject) + 1          # freie Nummern statt geratener
ln = d.GetLastObjectNo(R.LineObject) + 1
st = d.GetLastObjectNo(R.MemberObject) + 1
d.PrepareModification()                              # Block 1: anlegen
try:
    d.SetNode(struct("Node", No=kn, X=0.0, Y=0.0, Z=-3.0))
    d.SetLine(struct("Line", No=ln, NodeList=f"1,{kn}", Type=R.PolylineType))
    d.SetMember(struct("Member", No=st, LineNo=ln, Type=R.Cable, StartCrossSectionNo=3, EndCrossSectionNo=3))
    # Lager: -1 = starr, 0 = frei, sonst Federsteifigkeit (N/m bzw. Nm/rad)
    d.SetNodalSupport(struct("NodalSupport", No=d.GetLastObjectNo(R.NodalSupportObject) + 1, NodeList=str(kn),
                             ReferenceSystem=R.GlobalSystemType,
                             SupportConstantX=-1.0, SupportConstantY=-1.0, SupportConstantZ=-1.0))
    d.FinishModification()
except Exception:
    d.CancelModification(); raise

d.PrepareModification()                              # Block 2: löschen (getrennt, s. u.)
try:
    d.DeleteObjects(R.MemberObject, "1006,1007")     # Reihenfolge: Stäbe → Linien → Knoten
    d.FinishModification()
except Exception:
    d.CancelModification(); raise
```

Hinweise laut Dlubal (KB 001379): Anlegen und Löschen **in getrennten** Modifikations-Blöcken; viele `Set…` in **einem** Block sind deutlich schneller; erst nach `FinishModification` sind die Daten im Modell, und innerhalb eines Blocks kann nicht gerechnet werden. Eine bereits vergebene Nummer **nicht** blind wiederverwenden – freie Nummer über `GetLastObjectNo(...) + 1` holen (oder bewusst `GetData/SetData` zum Ändern). Zahlenfelder als Gleitkommazahl angeben (`-1.0`, `3.0`); comtypes wandelt ganze Zahlen zwar um, in VBA führt das aber zu Fehlern. (Im Projekt Böblingen lief ein gemischter Block aus Ändern + Löschen + Anlegen fehlerfrei – getrennte Blöcke sind trotzdem der sichere Weg.)

Praxis-Tipp: Neues Lager am besten aus einem bestehenden kopieren (`d.GetNodalSupport(2, R.AtNo).GetData()`, dann `No`/`NodeList` ändern) – so stimmen alle übrigen Felder. Ein komplettes Modell von Grund auf: `scripts\examples\bsp04_modell_erzeugen.py` (Übersetzung des offiziellen Dlubal-Beispiels „RFEMModeller“).

### 6.5 Lastfälle und Lasten

```python
L = m.GetLoads()
for lc in L.GetLoadCases():                                  # lesen
    print(lc.Loading.No, lc.Description, int(lc.ActionCategory))
ilc = L.GetLoadCase(1, R.AtNo)
print(ilc.GetNodalLoads(), ilc.GetMemberLoads(), ilc.GetImposedNodalDeformations())

# neuer Lastfall + Knotenlast
lc = R.LoadCase(); lc.Loading.No, lc.Loading.Type = 7, R.LoadCaseType
lc.ActionCategory, lc.Description = R.Imposed, "Zusatzlast"
L.PrepareModification(); L.SetLoadCase(lc); L.FinishModification()
ilc = L.GetLoadCase(7, R.AtNo)
nl = R.NodalLoad(); nl.No, nl.NodeList = 1, "3"
nl.Component.Force.Z = 5000.0                                # N, Richtung global Z
ilc.PrepareModification(); ilc.SetNodalLoad(nl); ilc.FinishModification()
```

Lastkombinationen: `L.GetLoadCombination(nr, R.AtNo).GetLoadings()`; Ergebniskombinationen analog `GetResultCombination`.

### 6.6 Rechnen

```python
C = m.GetCalculation()
C.Clean()                                    # alte Ergebnisse löschen → echte Neuberechnung
fehler = C.CalculateAll() or []              # alle LF/LK/RK (+ Module)
# oder gezielt: C.Calculate(R.LoadCombinationType, 100)
for e in fehler:
    print(e.ErrorNo, e.Load, int(e.Type), e.Description)
print("Ergebnisse vorhanden:", m.GetLoads().HasAnyResults())
```

Ohne `Clean()` kann `CalculateAll()` gespeicherte Ergebnisse unverändert zurückgeben (2 s statt Minuten). Weitere Varianten laut Typbibliothek: `CalculateAsync…`, `CalculateBatch`, `CalculateModules`, `GenerateFeMesh`. Einstellungen: `GetSettings/SetSettings`, `GetNonlinearities`, `GetBendingTheory` (Theorie I./II./III. Ordnung), `GetPrecisionAndTolerance`.

### 6.7 Ergebnisse auslesen

```python
r = C.GetResultsInFeNodes(R.LoadCombinationType, 100)      # oder GetResultsInRasterPoints
for f in r.GetMembersInternalForces(True):                 # True = Stabachsen, False = global
    print(f.MemberNo, f.Location, f.Forces.X / 1e3, "kN")  # Forces.X = N
for s in r.GetAllNodalSupportForces(False):                # False = globales System
    print(s.NodeNo, s.Forces.X / 1e3, s.Forces.Y / 1e3, s.Forces.Z / 1e3)
for u in r.GetAllNodalDeformations():
    print(u.NodeNo, u.Displacements.Z * 1e3, "mm")
```

- **Ergebniskombinationen (RK)** liefern je Ort mehrere Zeilen (Max/Min) – Extremwerte selbst bilden; das Feld `Type` zeigt die Zeilenart.
- Gezielter: `GetMemberInternalForces(nr, R.AtNo, True)`, `GetNodalSupportForces(nr, R.AtNo, False)`, Extremwerte `GetMembersExtremeInternalForces(...)`, Übersicht `GetSummary()`.
- `GetResultsInFeNodes` = Werte in FE-Knoten; `GetResultsInRasterPoints` = in den Stab-Teilungspunkten (wie im offiziellen Beispiel).

Fertig als Skript: `scripts\examples\bsp02_ergebnisse_csv.py` (Schnittgrößen, Lagerkräfte, Verformungen → CSV für Excel).

### 6.8 Speichern

```python
m.Save(r"X:\SANDBOX\modell_WORK_20261117.rf5")   # IMMER mit Pfad – ohne Pfad Fehler
```

Vorher/nachher SHA-256 bilden (`sha256(pfad)`) und protokollieren. „Speichern unter“ in der **GUI** speichert u. U. vorher das Ausgangsmodell – Hash der Quelle danach prüfen. Gesamter sicherer Ablauf: `scripts\examples\bsp03_kopie_aendern_rechnen.py`.

---

## 7. Einheiten, Achsen, Vorzeichen

| Größe | über COM | Anzeige RFEM (typisch) |
|---|---|---|
| Länge, Koordinate, Verschiebung | m | m / mm |
| Kraft | **N** | kN |
| Moment | **Nm** | kNm |
| Linien-/Stablast | **N/m** | kN/m |
| Verdrehung | rad | mrad |
| Federsteifigkeit Lager | N/m bzw. Nm/rad; **-1 = starr**, **0 = frei** | |

- **Globale Z-Achse:** oft **nach unten** (`m.GetGlobalZAxisOrientation()`). Für Vermessungsdaten (Z nach oben, Höhe ü. NN) gilt dann `z_Modell = c − Z_NN` und in der Lage y gespiegelt – Versatz `c` nie schätzen, sondern aus Passpunkten bestimmen und gegenprüfen.
- **Stabachsen:** `Forces.X` = Normalkraft N (Zug positiv), `Forces.Y/Z` = Querkräfte, `Moments.X` = Torsion.
- Lagerkräfte: Vorzeichen laut RFEM-Konvention; im Bericht immer angeben, welches System (global/lokal). **Live-Befund Selbsttest 17.11.2026:** Σ Lagerkräfte (global, `GetAllNodalSupportForces(False)`) = **+** Σ eingeprägte Lasten (gleiches Vorzeichen), d. h. RFEM gibt die vom Tragwerk auf das Lager wirkende Kraft aus.

---

## 8. Fehlerbilder und Lösungen

| Meldung / Symptom | Ursache | Lösung |
|---|---|---|
| `Schnittstelle nicht unterstützt` (win32com) | RFEM 5 hat kein IDispatch | comtypes + Typbibliothek verwenden |
| `COMError -2147221230 „Keine Lizenz für die Verwendung dieser Klasse vorhanden“` | `LockLicense()` fehlt oder kein RF-COM | `app.LockLicense()` vor jedem Zugriff; Lizenz prüfen (`IsComLicensed`) |
| `OSError … Vorgang nicht verfügbar` bei `GetActiveObject` | RFEM läuft nicht / COM-Server nicht registriert | RFEM starten bzw. `--start`; als Admin `RFEM64.exe /RegServer` |
| `ModuleNotFoundError: comtypes` | Python mit `-I` gestartet oder anderes Python | ohne `-I` starten; `python -m pip install comtypes` im richtigen Python |
| `AttributeError: GetNameAndPath` | Methode existiert nicht (geraten) | Namen nie raten: `rfem5_api_inspect.py --find …` |
| `AttributeError: GetNodalDeformations` auf `ILoadCase` | heißt dort `GetImposedNodalDeformations` | wie links; `GetNodalDeformations` gibt es nur auf `IResults` |
| RFEM-Oberfläche reagiert nicht mehr | Skript abgebrochen ohne `UnlockLicense` | immer `try/finally` bzw. `rfem_session()`; notfalls RFEM beenden |
| `CalculateAll` fertig in ~2 s, Ergebnisse unverändert | alte Ergebnisse gespeichert | vorher `C.Clean()` |
| Fehler bei `m.Save()` | Pfad fehlt | `m.Save(vollständiger_pfad)` |
| Falsches Modell geändert | `GetActiveModel()` ≠ erwartete Datei | Pfad prüfen, sonst Abbruch (siehe 6.1) |
| `GetNodes()`/`GetLines()` liefern nur einen Teil der Objekte | Auswahlmodus `EnableSelections(True)` ist noch aktiv | danach `EnableSelections(False)`; `SelectObjects(typ, "")` leert die Auswahl (Dlubal KB 001441, FAQ 004715) |
| Fehler bei `CreateModel`/`Save` in neuen Ordner | Zielordner existiert nicht | Ordner vorher anlegen (`os.makedirs`) (FAQ 004499) |
| Querschnittswerte aus der Bibliothek fehlen | liegen in der älteren Typbibliothek v3.4 | zusätzlich `cc.GetModule(r"C:\Program Files\Common Files\Dlubal\RFEM3_64.tlb")` (KB 001559; in Python noch nicht erprobt) |
| `GetModel(0)` schlägt fehl | kein Modell offen | vorher `app.GetModelCount() > 0` prüfen (KB 001408) |
| Spannungen um Faktor 10⁶ „falsch“ | Rückgabe in N/m² (SI) | in N/mm² bzw. MPa umrechnen (FAQ 004484) |
| GUI-CSV-Export unleserlich | Codepage cp1252, 2 Kopfzeilen, leere Nummernzeilen | `decode("cp1252")`, Kopf überspringen, Zeilen ohne Inhalt filtern |
| Werte um Faktor 1000 daneben | N/Nm vs. kN/kNm | Einheiten Kap. 7 |

---

## 9. Werkzeuge und Beispiele im Skill

| Datei | Zweck | Prüfstatus |
|---|---|---|
| `scripts\rfem_connect.py` | Verbindung, Lizenz-Klammer (`rfem_session`), Modellübersicht, `to_dict`, `sha256`, `find_model` | live ✓ 17.11.2026 (Verbindung, Modellübersicht; Fehlermeldung ohne laufendes RFEM) |
| `scripts\rfem5_api_inspect.py` | API-Referenz aus Typbibliothek erzeugen / durchsuchen (ohne RFEM) | live ✓ 17.11.2026 |
| `scripts\rfem5_selftest.py` | **Selbsttest des vollständigen Verbindungswegs** in 16 Schritten (T01 Python … T08 Schreiben+Rücklesen … T11 Gleichgewicht … T16 Unlock), PASS/FAIL je Schritt, JSON+MD-Protokoll; arbeitet nur an eigenem Testmodell | live ✓ 17.11.2026: **16/16 PASS** |
| `scripts\rfem5_paths.py` | Inventar aller RFEM-/Python-Pfade (+ Registry) und `--backup` der Benutzer-Einstellungen als ZIP mit SHA256SUMS | live ✓ 17.11.2026: 111 Einträge, Sicherung 11 Dateien + Registry |
| `references\API_REFERENZ_RFEM5.md` | 114 Interfaces · 184 Strukturen · 116 Aufzählungen mit Hilfetexten | erzeugt ✓ |
| `scripts\examples\bsp01_modell_lesen.py` | alle Modelldaten → JSON | offline ✓, **live ✓** |
| `scripts\examples\bsp02_ergebnisse_csv.py` | Ergebnisse einer LF/LK/RK → 3 CSV | offline ✓, **live ✓** |
| `scripts\examples\bsp03_kopie_aendern_rechnen.py` | Kopie → Knoten ändern → rechnen → speichern + Protokoll | offline ✓, **live ✓** |
| `scripts\examples\bsp04_modell_erzeugen.py` | neues Modell von Grund auf (offizielles C#-Beispiel in Python) | offline ✓, **live ✓** |

„offline ✓“ = Syntax geprüft und jede verwendete Konstante, Methode und jedes Strukturfeld gegen die Typbibliothek abgeglichen. „live ✓“ = Testlauf 17.11.2026 (RFEM 5.29.01.161059) in einem eigenen Testordner: bsp01 liest ein Modell nach JSON; bsp04 erzeugt und berechnet das Beispielmodell (3 Stäbe, LF 1); bsp02 exportiert 22 Schnittgrößen-, 2 Lager- und 4 Verformungszeilen; bsp03 verschiebt Knoten 3 in einer Kopie um +0,10 m, rechnet ohne Fehlermeldung, Quelle unverändert (SHA-256 gleich).

---

## 10. Arbeitsregeln für prüffähige Statik

1. **Original unantastbar:** Original nur lesen; Kopie in Ordner mit `SANDBOX` im Pfad; SHA-256 von Original vorher/nachher gleich.
2. **Protokoll pro Lauf (JSON):** Quelle, Hashes, jede Änderung *alt → neu* mit Quelle, Fehlerliste der Berechnung, Version RFEM/Python.
3. **Zahlen nur aus Primärquellen** (Pläne, Vermessung, RFEM) – abgeleitete Werte kennzeichnen, nichts „im Kopf“ rechnen lassen („LLM rechnet nichts“).
4. **Zurücklesen vor Speichern:** jede Änderung gegen den Sollwert prüfen, erst dann rechnen und `Save(pfad)`.
5. **Ergebnisse doppelt sichern:** Rohdaten (JSON/CSV) + lesbare Tabelle (XLSX/MD); Ausdruckprotokoll aus der GUI.
6. **Ein Client, eine Sitzung** – keine parallelen Skripte auf dieselbe RFEM-Instanz.

### 10.1 Freigabestufen (übernommen aus `rfem6-mcp-engineering`, GitHub nexus-platform)

| Stufe | Umfang | Voraussetzung |
|---|---|---|
| **G0** | nur lesen: Geometrie, Topologie, Lager, Material, Querschnitte, Lasten, vorhandene Ergebnisse – kein Rechnen, kein Speichern | Modellpfad + SHA-256 |
| **G1** | freigegebene Koordinaten/Lasten/Parameter ändern und rechnen – nur an geprüfter Arbeitskopie, vorher/nachher sichern, jede Änderung zurücklesen | Auftrag benennt das Delta |
| **G2** | Topologie: Knoten/Stäbe anlegen/löschen, Lager-/Systemkonzept ändern | ausdrückliche Entscheidung des Tragwerksplaners zum konkreten Delta |
| **G3** | kanonische Quelle überschreiben/befördern | ausdrückliche Freigabe + unveränderlicher Vorgänger + Vollhash |
| **G4** | Ingenieur-, Bestell- oder Einbaufreigabe | nur menschliche Unterschrift – `FINAL_RELEASE = HUMAN_SIGNOFF_REQUIRED` |

**Abbruchbedingungen:** unklare Modell-/Quellidentität, fehlende Eingaben, nicht freigegebenes Delta, Einheitenkonflikt, fehlgeschlagenes Rücklesen, keine Konvergenz → abhängige Schreib-/Rechenschritte stoppen, Befund dokumentieren, nie durch „Mock-PASS“ ersetzen.

**Nachweisordner je Lauf** (neuer Ordner mit Zeitstempel): Ausgangs-/Endzustand (`model_state_before/after.json`), Objektinventar, begrenzte Ergebnisexporte, `status.json`, `SHA256SUMS.txt`. Dateihash, Modell-Fingerabdruck und Ergebnishash sind verschiedene Dinge; ein Hash beweist nicht, dass RFEM das Ergebnis erzeugt hat – Ergebnis immer an Modellzustand + Berechnung + Kombination binden.

---

## 11. Grenzen der Schnittstelle

- **Ausdruckprotokoll** kann über COM **nicht** erzeugt oder gedruckt werden – `m.GetProtocols()` liefert nur Kopf- und Nummerierungsoptionen. Protokoll in der GUI erstellen; Vorlagen liegen in `C:\ProgramData\Dlubal\RFEM 5.29\General Data\RfemProtocolConfig.cfg` / `ProtocolTextsUser.db3`.
- Zusatzmodule (RF-STAHL EC3, RF-BETON, RF-DYNAM …) haben eigene Typbibliotheken (`…\Common Files\Dlubal\*.tlb`) und eigene SDK-Hilfen (`SDK\*.chm`); Zugriff über `m.GetModule("…")`.
- **RF-COM wird nicht mehr weiterentwickelt** (Dlubal Community, Jan. 2026): keine neue Interop-DLL; unter .NET 9 treten Zugriffsfehler auf (z. B. `GetLoadCombination(...).GetData()`). Für Python/comtypes nicht relevant, aber: langfristig ist RFEM 6 der Weg.
- **RFEM 6** ist nicht kompatibel (Dlubal FAQ 005190: RF-COM-Werkzeuge müssen neu geschrieben werden): dort `dlubal.api` (gRPC, Port 9000) mit **API-Key** aus dem Dlubal-Konto, alternativ der offizielle **Dlubal-MCP-Server**. Ein `.rf5` lässt sich in RFEM 6 über *Datei → Öffnen* importieren.

---

## 12. Pfade, Programmeinstellungen, Sicherung

Vollständiges, geprüftes Inventar jederzeit mit `python rfem5_paths.py` (Spalten: vorhanden, Größe, Datum, Pfad; `--json` zusätzlich mit SHA-256). Stand 17.11.2026: 111 von 111 Katalogeinträgen vorhanden.

| Kategorie | Pfad | Inhalt / Hinweis |
|---|---|---|
| **Programm** | `C:\Program Files\Dlubal\RFEM 5.29\RFEM64.exe`, `RFEM.ini`, `Help\RFEM_DEU.pdf` | COM-Server; `RFEM.ini` = externe Module/Menüeinträge |
| **COM-Typbibliothek** | `C:\Program Files\Common Files\Dlubal\RFEM5_64.dll` · `RFEM3_64.tlb` (v3.4) · `*_64.tlb` (Zusatzmodule) | comtypes-Cache: `%APPDATA%\Python\Python312\site-packages\comtypes\gen\` |
| **COM-Doku + Beispiele** | `C:\Users\Public\Documents\Dlubal\SDK\` – `RF-COM-5.chm`, `Reference Assemblies\x64\Dlubal.RFEM5.xml`, `Examples\RFEM\C#\…`, `VB.NET\…` | Kap. 15.1 |
| **RF-COM-5-Daten (Excel/VBA)** | `…\SDK\Examples\RFEM\Excel\RF-COM-5 - Model Data.xlsm` (Modellgeometrie), `- Loads.xlsm` (Lasten), `- Results.xlsm` (Resultate), `- Isolines.xlsm` | VBA mit Alt+F11; `Templates\Base` ist hier leer |
| **Materialbibliothek** | `C:\ProgramData\Dlubal\RFEM 5.29\General Data\Materialien.dbd` (Dlubal, 202 MB) · `Materialien_User.dbd` (Benutzer) | über COM: `d.GetMaterialDatabase()`; Material per `TextID` (Kap. 6.4) |
| **Querschnitte** | `General Data\profile_ro.DEU.db` · `EigProf.dat` (Benutzer) | `d.GetCrossSectionDatabase()` |
| **Programmeinstellungen** | `General Data\Config\*.rfconf` (Anzeige/Farben) · `Units\*.uni` (Einheitenprofile, z. B. `JUL.uni`) · `layers.db3` · `KombiNorm.dat` · `Default\` (Werkseinstellungen) | über COM nicht schaltbar – COM arbeitet immer in SI |
| **Ausdruckprotokoll** | `General Data\RfemProtocolConfig.cfg` · `ProtocolTextsUser.db3` · `AutoTranslate_User.txt` | Protokoll nur in der GUI (Kap. 11) |
| **Lastdaten** | `General Data\WIND.db3`, `SNOW.db3`, `Seismic*.db3` | Zonenkarten |
| **Rechenbeispiele** | `C:\Users\Public\Documents\Dlubal\Projects\Examples\RFEM-Beispiel-01…06.rf5` (+ `TESTMODELL.rf5`) · `…\Blocks\<Kategorie>\*.rss` (1.159 Bauteil-Blöcke) | zum gefahrlosen Testen (Kopie!) |
| **Registry** | `HKCR\RFEM5.Application` · `HKCR\CLSID\{5C397AC7-A317-4EE3-887C-0416236A44B1}\LocalServer32` = `RFEM64.exe /Automation` · `HKCU\Software\Dlubal\RFEM\5.29\64-bit` (Benutzereinstellungen, Modul-Konfigurationen `RF-…_CFG`, `Recent File List`) | nur lesen; Export per `reg export` |
| **Python** | `C:\Users\julia\AppData\Local\Programs\Python\Python312\python.exe` (3.12.10, 64 bit) · comtypes 1.4.16 | ohne `-I` starten |

### 12.1 Sicherung der Benutzer-Einstellungen

```bash
python rfem5_paths.py --backup "G:\Meine Ablage\_developement\LLM-LOCAL-SSOT\NEXUS.CAD.SKILLS\rfem5-com_BACKUPS"
```

Erzeugt `RFEM529_EINSTELLUNGEN_<Zeit>.zip` mit `Materialien_User.dbd`, `EigProf.dat`, `Config\`, `Units\`, `layers.db3`, `KombiNorm.dat`, `RfemProtocolConfig.cfg`, `ProtocolTextsUser.db3`, `AutoTranslate_User.txt`, Registry-Export `HKCU\Software\Dlubal\RFEM\5.29` sowie `SHA256SUMS.txt` und `MANIFEST.json`. Wiederherstellen: RFEM schließen, Dateien nach `General Data` zurückkopieren, `.reg` doppelklicken. Erste Sicherung: 17.11.2026 18:30 (11 Dateien + Registry).

### 12.2 Ablage im Google Drive (SSOT)

| Was | Ort (Drive = `G:\Meine Ablage`) |
|---|---|
| Skill (maßgeblich) | `_developement\LLM-LOCAL-SSOT\NEXUS.CAD.SKILLS\rfem5-com\` |
| installierte Kopie | `%USERPROFILE%\.claude\skills\rfem5-com\` (nach jeder Änderung neu kopieren, Hash-Abgleich) |
| Sicherungen (Skill-ZIP, Einstellungen) | `_developement\LLM-LOCAL-SSOT\NEXUS.CAD.SKILLS\rfem5-com_BACKUPS\` |
| Selbsttest-Protokolle | `_developement\LLM-LOCAL-SSOT\TESTS\RFEM5_COM_SANDBOX_SELFTEST\<Zeit>\` |
| Statusberichte | `_developement\LLM-LOCAL-SSOT\WORK\` (NEXUS-Syntax, `LEDGER-PENDING`) |

---

## 13. Rechenverfahren (Algorithmen) in RFEM 5

Die über COM einstellbaren Verfahren stehen in der Typbibliothek (Werte aus `API_REFERENZ_RFEM5.md`); Beschreibung laut RFEM-5-Handbuch Kap. 7.3.1.1.

| Bereich | Aufzählung (COM) | Werte | Wo setzen |
|---|---|---|---|
| Berechnungstheorie | `AnalysisMethodType` | `GeometricallyLinearStatic=1` (Th. I. O.), `SecondOrder=2` (Th. II. O.), `LargeDeformation=3` (Th. III. O.), `Postcritical=4` | je LF/LK: `ilc.GetAnalysisParameters()` → `.Method` |
| Iterationsverfahren | `SolvingSystemMethodType` | `NewtonRaphson=1`, `NewtonRaphsonPicard=2`, `Picard=3`, `NewtonRaphsonConstantMatrix=4`, `ModifiedNewtonRaphson=5` (postkritisch), `DynamicRelaxation=6` | `AnalysisParameters.SolvingSystemMethod` |
| Gleichungslöser | `SolverMethodType` | `DirectSolverMethod=1`, `IterativeSolverMethod=2` (ICG) | `C.GetSolverMethod()/SetSolverMethod()` |
| Laststufen | `AnalysisParameters.LoadIncrements`, `CalculationSettings.LoadCaseIncrements/LoadCombinationIncrements`, `MaxIterations` | Ganzzahl | `C.GetSettings()/SetSettings()` |
| Genauigkeit | `PrecisionAndTolerance` | `ConvergencePrecision`, `InstabilityDetection`, `DynamicRelaxationTimeStep`, `IterativeCalculationRobustness`, `MinimumInitialStrain` | `C.GetPrecisionAndTolerance()` |
| Flächentheorie | `BendingTheoryType` | `MindlingBendingTheory=1`, `KirchhoffBendingTheory=2` | `C.GetBendingTheory()` |
| Eigenwerte (RF-DYNAM Pro / RF-STABILITY) | – | Lanczos (Standard), Unterraumiteration, Wurzeln des charakteristischen Polynoms, ICG | Zusatzmodul-Schnittstelle |
| Formfindung (RF-FORM-FINDING) | – | URS-Verfahren (Bletzinger/Ramm), Zug- bzw. Projektionsmethode; Ergebnis-LF „RF-FORM-FINDING“ | Zusatzmodul |

**Für Seilstatik wichtig:**
- Stabtyp `Cable` (9) erzwingt Theorie III. Ordnung; Quersteifigkeit 1/200 der Längssteifigkeit. Für eine korrekte Durchhangslinie das Seil als **Seilkette aus mehreren Stäben** modellieren (Dlubal FAQ 001189).
- Für reproduzierbare Läufe Verfahren, Laststufen, Iterationen und Toleranz je LF/LK **auslesen und protokollieren** (`GetAnalysisParameters`, `GetSettings`, `GetPrecisionAndTolerance`) – Picard und Dynamische Relaxation können andere Konvergenzpfade liefern als Newton-Raphson.
- Direkter Löser für kleine/mittlere Modelle, iterativer bei sehr großen Modellen/RAM-Mangel (FAQ 000065).

**Hilfsalgorithmen für Skript-Workflows:** Ähnlichkeits-/Helmert-Transformation mit Ausgleichung (Vermessung ↔ Modell, ≥ 3 Passpunkte, Restklaffen ausweisen) · Kettenlinie y = a·cosh(x/a) als Plausibilitätsprüfung für Seile · SHA-256 (NIST FIPS 180-4) für Herkunftsnachweise · Gleichgewichtsprobe Σ Lagerkräfte = Σ Lasten (im Selbsttest T11).

| Quelle | Link |
|---|---|
| RFEM 5 Handbuch 7.3.1.1 Berechnungsparameter (Iterationsverfahren, Theorien, Laststufen) | ✓ <https://www.dlubal.com/en/downloads-and-information/documents/online-manuals/rfem-5/004276> |
| RFEM 5 Handbuch 7.3.3 Globale Berechnungsparameter | ✓ <https://www.dlubal.com/en/downloads-and-information/documents/online-manuals/rfem-5/004281> |
| RFEM 5 Handbuch 7.2.4 FE-Netzgenerierung | ✓ <https://www.dlubal.com/en/downloads-and-information/documents/online-manuals/rfem-5/004273> |
| FAQ 000065 Direkter vs. iterativer Gleichungslöser | ✓ <https://www.dlubal.com/en/support-and-learning/support/faq/000065> |
| FAQ 001189 Seilstrukturen nach Theorie III. Ordnung | ✓ <https://www.dlubal.com/en/support-and-learning/support/faq/001189> |
| KB 001391 Formfindung in RFEM (RF-FORM-FINDING) | ✓ <https://www.dlubal.com/en/support-and-learning/support/knowledge-base/001391> |
| RF-/DYNAM Pro Eigenwertlöser | ✓ <https://www.dlubal.com/en/support-and-learning/support/product-features/000325> |
| KB 000934 Eigenwertmethoden RF-STABILITY | ✓ <https://www.dlubal.com/en/support-and-learning/support/knowledge-base/000934> |
| RFEM 5 Produktseite Berechnung | ✓ <https://www.dlubal.com/en/products/older-products/rfem-5/calculation> |
| Helmert-Transformation · Kettenlinie · SHA-256 | ✓ <https://en.wikipedia.org/wiki/Helmert_transformation> · ✓ <https://mathworld.wolfram.com/Catenary.html> · ✓ <https://csrc.nist.gov/pubs/fips/180-4/upd1/final> |

---

## 14. Benchmark- und Verifikationsbeispiele

Zweck: Regressionstests für Skripte und Modelle – gleiche Eingabe muss die dokumentierte Referenzlösung liefern. Empfohlen für Seilstatik: **VE 0079, 0080, 0039, 0205, 0106** (jeweils RFEM-5-Modell + PDF mit Referenzlösung bei Dlubal).

| Beispiel | Prüft | Referenz | Link |
|---|---|---|---|
| VE 0079 Kettenlinie | Gleichgewichtsform eines Seils unter Eigengewicht | analytisch (cosh) | ✓ <https://www.dlubal.com/en/downloads-and-information/examples-and-tutorials/verification-examples/000079> |
| VE 0080 Seil mit Einzellasten | Normalkräfte, 2 Einzellasten | analytisch | ✓ <https://www.dlubal.com/en/downloads-and-information/examples-and-tutorials/verification-examples/000080> |
| VE 0039 Seil und Membran | max. Durchbiegung nach Th. III. O. | Ritz-Ansatz | ✓ <https://www.dlubal.com/en/downloads-and-information/examples-and-tutorials/verification-examples/0039> |
| VE 0205 Seil-Gleichgewichtskraft | Formfindung, vorgegebener Durchhang | analytisch | ✓ <https://www.dlubal.com/en-US/downloads-and-information/examples-and-tutorials/verification-examples/0205> |
| VE 0106 Eigenschwingung Saite | Eigenfrequenzen vorgespannter Saite | f_n = n/(2L)·√(N/μ) | ✓ <https://www.dlubal.com/en/downloads-and-information/examples-and-tutorials/verification-examples/000106> |
| VE 0040 Konsole große Verformung | Th. III. O. Biegung | analytisch | ✓ <https://www.dlubal.com/en/downloads-and-information/examples-and-tutorials/verification-examples/000040> |
| VE 0096 Euler-Knicken | 4 Euler-Fälle, RF-STABILITY (Lanczos), Abw. ≤ 0,2 % | analytisch | ✓ <https://www.dlubal.com/en/downloads-and-information/examples-and-tutorials/verification-examples/009096> |
| VE 0115 / 0101 | Biegeschwingung mit Normalkraft / Modalanalyse Kragarm | analytisch | ✓ <https://www.dlubal.com/en/downloads-and-information/examples-and-tutorials/verification-examples/0115> · ✓ <https://www.dlubal.com/en/downloads-and-information/examples-and-tutorials/verification-examples/0101> |
| NAFEMS Geometrische Nichtlinearität (B9 vorgespanntes Seil, B10 Seil unter Eigengewicht) | unabhängige FE-Benchmarks | Literatur | ✓ <https://www.nafems.org/publications/glossaryofbenchmarks/nonlinear/geometric> · ✓ P03 <https://www.nafems.org/publications/resource_center/p03/> (kostenpflichtig) |
| VDI 6201 Blatt 2 Verifikationsbeispiele (2019) | Software-Verifikation Tragwerksberechnung | Richtlinie | ✓ <https://vdi.de/richtlinien/details/vdi-6201-blatt-2-software-based-structural-analysis-verification-examples> (kostenpflichtig) |
| Lokal: `RFEM-Beispiel-01…06.rf5`, Selbsttest-Modell | Schnittstellen-Regression | Selbsttest T11 (Gleichgewicht) | `C:\Users\Public\Documents\Dlubal\Projects\Examples\` |

Hinweis: Die Dlubal-Übersichtsseite der Verifikationsbeispiele wird per JavaScript geladen; obige Einträge sind einzeln geprüft, die PDFs wurden nicht heruntergeladen. Immer `www.dlubal.com` verwenden (ohne `www` teils Umleitung auf die Startseite).

---

## 15. Quellen und weiterführende Links

### 15.1 Lokal installiert (dieser Rechner)

| Quelle | Pfad | Inhalt |
|---|---|---|
| **RF-COM-5-Hilfe** | `C:\Users\Public\Documents\Dlubal\SDK\RF-COM-5.chm` | offizielle Methodenreferenz (Doppelklick öffnet) |
| .NET-Doku als XML | `…\SDK\Reference Assemblies\x64\Dlubal.RFEM5.xml` | alle Methoden/Felder mit Beschreibung (durchsuchbar) |
| C#-Beispiele | `…\SDK\Examples\RFEM\C#\` | RFEMModeller, AreaLoads, SurfaceLoads, MemberVaryingLoads, NonlinearHinges, NonlinearSupports, SurfaceOrthotropic, Tendon, SelectObjects, PickTools, ExternalModule, ModuleSteelMembers |
| VB.NET-Beispiel | `…\SDK\Examples\RFEM\VB.NET\RFEMModeller\` | wie C# |
| **Excel-Vorlagen (VBA)** | `C:\Users\Public\Documents\Dlubal\SDK\Examples\RFEM\Excel\` (`Templates\Base` ist auf diesem Rechner leer) | `RF-COM-5 - Model Data / Loads / Results / Isolines.xlsm`, `Solids.xlsm`, `View.xlsm`, `RF-STABILITY.xlsm`, `RF-DYNAM Pro …xlsm`, `Member effective lengths.xlsm` – VBA-Code mit Alt+F11 ansehen |
| Hilfen Zusatzmodule | `…\SDK\STEEL-EC3.chm`, `RF-CONCRETE-Surfaces.chm`, `RF-DYNAM.chm`, `TIMBER-Pro.chm` … | Modul-Schnittstellen |
| Handbuch RFEM 5 | `C:\Program Files\Dlubal\RFEM 5.29\Help\RFEM_DEU.pdf` | Programmbedienung |
| Beispielmodelle | `C:\Users\Public\Documents\Dlubal\Projects\Examples\` | zum gefahrlosen Testen |

### 15.2 Eigene Ablage (Google Drive) und GitHub

| Dokument | Inhalt |
|---|---|
| [RFEM-Anbindung Filefinder (09.11.2026)](https://drive.google.com/file/d/1KjFrdYelpHbC4JJW8WBMaLoxtDqi7bGt/view) | Matrix aller RFEM-5/6-Anbindungen (COM, gRPC, Dlubal-MCP, NEXUS-Bridge) + Linkliste |
| [PowerShell-Transkript COM/gRPC 21.10.2026](https://drive.google.com/file/d/1Sm_ELlci5gO8hJzjb1F2q2WxssMpZyi9/view) | Live-Nachweis: Lizenzfehler ohne LockLicense, Methodeninventar IModel/IModelData/ICalculation |
| [BERICHT RFEM5 COM Seilstatik (08.10.2026)](https://drive.google.com/file/d/1uf4MUpiiqFiOJMO8DRC9UjvrseMreZOW/view) | Projektbericht Ablauf Kopie → Lesen → Ändern → Rechnen |
| [RFEM Apps v0.1 – W012 Eibengasse (README)](https://drive.google.com/file/d/15kUzMz9-MZvWGKxc0Gdm9BgicqNpa0Fo/view) · [rfem5_results.py](https://drive.google.com/file/d/1CtMFken2VoGYnq9NMmAe0cHj9FtP55kk/view) · [rfem_probe.py](https://drive.google.com/file/d/1boemzx87fEt69PrXaLFXnPosLSaGuV1x/view) | weitere RF5/RF6-Adapter (CLI) |
| [Linkliste Dlubal MCP und KI-Integration](https://drive.google.com/file/d/1erQgu8ODG29o1lyMnqe4JcqtqYhlyxPG/view) | RFEM 6 / MCP-Links |
| Projektordner `G:\Meine Ablage\26-03-18_Boeb_Adaptierung\SANDBOX_RFEM5_COM_20260923_1356\04_SKRIPTE_REPRO\` | erprobte Projekt-Skripte (Ändern: `neue_anker_v01_aufbauen.py`, Rechnen/Ergebnisse: `var_neu_rechnen_auswerten.py`, Export: `export_pruefdaten.py`) |

**GitHub `julianzotter` (privat, durchsucht 17.11.2026)** – RFEM-relevante Dateien:

| Repository / Datei | Inhalt | Nutzen für RF5-COM |
|---|---|---|
| `nexus-platform/plugins/nexus-aec-engineering/skills/rfem6-mcp-engineering/SKILL.md` | RFEM-6-Skill: Vertrag, Freigabestufen G0–G4, Abbruchbedingungen | in Kap. 10.1 übernommen |
| `…/rfem6-mcp-engineering/references/audit-contract.md`, `runtime-setup.md`, `boeblingen.md`, `scripts/validate_result.py` | Nachweis-Vertrag je Lauf, RF6-Setup, Projekt-Overlay Böblingen, Ergebnisprüfung | Nachweisordner Kap. 10.1 |
| `nexus-platform/tools/nexus-file-finder/` | Dateisuche mit Route `rfem5_com` (comtypes, LockLicense, 5.29) | Dateien schnell finden |
| `nexus-platform/WORK/REPORTS/26_11_09_0934_RFEM-ANBINDUNG-FILEFINDER_000_IDCL.md` | Anbindungsmatrix RF5/RF6 | wie Drive-Fassung |
| `nexus-platform/reports/26_10_19_19_00_ID-UNRESOLVED_AEC-RFEM-SKILLS_v0.1.0.md` | Skill-Report RFEM | Historie |
| `nexus-ai-operation-system/aec_rfem_hitl_mvp/` + `docs/aec-hitl-rfem-mvp.md` | Mensch-in-der-Schleife-MVP mit Freigabe-Gates und MCP-Server | Vorlage Freigabe-Workflow |
| `nexus-ai-operation-system/…/eibengasse_engine/rfem_adapter.py` | Statusprüfung `dlubal.api` | nur RF6 |
| `julianzotter/tools/26_10_06_ID-03-RF6-Ergebnis-Export.py`, `…_anpassen_rf6.py` | RF6-Ergebnisexport/-Anpassung | nur RF6 |
| `julianzotter/docs/26_10_03_SEILSTATIK-BOEB_NEUE-ARTEFAKTE-UEBERSICHT_v1.0.md` | Artefaktliste Seilstatik mit Hashes (RFEM 5.29, comtypes 1.4.17) | Herkunftsnachweise |
| `RFEM_Python_Client` (Fork von Dlubal) | RFEM 6 Webservice (SOAP), **kein** RF5-COM | Abgrenzung |

Ein RF5-COM-Skill existiert auf GitHub noch nicht. Vorschlag: `nexus-platform/plugins/nexus-aec-engineering/skills/rfem5-com/` (nur nach Freigabe pushen).

### 15.3 Web

Recherche 17.11.2026. **Ein öffentliches Python-Beispiel für RF-COM 5 gibt es nicht** (GitHub, Stack Overflow, Eng-Tips, Reddit geprüft). Die offiziellen Beispiele sind VBA und C#; die Aufrufe lassen sich fast 1:1 nach comtypes übertragen (`Set obj = …` → `obj = …`, `AtNo` → `R.AtNo`). ✓ = Seite geöffnet und Inhalt bestätigt.

**Einstieg und Grundlagen (Dlubal)**

| Link | Inhalt | Sprache |
|---|---|---|
| ✓ [FAQ 002390 – Lernmaterial-Übersicht RF-COM](https://www.dlubal.com/en-US/support-and-learning/support/faq/002390) | Index: Webinar + gesamte VBA-Artikelserie | – |
| ✓ [KB 001242 – SDK COM ab Version X.06](https://www.dlubal.com/en/support-and-learning/support/knowledge-base/001242) | wo SDK, `RF-COM-5.chm` und Beispiele liegen | – |
| ✓ [Webinar 001921 – Programmierbare COM-Schnittstelle RFEM/RSTAB](https://www.dlubal.com/en/support-and-learning/learning/webinars/001921) | Aufzeichnung, Folien-PDF, Beispiel-.xlsm | VBA |
| ✓ [KB 001293 – VBA Teil 1: Modell öffnen, anlegen, speichern, schließen](https://www.dlubal.com/en/support-and-learning/support/knowledge-base/001293) | `LockLicense`, `Show`, `Save`, `UnlockLicense` | VBA |
| ✓ [KB 001379 – VBA Teil 2.1: Stab anlegen](https://www.dlubal.com/en/support-and-learning/support/knowledge-base/001379) | `PrepareModification`, Strukturen Node/Line/Material/CrossSection/Member, Nummernregeln | VBA |
| ✓ [KB 001408 – VBA Teil 2.2: Lager, Lastfälle, Kombinationen, Lasten](https://www.dlubal.com/en/support-and-learning/support/knowledge-base/001408) | `SetLoadCases`, `SetLoadCombinations`, `SetMemberLoads`, Fehlerbehandlung | VBA |
| ✓ [KB 001441 – VBA Teil 3: Excel-Werkzeug aus RFEM starten](https://www.dlubal.com/en/support-and-learning/support/knowledge-base/001441) | `EnableSelections`, Eintrag in `RFEM.ini`, Quellcode-ZIP | VBA |
| ✓ [KB 001459 – VBA Teil 4.1: Rahmenoptimierung mit RF-STAHL EC3](https://www.dlubal.com/en/support-and-learning/support/knowledge-base/001459) | Zusatzmodul über `GetModule("STEEL_EC3")` | VBA |
| ✓ [KB 001515 – VBA Teil 5: Hilfslinien](https://www.dlubal.com/en/support-and-learning/support/knowledge-base/001515) | Hilfslinien kopieren/verschieben | VBA |
| ✓ [KB 001559 – Stückliste](https://www.dlubal.com/en/support-and-learning/support/knowledge-base/001559) | braucht zusätzlich Typbibliothek v3.4 | VBA |
| ✓ [KB 001596 – Elemente auswählen](https://www.dlubal.com/en-US/support-and-learning/support/knowledge-base/001596) | `SelectObjects` mit Nummernlisten | VBA |

**Ergebnisse und Berechnung (FAQ mit Download .xlsm + .rf5)**

| Link | Inhalt |
|---|---|
| ✓ [FAQ 004869 – Schnittresultierende](https://www.dlubal.com/en/support-and-learning/support/faq/004869) | `GetResultsInFeNodes` → `IResults2.GetResultant` |
| ✓ [FAQ 004951 – Stabverformungen](https://www.dlubal.com/en/support-and-learning/support/faq/004951) | `GetMemberDeformations(nr, AtNo, Achsen)` |
| ✓ [FAQ 004484 – Flächenspannungen](https://www.dlubal.com/en/support-and-learning/support/faq/004484) | `GetSurfaceEquivalentStresses`; Einheit N/m² |
| ✓ [FAQ 004409 – Schnitte](https://www.dlubal.com/en/support-and-learning/support/faq/004409) | `GetResultsInSection` |
| ✓ [FAQ 004184 – Berechnungsparameter](https://www.dlubal.com/en/support-and-learning/support/faq/004184) | `GetOptions/SetOptions`, `GetNonlinearities`, `GetSettings` |
| ✓ [Video 001545 / FAQ 004499 – RFEM unsichtbar im Hintergrund](https://www.dlubal.com/en/support-and-learning/learning/videos/001545) | `New Application`, `CreateModel`, optional `Show` |

**Weitere FAQ (VBA)**: ✓ [004903 Parameterliste](https://www.dlubal.com/en/support-and-learning/support/faq/004903) · ✓ [004715 Objekte auswählen](https://www.dlubal.com/en/support-and-learning/support/faq/004715) · ✓ [004638 RfLine statt Line (VBA)](https://www.dlubal.com/en/support-and-learning/support/faq/004638) · ✓ [004563 Stabexzentrizitäten](https://www.dlubal.com/en/support-and-learning/support/faq/004563) · ✓ [004326 Kommentare](https://www.dlubal.com/en/support-and-learning/support/faq/004326) · ✓ [004622 DYNAM Pro Antwortspektrum](https://www.dlubal.com/en/support-and-learning/support/faq/004622) · ✓ [004629 wo finde ich RF-COM (NodalLoads.xlsm)](https://www.dlubal.com/en/support-and-learning/support/faq/004629)

**C# / .NET und Umfang**: ✓ [FAQ 002338 – Verweis in Visual Studio](https://www.dlubal.com/en/support-and-learning/support/faq/002338) · ✓ [FAQ 004627 – Fehler in den C#-Beispielen](https://www.dlubal.com/en/support-and-learning/support/faq/004627) · ✓ [FAQ 003034 – erreichbare Zusatzmodule](https://www.dlubal.com/en/support-and-learning/support/faq/003034) · ✓ [Produktmerkmal 000394](https://www.dlubal.com/en/support-and-learning/support/product-features/000394) · ✓ [FAQ 005190 – RF-COM-Werkzeuge in RFEM 6](https://www.dlubal.com/en/support-and-learning/support/faq/005190)

**Community und Open Source**

| Link | Inhalt |
|---|---|
| ✓ [Dlubal Community: RF-COM 5 mit C# .NET 9 (Jan. 2026)](https://community.dlubal.com/t/rf-com-5-compatibility-issues-when-calling-using-c-net9/2660) | .NET-9-Probleme; Dlubal: RF-COM wird nicht weiterentwickelt |
| ✓ [BHoM/RFEM5_Toolkit (GitHub, C#, LGPL-3.0, aktiv)](https://github.com/BHoM/RFEM5_Toolkit) | umfangreichster öffentlicher Code für das komplette Objektmodell (Anlegen, Lesen, Ergebnisse) – beste Vorlage zum Übertragen nach Python |
| Altes Dlubal-Forum: [RF-COM-Schnittstelle mit Python](https://www.dlubal.com/forum/deutschsprachiges-dlubal-forum/4207-verwenden-sie-die-rf-com-schnittstelle-zusammen-mit-python) · [RF-COM-Steuerung mittels Python](https://www.dlubal.com/forum/deutschsprachiges-dlubal-forum/264-rf-com-steuerung-mittels-python) | nur in Suchergebnissen gesehen (Seiten antworteten nicht): comtypes mit RFEM 4/Python 2.6, Probleme bei Zusatzmodulen |
| ✓ [Dlubal-Software (GitHub)](https://github.com/Dlubal-Software) | **keine** RFEM-5-Repositories; `RFEM_Python_Client` = RFEM 6 (Webservice) |
| [RFEM 6 API-Dokumentation (dlubal.api, gRPC)](https://apidocs.dlubal.com/) · [Dlubal-MCP-Server](https://apidocs.dlubal.com/installation_mcp.html) | Abgrenzung RFEM 6 |

---

## 16. Schnittstellen-Landkarte RFEM 5 / RFEM 6 (live geprüft 17.11.2026)

Prüfwerkzeug: `python scripts\rfem_interfaces_probe.py [--key-name NAME] [--json f]` – nur lesend; ein API-Key wird nur zur Laufzeit aus `RFEM_API_KEY` oder per **Name** aus dem Dlubal-Key-Store geholt und nie ausgegeben.

| Weg | Version hier | Technik / Port | Authentifizierung | Live-Befund | Einsatz |
|---|---|---|---|---|---|
| **A · RF5 COM** | RFEM 5.29.01.161059 | comtypes + `RFEM5_64.dll` | RF-COM-Lizenz, `LockLicense` | ✅ PASS (Selbsttest 16/16) | produktiv |
| **B · RF6 gRPC (API II)** | RFEM 6.12 (`RFEM6.exe` hört auf `::9000`) · `dlubal.api` 2.12.8 (Minor passt) | `rfem.Application(url, port=9000)` | API-Key (Bearer) **+** API-Abo (auch Free) **+** Lizenzserver | ⛔ ohne Key: `UNAUTHENTICATED – API key is in incorrect format`; **alle drei vorhandenen Dlubal-Keys** (Fingerabdrücke SHA-256/12: `6a169f28afba` Key-Store `nexus_aec_engine`, `d37afae812be` Drive-Textdatei, `dd16c94ef566` HTML-Chatexport) → `API key is either missing or invalid`; einmalig „Verbindung zum Dlubal-Lizenzserver ist blockiert“ | blockiert bis gültiger Key + Abo |
| **C · RF6 WebServices (API I, SOAP)** | RFEM 6.12 | Port 8081, `RFEM_Python_Client` | kein API-Key (lokal), aber Webservice-Lizenz/Option | ⛔ in den Programmoptionen aktiviert (Screenshot), **kein Listener auf 8081** (nur `RFEM6.exe` auf `::9000`); API I seit 23.04.2025 im Wartungsmodus | nach RFEM-6-Neustart erneut prüfen; nur Übergang |
| **D · Dlubal-MCP** | – | `bin\python.exe -m rfem_mcp_server` (STDIO) bzw. `dlubal-mcp` (pip) | wie B | ⛔ in RFEM 6.12 nicht enthalten (erst ab 6.13.0002) | nach Update |
| **E · RF6-Datei ohne API** | `.rf6` | ZIP + SQLite (`model.db`) | keine | ✅ Inventar (Skill `cad-statik-pipeline`) | Bestandsaufnahme |
| **F · RF5 → RF6** | – | RFEM 6 *Datei → Öffnen* `.rf5` | – | – | Migration |

### 16.1 Die drei lokalen Wege ohne API-Key (Stand 17.11.2026)

| # | Weg | Key nötig | Stand | Wofür |
|---|---|---|---|---|
| 1 | **RFEM 5 über COM** (Weg A) | nein (RF-COM-Lizenz) | ✅ vollständig getestet: Selbsttest 16/16, Lesen/Schreiben inkl. Flächen und Lasten (Skill `cad-statik-pipeline`, K01–K11) | Modellaufbau, Rechnung, Ergebnisse – produktiver Weg |
| 2 | **RFEM-6-Dateien direkt** (Weg E) bzw. **IFC-Export aus RFEM 6** | nein | ✅ `.rf6` = ZIP + SQLite → Inventar (K06); Geometrie/Lasten über *Datei → Export → IFC* aus RFEM 6 und dann `cad-statik-pipeline` (IFC-Leser wie K01/K02) | Bestandsaufnahme, Übergabe RF6 → NSM → RF5 |
| 3 | **SOAP-Webservice von RFEM 6** (Weg C) | nein (lokal), Webservice-Option nötig | ⛔ Option gesetzt, Port 8081 hört nicht | nur Übergang; Prüfung: RFEM 6 neu starten, dann `rfem_interfaces_probe.py` (Teil C) bzw. `Test-NetConnection 127.0.0.1 -Port 8081` |

**Vorhandene Dlubal-API-Keys:** drei Keys gefunden (Key-Store, Drive-Textdatei, HTML-Chatexport), **alle drei vom Server abgelehnt** (`missing or invalid`). In `C:\zotter_ai\keys` liegt **kein** Dlubal-Key. Ursache vermutlich: Key widerrufen/abgelaufen oder kein aktives API-II-Abo. Zwei Fundstellen enthalten den Key **im Klartext** in Drive → Key im Extranet widerrufen, Dateien bereinigen (Benutzeraktion).

**Umgebungsvariablen (Analyse 17.11.2026, nur Namen):** keine Variable mit `RFEM`/`DLUBAL`; `RFEM_API_KEY` ist nicht gesetzt. Auffällig: derselbe Wert unter `OPENAI_API_KEY`, `DeepSeek-Bridge` und `DeepSeek-Bridge1` (Fingerabdruck gleich), `GEMMA_API_KEY` zusätzlich als Systemvariable. Empfehlung: einen gültigen Key nur sitzungsweise als `RFEM_API_KEY` setzen, nie dauerhaft und nie in Drive/Git.

**Widerlegt:** „RFEM-API-Zugriff lokal ohne Key“ (Notiz in `NEXUS.CAD.PYTHON.md`) – die Zeile `api_key_value=None, … port=9000` ist nur die **Standardsignatur** von `rfem.Application()`; der Server lehnt ohne Key ab.

**Key-Ablage in `dlubal.api` 2.12.8 (Code gelesen):** `config.ini` liegt im **Paketordner** `site-packages\dlubal\api\config.ini` (`Path(__file__).parents[1]`); mit `api_key_name` + `api_key_value` wird der Key dort **im Klartext gespeichert**. Neuere Doku/Versionen: `%LOCALAPPDATA%\Dlubal\api\config.ini`. Empfehlung: Key nur als Umgebungsvariable zur Laufzeit, nie in Drive/Git; Wert im Extranet nur einmal sichtbar → neu erzeugen, wenn unsicher.

**Versionsregel:** `dlubal.api 2.<minor>.*` = `RFEM 6.<minor>` (der Client warnt bei Abweichung); ab 2.12.11 heißt `structure_core.Section` → `CrossSection` (Hinweis aus `boeb_seilnetz/rfem_adapter.py`).

**`dlubal.api` 2.12.8 – Methoden von `rfem.Application`:** `get_object(_list)`, `create_object(_list)`, `update_object(_list)`, `delete_object(_list)`, `select_objects`, `get_results`, `get_result_table`, `convert_objects`, `import_from`, `export_to`, `create_model`, `open_model`, `save_model`, `close_model`, `close_all_models`, `get_active_model`, `set_active_model`, `get_model_list`, `get_application_info`, `get_subscription_info`, `delete_all_objects`, `calculate_all`, `calculate_specific`, `has_results`, `plausibility_check`, `get_object_id_list`, `get_model_main_parameters`, `generate_combinations`, `get/set_base_data`, `get/set_mesh_settings`, `generate_mesh`, `get_mesh_statistics`, `delete_mesh`, `get/set_design_settings`.

**Freischaltung RF6 (Mensch):** ① Extranet: API-II-Abo prüfen (Free genügt), Key neu erzeugen · ② Firewall/Netz: Zugang zum Dlubal-Lizenzserver freigeben (vollständige Meldung im Probe-JSON) · ③ Key nur als `RFEM_API_KEY` setzen · ④ `rfem_interfaces_probe.py` erneut · ⑤ dann vorhandene Brücke `WORK\REPORTS\RFEM6_MCP_Bridge_Extended.py` (gepinnt auf 2.12.8/6.12.0008) statt Neubau.

---

## 17. Integrationswege mit Claude

| Weg | Wer führt aus | Reproduzierbarkeit | Einsatz | Bezug |
|---|---|---|---|---|
| **1 · Python-Skript lokal** | Mensch startet Skript | sehr hoch (Git, Hash, Protokoll) | Produktion, wiederkehrende Nachweise | alle `scripts\*.py` dieses Skills |
| **2 · Claude Code (Agent im Terminal)** | Claude liest/schreibt/führt Skripte aus, sieht Fehler | hoch, wenn Skripte + Protokolle gespeichert werden | Entwicklung, Tests, Auswertungen | diese Sitzung |
| **3 · MCP-Server (Claude Desktop)** | Claude ruft Werkzeuge direkt auf | gering (Chatverlauf) | Erkundung, Prototyp | RF6 ab 6.13.0002; für RF5 kein offizieller MCP |

Empfehlung: erkunden über 3 (nur G0), stabilisieren über 2, produktiv über 1 mit Selbsttest, Freigabestufen und Nachweisordner (Kap. 10.1). Laut Dlubal verbrauchen API-II-Aufrufe (Berechnen, Speichern, Ergebnisse) Abo-Kontingent; `get_application_info` ist frei.

---

## 18. Analyse der Bestandsskripte und -dokumente (17.11.2026)

| Quelle | Befund | Belegt durch |
|---|---|---|
| `NEXUS.CAD.SKILLS\precast_residential_building.py` (RF6, dlubal.api) | `# VERIFY`-Felder existieren alle (`Node.coordinate_1..3`, `Line.definition_nodes`, `Member.line/section_start`, `Surface.boundary_lines/material`, `NodalSupport.spring_*`) – **aber** `Surface(thickness=0.20)` ist **falsch**: `thickness` ist `int32` = Nummer eines `Thickness`-Objekts → `TypeError`. Korrektur: `Thickness(no=1, material=1, uniform_thickness=0.20)` + `Surface(thickness=1)` | Protobuf-Deskriptoren dlubal.api 2.12.8, Testaufruf |
| dito | `api_key_name="default"` – im Key-Store gibt es keinen `default`-Eintrag → Verbindung scheitert | Key-Store-Prüfung |
| dito | `sanity_check` mit `assert` (bei `python -O` wirkungslos) → `ValueError` verwenden | Code |
| dito | `quick_equilibrium_estimate` rechnet Lasten/Beiwerte im Skript → nur Plausibilität, kein Nachweis („LLM rechnet nichts“) | Code |
| dito | Querschnitts-/Materialnamen (`R_300/300`, `C30/37`) gegen RFEM-6-Bibliothek ungeprüft; Achse dort Z nach oben, RFEM-Standard Z nach unten | Code |
| `26_04_11_RFEM6-API-KEY-CLAUDE-Steuerung.docx` | vermischt API I (SOAP, `RFEM_Python_Client`, Port 8081) und API II (gRPC); Teil 1: `NodalSupportType` nicht importiert | Textanalyse |
| `RFEM6 API-Schnittstelle und Lizenzstatus prüfen - Claude.html` | **Klartext-API-Key** an zwei Stellen → widerrufen; Lizenz-Ausleihe („Entliehen“) ≠ Vertragsende; MCP ab 6.13.0002 | Textanalyse |
| `26_03_18_RFEM_Python_Client Repo from Github.txt` | API I: `connection refused` 8081 = WebService nicht aktiv; SOAP-Fault bei offenem Dialog „Programmoptionen“; `input()` → `EOFError` in nicht-interaktiven Läufen | Protokoll |
| `NEXUS.CAD.PYTHON.md` | „Zugriff ohne Key“ widerlegt (Kap. 16) | Live-Probe |
| `CLAUDE RFEM6 INTEGRATION (API-KEY – MCP-SERVER).docx` | drei Integrationswege → Kap. 17; `precast_cad_generator.py` erzeugt nur CAD (DXF/IFC/STL/SVG/VRML/Three.js), kein RFEM | Textanalyse |
| `26_04_9_DXF+IFC-CAD-Datenextraktion…docx` | ezdxf `recover.readfile`; ifcopenshell 0.8.4 scheitert an `IFC4X3_RC4`; Allplan exportiert alles als `IfcBuildingElementProxy` → Klassifikation über Psets; Toleranzen ±1 mm / Achsen ±20 mm | Textanalyse |

---

## 19. CAD-Datenpipeline DXF/IFC → RFEM

Umgesetzt als eigener Skill **`cad-statik-pipeline`** (`NEXUS.CAD.SKILLS\cad-statik-pipeline\`, Handbuch `references\HANDBUCH_CAD_STATIK_PIPELINE.md`):
neutrales Statikmodell (NSM) mit Lesern/Schreibern für DXF, DWG, IFC, RFEM-CSV, JSON, CSV, SQLite, RF5 (COM) und RF6 (Inventar), formatübergreifender Vergleich und Anlegen neuer RF5-Modelle.
Live geprüft: `EIS_Gesamt_26_BETONBAU` DXF ↔ IFC ↔ RF5 je PASS (1.519 Knoten, 376 Stäbe), Rückweg IFC → neues RF5 PASS, Böblingen-CSV ↔ RF5 PASS.
**Wichtigste Regel:** RFEM-System (Z unten) ↔ IFC/Welt (Z oben) = Drehung 180° um X `(x, y, z) → (x, −y, −z)`.

---

## 20. Architekturprinzipien für deterministische Skript-Workflows

| Prinzip | Umsetzung in den Skills |
|---|---|
| Deterministischer, reiner Kern | `nsm.py` (keine Ein-/Ausgabe in Kernfunktionen, sortierte Ausgabe, Fingerabdruck) |
| Validierung an der Grenze, früh scheitern | `validate()`, Pfad-Guards (`SANDBOX`), Versions-/Lizenzprüfung vor Zugriff |
| Adapter statt verstreuter Schnittstellenaufrufe | `rfem_connect.py` (RF5), `formats.py` (Formate), Probe für RF6 |
| Kein stilles Korrigieren | Befunde/Hinweise statt Annahmen; Platzhalter werden gemeldet |
| Idempotenz und Nachweis | gleiche Eingabe → gleiche Ausgabe; SHA-256, JSON-Protokolle, neue Ordner je Lauf |
| Freigabestufen G0–G4 | Kap. 10.1 |
| LLM rechnet nichts | Zahlen nur aus Quellen oder RFEM; abgeleitete Werte gekennzeichnet |
| Wiederverwenden vor Neubauen | vorhandene Brücken/Adapter (Kap. 15.2, Kap. 16 ⑤) |

---

## 21. Glossar

| Begriff | Bedeutung |
|---|---|
| COM | Component Object Model – Windows-Technik, über die Programme einander steuern |
| RF-COM | Lizenzmodul von RFEM 5 für die COM-Schnittstelle |
| Typbibliothek | Beschreibung aller Interfaces/Strukturen (`RFEM5_64.dll`); comtypes erzeugt daraus Python-Code |
| comtypes | Python-Paket für COM mit vtable-Interfaces (Alternative zu pywin32) |
| IDispatch | „Spät gebundene“ COM-Schnittstelle; fehlt bei RFEM 5 → pywin32 geht nicht |
| Interface (`I…`) | Objekt mit Methoden, z. B. `IModel` |
| Struktur | Datensatz mit Feldern, z. B. `Node` |
| `AtNo` / `AtIndex` | Zugriff über Objektnummer / über Position in der Liste |
| LF / LK / RK / SK | Lastfall / Lastkombination / Ergebniskombination / Superkombination |
| FE-Knoten / Rasterpunkte | Ergebnisorte: Netzknoten bzw. Teilungspunkte der Stäbe |
| SSOT | Single Source of Truth – die eine maßgebliche Ablage |
