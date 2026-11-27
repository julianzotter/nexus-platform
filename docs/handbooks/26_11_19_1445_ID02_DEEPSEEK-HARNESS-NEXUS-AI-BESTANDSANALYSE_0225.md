---
title: "DeepSeek Harness × NEXUS-AI – Bestandsanalyse und Quellenregister"
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
verification_status: "SOURCE_READ_VERIFIED; WINDOWS_RUNTIME_NOT_TESTED"
canonical_folder: "gdrive:1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP"
github_role: "review_snapshot_only"
source_date: "2026-11-19"
---

# DeepSeek Harness × NEXUS-AI – Bestandsanalyse und Quellenregister

## 1. Ausgangsbefund (aus der vorigen Chat-Ausgabe übernommen)

**TL;DR:** Für dein NEXUS-AI-AEC-System ist eine personalisierte Integration von DeepSeek Harness technisch sinnvoll. Drei Punkte sind entscheidend:

1. **Modellstrategie:** `deepseek-flash` für Routineaufgaben, `deepseek-v4-pro` für komplexe Analysen, Ollama für lokal vertrauliche Verarbeitung. Die beiden DeepSeek-Modelle sind Cloudmodelle.
2. **Tool-Integration:** Die offizielle Harness-Version enthält bereits einen MCP-Manager. SQLite, GitHub und Google Drive sollten darüber zunächst lesend angebunden werden. Zusätzliche Community-Plugins sind optional.
3. **Datenschutz und Qualität:** Ein lokales Peer-Review-LLM verhindert keine bereits erfolgte Cloud-Übertragung. Für echte lokale Verarbeitung müssen Modellaufrufe, Tools, Logging und Netzwerkzugriffe gemeinsam kontrolliert werden. Besonders wichtig ist die Prüfung des standardmäßig aktiven DeepSeek-Session-Log-Uploads.

## 2. Identifizierte NEXUS-Quellen (19.11.2026)

| Quelle | Referenz | Verifizierter Befund / Reichweite |
|---|---|---|
| DeepSeek-Chat-Export Part-02 | [Drive-Datei](https://drive.google.com/file/d/157nBKsS9ksXnlsoBFtBxwDKVwPsgjwI_/view) | 396.192 Byte; gemeldete Windows-Version 0.2.0-rc.2, Provider `deepseek-official`, Modelle `deepseek-flash`/`deepseek-v4-pro`, Pluginliste und Settings; Benutzerangaben, kein Live-Hosttest. Der Export enthält eingebettete Bilddaten und ist nicht als ungefilterter Systemprompt zu verwenden. |
| DeepSeek-Chat-Export Part-01 | [Drive-Datei](https://drive.google.com/file/d/19RbupTeNYu1kl0v41DzDWVPSaD1ueyEU/view) | Ergänzendes Gesprächsprotokoll; keine Runtime-Abnahme. |
| Ursprüngliche Diagrammvorlage | [Drive-Datei](https://drive.google.com/file/d/1yiI_yLaIQaYb22ubaGwTW0E6QpJob1Y-/view) | Schichtenentwurf für Harness/Orchestrierung/MCP/Daten; kein abgenommenes Implementierungsschema. |
| NEXUS-Benutzerhandbuch 18.11. | [Drive-Datei](https://drive.google.com/file/d/1YiVFpt9z0PaxnpvvSdfeGvBLu-SW97iJ/view) | Wiederverwendbare Architektur-Inhalte; unbereinigtes Session-Transkript, nicht automatisch kanonisch. |
| NEXUS `_AGBS.md` v007.1 | [Drive-Datei](https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view) | Im Lesezugriff v007.1 mit `FREIGEGEBEN_ID01`; Raw-Byte-Readback der früheren Aktivierung bleibt getrennt zu prüfen. |
| `Folder.md` (WORK) | [Drive-Datei](https://drive.google.com/file/d/1nDjF78dq3l8PGpXsauzBz1bzHescDSwv/view) | WORK als Dokument-SSOT; GitHub Review-Snapshot, nicht als funktionierender Bidirektional-Sync ausgegeben. |
| NEXUS Manifest (kanonisches MD) | [Drive-Datei](https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view) | ID01 Human Gate; ID02 Orchestrator; ID07 DeepSeek Prüfinstanz; ID08 Ollama lokal. |
| NEXUS Baseline (kanonisches MD) | [Drive-Datei](https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view) | MUST-20/21 Speicherorte, MUST-26 Secrets, MUST-40/45 Aufträge, MUST-50–54 Reporting, MUST-60–68 Quellen, Human Gate. |
| `_TROUBLESHOOTING.md` | [Drive-Datei](https://drive.google.com/file/d/1OXKmuSPdXTwwy3AfECQR4hRm1iNu_4JR/view) | T01 Dateiersetzung, T04 OAuth, T12 Registrierung; Status Entwurf. |
| `nexus-platform/AGENTS.md` | [GitHub](https://github.com/julianzotter/nexus-platform/blob/main/AGENTS.md) | Arbeitsbeginn mit aktuellen Governance-Dateien, Draft-PR/Readback/Review-Anforderungen; Actor-Runtime nicht gleich Rollennummer. |
| DeepSeek × NEXUS RFEM-Pilot | [GitHub PR #84](https://github.com/julianzotter/nexus-platform/pull/84) | Draft/open, 19 Offline-Tests gemeldet; Windows-DSH-Authentifizierung und RFEM Liveprüfung explizit offen. |
| Critical-Gates/Synchronisation | [GitHub Issue #73](https://github.com/julianzotter/nexus-platform/issues/73) | Laufnachweise für Monitor/Poller/Delivery erforderlich, keine automatisch angenommene Sync-Funktion. |
| NEXUS CPLM-Audit v0.2.139 | [Drive-Datei](https://drive.google.com/file/d/1lQ02o39bJUn322FQl_GYYb8FCdFQEyUV/view) | `BLOCKED_NO_RELEASE`; einzelne CI erfolgreich, systemweite Sync-Gates weiter FAIL, Registry-Pending. |

## 3. Maßgebliche offizielle / primäre Entwicklerquellen

| Gegenstand | Quelle | Befund |
|---|---|---|
| Profile, Konfigurationsschichten | [DeepSeek Harness CLI/Profilreferenz](https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/reference/README.md) | Profilpatch `$DSH_HOME/profiles/<profile>/cordis.patch.yml`; darüber Home-Patch und `--patch`-Overlays; ältere `settings.yaml`-Anleitung nicht unbesehen übernehmen. |
| Modelleinstellungen | [Harness Providers Guide](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/providers.md) | Settings → Models; Default für neue Sessions; nach erstem Turn bleibt das Modell in Sessionhistorie festgehalten; Modell-/Effort-Felder adapterabhängig. |
| Offizieller MCP-Manager | [dsh-mcp-manager](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/mcp/mcp-manager/README.md) | Web/Desktop enthalten den Manager; `config.servers`, Status, Probe, Readback; credential references statt Klartext. |
| MCP-Client | [dsh-mcp-client](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/mcp/mcp-client/README.md) | Tools werden unter `mcp__<server>__<tool>` sichtbar; verbundenes Tool ≠ erlaubter Write. |
| Cloudpreise | [DeepSeek Pricing](https://api-docs.deepseek.com/quick_start/pricing/) | Flash/Pro, Peak/Off-Peak, Cache-Hit/Miss getrennt; Preisangaben immer mit Abrufdatum führen. |
| Thinking | [DeepSeek Thinking Mode](https://api-docs.deepseek.com/guides/thinking_mode/) | `reasoning_effort`/`reasoning`/`thinking` sind endpointabhängig. |
| Context Caching | [DeepSeek KV Cache](https://api-docs.deepseek.com/guides/kv_cache/) | Exakte Präfixübereinstimmung; `prompt_cache_hit_tokens`, `prompt_cache_miss_tokens`; best effort. |
| Lokales LLM (Community) | [songzhiyin/dsh-local-model](https://github.com/songzhiyin/dsh-local-model) | Kandidat Ollama; Funktions-/Kompatibilitätsprüfung gegen RC und Supply-Chain-Prüfung ausstehend. |

## 4. Evidenzmatrix: IST / Vorschlag / kritischer Korrekturbedarf

| Aussage | Klassifikation | Konsequenz |
|---|---|---|
| Harness 0.2.0-rc.2 auf Julians Windows-Rechner | `USER_REPORTED` | Versionsbefehl/Screenshot erneut am Host prüfen. |
| `deepseek-official` mit Flash/Pro | `USER_REPORTED`; API-/Cloudnatur `DOC_VERIFIED` | Keine Annahme eines lokal laufenden DeepSeek V4. |
| 29 Session-Plugins/194 globale Plugins | `USER_REPORTED` | Exakten Profil-/Preset-Export lesen; nicht mit aktiviertem Connectorumfang gleichsetzen. |
| `tool-fs`, `tool-fs-search`, `tool-pwsh`, `skill-filesystem`, `tool-workflow` | `USER_REPORTED` | Tool-Aktionsumfang/Permissions per harmlosen Read-Test bestätigen. |
| Ollama Qwen-Modell / RTX 4080 | `HISTORY_REPORTED` | `ollama list`, Endpoint und GPU am Windows-Host prüfen; kein Laufbeleg hier. |
| `G:\Meine Ablage\_INDEX_LNK\00-AnythingSearch\AnythingSearch.db` | `HISTORY_REPORTED` | Existenz, DB-Version, SQLite `quick_check` read-only; kein Cloud-Index als Dateibeleg. |
| DeepSeek API Key vorhanden | `USER_REPORTED_CONFIGURATION` | Gespeicherter Provider ≠ authentifizierter Request; Secret nie ausgeben. |
| Lokaler Ollama-Reviewer = Zero Egress | `REJECTED_INFERENCE` | Nur rein lokal geroutete Gesamtkette mit kontrolliertem Logging, Tools und Netzwerk kann Zero-Egress beanspruchen. |
| Pro/Flash und Cacheoptimierung | `DOCUMENTED_DESIGN` | Messung von Nutzung, Cache und Qualität anhand gleicher Testfälle. |
| Third-Party-Plugin `dsh-workspace-mcp` | `COMMUNITY_CANDIDATE` | Projektdateiname/Syntax und Kompatibilität uneinheitlich; zunächst offiziellen MCP-Manager vorziehen. |
| OAuth Drive↔GitHub Sync erfolgreich | `NOT_VERIFIED / FAIL` | Monitoring-/Poller-/Delivery-Receipts nach Issue #73 erforderlich. |

## 5. Drei priorisierte Folgemaßnahmen

1. **Windows-Preflight / Privatsphäre:** effektives DSH-Profil, Modell, Session-Log-Upload, Ollama-Endpoint und Plugininventar read-only belegen.
2. **Ein MVP, nur lesend:** AnythingSearch-Metadaten → Originalquelle mit Hash → NEXUS-Workorder → DeepSeek (nur freigegebene Inhalte) → deterministische Prüfung → ID01-Freigabe.
3. **Versionierte Umsetzung:** vollständiges Handbuch, Audit-Tests und GitHub-Draft-PR; WORK-Raw-Markdown mit SHA-256-Readback; Ledger-Schreiber separat, Registrierung und Peer-Review offen ausweisen.

## 6. Status / Grenzen

- `FINDINGS`: Quellen und Governance gelesen; widersprüchliche historische Konfigurations- und Rollenaussagen abgegrenzt.
- `EVIDENCE/SOURCES`: Abschnitt 2/3; Retrieval am 19.11.2026.
- `ARTIFACTS`: dieses Basisdokument; dazugehöriger Implementierungsguide separat.
- `RISKS`: private Daten bei Cloud-Modell/Session-Log/Community-Plugins; laufender Sync-FAIL; Windows-Rechte und Ledger nicht nachgewiesen.
- `QA_STATUS`: inhaltliche Quellenprüfung; kein Windows-Livetest, kein unabhängiges Review, keine technische Betriebsfreigabe.
- `NEXT_ACTION`: Readback/Hashes prüfen, Workspace-Preflight durch ID01 oder autorisierte Windows-Runtime; bestehenden Single-Writer-Ledger verwenden.
