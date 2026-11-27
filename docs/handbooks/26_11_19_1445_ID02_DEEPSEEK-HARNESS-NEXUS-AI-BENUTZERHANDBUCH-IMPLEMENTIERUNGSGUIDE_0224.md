---
title: "DeepSeek Harness × NEXUS-AI – Praxis-Handbuch und Windows-Implementierungsguide"
version: "1.0.0"
status: "REVIEW_PENDING"
created_at: "2026-11-19T14:45:00+01:00"
timezone: "Europe/Vienna"
owner: "Julian Zotter (ID01)"
role_id: "ID02"
executor: "OpenAI Codex /root"
provider: "OpenAI"
model_id: null
ticket_id: null
ledger_id: null
registration_status: "REGISTRATION_PENDING"
verification_status: "DOC_SOURCES_CHECKED; WINDOWS_LIVE_TESTS_PENDING"
canonical_folder: "gdrive:1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP"
github_role: "review_snapshot_only"
supersedes: null
---

# DeepSeek Harness × NEXUS-AI
## Personalisiertes Benutzerhandbuch und Windows-Implementierungsguide

**Stand:** 19.11.2026 · **Zielsystem:** Julian Zotter, Windows-Workstation, NEXUS-AI-AEC-Engineering-Knowledge-System · **Status:** ENTWURF / REVIEW_PENDING, keine produktive Freigabe.

## 0. Lesehilfe und verbindliche Grundentscheidung

- **Ziel:** DeepSeek Harness (DSH) als kontrollierbare Agent-Runtime für quellengebundene Engineering-Aufgaben, lokales Filesystem, AnythingSearch/SQLite und deterministische Python-/RFEM-/CAD-Tools.
- **Nicht-Ziel:** autonomer statischer Nachweis, Freigabe einer fremden Datei, Cloud-Übertragung vertraulicher Inhalte ohne Human Gate, automatisch bestätigte Drive↔GitHub-Synchronisation.
- **Autorität:** ID01 Julian Zotter entscheidet. ID02 orchestriert. ID07 DeepSeek ist gemäß aktuellem Manifest unabhängiger Prüfakteur, ID08 Ollama lokaler Modellbetrieb; diese Rollen belegen keine ausgeführte Runtime. Rechnungen ausschließlich deterministisch prüfen.
- **Quelle:** Kanonisches [Manifest-MD](https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view), [Baseline-MD](https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view), operative [_AGBS.md v007.1](https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view) und [Folder.md](https://drive.google.com/file/d/1nDjF78dq3l8PGpXsauzBz1bzHescDSwv/view).

### 0.1 Aktueller belegter Bestand

| Teil | Gelesene Quelle / Status | Konsequenz |
|---|---|---|
| Windows DSH v0.2.0-rc.2 | Benutzerauszug im [Chat-Export](https://drive.google.com/file/d/157nBKsS9ksXnlsoBFtBxwDKVwPsgjwI_/view), `USER_REPORTED` | Aktive Installation und effektives Profil am Windows-PC verifizieren. |
| Cloudprovider `deepseek-official`, Flash/Pro | Benutzerauszug, `USER_REPORTED`; Cloud-Endpunkt offiziell belegt | Kein lokal laufendes DeepSeek V4 aus der Providerliste ableiten. |
| Basis-Plugins `tool-fs`, `tool-fs-search`, `tool-pwsh`, `agent-instructions`, `skill-filesystem`, `tool-workflow`, `compaction-basic` | Benutzerauszug, `USER_REPORTED` | Toolrechte im aktiven Agent-Preset einzeln überprüfen. |
| Ollama / RTX 4080 / Qwen | bisherige persönliche Projektangaben, `HISTORY_REPORTED` | Verfügbare Modelle/GPU/Endpunkt derzeit **nicht live verifiziert**. |
| AnythingSearch SQLite | Windows-Wunschpfad `G:\Meine Ablage\_INDEX_LNK\00-AnythingSearch\AnythingSearch.db`, `HISTORY_REPORTED` | Kein DB-Schreibzugriff vor Dateiexistenz, Lock-/WAL- und Schema-Check. |
| GitHub | [julianzotter/nexus-platform](https://github.com/julianzotter/nexus-platform), Repository direkt lesbar | Source-/Review-Snapshot; kein Beleg für laufenden Sync. |
| Governance/Sync | [WORK](https://drive.google.com/drive/folders/1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP), [Issue #73](https://github.com/julianzotter/nexus-platform/issues/73), [CPLM-Audit](https://drive.google.com/file/d/1lQ02o39bJUn322FQl_GYYb8FCdFQEyUV/view) | Monitor/Poller/Delivery weiter FAIL, keine globale Produktionsfreigabe. |

## 1. Benutzerhandbuch: Was DSH für NEXUS leisten soll

Der Harness verbindet Modellaufrufe mit Werkzeugen. Die tatsächliche Daten-/Sicherheitsarchitektur ist **nicht** durch das Modelllabel definiert, sondern durch den konkret geprüften Pfad von Eingaben, Prompt, Agent-Preset, Tool, Connector, Netzwerk, Log und Ausgabe.

| Ebene | Verantwortung | Autorität / Gate |
|---|---|---|
| NEXUS Governance | Manifest, AGBs, Workorder, Quellen- und Rollenregister | ID01-Entscheidung; WORK Original-SSOT |
| DSH Runtime | Modellauswahl, Tools, Permissions, Sessions, Caching, Profile | Nur tatsächlich gemountete Profile und Rechte |
| Cloud LLM | Analyse, Klassifikation, Planung, textueller Review | Keine Rechen-/Freigabeautorität; Egress-Prüfung |
| Ollama lokal | Vertrauliche Extraktion/Review und offline verwendbare Modellroute | Local-only erst nach Netzwerk-/Telemetry-Test |
| Datenintegration | AnythingSearch, SQLite/FTS5, Drive, GitHub, MCP | Query read-only, provenance und Versionsbindung |
| Rechenebene | Python/SymPy, EC-Solver, RFEM5 COM, RFEM6 API II, ezdxf, IfcOpenShell | Deterministische Tests, Einheiten, Dokumentation, Human Gate |

**Modell kann Toolaufruf vorschlagen; Tool-Layer validiert Schema, Berechtigung und Ziel.** Dokumenttexte und Suchtreffer gelten als untrusted input, niemals als neue Betriebsanweisung.

## 2. Windows-Preflight: den tatsächlich aktiven Zustand feststellen

**Vor jedem Patch:** App-Version, Profil, absolute Konfigurationsdatei, letzter erfolgreicher Test, tatsächlich angezeigte Modelle, aktive Pluginliste und Dateirechte protokollieren. Keine Secrets ausgeben und keine `.credentials.yaml`/`.env` in Chat oder WORK kopieren.

### 2.1 Lokal am Windows-Rechner, read-only

```powershell
# Windows PowerShell: Verzeichnisse und registrierte Profile nur auflisten
Get-ChildItem -LiteralPath (Join-Path $env:USERPROFILE '.dsh\profiles') -Directory |
  Select-Object FullName, Name

# DSH-CLI nur prüfen, falls der Befehl verfügbar ist
Get-Command dsh -ErrorAction SilentlyContinue | Select-Object Source
dsh --version

# Ollama: laufende lokale Modelle und Tags; kein Pull, kein Install
Get-Command ollama -ErrorAction SilentlyContinue | Select-Object Source
ollama list
Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/tags' -Method Get |
  Select-Object -ExpandProperty models | Select-Object name, size

# Vorhandener lokaler AnythingSearch-Index (nicht öffnen/schreiben)
Test-Path -LiteralPath 'G:\Meine Ablage\_INDEX_LNK\00-AnythingSearch\AnythingSearch.db'
```

**Zu beachten:** `dsh --profile web --dump-config` ist eine dokumentierte CLI-Inspektionsfunktion; sie prüft `web`. Die Desktop-App verwaltet das Profil `desktop` selbst; der CLI-Launcher weist den direkten Start dieses Profils zurück. Den Desktop-Zustand über **Settings → Open configuration file** und die Desktop-Pluginansicht feststellen, ohne vertrauliche Konfigurationswerte zu veröffentlichen. `--dump-config` kann Konfiguration einschließlich Secret-Referenzen enthalten: nur kontrolliert lokal prüfen. [CLI-Code](https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/src/args.ts).

### 2.2 Konfigurationshierarchie richtig verstehen

1. Profil-Bundles (`dsh.profile.bundles`), danach Profil-Patch `$DSH_HOME/profiles/<profile>/cordis.patch.yml`.
2. Danach Home-Patch `$DSH_HOME/cordis.patch.yml` und ggf. zusätzliche `--patch`-Overlays; spätere Schichten überschreiben die komplette betroffene Config-Row.
3. Die in älteren Chats wiederholte `~/.dsh/settings.yaml` ist **kein verlässlicher zentraler Änderungsort** für v0.2.x. Keine Altdatei migrieren oder umbenennen ohne Versions-/Backup-Test.

Primärquellen: [Profil/CLI](https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/reference/README.md) und [Model Provider Guide](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/providers.md).

### 2.3 Privacy-Gate unbedingt vor Cloud- oder lokalem Pilot

Der offizielle DSH-Basissatz kann **zwei verschiedene Datenabgaben** durchführen:

- `session-log-deepseek`: standardmäßig `enabled: true`; hängt einen Session-Log-Suffix an offizielle DeepSeek-Requests an (maximal 8 MiB je Request). **Settings → General → Upload Session Log when using the official model API: OFF** und anschließend effektive Einstellung am aktiven Profil nachprüfen. Reaktivieren kann ältere ausstehende Logteile übertragen.
- OpenTelemetry (`session-telemetry-otel`): Default `FEEDBACK_ONLY`; Feedback-Aktionen können Protokollpräfixe übertragen. `DSH_TELEMETRY_MODE=DISABLED` oder eine nichtleere `DSH_TELEMETRY_DISABLED`-Variable deaktiviert laut offizieller CLI-Referenz **nur diesen OTel-Kanal**, nicht `session-log-deepseek`.

**Falsch wäre:** `DSH_TELEMETRY_DISABLED=1` allein als Zero-Egress-Zertifikat. Drittplugin `dsh-no-phone-home` ist kein Ersatz für den beobachtbaren zweigleisigen Test. Primärquellen: [CLI Referenz](https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/reference/README.md), [Session-Log Plugin](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/session/session-log-deepseek/README.md).

**Test:** Mit nicht vertraulichen Testdaten, lokalem Modell und ausschließlich lokalen Tools Netzwerk-/DNS-/Proxy-Verbindungen und App-Telemetrie beobachten. Kein Zero-Egress-PASS allein aufgrund eines GUI-Schalters.

## 3. Modelle, Thinking, Kosten und Prompt-Cache

### 3.1 Routing-Regel (Designvorschlag, noch nicht erzwungen)

| Aufgabenklasse | Vorgeschlagene Route | Datenfreigabe |
|---|---|---|
| Triage, Dateiklassifikation, Kurztexte, öffentliches Bibliografieren | `deepseek-flash` (Thinking bei Bedarf reduzieren) | Cloud nur für freigegebene Daten |
| Komplexe Architektur- und Codekritik, adversarial Review | `deepseek-v4-pro` | Cloud nur für freigegebene Daten; Output keine fachliche Abnahme |
| Vertrauliche Unterlagen, geschützte Normtexte, interne Statikmodelle | Ollama lokal mit Modell-/Tool-Review | Local-only-Pipeline; Cloud-Fallback ausdrücklich **verboten**, sofern nicht freigegeben |
| Rechenergebnis, Bemessung, Geometrie, GWP-Kennwerte | Versionierter deterministischer Solver (Python/RFEM/Excel) | LLM lediglich Eingabe-/Protokollhilfe; ID01 prüft |

**Settings → Models:** Auswahl ändert Default für neue Sessions; bereits verwendete Session führt den protokollierten Modellstand weiter. Neue Session für Modellvergleich und Kosten-A/B-Test. [Offizielle Provider-Anleitung](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/providers.md).

### 3.2 Thinking und Endpoint-Semantik

DeepSeek dokumentiert je API-Fläche unterschiedliche Felder:

| Endpoint | Schalten / Effort laut offizieller DeepSeek-Doku |
|---|---|
| OpenAI Chat Completions | `thinking: {type: enabled/disabled}`; `reasoning_effort` für gewünschte Tiefe laut API-Anleitung |
| Anthropic-kompatibel | `reasoning: {effort: none/low/high/max}`, `none` deaktiviert |
| Responses | separates `output_config`/Reasoning-Schema laut jeweils aktuell gültiger API-Doku |

Eingabe in DSH-GUI bevorzugen; **kein** ungeprüftes `reasoningEfforts: false` in eine unbekannte `llm-deepseek`-Row schreiben. Für Effort-A/B-Test zwei frische Sessions mit gleichem synthetischem Prompt, Modellversion, Endpoint, Tokenlimits und Toolset vergleichen. [Thinking Mode](https://api-docs.deepseek.com/guides/thinking_mode/).

### 3.3 Caching ohne ungeprüftes Einfügen ganzer Normwerke

Stabiler und freigegebener Systemkontext → freigegebene unveränderliche Quellenzitate/Schema → neue Aufgabe/Toolergebnisse. Achtung: Normvolltexte oder vertrauliche Projektdaten nur übertragen, wenn Rechte und Zweck dies zulassen. Cache basiert auf identischen Tokenpräfixen, ist best-effort und nicht für dynamische Referenzinhalte garantiert.

`cache_hit_ratio = prompt_cache_hit_tokens / (prompt_cache_hit_tokens + prompt_cache_miss_tokens)`; Anteil nur rechnen, wenn Summennenner > 0. Vergleichsmessung: gleicher freigegebener Präfix, zwei bis drei kurz hintereinander folgende harmlose Requests, Nutzungsdaten aufzeichnen; eine einmalige Anfrage darf 0 Hits zeigen. [Offizielle Cache-Regeln](https://api-docs.deepseek.com/guides/kv_cache/).

### 3.4 Preis-/Budgetstrategie (abgerufen 19.11.2026)

Offizielle Off-Peak-Tarife je 1 Mio. Token: Flash Input Cache-Miss **0,15 USD**, Cache-Hit **0,003 USD**, Output **0,60 USD**; Pro **0,66 / 0,022 / 1,98 USD**. Peak abweichend, siehe [DeepSeek-Preise](https://api-docs.deepseek.com/quick_start/pricing/). **Wichtige Änderung seit 18.11.2026 (12:00 Beijing Time):** Vom Modell ausgelöste serverseitige Websuche und Web-Fetch werden nicht mehr zusätzlich pro Request abgerechnet; eingefügte Resultattokens bleiben Modellinputkosten. Die eigenständigen Search- und Fetch-APIs haben weiterhin dokumentierte separate Tarife. Historische Kosteninterpretationen des Chat-Exports entsprechend aktualisieren.

Kostenformel (USD) getrennt nach Modell, Tageszeit und Tokenart:

`cost = N_miss/1e6*p_miss + N_hit/1e6*p_hit + N_output/1e6*p_output + separate_api_fees`.

Bei wiederholbaren Tests `model_id`, Endpoint, Thinking, Cache-Hit/Miss, Outputtokens, Zeit und Gebührenquelle protokollieren; Reasoning-Tokens nicht zusätzlich zu Outputtokens doppelt bepreisen. `dsh-budget-watcher` ist Community-Software, Warn-/Blockierwirkung **erst nach realem Budget-Cap-Test** als durchgesetzt betrachten. Offizielles Portal: [Usage](https://platform.deepseek.com/usage).

## 4. Plugins, MCP und Sicherheitsgrenzen

### 4.1 Priorisierte Auswahl

| Komponente | Entscheidung | Reifegrad am 19.11.2026 |
|---|---|---|
| Bestehende DSH Built-ins `tool-fs`, `tool-fs-search`, `tool-pwsh`, Skills, Workflow | Beibehalten, Berechtigungen lesen und Read-Tests durchführen | `USER_REPORTED` |
| Offizieller `@deepseek-ai/dsh-mcp-manager` | **Erste Wahl** für zunächst lesende MCP-Endpunkte | Offizielle Dokumentation, Desktop/Web bereits als Manager-Row vorgesehen |
| `dsh-local-model` (songzhiyin) | Kandidat für lokalen Ollama-Adapter | Existiert; Version/Supply-Chain/API-Calls lokal prüfen |
| `dsh-workspace-mcp` | Nur bei nachgewiesen notwendigem Per-Workspace-Isolationseffekt | Community; Runtime-Version/Dateischema nicht abgenommen |
| `dsh-connectors`, `dsh-set-model`, `dsh-budget-watcher` | Optional nach Sicherheits-/Kompatibilitätsreview | Community; nicht blind installieren |
| `mcp-server-sqlite` aus alten MCP-Beispielen | **Nicht ungeprüft als Produktionsserver verwenden** | Historische Referenzarchivierung; `SQLITE_READONLY` allein keine Sicherheitsgrenze |
| `dsh-no-phone-home` | Nicht als alleiniger Egress-Schutz | Community; erster Schritt ist offizielle Opt-out-/Netzwerkprüfung |

**Wichtig:** DSH-Plugins sind ausführbarer Code. Ein Drittplugin kann potentiell Hostdateien, Prompts und Credentials berühren. Vor Installation Maintainer, Release/Commit, Lizenz, Dependencies/Install-Scripts, DSH `engines`-Bereich und Quellcode prüfen, dann zuerst isoliert testen.

### 4.2 Offizieller MCP-Manager statt unsicherer Beispielkonfiguration

Der offizielle Manager bietet konfigurierbare `servers`, `probe`, `restart`, `status`, `enabled:false` und Credential-Referenzen wie `${credential:REF}`. Er wird laut Hersteller im Web-/Desktop-Profil montiert. Die tatsächlich erforderliche JSON/YAML-Struktur nach aktiver Installation aus dem spezifischen Manager-Config-Schema und der Hostoberfläche übernehmen. **Kein** universelles `.dsh/mcp.json` und keine frei erfundene GitHub-URL `https://api.github.com/mcp` annehmen. Primärquelle: [MCP Manager](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/mcp/mcp-manager/README.md).

**MCP Testvertrag:**

1. Server **disabled**, lokale Programmpfade/Serveridentität verifizieren.
2. Harmloses `probe`: Serveridentität, Transport, Tools/Schemas auslesen, keine Schreibtools freigeben.
3. Gezielt enable (READ-ONLY Agent-Preset/Server/Account), `mcp__<server>__<tool>`-Namen nachweisen.
4. Eine definierte synthetische Lesefrage ausführen, Resultat prüfen; absichtlich unzulässige Write-Aktion muss kontrolliert abgewiesen werden.
5. Log: Konfig-Hash, Server-Version, Dateiquelle, Startzeit, Request-ID/Status, Ergebnis ohne Credentials.

### 4.3 SQLite: Schreibschutz wirklich technisch erzwingen

- Der bestehende AnythingSearch-Index dient **zuerst nur als Metadaten-Router** (Name, Pfad, Dateityp, Zeitstempel). Ein Treffer ist kein Originalinhalt und kein aktueller Dateibeleg.
- Nicht direkt eine aktive DB auf Google Drive synchronisieren; bei Bedarf konsistenten Snapshot/SQLite-Backup der lokal schreibenden Instanz erstellen.
- Connection-URI `file:...?...mode=ro` / Dateiberechtigung read-only / Servertool-Allowlist; „read-only“ als Umgebungsvariable ist ohne Quellcode-Nachweis kein Gate.
- Schema prüfen (`sqlite_master`, `PRAGMA table_info`), `PRAGMA quick_check` auf ruhendem Snapshot, repräsentative Queries reproduzierbar testen. Quellen: [SQLite URI](https://www.sqlite.org/uri.html), [SQLite PRAGMA](https://www.sqlite.org/pragma.html).
- Wenn mit SQLite-MCP: kein generischer SQL-Write-Endpunkt für das Modell, sondern eng begrenzte und parameterisierte Query-Tools mit Tabellen-/Limit-Allowlist.

### 4.4 GitHub und Google Drive

- **Drive:** WORK-Original und Canonical File-ID; Drive Desktop-Mount unter Windows kein Beweis für Offline-Pinning. Datei per Provider-ID und gegebenenfalls lokaler Freigabe lesen. OAuth-Zugriff/Refresh ausschließlich in kontrollierter Credentials-Umgebung.
- **GitHub:** Revisionierter Code/Review-Snapshot; PR, Code-Checks und Branchschutz. Kein inhaltlicher Ersatz für WORK-Original und keine Behauptung eines automatischen Zweiwege-Sync.
- **Stand:** Monitor, Poller und Delivery laut [Issue #73](https://github.com/julianzotter/nexus-platform/issues/73) / [CPLM v0.2.139](https://drive.google.com/file/d/1lQ02o39bJUn322FQl_GYYb8FCdFQEyUV/view) noch fehlerhaft. Der bestehende Windows-OAuth-Reparaturpfad `tools/configure_drive_oauth.py --check` ist zuerst **lesend** zu prüfen; Secret-Publish und Reautorisierung nur ID01 nach Risiko-/Scope-Entscheid.

## 5. NEXUS Engineering Usecases: die drei MVP-Workflows

### UC-01 Quelleninventar, Normen-Retrieval und Engineering Knowledge

1. NEXUS File Router → bestehender AnythingSearch-Index (read-only): Suchbegriff `EC5`, `19103`, `HBV`, `RFEM` plus Dateityp.
2. Treffersatz mit Originalpfad/Drive-ID, Quelle, Revision und Hash; nur relevante Originaldokumente lesen, keine großflächige Normtextkopie ins Cloud-LLM.
3. Python/SQLite FTS5/BM25 → zulässige Quellenkandidaten mit exakten Fundstellen; optional spätere Vektorsuche, nicht als Freigabekriterium.
4. DeepSeek/Ollama extrahiert **Behauptungen mit Beleganker**, Schema validiert Status `VERIFIED/DERIVED/UNVERIFIED`.
5. Fachlicher Reviewer und ID01 prüfen normative Fassung, österreichischen Nationalen Anhang und Anwendungsbereich.

**Abnahme:** 10 festgelegte Query-Testfälle; Original-URI und Fundstelle je fachlichem Claim vorhanden; fehlende Quelle führt zu `UNVERIFIED`; unveränderte Testdaten erzeugen identische Retrieval-Metadaten.

### UC-02 RFEM/CAD/EC2-EC5-HBV-Fachworkflow

1. Workorder beschreibt Geometrie, Einheiten SI, Auflager, Lastfälle, Kombination, Material, Normausgabe, Anhang, verifizierte Eingaben und Referenzmodell.
2. DSH strukturiert nur Eingabe und Testplan; keine selbstständige FE-Bemessung. Versionierter Python-Adapter und freigegebene RFEM-API/COM-Schicht sind Rechenautorität.
3. Ein **isoliertes neues Testmodell** erzeugen; weder vorhandene `.rf5/.rf6` überschreiben noch ungeprüfte Ergebnisse als Bemessung verwenden.
4. deterministische Plausibilität: Modellhash, Parametergleichheit, Solverversion, Gleichgewicht, Grenzwerte, Einheiten, Gegenrechnung.
5. ID07 / unabhängiger Reviewer falsifiziert; ID01 Freigabe; Engineering-Ausgabe nur nach Gate.

**Referenz:** [NEXUS PR #84](https://github.com/julianzotter/nexus-platform/pull/84) ist Draft, Offline-Tests belegt/gemeldet, aber Windows-DSH-Auth/RFEM-Live-Betrieb nicht abgenommen. [RFEM/CAD Review-Workorder](https://drive.google.com/file/d/17Z8J1FMpTqSeZXJnkqK_y4OutIPd25dT/view).

### UC-03 Drive→GitHub Review-Snapshot mit Delivery-Receipt

1. Drive-Datei-ID, MIME, Version, Raw-Bytes und SHA-256 erfassen.
2. GitHub-Dokument auf **separatem Draft-Branch** ablegen, keinen Main-Merge ohne ID01.
3. Gegenlesen aus dem GitHub-Branch: UTF-8-Inhalt bytegleich zum Drive-Original; SHA-256 beider normalisierten Rohdateien vergleichen.
4. Status `FILE_VERIFIED / REGISTRATION_PENDING` bis Ledger-Eintrag durch autorisierten Single Writer; separates ACK/Peer-Review erforderlich.
5. Erst mehrere erfolgreiche **echte** GitHub Actions-Läufe mit Run-ID, Checkpoint, Delivery- und Readback-Evidenz erlauben Aussage „Sync produktiv“.

## 6. Schritt-für-Schritt-Umsetzung (Windows, risikoarm)

| Schritt | Aktion | Abnahmekriterium | Status bei Erstellung |
|---|---|---|---|
| P0 | Manifest, Baseline, `_AGBS`, Folder, offenes Ticket lesen | exakte Quell-ID/Version im Run-Receipt | `PASS_READ` |
| P1 | Desktop/CLI-Version, effektives DSH-Profil und Pluginliste prüfen | Windows-Output/Screenshot und Profilpfad | `PENDING_WINDOWS` |
| P2 | Session-Log und OTel separat abstellen und Netzverhalten prüfen | zwei Kontrollkanäle + beobachtbarer Egress-Test | `PENDING_WINDOWS` |
| P3 | `ollama list`/`api/tags`; Modell/Tool-Call A/B offline testen | exakter Modelltag, lokaler Endpunkt, erwartete Ausgabe | `PENDING_WINDOWS` |
| P4 | DSH-Cloud-Flash/Pro mit **synthetischen** Daten getrennt testen | HTTP/Modell/Usage, Timeout, Schema, Kosten | `PENDING_CREDENTIAL_SCOPE` |
| P5 | Offiziellen MCP-Manager/Server read-only anbinden | `probe`, ein Read, abgewiesene Write-Aktion | `PENDING_SERVER_REVIEW` |
| P6 | AnythingSearch-Snapshot + FTS5-Abfrage und Quellenbelege | DB `mode=ro`, `quick_check`, Quelle/URI/Hash | `PENDING_WINDOWS` |
| P7 | UC-01/UC-02 Golden Slice und unabhängigen Review | reproduzierbare Python/solver-QA, unabhängiges Review | `PENDING_REVIEW` |
| P8 | WORK/GitHub-Snapshot und SHA-256-Readback | gleicher Bytehash, Ziel-ID, Commit/PR, Receipt | `PENDING_DELIVERY` |
| P9 | Registrieren / Freigabe | Ledger-ID durch Single Writer, ACK, ID01 Human Gate | `REGISTRATION_PENDING` |

**Keine blind ausgeführten Installationsbefehle:** Download/Plugin-Installation, OAuth, DB-Write, API-Kosten und Desktop-Einstellungsänderung sind eigene, explizit prüfpflichtige Arbeitsschritte.

## 7. Abgleich: Gemini v1.3, DeepSeek-Gegenentwurf und Primärquellen

| Gegenentwurf / Hinweis | Übernommen | Korrigierte Aussage / offen |
|---|---|---|
| [Gemini v1.3](https://drive.google.com/file/d/1SHOFokCl-v8SiVviD651fRl8HxqgVsGJ/view), [Windows-Guide](https://drive.google.com/file/d/1ie4-fozcnoYNHkikwql2ZqFtmsXs9TVF/view) | Windows-Preflight, Flash/Pro-Routing, Caching, Ollama, MCP-Pilot, Engineering-Usecases | `settings.yaml`-Primärrolle veraltet; `master_register.db`, `worm_ledger.jsonl` und Workspace-MCP-Format nicht als wirklich vorhandene kanonische Instanz behaupten; Archiv-/Git-Hash ist keine echte WORM-Unveränderlichkeit. |
| [Gemini Google-Docs-Guide](https://docs.google.com/document/d/1AAQh69OUuXaKjFWb1umYwQ9SLZfeOYIU8kaU26XES2o/edit) | Übersicht/Checkliste | Native Google Docs mit `.md`-Suffix sind kein Raw-UTF-8-Markdown; Kern-Hash im Dokument ohne Rechen-/Quellscope kein Beleg. |
| DeepSeek-Korrekturtext aus dem Upload 19.11. | Trennung `cordis.patch.yml`/Session-Log; Flash/Pro/Ollama | `DSH_TELEMETRY_DISABLED` stoppt **nicht** den DeepSeek-Session-Log-Kanal; die als `local-model`/`llm-deepseek` gezeigten YAML-Configs sind **keine** gegen die aktive DSH-Schema-Version verifizierten Rezepte. |
| DeepSeek `dsh --profile web --dump-config` | CLI-Inspektionsbefehl offiziell vorhanden | Kein Nachweis des Desktop-Profils; `desktop` über Electron verwaltet; Configdump ist kein Netzwerk-/Egress-Beweis. |
| DeepSeek `dsh-workspace-mcp`, `.dsh/mcp.servers.yml` | Pluginidee für projektspezifische Isolation | Communityabhängig; offizielle Basiskonfiguration bietet MCP Manager; Test auf aktuell genutzter RC erforderlich. |
| DeepSeek `dsh-budget-watcher` | Kandidat | tatsächliche Budget-Blockierung/Abrechnungsgenauigkeit erst mit Test verifiziert; keine Produktionsgates aus Marketing-Claims. |
| DeepSeek `https://api.github.com/mcp` | **Nicht übernommen** | Keine offizielle Service-/Authentifizierungsprüfung; keinen fiktiven MCP-Endpunkt in produktiver Konfiguration verteilen. |

## 8. Vier gezielte Eingaben von ID01 für die produktive Feinabstimmung

1. **DSH-Profil und Version**: Screenshot aus der Desktop-App mit aktivem Modell/Profil und Pfad der geöffneten `cordis.patch.yml` (ohne Secrets).
2. **Lokaler Modellbestand**: Ausgabe `ollama list` und `Get-Command dsh` (ohne Token) sowie GPU-/RAM-Daten, sofern bereits bekannt.
3. **SQLite-Quellpfad**: ist AnythingSearch `G:\Meine Ablage\_INDEX_LNK\00-AnythingSearch\AnythingSearch.db` tatsächlich die aktuell konsistente DB? Gibt es zusätzliche Projekt-DBs und welches Read-only-Scope?
4. **Monatliche Kostenobergrenze / Cloud-Datenfreigabe**: Budget in USD sowie explizite Klassifikation der Daten, die DeepSeek-Cloud erhalten darf.

Diese Angaben sind für den **generischen Read-only-MVP nicht blockierend**; sie sind Pflicht vor Windows-Installation, kostenträchtigem Cloud-Test oder produktiver Durchsetzung.

## 9. Quellenverzeichnis (Primärquellen)

- DeepSeek Harness: [Hauptrepository](https://github.com/deepseek-ai/deepseek-harness), [Provider/Models](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/providers.md), [CLI-Konfiguration](https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/reference/README.md), [Desktop](https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/desktop/README.md), [MCP Manager](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/mcp/mcp-manager/README.md), [MCP Client](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/mcp/mcp-client/README.md), [Session-Log](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/session/session-log-deepseek/README.md).
- DeepSeek API: [Preise/Modelle](https://api-docs.deepseek.com/quick_start/pricing/), [Thinking Mode](https://api-docs.deepseek.com/guides/thinking_mode/), [KV Cache](https://api-docs.deepseek.com/guides/kv_cache/), [Chat Completions](https://api-docs.deepseek.com/api/create-chat-completion/).
- SQLite: [URI mode=ro](https://www.sqlite.org/uri.html), [PRAGMA quick_check](https://www.sqlite.org/pragma.html).
- MCP: [offizielle Serverreferenzen](https://github.com/modelcontextprotocol/servers), [archivierte SQLite-Implementierung](https://github.com/modelcontextprotocol/servers-archived), separat zu bewertende Community-Plugins [dsh-local-model](https://github.com/songzhiyin/dsh-local-model) und [dsh-workspace-mcp](https://github.com/Momojie-S/dsh-workspace-mcp).
- NEXUS eigene Quellen, genaue Fundstellen: Begleitdatei **Bestandsanalyse und Quellenregister** vom selben Datum sowie aktuelle WORK-Governance-Originale.

## 10. Statusreport / Hand-off

- `FINDINGS`: Gemini, DeepSeek und aktuelle Herstellerdokumentation konsolidiert; kritische Telemetrie-, MCP-, Desktop- und SQLite-Aussagen korrigiert.
- `EVIDENCE/SOURCES`: Kapitel 0/7/9 plus separate Bestandsanalyse; Datum 19.11.2026.
- `ARTIFACTS`: dieses versionierte MD-Handbuch, separate Quelleninventar-/Bestandsanalyse-Datei.
- `RISKS`: unbestätigtes Windows-DSH-Profil/Ollama/SQLite; Drittplugin-Supply-Chain; private Daten-Exfiltration; Sync-Gates FAIL; Single-Writer-/Ledger-Pending.
- `QA_STATUS`: Primärquellen-Abgleich und Dokumentenreview durch diese Instanz; **kein** unabhängiges Review oder Windows-Livetest; keine Engineering-/Security-Release-Freigabe.
- `NEXT_ACTION`: beide Raw-MD-Originale mit SHA-256 in WORK ablegen, per Readback prüfen, GitHub nur als Draft-PR-Snapshot; Ledger-Registrierung an autorisierten Single Writer übergeben.
