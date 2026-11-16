---
name: knowledge-ingestion
description: "Überführt eine zulässige Quelle (PDF, DOCX, Markdown) deterministisch in ein versioniertes NEXUS Knowledge Package mit document.md, blocks.jsonl, chunks.jsonl, manifest.json und provenance.json. Identische Eingabe und Konfiguration liefern identische Hashes. Voraussetzung ist ein Entscheid von source-governance."
version: '0.1.0'
status: PLANNED
timestamp: "2026-10-13"
priority: 2
depends_on:
- source-governance
replaces:
- pdf-ground-truth-freeze
---

# knowledge-ingestion

## Zweck
Einheitlicher Eingang für alle Wissensquellen. Aus einer Quelldatei entsteht ein unveränderliches, hash-gesichertes Paket, in dem jeder Chunk auf seine Quellblöcke und deren Seiten- oder Zeilenanker zurückführbar ist. `text_raw` bleibt unverändert; keine fachliche Interpretation, kein LLM im MVP.

## Voraussetzungen (werden geprüft, sonst Abbruch)
1. `governance-decision.json` liegt vor und ist schemagültig.
2. `decision.source.sha256` entspricht dem SHA-256 der Eingabedatei.
3. `local_processing` ist in `allowed_targets` (immer der Fall, wird dennoch geprüft).

## Inputs
| Input | Pflicht | Beschreibung |
|---|---|---|
| Quelldatei | ja | PDF, DOCX oder Markdown |
| Governance-Entscheid | ja | siehe `source-governance` |
| Profil | nein | Ingestion-Profil (YAML), Standard `default` |

Profil (Beispiel, wirkt über `config_sha256` auf alle Hashes):
```yaml
profile: default
max_tokens_per_chunk: 400         # Näherung: Wörter (deterministisch, keine Tokenizer-Abhängigkeit)
overlap_blocks: 0
heading_regex: '^(\d+(\.\d+){0,5})\s+\S'
ocr: {enabled: true, engine: tesseract, languages: [deu, eng], min_chars_per_page_median: 50}
crosscheck: {enabled: true, engine: pdfminer, min_similarity: 0.98}   # nur PDF, nur Flag
```

## Workflow
1. **Hashing**: SHA-256 der Quelldatei und der wirksamen Konfiguration (`config_sha256`, kanonisches JSON).
2. **Extraktion lokal**
   - PDF: PyMuPDF; Test 1 = Median der Zeichen pro Seite größer als `min_chars_per_page_median`. Sonst Scan: OCR lokal (OCRmyPDF/Tesseract `deu+eng`), Blöcke mit `source=tesseract` und `ocr_confidence`.
   - PDF mit komplexem Layout: zusätzlich pdfplumber/Docling als Hilfe für Tabellen (Ergebnis wird als Blöcke übernommen, Reihenfolge deterministisch).
   - DOCX: Absätze und Tabellen in Dokumentreihenfolge, Anker `para`.
   - Markdown: Zeilenblöcke, Anker `line`.
3. **Normalisierung**: Nur `text_norm` (Unicode NFC, Whitespace zusammenfassen, Silbentrennung am Zeilenende auflösen). `text_raw` bleibt unverändert.
4. **Strukturauflösung** (deterministisch, regelbasiert): Überschriften über `heading_regex` plus Layout-Merkmal (Schriftgröße/Fett bei PDF, Überschriftenstil bei DOCX, `#` bei Markdown). Ergebnis: `chapter_id` (`<doc_id>#<Nummer>` oder `<doc_id>#h<laufende Nr>`) und `heading_path`.
5. **Chunking**: Je Kapitel Blöcke der Reihe nach sammeln, bis `max_tokens_per_chunk` erreicht ist. Ein Block wird nie geteilt (Formelzeilen bleiben intakt). Ein einzelner zu großer Block wird ein eigener Chunk mit Flag `oversize`.
6. **Provenienz**: Jeder Chunk trägt `source_hashes` (alle enthaltenen Blöcke) und `anchors` (erster und letzter Anker).
7. **Export atomar**: Schreiben in ein temporäres Verzeichnis, Hashes berechnen, dann `rename` nach `data/packages/pkg-<root_hash[:16]>/`; Dateien danach schreibgeschützt. Bei Abbruch bleibt kein Teilpaket zurück.

## Outputs
```
data/packages/pkg-<root_hash[:16]>/
  document.md        # lesbare Fassung mit Kapitelstruktur (Quelle für Menschen)
  blocks.jsonl       # TextBlock je Zeile (Reihenfolge = Lesereihenfolge)
  chunks.jsonl       # RagChunk je Zeile
  manifest.json      # Zähler, Hashes, Tool-Versionen, Klassifikation, root_hash
  provenance.json    # Schritte mit Ein-/Ausgabe-Hashes, Lauf-Zeitstempel (nicht Teil der Hashes)
```
Alle Schemas: `docs/CONTRACTS.md` (`TextBlock`, `RagChunk`, `Manifest`). Das Verzeichnis liegt unter `data/` und ist per `.gitignore` gesperrt; ein Git-Export ist nur nach `source-governance` und `knowledge-quality-gate` zulässig.

## Determinismus-Regeln
- Kanonisches JSON: sortierte Schlüssel, kompakte Trenner, UTF-8; ein Datensatz je Zeile.
- Float-Werte (bbox) auf 3 Nachkommastellen gerundet; Rundung ist dokumentiert.
- Feste Reihenfolge: Seite, dann y, dann x; Tie-Break über Extraktionsindex.
- Keine Zeitstempel, Zufallswerte oder absoluten Pfade in Hash-relevanten Daten.
- Tool-Versionen gepinnt (`requirements.lock`) und im Manifest vermerkt.
- `--self-check` führt die Ingestion ein zweites Mal aus und vergleicht `root_hash` und Dateihashes.

## CLI
```
nexus ingest <datei> --decision governance-decision.json [--profile default|FILE]
                     [--out data/packages] [--self-check]
nexus run <datei> [--origin ...] [--owner ...] [--license-hint ...]   # classify, ingest, validate
```

## Exit-Codes
| Code | Bedeutung |
|---|---|
| 0 | Paket erzeugt |
| 11 | Entscheid fehlt, ist ungültig oder passt nicht zur Datei |
| 12 | Format nicht unterstützt |
| 13 | Extraktion fehlgeschlagen |
| 14 | Selbstprüfung: Hashes beider Läufe weichen ab |

## Hard Gates
- Identische Eingabe plus identische Konfiguration ergibt identische kanonische Hashes und dieselbe Blockreihenfolge.
- Jeder Chunk enthält mindestens einen `source_hash` und einen Anker.
- Ohne gültigen Governance-Entscheid keine Verarbeitung.
- Keine Netzwerkzugriffe während der Extraktion (OCR nur lokal).

## Tests
| # | Fall | Erwartung |
|---|---|---|
| I1 | Zwei Läufe, gleiche Fixture | identischer `root_hash`, `diff -r` leer |
| I2 | Mehrspalten-Fixture | stabile Lesereihenfolge |
| I3 | Zeile `M_Ed ≤ M_Rd` | `text_raw` Zeichen für Zeichen erhalten |
| I4 | Reines Bild-PDF | als Scan erkannt, OCR-Pfad, `source=tesseract` |
| I5 | Chunk über mehrere Blöcke | `source_hashes` enthält alle Blockhashes |
| I6 | Entscheid mit anderer `sha256` | Exit 11 |
| I7 | Abbruch während des Schreibens (simuliert) | kein Teilpaket in `data/packages/` |
| I8 | Markdown und DOCX | Anker `line` bzw. `para` vorhanden |
| I9 | Konfiguration ändern (`max_tokens_per_chunk`) | anderer `config_sha256` und `root_hash` |

Fixtures: nur selbst erzeugte, öffentliche Beispiele unter `tests/fixtures/public/` (kein lizenzierter Inhalt), erzeugt per Skript.

## Abnahme
Zwei Läufe mit identischer Eingabe erzeugen identische kanonische Hashes und dieselbe Blockreihenfolge; Paket besteht den Check Q01 bis Q03 des `knowledge-quality-gate`.

## Nicht im MVP
LLM-gestützte Kapitelzuordnung, Formel-LaTeX-Erkennung, Audio-Transkripte und Human-OCR (separater Public-Connector nach Gate).

## Log
- 2026-10-13: Vollständige Spezifikation erstellt (Status PLANNED).
