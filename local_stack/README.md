# NEXUS Local Stack v0.1.0 (Review-Kandidat, ID05)

Lokale, automatisch startende NEXUS-Laufzeit auf der ID01-Workstation, damit token-intensive
Arbeit lokal statt in Cloud-LLMs läuft. Nur Python-Standardbibliothek zur Laufzeit; `pytest` nur für Tests.

Status: **Implementiert und auf Linux getestet. Auf Windows nicht gelaufen (NOT_RUN). Keine Produktionsfreigabe.**
Freigabe erst nach Windows-Abnahme (`Test-NexusLocal.ps1`), unabhängigem Review und ID01-Entscheid (AGENTS.md Punkt 8).

## Architektur

```
Anmeldung Windows ──► Aufgabe "NEXUS-LocalStack" (AtLogOn +1 min, Watchdog alle 15 min, RestartCount 5)
                        └─► pythonw -m nexus_local.supervisor   (Einzelinstanz-Sperre, Job Object)
                              ├─ control_tower  127.0.0.1:8770   TASK-MANAGER-Dashboard
                              ├─ mcp_gateway    127.0.0.1:8766/mcp  MCP 2026-07-28 + Legacy 2025-11-25
                              ├─ ollama         127.0.0.1:11434  nur Überwachung (wird nie gestoppt)
                              ├─ bridges        OneDrive ⇄ Google Drive (G:) – einwegige Regeln, Journal
                              ├─ git_mirror     EXPORT-APPROVED ─► GitHub review/* (standardmäßig AUS)
                              ├─ gpt_to_skill   GPT-Export ─► SKILL.md (lokales Staging)
                              └─ reporter       Heartbeat LLM-HISTORY-LOG + Statusbericht WORK
```

## Wo laufen die Watcher?

Ausschließlich auf der Workstation. Nur dort sind Drive for desktop (G:), OneDrive und Git gleichzeitig eingebunden.

| Was | Ort | Warum |
|---|---|---|
| Programmcode (unveränderlich je Version) | `%LOCALAPPDATA%\NEXUS\local\app\<commit>\` | Kein laufender Code in Cloud-/Git-Arbeitskopie |
| Konfiguration | `%LOCALAPPDATA%\NEXUS\local\nexus-local.json` | wird vom Installer nie überschrieben |
| Zustand (SQLite, Journal, Sperre) | `%LOCALAPPDATA%\NEXUS\local\state\` | nie in synchronisierten Ordnern |
| Logs (Tagesdateien, nie gelöscht) | `%LOCALAPPDATA%\NEXUS\local\logs\` | |
| Token (nur Benutzer-ACL) | `%LOCALAPPDATA%\NEXUS\local\token.txt` | nie in WORK/Repo |
| Brücken-Eingang OneDrive | `%OneDrive%\NEXUS\INBOX\` ─► `WORK\_INBOX_ONEDRIVE\` | nur neue Dateien |
| Spiegel WORK ─► OneDrive | `%OneDrive%\NEXUS\WORK-MIRROR\` | neu + geändert, Vorversion in `.nexus_versions` |
| Git-Freigabeordner | `%OneDrive%\NEXUS\EXPORT-APPROVED\` | nur was ID01 hier ablegt, geht nach GitHub |
| GPT-Exporte / Skill-Staging | `%LOCALAPPDATA%\NEXUS\local\gpt-exports\`, `...\skills-staging\` | privat, außerhalb aller Syncs |

Die Cloud-Synchronisierung selbst übernehmen Drive for desktop und der OneDrive-Client. Die Brücken
lesen, kopieren und schreiben nur lokal. Sie löschen nie und überschreiben nie fremde Änderungen.

## Installation (Workstation, normale PowerShell, kein Admin)

```powershell
git clone https://github.com/julianzotter/nexus-platform.git $env:USERPROFILE\nexus-platform   # falls noch nicht vorhanden
cd $env:USERPROFILE\nexus-platform; git fetch origin; git checkout feat/local-stack-id05
powershell -ExecutionPolicy Bypass -File .\local_stack\windows\Install-NexusLocal.ps1
```

Der Installer legt Ordner, Token und die Aufgabe an. Er richtet die Modelle ein (fragt nach dem Ollama-Neustart),
startet den Stack, führt den Abnahmetest aus und öffnet den Control Tower.

Danach Brücken scharf schalten (ID01-Entscheidung): in `nexus-local.json` `"bridge_dry_run": false`,
dann im Control Tower `bridges` → *Neu*.

| Befehl | Zweck |
|---|---|
| `Start-NexusLocal.cmd` | Start über die Aufgabenplanung + Dashboard öffnen |
| `Stop-NexusLocal.cmd` | geordneter Stopp; bleibt gestoppt bis zum nächsten Start |
| `Test-NexusLocal.ps1` | Abnahme T1–T9 (PASS / FAIL / NOT_RUN) |
| `Setup-NexusModels.ps1 [-NoPull]` | Ollama-Umgebung, Varianten, Messung, Standardmodell |
| `Install-NexusLocal.ps1 -Uninstall` | Aufgabe abmelden (nichts wird gelöscht) |

## Lokales Modell (RTX 3080, 10 GB)

| Variante | Basis | Kontext | Rolle |
|---|---|---|---|
| `nexus-q35-9b-16k` | `qwen3.5:9b` (6,6 GB, Tools, Thinking, Vision) | 16K | Standard |
| `nexus-q35-9b-32k` | `qwen3.5:9b` | 32K | wenn Messung 100 % GPU zeigt |
| `nexus-q35-4b-32k` | `qwen3.5:4b` | 32K | schnell / Fallback |

Die KV-Cache-Kosten sind klein (32 KiB/Token f16, nur 8 von 32 Schichten mit voller Attention).
Die 32K-Stufe gilt trotzdem erst als gesetzt, wenn `Setup-NexusModels.ps1` auf dem Rechner 100 % GPU und
mindestens 15 Tokens/s gemessen hat. Das Skript wählt das Standardmodell nach dieser Messung.

DeepSeek Harness: Base URL `http://127.0.0.1:11434/v1`, Model-ID = Standardmodell, neue Session.

## MCP-Anbindung (lokale Clients)

```json
{ "mcpServers": { "nexus-local": { "type": "http", "url": "http://127.0.0.1:8766/mcp",
  "headers": { "Authorization": "Bearer <Inhalt von token.txt>" } } } }
```

Tools v1: `nexus_status`, `work_list`, `work_read`, `work_search`, `repo_read`, `local_llm` (nur lesen, plus lokales Modell).
`web_search` erscheint nur, wenn `search.enabled=true` und ein lokales SearXNG konfiguriert ist.
Cloud-Chats (Perplexity, ChatGPT, Claude.ai) erreichen `127.0.0.1` nicht. Ein Tunnel ist bewusst nicht
eingerichtet und braucht eine eigene ID01-Entscheidung.

## GPTs ─► Skills

Je GPT ein Ordner in `gpt-exports\<name>\` mit `gpt.json` (Schema `nexus-skills-factory/schemas/gpt-capture.schema.json`),
`instructions.md` und optional `knowledge\*`. Der Task erzeugt `skills-staging\<slug>\SKILL.md`, `references\` und
`source-manifest.json` mit dem Status `MIGRATED_UNTESTED`. Aktiviert oder veröffentlicht wird nichts automatisch.
Actions und Auth werden nicht übernommen.

## Nachweiszustände

`LOCAL_WRITTEN_READBACK_OK` (lokal geschrieben + SHA-256 gelesen) ≠ `DRIVE_SYNC_UNVERIFIED` (Cloud-Upload ungeprüft)
≠ `REGISTRATION_PENDING` ≠ Review ≠ ID01-Freigabe. Das Dashboard ist eine Statusprojektion, kein Nachweis.

## Bewusst nicht in v0.1

Echte Bidirektionalität auf demselben Ordner, Schreib-Tools über MCP, Web-Fetch, Tunnel nach außen,
automatisches `git push` von WORK und automatische Skill-Aktivierung. Begründung: Review G01–G06.

## Hardware-Abnahme

Einmalig `local_stack/windows/Test-NexusHardware.ps1` ausfuehren; Ergebnisse in `local_stack/MEASUREMENTS.md`.

## GitHub -> Drive (github_to_work)

Default aus + Probelauf. Liest `origin/<branch>:<prefix>` aus dem vorhandenen Klon (`repo_dir`) nur per
`git fetch` + `ls-tree` + `cat-file` (Arbeitsverzeichnis bleibt unberuehrt) und schreibt create-only nach
`WORK\_INBOX_GITHUB`. Geaenderte Dateien -> `<name>.UPDATE-<blob12>-github_to_work<ext>`. Nachweis je Datei in
`_MANIFEST_GITHUB.json` (commit, blob, sha256). Branch = git_mirror.branch wird blockiert (keine Schleife).
Aktivieren in `%LOCALAPPDATA%\NEXUS\local\nexus-local.json`: `"github_to_work": {"enabled": true, ...}`,
nach Probelauf `"dry_run": false`.
