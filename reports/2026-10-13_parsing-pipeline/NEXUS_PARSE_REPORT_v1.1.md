# NEXUS-AI – Technischer Bericht Parsing-Pipeline v1.1
Stand: 2026-10-13 (v1.1: OCR + Vektorindex) · Projekt: NEXUS-AI Multi-LLM System · Autor: Perplexity Computer (Orchestrator)

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
- 26_09_19_BOOKKEEPER_v1.1.0: 69
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
| NEXUS_PARSE_REPORT_v1.1.md | dieser Bericht |
| NEXUS_PARSE_INVENTORY_v1.1.json | Vollinventar (Drive + Repos + Duplikate) |
| NEXUS_PARSE_DASHBOARD_v1.1.html | interaktives Dashboard (Suche, Filter, Charts) |
| parse.py | reproduzierbares Pipeline-Skript |

## 6 Erweiterung v1.1 – OCR-Parsing und Vektorindex
Umfang: Root C, Textdateien < 2 MB, PDF/Bilder < 5 MB, Google Docs (Export text/plain) = 671 Dateien.

| Methode | Dateien |
|---|---|
| Text direkt (md, txt, json, yaml, py, csv, html, gdoc) | 418 |
| PDF-Textlayer (pdftotext, max. 30 Seiten) | 23 |
| OCR PDF (Scan, pdftoppm 150 dpi, Seiten 1–3, Tesseract deu+eng) | 44 |
| OCR Bild (jpg/png, Tesseract deu+eng) | 108 |
| Fehler (Netzdrosselung nach 2 Leseversuchen) | 78 |

Vektorindex: 4 534 Chunks (220 Wörter, Überlappung 40), Vokabular 36 914 Terme (df ≥ 2, < 50 % der Chunks), TF-IDF mit log-TF, L2-normiert, Top-60 Terme je Chunk, Kosinus-Ähnlichkeit im Browser. Datei: NEXUS_VECTOR_INDEX_v1.0.json.

Grenzen: lexikalischer Index (keine semantischen Embeddings); OCR-Qualität bei Fotos/Plänen begrenzt; PDFs > 5 MB (30 Stk.) nicht verarbeitet. Nächster Schritt: Embeddings (z. B. lokal via Ollama nomic-embed-text) in Chroma/Qdrant über nexus_orch.
