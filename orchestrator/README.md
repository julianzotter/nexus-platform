# NEXUS-AI Multi-LLM Orchestrator v1.1.0

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

## SSOT
Google Drive `/LLM-LOCAL-SSOT` = Wahrheit · GitHub `julianzotter/nexus-platform` = Versionierung · OneDrive/Dropbox = Spiegel · Perplexity-Projekt „NEXUS-AI Multi-LLM System“ = Orchestrator-Kontext.
