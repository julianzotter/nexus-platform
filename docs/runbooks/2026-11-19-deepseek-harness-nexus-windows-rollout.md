---
title: "NEXUS DeepSeek Harness – Windows-Live-Rollout und Akzeptanztests"
version: "1.0.0"
status: "STAGED_WINDOWS_RUNTIME_BLOCKED"
date: "2026-11-19"
role_id: "ID02"
executor: "OpenAI Codex /root"
id01_authorization: "2026-11-19 Chat – Implementierung beauftragt"
registration_status: "REGISTRATION_PENDING"
---

# DeepSeek Harness × NEXUS-AI: Windows-Ausführung (ID01-Auftrag)

## Ist-Stand und harte Grenze

- [VERIFIED] Dokumenten-PR #101 wurde gemergt: https://github.com/julianzotter/nexus-platform/pull/101.
- [VERIFIED] NEXUS-Governance: `_AGBS.md` v007.1, Manifest, Baseline und `WORK/Folder.md` gelesen; WORK ist die Dokumenten-SSOT. Das Register `file-registry.jsonl` enthält aktuell **keine** Einträge für Drive-IDs `190jsx6hnyc6r6CdevquJMzPheSbndxas` und `1HpducdBEOf9RGPZkkVw8p70sds_HQ8td` (Abruf 19.11.2026).
- [VERIFIED] Diese ausführende Cloud-Umgebung ist Linux. `dsh`, `ollama` und `pwsh` sind hier nicht vorhanden. Ein Windows-Host wird über keinen aktuellen Ausführungskanal erreicht.
- [NOT_RUN] Die tatsächlichen lokalen Profilpfade, DSH-Desktop-Version, lokale Modelle, Plugin-Versionen, MCP-Verbindungen und API-Credentials dürfen deshalb **nicht** als funktionierend bezeichnet werden.
- [GATE] Die ID01-Freigabe ist Auftrag zur Umsetzung, aber keine Behauptung eines erfolgreichen Windows-Laufes. Keine fremde Konfiguration blind überschreiben; Änderungen nur nach Vorher-Hash, Sicherung und isoliertem Test.

## RUN 01: lokale Windows-Inventur – sicher, lesend

Im tatsächlichen Windows-Checkout von `julianzotter/nexus-platform` mit Python 3:

```powershell
Set-Location (git rev-parse --show-toplevel)
$work = 'G:\Meine Ablage\_developement\LLM-LOCAL-SSOT\WORK'
py -3 .\tools\windows\nexus_dsh_preflight.py --repo . --work $work --check-github
```

Optionaler Test des historischen AnythingSearch-Pfades nur bei tatsächlich vorhandener Datei:

```powershell
py -3 .\tools\windows\nexus_dsh_preflight.py --repo . --work $work --sqlite 'G:\Meine Ablage\_INDEX_LNK\00-AnythingSearch\AnythingSearch.db' --check-github
```

Das Skript nimmt **keine** DSH-, MCP-, GitHub- oder Datenbankänderungen vor. Es liest: Windows-Host, `dsh`-CLI im `PATH`, `DSH_HOME`/`.dsh`-Profile und Datei-Hashes, Repo-/WORK-Pfad, lokales Ollama `/api/tags`, optional `gh api` und SQLite `mode=ro` + `PRAGMA query_only=ON`. Es gibt **keine** Credential-Inhalte aus. Ein fehlgeschlagener Host-/Zugriffstest ergibt Exit-Code 2. Die Datei `mcp.local.example.json` ist ein MCP-Client-Beispiel und **keine** automatisch gültige DSH-Konfigurationsdatei.

## RUN 02: echter Windows-Lauf, getrennte Gates

| Gate | Test/Execution | PASS nur bei | Negative Case / STOP |
|---|---|---|---|
| W01 Konfiguration | DSH-App und CLI-Version bestimmen; effektiven Desktop-Host/-Profil-Namen feststellen; vor Änderung exakte Patchdatei kopieren, SHA-256 | Exakte Version, Profil, Originalhash, gesicherte Kopie | Fehlendes Profil, unbekannter tatsächlicher Host |
| W02 Provider | `deepseek-official` + `deepseek-flash` mit synthetischer Anfrage, begrenzten Tokens/Timeout; `deepseek-v4-pro` in separater Session | Authentifizierte Antwort, tatsächliche Modell-ID, HTTP-/Usage-Status | 401/403/429/Timeout, Modell-Fehlzuordnung; nicht blind retryen |
| W03 Thinking | Chat-API separat mit `reasoning_effort=none` und `high` bzw. `thinking.type` testen | Antwort + Usage; unterschiedliche Modi dokumentiert | Nicht durch `reasoningEfforts:false` ersetzen |
| W04 Cache/Kosten | Identisches langes statisches Präfix zweimal, variable Frage hinten; Usage vergleichen | `prompt_cache_hit_tokens` nachvollziehbar, Kosten mit aktueller Preistabelle | Cache-Hit nicht behaupten, falls Zähler 0/fehlend |
| W05 Ollama | `/api/tags`, tatsächliche Modell-ID; optional `--ollama-model` für synthetischen `/api/generate`-Test | Lokale Antwort, keine unautorisierte Verbindung nach außen | Kein Modell oder Server, Generation Timeout |
| W06 DSH-MCP | **Offiziellen MCP Manager** in Settings bestätigen; `nexus-bridge` erst mit `NEXUS_MCP_WRITE=0` anbinden | `connected`, Toolauflistung, `status`-Tool lesbar | Schreibtool akzeptiert Mutation trotz Read-Only; STOP |
| W07 GitHub-MCP | Remote `https://api.githubcopilot.com/mcp/`; OAuth/Token nur im DSH Credential Store; `X-MCP-Readonly: true`; nur `repos,issues,pull_requests` | Authentifiziert, Tools geladen, privates Repo lesbar, Mutations-Tool nicht verfügbar | 401/403, ungeprüfte Scopes, Schreiben möglich; STOP |
| W08 SQLite | Auf tatsächlicher Datei `mode=ro` + `query_only=ON`; `SELECT ... sqlite_master` und DSH-Toolabfrage | Read funktioniert; separate kontrollierte Mutationsprobe wird abgewiesen | Nur eine UI-Checkbox als Read-Only-Beweis unzureichend |
| W09 Datenschutz | DSH-Cloud-Request, OTel und separaten `session-log-deepseek`-Upload per Netzwerk-/Prozessdiagnostik unterscheiden | Datenfluss dokumentiert; kein Zero-Egress-Claim bei Cloud-Session | `DSH_TELEMETRY_DISABLED=1` allein ist kein Session-Log-Nachweis |
| W10 Plugin-QA | Installierte Namen/Versionen, Publisher, Quelle, Berechtigungen, Hash und Abhängigkeiten aufnehmen | Versionsgebundener Review + Aktivierungsmessung | Community-Plugins `dsh-local-model`, `dsh-workspace-mcp`, `dsh-budget-watcher`, `dsh-no-phone-home` nicht ungeprüft installieren |
| W11 Rollback | DSH mit dokumentierter Sicherung wiederherstellen, neu starten, erneut inventarisieren | Originalhash und Funktion wiederhergestellt | Backup fehlt/hat andere Bytes |
| W12 End-to-End | Synthetischer NEXUS-Arbeitsauftrag: DSH→MCP lokaler Status→LLM→Review→Report ohne Egress privater Daten | Reproduzierbare Receipts und explizite ID01-Freigabe des Ergebnisses | Kein automatisches HUMAN_GATE bei grünem Teiltest |

## MCP-Konfiguration – sichere Zielarchitektur

1. In DeepSeek Harness das **vorhandene** `@deepseek-ai/dsh-mcp-manager`-Panel in Settings nutzen. Ein Profil-Patch ersetzt ggf. die komplette Server-Map; deshalb keine ungetestete Patchdatei einsetzen.
2. GitHub: offizieller Remote-Endpunkt **`https://api.githubcopilot.com/mcp/`**, Transport `streamable-http`. HTTP-Header `X-MCP-Readonly: true` und `X-MCP-Toolsets: repos,issues,pull_requests`; Credentials als `${credential:GITHUB_MCP_TOKEN}` nur über DSH-Credential-Provider, sofern dieser Mechanismus im konkreten Desktop-Profil bestätigt ist. Keine PATs in YAML, Drive oder GitHub.
3. Lokal: Existierende `mcp_bridge/nexus_mcp_server.py` per venv/`stdio` anbinden; **`NEXUS_MCP_WRITE=0` belassen**. `mcp_bridge/install_mcp_bridge.ps1` ohne `-ClaudeDesktop` bereitet die Bridge vor, installiert aber nicht automatisch den DSH-MCP-Eintrag. Absolute echte Windows-Pfade erst nach W01 einsetzen.
4. OLLAMA: Local-Model-Integration nur nach Bestätigung von Modell, Plugin-Version und DSH-Kompatibilität; ein Cloud-Orchestrator verursacht weiterhin Cloud-Egress.
5. GitHub-Remote **nicht** mit `https://api.github.com/mcp` verwechseln. `dsh-workspace-mcp`/Community-Plugins vorerst nicht als Standardvoraussetzung behandeln.

## RUN 03: Ticket, Ledger und Registrierung – separater, autorisierter Schreiber

1. `file-registry.jsonl` im SSOT erneut vollständig lesen; Drive-IDs der zwei Handbuchartefakte sowie dieses neuen Reports gegen Duplikate/Revisionen prüfen. Heute fehlen die beiden Handbuch-IDs (Quelle: Register `15m8T5cWbogIup9snzFwiB1g9HqNCoGow`).
2. Ticket-/Work-Order referenzieren. AGB v007.1 §6 benennt **genau einen** Ledger-Schreiber: „Claude (Peer-Reviewer, delegiert durch ID01)“. Keine konkurrierende Registeränderung durch ID02. Historische widersprüchliche Rollenangaben bleiben Prüfpunkt.
3. Vor dem Schreiben `py tools/configure_drive_oauth.py --check --require-write` und eine aktuelle CAS-Probe ausführen. **Wichtig:** Der bestehende Workflow `NEXUS Control Register Repair` (`nexus-register-repair.yml`) ist auf eingefrorene alte Reparaturziele/Hashes ausgelegt und **kann nicht unverändert neue Handbuchartefakte registrieren**. `NEXUS Registry Append` ist ein eingeschränkter Legacy-Einstieg. ID06 muss einen neuen, auf die aktuellen Drive-IDs zugeschnittenen append-only-Plan mit denselben CAS-/Rollback-Gates entwerfen, prüfen und dann vom einen autorisierten Schreiber ausführen lassen.
4. Der delegierte Schreiber erstellt aus **frischen Originalbytes** den neuen Delta-/Append-Plan für die Drive-IDs (keine Nummern raten), testet einen Konflikt, führt danach genau einen kontrollierten Append durch. Akzeptanz: gleiche Drive-IDs, alter Byte-Präfix unverändert, neuer SHA-256 nach Readback, `REGISTERED_VERIFIED` und Ticket-Verweis. Bei `HTTP_400`, fehlenden ETags oder `CAS_CONFLICT`: **BLOCKED**, keine unbedingte Ersetzung.
5. Notwendige getrennte Runs: OAuth/WORK-Preflight → CAS-Probe → neuer Registry-Plan-Dryrun → autorisierter Registry-Append mit Byte-Readback → aktueller GitHub→WORK-Delivery-Readback → WORK→GitHub-Poll-Readback. Die bestehenden Workflow-Bezeichnungen sind keine Bestätigung ihrer Eignung für diesen neuen Plan. Jeder Run braucht URL, Commit, SHA, ACK und Ergebnis; ein grüner alter Run zählt nicht.

## Nachweise, die ID01 zur lokalen Freigabe erhält

- Sanitisierter RUN-01-JSON-Report, Hash der Original-DSH-Konfiguration, Backup-/Rollback-Hash.
- RUN-02-Gate-Matrix mit DSH-Version, Modell-IDs, MCP-Tools, tatsächlich erreichten Providern und Privatsphäre-Befund.
- RUN-03-Work-Order/Registry-Receipt mit echten IDs, Run-URLs, SHA-256; keine Credentials und keine privaten Promptinhalte.
- Wenn alle relevanten Tests und getrennten Reviews PASS sind: **separate endgültige ID01-Produktionsabnahme** des geprüften Konfigurationsstands.

## Primärquellen (abgerufen 2026-11-19)

- [DeepSeek Harness MCP Manager](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/mcp/mcp-manager/README.md)
- [DeepSeek Chat Completions](https://api-docs.deepseek.com/api/create-chat-completion/)
- [DeepSeek Thinking](https://api-docs.deepseek.com/guides/thinking_mode/)
- [GitHub MCP Server: Einrichtung](https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/customize-copilot/extend-copilot-with-tools-and-context/set-up-the-github-mcp-server)
- [GitHub MCP Server: Read-only/Toolsets](https://github.com/github/github-mcp-server/blob/main/docs/server-configuration.md)
- [NEXUS Registry-Reparaturverfahren](https://github.com/julianzotter/nexus-platform/blob/main/docs/NEXUS-CONTROL-REGISTER-REPAIR.md)
- [AGB v007.1](https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view), [WORK Folder](https://drive.google.com/file/d/1nDjF78dq3l8PGpXsauzBz1bzHescDSwv/view)
