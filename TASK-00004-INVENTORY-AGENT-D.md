# TASK-00004: INVENTAR — Agent D / Curator

**Status:** IN_PROGRESS  
**Owner:** ID-02 Gemini + deterministischer Python-Indexer  
**ETA:** 2–3 Tage  
**Start:** 2026-10-08  

---

## Aufgabe

Alle Quellen inventarisieren: Repos, Obsidian-Vault, Google Drive.  
Output: `registry/file-registry.jsonl` + `catalog-draft.yaml` + Duplikat-Report.

## Input

- `julianzotter/julianzotter/tools/01_scan_registry.py` (atomares Scan-Skript)
- Quellen:
  - `julianzotter/NEXUS-AI-AEC-ENGINEERIN-KNOWLEDGE-GRAPH` (TypeScript UI + Solver)
  - `julianzotter/julianzotter` (Docs, Tools, Routines, Quellenlog)
  - Obsidian-Vault (lokal oder Drive: `_SEILSTATIK_BOEBLINGEN`, `_code`, etc.)
  - Google Drive (bei Zugang verfügbar)

## Output (Expected)

```
registry/
├─ file-registry.jsonl         ← 1 Zeile = 1 Datei, SHA-256, Metadaten
├─ duplicates-report.md         ← Hash-basierte Duplikat-Kandidaten
├─ catalog-draft.yaml           ← Erste YAML-Fassung, Status=DRAFT
└─ inventory-summary.txt        ← Statistik: X Dateien, Y Duplikate, Z Größe
```

## Abnahmekriterium

- [ ] `file-registry.jsonl` erfasst ≥90% aller Dateien aus Quellen
- [ ] Jeder Datensatz:
  - `id`: SHA-256(root + relpath)[:16] (stabil, eindeutig)
  - `root`: Quellname (z.B. "NEXUS-AI-AEC", "julianzotter", "Obsidian_SEILSTATIK")
  - `path`: Relativpfad
  - `name`: Dateiname
  - `ext`: Dateiendung (lowercased)
  - `size`: Bytes
  - `mtime`: ISO 8601
  - `sha256`: Hex-Hash (Dateien < 500 MB)
  - `status`: "FOUND" | "SKIPPED" | "ERROR"
- [ ] SHA-256 Hashes für Dateien < 500 MB korrekt
- [ ] Duplikate identifiziert: gleicher SHA-256 = gleiche Datei
- [ ] Duplikate gekennzeichnet (nicht gelöscht): `supersedes` Feld
- [ ] Ausschlüsse: `__pycache__`, `.git`, `node_modules`, `$RECYCLE.BIN`, System-Ordner
- [ ] Credentials-Dateien ausgeschlossen: `token.json`, `credentials.json`, `.env*`
- [ ] Atomar geschrieben: `.jsonl.tmp` → `file-registry.jsonl`
- [ ] `catalog-draft.yaml`: Struktur folgt `registry/README.md`, Objekt-IDs nach Schema
- [ ] Duplikat-Report: Kandidaten mit Hash, Größe, Quelle(n), Empfehlung
- [ ] Signiert: Kürzel (ID-02), Datum (ISO), Evidence-Ref (PR)

## Tools & Scripts

```bash
# Beispiel-Aufruf:
python tools/01_scan_registry.py \
  --root "/path/to/NEXUS-AI-AEC-ENGINEERIN-KNOWLEDGE-GRAPH" \
  --root "/path/to/julianzotter" \
  --root "/path/to/Obsidian-Vault" \
  --out registry/file-registry.jsonl \
  --hash \
  --exclude __pycache__ .git node_modules

# Duplikat-Erkennung (separate, deterministischer Python):
python tools/detect_duplicates.py \
  --input registry/file-registry.jsonl \
  --output registry/duplicates-report.md \
  --min-size 1000  # nur Dateien > 1 KB
```

## Workflow

1. **Scan ausführen**
   - `01_scan_registry.py` auf alle 3–4 Quellen laufen lassen
   - Atomar in `file-registry.jsonl` schreiben
   - Fehler protokollieren, nicht abbrechen

2. **Duplikate erkennen**
   - Python-Skript: Lese `file-registry.jsonl`, Gruppiere nach SHA-256
   - Schreibe `duplicates-report.md` mit Kandidaten

3. **YAML-Katalog erzeugen**
   - Lese `file-registry.jsonl`
   - Erzeuge `catalog-draft.yaml` mit Struktur:
     ```yaml
     version: "0.1.0-draft"
     generated_at: "2026-10-08T..."
     agent: "ID-02-Gemini"
     objects:
       - id: SNP-0001  # oder KNW-, RUL-, DAT-Präfix
         title: "Quelle / Dateiname"
         type: "snippet | knowledge | rule | dataset | prompt"
         source_file: "path/to/file"
         source_hash: "sha256..."
         status: "DRAFT"
         owner: "ID-02"
         version: "0.1.0"
         description: "(auto-generated oder leer)"
     ```

4. **PR einreichen**
   - Branch: `feature/TASK-00004-inventory`
   - 3 neue Dateien + `.gitignore` Update (falls nötig)
   - PR-Template ausfüllen (Agent D, Task, Evidence, Signatur)
   - Reviewer: ID-01 (Human Gate)

## Dependencies

- Keine vorgelagerten Tasks
- Blockiert: TASK-00001 (A braucht Registry für Kontext)

## Hinweise

- `01_scan_registry.py` existiert bereits in `julianzotter/julianzotter/tools/`
- Keine Dateien editieren, nur Metadaten erfassen
- Atomar schreiben schützt vor korrupten Dateien bei Abbruch
- Duplikat-Kandidaten können False-Positives sein (z.B. zwei identische README.md)
  → Report muss „RECOMMENDATION" haben (z.B. „Merge diese zwei?")

## Erfolgsmetriken (für Review)

| Metrik | Schwelle |
|---|---|
| Erfassungs-Quote | ≥90% |
| Duplikat-Kandidaten | ≥5 (realistisch für diesen Bestand) |
| Größe registry.jsonl | < 10 MB (komprimierbar) |
| Runtime | < 5 Minuten (auf normalem Rechner) |

---

## Signatur (nach Abschluss)

```
✓ Agent: D (Curator / Gemini + Python)
✓ Kürzel: ID-02
✓ Datum: [Abschluss-Datum]
✓ Evidence: [PR-Link]
✓ Registry live: ja/nein
```

---

**NEXT TASK:** Nach Merge von TASK-00004 → TASK-00001 (Agent A / Reference) starten
