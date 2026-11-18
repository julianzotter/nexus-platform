---
name: 26_11_17_1928_ID06_REINSCHRIFT_RFEM-CAD-PYTHON-PIPELINE_LEDGER-PENDING
version: 1.0.0
status: REVIEW_CANDIDATE
document_type: reinschrift
timestamp: '2026-11-17T19:28:23+01:00'
timezone: Europe/Vienna
agent_id: ID06
agent_name: Claude
executor: Claude Code (Desktop, Code-Tab)
executor_instance: lokaler Windows-11-RFEM-Host (JUL)
provider: Anthropic
model_id: claude-opus-5-5
role_source: NEXUS-ROLES-v1.1, Manifest §4 (ID06 – Claude, Coding/Implementierung)
source: NEXUS.CAD.SKILLS/26_11_17_RFEM-CAD-PYTHON-Pipeline.md (755 Zeilen, Stand 19:26, SHA-256 1e69d3e169d699f3…) – Arbeitsprotokoll ID01/ID06
ablage: [WORK, NEXUS.CAD.SKILLS, GitHub julianzotter/nexus-platform WORK/REPORTS (PR #97)]
ticket_id: null
ledger_id: null
REGISTRATION_STATUS: REGISTRATION_PENDING
FINAL_RELEASE: HUMAN_SIGNOFF_REQUIRED
---
# REINSCHRIFT – RFEM-CAD-Python-Pipeline (17.11.2026)

Diese Reinschrift fasst das Arbeitsprotokoll geordnet, ohne Wiederholungen und auf aktuellem Stand zusammen.
Zahlen stammen aus Live-Läufen, aus der Typbibliothek bzw. dlubal.api-Code oder aus den genannten Dateien. Geschätzt ist nichts.

---

## 1 · Auftrag (ID01, konsolidiert)

| Nr | Auftrag |
|---|---|
| A1 | RFEM 5.29 über die COM-Schnittstelle verbinden: allgemeines Skript `rfem_connect.py` und Skill `rfem5-com`, installiert unter `~/.claude/skills/rfem5-com/` |
| A2 | Wichtige Pfade und Schnittstellen für deterministische Skript-Workflows: COM-Doku und Beispiele, RF-COM-5-Daten (Geometrie, Lasten, Resultate), Materialbibliothek, Programmeinstellungen, Ausdruckprotokoll, Rechenbeispiele, Registry |
| A3 | Ablage im Google Drive mit Sicherungen: `LLM-LOCAL-SSOT › NEXUS.CAD.SKILLS › rfem5-com`; Statusbericht in NEXUS-Syntax unter `LLM-LOCAL-SSOT › WORK` |
| A4 | github.com/julianzotter nach RFEM-Anbindungen durchsuchen; Skill als eigenen Branch in `nexus-platform/plugins/nexus-aec-engineering/skills/` ablegen, als Gegenstück zu `rfem6-mcp-engineering`; Pull Request eröffnen |
| A5 | Live-Test gegen das laufende RFEM: Lesen, Schreiben, Syntax, Befehlsübersicht, Fallstricke, Arbeitsregeln, Typbibliothek |
| A6 | Rechenverfahren, Benchmark-Rechenbeispiele und Linkliste recherchieren; Benutzerhandbuch zur RFEM-COM-Anwendung |
| A7 | Bestehende Dateien analysieren und Skills/Handbuch erweitern: RFEM-6-Dokumente, Python-Skripte, NEXUS-Sync-Dokument, Ordnerliste `_developement`, `D:\RFEM` |
| A8 | Gültige Testdaten für die CAD-Pipeline DXF/IFC → RFEM finden; Beispiele und Vorlagen; Formate SQLite, IFC, CSV, JSON, DXF, DWG, RF5, RF6 |
| A9 | PowerShell-Skript zum Prüfen der API-Keys in `C:\zotter_ai\keys`; Umgebungsvariablen analysieren; vorhandene Dlubal-Keys verwenden |
| A10 | Freien DWG-Konverter nutzen (nicht kommerziell, Testzweck); Flächen und Lasten beim Schreiben nach RF5; öffentliche Testdaten (buildingSMART, SAF) |
| A11 | Lokale Wege ohne Key in Skill und Handbuch einarbeiten: RFEM 5 COM, RF6-Datei/IFC-Export, SOAP-Webservice |
| A12 | Schnellübersicht des Status; nächste Schritte; Rollen-ID von Claude verwenden; diese Reinschrift in WORK, NEXUS.CAD.SKILLS und auf GitHub ablegen |

## 2 · Ergebnisse

### 2.1 Skill `rfem5-com` (v1.2) – RFEM 5.29 über COM
- **Verbindung:** nur über `comtypes` mit der Typbibliothek `C:\Program Files\Common Files\Dlubal\RFEM5_64.dll`. `win32com` scheitert, weil RFEM 5 kein IDispatch anbietet. Ablauf: `GetActiveObject` → `LockLicense()` → Arbeit → im `finally`-Block `UnlockLicense()`.
- **Werkzeuge** (Ordner `scripts/`):

  | Skript | Zweck |
  |---|---|
  | `rfem_connect.py` | Verbindung, `rfem_session()` |
  | `rfem5_api_inspect.py` | API-Referenz direkt aus der Typbibliothek: 114 Interfaces, 184 Strukturen, 116 Aufzählungen |
  | `rfem5_selftest.py` | Selbsttest in 16 Schritten, **live 16/16 PASS** am 17.11. um 18:31 und 19:16 |
  | `rfem5_paths.py` | Pfadinventar (1.270/1.270) plus Sicherung der Einstellungen |
  | `rfem_interfaces_probe.py` | Prüfung aller RFEM-Schnittstellen |
  | `examples/bsp01–04` | Beispiele, alle live PASS |

- **Handbuch** `references/BENUTZERHANDBUCH_RFEM5_COM.md` v1.2 mit 21 Kapiteln: Rezepte, Einheiten und Achsen, Fehlerbilder, Freigabestufen G0–G4, Pfade und Sicherung, Rechenverfahren (aus der Typbibliothek), Benchmarks (Dlubal-Verifikationsbeispiele, NAFEMS, VDI 6201), Linkliste, Schnittstellen-Landkarte, Integrationswege, Analyse der Bestandsskripte, CAD-Pipeline, Architekturprinzipien.
- **Korrekturen und Befunde:**
  - `GetMembersInternalForces` erwartet bool. Die Böblingen-Ergebnisse sind trotzdem korrekt, weil der übergebene Wert 2 als `True` gilt.
  - Lagerkräfte haben dasselbe Vorzeichen wie die Lasten.
  - Die Excel-Vorlagen liegen unter `SDK\Examples\RFEM\Excel\`, nicht unter `Templates\Base`.

### 2.2 Skill `cad-statik-pipeline` (v1.0) – CAD/BIM ↔ neutrales Statikmodell ↔ RFEM
- **NSM** (`nsm.py`): Knoten, Stäbe, Lager und Flächen; Ein-/Ausgabe als JSON, CSV und SQLite (inkl. View `member_geometry`); `validate()` und `fingerprint()`.
- **Leser und Schreiber** (`formats.py`):
  - DXF: RFEM-Export und generische Zeichnung, mit Umriss-Modus und Einheitenumrechnung
  - IFC: Statikmodell und physische Achsen
  - RF5: lesen über COM an einer Kopie, schreiben nur als neues Modell unter `SANDBOX`
  - RF6: Inventar aus ZIP + SQLite, ohne API
  - RFEM-CSV-Tabellenexport
  - DWG: über GNU LibreDWG
- **Kommandozeile** (`pipeline.py`): `inspect`, `convert`, `compare` (unabhängig von der Nummerierung, `--2d`), `learn-map`, `rf5-active`.
- **Tests:** 8 Offline-Tests PASS. Testsammlung K01–K08 mit Prüfsummen in `references/testkorpus.json`:

| ID | Fall | Ergebnis |
|---|---|---|
| K01 | EIS26 BETONBAU: DXF ↔ IFC ↔ RF5 (1.519 Knoten, 376 Stäbe) | 3× PASS, höchstens 6 µm |
| K02 | IFC → NSM → neues RF5 → zurückgelesen | PASS (gegen IFC und gegen Original-RF5) |
| K03 | Böblingen 5e: RFEM-CSV ↔ RF5 (86 Knoten, 88 Stäbe, 35 Lager) | PASS, höchstens 0,49 mm |
| K04/K05 | Plan-DXF (Umrisse, mm) ↔ IFC4 physisch | PASS (2D) |
| K06 | RF6-Inventar ohne API | PASS |
| K07 | DWG AC1032 | jetzt **umgewandelt** (LibreDWG 0.14): 98.649 Linien auf 185 Layern; Layerfilter in Arbeit |
| K08 | Synthetisches Fachwerk | PASS |

- **Wichtigste Regeln aus den Tests:**
  - RFEM-System (Z nach unten) ↔ IFC/Welt (Z nach oben) = **Drehung 180° um X**, also (x, y, z) → (x, −y, −z).
  - Im RFEM-DXF ist jeder Knoten ein Würfel aus 12 Kanten. Gezählt werden nur vollständige Würfel (mit 1 mm Fangradius).
  - Die Namenszuordnung (z. B. IFC `300X1100` → RFEM `Rechteck 300/1100`) wird nur aus einem PASS-Paar abgeleitet und ist eine G2-Entscheidung.

### 2.3 Schnittstellen (live, 17.11.2026)

| Weg | Status | Befund |
|---|---|---|
| RFEM 5.29 über COM | ✅ | ohne Key, vollständig getestet |
| RF6-Datei direkt (ZIP + SQLite) | ✅ | Inventar ohne Key |
| RF6 → IFC-Export → CAD-Pipeline | ✅ | Weg geprüft (K01/K02 mit RFEM-IFC) |
| RFEM 6.12 gRPC (Port 9000) | ⛔ | ohne Key: `API key is in incorrect format`; mit **allen drei vorhandenen Dlubal-Keys** `The API key is either missing or invalid` |
| RFEM 6 SOAP-Webservice (8081) | ⛔ | im Optionsdialog aktiviert, aber **kein Port offen** (live geprüft); API I gilt als veraltet |
| Dlubal-MCP | ⛔ | erst ab RFEM 6.13.0002, installiert ist 6.12 |

**Behauptung „lokaler Zugriff ohne Key/Extranet“ widerlegt:** Die Zeile `api_key_value=None … port=9000` ist nur die Standardsignatur von `rfem.Application()`. Der lokale Server prüft den Key.

### 2.4 Keys und Umgebungsvariablen (nur Fingerabdrücke, keine Werte)
- **Dlubal-Keys:** Es gibt drei verschiedene (je 51 Zeichen). Alle sind **ungültig** für RFEM 6.12:
  - Key-Store `nexus_aec_engine` (`6a169f28afba`)
  - Drive-Textdatei `_RFEM-MCP-SERVER-REPO_RFEM5-COM-Schnittstelle_.txt` (`d37afae812be`)
  - Claude-HTML-Export (`dd16c94ef566`)
- In `C:\zotter_ai\keys` liegt **kein** Dlubal-Key.
- **Umgebungsvariablen:**
  - 13 Benutzer- und 1 Systemvariable mit Key-Bezug; **keine RFEM- oder Dlubal-Variable**.
  - Doppelt belegt: `OPENAI_API_KEY` = `DeepSeek-Bridge` = `DeepSeek-Bridge1`; `GEMMA_API_KEY` ist zusätzlich als Systemvariable gesetzt und damit für alle Benutzer lesbar.
- `SCRIPTS/Check-ApiKeys.ps1`: 8 Keys in 7 Dateien, Ausgabe nur maskiert. In `C:\zotter_ai\keys` dürfen alle angemeldeten Benutzer ändern.

### 2.5 Quellenanalyse
- `D:\RFEM`: Exportpaar `EIS_Gesamt_26_BETONBAU` (rf5/dxf/ifc), RF6-Beispiele, kleine Testmodelle, HBV-Vorlagen. **Kundendaten**, daher nur lokal.
- Ordnerliste `_developement`: 278 Kernfunde in `26_11_17_RFEM-QUELLEN_TREE-ANALYSE_ID06.md`. Wiederverwendbar:
  - `boeb_rfem5_readonly_audit.py`
  - `RFEM6_MCP_Bridge_Extended.py` (gepinnt auf dlubal.api 2.12.8 / RFEM 6.12)
  - `rfem_adapter.py` (Mock-fähig)
  - DXF/IFC-Testfälle aus `PARAMETRIC-DESIGN-TEST`
- Bestandsskripte:
  - `precast_residential_building.py`: `Surface(thickness=0.20)` → TypeError, weil `thickness` die Nummer eines Thickness-Objekts ist.
  - Das RF6-Dokument vom April 2026 vermischt API I und API II.
- GitHub: Freigabestufen G0–G4 und Vorgaben für Nachweisdateien aus `rfem6-mcp-engineering` übernommen.

### 2.6 Öffentliche Testdaten (geladen in `D:\RFEM_SANDBOX_CAD\OEFFENTLICH\`)

| Datei | Quelle | Größe / SHA-256 (16) | Stand |
|---|---|---|---|
| `structural-curve-member.ifc` | buildingSMART IFC4.x-specification-models (IFC4X3, Einheiten Zoll/lbf, Lastkonfiguration) | 15.275 B / `9ccd7cc699cddf11` | Leser-Anpassung in Arbeit |
| `SAF_example_HOUSE_metric_ZYX_220.xlsx` | StructuralAnalysisFormat-Examples 2.2.0 | 133.350 B / `5b0f8271edfcad66` | SAF-Leser in Arbeit |
| `libredwg-0.14-win64.zip` (`dwg2dxf.exe`) | GNU LibreDWG 0.14, GPL-3, nur Testzweck | 12.084.779 B / `1ad7e15344d20b34` | in Pipeline eingebunden; Signatur vorhanden, Schlüssel nicht importiert |

## 3 · Ablage

| Was | Ort |
|---|---|
| Skills (SSOT) | `LLM-LOCAL-SSOT\NEXUS.CAD.SKILLS\rfem5-com\`, `…\cad-statik-pipeline\` |
| installiert | `%USERPROFILE%\.claude\skills\rfem5-com\` (14 Dateien), `…\cad-statik-pipeline\` (17 Dateien), Hash-Abgleich 0 Abweichungen |
| Sicherungen | `NEXUS.CAD.SKILLS\rfem5-com_BACKUPS\`: Skill-ZIPs 19:16, RFEM-Einstellungen 18:30 |
| Selbsttest-Protokolle | `LLM-LOCAL-SSOT\TESTS\RFEM5_COM_SANDBOX_SELFTEST\` |
| Statusberichte | `WORK\26_11_17_1917_ID06_STATUSREPORT_RFEM-CAD-PYTHON-PIPELINE_LEDGER-PENDING.md` (ersetzt `…1835_ID-UNVERIFIED…`) |
| GitHub | Branch `feat/rfem5-com-cad-statik-pipeline-ID06`, **PR #97** (offen) |
| lokale Prüfdaten | `D:\RFEM_SANDBOX_CAD\` (Kundendaten, nicht in Drive/Git) |
| Werkzeuge | `C:\zotter_ai\tools\libredwg-0.14\`, `LLM-LOCAL-SSOT\SCRIPTS\Check-ApiKeys.ps1` |

## 4 · Schnellübersicht des Status

Legende: ✅ erledigt und geprüft · ⚠ mit Einschränkung · 🔄 in Arbeit · ⏸ offen · ⛔ blockiert · 🔴 ID01 muss handeln

| # | Punkt | Status |
|---|---|---|
| 1 | Skill rfem5-com + Installation + Sicherung | ✅ |
| 2 | Pfade, Registry, Material, Einstellungen, Protokoll-Konfiguration | ✅ (das Ausdruckprotokoll selbst nur in der GUI) |
| 3 | Selbsttest RFEM 5 live | ✅ 16/16 |
| 4 | Benutzerhandbuch rfem5-com v1.2 | ✅ |
| 5 | Benchmarks, Algorithmen, Linkliste | ✅ (Dlubal-VE-Modelle nicht geladen) |
| 6 | GitHub durchsucht, Branch, PR #97 | ✅ (Review durch ID03/ID07 offen) |
| 7 | Skill cad-statik-pipeline + Handbuch + Testsammlung | ✅ |
| 8 | DWG-Konverter (LibreDWG) | ✅ eingebunden · 🔄 Layerfilter `--layers` |
| 9 | Flächen nach RF5 schreiben | 🔄 |
| 10 | Lasten lesen/schreiben (IFC, RF5) | 🔄 (Analyse fertig: 12 Lastfälle RF5, 8 Lastgruppen IFC, leere Objektlisten im Bestand) |
| 11 | buildingSMART-IFC4X3 und SAF als Testfälle | 🔄 (geladen, Leser folgt) |
| 12 | Lokale Wege ohne Key in Skill/Handbuch | ⚠ (Kap. 16 enthält sie; SOAP-Befund und Key-Ergebnis werden nachgetragen) |
| 13 | RFEM 6 gRPC / MCP | ⛔ (alle Keys ungültig) |
| 14 | SOAP-Webservice RF6 | ⛔ (kein Port offen) |
| S1 | Klartext-Dlubal-Keys in Drive-Dateien bereinigen | 🔴 |
| S2 | ACL `C:\zotter_ai\keys` einschränken | 🔴 |
| S3 | `GEMMA_API_KEY` als Systemvariable (alle Benutzer) | 🔴 prüfen |

## 5 · Nächste Schritte

| Prio | Schritt | Wer | Abnahme |
|---|---|---|---|
| P0 | Flächen und Lasten in `write_rf5` und den Lesern fertigstellen, mit Lastsummen-Vergleich je Lastfall | ID06 | K02 mit Flächen und Lasten PASS |
| P0 | bSI-IFC4X3 (Zoll/lbf, Lastkonfiguration) und SAF-Leser als Testfälle K09/K10 | ID06 | Knoten, Stäbe und Lasten plausibel, Einheiten in SI |
| P0 | Layerfilter für DWG/DXF, Testfall Stützenplan | ID06 | Stützen-Layer → Stützenpunkte |
| P1 | Review von PR #97 (Architektur, QA) | ID03, ID07 | drei Perspektiven, Delta-Korrektur |
| P1 | gültigen Dlubal-Key beschaffen **oder** SOAP-Port in RFEM 6 prüfen und neu starten | ID01 | `rfem_interfaces_probe.py` PASS |
| P1 | Sicherheit S1–S3 | ID01 | Dateien bereinigt, ACL eng, Variablen geprüft |
| P2 | RFEM-6-Weg: vorhandene `RFEM6_MCP_Bridge_Extended.py` statt Neubau; Update auf 6.13.0002+ für MCP | ID06 nach Freigabe | Healthcheck PASS |
| P2 | `boeb_rfem5_readonly_audit.py` live ausführen und in den Skill übernehmen | ID06 | Audit-JSON + Vergleich |
| P2 | Benchmarks als Regression: Dlubal VE 0079/0080/0039 (Seil) gegen analytische Lösung | ID06 | Abweichung dokumentiert |
| P3 | Ledger-Nummern für die Berichte vergeben (Registrierung) | ID02 | Ledger-Eintrag |

## LOG
- 2026-11-17T19:28+01:00 | ID06 | Reinschrift aus dem Arbeitsprotokoll erstellt (Quelle: SHA-256 1e69d3e169d699f3…), abgelegt in WORK, NEXUS.CAD.SKILLS und GitHub (PR #97).
