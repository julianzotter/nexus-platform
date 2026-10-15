---
schema: IOD.01/1.0
run_id: 2026-10-13__NEXUS-MULTI-LLM-ORCHESTRATOR__R001
type: artifact
artifact: 03_ARTIFACTS/evaluation/EVAL_PROMPT_SENT_6e8f574.md
archived_ts: 2026-10-15T06:00:48+02:00
sha256_original: 139ca4cf2bc5376713085a940d6e80b28d8aff3516f49b9e8dd67c16727dce8b
---

# NEXUS-AI – Evaluierungsbogen v1.0
Prüfgegenstand: GitHub `julianzotter/nexus-platform` (Branch `main`, Stand 2026-10-13), Schwerpunkt `orchestrator/` (NEXUS-AI Multi-LLM Orchestrator v1.2.0)
Auftraggeber: ZOTTERCONSULT, DI Julian Zotter · Rückgabe: ausgefüllter Prüfbericht (Abschnitt 5) als Markdown inkl. JSON-Block

---

## 0 Anweisung an das prüfende Modell (bitte vollständig befolgen)
Du bist unabhängige:r Gutachter:in für Software-Architektur, LLM-Orchestrierung und Informationssicherheit mit Bezug zu Ingenieurbüros (Tragwerksplanung, Eurocode/ÖNORM). Prüfe das NEXUS-AI-System ausschließlich anhand des Kontextpakets in Abschnitt 6 (und, falls du Zugriff hast, des Repos selbst).

Regeln:
1. **Belegpflicht:** Jede Feststellung mit Fundstelle `Datei:Zeile` oder `Datei → Abschnitt`. Ohne Beleg = als **Annahme** kennzeichnen.
2. **Nicht prüfbar** ausweisen, statt zu raten (z. B. Laufzeitverhalten, das du nicht ausführen kannst).
3. **Keine Schönfärberei:** Note nach den Ankerbeschreibungen in Abschnitt 3, nicht nach Gesamteindruck.
4. **Lösungen statt Problemlisten:** Jeder Mangel bekommt eine konkrete, umsetzbare Maßnahme (Datei, Änderung, Aufwand S/M/L).
5. **Deterministisch und knapp:** Deutsch, keine Einleitung, keine Wiederholung des Bogens.
6. Halte das Ausgabeformat aus Abschnitt 5 **exakt** ein (der JSON-Block wird maschinell ausgewertet).

## 1 Systemkurzbeschreibung (Soll laut Doku)
- Ein Einstiegspunkt (`nexus` / `python -m nexus_orch.cli`) routet Aufgaben deterministisch an Perplexity (Sonar), Claude, GPT, Gemini, Google Vision (OCR) oder lokal (Ollama).
- Routen: research, norm_check, code, review, draft, long_context, private, engineering_decision, ocr; Fallback-Ketten.
- Privacy Hard Gate: Marker `VERTRAULICH`/`CONFIDENTIAL`/`[P3]` → nur lokal, kein Cloud-Fallback.
- Model Council mit Konsensprüfung und Synthese; Shared-Lessons-Layer (`lessons.jsonl`); Audit-Log nur mit Prompt-Hash; Workflow-Registry (17 Workflows).
- SSOT: Google Drive `/LLM-LOCAL-SSOT`; GitHub = Versionierung; Sync über `sync_nexus.ps1`.

## 2 Die 4 Entscheidungskriterien
| Nr. | Kriterium | Gewicht | Kernfrage |
|---|---|---|---|
| K1 | Funktionale Korrektheit und Zuverlässigkeit | 30 % | Tut das System nachweisbar, was die Doku verspricht – auch im Fehlerfall? |
| K2 | Sicherheit, Datenschutz und Governance | 25 % | Sind vertrauliche Projektdaten, Keys und Freigaben belastbar geschützt und nachvollziehbar? |
| K3 | Architektur, Erweiterbarkeit und Wartbarkeit | 25 % | Lässt sich das System mit vertretbarem Aufwand erweitern, testen und von Dritten warten? |
| K4 | Betriebsfähigkeit und Praxisnutzen im Ingenieurbüro | 20 % | Ist es installierbar, reproduzierbar, kostenbewusst und bringt es im Statik-/AEC-Alltag messbaren Nutzen? |

### Prüfpunkte je Kriterium (jeweils bewerten: erfüllt / teilweise / nicht erfüllt / nicht prüfbar)
**K1 Funktion**
- K1.1 Routing: jede Route in `routing.json` ist in `core.py` auflösbar; unbekannte Route → definierter Fehler.
- K1.2 Fallback: Ausfall des Primärproviders führt zum nächsten; Fehler werden gesammelt und ausgegeben.
- K1.3 Model Council: Konsensprüfung und Synthese logisch korrekt; Verhalten bei nur einem verfügbaren Mitglied.
- K1.4 Perplexity-Integration: Zitate werden durchgereicht; Modellname konfigurierbar.
- K1.5 Tests: Abdeckung der Kernpfade (Routing, Fallback, Privacy Gate, Council, Lessons); Tests ohne Netz lauffähig.
- K1.6 Determinismus: Temperatur/Parameter je Provider tatsächlich gesetzt.

**K2 Sicherheit/Governance**
- K2.1 Privacy Hard Gate: Marker-Erkennung robust (Groß-/Kleinschreibung, Varianten); garantiert kein Cloud-Fallback.
- K2.2 Secrets: Keys nur aus Umgebung; kein Logging von Keys oder Klartext-Prompts; `.gitignore`/Sync-Ausschlüsse.
- K2.3 Audit: Nachvollziehbarkeit (wer/was/wann/welcher Provider) bei Datensparsamkeit (Hash statt Klartext).
- K2.4 Freigabeprozess: Lessons mit Status PROPOSED → Review; keine automatischen destruktiven Aktionen (Sync ohne Löschen).
- K2.5 DSGVO/Berufsgeheimnis: Welche Daten verlassen den Rechner, an welche Anbieter; Risiko-Restbewertung.

**K3 Architektur/Wartbarkeit**
- K3.1 Trennung Konfiguration (JSON) / Logik (core) / Provider-Adapter (providers) / CLI.
- K3.2 Neuer Provider oder neue Route: Anzahl betroffener Dateien, Aufwand.
- K3.3 Abhängigkeiten (nur Standardbibliothek): Vor-/Nachteile, Fehlerbehandlung HTTP, Timeouts, Retries.
- K3.4 Code-Qualität: Lesbarkeit, Typisierung, Fehlerklassen, Dokumentation im Code.
- K3.5 Versionierung und SSOT-Konsistenz (Repo ↔ Drive ↔ Registry).

**K4 Betrieb/Nutzen**
- K4.1 Installation Windows/PowerShell (`setup.ps1`, `pip install -e .`), Fehlermeldungen mit Handlungshinweis.
- K4.2 Reproduzierbarkeit (Versionen, Modellnamen, Konfiguration, Logs).
- K4.3 Kosten- und Latenzbewusstsein (lokal vs. Cloud, Council-Kosten).
- K4.4 Fachlicher Nutzen: Eignung für Normenrecherche (EN 1995, ÖNORM B 1995), Variantenentscheid (z. B. BSP vs. HBV), OCR von Plänen/Positionsplänen.
- K4.5 Integration in bestehende Werkzeuge (Drive-SSOT, Workflow-Registry, Perplexity-Projekt).

## 3 Notenskala (österreichisches Schulnotensystem, 1 = beste)
| Note | Bezeichnung | Anker |
|---|---|---|
| 1 | Sehr gut | Alle Prüfpunkte erfüllt, belegt und getestet; keine relevanten Mängel. |
| 2 | Gut | Überwiegend erfüllt; kleine Mängel ohne Einfluss auf Sicherheit oder Ergebnisrichtigkeit. |
| 3 | Befriedigend | Kernfunktion vorhanden; mehrere Lücken (Tests, Fehlerfälle, Doku), Nacharbeit nötig. |
| 4 | Genügend | Nur eingeschränkt einsetzbar; wesentliche Lücken, Einsatz nur unter Aufsicht. |
| 5 | Nicht genügend | Kernanforderung nicht erfüllt oder sicherheitskritischer Mangel. |

**Gesamtnote** = gewichtetes Mittel, auf eine Nachkommastelle. **K.-o.-Regel:** Erhält ein Kriterium die Note 5, ist die Gesamtnote nicht besser als 4,0 (d. h. Gesamt = max(gewichtetes Mittel; 4,0)).

## 4 Ablauf (empfohlen)
1. Kontextpaket lesen (Abschnitt 6), Soll (Abschnitt 1) gegen Ist prüfen.
2. Prüfpunkte K1.1–K4.5 einzeln bewerten, Belege notieren.
3. Je Kriterium Note nach Abschnitt 3 vergeben, Begründung in 2–4 Sätzen.
4. Top-5-Maßnahmen nach Wirkung/Aufwand priorisieren.
5. Prüfbericht exakt im Format von Abschnitt 5 ausgeben.

## 5 Ausgabeformat Prüfbericht (exakt so ausgeben)
````markdown
# Prüfbericht NEXUS-AI v1.2.0
Prüfendes Modell: <Name, Version>  ·  Datum: <JJJJ-MM-TT>  ·  Repo-Zugriff: <ja/nein, nur Kontextpaket>

## A Ergebnis
| Kriterium | Note | Begründung (2–4 Sätze) |
|---|---|---|
| K1 Funktion | | |
| K2 Sicherheit/Governance | | |
| K3 Architektur/Wartbarkeit | | |
| K4 Betrieb/Nutzen | | |
| **Gesamt (gewichtet)** | | K.-o.-Regel angewendet: ja/nein |

## B Prüfpunkte
| ID | Status (erfüllt/teilweise/nicht erfüllt/nicht prüfbar) | Beleg (Datei:Zeile) | Feststellung |
|---|---|---|---|
| K1.1 | | | |
... (alle 21 Prüfpunkte K1.1–K4.5)

## C Kritische Befunde (max. 5, nur sicherheits- oder ergebnisrelevant)
1. <Befund> – Beleg – Risiko – Maßnahme

## D Top-5-Maßnahmen
| Rang | Maßnahme | Datei(en) | Kriterium | Wirkung (hoch/mittel/gering) | Aufwand (S/M/L) |
|---|---|---|---|---|---|

## E Stärken (max. 3)

## F Annahmen und nicht Prüfbares

## G JSON (maschinenlesbar, keine Kommentare)
```json
{"modell":"","datum":"","repo_zugriff":false,
 "noten":{"K1":0,"K2":0,"K3":0,"K4":0},"gesamt":0.0,"ko_regel":false,
 "pruefpunkte":{"K1.1":"","K1.2":"","K1.3":"","K1.4":"","K1.5":"","K1.6":"",
   "K2.1":"","K2.2":"","K2.3":"","K2.4":"","K2.5":"",
   "K3.1":"","K3.2":"","K3.3":"","K3.4":"","K3.5":"",
   "K4.1":"","K4.2":"","K4.3":"","K4.4":"","K4.5":""},
 "kritisch":[{"befund":"","datei":"","massnahme":""}],
 "massnahmen":[{"rang":1,"massnahme":"","datei":"","kriterium":"K1","wirkung":"hoch","aufwand":"S"}]}
```
````
Status-Werte im JSON: `erfuellt`, `teilweise`, `nicht_erfuellt`, `nicht_pruefbar`.

---

## 6 Kontextpaket (automatisch erzeugt, Commit 6e8f574, 2026-10-13)

### Dateibaum
```
     4728  .gitignore
     1069  LICENSE
      924  NEXUS-TEAM-WORK-01.ipynb
      280  README.md
     6430  TASK-00004-INVENTORY-AGENT-D.md
     5407  docs/concepts/2026-10-13/INTEGRATION.md
     1828  docs/concepts/2026-10-13/README.md
     5784  docs/concepts/2026-10-13/REVIEW.md
     4740  docs/concepts/2026-10-13/catalog.json
     9309  docs/concepts/2026-10-13/sources/pdf-normen-parser-skill.extracted.txt
     4102  evaluation/NEXUS_EVAL_BOGEN_KURZ_v1.0.md
    46670  evaluation/NEXUS_EVAL_BOGEN_v1.0.md
     4049  evaluation/nexus_eval_auswertung.py
        0  orchestrator/COMMUNICATION/lessons/.gitkeep
     5139  orchestrator/README.md
     2335  orchestrator/config/routing.json
      795  orchestrator/config/sync_targets.json
     1716  orchestrator/install_autosync.ps1
      105  orchestrator/nexus_orch/__init__.py
     2986  orchestrator/nexus_orch/cli.py
     4690  orchestrator/nexus_orch/core.py
     4536  orchestrator/nexus_orch/evaluate.py
     4659  orchestrator/nexus_orch/providers.py
      353  orchestrator/pyproject.toml
     2984  orchestrator/registry/workflow-registry.json
      635  orchestrator/setup.ps1
     2401  orchestrator/sync_nexus.ps1
     3268  orchestrator/sync_nexus_rclone.ps1
     4982  orchestrator/tests/test_orch.py
     1550  prototypes/vibe-coder-v2.3/README.md
    36304  prototypes/vibe-coder-v2.3/index.html
      644  registry/catalog-draft.yaml
     1493  registry/coverage-per-source.json
      502  registry/duplicates-report.md
        0  registry/file-registry.jsonl
     1183  registry/inventory-summary.txt
   162152  reports/2026-10-13_parsing-pipeline/NEXUS_PARSE_DASHBOARD_v1.0.html
   165592  reports/2026-10-13_parsing-pipeline/NEXUS_PARSE_DASHBOARD_v1.1.html
   153961  reports/2026-10-13_parsing-pipeline/NEXUS_PARSE_INVENTORY_v1.0.json
     2167  reports/2026-10-13_parsing-pipeline/NEXUS_PARSE_REPORT_v1.0.md
     3167  reports/2026-10-13_parsing-pipeline/NEXUS_PARSE_REPORT_v1.1.md
  8089502  reports/2026-10-13_parsing-pipeline/NEXUS_VECTOR_INDEX_v1.0.json
     2444  reports/2026-10-13_parsing-pipeline/ocr.py
     1743  reports/2026-10-13_parsing-pipeline/parse.py
     4005  tests/test_inventory_completeness.py
     6711  tools/coverage_stats.py
     3553  tools/detect_duplicates.py
     8176  tools/validate_registry.py
```

### FILE: README.md
~~~~markdown
   1 # nexus-platform
   2 NEXUS Platform Hub: Unified registry, coordinated execution, evidence-based learning. Single source of truth for engineering knowledge, deterministic solvers, validated workflows, and multiagent orchestration with dual-mode operations (production + improvement).
~~~~

### FILE: orchestrator/README.md
~~~~markdown
   1 # NEXUS-AI Multi-LLM Orchestrator v1.2.0
   2 
   3 Integrationsschicht des NEXUS AI-OS: ein Einstiegspunkt, der Aufgaben deterministisch (T=0.0) an Perplexity, Claude, GPT, Gemini oder ein lokales Modell (Ollama) routet.
   4 
   5 ## Funktionen
   6 | Funktion | Umsetzung |
   7 |---|---|
   8 | Routing nach Aufgabentyp | `config/routing.json` → `routes` (research, norm_check, code, review, draft, long_context, private, engineering_decision) |
   9 | Fallback-Kette | primary → fallback[], Fehler protokolliert |
  10 | Privacy Hard Gate | Marker `VERTRAULICH`/`CONFIDENTIAL`/`[P3]` → nur `local`, kein Cloud-Fallback |
  11 | Model Council | `council`: alle Mitglieder, Konsensprüfung, sonst Synthese (Konsens / Abweichungen / Empfehlung) |
  12 | Perplexity-Integration | Sonar API (`sonar-pro`), Zitate werden mit ausgegeben |
  13 | Shared Lessons Layer | `COMMUNICATION/lessons/lessons.jsonl` (agent, context, condition, pattern, evidence; Status PROPOSED) |
  14 | OCR (Google Cloud Vision) | Route `ocr`: Vision `DOCUMENT_TEXT_DETECTION` (Bild-URL, gs:// oder lokaler Pfad), Fallback Gemini; vertraulich → lokal |
  15 | Audit | `COMMUNICATION/audit/YY_MM_DD_audit.jsonl` (nur Prompt-Hash, kein Klartext) |
  16 | Workflow-Registry | `registry/workflow-registry.json` – 17 Workflows (nexus-mvp, nexus-skill-family, nexus-platform, Control Tower, Mail-Triage) mit Route |
  17 
  18 ## Installation als Befehl `nexus`
  19 ```powershell
  20 cd "$env:USERPROFILE\nexus-platform\orchestrator"; python -m pip install -e .
  21 nexus status   # funktioniert danach in jedem Ordner
  22 ```
  23 
  24 ## Start
  25 ```powershell
  26 .\setup.ps1                                   # Keys als User-Env, Tests, Status
  27 python -m nexus_orch.cli run research "EN 1995-1-1 kmod NKL2 Quellen"
  28 python -m nexus_orch.cli council engineering_decision "BSP vs. HBV Decke 7,5 m Spannweite"
  29 python -m nexus_orch.cli lesson --agent claude --context EC5 --condition "wenn NKL fehlt" --pattern "NKL vor kmod abfragen" --evidence "Session 2026-10-13"
  30 python -m nexus_orch.cli run ocr "C:/Scans/Positionsplan_EG.jpg"
  31 python -m nexus_orch.cli lessons kmod
  32 python -m nexus_orch.cli registry
  33 ```
  34 Nur Python-Standardbibliothek; `pytest` für Tests. Modellnamen in `routing.json` anpassen.
  35 
  36 ## Drive-Sync (Windows)
  37 ```powershell
  38 .\sync_nexus.ps1              # main pullen, Tests, dann: orchestrator -> LLM-LOCAL-SSOT + BENCHMARK, komplettes Repo -> LLM-LOCAL-SSOT\nexus-platform
  39 .\sync_nexus.ps1 -NoFullRepo  # nur orchestrator
  40 # ausgeschlossen: .git, Caches, venv, node_modules, .env/*.key/*.pem; kein Loeschen in Drive
  41 ```
  42 
  43 ## Drive-Sync per rclone (ohne Laufwerk G:)
  44 Für Rechner ohne Google Drive for desktop, Server/VM oder Aufgabenplanung. Ziele per Drive-Ordner-ID in `config/sync_targets.json` (orchestrator, reports, evaluation → SSOT + BENCHMARK). Nur `rclone copy`, kein Löschen.
  45 ```powershell
  46 # einmalig: rclone installieren (ohne winget)
  47 $d="$env:LOCALAPPDATA\rclone"; New-Item -ItemType Directory -Force $d | Out-Null
  48 Invoke-WebRequest https://downloads.rclone.org/rclone-current-windows-amd64.zip -OutFile "$env:TEMP\rclone.zip"
  49 Expand-Archive "$env:TEMP\rclone.zip" "$env:TEMP\rclone" -Force
  50 Copy-Item "$env:TEMP\rclone\rclone-*-windows-amd64\rclone.exe" $d -Force
  51 [Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path","User")+";$d", "User")
  52 rclone config                      # n → gdrive → drive → scope 1 → Browser-Login
  53 python -m pip install pytest
  54 
  55 .\sync_nexus_rclone.ps1 -DryRun    # anzeigen
  56 .\sync_nexus_rclone.ps1            # ausführen
  57 .\sync_nexus_rclone.ps1 -Only reports
  58 ```
  59 Wann welcher Weg: `sync_nexus.ps1` = Arbeits-PC mit Laufwerk G: · `sync_nexus_rclone.ps1` = PC ohne G:, Server, geplante Läufe, Ziel unabhängig von Ordnernamen.
  60 
  61 ## SSOT
  62 Google Drive `/LLM-LOCAL-SSOT` = Wahrheit · GitHub `julianzotter/nexus-platform` = Versionierung · OneDrive/Dropbox = Spiegel · Perplexity-Projekt „NEXUS-AI Multi-LLM System“ = Orchestrator-Kontext.
  63 
  64 ## Automatisierung
  65 | Ziel | Befehl | Wirkung |
  66 |---|---|---|
  67 | Drive-Sync ohne Handarbeit | `.\install_autosync.ps1` (einmalig) | Windows-Aufgabe `NEXUS-AutoSync`: täglich 07:00 + bei Anmeldung `sync_nexus.ps1`; Log `%LOCALAPPDATA%\NEXUS\autosync.log`; `-Rclone` für Rechner ohne G:, `-Remove` zum Entfernen |
  68 | Evaluierung an alle Modelle | `nexus eval` | Bogen `evaluation/NEXUS_EVAL_BOGEN_v1.0.md` + frisch erzeugtes Kontextpaket (aktueller Commit) an alle Cloud-Modelle mit Key; Berichte `evaluation/berichte/EVAL_<modell>_<JJMMTT>.md`, Auswertung `NEXUS_EVAL_AUSWERTUNG.md` |
  69 | Vorschau | `nexus eval --dry-run` | Prompt-Größe und verfügbare Modelle, ohne Versand |
  70 | Auswahl | `nexus eval --models perplexity,claude` | nur diese Modelle |
  71 | Nur Auswertung | `nexus eval-summary` | wertet manuell abgelegte Berichte (z. B. aus ChatGPT-Web) in `evaluation/berichte` aus |
  72 
  73 `nexus eval` sendet nur Repo-Inhalt (Code/Doku). Das Privacy-Gate gilt dafür bewusst nicht; Projektdaten gehören nicht ins Repo. Das lokale Modell ist ausgenommen (Paket > 16k Kontext).
  74 Drive-Sync kopiert zusätzlich `reports/` und `evaluation/` nach `LLM-LOCAL-SSOT\nexus-reports|nexus-evaluation` und `BENCHMARK…\nexus-reports|nexus-evaluation`.
~~~~

### FILE: orchestrator/pyproject.toml
~~~~toml
   1 [build-system]
   2 requires = ["setuptools>=61"]
   3 build-backend = "setuptools.build_meta"
   4 
   5 [project]
   6 name = "nexus-orch"
   7 version = "1.2.0"
   8 description = "NEXUS-AI Multi-LLM Orchestrator (Perplexity, Claude, GPT, Gemini, Vision, Ollama)"
   9 requires-python = ">=3.10"
  10 
  11 [project.scripts]
  12 nexus = "nexus_orch.cli:main"
  13 
  14 [tool.setuptools]
  15 packages = ["nexus_orch"]
~~~~

### FILE: orchestrator/config/routing.json
~~~~json
   1 {
   2   "version": "1.2.0",
   3   "default_temperature": 0.0,
   4   "providers": {
   5     "perplexity": {
   6       "kind": "openai_compat",
   7       "base_url": "https://api.perplexity.ai",
   8       "model": "sonar-pro",
   9       "env_key": "PERPLEXITY_API_KEY"
  10     },
  11     "claude": {
  12       "kind": "anthropic",
  13       "base_url": "https://api.anthropic.com",
  14       "model": "claude-sonnet-4-5",
  15       "env_key": "ANTHROPIC_API_KEY"
  16     },
  17     "gpt": {
  18       "kind": "openai_compat",
  19       "base_url": "https://api.openai.com/v1",
  20       "model": "gpt-5",
  21       "env_key": "OPENAI_API_KEY"
  22     },
  23     "gemini": {
  24       "kind": "gemini",
  25       "base_url": "https://generativelanguage.googleapis.com/v1beta",
  26       "model": "gemini-2.5-pro",
  27       "env_key": "GEMINI_API_KEY"
  28     },
  29     "local": {
  30       "kind": "ollama",
  31       "base_url": "http://localhost:11434",
  32       "model": "qwen2.5:7b",
  33       "env_key": null,
  34       "num_ctx": 16384
  35     },
  36     "vision": {
  37       "kind": "gcv_ocr",
  38       "base_url": "https://vision.googleapis.com/v1",
  39       "model": "DOCUMENT_TEXT_DETECTION",
  40       "env_key": "GOOGLE_VISION_API_KEY"
  41     }
  42   },
  43   "routes": {
  44     "research": {
  45       "primary": "perplexity",
  46       "fallback": [
  47         "gemini",
  48         "gpt"
  49       ]
  50     },
  51     "norm_check": {
  52       "primary": "perplexity",
  53       "fallback": [
  54         "claude"
  55       ],
  56       "council": true
  57     },
  58     "code": {
  59       "primary": "claude",
  60       "fallback": [
  61         "gpt",
  62         "local"
  63       ]
  64     },
  65     "review": {
  66       "primary": "claude",
  67       "fallback": [
  68         "gpt"
  69       ]
  70     },
  71     "draft": {
  72       "primary": "gpt",
  73       "fallback": [
  74         "claude"
  75       ]
  76     },
  77     "long_context": {
  78       "primary": "gemini",
  79       "fallback": [
  80         "claude"
  81       ]
  82     },
  83     "private": {
  84       "primary": "local",
  85       "fallback": []
  86     },
  87     "engineering_decision": {
  88       "primary": "claude",
  89       "fallback": [
  90         "gpt"
  91       ],
  92       "council": true,
  93       "council_members": [
  94         "perplexity",
  95         "claude",
  96         "gpt",
  97         "gemini"
  98       ]
  99     },
 100     "ocr": {
 101       "primary": "vision",
 102       "fallback": [
 103         "gemini"
 104       ]
 105     }
 106   },
 107   "privacy": {
 108     "confidential_route": "private",
 109     "markers": [
 110       "VERTRAULICH",
 111       "CONFIDENTIAL",
 112       "[P3]"
 113     ]
 114   },
 115   "lessons_dir": "COMMUNICATION/lessons"
 116 }
~~~~

### FILE: orchestrator/config/sync_targets.json
~~~~json
   1 {
   2   "_doc": "Ziele fuer sync_nexus_rclone.ps1 (Drive-Ordner-IDs, unabhaengig von Pfaden/Namensdubletten). remote = Name aus 'rclone config'.",
   3   "remote": "gdrive",
   4   "targets": {
   5     "SSOT":      "1j3FLJkWpQv6xGA_KO0D9sMyA11f0vxBV",
   6     "BENCHMARK": "1ac7jYmO5SDtbXtjhfwylW_7QgpVi2i-N"
   7   },
   8   "jobs": [
   9     {"src": "orchestrator", "target": "SSOT",      "dest": "nexus-llm-orchestrator"},
  10     {"src": "orchestrator", "target": "BENCHMARK", "dest": "nexus-llm-orchestrator"},
  11     {"src": "reports",      "target": "SSOT",      "dest": "nexus-reports"},
  12     {"src": "reports",      "target": "BENCHMARK", "dest": "nexus-reports"},
  13     {"src": "evaluation",   "target": "SSOT",      "dest": "nexus-evaluation"},
  14     {"src": "evaluation",   "target": "BENCHMARK", "dest": "nexus-evaluation"}
  15   ]
  16 }
~~~~

### FILE: orchestrator/registry/workflow-registry.json
~~~~json
   1 {
   2   "version": "1.1.0",
   3   "ssot": {
   4     "primary": "Google Drive /LLM-LOCAL-SSOT",
   5     "versioning": "github.com/julianzotter/nexus-platform",
   6     "mirror": [
   7       "OneDrive",
   8       "Dropbox"
   9     ],
  10     "perplexity_project": "https://www.perplexity.ai/projects/nexus-ai-multi-llm-system-JCDYwmIfSliQifFlkLD9NA"
  11   },
  12   "pipeline": [
  13     "inventory",
  14     "parse",
  15     "validate",
  16     "register",
  17     "report"
  18   ],
  19   "workflows": [
  20     {
  21       "id": "WF-01",
  22       "name": "knowledge-ingestion",
  23       "route": "long_context",
  24       "source": "Drive:nexus-mvp.zip/skills/knowledge-ingestion"
  25     },
  26     {
  27       "id": "WF-02",
  28       "name": "knowledge-quality-gate",
  29       "route": "review",
  30       "source": "Drive:nexus-mvp.zip/skills/knowledge-quality-gate"
  31     },
  32     {
  33       "id": "WF-03",
  34       "name": "source-governance",
  35       "route": "review",
  36       "source": "Drive:nexus-mvp.zip/skills/source-governance"
  37     },
  38     {
  39       "id": "WF-04",
  40       "name": "norm-chunk-validator",
  41       "route": "norm_check",
  42       "source": "Drive:nexus-skill-family.zip"
  43     },
  44     {
  45       "id": "WF-05",
  46       "name": "ssot-github-sync",
  47       "route": "code",
  48       "source": "Drive:nexus-skill-family.zip"
  49     },
  50     {
  51       "id": "WF-06",
  52       "name": "audit-reporter",
  53       "route": "draft",
  54       "source": "Drive:nexus-skill-family.zip"
  55     },
  56     {
  57       "id": "WF-07",
  58       "name": "transcript-ingest",
  59       "route": "long_context",
  60       "source": "Drive:nexus-skill-family.zip"
  61     },
  62     {
  63       "id": "WF-08",
  64       "name": "license-router",
  65       "route": "review",
  66       "source": "Drive:nexus-skill-family.zip"
  67     },
  68     {
  69       "id": "WF-09",
  70       "name": "ko-extractor",
  71       "route": "long_context",
  72       "source": "Drive:nexus-skill-family.zip"
  73     },
  74     {
  75       "id": "WF-10",
  76       "name": "rag-eval-harness",
  77       "route": "code",
  78       "source": "Drive:nexus-skill-family.zip"
  79     },
  80     {
  81       "id": "WF-11",
  82       "name": "pdf-ground-truth-freeze",
  83       "route": "review",
  84       "source": "Drive:nexus-skill-family.zip"
  85     },
  86     {
  87       "id": "WF-12",
  88       "name": "human-ocr-public",
  89       "route": "private",
  90       "source": "Drive:nexus-skill-family.zip"
  91     },
  92     {
  93       "id": "WF-13",
  94       "name": "registry-inventory (TASK-00004)",
  95       "route": "code",
  96       "source": "GitHub:nexus-platform/tools"
  97     },
  98     {
  99       "id": "WF-14",
 100       "name": "control-tower-daily-0700",
 101       "route": "draft",
 102       "source": "Perplexity automation"
 103     },
 104     {
 105       "id": "WF-15",
 106       "name": "mail-executive-triage",
 107       "route": "draft",
 108       "source": "GitHub:EMAIL-MANAGER-DASHBAORD"
 109     },
 110     {
 111       "id": "WF-16",
 112       "name": "engineering-decision-council",
 113       "route": "engineering_decision",
 114       "source": "nexus_orch.council"
 115     },
 116     {
 117       "id": "WF-17",
 118       "name": "vision-ocr (Plaene, Scans, Fotos, Normtabellen)",
 119       "route": "ocr",
 120       "source": "Google Cloud Vision (Perplexity-Connector / REST)"
 121     }
 122   ]
 123 }
~~~~

### FILE: orchestrator/nexus_orch/core.py
~~~~python
   1 """Router + fallback + council + shared-lessons log."""
   2 import datetime as dt, hashlib, json, pathlib
   3 from .providers import Provider, ProviderError
   4 
   5 ROOT = pathlib.Path(__file__).resolve().parent.parent
   6 
   7 def load_config(path=None):
   8     return json.loads(pathlib.Path(path or ROOT / "config/routing.json").read_text(encoding="utf-8"))
   9 
  10 class Orchestrator:
  11     def __init__(self, cfg=None, providers=None, root=ROOT):
  12         self.cfg = cfg or load_config()
  13         self.root = pathlib.Path(root)
  14         self.providers = providers or {n: Provider(n, c) for n, c in self.cfg["providers"].items()}
  15 
  16     def classify(self, task, prompt):
  17         p = self.cfg["privacy"]
  18         if any(m in prompt for m in p["markers"]):
  19             return p["confidential_route"]  # hard gate: confidential never leaves local
  20         if task not in self.cfg["routes"]:
  21             raise KeyError(f"unknown task '{task}', known: {sorted(self.cfg['routes'])}")
  22         return task
  23 
  24     def chain(self, route):
  25         r = self.cfg["routes"][route]
  26         return [r["primary"], *r.get("fallback", [])]
  27 
  28     def run(self, task, prompt, system=""):
  29         route = self.classify(task, prompt)
  30         errors = []
  31         for name in self.chain(route):
  32             try:
  33                 res = self.providers[name].complete(prompt, system, self.cfg["default_temperature"])
  34                 out = {"route": route, "provider": name, **res, "errors": errors}
  35                 self._audit(out, prompt)
  36                 return out
  37             except ProviderError as e:
  38                 errors.append(str(e))
  39         raise ProviderError(f"all providers failed for route {route}: {errors}")
  40 
  41     def council(self, task, prompt, system=""):
  42         route = self.classify(task, prompt)
  43         r = self.cfg["routes"][route]
  44         members = r.get("council_members") or self.chain(route)
  45         answers = {}
  46         for n in members:
  47             try:
  48                 answers[n] = self.providers[n].complete(prompt, system, 0.0)["text"]
  49             except ProviderError as e:
  50                 answers[n] = None
  51         valid = {k: v for k, v in answers.items() if v}
  52         if not valid:
  53             raise ProviderError("council: no valid answers")
  54         norm = lambda s: " ".join(s.lower().split())
  55         groups = {}
  56         for k, v in valid.items():
  57             groups.setdefault(norm(v), []).append(k)
  58         consensus = len(groups) == 1
  59         synth = None
  60         if not consensus:
  61             judge = r["primary"] if r["primary"] in valid else next(iter(valid))
  62             body = "\n\n".join(f"### {k}\n{v}" for k, v in valid.items())
  63             synth = self.providers[judge].complete(
  64                 f"Frage:\n{prompt}\n\nAntworten:\n{body}\n\nSynthetisiere: 1) Konsens, 2) Abweichungen je Modell, 3) begruendete Empfehlung.",
  65                 system, 0.0)["text"]
  66         out = {"route": route, "members": members, "answers": answers, "consensus": consensus,
  67                "synthesis": synth or next(iter(valid.values()))}
  68         self._audit(out, prompt)
  69         return out
  70 
  71     def _audit(self, out, prompt):
  72         d = self.root / "COMMUNICATION/audit"; d.mkdir(parents=True, exist_ok=True)
  73         rec = {"ts": dt.datetime.now(dt.timezone.utc).isoformat(), "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
  74                **{k: out[k] for k in ("route", "provider", "consensus") if k in out}}
  75         with open(d / f"{dt.date.today():%y_%m_%d}_audit.jsonl", "a", encoding="utf-8") as f:
  76             f.write(json.dumps(rec, ensure_ascii=False) + "\n")
  77 
  78 REQUIRED_LESSON = ("agent", "context", "condition", "pattern", "evidence")
  79 
  80 def write_lesson(lesson, root=ROOT):
  81     """Shared-Lessons-Layer: conditional reusable pattern, published to COMMUNICATION/lessons."""
  82     miss = [k for k in REQUIRED_LESSON if not lesson.get(k)]
  83     if miss:
  84         raise ValueError(f"lesson missing fields: {miss}")
  85     lesson = {"id": hashlib.sha1(json.dumps(lesson, sort_keys=True).encode()).hexdigest()[:12],
  86               "ts": dt.datetime.now(dt.timezone.utc).isoformat(), "status": "PROPOSED", **lesson}
  87     p = pathlib.Path(root) / "COMMUNICATION/lessons/lessons.jsonl"; p.parent.mkdir(parents=True, exist_ok=True)
  88     with open(p, "a", encoding="utf-8") as f:
  89         f.write(json.dumps(lesson, ensure_ascii=False) + "\n")
  90     return lesson
  91 
  92 def search_lessons(query, root=ROOT):
  93     p = pathlib.Path(root) / "COMMUNICATION/lessons/lessons.jsonl"
  94     if not p.exists():
  95         return []
  96     q = query.lower().split()
  97     rows = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
  98     return [r for r in rows if all(t in json.dumps(r, ensure_ascii=False).lower() for t in q)]
~~~~

### FILE: orchestrator/nexus_orch/providers.py
~~~~python
   1 """Provider adapters (stdlib only). temperature=0.0 default, deterministic."""
   2 import base64, json, os, urllib.error, urllib.request
   3 
   4 class ProviderError(RuntimeError):
   5     pass
   6 
   7 def _post(url, headers, body, timeout=120):
   8     req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", **headers})
   9     try:
  10         with urllib.request.urlopen(req, timeout=timeout) as r:
  11             return json.loads(r.read())
  12     except urllib.error.HTTPError as e:
  13         detail = e.read().decode("utf-8", "replace")[:300]
  14         hint = " -> Modell fehlt: 'ollama pull <model>' bzw. 'ollama list' pruefen" if e.code == 404 and "11434" in url else ""
  15         raise ProviderError(f"{url.split('?')[0]}: HTTP {e.code} {detail}{hint}") from e
  16     except Exception as e:  # network, JSON
  17         raise ProviderError(f"{url.split('?')[0]}: {e}") from e
  18 
  19 class Provider:
  20     def __init__(self, name, cfg):
  21         self.name, self.cfg = name, cfg
  22     def key(self):
  23         env = self.cfg.get("env_key")
  24         if env is None:
  25             return ""
  26         k = os.environ.get(env)
  27         if not k:
  28             raise ProviderError(f"{self.name}: env {env} missing")
  29         return k
  30     def available(self):
  31         try:
  32             self.key(); return True
  33         except ProviderError:
  34             return False
  35     def complete(self, prompt, system="", temperature=0.0):
  36         post = lambda u, h, body: _post(u, h, body, self.cfg.get("timeout", 120))
  37         kind, base, model, key = self.cfg["kind"], self.cfg["base_url"], self.cfg["model"], self.key()
  38         if kind == "openai_compat":
  39             msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
  40             h = {"Authorization": f"Bearer {key}"} if key else {}
  41             d = post(f"{base}/chat/completions", h, {"model": model, "messages": msgs, "temperature": temperature})
  42             return {"text": d["choices"][0]["message"]["content"], "citations": d.get("citations", []), "model": model}
  43         if kind == "anthropic":
  44             d = post(f"{base}/v1/messages", {"x-api-key": key, "anthropic-version": "2023-06-01"},
  45                       {"model": model, "max_tokens": self.cfg.get("max_tokens", 4096), "system": system, "temperature": temperature,
  46                        "messages": [{"role": "user", "content": prompt}]})
  47             return {"text": "".join(b.get("text", "") for b in d["content"]), "citations": [], "model": model}
  48         if kind == "gemini":
  49             body = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": temperature}}
  50             if system:
  51                 body["systemInstruction"] = {"parts": [{"text": system}]}
  52             d = post(f"{base}/models/{model}:generateContent?key={key}", {}, body)
  53             return {"text": d["candidates"][0]["content"]["parts"][0]["text"], "citations": [], "model": model}
  54         if kind == "ollama":
  55             # native API: num_ctx per request, unabhaengig vom App-Regler
  56             msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
  57             d = post(f"{base}/api/chat", {}, {"model": model, "messages": msgs, "stream": False,
  58                       "options": {"temperature": temperature, "num_ctx": self.cfg.get("num_ctx", 16384)}})
  59             return {"text": d["message"]["content"], "citations": [], "model": model}
  60         if kind == "gcv_ocr":
  61             # prompt = image URL (http/https/gs) or local file path
  62             img = {"source": {"imageUri": prompt}} if prompt.startswith(("http://", "https://", "gs://")) \
  63                 else {"content": base64.b64encode(open(prompt, "rb").read()).decode()}
  64             d = post(f"{base}/images:annotate?key={key}", {},
  65                       {"requests": [{"image": img, "features": [{"type": model}]}]})
  66             r0 = d["responses"][0]
  67             if "error" in r0:
  68                 raise ProviderError(f"vision: {r0['error'].get('message')}")
  69             return {"text": r0.get("fullTextAnnotation", {}).get("text", ""), "citations": [prompt], "model": model}
  70         raise ProviderError(f"unknown kind {kind}")
  71 
  72 class MockProvider(Provider):
  73     """For tests / dry-run."""
  74     def __init__(self, name, answer="OK", fail=False):
  75         super().__init__(name, {"kind": "mock", "model": "mock", "env_key": None})
  76         self.answer, self.fail = answer, fail
  77     def complete(self, prompt, system="", temperature=0.0):
  78         if self.fail:
  79             raise ProviderError(f"{self.name}: forced failure")
  80         return {"text": self.answer, "citations": [], "model": "mock"}
~~~~

### FILE: orchestrator/nexus_orch/cli.py
~~~~python
   1 """python -m nexus_orch.cli {status|run|council|lesson|lessons|registry}"""
   2 import argparse, json, pathlib, sys
   3 from .core import Orchestrator, write_lesson, search_lessons, ROOT
   4 from .providers import ProviderError
   5 
   6 def main(argv=None):
   7     ap = argparse.ArgumentParser(prog="nexus")
   8     sp = ap.add_subparsers(dest="cmd", required=True)
   9     sp.add_parser("status")
  10     for c in ("run", "council"):
  11         p = sp.add_parser(c); p.add_argument("task"); p.add_argument("prompt"); p.add_argument("--system", default="")
  12     p = sp.add_parser("lesson"); [p.add_argument(f"--{k}", required=True) for k in ("agent", "context", "condition", "pattern", "evidence")]
  13     p = sp.add_parser("lessons"); p.add_argument("query", nargs="?", default="")
  14     sp.add_parser("registry")
  15     p = sp.add_parser("eval", help="Evaluierung an alle Modelle mit Key senden, Berichte + Auswertung schreiben")
  16     p.add_argument("--models", default="", help="z.B. perplexity,claude (Standard: alle Cloud-Modelle mit Key)")
  17     p.add_argument("--dry-run", action="store_true", help="nur Prompt bauen und Groesse/Modelle anzeigen")
  18     sp.add_parser("eval-summary", help="vorhandene Berichte in evaluation/berichte auswerten")
  19     a = ap.parse_args(argv)
  20     o = Orchestrator()
  21     if a.cmd == "status":
  22         r = {"providers": {n: p.available() for n, p in o.providers.items()},
  23              "routes": {k: o.chain(k) for k in o.cfg["routes"]}}
  24     elif a.cmd in ("run", "council"):
  25         try:
  26             r = (o.run if a.cmd == "run" else o.council)(a.task, a.prompt, a.system)
  27         except (ProviderError, KeyError) as e:
  28             missing = [p.cfg["env_key"] for p in o.providers.values() if p.cfg.get("env_key") and not p.available()]
  29             print(json.dumps({"ok": False, "error": str(e).strip("'\""), "missing_keys": missing,
  30                               "hint": "Keys setzen: .\\setup.ps1, danach neues PowerShell-Fenster; lokal: Ollama starten"},
  31                              ensure_ascii=False, indent=2))
  32             return 2
  33     elif a.cmd == "lesson":
  34         r = write_lesson({k: getattr(a, k) for k in ("agent", "context", "condition", "pattern", "evidence")})
  35     elif a.cmd == "lessons":
  36         r = search_lessons(a.query)
  37     elif a.cmd == "eval":
  38         from . import evaluate as ev
  39         models = [m for m in a.models.split(",") if m] or None
  40         if a.dry_run:
  41             pr = ev.build_prompt()
  42             r = {"commit": ev.commit(), "prompt_zeichen": len(pr), "ca_tokens": len(pr) // 4,
  43                  "modelle": {n: o.providers[n].available() for n in (models or ev.CLOUD)}}
  44         else:
  45             r = ev.run(o, models)
  46     elif a.cmd == "eval-summary":
  47         from . import evaluate as ev
  48         r = {"auswertung": ev.aggregate(ev.EVAL / "berichte")}
  49     else:
  50         r = json.loads((ROOT / "registry/workflow-registry.json").read_text(encoding="utf-8"))
  51     print(json.dumps(r, ensure_ascii=False, indent=2))
  52 
  53 if __name__ == "__main__":
  54     sys.exit(main())
~~~~

### FILE: orchestrator/nexus_orch/evaluate.py
~~~~python
   1 """nexus eval: Evaluierungsbogen + aktuelles Kontextpaket an alle verfuegbaren Modelle, Berichte speichern, auswerten.
   2 
   3 Bewusste Ausnahme vom Privacy-Gate: gesendet wird ausschliesslich Repo-Inhalt (Code/Doku, keine Projektdaten).
   4 Der Bogen wird gegen Marker geprueft; enthaelt ein Repo-File echte Projektdaten, gehoert es nicht ins Repo.
   5 """
   6 import datetime as dt, json, pathlib, re, runpy, subprocess, sys
   7 
   8 REPO = pathlib.Path(__file__).resolve().parents[2]
   9 EVAL = REPO / "evaluation"
  10 BOGEN = EVAL / "NEXUS_EVAL_BOGEN_v1.0.md"
  11 PACK_FILES = [
  12     "README.md", "orchestrator/README.md", "orchestrator/pyproject.toml",
  13     "orchestrator/config/routing.json", "orchestrator/config/sync_targets.json",
  14     "orchestrator/registry/workflow-registry.json",
  15     "orchestrator/nexus_orch/core.py", "orchestrator/nexus_orch/providers.py",
  16     "orchestrator/nexus_orch/cli.py", "orchestrator/nexus_orch/evaluate.py",
  17     "orchestrator/tests/test_orch.py", "orchestrator/setup.ps1",
  18     "orchestrator/sync_nexus.ps1", "orchestrator/sync_nexus_rclone.ps1", "orchestrator/install_autosync.ps1",
  19 ]
  20 LANG = {".py": "python", ".json": "json", ".ps1": "powershell", ".toml": "toml", ".md": "markdown"}
  21 CLOUD = ["perplexity", "claude", "gpt", "gemini"]
  22 
  23 def commit(repo=REPO):
  24     try:
  25         return subprocess.run(["git", "-C", str(repo), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip() or "unbekannt"
  26     except OSError:
  27         return "unbekannt"
  28 
  29 def build_pack(repo=REPO):
  30     """Kontextpaket zum aktuellen Stand: Dateibaum + Kerndateien mit Zeilennummern."""
  31     repo = pathlib.Path(repo)
  32     skip = {".git", "__pycache__", ".pytest_cache", "node_modules", ".venv", "venv"}
  33     tree = [f"{p.stat().st_size:>9}  {p.relative_to(repo).as_posix()}" for p in sorted(repo.rglob("*"))
  34             if p.is_file() and not (set(p.relative_to(repo).parts) & skip) and "egg-info" not in str(p)]
  35     out = [f"## 6 Kontextpaket (automatisch erzeugt, Commit {commit(repo)}, {dt.date.today()})", "", "### Dateibaum", "```", *tree, "```"]
  36     for rel in PACK_FILES:
  37         f = repo / rel
  38         if not f.exists():
  39             continue
  40         lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
  41         out += ["", f"### FILE: {rel}", "~~~~" + LANG.get(f.suffix, "text"), *[f"{i:4} {l}" for i, l in enumerate(lines, 1)], "~~~~"]
  42     return "\n".join(out)
  43 
  44 def build_prompt(repo=REPO):
  45     text = (pathlib.Path(repo) / "evaluation/NEXUS_EVAL_BOGEN_v1.0.md").read_text(encoding="utf-8")
  46     head = re.split(r"(?m)^## 6 Kontextpaket", text)[0]  # Anweisung + Kriterien + Format, ohne altes Paket
  47     return head.rstrip() + "\n\n" + build_pack(repo)
  48 
  49 def run(orch, models=None, outdir=None, repo=REPO):
  50     outdir = pathlib.Path(outdir or pathlib.Path(repo) / "evaluation/berichte"); outdir.mkdir(parents=True, exist_ok=True)
  51     prompt, stamp = build_prompt(repo), dt.date.today().strftime("%y%m%d")
  52     system = "Du bist unabhaengige Pruefinstanz. Befolge den Evaluierungsbogen exakt, inklusive JSON-Block am Ende. Deutsch."
  53     done, skipped, failed = [], [], []
  54     for name in models or CLOUD:
  55         p = orch.providers.get(name)
  56         if p is None or not p.available():
  57             skipped.append(name); continue
  58         p.cfg = {**p.cfg, "timeout": 900, "max_tokens": max(p.cfg.get("max_tokens", 4096), 8192)}
  59         try:
  60             r = p.complete(prompt, system, 0.0)
  61         except Exception as e:  # ProviderError oder unerwartete Antwort
  62             failed.append(f"{name}: {e}"); continue
  63         f = outdir / f"EVAL_{name}_{stamp}.md"
  64         body = r["text"]
  65         if r.get("citations"):
  66             body += "\n\n## Quellen (Provider)\n" + "\n".join(f"- {c}" for c in r["citations"])
  67         f.write_text(f"<!-- model={r.get('model')} commit={commit(repo)} -->\n" + body, encoding="utf-8")
  68         done.append(f.name)
  69     summary = aggregate(outdir) if done or list(outdir.glob("EVAL_*.md")) else None
  70     return {"commit": commit(repo), "berichte": done, "uebersprungen_ohne_key": skipped, "fehler": failed,
  71             "auswertung": summary, "prompt_zeichen": len(prompt)}
  72 
  73 def aggregate(outdir):
  74     script = EVAL / "nexus_eval_auswertung.py"
  75     if not script.exists():
  76         return None
  77     argv = sys.argv
  78     try:
  79         sys.argv = [str(script), str(outdir)]
  80         runpy.run_path(str(script), run_name="__main__")
  81     except SystemExit as e:
  82         return f"keine Auswertung: {e}"
  83     finally:
  84         sys.argv = argv
  85     return str(pathlib.Path(outdir) / "NEXUS_EVAL_AUSWERTUNG.md")
~~~~

### FILE: orchestrator/tests/test_orch.py
~~~~python
   1 import json, pytest
   2 from nexus_orch.core import Orchestrator, load_config, write_lesson, search_lessons, ROOT
   3 from nexus_orch.providers import MockProvider, ProviderError
   4 
   5 def mk(tmp_path, **over):
   6     cfg = load_config()
   7     prov = {n: MockProvider(n, answer=f"A-{n}") for n in cfg["providers"]}
   8     prov.update(over)
   9     return Orchestrator(cfg, prov, root=tmp_path)
  10 
  11 def test_primary(tmp_path):
  12     r = mk(tmp_path).run("research", "Q")
  13     assert r["provider"] == "perplexity"
  14 
  15 def test_fallback(tmp_path):
  16     r = mk(tmp_path, perplexity=MockProvider("perplexity", fail=True)).run("research", "Q")
  17     assert r["provider"] == "gemini" and r["errors"]
  18 
  19 def test_privacy_gate(tmp_path):
  20     assert mk(tmp_path).run("research", "VERTRAULICH Statik")["provider"] == "local"
  21 
  22 def test_privacy_no_cloud_fallback(tmp_path):
  23     with pytest.raises(ProviderError):
  24         mk(tmp_path, local=MockProvider("local", fail=True)).run("research", "VERTRAULICH x")
  25 
  26 def test_unknown_task(tmp_path):
  27     with pytest.raises(KeyError):
  28         mk(tmp_path).run("xyz", "Q")
  29 
  30 def test_council_dissent(tmp_path):
  31     r = mk(tmp_path).council("engineering_decision", "Q")
  32     assert r["consensus"] is False and r["synthesis"]
  33 
  34 def test_council_consensus(tmp_path):
  35     cfg = load_config()
  36     o = Orchestrator(cfg, {n: MockProvider(n, answer="Same") for n in cfg["providers"]}, root=tmp_path)
  37     assert o.council("engineering_decision", "Q")["consensus"] is True
  38 
  39 def test_lessons(tmp_path):
  40     with pytest.raises(ValueError):
  41         write_lesson({"agent": "x"}, root=tmp_path)
  42     write_lesson({"agent": "claude", "context": "EC5", "condition": "wenn kmod fehlt", "pattern": "NKL pruefen", "evidence": "s1"}, root=tmp_path)
  43     assert len(search_lessons("kmod", root=tmp_path)) == 1
  44 
  45 def test_registry_routes_valid():
  46     cfg = load_config(); reg = json.loads((ROOT / "registry/workflow-registry.json").read_text())
  47     assert all(w["route"] in cfg["routes"] for w in reg["workflows"])
  48     assert all(set(r["fallback"] + [r["primary"]]) <= set(cfg["providers"]) for r in cfg["routes"].values())
  49 
  50 def test_ocr_route(tmp_path):
  51     assert mk(tmp_path).run("ocr", "https://x/plan.jpg")["provider"] == "vision"
  52 
  53 def test_ocr_fallback(tmp_path):
  54     assert mk(tmp_path, vision=MockProvider("vision", fail=True)).run("ocr", "https://x/p.jpg")["provider"] == "gemini"
  55 
  56 def test_ocr_confidential_local(tmp_path):
  57     assert mk(tmp_path).run("ocr", "VERTRAULICH C:/scan.png")["provider"] == "local"
  58 
  59 def test_cli_clean_error(monkeypatch, capsys):
  60     from nexus_orch import cli
  61     for k in ("PERPLEXITY_API_KEY", "GEMINI_API_KEY", "OPENAI_API_KEY"):
  62         monkeypatch.delenv(k, raising=False)
  63     assert cli.main(["run", "research", "Q"]) == 2
  64     out = json.loads(capsys.readouterr().out)
  65     assert out["ok"] is False and "PERPLEXITY_API_KEY" in out["missing_keys"]
  66 
  67 def test_http_error_detail(monkeypatch):
  68     import io, urllib.error, urllib.request
  69     from nexus_orch import providers
  70     def boom(*a, **k):
  71         raise urllib.error.HTTPError("http://localhost:11434/v1/chat/completions", 404, "Not Found", {}, io.BytesIO(b'{"error":"model \'qwen2.5:7b\' not found"}'))
  72     monkeypatch.setattr(urllib.request, "urlopen", boom)
  73     with pytest.raises(ProviderError) as e:
  74         providers._post("http://localhost:11434/v1/chat/completions", {}, {})
  75     assert "not found" in str(e.value) and "ollama pull" in str(e.value)
  76 
  77 def test_ollama_num_ctx(monkeypatch):
  78     from nexus_orch import providers
  79     seen = {}
  80     def fake(url, h, body, timeout=120):
  81         seen.update(url=url, body=body); return {"message": {"content": "OK"}}
  82     monkeypatch.setattr(providers, "_post", fake)
  83     cfg = load_config()["providers"]["local"]
  84     r = providers.Provider("local", cfg).complete("Q")
  85     assert r["text"] == "OK" and seen["url"].endswith("/api/chat") and seen["body"]["options"]["num_ctx"] == 16384
  86 
  87 EVAL_JSON = '{"modell":"mock","datum":"2026-10-13","repo_zugriff":false,"noten":{"K1":2,"K2":3,"K3":2,"K4":3},"gesamt":2.5,"ko_regel":false,"pruefpunkte":{"K1.1":"erfuellt"},"kritisch":[],"massnahmen":[{"rang":1,"massnahme":"Retries","datei":"providers.py","kriterium":"K1","wirkung":"hoch","aufwand":"S"}]}'
  88 
  89 def test_eval_prompt_fresh_pack():
  90     from nexus_orch import evaluate as ev
  91     pr = ev.build_prompt()
  92     assert "## 0 Anweisung" in pr and "Kontextpaket (automatisch erzeugt" in pr
  93     assert "### FILE: orchestrator/nexus_orch/core.py" in pr and pr.count("\n## 6 Kontextpaket") == 1
  94 
  95 def test_eval_run_and_aggregate(tmp_path):
  96     from nexus_orch import evaluate as ev
  97     cfg = load_config()
  98     prov = {n: MockProvider(n, answer="# Bericht\n```json\n" + EVAL_JSON + "\n```") for n in cfg["providers"]}
  99     prov["gemini"] = MockProvider("gemini", fail=True)
 100     o = Orchestrator(cfg, prov, root=tmp_path)
 101     r = ev.run(o, ["perplexity", "claude", "gemini"], outdir=tmp_path)
 102     assert len(r["berichte"]) == 2 and r["fehler"] and (tmp_path / "NEXUS_EVAL_AUSWERTUNG.md").exists()
~~~~

### FILE: orchestrator/setup.ps1
~~~~powershell
   1 # NEXUS-AI Multi-LLM Orchestrator - Windows Setup (Keys nur als User-Env, nie im Repo)
   2 python -m pip install -q pytest
   3 foreach ($k in "PERPLEXITY_API_KEY","ANTHROPIC_API_KEY","OPENAI_API_KEY","GEMINI_API_KEY","GOOGLE_VISION_API_KEY") {
   4   if (-not [Environment]::GetEnvironmentVariable($k,"User")) {
   5     $v = Read-Host "$k (leer = ueberspringen)" -AsSecureString
   6     $p = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($v))
   7     if ($p) { [Environment]::SetEnvironmentVariable($k,$p,"User"); Set-Item "env:$k" $p }
   8   }
   9 }
  10 python -m pytest -q tests
  11 python -m nexus_orch.cli status
~~~~

### FILE: orchestrator/sync_nexus.ps1
~~~~powershell
   1 # NEXUS Sync: GitHub (nexus-platform, main) -> Google Drive for desktop (G:)
   2 # Richtung: GitHub = Versionierung -> Drive = SSOT-Ablage + Benchmark-Kopie. Kein Push, kein Loeschen (robocopy ohne /MIR).
   3 #   .\sync_nexus.ps1              Orchestrator (SSOT + Benchmark) + komplettes Repo (SSOT\nexus-platform)
   4 #   .\sync_nexus.ps1 -NoFullRepo  ohne komplettes Repo (Orchestrator, reports, evaluation bleiben)
   5 param(
   6   [string]$Repo      = "$env:USERPROFILE\nexus-platform",
   7   [string]$Drive     = "G:\Meine Ablage",
   8   [string]$Ssot      = "_developement\LLM-LOCAL-SSOT\nexus-llm-orchestrator",
   9   [string]$Benchmark = "_INDEX_LNK\BENCHMARK Multi-LLM-Orchestrierung\nexus-llm-orchestrator",
  10   [string]$FullRepo  = "_developement\LLM-LOCAL-SSOT\nexus-platform",
  11   [switch]$NoFullRepo
  12 )
  13 $ErrorActionPreference = "Stop"
  14 if (-not (Test-Path $Drive)) { throw "Drive-Pfad fehlt: $Drive (Google Drive for desktop gestartet?)" }
  15 if (-not (Test-Path $Repo)) { git clone https://github.com/julianzotter/nexus-platform.git $Repo }
  16 git -C $Repo checkout main; git -C $Repo pull --ff-only
  17 if ($LASTEXITCODE -ne 0) { throw "git pull fehlgeschlagen (lokale Aenderungen? -> git -C `"$Repo`" status)" }
  18 $src = Join-Path $Repo "orchestrator"
  19 python -m pytest -q (Join-Path $src "tests"); if ($LASTEXITCODE -ne 0) { throw "Tests fehlgeschlagen - kein Sync" }
  20 $sha = (git -C $Repo rev-parse --short HEAD)
  21 $XD  = @(".git", "__pycache__", ".pytest_cache", ".ipynb_checkpoints", "node_modules", ".venv", "venv", "audit")
  22 $XF  = @("*.pyc", ".env", "*.key", "*.pem", "*.secret")
  23 
  24 function Sync-Dir($from, $to) {
  25   robocopy $from $to /E /XD $XD /XF $XF /R:2 /W:2 /NFL /NDL /NJH /NP | Out-Null
  26   if ($LASTEXITCODE -ge 8) { throw "robocopy Fehler $LASTEXITCODE -> $to" }
  27   "commit=$sha`nsynced=$(Get-Date -Format s)`nsource=github.com/julianzotter/nexus-platform/$(Split-Path $from -Leaf)" |
  28     Set-Content (Join-Path $to "SYNC_STAMP.txt") -Encoding UTF8
  29   Write-Host "[OK] $to  @ $sha"
  30 }
  31 
  32 $jobs = @(@($src, $Ssot), @($src, $Benchmark))
  33 foreach ($d in "reports", "evaluation") {           # wie sync_targets.json (rclone): nexus-reports / nexus-evaluation
  34   $from = Join-Path $Repo $d
  35   if (Test-Path $from) { foreach ($t in $Ssot, $Benchmark) { $jobs += ,@($from, (Join-Path (Split-Path $t) "nexus-$d")) } }
  36 }
  37 if (-not $NoFullRepo) { $jobs += ,@($Repo, $FullRepo) }
  38 foreach ($j in $jobs) { Sync-Dir $j[0] (Join-Path $Drive $j[1]) }
~~~~

### FILE: orchestrator/sync_nexus_rclone.ps1
~~~~powershell
   1 # NEXUS Sync via rclone: GitHub (nexus-platform, main) -> Google Drive per Ordner-ID
   2 # Fuer Rechner ohne Google Drive for desktop (G:), Server/VM, Aufgabenplanung.
   3 # Kein Push, kein Loeschen in Drive (rclone copy, niemals sync/delete).
   4 #   .\sync_nexus_rclone.ps1               alle Jobs aus config\sync_targets.json
   5 #   .\sync_nexus_rclone.ps1 -DryRun       nur anzeigen
   6 #   .\sync_nexus_rclone.ps1 -Only reports nur Jobs mit src=reports
   7 #   .\sync_nexus_rclone.ps1 -SkipTests    ohne pytest (nicht empfohlen)
   8 param(
   9   [string]$Repo   = "$env:USERPROFILE\nexus-platform",
  10   [string]$Config = "",
  11   [string]$Only   = "",
  12   [switch]$DryRun,
  13   [switch]$SkipTests
  14 )
  15 $ErrorActionPreference = "Stop"
  16 if (-not (Get-Command rclone -ErrorAction SilentlyContinue)) { throw "rclone fehlt -> siehe orchestrator\README.md (Abschnitt Drive-Sync rclone)" }
  17 if (-not (Test-Path $Repo)) { git clone https://github.com/julianzotter/nexus-platform.git $Repo }
  18 git -C $Repo checkout main; git -C $Repo pull --ff-only
  19 if ($LASTEXITCODE -ne 0) { throw "git pull fehlgeschlagen (lokale Aenderungen? -> git -C `"$Repo`" status)" }
  20 if (-not $Config) { $Config = Join-Path $Repo "orchestrator\config\sync_targets.json" }
  21 $cfg = Get-Content $Config -Raw -Encoding UTF8 | ConvertFrom-Json
  22 $remote = $cfg.remote
  23 rclone listremotes | Out-String | ForEach-Object { if ($_ -notmatch "(?m)^$remote`:") { throw "rclone-Remote '$remote' fehlt -> rclone config (Storage: drive)" } }
  24 
  25 if (-not $SkipTests) {
  26   python -m pytest --version *> $null
  27   if ($LASTEXITCODE -ne 0) { throw "pytest fehlt -> python -m pip install pytest (oder -SkipTests)" }
  28   python -m pytest -q (Join-Path $Repo "orchestrator\tests"); if ($LASTEXITCODE -ne 0) { throw "Tests fehlgeschlagen - kein Sync" }
  29 }
  30 $sha = (git -C $Repo rev-parse --short HEAD)
  31 $excl = @("--exclude", ".git/**", "--exclude", "__pycache__/**", "--exclude", ".pytest_cache/**",
  32           "--exclude", ".ipynb_checkpoints/**", "--exclude", "node_modules/**", "--exclude", ".venv/**",
  33           "--exclude", "venv/**", "--exclude", "audit/**", "--exclude", "*.pyc", "--exclude", ".env",
  34           "--exclude", "*.key", "--exclude", "*.pem", "--exclude", "*.secret", "--exclude", "desktop.ini")
  35 $log = Join-Path $env:TEMP "nexus_rclone_$(Get-Date -Format yyMMdd_HHmmss).log"
  36 $ok = 0; $fail = @()
  37 foreach ($j in $cfg.jobs) {
  38   if ($Only -and $j.src -ne $Only) { continue }
  39   $from = Join-Path $Repo $j.src
  40   if (-not (Test-Path $from)) { Write-Host "[SKIP] $($j.src) fehlt im Repo"; continue }
  41   $id = $cfg.targets.($j.target)
  42   $to = "$remote,root_folder_id=$id`:$($j.dest)"
  43   $rcArgs = @("copy", $from, $to) + $excl + @("--log-file", $log, "--log-level", "INFO", "--stats-one-line", "-P")
  44   if ($DryRun) { $rcArgs += "--dry-run" }
  45   & rclone @rcArgs
  46   if ($LASTEXITCODE -ne 0) { $fail += "$($j.src)->$($j.target)"; Write-Host "[FEHLER] $($j.src) -> $($j.target)/$($j.dest)"; continue }
  47   if (-not $DryRun) {
  48     $stamp = "commit=$sha`nsynced=$(Get-Date -Format s)`nsource=github.com/julianzotter/nexus-platform/$($j.src)`nhost=$env:COMPUTERNAME"
  49     $stamp | rclone rcat "$to/SYNC_STAMP.txt"
  50   }
  51   $ok++; Write-Host "[OK] $($j.src) -> $($j.target)/$($j.dest) @ $sha"
  52 }
  53 Write-Host "Fertig: $ok ok, $($fail.Count) Fehler. Log: $log"
  54 if ($fail.Count) { exit 1 }
~~~~

### FILE: orchestrator/install_autosync.ps1
~~~~powershell
   1 # NEXUS Auto-Sync: Windows-Aufgabenplanung fuer sync_nexus.ps1 (GitHub main -> Google Drive, testgated, ohne Loeschen)
   2 #   .\install_autosync.ps1                  taeglich 07:00 + bei Anmeldung
   3 #   .\install_autosync.ps1 -Time 18:30      andere Uhrzeit
   4 #   .\install_autosync.ps1 -Rclone          sync_nexus_rclone.ps1 statt Laufwerk G:
   5 #   .\install_autosync.ps1 -Remove          Aufgabe entfernen
   6 param([string]$Time = "07:00", [switch]$Rclone, [switch]$Remove, [string]$Name = "NEXUS-AutoSync")
   7 $ErrorActionPreference = "Stop"
   8 if ($Remove) { Unregister-ScheduledTask -TaskName $Name -Confirm:$false; Write-Host "[OK] Aufgabe $Name entfernt"; return }
   9 $script = Join-Path $PSScriptRoot ($(if ($Rclone) { "sync_nexus_rclone.ps1" } else { "sync_nexus.ps1" }))
  10 if (-not (Test-Path $script)) { throw "Skript fehlt: $script" }
  11 $log = Join-Path $env:LOCALAPPDATA "NEXUS\autosync.log"
  12 New-Item -ItemType Directory -Force (Split-Path $log) | Out-Null
  13 $cmd = "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command `"& '$script' *>> '$log'`""
  14 $action   = New-ScheduledTaskAction -Execute "powershell.exe" -Argument $cmd -WorkingDirectory $PSScriptRoot
  15 $triggers = @((New-ScheduledTaskTrigger -Daily -At $Time), (New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME))
  16 $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RunOnlyIfNetworkAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 30)
  17 Register-ScheduledTask -TaskName $Name -Action $action -Trigger $triggers -Settings $settings -Description "NEXUS GitHub->Drive Sync" -Force | Out-Null
  18 Write-Host "[OK] Aufgabe $Name: taeglich $Time + bei Anmeldung -> $script"
  19 Write-Host "     Log: $log  ·  Sofort testen: Start-ScheduledTask -TaskName $Name"
~~~~