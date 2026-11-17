---
name: rfem5-com
description: RFEM 5 (5.29) per Python über die COM-Schnittstelle (comtypes) verbinden, Modelle lesen, ändern, rechnen und Ergebnisse auslesen. Verwenden, wenn RFEM 5, .rf5-Dateien, RF-COM, Dlubal COM, LockLicense oder Ergebnisse aus RFEM 5 per Skript gefragt sind. Nicht für RFEM 6 (dort dlubal.api/gRPC mit API-Key).
---

# RFEM 5 – COM-Schnittstelle (Python)

Stand 17.11.2026 · geprüft mit RFEM 5.29.01.161059 (64 bit), Python 3.12, comtypes 1.4.16 · Quelle: Projekt Seilstatik Böblingen (Sept.–Okt. 2026) + Pfaderhebung `26_11_17_RFEM 5.29 AnythingSearchResults.md`

## 1. Verbinden – das Wichtigste

```python
import comtypes.client as cc
R = cc.GetModule(r"C:\Program Files\Common Files\Dlubal\RFEM5_64.dll")      # Typbibliothek
app = cc.GetActiveObject(R.Application, interface=R.IApplication)           # an laufendes RFEM anhängen
app.LockLicense()
try:
    print(app.GetVersion(), bool(app.IsComLicensed()))
    m = app.GetModel(0)                                                     # oder app.OpenModel(pfad)
finally:
    app.UnlockLicense()                                                     # IMMER, sonst bleibt die GUI gesperrt
```

Dateien in diesem Skill-Ordner (Pfad = Ordner dieser SKILL.md):

| Datei | Wann lesen/benutzen |
|---|---|
| `references/BENUTZERHANDBUCH_RFEM5_COM.md` | ausführliche Anleitung: Rezepte, Einheiten, Fehlerbilder, Quellen/Weblinks – bei jeder nicht-trivialen Aufgabe zuerst den passenden Abschnitt lesen |
| `references/LINKLISTE_RFEM5_COM.md` | alle geprüften Weblinks: Dlubal-VBA/C#-Serie, FAQ, Rechenverfahren, Benchmarks (VE), RFEM 6 |
| `references/API_REFERENZ_RFEM5.md` | alle 114 Interfaces / 184 Strukturen / 116 Enums mit Hilfetext – **Methodennamen nie raten**, hier nachschlagen (grep) |
| `scripts/rfem5_api_inspect.py --find <Text>` | schnelle Namenssuche direkt in der Typbibliothek (RFEM muss nicht laufen) |
| `scripts/rfem_connect.py` | Verbindungstest (`--open`, `--guard`, `--start`, `--json`); als Modul: `rfem_session()`, `find_model()`, `to_dict()`, `sha256()` |
| `scripts/examples/bsp01_modell_lesen.py` | Modelldaten → JSON |
| `scripts/examples/bsp02_ergebnisse_csv.py` | Ergebnisse LF/LK/RK → CSV |
| `scripts/examples/bsp03_kopie_aendern_rechnen.py` | sicherer Ablauf Kopie → ändern → rechnen → speichern + Protokoll |
| `scripts/examples/bsp04_modell_erzeugen.py` | neues Modell (offizielles C#-Beispiel in Python) |
| `scripts/rfem5_selftest.py [--out …SANDBOX…]` | Selbsttest Lesen+Schreiben+Rechnen in 16 Schritten (PASS/FAIL, JSON+MD) – **vor jeder Projektarbeit laufen lassen** |
| `scripts/rfem5_paths.py [--json f] [--backup ordner]` | Pfadinventar RFEM/Python/Registry, Sicherung der Benutzer-Einstellungen (ZIP + SHA256SUMS) |
| `scripts/rfem_interfaces_probe.py [--key-name N]` | Schnittstellen-Landkarte live: RF5 COM, RF6 gRPC (mit/ohne Key), SOAP 8081, Installationen/MCP – Key nie ausgegeben (Handbuch Kap. 16) |

RFEM 6 / dlubal.api: Stand 17.11.2026 **blockiert** (Key/Abo/Lizenzserver) – Details und Freischaltschritte Handbuch Kap. 16. CAD/BIM-Daten (DXF/IFC/CSV/RF6) → Skill **`cad-statik-pipeline`**.

Freigabestufen (wie `rfem6-mcp-engineering`): **G0** nur lesen · **G1** freigegebene Werte an Arbeitskopie ändern + rechnen · **G2** Topologie/Lagerkonzept nur nach Entscheidung des Tragwerksplaners · **G3** Quelle überschreiben nur mit Freigabe + Vorgänger + Hash · **G4** Ingenieurfreigabe nur durch Menschen. Bei unklarer Modellidentität, Einheitenkonflikt, fehlgeschlagenem Rücklesen oder fehlender Konvergenz: stoppen und dokumentieren.

Rechenverfahren per COM (je LF/LK `GetAnalysisParameters()`): `AnalysisMethodType` (Th. I/II/III. O., postkritisch), `SolvingSystemMethodType` (Newton-Raphson, NR+Picard, Picard, NR konst. Matrix, modif. NR, Dynamische Relaxation) – immer mitprotokollieren. Benchmarks für Seile: Dlubal VE 0079/0080/0039/0205/0106 (Handbuch Kap. 14).

Alle Skripte offline gegen die Typbibliothek geprüft und live getestet (RFEM 5.29.01, 17.11.2026). Trotzdem nur an Kopien arbeiten.

| Regel | Grund |
|---|---|
| **comtypes, nicht win32com** | RFEM 5 bietet kein IDispatch → win32com: „Schnittstelle nicht unterstützt“ |
| `GetActiveObject` statt `CreateObject` | hängt sich an die offene Instanz; CreateObject startet eine neue |
| `LockLicense()` … `finally: UnlockLicense()` | nur ein Client gleichzeitig; Abbruch ohne Unlock blockiert RFEM (dann Task-Manager) |
| Python **ohne** `-I` starten | `-I` blendet User-site-packages (comtypes) aus |
| 64-bit-Python | Typbibliothek RFEM5_64 |
| COM-Server fehlt | `RFEM64.exe /RegServer` (Admin), Start als Server: `RFEM64.exe /Automation` |
| Lizenz | `app.IsComLicensed()` – Schreiben/Rechnen braucht RF-COM |

## 2. Wichtige Pfade (RFEM 5.29, dieser Rechner)

| Zweck | Pfad |
|---|---|
| Programm | `C:\Program Files\Dlubal\RFEM 5.29\` (`RFEM64.exe`, `RFEM.ini`, `RFEM64.exe.config`, `Help\RFEM_DEU.pdf` Handbuch) |
| **COM-Typbibliothek** | `C:\Program Files\Common Files\Dlubal\RFEM5_64.dll` (+ Add-on-TLBs `STEEL_EC3_64.tlb`, `RF_CONCRETE_S_64.tlb`, `RF_DYNAM_64.tlb`, `RF_STABILITY_64.tlb`, `CONCRETE_M_64.tlb`, `STEELM_64.tlb`, `ALUMINIUM_64.tlb`, `DSTVA_64.tlb`) |
| COM-Registrierung | `HKCR\RFEM5.Application` (CLSID `{5C397AC7-A317-4EE3-887C-0416236A44B1}`) · Benutzereinstellungen `HKCU\Software\Dlubal\RFEM\5.29` |
| **SDK / Doku COM** | `C:\Users\Public\Documents\Dlubal\SDK\RF-COM-5.chm` (Methodenreferenz), `SDK\Examples\RFEM\{C#,VB.NET,Excel}`, `SDK\Reference Assemblies\x64\Dlubal.RFEM5.dll/.xml` (.NET-Interop, XML = Methodendoku) |
| **Excel-Vorlagen COM** | `C:\Users\Public\Documents\Dlubal\SDK\Examples\RFEM\Excel\RF-COM-5 - Model Data.xlsm` (`Templates\Base` ist leer), `… - Loads.xlsm`, `… - Results.xlsm`, `… - Isolines.xlsm`, `Member effective lengths.xlsm` |
| Beispielmodelle | `C:\Users\Public\Documents\Dlubal\Projects\Examples\RFEM-Beispiel-0x.rf5` |
| Blöcke (Bauteilbibliothek) | `C:\Users\Public\Documents\Dlubal\Blocks\<Kategorie>\…\*.rss` (1.159 Blöcke in Unterordnern) |
| **Stammdaten (global)** | `C:\ProgramData\Dlubal\RFEM 5.29\General Data\`: `Materialien.dbd` / `Materialien_User.dbd` (Materialbibliothek), `Config\*.rfconf` (Anzeige-/Farbkonfiguration), `Units\*.uni` (Einheitenprofile), `RfemProtocolConfig.cfg` + `ProtocolTextsUser.db3` (**Ausdruckprotokoll-Konfiguration/Texte**), `WIND.db3`, `SNOW.db3`, `Seismic*.db3`, `layers.db3`, `Fasteners.db3`, `Default\` (Werkseinstellungen) |
| Logs | `C:\Users\Public\Documents\Dlubal\Logs\` (Installer, Import/Export) |

Backup vor Änderungen an `General Data` (Kopie mit Hash), sonst gehen Benutzerbibliotheken verloren.

## 3. API-Spickzettel (in Projekten verifiziert)

| Bereich | Aufruf |
|---|---|
| Modelle | `app.GetActiveModel()`, `app.GetModelCount()`, `app.GetModel(i)`, `app.OpenModel(path)`, `app.CreateModel(name)`, `m.GetPath()`, `m.GetName()`, `m.SetName()`, `m.SetDescription()`, `m.Save(path)` (**immer mit Pfad**; ohne Pfad Fehler), `m.Close()` |
| Modelldaten | `d = m.GetModelData()`: `GetNodes()`, `GetLines()` (`NodeList`), `GetMembers()` (`LineNo`, `Type` 9 = Seil, `StartCrossSectionNo`), `GetMaterials()`, `GetCrossSections()`, `GetNodalSupports()`, `GetMemberHinges()`, `GetMemberNonlinearities()`, `GetMemberEccentricities()`, `GetMemberDivisions()`, `GetSurfaces()`, `Get…Count()` |
| Ändern | `d.PrepareModification()` … `d.FinishModification()` (Fehler → `d.CancelModification()`); `ni = d.GetNode(no, R.AtNo); nd = ni.GetData(); nd.X = …; ni.SetData(nd)`; `d.DeleteObjects(R.NodeObject / R.MemberObject / R.LineObject / R.NodalSupportObject, "1,2")`; `d.SetNodalSupport(data)` (Lager: `ReferenceSystem = R.GlobalSystemType`) |
| Lasten | `L = m.GetLoads()`: `GetLoadCases()`, `GetLoadCombinations()`, `GetResultCombinations()`, `L.GetLoadCase(no, R.AtNo)` → `GetNodalLoads()`, `GetMemberLoads()`, `GetLineLoads()`, `GetImposedNodalDeformations()`, `GetAnalysisParameters()`; `L.GetLoadCombination(no, R.AtNo).GetLoadings()`; `L.HasAnyResults()` |
| Rechnen | `C = m.GetCalculation()`: `C.Clean()` (Ergebnisse löschen → echte Neuberechnung), `C.CalculateAll()` (gibt Fehlerliste zurück), `C.GetSettings()`, `GetOptions()`, `GetPrecisionAndTolerance()`, `GetNonlinearities()`, `GetSolverMethod()`, `GetBendingTheory()` |
| Ergebnisse | `r = C.GetResultsInFeNodes(R.LoadCaseType / R.LoadCombinationType / R.ResultCombinationType, no)`: `r.GetAllNodalDeformations()`, `r.GetAllNodalSupportForces(False)` (global), `r.GetMembersInternalForces(True)` (Argument ist **bool**: True = Stabachsen; `MemberNo`, `Location`, `Forces.X` = N) |
| Strukturen → dict | ctypes-Struktur rekursiv über `_fields_` auslesen (siehe Projekt-Skripte `export_pruefdaten.py`) |
| Protokoll | `m.GetProtocols()` liefert nur Kopf-/Nummerierungsoptionen – **Ausdruckprotokoll kann nicht per COM erzeugt/gedruckt werden** (GUI) |

## 4. Fallstricke

- **Einheiten:** Kräfte in **N**, Momente in **Nm**, Längen in **m**, Stablasten roh in N/m → selbst umrechnen.
- **Achsen:** häufig globale **Z nach unten** (`m.GetGlobalZAxisOrientation()`); bei Abgleich mit Vermessung y spiegeln.
- Methode heißt `GetImposedNodalDeformations` (nicht `GetNodalDeformations`).
- RK-Ergebnisse liefern pro Knoten/Stab mehrere Extremzeilen (Max/Min) → selbst min/max bilden.
- `CalculateAll()` ohne vorheriges `Clean()` kann gespeicherte Ergebnisse unverändert zurückgeben (2 s statt Minuten).
- „Speichern unter“ in der GUI speichert das Ausgangsmodell u. U. vorher neu → Hash vorher/nachher prüfen.
- CSV-Export der GUI: Codepage **cp1252**, 2 Kopfzeilen, leere Nummernzeilen („Nr. ohne Inhalt“) filtern.
- Nur eine Instanz/ein Client hält die Lizenz – parallele Skripte/KI-Sitzungen vermeiden.
- Ohne `LockLicense()`: `COMError -2147221230 „Keine Lizenz für die Verwendung dieser Klasse vorhanden“`.
- Anlegen und Löschen in **getrennten** Prepare/Finish-Blöcken; innerhalb eines Blocks nicht rechnen; freie Nummern über `d.GetLastObjectNo(R.NodeObject) + 1`.
- `EnableSelections(True)` bleibt aktiv → `GetNodes()` usw. liefern nur die Auswahl; danach auf False setzen.
- Zielordner muss vor `Save`/`CreateModel` existieren. Spannungen kommen in N/m².
- Querschnittswerte aus der Bibliothek brauchen zusätzlich `RFEM3_64.tlb` (Typbibliothek v3.4).
- Öffentliche Python-Beispiele für RF-COM 5 gibt es nicht; Vorlagen sind Dlubal-VBA/C# (Weblinks im Handbuch Kap. 15) und `BHoM/RFEM5_Toolkit` (C#). RF-COM wird von Dlubal nicht weiterentwickelt.

## 5. Arbeitsregeln (Statik-Projekte)

1. Originale nie öffnen/speichern – nur hash-geprüfte Kopien in einer Sandbox (`--guard SANDBOX`).
2. Vor/nach jeder Änderung SHA-256 + JSON-Protokoll (was, alt → neu, Quelle).
3. Zahlen nur aus Originalunterlagen oder RFEM; abgeleitete Werte kennzeichnen („LLM rechnet nichts“).
4. Nach Änderung zurücklesen und gegen Soll prüfen, erst dann `Save(pfad)`.

## 6. RFEM 6 (Abgrenzung)

RFEM 6: `dlubal.api` (gRPC, Port 9000) – benötigt **API-Key** (Dlubal-Konto), sonst `UNAUTHENTICATED`. Alternative ohne Key: .rf5 in RFEM 6 über *Datei → Öffnen* importieren.
