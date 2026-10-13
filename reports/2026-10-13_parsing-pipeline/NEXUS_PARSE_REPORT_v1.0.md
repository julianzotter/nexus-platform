# NEXUS-AI – Technischer Bericht Parsing-Pipeline v1.0
Stand: 2026-10-13 · Projekt: NEXUS-AI Multi-LLM System · Autor: Perplexity Computer (Orchestrator)

## 1 Zweck
Vollständige Inventarisierung der SSOT-Bestände (Google Drive LLM-LOCAL-SSOT) und der NEXUS-relevanten GitHub-Repos (julianzotter) als Basis für Routing, Deduplizierung und Index.

## 2 Pipeline
1. Quelle A/B/C: drei Drive-Ordner gleichen Namens, rekursiv über Drive API v3 (`files.list`, Paging, max. 4000 Objekte/Root).
2. Metadaten: id, Name, MIME, Größe, Änderungsdatum, MD5.
3. GitHub: `gh repo list` gefiltert auf nexus|ai|llm|agent|ssot.
4. Duplikatprüfung: MD5-Gleichheit über alle Roots.
5. Ausgabe: JSON-Inventar, Bericht (MD), Dashboard (HTML).

## 3 Ergebnisse
| Kennwert | Wert |
|---|---|
| Objekte gesamt | 858 |
| Datenvolumen | 1.28 GB |
| Root A (1MDir…) | 2 Objekte |
| Root B (1uBR…) | 3 Objekte |
| Root C (1j3F…) = kanonische SSOT | 853 Objekte |
| MD5-Duplikatgruppen | 27 (55 Dateien) |
| Repos | 17 |

### Dateitypen
- md: 251
- txt: 111
- pdf: 97
- jpg: 93
- ORDNER: 60
- json: 41
- py: 31
- css: 24
- gdoc: 23
- docx: 22
- png: 18
- html: 14
- yaml: 14
- zip: 12

### Top-Ordner (Root C)
- WORK: 200
- BILDER-RAW: 93
- PDF-RAW: 74
- 26_09_19_BOOKKEEPER_v1.0.0: 69
- scratch_gdoc-meta.ai: 64
- NORMEN: 23
- ALT: 14
- scripts: 8
- nexus_os: 4
- HISTORICAL: 3
- 00_ID_LEDGER.csv: 2
- tests: 2

## 4 Bewertung / Maßnahmen
- Root C ist die SSOT (https://drive.google.com/drive/folders/1j3FLJkWpQv6xGA_KO0D9sMyA11f0vxBV). A und B sind Reste (≤3 Objekte) → nach Freigabe in C zusammenführen und archivieren.
- Duplikate meist Root ↔ WORK/ → Original in WORK/ belassen, Root-Kopie durch Verweis ersetzen.
- Rohbestände (PDF-RAW, BILDER-RAW) → nächster Schritt: Text-/OCR-Parsing, Chunking, Vektorindex (Chroma/Qdrant laut Work Order 26_10_06).

## 5 Artefakte
| Datei | Inhalt |
|---|---|
| NEXUS_PARSE_REPORT_v1.0.md | dieser Bericht |
| NEXUS_PARSE_INVENTORY_v1.0.json | Vollinventar (Drive + Repos + Duplikate) |
| NEXUS_PARSE_DASHBOARD_v1.0.html | interaktives Dashboard (Suche, Filter, Charts) |
| parse.py | reproduzierbares Pipeline-Skript |
