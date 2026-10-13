# NEXUS-AI Multi-LLM Orchestrator v1.2.0

Integrationsschicht des NEXUS AI-OS: ein Einstiegspunkt, der Aufgaben deterministisch (T=0.0) an Perplexity, Claude, GPT, Gemini oder ein lokales Modell (Ollama) routet.

## Funktionen
| Funktion | Umsetzung |
|---|---|
| Routing nach Aufgabentyp | `config/routing.json` → `routes` (research, norm_check, code, review, draft, long_context, private, engineering_decision) |
| Fallback-Kette | primary → fallback[], Fehler protokolliert |
| Privacy Hard Gate | Marker `VERTRAULICH`/`CONFIDENTIAL`/`[P3]` → nur `local`, kein Cloud-Fallback |
| Model Council | `council`: alle Mitglieder, Konsensprüfung, sonst Synthese (Konsens / Abweichungen / Empfehlung) |
| Perplexity-Integration | Sonar API (`sonar-pro`), Zitate werden mit ausgegeben |
| Shared Lessons Layer | `COMMUNICATION/lessons/lessons.jsonl` (agent, context, condition, pattern, evidence; Status PROPOSED) |
| OCR (Google Cloud Vision) | Route `ocr`: Vision `DOCUMENT_TEXT_DETECTION` (Bild-URL, gs:// oder lokaler Pfad), Fallback Gemini; vertraulich → lokal |
| Audit | `COMMUNICATION/audit/YY_MM_DD_audit.jsonl` (nur Prompt-Hash, kein Klartext) |
| Workflow-Registry | `registry/workflow-registry.json` – 17 Workflows (nexus-mvp, nexus-skill-family, nexus-platform, Control Tower, Mail-Triage) mit Route |

## Installation als Befehl `nexus`
```powershell
cd "$env:USERPROFILE\nexus-platform\orchestrator"; python -m pip install -e .
nexus status   # funktioniert danach in jedem Ordner
```

## Start
```powershell
.\setup.ps1                                   # Keys als User-Env, Tests, Status
python -m nexus_orch.cli run research "EN 1995-1-1 kmod NKL2 Quellen"
python -m nexus_orch.cli council engineering_decision "BSP vs. HBV Decke 7,5 m Spannweite"
python -m nexus_orch.cli lesson --agent claude --context EC5 --condition "wenn NKL fehlt" --pattern "NKL vor kmod abfragen" --evidence "Session 2026-10-13"
python -m nexus_orch.cli run ocr "C:/Scans/Positionsplan_EG.jpg"
python -m nexus_orch.cli lessons kmod
python -m nexus_orch.cli registry
```
Nur Python-Standardbibliothek; `pytest` für Tests. Modellnamen in `routing.json` anpassen.

## Drive-Sync (Windows)
```powershell
.\sync_nexus.ps1              # main pullen, Tests, dann: orchestrator -> LLM-LOCAL-SSOT + BENCHMARK, komplettes Repo -> LLM-LOCAL-SSOT\nexus-platform
.\sync_nexus.ps1 -NoFullRepo  # nur orchestrator
# ausgeschlossen: .git, Caches, venv, node_modules, .env/*.key/*.pem; kein Loeschen in Drive
```

## Drive-Sync per rclone (ohne Laufwerk G:)
Für Rechner ohne Google Drive for desktop, Server/VM oder Aufgabenplanung. Ziele per Drive-Ordner-ID in `config/sync_targets.json` (orchestrator, reports, evaluation → SSOT + BENCHMARK). Nur `rclone copy`, kein Löschen.
```powershell
# einmalig: rclone installieren (ohne winget)
$d="$env:LOCALAPPDATA\rclone"; New-Item -ItemType Directory -Force $d | Out-Null
Invoke-WebRequest https://downloads.rclone.org/rclone-current-windows-amd64.zip -OutFile "$env:TEMP\rclone.zip"
Expand-Archive "$env:TEMP\rclone.zip" "$env:TEMP\rclone" -Force
Copy-Item "$env:TEMP\rclone\rclone-*-windows-amd64\rclone.exe" $d -Force
[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path","User")+";$d", "User")
rclone config                      # n → gdrive → drive → scope 1 → Browser-Login
python -m pip install pytest

.\sync_nexus_rclone.ps1 -DryRun    # anzeigen
.\sync_nexus_rclone.ps1            # ausführen
.\sync_nexus_rclone.ps1 -Only reports
```
Wann welcher Weg: `sync_nexus.ps1` = Arbeits-PC mit Laufwerk G: · `sync_nexus_rclone.ps1` = PC ohne G:, Server, geplante Läufe, Ziel unabhängig von Ordnernamen.

## SSOT
Google Drive `/LLM-LOCAL-SSOT` = Wahrheit · GitHub `julianzotter/nexus-platform` = Versionierung · OneDrive/Dropbox = Spiegel · Perplexity-Projekt „NEXUS-AI Multi-LLM System“ = Orchestrator-Kontext.

## Automatisierung
| Ziel | Befehl | Wirkung |
|---|---|---|
| Drive-Sync ohne Handarbeit | `.\install_autosync.ps1` (einmalig) | Windows-Aufgabe `NEXUS-AutoSync`: täglich 07:00 + bei Anmeldung `sync_nexus.ps1`; Log `%LOCALAPPDATA%\NEXUS\autosync.log`; `-Rclone` für Rechner ohne G:, `-Remove` zum Entfernen |
| Evaluierung an alle Modelle | `nexus eval` | Bogen `evaluation/NEXUS_EVAL_BOGEN_v1.0.md` + frisch erzeugtes Kontextpaket (aktueller Commit) an alle Cloud-Modelle mit Key; Berichte `evaluation/berichte/EVAL_<modell>_<JJMMTT>.md`, Auswertung `NEXUS_EVAL_AUSWERTUNG.md` |
| Vorschau | `nexus eval --dry-run` | Prompt-Größe und verfügbare Modelle, ohne Versand |
| Auswahl | `nexus eval --models perplexity,claude` | nur diese Modelle |
| Nur Auswertung | `nexus eval-summary` | wertet manuell abgelegte Berichte (z. B. aus ChatGPT-Web) in `evaluation/berichte` aus |

`nexus eval` sendet nur Repo-Inhalt (Code/Doku). Das Privacy-Gate gilt dafür bewusst nicht; Projektdaten gehören nicht ins Repo. Das lokale Modell ist ausgenommen (Paket > 16k Kontext).
Drive-Sync kopiert zusätzlich `reports/` und `evaluation/` nach `LLM-LOCAL-SSOT\nexus-reports|nexus-evaluation` und `BENCHMARK…\nexus-reports|nexus-evaluation`.
