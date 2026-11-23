---
name: 26_11_23_1923_ID03_NEXUS-BASELINE_FAQ-REVIEW_UNREGISTERED.md
version: 1.0.0-review
artifact_category: status_report
content_sections:
- faq
- baseline_review
- work_order_revision
role_id: ID03
provider: OpenAI
model_id: null
executor_instance: /root
timestamp: '2026-11-23T19:23:54+01:00'
run_id: ID03-BASELINE-EVAL-20261123T181602Z
ticket_id: WO-20261112-ID02-CAPABILITY-ACK
status: PARTIAL_VERIFIED
registration_status: REGISTRATION_PENDING
ledger_number: null
review_status: INTERNAL_DOCUMENT_REVIEW_PASS
cross_id_acceptance: PENDING
canonical_parent: gdrive:1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP
work_order_ref: gdrive:1y0DSTvkH_04avqI8TZKyaKOy05gWfZgx
sha256_scope: body_utf8_after_closing_frontmatter_lf
sha256: 364149a59550c91c400b09a881b2f488e4d1eff360ac635825ff3d39227ba23b
persistence_receipt_ref: gdrive:1y0DSTvkH_04avqI8TZKyaKOy05gWfZgx
capabilities_used:
- google_drive.read
- google_drive.create
- google_drive.update
- github.read
- github.api_commit
- python.sha256
capabilities_tested:
  drive_api_write_readback: PASS
  github_api_commit_readback: PASS
  drive_local_mount: BLOCKED
source_refs:
  roles: gdrive:1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn#4
  agbs: gdrive:10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg
  baseline: gdrive:1CdwNHr6i8lMG3k8A939kiznLMw8q7J69
  folder: gdrive:1nDjF78dq3l8PGpXsauzBz1bzHescDSwv
  github_snapshot: c6379c6fbe9b10a1b031711ca61335d6540aa0f1
  capability_work_order: gdrive:1y0DSTvkH_04avqI8TZKyaKOy05gWfZgx
source_versions:
  roles: NEXUS-ROLES-v1.1
  agbs: v007.1; provider_modified=2026-11-23T12:56:53.289Z
  baseline: CURRENT-2026-09-28; provider_modified=2026-11-17T19:21:52.328Z
  folder: 0.4.0-pilot; provider_modified=2026-11-16T21:50:06.607Z
registry_ref: gdrive:15m8T5cWbogIup9snzFwiB1g9HqNCoGow
reviewer_instance: /root/review_governance
reviewed_body_sha256: 364149a59550c91c400b09a881b2f488e4d1eff360ac635825ff3d39227ba23b
---
# NEXUS: FAQ, Baseline-Review und konsolidierter Prüfauftrag

## 1. Ergebnis und Geltungsbereich

Stand: 23.11.2026. Dieser Bericht beantwortet die FAQ und konsolidiert die widersprüchlichen v1–v3-Protokolle. Er ergänzt die [bestehende Capability-Work-Order](https://drive.google.com/file/d/1y0DSTvkH_04avqI8TZKyaKOy05gWfZgx/view); er eröffnet weder ein zweites Rollenregister noch ein neues Masterticket. Die unten formulierte v3.1 ist ein Reviewvorschlag. Die von ID01 bereits erlaubte Baseline-Prüfung und reversible Bereinigung sind davon getrennte, tatsächlich ausgeführte Arbeiten.

VERIFIED: ID03 hat ein Testartefakt über den Drive-Connector geschrieben und über die GitHub-API auf einem eigenen Zweig committet. Die anschließend von beiden Providern gelesenen Bytes stimmen mit dem lokalen Original überein. ID03 hat außerdem die schon zuvor ergänzte WORK-Work-Order erneut byteweise geprüft.

BLOCKED: Ein Google-Drive-Mount ist in dieser ChatGPT-Laufzeit nicht identifiziert. Die sichtbare Arbeitsfläche ist /workspace mit Dateisystemtyp overlay. Kein Befund über die Verfügbarkeit von G: auf ID01s Windows-Rechner.

UNVERIFIED: Gesamtsynchronisation aller Ordner, Fähigkeiten fremder Laufzeiten ohne Ausführungsbeleg, lokales RAG, fachlicher Eurocode-Golden-Case, vollständige Registrierung und Cross-ID-Abnahme. Eine auf Drive vorhandene Datei beweist nicht automatisch, welches Modell den Upload technisch ausgeführt hat.

## 2. FAQ: Speicherung, Tests und Reporting

| Frage | Präzise Antwort und Nachweis |
|---|---|
| Cloud Storage versus lokal gemountetes Laufwerk? | Cloud Storage liegt beim Provider und wird beispielsweise über die Drive-API angesprochen. Ein Mount stellt einen Dateisystempfad in einer bestimmten Runtime bereit. G: kann ein virtuelles Streaming-Laufwerk sein. Ein sichtbarer Pfad beweist weder vollständige Offline-Verfügbarkeit noch abgeschlossene Cloud-Synchronisation. Google unterscheidet Streaming mit lokaler Zwischenspeicherung und Spiegelung mit lokaler und Cloud-Kopie. [Google Drive](https://support.google.com/drive/answer/13401938) |
| API-Persistenz? | Tatsächlicher Upload/Update, zurückgelieferte Datei-ID und Zielparent, danach erneuter Download der Rohbytes und SHA-256-Vergleich. Die API kann Dateien erstellen und aktualisieren, ohne einen lokalen Mount zu benötigen. [Drive API](https://developers.google.com/workspace/drive/api/guides/manage-uploads) |
| Testartefakt im lokalen Drive speichern und zurücklesen? | Den Mount in der ausführenden Runtime identifizieren; absoluten Pfad und Hostkontext festhalten; Originalbytes hashen; über diesen Pfad schreiben; Datei schließen und neu öffnen; Rohbytes erneut hashen. Für belegte Cloud-Persistenz zusätzlich die entsprechende Provider-Datei identifizieren und dort rücklesen. Der lokale Cache allein genügt dafür nicht. |
| Zwei Capability-Einträge? | Ja: storage.drive_api.write_readback und storage.drive_mount.write_readback. Unterschiedliche Runtime, Operation, Scope und Ausführungsbelege. Cloud-Synchronisation nach lokalem Schreiben ist ein zusätzlicher Prüfaspekt. Ein API-PASS ersetzt den Mount-Test nicht. |
| Sandbox-Leerstand? | Gemeint ist: kein Ergebnis dieses Laufs liegt ausschließlich flüchtig vor. Lokale Arbeitskopien dürfen bleiben, da nichts gelöscht werden soll. Ein abschließendes Artefaktmanifest nennt jeden erzeugten/geänderten Output, sein dauerhaftes Ziel und seinen Hash. Eingangsdateien und reproduzierbare Caches getrennt behandeln; keine Behauptung über fremde Sandboxes. |
| Statusbericht nach AGBs? | UTF-8-Markdown in WORK, gemessener Zeitpräfix, belegte Rolle/Runtime, Kategorie, run_id, Auftrag, Quellen, Ergebnis, Blocker und nächste Aktion. Datei-ID, Parent, Name, MIME und Versionsstand dokumentieren; Rohbyte-Readback prüfen. Ohne Registrierung gilt FILE_VERIFIED / REGISTRATION_PENDING. [_AGBS §§4–7](https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view) |
| Reporting? | Startzeile in LLM-HISTORY-LOG, zusätzlich START_ACK in WORK; danach Annahme, wesentliche Blocker und Abschluss im bestehenden Laufbericht. Keine neue Datei pro Gesprächsbestätigung. Publikation, Zustellung, ACK, Review und Freigabe sind eigene Zustände. [_AGBS §§2,5,10 und Ergänzung 23.11.](https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view) |

Prüfstatus: PASS = ausgeführt und Soll erfüllt; FAIL = ausgeführt und Soll verfehlt; BLOCKED = erforderliche Voraussetzung fehlt; NOT_RUN = noch nicht ausgeführt. UNVERIFIED bezeichnet eine nicht belegte Aussage oder Herkunft, nicht automatisch eine fehlende technische Fähigkeit.

## 3. FAQ: GitHub, Automation und Zustandskontrolle

| Begriff | Bedeutung und NEXUS-Anwendung |
|---|---|
| Repository | Versionierter Projektbestand mit Dateien und Änderungshistorie. Das hier geprüfte Repository ist [julianzotter/nexus-platform](https://github.com/julianzotter/nexus-platform). |
| Branch / Commit / Push / Pull | Branch: eigener Entwicklungszweig. Commit: referenzierbarer Änderungsstand. Push: lokale Git-Commits an ein Remote übertragen. Pull: Remote-Änderungen in den lokalen Zweig übernehmen. Ein GitHub-API-Dateischreibvorgang erzeugt ebenfalls einen Remote-Commit, belegt aber keinen tatsächlich ausgeführten lokalen git push. |
| Pull Request / merged | Ein Pull Request schlägt Änderungen zwischen Zweigen zur Prüfung vor. Merged bedeutet, dass sie in den Zielzweig übernommen wurden. Das ist noch kein Beleg für Deployment, Drive-Synchronisation oder fachliche Freigabe. [GitHub PR-Dokumentation](https://docs.github.com/en/pull-requests/get-started/about-pull-requests) |
| GitHub-Sync | Für NEXUS gilt gegenwärtig: Drive ist Dokument-SSOT, GitHub führt Review-Snapshots. Punktueller Nachweis: Dateipfad und vollständiger Commit plus Rohbyte-Hashvergleich. Dauerhafte Synchronisation erfordert zusätzlich definierten Umfang, Richtung, Fehler-/Nachhollogik und aktuelle Laufbelege. [Folder.md, sync_rule](https://drive.google.com/file/d/1nDjF78dq3l8PGpXsauzBz1bzHescDSwv/view) |
| GitActions | Gemeint ist GitHub Actions: Automationsplattform. Workflows in .github/workflows enthalten Jobs/Schritte, ausgelöst durch Ereignisse, manuell oder nach Zeitplan. Sie laufen auf einem Runner. Eine Workflow-Datei ist kein Beleg für einen erfolgreichen Lauf. [GitHub Actions](https://docs.github.com/en/actions/get-started/understand-github-actions) |
| Scheduled Tasks | Zeit- oder ereignisgesteuerte Aufträge. Windows-Aufgabenplanung startet Programme auf einem bestimmten Rechner; GitHub-Schedules starten Workflow-Läufe auf Runnern. Der lokale Zugriff auf G: muss für genau den ausführenden Benutzer-/Dienstkontext geprüft werden. GitHub-Schedules können sich verzögern; ein aktivierter Zeitplan beweist keinen erfolgreichen Lauf. [Microsoft](https://learn.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page), [GitHub](https://docs.github.com/en/actions/how-tos/troubleshoot-workflows) |
| State-control | Zustandsführung mit Auftrag, Owner, run_id, Übergang, Zeitpunkt und Beleg. NEXUS definiert OPEN → CLAIMED → RUNNING → DONE sowie BLOCKED / REVIEW_REQUIRED / FAILED. Ein Dashboard zeigt einen projizierten Stand; ausschlaggebend sind Quittungen und getestete Übergänge. Schweigen und fehlender Fehlerlog sind kein Erfolg. [Manifest §6](https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view) |

Aktueller enger Actions-Befund aus unabhängigem API-Read: [Monitor 45198194995](https://github.com/julianzotter/nexus-platform/actions/runs/45198194995), gestartet 23.11.2026 14:48 UTC, FAILURE; [Delivery 45198599526](https://github.com/julianzotter/nexus-platform/actions/runs/45198599526), 14:50 UTC, FAILURE, eigentliche Zustellung nach fehlgeschlagenem Preflight übersprungen. Der am älteren Commit 5b0794887a392e50a11d8fe37ba0c3bfae7a1d5b ausgeführte [Poll-Lauf 45149342862](https://github.com/julianzotter/nexus-platform/actions/runs/45149342862), 09:41 UTC, ebenfalls FAILURE. Diese Belege erlauben kein aktuelles Gesamt-PASS für die automatische Synchronisation. Der Status lokaler Windows-Aufgaben wurde nicht gelesen.

Geprüfte Workflow-Konfiguration am Commit c6379c6fbe9b10a1b031711ca61335d6540aa0f1:

| Workflow | Deklarierter Auslöser | Ausführung und State |
|---|---|---|
| [Drive-Poll](https://github.com/julianzotter/nexus-platform/blob/c6379c6fbe9b10a1b031711ca61335d6540aa0f1/.github/workflows/nexus-drive-poll.yml) | Minute 07 und 37 jeder Stunde (UTC), manuell oder drive_change-Dispatch | GitHub-gehostetes Ubuntu 24.04; lesendes Änderungsfeed-Polling; Checkpoint im Actions-Cache. Der Name „Drive to GitHub“ beweist hier keine Dateiübertragung oder Commits. |
| [Monitor](https://github.com/julianzotter/nexus-platform/blob/c6379c6fbe9b10a1b031711ca61335d6540aa0f1/.github/workflows/nexus-monitor.yml) | Stündlich Minute 17 (UTC), Push auf main oder manuell | Repo-/Evidenzprüfung, Dashboard und Inventare; kein Repo-Push deklariert. |
| [GitHub → WORK](https://github.com/julianzotter/nexus-platform/blob/c6379c6fbe9b10a1b031711ca61335d6540aa0f1/.github/workflows/nexus-delivery.yml) | Abschluss eines Monitor-Laufs auf main oder manuell | Preflight, danach vorgesehener Transfer und Registrierung mit conditional-cas. Der letzte geprüfte Lauf erreichte den Schreibschritt nicht. |

Actions-Artefakte werden in diesen Konfigurationen 14 Tage beim Poll und 30 Tage bei Monitor/Delivery aufbewahrt. Sie ersetzen deshalb die langfristige SSOT-Ablage nicht. Die gemeinsame Writer-Concurrency-Gruppe serialisiert nur ihre GitHub-Workflows; sie sperrt keine fremden Drive-Connectoren oder lokalen Skripte. Die tatsächliche CAS-Funktion wurde hier nicht ausgeführt. Windows-Aufgabenstatus und kontinuierliche Einhaltung der Cron-Taktung bleiben ungeprüft.

Die Live-Kontrollpanel-Seite war über das verfügbare Web-Lesewerkzeug nicht abrufbar. Das ist eine Zugriffslücke dieses Prüfwegs; kein Nachweis, dass die Seite allgemein ausgefallen ist.

## 4. FAQ: Kernfunktionen, Ordner, Rollen und Registry

NEXUS verbindet nach seinem [Manifest §§1–8](https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view) quellengebundene Wissensarbeit, auftragsbasierte Agentenkoordination, deterministische Werkzeuge und nachvollziehbare Prüfung. Für diesen Auftrag ist das Zielprofil Tragwerksplanung/AEC: Eurocode-Nachweise, parametrische CAD/BIM-Modellierung, Python-/Fachsolver, Quellenretrieval/RAG sowie Berichte und Qualitätssicherung. Das Zielprofil ist keine Bestätigung, dass jede Funktion schon integriert oder fachlich freigegeben ist.

| Kernfunktion / Ablage | Zuständigkeit und nachgewiesener Ort |
|---|---|
| Rollenautorität | [Manifest §4](https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view), NEXUS-ROLES-v1.1. ID01 Julian; ID02 ChatGPT Orchestrator; ID03 ChatGPT Peer Reviewer; ID04 Gemini; ID05 Perplexity; ID06 Claude; ID07 DeepSeek; ID08 Ollama. ID09/10 inaktiv. Dieser Auszug bleibt eine Quellenwiedergabe, kein zweites Rollenregister. |
| LLM-LOCAL-SSOT | [Root](https://drive.google.com/drive/folders/1j3FLJkWpQv6xGA_KO0D9sMyA11f0vxBV): kanonisches Manifest, Baseline und gemeinsame Steuerartefakte. Dokumentquelle und Zugriffsort sind von einem ausführenden lokalen RAG-Dienst zu unterscheiden. |
| Basic Instructions / Baseline | [Baseline CURRENT](https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view): stabile Regeln, Pflichten und Verweise. Keine ständig wechselnden Endpunkte oder geheimen Zugangsdaten hineinkopieren. |
| Frontmatter | Maschinenlesbare Metadaten am Kopf einer einzelnen Datei. Es identifiziert Kategorie, Verfasser/Rolle, tatsächliche Runtime, Version, Zeit, Auftrag, Quellen und Prüfstatus. Es ist keine eigenständige Autorität für neue Rollen oder Rechte. Aktuelle auftragsrelevante Steuer-/Eingabedateien lesen; DRAFT und archivierte Dateien als solche behandeln. |
| WORK | [WORK](https://drive.google.com/drive/folders/1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP): Aufträge, ACKs, Statusberichte und Laufartefakte. _AGBS.md und Folder.md bestimmen den Betrieb. |
| SCRIPTS | [SCRIPTS](https://drive.google.com/drive/folders/1wkKlC7LIvcFDnLZkB4P35gN-KPL7oToF): vorhandener Skriptbestand. Ein Dateiname allein entscheidet weder kanonische Betriebsquelle noch Dublettenstatus. |
| MCP-ACCESS-TOOLS | [Ordner](https://drive.google.com/drive/folders/1fRa7rQvKi-BkhVIzjXPcY_u8iIJ4Vn5J): vorhandene Connector-/Dispatcher-Werkzeuge, Schemas, scripts/tools und Konfigurationen. Aktive Startbefehle, Versionen, Abhängigkeiten, Aufrufer und Runtime-Rechte prüfen. Konfigurationsdateien sind keine Funktionsbelege. |
| NEXUS.MCP.SERVER | [Ordner](https://drive.google.com/drive/folders/1tcgucSrrl-esSbbhhn4yYosDq8YSipEh): vorhandene Server-Ablage. Serverbetrieb/Erreichbarkeit in diesem Audit nicht getestet. |
| LLM-HISTORY-LOG | [Ordner](https://drive.google.com/drive/folders/1uavEf5g_ZisiEMsksrGi_KYzMsx37DWc): Start-, Watch-, Wartungs- und Steuerlogs. Kein Ersatz für den Ergebnisbericht in WORK. |
| Archiv | [WORK/ALT](https://drive.google.com/drive/folders/13SGKR4GgWbG_7ENiCUOvIzkpCWG0tpzY) für die hier begründete historische Protokollkopie; [_ARCHIVE_STEUERDATEIEN](https://drive.google.com/drive/folders/1FaqZ2xH3nzlDI80UDa_wrGmObvT6IB52) für überholte Steuerdateien. Bewegen erhält die Drive-ID; nichts löschen. |
| Registry / Ledger | [file-registry.jsonl](https://drive.google.com/file/d/15m8T5cWbogIup9snzFwiB1g9HqNCoGow/view) identifiziert Artefakte und Versionen; [00_ID_LEDGER.csv](https://drive.google.com/file/d/1Qso4VQE-cySJdxo6j-MNjxxOc5-GJlrK/view) führt Artefaktnummern; [Ticketregister](https://docs.google.com/spreadsheets/d/1o1ZCZUgsCGTDOwdbJ7EbUCKOKJng1LcJLFnrRiPjYTE/edit) führt Aufträge. Diese Register vergeben keine neuen Rollen-IDs. |
| Capability-Register | Liefert belegte Fähigkeiten je Rolle UND Runtime UND Operation. Ein kanonisches aktuelles _CAPABILITIES.jsonl wurde in der begrenzten Namenssuche nicht gefunden. Bis zur geprüften Einbindung: Laufdeltas im bestehenden Auftragskontext, keine konkurrierenden Master. Einziger Ledger-Schreiber ist laut _AGBS §6.6 Claude; Registrierung und fachliche Freigabe bleiben getrennt. |

Empfehlung für Basic Instructions: auf Manifest §4, _AGBS.md, bestehende Capability-Work-Order und das nach Prüfung registrierte Capability-Ziel verweisen. Im Lauf-Frontmatter die tatsächlich verwendeten Quellenstände und Tool-Bindungen angeben. Endpunkte nur als nicht geheime Kennung bzw. bereinigte Adresse; Schlüssel und tokenhaltige Webhook-URLs bleiben außerhalb der Dokumente.

## 5. Belegter Auditstand

### 5.1 Eigener ID03-Lauf

run_id: ID03-BASELINE-EVAL-20261123T181602Z; Executor ChatGPT / OpenAI / /root. Die Rollenkennung ID03 folgt der ausdrücklichen aktuellen ID01-Zuordnung; eine beobachtete API-Modell-ID liegt nicht vor. Interne ChatGPT-Prüfer sind keine Gemini-/Claude-Instanzen.

| Test | Status | Beweis | Blocker / Workaround |
|---|---|---|---|
| T1a GitHub-API-Publikation | PASS | [Commit 974e63df3ee7ad117f4c63af2b18f7d1f0606637](https://github.com/julianzotter/nexus-platform/commit/974e63df3ee7ad117f4c63af2b18f7d1f0606637); eigener Branch id03/baseline-eval-20261123t181602z; Datei WORK/BASELINE-EVAL/2026-11-23/ID03/TEST_ID03_20261123-1916.md; 878 Bytes; Remote=Drive=lokal. | Belegt diesen API-Vorgang. Keine dauerhafte bidirektionale Synchronisation. |
| T1b lokaler git push | NOT_RUN | Kein lokaler git push in diesem Lauf. | API-Commit getrennt erfassen. |
| T2 WORK-Bericht | PASS | Eigener früherer Append zur bestehenden Work Order, erneut am 23.11.18:16UTC zurückgelesen: 13616 Bytes, SHA-256 8e1c34003444b4d34a446aa775be219c867c4e138984c0316becb4fb691b061a. | Registrierung offen. Der spätere Abschlussreceipt verifiziert diese neue Berichtsversion gesondert. |
| T3a Drive-API | PASS | [Testdatei](https://drive.google.com/file/d/1rrV1kwV0GiWy01LnBGFCwWIIJQ2xivF8/view), Parent WORK; SHA-256 69ab937978ee186e034aa4f6416be7cef676875ce93551d4d157ae0ecb416e12. Upload plus unabhängiger Rohdownload ausgeführt. | Kein Mount-Beleg. |
| T3b lokaler Mount | BLOCKED | Sichtbare Arbeitsfläche /workspace overlay; kein identifizierter Drive-Mount. | In einer tatsächlich angebundenen lokalen Runtime prüfen. |
| T4 Laufoutputs vollständig persistiert | NOT_RUN | Test und Startlog sind bereits rückgelesen; Bericht, letzter Logstand und WO-Nachtrag werden anschließend persistiert. | Abschließender Nachweis folgt in der bestehenden Work Order; kein vorgezogenes PASS. |
| T5 Eurocode-/Rechen-Golden-Case | BLOCKED | In diesem Lauf keine fachliche Rechnung ausgeführt. | Versionierter, unabhängig geprüfter Fall einschließlich Normausgabe/NA fehlt; widersprüchliche v3-Fixtures nicht vermischen. |
| T6 Dokumentzugriff | PASS | _AGBS.md v007.1 direkt gelesen; Persistenz-Nachweis steht in §7. | Das ist kein lokaler RAG-Lauf. |
| T6 lokales RAG | NOT_RUN | Kein lokaler Retriever-/Index-Endpunkt aufgerufen. | Pipeline, Corpus-Version und Golden Case festlegen und tatsächlich ausführen. |
| T7 Drive/GitHub lesen | PASS | Tatsächliche Metadaten-/Datei-/Commit-Aufrufe und Rückläufe dieses Laufs. | Andere Connectoren und andere Operationen nicht mitabgedeckt. |

Capability-Statement: Kann in dieser Runtime nachgewiesen Drive-Dateien lesen, neue Rohdateien schreiben, eigene Berichte in-place ergänzen und rücklesen, eine Datei metadata-seitig verschieben sowie GitHub-API-Commits auf eigenem Zweig erstellen und lesen. Kein identifizierter lokaler Drive-Mount. Lokaler Git-Transport, fachliche Solverintegration, RAG und sämtliche übrigen Connectoren in diesem Lauf nicht getestet.

[Start-/Lauflog](https://drive.google.com/file/d/1aAI7nO4ziDk1CHuA_oYCfqHOrtSZxnGA/view): RESUME_START am 23.11.2026 18:16:02UTC; der zuvor fehlende Startlog wird ausdrücklich nicht rückdatiert. Naming-Ausnahme UNREGISTERED dokumentiert, da keine Nummer vom Ledger-Schreiber vergeben wurde.

### 5.2 Unabhängiger Review fremder Belege

ID06: Die [Testdatei](https://drive.google.com/file/d/12HB6noYZewfbmvGGzCV5M9igD4UFwzmD/view), der [Status](https://drive.google.com/file/d/1JHx9-tLrseOlG9b2g3-EXMtQSO9jYuUZ/view), [ACK](https://drive.google.com/file/d/1kuYnOZ9XdSkiPW6owXRl-OfrBoH9GNKN/view) und [RUNLOG](https://drive.google.com/file/d/1f6eATmEDo-GhWUgjRjKWJU363iIClYoJ/view) wurden durch einen separaten internen ChatGPT-Prüfer als Rohbytes gegen Commit ed207168e67633e6043e2ab97acab8e9cd521611 verglichen: jeweils bytegleich. Auch Commit 49774f0baf643a2adce07ba043088c789f0e4866 existiert. Das belegt den Remote-Dateibestand; der ursprüngliche lokale Push, G:-Write und vollständige Sandbox-Inhalt bleiben ohne unabhängiges Ausführungsreceipt unbestätigt.

Der [Claude-v3-Entwurf](https://drive.google.com/file/d/1V6jC1IQhsqFj3YNn-VOeGP6C-zglOud2/view) ist bytegleich zur Datei am Commit 856a88a9657ac0c47f6dee80e94037a1d28d55a5; 3444 Bytes; SHA-256 af5120dcd74284b21c527ee4747d7d698e27a0f5e48a2f518203190d304995ba. Er ist ENTWURF, nicht global freigegebene Baseline. Fehler: Perplexity als NN, Mounttest zu allgemeinem Drive-Test abgeschwächt, T6 nur Dokumentfrage, Eurocode-Soll vom selben Autor ohne belegte Normausgabe/NA. Der andere als v3 bezeichnete Perplexity-Text verwendet abweichende Geometrie/Lasten und eine andere Review-Kette. Der Versionsname allein bezeichnet somit keinen eindeutigen Test.

ID05/Perplexity: Der [referenzierte Beleg](https://drive.google.com/file/d/1wjxj22S3dkusFcfESgJJMB62d7S_prWI/view) und die [zweite Kopie](https://drive.google.com/file/d/1rlPWUzMWUfbA_aO83Rau8pqYABk3YinN/view) sind 4182 Bytes, SHA-256 b13372b3af6317d020fde612034c42448682b15f1a6a6421320c9cafbb822819. Ihr Bodyhash 4a5bdd71e73db6ad6eee79860cbe1d8c10c01ba5ca7bc4d530cbb9be4bcb962a stimmt. VERIFIED ist die Persistenz dieser Bytes. Der technisch ausführende Uploader ist aus diesen Dokumenten nicht authentifiziert; deshalb kein eigenes Connector-PASS für Perplexity ableiten.

Korrekturreceipt: declared_agent_id=NN; normalized_role_id=ID05 nach Manifest §4; observed_storage=Google Drive; ursprüngliches storage:sandbox_only ist als aktueller Speicherstatus überholt. Die Originalbytes bleiben als historische Evidenz erhalten. Dieser ausdrückliche Nachtrag korrigiert ihre heutige Auslegung; eine neue Datei mit unverändertem eigenem Hash wird nicht fingiert.

### 5.3 Tatsächliche Bereinigung und offene Konsolidierung

Ausgeführt: Die ältere byteidentische Perplexity-Kopie 1rlPWUzMWUfbA_aO83Rau8pqYABk3YinN wurde aus WORK nach vorhandenem WORK/ALT (13SGKR4GgWbG_7ENiCUOvIzkpCWG0tpzY) verschoben. ID und Name bleiben erhalten. Erneuter Rohbyte-Readback bestätigt denselben SHA-256. Der von ID01 referenzierte Beleg 1wjxj22S3dkusFcfESgJJMB62d7S_prWI bleibt in WORK. ALT ist eine dokumentierte operative Wahl für diesen Einzelfall; keine neue allgemeine Archivregel.

Offen: Das [Ledger-Delta 17.11.](https://drive.google.com/file/d/1SzINh0IX5Ng-kmmkAGjyyqd02J3kLLym/view) enthält 25 Datensätze 0212–0236; sie fehlen im gelesenen Master. Dessen 201 Datensätze reichen numerisch bis 0211. [Vorhandenen Merge-Auftrag v0.2](https://drive.google.com/file/d/1ArJmk08HVn-wnOj18xpY7bqysv5Tclb8/view) fortführen, kein weiteres Merge-Ticket erzeugen. Root hat das gemeinsame Ledger nicht geschrieben. Historische ID10-Provenienz in einer Deltazeile ist nicht automatisch eine heutige aktive Rollenkennung.

Skript-Dublette VERIFIED: [WORK-Kopie](https://drive.google.com/file/d/1aTsZyWz6CneSBE4fXOzSM0Jha89KRyre/view) und [SCRIPTS-Kopie](https://drive.google.com/file/d/1GAxp5TGVYXnspYKf5ZNnCx1oX49novti/view) von P205_FT_Excel_Native_Recalc_v1_2.ps1 sind jeweils 5408 Bytes und hashgleich: 1d91a1c5ae5676bd40d83aaba5fa453addd4228b5277741883c756117d055ac3. Der [Windows-Handoff](https://drive.google.com/file/d/1IYOV-B8EmaVrk6IbqG_cTKjfh-vPihL8/view) ruft C:\NEXUS\tools\windows\P205_FT_Excel_Native_Recalc_v1_2.ps1 auf, legt aber keine der Drive-Kopien als Installationsquelle fest. Deshalb vor einem Verschieben kanonische Betriebsquelle und Caller abgleichen.

MCP: nexus_tower.py v0.3.0 und nexus_tower-1.py v0.2.0 sind unterschiedliche Inhalte, keine Hash-Dubletten. Der vorhandene Launcher startet nexus_tower.py; v0.3.0 importiert nexus_status aus demselben Ordner. Keine ungeprüfte Zusammenlegung. Vorhandenen [MCP-Teilauftrag D](https://drive.google.com/file/d/1uniI-8U2rUDh7Y4zTQ3nuMuN4nqJmpjf/view) und [Review-Pointer](https://drive.google.com/file/d/13lWii4cWaUS81CRbTBf8vytxIVw2R6ax/view) weiterverwenden.

Inventargrenze: SCRIPTS und direkte MCP-Unterordner wurden vollständig auf erster Ebene gelistet; WORK-Pending-Suche war paginiert und nicht vollständig ausgewertet. Keine Gesamtzahl oder pauschale Erledigung aller Pending-Dateien. Das gelesene file-registry.jsonl enthält 472 gültige JSON-Zeilen, SHA-256 3ae1bd1f36c193d63338ec81285fe282231eb793ec81990ef53aaf2f32e7f592; die beiden Perplexity-Dateien und die beiden P205-Kopien wurden darin nicht gefunden. Registrierung bleibt offen.

## 6. Konsolidierter Prüfauftrag v3.1 – Reviewvorschlag

Auftrag: WO-BASELINE-EVAL; Anker: WO-20261112-ID02-CAPABILITY-ACK.
Absender: ID01. Empfänger: ID02–ID08 in ihrer tatsächlich verfügbaren Runtime. ID01 ist Human in the Loop. Keine neue ID vergeben. Die Rollenautorität bleibt Manifest §4.

Ziel: Fähigkeiten der tatsächlich ausgeführten Operationen belegen. Sprachliche Regelbindung ist eine Prozessanforderung; deterministische Rechenaussagen stammen aus versionierten Werkzeugläufen. Kein universell deterministisches LLM-Verhalten versprechen.

### 6.1 Bootstrap, Zuständigkeit und Schutzregeln

1. Aktuelle _AGBS.md, Manifest-MD, Baseline-MD, WORK/Folder.md, Ticket und relevante Frontmatter lesen. Quelle, Version/Hash, Abrufzeit, Geltungsbereich und Konflikte dokumentieren. Fehlendes blockiert nur den betroffenen Schritt.
2. Eigene Rolle, Provider, Modellkennung soweit beobachtbar, Runtime-Instanz und Werkzeug-/Dateisystemscope deklarieren. Fremde Berichte nicht als eigene Ausführung übernehmen. Unbekannte Modellkennung = null.
3. START_ACK in WORK und Startzeile in LLM-HISTORY-LOG. Die bestehende Session-Erlaubnis deckt die genannten isolierten Tests ab; keine erneute Einzelgenehmigung erfinden. Ein erstmalig fehlendes Konto, Endziel oder Secret bleibt konkreter Blocker.
4. Keine E-Mails, keine Löschung, keine Geheimnisse. Testphase: neue Testdateien und angehängte Laufereignisse. Keine Main-Änderung. Die bereits autorisierte Archivierung ist eine getrennt protokollierte Phase mit ID-/Hash-Erhalt.
5. Genau ein zuständiger Writer pro gemeinsamem Register. Alle anderen liefern ein gebündeltes Delta je Lauf. Vor Merge aktuellen Stand lesen, Kollisionen prüfen, Altinhalt erhalten und nach Write byteweise vergleichen; ohne atomare Sperre keinen parallelen Writer starten.
6. Rollen bleiben im Manifest. Das bestehende Artefaktregister bleibt erhalten. Ein Capability-Register benötigt verifizierten Ort, Schema und Writer; es wird nicht allein durch seine Erwähnung als existent oder registriert behandelt.
7. Autor und Reviewer sind getrennte Instanzen. Für die geforderte Cross-ID-Abnahme zusätzlich einen anderen realen Rolleninhaber mit reviewer_role_id ungleich subject_role_id einsetzen; Rolle, Runtime und Prüflauf belegen. Reviewer erst nach echtem ACK und belegtem Zugriff zuweisen. Interne ChatGPT-Unteragenten erfüllen nur die interne Dokument-QA, keinen externen Rollen-ACK. Technische Freigabe bleibt bei ID01.
8. Sprachmodus: nur mit Sprechrecht von ID01 sprechen; Beginn „Hier spricht ID xx“, Abschluss „Over and Out“; danach mindestens zwei Sekunden Übergabezeit. Bei parallelem Beginn entscheidet ID01. Keine hörbaren Schweige-/Wartebestätigungen. Schweigen ist weder ACK noch Freigabe. Ein Prompt stellt keine technische Audiokanalsperre her.

### 6.2 Ziele und Frontmatter

Repository: https://github.com/julianzotter/nexus-platform.
WORK: https://drive.google.com/drive/folders/1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP.
Logs: https://drive.google.com/drive/folders/1uavEf5g_ZisiEMsksrGi_KYzMsx37DWc.

Pro Runtime ein kollisionsfreier Testzweig mit tatsächlicher ID und gemessener Startzeit. Pro Lauf ein unveränderliches TEST-Artefakt und ein konsolidierter ACK-/Status-/Korrekturbericht; zusätzliche Quittungen nur für tatsächliche Ergebnisse. Dateiname nach _AGBS §4; ohne zugewiesene Nummer ausdrücklich UNREGISTERED, keine Nummer aus Dateinamen ableiten. UTC-Zeit im Laufdatensatz, lokale Dateizeit Europe/Vienna; Europe/Berlin ist am Prüftag ebenfalls UTC+01:00.

Pflichtfelder des Lauf-Frontmatters:

| Feld | Inhalt |
|---|---|
| name, version, artifact_category | Tatsächlicher Dateiname, Version, eindeutige Kategorie: work_order, status_report, capability_delta, runlog, test_fixture oder review. Kombinierte Inhalte im Statusbericht als Abschnitte kennzeichnen. |
| role_id, provider, model_id, executor_instance | Manifestrolle und tatsächliche Ausführungsidentität getrennt; unbekannte Angaben null. |
| ticket_id, run_id, timestamp | Bestehendes Ticket, eindeutiger Lauf, gemessener ISO-8601-Zeitpunkt mit Zeitzone. |
| source_refs, source_versions | Kanonische Rollen-/Regel-/Testquellen mit Stand und Fundstelle. |
| capabilities_used, capabilities_tested | Konnektor plus konkrete Operation/Scope; nur Ergebnisse dieses Laufs mit Beleg. |
| evidence_status, registration_status, review_status | Belegprüfung, Registrierung und Review getrennt. |
| sha256, sha256_scope | Bodyhash über UTF-8-Bytes nach schließendem Frontmatter samt festgelegten Zeilenenden; vollständigen Datei-Hash extern im Receipt führen. Kein zirkulärer Vollhash der eigenen Datei. |
| storage_at_creation, persistence_receipt_ref | Historischen Erstellungsort und späteren aktuellen Speicherbeleg trennen. Keine zeitlose Behauptung sandbox_only nach bestätigter Persistierung. |

Ein Datei-ID-Eintrag in einer neuen Kopie muss deren eigene Provider-ID meinen; die ID des Vorgängers gehört in derived_from. Für unveränderliche Testdateien Speicherbelege extern referenzieren.

### 6.3 Tests und Akzeptanz

| Test | Ausführung | PASS-Kriterium und Grenze |
|---|---|---|
| T1a GitHub-Persistenz | Testdatei über den tatsächlich vorhandenen Weg auf eigenen Branch schreiben. Vollständigen Commit auflösen, dieselbe Datei am festen Commit rücklesen. | Remote-Rohbytes = Original; Dateipfad, Commit, Hash und Werkzeugweg belegt. |
| T1b lokaler Git-Transport | Nur in einer tatsächlich verbundenen Git-Runtime: lokaler Commit und git push; Remote-Ref prüfen. | Erfolgreicher echter Push und korrekter Remote-Stand. API-Commit ist kein Ersatzbeleg. |
| T2 WORK-Bericht | AGB-konformen Laufbericht in WORK schreiben, Provider-Metadaten und Rohbytes rücklesen. | Richtiger Parent, Name, MIME, stabiler Stand und SHA-Gleichheit. Ohne Registry weiterhin REGISTRATION_PENDING. |
| T3a Drive-API | Derselben Runtime einen begrenzten API-Write plus Rohdownload zuordnen. | Datei-ID, Scope, tatsächlicher Ausführungsbeleg und SHA-Gleichheit. Bloßes Vorhandensein einer fremden Datei ist kein eigener Capability-Test. |
| T3b lokaler Drive-Mount | Tatsächlichen Mount identifizieren; über absoluten Pfad schreiben und erneut lesen; Cloud-Ziel gesondert rücklesen. | Lokaler Pfad-/Write-/Readbackbeleg und zugeordnetes Cloud-Receipt. Fehlender Mount = BLOCKED. |
| T4 Persistenzabschluss | Vollständiges Manifest der Outputs dieses Laufs gegen dauerhaft gespeicherte Kopien abgleichen. | Kein Output ausschließlich flüchtig. Bereich, Ausnahmen und Hashbelege explizit. Keine Löschpflicht für lokale Kopien. |
| T5a Python-Ausführung | Versioniertes Skript mit eingefrorenen Eingaben, Einheiten, Umgebung und vorab unabhängig festgelegtem Soll/Toleranz zweimal ausführen. | Exitcode erfolgreich, Soll erfüllt, reproduzierbare Ausgabe, Skripthash. |
| T5b Eurocode-Fachfall | Zusätzlich Normausgabe, nationalen Anhang, Formeln/Fundstellen, Anwendungsbereich und Golden Case prüfen. | Erst nach unabhängiger fachlicher Bestätigung aller Voraussetzungen. Keine der widersprüchlichen v3-Zahlenlisten ungeprüft übernehmen. Ohne Referenzfall BLOCKED. |
| T6a Dokumentretrieval | Festgelegte Frage: Welche AGB-Version wurde gelesen, welcher Abschnitt regelt Persistenz? | Aktueller Quellstand, Fundstelle und passender Inhalt. Eingefrorener Referenzstand dieser Prüfung: v007.1, §7. Bei Versionswechsel Referenzfall aktualisieren, nicht alte Antwort erzwingen. |
| T6b lokales RAG | Dieselbe Frage über benannte echte Retrieval-Pipeline stellen; Corpus-/Indexstand, Anfrage, Quellenrücklauf und Locator sichern. | Quellenidentität und vorab festgelegte fachliche Assertions erfüllt. Direktes Drive-Lesen ersetzt die Pipelineprüfung nicht. |
| T7 Konnektoren | Pro auftragsrelevantem Connector und benötigter Operation ein begrenzter Smoke-Test. Standardmäßig nur lesend; T1–T3 sind ausdrücklich begrenzte Schreibtests. | Werkzeugname, Operation, Scope, UTC, normalisierte Antwort/Fehlercode und Beleg. Tokenhaltige URLs redigieren; Webhook-Aufrufe nicht pauschal als nebenwirkungsfrei ansehen. |

Pflichtausgabe: Test | PASS/FAIL/BLOCKED/NOT_RUN | Beweis | Blocker | Workaround. Danach Capability-Statement „nachgewiesen / in dieser Runtime nicht verfügbar / nicht getestet“. Eine Rolle erhält kein Gesamt-PASS, solange verpflichtende Nachweise fehlen. Der Router darf nur Fähigkeiten anfordern, die im konkreten Ausführungskontext belegt oder im Auftrag ausdrücklich erst zu prüfen sind.

### 6.4 Abschluss und Delta-Vertrag

Ein Delta-Datensatz enthält mindestens run_id, subject_role_id, executor_instance, provider, model_id, connector, operation, scope, endpoint_ref ohne Secrets, test_status, evidence_uri, content_sha256, observed_at und reviewer_ref. Quellstatus und gegebenenfalls original_upload_executor=UNVERIFIED erhalten. Keine eigene Ausführung im Namen anderer Rollen eintragen.

Alle Deltas im konsolidierten Laufbericht bündeln; eine separate Importdatei nur, wenn der vorhandene Writer sie technisch benötigt. Genau der benannte Ledger-Schreiber führt nach ID-/Versions-/Kollisionsprüfung zusammen. Danach Provider-Readback und Registrierungsbeleg. Ohne diesen Schritt bleiben REGISTRATION_PENDING und der bestehende Merge-Auftrag offen.

Abschluss: Outputmanifest und externe Speicherreceipts; Runlog fortschreiben; eigenen ACK/Status in WORK veröffentlichen. Zustellung und tatsächliche Kenntnisnahme jeder anderen Rolle separat belegen. Kein Versand/Empfang allein aus einer Drive-Datei ableiten.

## 7. Übergabe

ID03: aktuelle Datei-/Hashbelege, FAQ und korrigierte Prüfdefinition konsolidiert; keine fachliche Eurocode-Freigabe.
ID06 als benannter Ledger-Schreiber: bestehenden Merge-Auftrag und Registrierung der belegten Änderungen bearbeiten; eigene technische Ausführungsbelege liefern.
ID02: reales Routing und Reviewer-Zuordnung anhand verfügbarer Runtime-Capabilities und tatsächlicher ACKs.
ID01: verbleibende technische Annahme-/Governanceentscheidungen anhand der konkreten konsolidierten Fassung, ohne erneute Freigabe bereits autorisierter isolierter Arbeit.

Die formelle Aktualisierung der globalen Basic Instructions, eines kanonischen Capability-Registers und der anderen Modelleinstellungen ist mit diesem Bericht nicht behauptet. Diese Datei ist ein nachvollziehbarer Arbeitsstand mit Quellen und umsetzbarem Prüfvertrag.
