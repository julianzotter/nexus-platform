---
name: rfem-anbindung-filefinder
description: RFEM5/RFEM6-Anbindungen (COM, gRPC API-II, Dlubal-MCP, NEXUS-Bridge) – Bestand, Status, Links; plus optimaler Datei-Such-Algorithmus (Routen + SQLite-FTS5) über AnythingSearch-Export
version: 0.1.0
status: Bestand gelesen (3 Primärdateien + 50 Drive-Treffer) · Finder-Modul gebaut + Smoke-Test PASS · NICHT auf RFEM-Host ausgeführt
timestamp: 2026-11-09T08:36:42Z
agent: ID-CL (Claude Fable 5.1)
artifact_number: UNKNOWN (Ledger nicht gelesen, Platzhalter 000)
tasks_done: Memory + 3 Drive-Dateien gelesen · Drive-Sweep RFEM/Dlubal/gRPC · PyPI/Dlubal-Doku geprüft · nexus_file_finder.py v0.1.0 · Linkliste
tasks_open: files.csv aus AnythingSearch.db exportieren (Colab/Lokal) → Index bauen · RFEM6 API-Abo (D03) · dlubal.api Version an installierte RFEM-Version pinnen · Ledger-Nr
problems: RFEM6-gRPC bisher BLOCKED (API-Key/Abo, A04) · Drive-Ordner 00-AnythingSearch/Database leer, keine zerteilten DBs gefunden
open_questions: Welche RFEM-6-Version ist produktiv (6.07/6.11/6.13/6.15 installiert)? · RF5 bleibt primär (Human-Gate 14.10.)?
---

## 0 · TL;DR
- **RFEM 5 (5.29) → COM** funktioniert nachweislich (21.10.2026): `comtypes` + `RFEM5.Application` + **`LockLicense()`** vor jedem Zugriff; 86 Knoten / 88 Stäbe / 27 Lager gelesen, `CalculateAll` verfügbar. Ohne LockLicense: Fehler „Keine Lizenz für die Verwendung dieser Klasse“.
- **RFEM 6 → gRPC API-II** (`dlubal.api`, Port 9000): Bridge-Code vorhanden (NEXUS RFEM6_MCP_Bridge v1.0.0, read-only, STDIO/HTTP), aber **BLOCKED** bis API-Abo/Key bestätigt (Blocker D03/A04). SDK-Minor muss zur RFEM-Minor passen (6.15 ↔ 2.15.*).
- **Offizieller Dlubal-MCP** (`dlubal-mcp` ≥ 1.0.17, STDIO, Tools `read_rfem_results`, `run_rfem_script`) ist der kürzeste Weg für Claude Code/Codex – ersetzt Eigenbau für Standardfälle.
- **File-Finder**: AnythingSearch.db → `files.csv` (bestehendes `anythingsearch_refresh.py`) → `nexus_file_finder.py` (Routentabelle + SQLite-FTS5 Trigram + BM25-Boost). Suche O(log n), Build O(n). Smoke-Test PASS.

## 1 · RFEM-Anbindungen – Matrix (Stand 09.11.2026)
| Weg | Version | Technik | Status im Bestand | Primärquelle |
|---|---|---|---|---|
| **A · COM (RF-COM)** | RFEM 5.29 | `comtypes.client.GetModule(RFEM5_64.dll)` → `GetActiveObject("RFEM5.Application")` → `LockLicense()` → `GetActiveModel().GetModelData()` | ✅ **geprüft 21.10.** Lesen + Methoden-Inventar; Schreiben via `PrepareModification/FinishModification` beschrieben, nicht protokolliert | Drive #1 PS-Transkript; #6 BERICHT_RFEM5_COM |
| **B · gRPC API-II** | RFEM 6.x | `pip install dlubal.api==2.<minor>.*`; `rfem.Application(api_key_value=…, url=127.0.0.1, port=9000)`; Server startet mit GUI oder `RFEM6Server.exe --start-grpc-server=9000` | ⛔ **BLOCKED** (Key/Abo D03); Healthcheck-Skript + Bridge fertig | PyPI dlubal.api; apidocs.dlubal.com; Drive #2, #7, #8 |
| **C · Dlubal-MCP (offiziell)** | RFEM 6 / RSTAB 9 / RSECTION | `py -3.12 -m venv %USERPROFILE%\dlubal-mcp` → `pip install dlubal-mcp "dlubal.api==2.15.*"`; `.mcp.json` command=…\Scripts\python.exe args=["-m","dlubal_mcp","--transport","stdio"]; Ports 9000/9001/9002; `DLUBAL_MCP_ALLOW_SCRIPTS=false` zum Härten | 🟡 dokumentiert, nicht installiert | apidocs.dlubal.com/installation_mcp.html |
| **D · NEXUS RFEM6_MCP_Bridge** | RFEM 6.12.0008 (SDK 2.12.8 gepinnt) | FastMCP, read-only Tools `rfem_health`, `rfem_read_objects`, `rfem_read_results`; `--export` → INPUT_MODELL.txt + MANIFEST.json + SHA256; `--compare`, `--verify` | 🟡 Code vollständig, Lauf nicht belegt (PRECHECK_BLOCKED) | Drive #2; #3 Skills-Report |
| **E · WebService API-I (HTTP/SOAP, RFEM_Python_Client)** | RFEM 6 (Legacy) | Port 8081, `RfemPythonWsClient` | ⚪ bekannt, im Bestand nicht genutzt; Dlubal führt API-II (gRPC) als Nachfolger | Dlubal GitHub (nicht neu geprüft) |
| **F · RF5-CSV → RF6** | RF5 → RF6 | Export Tabellen (.xlsx) aus RF5, Skill „RF5-CSV-RFEM6-SEILSTATIK“ | 🟡 Skill + Wegweiser vorhanden | Drive #13, #14 |

**Empfehlung (Entscheidungsgrundlage)**
1. Produktiv jetzt: **A (RF5-COM)** – läuft, Lizenz vorhanden, Modell 5e ist Human-Gate-Basis.
2. Sobald API-Abo bestätigt: **C (Dlubal-MCP)** für Lesen/Skripte aus Claude Code; **D (NEXUS-Bridge)** nur, wo Audit-Export (Hash, Manifest, Verify) gebraucht wird.
3. Versionsregel: `dlubal.api` Minor = RFEM Minor; nach RFEM-Update `pip install --upgrade "dlubal.api==2.<neu>.*"`.
4. Keys: nur lokal (`%LOCALAPPDATA%\NEXUS\RFEM-MCP\credentials.json` bzw. Dlubal-Key-Store), nie in Drive/Repo.

### Minimal-Snippets (geprüft im Bestand)
```python
# A · RFEM5 COM (comtypes) – read-only Inventar
import comtypes.client as cc
m = cc.GetModule(r"C:\Program Files\Common Files\Dlubal\RFEM5_64.dll")
app = cc.GetActiveObject("RFEM5.Application", interface=m.IApplication)
app.LockLicense()
try:
    model = app.GetActiveModel(); md = model.GetModelData()
    print(model.GetPath(), md.GetNodeCount(), md.GetMemberCount())
finally:
    app.UnlockLicense()
```
```python
# B · RFEM6 gRPC – Healthcheck (Drive #8, read-only)
from dlubal.api import rfem
with rfem.Application(url="127.0.0.1", port=9000, api_key_value=KEY) as app:
    print(app.get_application_info().version, app.get_active_model().guid)
```
```json
// C · Dlubal-MCP in .mcp.json (Claude Code) – Skripte deaktiviert
{"mcpServers":{"dlubal-mcp":{"command":"C:\\Users\\<u>\\dlubal-mcp\\Scripts\\python.exe",
 "args":["-m","dlubal_mcp","--transport","stdio"],"env":{"RFEM_API_PORT":"9000","DLUBAL_MCP_ALLOW_SCRIPTS":"false"}}}}
```

## 2 · Bestand – Links nach Stichwort (Drive)
Format: `#NR, NAME, URL` · Stichwort-Tags in [ ]

**[RF5] [COM] [Python]**
- #1, PS-COM-gRPC-Transkript 21.10., https://drive.google.com/file/d/1Sm_ELlci5gO8hJzjb1F2q2WxssMpZyi9/view (Duplikat 1mg1P5AKeNjKOb5NHOy6H5G4aOsvBYfS7)
- #6, BERICHT_RFEM5_COM_Seilstatik, https://drive.google.com/file/d/1uf4MUpiiqFiOJMO8DRC9UjvrseMreZOW/view
- #9, Ordner RFEM5_COM_Seilstatik, https://drive.google.com/drive/folders/17I2jE-bhDkq0xrgwerG9ojwMn1Avvf13
- #10, RFEM 5.29 COM-Schnittstelle.docx, https://drive.google.com/file/d/1s-4lsziKlaISqAEB70qAFD24vOdC-Nyd/view
- #11, RFEM-MCP-SERVER-REPO_RFEM5-COM.txt, https://drive.google.com/file/d/1c97AyJyiV07wA33JsTwqvcpH5lPIcuLr/view
- #12, 5e-Modell BOEB_BESTAND (.rf5), https://drive.google.com/file/d/1iJuUNvSDlwgsHpFHA6k4ZAFLnOTfNwGc/view
- #17, Seilstatik-Workflow RFEM5, https://drive.google.com/file/d/1ClnuoNwqzYT8yJtqF8EgDfW5VXpF95cC/view

**[RF6] [gRPC] [API-II] [Python]**
- #2, RFEM6-MCP-Bridge-Extended (Quelle+Linkliste), https://drive.google.com/file/d/1n24WxD7lp0lpdZs-SF-YHBJNh5KplLTn/view (.py: 1fB_qPiucUdvq7LW01_GuEx7yayA6trgr)
- #7, Authentication/Starting Server (gRPC), https://drive.google.com/file/d/17Mi2IuaT2K7sxbj-O8jTc4YCj2GtusD-/view
- #8, healthcheck_rfem_grpc.py, https://drive.google.com/file/d/1hjNr53Z8hMKK-c8dcrZY0lQKqgC483k5/view
- #15, Python-Script Dlubal-API-gRPC.py (108 KB), https://drive.google.com/file/d/1FYqqqYCXVXzYLj4n3UoMXJGVcuorzA3q/view
- #16, RFEM6 API+Lizenzstatus prüfen (Claude.html), https://drive.google.com/file/d/1eoJcwqH-Ouo17p9RA4Xzh_3HX14j-tf9/view
- #18, Dlubal-API-Doku Application.url, https://drive.google.com/file/d/1E8qS_dlJX8vjqQhjZblHPdhYeLpT3mXC/view
- #19, RFEM-6-Teilmodell.txt, https://drive.google.com/file/d/1t9W_s_3mqzdvoc6ACfMnRGqCcb9wTAeb/view

**[MCP] [Skills]**
- #3, AEC-RFEM-Skills v0.1.0 Report, https://drive.google.com/file/d/123aMWkOsdd_Zg-3hmaMtJcg8tbImNV3A/view
- #20, Ordner rfem6-mcp-engineering, https://drive.google.com/drive/folders/1EMRXq0F6w4_Kvs-JycwZ0pO8tv0caHlS
- #21, 26_09_16_MCP_RFEM_Implementierung.md, https://drive.google.com/file/d/1gPCACw459SvO49zhky8kg0IV3Bt2cMUL/view
- #22, Copilot-RFEM-6-LLM-API-Pilotworkflow.docx, https://drive.google.com/file/d/1dIktSQoGvaEYXFKWufGBaMmYCqtw0nLV/view
- #23, Copilot-Linkliste Dlubal MCP+KI, https://drive.google.com/file/d/1erQgu8ODG29o1lyMnqe4JcqtqYhlyxPG/view
- #24, TECHNISCHES DOSSIER RFEM-MCP-API-CSV-SKILL.docx, https://drive.google.com/file/d/1lfWu1whO1zPbdkq9cHsJghoG5O8xPnA_/view
- #25, rfem5-rfem6-api-bruecke-readme.pplx.md, https://drive.google.com/file/d/1jH7X_njC53UpSx7JQT2Ku8o-icmxZy9_/view
- #26, copilot workflow-api-dlubal-RF5-RF6+.md, https://drive.google.com/file/d/1un6mttXa8Zh18hzYspc5U0G14kgdaSuo/view

**[RF5→RF6] [CSV] [Inventur]**
- #13, RF5-CSV-RFEM6-SEILSTATIK_SKILL, https://drive.google.com/file/d/1m_3ykp31kbudSqRIFXAgGccA3W05CoE7/view
- #14, RF5-CSV-RFEM6-SEILSTATIK_WEGWEISER, https://drive.google.com/file/d/1-XwTNgHi3SZUd14IwcbgV3dx1ZuaJonj/view
- #27, AnythingSearch '.rf5' RFEM5-FILES-INVENTARY (740 KB), https://drive.google.com/file/d/1JVYmi3cLWDanjwGBhwYSDHofnyMMw7t8/view
- #28, RFEM-INVENTUR-DELTA v1.26.0, https://drive.google.com/file/d/11zL6IsksHZM_WyNzQc_82N5Ug7Ah6gwd/view
- #29, RFEM_STATUS_KEYVALUES_BRIDGETEST, https://drive.google.com/file/d/1heFLajMJOJgJw4xBZh_g4YewHyeUUj57/view
- #30, TABELLEN_5e_RFEM-EXPORT.xlsx, https://drive.google.com/file/d/11CH2-I6ZFtX7gE0nHlHlqFsQttinQYlu/view

**[Sammlungen]**
- #5, KB-007 DXF+IFC+RFEM-GPT, https://drive.google.com/drive/folders/1gVFfmyQZk1viZDHjGj8xVZGz3CXo8jt2
- #31, 22-BENCHMARK DLUBAL, https://drive.google.com/drive/folders/1P4lPd6xCS0qjbpU73eiEdfQDfKtqMAh7
- #32, CLAUDE RFEM6 INTEGRATION (API-KEY–MCP).docx, https://drive.google.com/open?id=1DtypVIbt8pe34v2pOPwm4xsuVMCfVlTB
- #33, RFEM-API-Internet-Recherche-FAQ 06.07., https://drive.google.com/open?id=1tB_yLqBQe3QkIRy82dy9y_LQK3gcv2TH
- #34, RFEM 6 MCP Engineering Workflow.txt, https://drive.google.com/open?id=1xIw6gQkANRpqvWlvshXv2JxCOOT1hG1N

**[Extern]**
- #E1, dlubal.api PyPI, https://pypi.org/project/dlubal.api/
- #E2, Dlubal MCP Install, https://apidocs.dlubal.com/installation_mcp.html
- #E3, Dlubal API Docs, https://apidocs.dlubal.com/
- #E4, colab-mcp, https://github.com/googlecolab/colab-mcp
- #E5, MCP Spec, https://modelcontextprotocol.io

## 3 · Optimaler Such-Algorithmus (Datei schnell finden)
**Ziel**: Stichwort (RF5, RF6, API, gRPC, Python, MCP, …) → vollständiger Pfad in < 100 ms, auch vom Handy (Chat liest Ergebnisliste).

**Vergleich**
| Variante | Build | Suche | Substring („rf5“ in „…RFEM529…“) | Ranking | Mobil nutzbar |
|---|---|---|---|---|---|
| Drive-Titelsuche (Connector) | – | ~1 s/Query | nur Titel, kein Pfad | nein | ja (Chat) |
| grep/rg über files.csv | – | O(n) ≈ 0,5–2 s bei 1 Mio Zeilen | ja | nein | nur mit Shell |
| SQLite LIKE | O(n) | O(n) | ja | nein | ja |
| **SQLite FTS5 (trigram) + Routen + BM25-Boost** | O(n) einmalig | **O(log n + k)** | **ja** | **ja** | **ja** (DB in Drive, Colab/Chat liest) |
| Embeddings (Vektor) | teuer | schnell | semantisch, ungenau bei Codes | ja | später (V2-Modul) |

**Gewählt**: FTS5-Trigram (Substring-fähig, exakt bei Kürzeln) + Routentabelle (Domain → Begriffe/Synonyme/Endungen/Pfad-Boosts) + Score = BM25 + 2·(Endung passt) + 1,5·(Pfadwort) + 1·(2026-Datei). Deterministisch, auditierbar, kein Modell nötig.

**Pipeline (4 Schritte)**
1. `python anythingsearch_refresh.py --db G:\…\00-AnythingSearch\AnythingSearch.db --out G:\…\_INDEX_LNK\FINDER` → `files.csv` + `refresh.json` (read-only, bestehendes Skript)
2. `python -I nexus_file_finder.py build --csv files.csv --db nexus_index.db` (einmalig; ~1 Mio Zeilen ≈ 30–60 s, DB ≈ 10–15 % der CSV)
3. `python -I nexus_file_finder.py search --db nexus_index.db --route rfem6_api --q "grpc 9000"`
4. Ergebnis (`score | ext | date | path`) als TXT/CSV nach Drive → am Handy in jedem Chat öffnen; optional Colab-Zelle mit denselben zwei Befehlen.

**Routen (v0.1.0)**: `rfem5_com`, `rfem6_api`, `rfem_mcp`, `python`, `anything` – erweiterbar in `ROUTES` (z. B. `hbv`, `ec5`, `seilstatik`). Deckt die im Chat genannten Stichworte RF5/RF6/API/gRPC/Python/MCP ab; „Global“ = Drive-Root-Suche über denselben Index.

**Plausibilität**: Smoke-Test 5 Zeilen → Route `rfem6_api` liefert Bridge.py (7,42) vor Healthcheck (4,55); Route `rfem5_com` liefert 5e_CALC_KOPIE.rf5 (6,01). Keine Treffer auf irrelevante Datei (Urlaub.jpg). ✓

## 4 · Nächste Schritte (ausführbar)
1. **Lokal/Colab**: Schritt 1–2 der Pipeline → `nexus_index.db` nach `_INDEX_LNK/FINDER/` legen (Move-only-Regel beachtet, Original-DB unangetastet).
2. **RF5**: COM-Skript aus #1 in Modul `rfem5_com.py` überführen (Lizenz-Lock, Kopie-Pflicht, Protokoll) – Grundlage BERICHT #6 Kap. 6–9.
3. **RF6**: D03 klären (API-Abo) → `dlubal-mcp` installieren, `DLUBAL_MCP_ALLOW_SCRIPTS=false`, Healthcheck #8 laufen lassen, Ergebnis in STATUS.
4. Ledger-Nummer für diesen Report nachtragen.

## LOG
- 2026-11-09T08:36:42Z | ID-CL | Bestand gelesen (Memory 2 Dateien, Drive #1 #2 #3 #6 #7 #8, Sweep 50 Treffer), PyPI + apidocs geprüft, Finder v0.1.0 gebaut + Smoke-Test PASS, Report erstellt, archiviert Drive WORK + Repo
