---
name: NEXUS-CAPABILITY-ACK
version: 1.0.0
status: OPEN
timestamp: 2026-11-12T00:12:17+01:00
timezone: Europe/Vienna
agent_id: ID02
executor: ChatGPT tool-enabled session
ticket_id: WO-20261112-ID02-CAPABILITY-ACK
source_role_register: NEXUS-ROLES-v1.1
registration_status: REGISTRATION_PENDING
ledger_number: null
independent_review: PENDING
---
# P0 Work Order: Rollen-ACK und Runtime-Capabilities

OWNER_ID: ID02; APPROVER: ID01; RECIPIENTS: ID03–ID08. ID09/ID10 inaktiv, nicht zu aktivieren.
OBJECTIVE: Für jede aktive Rolle tatsächliche Kenntnisnahme der aktuellen Regeln und Schreibfähigkeiten pro realer Runtime nachweisen.
SOURCE/SSOT: Manifest §4 NEXUS-ROLES-v1.1 https://docs.google.com/document/d/1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg/edit ; AGB v006 https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view ; Frontmatter v006-ID02-ROLE-ADOPTED (Gesamtstatus ENTWURF) https://drive.google.com/file/d/1rKnQMZbhO6ii0ThnJLhUCRYrXFcDvRbi/view ; Ticketregister https://docs.google.com/spreadsheets/d/1o1ZCZUgsCGTDOwdbJ7EbUCKOKJng1LcJLFnrRiPjYTE/edit ; Rollenbekanntgabe https://github.com/julianzotter/nexus-platform/issues/76 .
INPUTS: Bestandsmatrix v0.1 vom 14.10.2026 ist historischer DRAFT und enthält veraltete ID02/ID03-Zuordnung; nicht als aktueller Rechtebeweis verwenden. GitHub- und Drive-Schreibrechte sind Runtime-, Konto- und Scope-abhängig.
TASK: Jede aktive Rolle liest die drei aktuellen Quellen selbst und antwortet mit Version, Zeit, tatsächlicher Runtime und Konflikten. Je Runtime werden GitHub/Drive read/create/update/commit/push getrennt erfasst; Scope, Kontoidentität, Auth-Status und überprüfbarer Beleg. Keine Probeänderung ohne gesondert autorisiertes Ziel. ID03 prüft die Konsolidierung unabhängig.
EXPECTED_OUTPUT: ein Antwortdatensatz je Rolle und Runtime; Aktualisierung bestehender ACK-ROLES-v1.1-Tickets; quellengebundene Capability-Matrix ohne neue Masterregistry.
ACCEPTANCE_CRITERIA: Für ID02–ID08 jeweils tatsächlicher ACK; aktuelle Quellen mit Version; belegte Capability je Operation als VERIFIED/DENIED/UNVERIFIED; getrennte unabhängige ID03-Prüfung. Veröffentlichung allein ist kein Zustell- oder ACK-Nachweis.

## Antwortschema v1
```json
{"ticket_id":"WO-20261112-ID02-CAPABILITY-ACK","role_id":null,"executor_instance":null,"provider":null,"model_id":null,"read_sources":[{"uri":null,"version":null,"read_at":null}],"capabilities":[{"service":"github|google_drive","operation":"read|create|update|commit|push","scope":null,"account_identity":null,"auth_status":"VERIFIED|DENIED|UNVERIFIED","evidence_uri":null,"observed_at":null}],"conflicts":[],"ack_status":"ACK|PENDING|BLOCKED","response_uri":null}
```
Null bedeutet unbekannt, nicht fehlendes Recht. Jede Antwort muss die eigene Runtime nennen; Rollenname allein ist kein Berechtigungsbeleg.

## Writeback / Tracking
1. Vor jeder Änderung Ticketregister erneut lesen; betroffene Zeile anhand eindeutiger ticket_id prüfen. Bestehende ACK-ROLES-v1.1-Zeilen ID02–ID08 fortschreiben, kein zweites Register. Für diesen Auftrag eine eindeutige neue Ticketzeile nur nach Konfliktprüfung.
2. Eingehenden Original-ACK mit Quelle, Zeit und Runtime erhalten; keinen fremden ACK aus Veröffentlichung ableiten. Status OPEN → CLAIMED → RUNNING → REVIEW_REQUIRED → DONE nur nach Abnahmekriterien; BLOCKED mit Grund.
3. Schreibvorgang gegen erwarteten Vorzustand prüfen, danach Provider-Readback der betroffenen Zellen. Bei Konflikt stoppen und frisch abgleichen. Sheets-Connector bietet hier keinen atomaren Compare-and-Swap; parallele Schreiber müssen über eine zuständige Einzelinstanz serialisiert werden.
4. Neue WORK-Artefakte im bestehenden file-registry.jsonl append-only registrieren; vollständige Rohbytes und SHA-256 vor Abschluss rücklesen. Ledgernummer ausschließlich ID03 nach tatsächlicher Vergabe. Ohne Registrierungs- oder History-Beleg: REGISTRATION_PENDING / LEDGER-PENDING.
5. Bis alle Antworten vorliegen, nur belegten Teilstand berichten; Empfängerzustellung, ACK, Capability und Review getrennt verfolgen.

CURRENT_OBSERVATION: Manifest registriert ID01–ID08; ID09/ID10 sind inaktiv. Ticketregister: ID02 Selbst-ACK DONE; ID03–ID08 OPEN/PENDING_ACTUAL_RESPONSE. Historische Capability-Matrix v0.1 ist DRAFT und für aktuelle GitHub-/Drive-Rechte nicht maßgeblich.
NEXT_ACTION: Rundfrage im bestehenden Rollen-Issue #76 veröffentlichen; reale Antworten der Rollen einsammeln und nach obigem Writeback nachführen.


## ID01-Auftrag und ID03-Evaluierung · 2026-11-23

### Lauf und Geltungsbereich
- ticket_id: WO-20261112-ID02-CAPABILITY-ACK
- run_id: ID03-BASELINE-AUDIT-20261123T173713Z
- observed_at: 2026-11-23T17:37:13Z / 18:37:13 Europe/Berlin
- executor: ChatGPT / OpenAI; executor_instance: /root; model_id: null (API-Modellkennung nicht separat verifiziert)
- role_id: ID03, gemäß ausdrücklicher Zuordnung im aktuellen ID01-Sprachauftrag und Manifest §4.
- ack_status: ACK für ID03; ID04 und ID06: PENDING_ACTUAL_RESPONSE.
- inspection_status: COMPLETED_BOUNDED; Gesamtanforderung: BLOCKED_LOCAL_MOUNT / SYNC_UNVERIFIED.
- registration_status: REGISTRATION_PENDING; ledger_number: null. Keine neue Nummer vergeben.
- Der ursprüngliche Auftrag oben bleibt erhalten. Dieser datierte Nachtrag aktualisiert nur den belegten Teilstand dieser Laufzeit.

### Korrigierter Befehl
> ID01 – Julian Zotter, Human in the Loop – an ID03 ChatGPT, ID04 Gemini und ID06 Claude: Führt umgehend jeweils in eurer tatsächlich verfügbaren Laufzeit eine interne Evaluierung der freigegebenen Baseline-Konfiguration durch. Lest zuerst die aktuellen Projektanweisungen, _AGBS.md, Manifest, Baseline und Ticketregister. Prüft eure Fähigkeiten zur GitHub-Synchronisation im freigegebenen Umfang, zum obligatorischen Schreiben von Statusberichten in die zugehörige Work Order und zur Speicherung sämtlicher erzeugter Artefakte im verifizierten, lokal gemounteten Google Drive. Belegt Repository, Branch und Commit-Stand sowie Zielpfad, Drive-Datei-ID, Hash und Readback. Kein Arbeitsergebnis darf ausschließlich in einer flüchtigen Sandbox verbleiben. Fehlende Mounts, Zugriffe, Quellen oder Synchronisationsnachweise sind als BLOCKED beziehungsweise UNVERIFIED auszuweisen. Jede Rolle bestätigt Empfang, tatsächliche Laufzeit, Prüfstatus, Evidenz, Blocker und nächste Aktion selbst. Technische Freigaben bleiben bei ID01.

Routing-Empfehlung: Für diesen fest zugeordneten Auftrag genügt direkte Multi-Agent-Orchestrierung über die Rollen-IDs und die bestehende Work Order. Ein zusätzlicher Router wird nicht eingerichtet. Die ID-Ansprache allein stellt keinen technischen Zustellkanal her. Publikation, Zustellung, ACK, Review und Freigabe bleiben getrennt.

### Rollenbezug
Nach aktuellem Manifest §4, NEXUS-ROLES-v1.1:
- ID01: Julian Zotter – Human in the Loop, Prioritäten und Freigaben.
- ID03: ChatGPT Assistant / Peer Reviewer – Abnahmekriterien, QA und Peer Review.
- ID04: Gemini – Protokoll, Evidenz, Quellenverfolgung und Status.
- ID06: Claude – Implementierung, deterministische Werkzeuge und Tests.
Diese Liste ist ein zitierter Auszug für den Auftrag; die Rollenautorität bleibt das Manifest.

### ID03: belegter Fähigkeitstest
| Prüffeld | Status | Beobachtung / Beleg | Grenze / nächste Aktion |
|---|---|---|---|
| Governance-Lesezugriff | VERIFIED | _AGBS.md v007.1, Manifest, Baseline, Folder.md und Ticketregister über Drive gelesen; Quellen unten. | Lesezugriff beweist keine automatische Durchsetzung. |
| Google-Drive-Dateilesen | VERIFIED | Bestehende Capability-Work-Order als Text und vollständige Rohdatei (4.501 Byte) gelesen; parent = WORK. | Kein Nachweis eines lokalen Mounts. |
| Google-Drive-Schreiben | PENDING_AT_REPORT_RENDER | Schreibwerkzeug für bestehenden Markdown-Dateiinhalt vorhanden; dieser Nachtrag ist das autorisierte Berichtsupdate. | Erst ausgeführter Write plus nachfolgender Rohbyte-Readback belegen Erfolg. |
| Lokaler Google-Drive-Mount | BLOCKED | Aktuelle Laufzeit: /workspace/scratch/d2e73e523b5b; findmnt -T meldet /workspace, Typ overlay; sichtbare Mount-Tabelle ohne identifizierbaren Google-Drive-/rclone-/FUSE-Mount. | Kein Urteil über ID01s Windows-Rechner. Mountpflicht muss in einer tatsächlich verbundenen lokalen Runtime geprüft werden. |
| GitHub-Lesezugriff | VERIFIED | julianzotter/nexus-platform lesbar; main zum Prüfzeitpunkt c6379c6fbe9b10a1b031711ca61335d6540aa0f1; AGENTS.md gelesen. | Zeitgebundene Remote-Beobachtung. |
| GitHub-Berechtigung | VERIFIED_METADATA_ONLY | Repository-Metadaten melden pull=true, push=true, admin=true. | Diese Rechteangaben ersetzen keinen tatsächlich ausgeführten Commit-/Push-Test. |
| GitHub Commit/Push | NOT_RUN / UNVERIFIED | Keine Probeänderung am Repository ausgeführt. | Vor einer Erfolgsaussage konkretes autorisiertes Testziel und Remote-Readback erforderlich. |
| Lokaler Git-Abgleich | BLOCKED | git rev-parse --show-toplevel im aktuellen Workspace: fatal: not a git repository. Git 2.56.1 und gh 2.46.0 sind vorhanden. | Kein lokaler HEAD/Origin für einen vollständigen Standvergleich. |
| Lückenlose Synchronisation | UNVERIFIED | Kein vollständiges Artefaktmanifest, kein kontinuierlicher Lauf-/Fehler-/Nachholnachweis in diesem Audit geprüft. | Ein punktueller Remote-Read beweist keine dauerhafte Synchronisation. |
| ID04-/ID06-Ausführung | UNVERIFIED | In diesem Lauf keine tatsächliche Antwort von Gemini oder Claude. | Echte Empfänger müssen Auftrag annehmen und eigenständig berichten. |
| Ausschließlich flüchtige Daten | UNVERIFIED_SYSTEMWIDE | Prüfung betrifft diese Laufzeit. Fremde Sandboxes, andere Geräte und die Vollständigkeit aller bisherigen Artefakte wurden nicht geprüft. | Keine globale Aussage „alles gesichert“. Dieser Nachtrag wird dauerhaft als bestehende Work Order gespeichert. |

### Relevante Baseline-Abweichungen
1. _AGBS.md §9 und Troubleshooting T11 bezeichnen die Claude-Kennung noch als ungeklärt; das kanonische Manifest §4 weist ID06 ausdrücklich Claude zu. Für diesen Auftrag gilt Manifest plus aktuelle ID01-Anweisung. Keine Governance-Datei wurde stillschweigend geändert.
2. Der ursprüngliche Auftrag verweist auf AGB v006. Das aktuelle kanonische _AGBS.md liefert v007.1 samt Ergänzung vom 23.11.2026. Historische Quellenangaben oben bleiben erhalten; dieser Nachtrag verwendet die neu gelesene Fassung.
3. Folder.md begrenzt GitHub auf Review-Snapshots und untersagt unbelegte bidirektionale Synchronisationsbehauptungen. Die Formulierung „lückenlos“ wird deshalb nur für einen definierten, nachweisbaren Synchronisationsumfang bewertet.

### Quellen und Fundstellen
| Quelle | Version / beobachtete Provider-Änderung | Fundstelle |
|---|---|---|
| [Manifest](https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view) | NEXUS-ROLES-v1.1; modified 2026-11-17T19:21:49.987Z | §4 Rollen; §6 Kommunikation; §10 Governance |
| [Baseline](https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view) | CURRENT 2026-09-28 mit Nachträgen; modified 2026-11-17T19:21:52.328Z | MUST-20/21/25; 40–54; 90–96; 150/159 |
| [_AGBS.md](https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view) | v007.1; modified 2026-11-23T12:56:53.289Z | §§5–10; ID01-Ergänzung vom 23.11.2026 |
| [Folder.md](https://drive.google.com/file/d/1nDjF78dq3l8PGpXsauzBz1bzHescDSwv/view) | policy_version 0.4.0-pilot; modified 2026-11-16T21:50:06.607Z | sync_rule; historische Statusdaten nicht als neuer Live-Test verwendet |
| [Ticketregister](https://docs.google.com/spreadsheets/d/1o1ZCZUgsCGTDOwdbJ7EbUCKOKJng1LcJLFnrRiPjYTE/edit) | modified 2026-11-23T17:06:45.362Z | WO-20261112-ID02-CAPABILITY-ACK; ACK-ROLES-v1.1-ID03/04/06 |
| [Troubleshooting](https://drive.google.com/file/d/1OXKmuSPdXTwwy3AfECQR4hRm1iNu_4JR/view) | v001; modified 2026-11-23T14:15:22.912Z | T01/T03/T11/T12 |
| [Repository-AGENTS.md](https://github.com/julianzotter/nexus-platform/blob/main/AGENTS.md) | bei diesem Lauf live gelesen | WORK Markdown; Nachweisgrenzen; Control-Panel-Startgate |
| [GitHub main-Snapshot](https://github.com/julianzotter/nexus-platform/commit/c6379c6fbe9b10a1b031711ca61335d6540aa0f1) | abgefragter Branch-HEAD | Remote-Stand; kein eigener neuer Commit |
| Lokale Werkzeugausgabe | 2026-11-23, interner Prüfer /root/local_capability_audit | pwd; findmnt; git rev-parse; git --version; gh --version |

### QA und offene Nachweise
- Separater ChatGPT-Prüfer kontrollierte die lokale Laufzeit; ein zweiter prüfte Befehlsfassung, Rollen, Zustellung und den Unterschied zwischen Momentaufnahme und dauerhafter Synchronisation. Keine Gemini-/Claude-Beteiligung behauptet.
- Lokale Prüfung und Formulierungsreview: abgeschlossen im angegebenen Umfang. Das ist keine Abnahme der anderen Agenten oder der NEXUS-Gesamtintegration.
- Control-Panel-Live-Stand, LLM-HISTORY-LOG, Ticket-Writeback und file-registry-Registrierung wurden in diesem begrenzten Audit nicht aktualisiert; die entsprechenden Pflichten bleiben offen.
- Nach Persistierung sind Ziel-Datei-ID, unveränderter WORK-Parent und vollständige Rohbytes gegen den lokalen SHA-256 zu prüfen. Dieser Text stellt keine eigene Speicherquittung dar.
- GitHub-Spiegel dieses Nachtrags: NOT_RUN. Zustellung/ACK ID04 und ID06: PENDING.
- Nächste Aktion: ID04 und ID06 bestätigen den Auftrag in ihrer realen Laufzeit; die lokale Runtime mit Google-Drive-Mount liefert Pfad-/Schreib-/Readbacknachweise. Anschließend kann der autorisierte GitHub-Synchronisationslauf auf einem konkreten Review-Ziel verifiziert werden.


## ID03-Abschlussreceipt: Basic-Instructions-EVAL + FAQ · 2026-11-23 18:29:16 UTC

category: status_report; run_id: ID03-BASELINE-EVAL-20261123T181602Z.
START_ACK: ID03 hat diesen Auftrag in der tatsächlichen ChatGPT/OpenAI-Runtime /root angenommen. Quellen: _AGBS v007.1, NEXUS-ROLES-v1.1, Baseline CURRENT und Folder 0.4.0-pilot. Fremde ACKs werden daraus nicht abgeleitet.

### Ergebnis und aktueller Einstieg
[Basic-Instructions-Evaluierung, FAQ und konsolidierter Prüfauftrag v3.1](https://drive.google.com/file/d/1w_IyHkyo07JJZf6Pp69h-Fh10FKAq6jE/view) sind in WORK veröffentlicht und als Rohbytes verifiziert: 35364 Bytes, vollständiger SHA-256 444403823c4159c8df7cb0de163576364c1d6222da56666edeec10668eb96a92. Dieser Bericht bündelt die Antworten; es wurde kein zweites Rollenregister oder Masterticket eingerichtet.

Interner Dokumentreview: PASS durch /root/review_governance für Body-SHA-256 364149a59550c91c400b09a881b2f488e4d1eff360ac635825ff3d39227ba23b. Finaler Dateikopf dokumentiert das Review; keine Cross-ID-Abnahme und keine technische Freigabe behauptet. Globale Basic Instructions und fremde Modelleinstellungen wurden nicht geändert.

### Aktuelle eigene Capability-Belege
- ID03 Drive-API create + raw readback: PASS. Testdatei 1rrV1kwV0GiWy01LnBGFCwWIIJQ2xivF8, WORK, 878 Bytes, SHA-256 69ab937978ee186e034aa4f6416be7cef676875ce93551d4d157ae0ecb416e12.
- ID03 GitHub-API commit + raw readback: PASS. Repository julianzotter/nexus-platform, eigener Zweig id03/baseline-eval-20261123t181602z, [Testcommit 974e63df3ee7ad117f4c63af2b18f7d1f0606637](https://github.com/julianzotter/nexus-platform/commit/974e63df3ee7ad117f4c63af2b18f7d1f0606637). Drive=GitHub=lokales Original. Lokaler git push: NOT_RUN.
- ID03 Drive-Mount: BLOCKED_LOCAL_MOUNT. API-Persistenz ersetzt den fehlenden Mountnachweis nicht.
- T2 bisheriger WORK-Append: Rohbytegleichheit bestätigt; weitere Berichtspersistenz oben belegt. Registrierung offen.
- T4 für die vor diesem Receipt eingefrorenen Outputs Test/FAQ-Bericht/Lauflog: PASS, alle drei in Drive mit Rohbytevergleich. Dieses Receipt wird anschließend als Ergänzung derselben Work Order separat rückgelesen; sein eigener vollständiger Dateihash wird nicht zirkulär im Text eingebettet. Der GitHub-Abschlusssnapshot folgt auf demselben Zweig.
- T5: BLOCKED, unabhängiger Eurocode-/NA-Golden-Case fehlt. T6 Dokumentlesen: PASS; lokales RAG: NOT_RUN. T7 Drive-/GitHub-Lesen: PASS im benannten Scope; andere Connectoren NOT_RUN.
- [Lauflog in LLM-HISTORY-LOG](https://drive.google.com/file/d/1aAI7nO4ziDk1CHuA_oYCfqHOrtSZxnGA/view): 2459 Bytes, SHA-256 2d263c92453ced9fcf863b6bc4f3aac2c8e883e3b377744486f57126390c9631, rohbytegleich. Ein früher fehlender Startlog wurde als RESUME_START nachgetragen, nicht rückdatiert.

### Rollen-/Speicherkorrektur und Archivierung
Perplexity = ID05, DeepSeek = ID07, Claude = ID06 gemäß [Manifest §4](https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view). Rollenidentität und nachgewiesener technischer Ausführer sind getrennt.

Der von ID01 referenzierte Perplexity-Protokollbeleg 1wjxj22S3dkusFcfESgJJMB62d7S_prWI bleibt in WORK. Seine Rohbytes sind identisch zur zweiten Kopie 1rlPWUzMWUfbA_aO83Rau8pqYABk3YinN: je 4182 Bytes, SHA-256 b13372b3af6317d020fde612034c42448682b15f1a6a6421320c9cafbb822819.
Die zweite Kopie wurde nach bestehendem WORK/ALT, Parent 13SGKR4GgWbG_7ENiCUOvIzkpCWG0tpzY, verschoben. ID und Bytes unverändert, nach Move geprüft. Original-Felder id:NN und storage:sandbox_only bleiben historische Eigendeklaration; aktuelle Rollen-Normalisierung=ID05, beobachteter Speicherort=Drive. Der tatsächliche ursprüngliche Uploader bleibt UNVERIFIED. Kein Perplexity-Connector-PASS allein aus der vorhandenen Datei.

### Registerdelta – bereitgestellt, noch nicht gemergt
Die folgenden Datensätze sind Übergabedaten für den nach _AGBS §6.6 benannten Ledger-Schreiber Claude, keine behaupteten Einträge im bestehenden Register. Fehlende Werte bleiben null. Einheiten/Quellen und weitere Prüfgrenzen stehen im verlinkten Bericht.
~~~jsonl
{"artifact_id":"gdrive:1rrV1kwV0GiWy01LnBGFCwWIIJQ2xivF8","provider_file_id":"1rrV1kwV0GiWy01LnBGFCwWIIJQ2xivF8","name":"TEST_ID03_20261123-1916.md","canonical_uri":"https://drive.google.com/file/d/1rrV1kwV0GiWy01LnBGFCwWIIJQ2xivF8/view","version":"ID03-BASELINE-EVAL-20261123T181602Z","provenance":"ID03 actual Drive upload and GitHub API commit; raw-byte readback","verification_status":"FILE_VERIFIED","registration_status":"REGISTRATION_PENDING","registered_at":null,"owner":"ID03","ticket_id":"WO-20261112-ID02-CAPABILITY-ACK","sha256":"69ab937978ee186e034aa4f6416be7cef676875ce93551d4d157ae0ecb416e12"}
{"artifact_id":"gdrive:1w_IyHkyo07JJZf6Pp69h-Fh10FKAq6jE","provider_file_id":"1w_IyHkyo07JJZf6Pp69h-Fh10FKAq6jE","name":"26_11_23_1923_ID03_NEXUS-BASELINE_FAQ-REVIEW_UNREGISTERED.md","canonical_uri":"https://drive.google.com/file/d/1w_IyHkyo07JJZf6Pp69h-Fh10FKAq6jE/view","version":"1.0.0-review","provenance":"ID03 author; internal reviewer /root/review_governance; observed sources in report","verification_status":"FILE_VERIFIED","registration_status":"REGISTRATION_PENDING","registered_at":null,"owner":"ID03","ticket_id":"WO-20261112-ID02-CAPABILITY-ACK","sha256":"444403823c4159c8df7cb0de163576364c1d6222da56666edeec10668eb96a92"}
{"artifact_id":"gdrive:1aAI7nO4ziDk1CHuA_oYCfqHOrtSZxnGA","provider_file_id":"1aAI7nO4ziDk1CHuA_oYCfqHOrtSZxnGA","name":"26_11_23_1916_ID03_BASELINE-EVAL_RUNLOG_UNREGISTERED.md","canonical_uri":"https://drive.google.com/file/d/1aAI7nO4ziDk1CHuA_oYCfqHOrtSZxnGA/view","version":"ID03-BASELINE-EVAL-20261123T181602Z-final","provenance":"ID03 append-only runlog in LLM-HISTORY-LOG","verification_status":"FILE_VERIFIED","registration_status":"REGISTRATION_PENDING","registered_at":null,"owner":"ID03","ticket_id":"WO-20261112-ID02-CAPABILITY-ACK","sha256":"2d263c92453ced9fcf863b6bc4f3aac2c8e883e3b377744486f57126390c9631"}
{"artifact_id":"gdrive:1rlPWUzMWUfbA_aO83Rau8pqYABk3YinN","provider_file_id":"1rlPWUzMWUfbA_aO83Rau8pqYABk3YinN","name":"26_11_23_ID-PERPLEXITY_BASELINE-INSTRUCTION-EVALUATION.md","canonical_uri":"https://drive.google.com/file/d/1rlPWUzMWUfbA_aO83Rau8pqYABk3YinN/view","version":"original-bytes-metadata-move","provenance":"ID03 archived byte-identical duplicate; original uploader UNVERIFIED","verification_status":"FILE_VERIFIED","registration_status":"REGISTRATION_PENDING","registered_at":null,"owner":null,"ticket_id":"WO-20261112-ID02-CAPABILITY-ACK","sha256":"b13372b3af6317d020fde612034c42448682b15f1a6a6421320c9cafbb822819","parent_id":"13SGKR4GgWbG_7ENiCUOvIzkpCWG0tpzY","duplicate_of":"gdrive:1wjxj22S3dkusFcfESgJJMB62d7S_prWI"}
~~~

Offene bestehende Konsolidierung: 25 Delta-Zeilen 0212–0236 sind noch nicht im gelesenen Master. [Merge-Auftrag v0.2](https://drive.google.com/file/d/1ArJmk08HVn-wnOj18xpY7bqysv5Tclb8/view) fortsetzen. Die hashgleiche P205-Skriptkopie wurde identifiziert; kanonische Betriebsquelle und lokale Caller sind vor Verschiebung festzulegen. MCP-Skripte verschiedener Versionen wurden nicht als Dubletten behandelt.

Status: FAQ/Evaluierung im belegten Scope abgeschlossen; globale Baseline und Registrierung offen. Publication≠Delivery≠ACK≠Review≠Release. Keine E-Mails, keine Löschungen, keine Main-Änderung und kein behaupteter automatischer Rollout.
