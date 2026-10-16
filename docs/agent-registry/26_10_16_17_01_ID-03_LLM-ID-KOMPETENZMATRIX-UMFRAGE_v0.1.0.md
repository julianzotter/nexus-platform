---
document_id: NEXUS-LLM-AGENT-REGISTRY
version: 0.1.0
timestamp: "2026-10-16T17:01:00+02:00"
status: REGISTRATION_OPEN_NOT_CANONICAL
owner: ID01_UNRESOLVED_NUMBER_HUMAN_JULIAN
author: ChatGPT-Codex / bisherige Sitzungskennung ID-03
folder_id: 1blG7BkL19NvIcNrB7qwglMCXIHNGlvok
source_of_truth: "Drive-Draft; GitHub nur versionierter Review-Snapshot"
id_mapping_status: CONFLICT_REQUIRES_RESOLUTION
---
# NEXUS LLM-ID-Kompetenzmatrix, Fähigkeitsumfrage und Troubleshooting
## 1. Ziel und Grenzen
Der WORK-Einstieg verlinkt auf diesen separaten Registrierungsordner. Kein zweiter unabhängig bearbeiteter Master in WORK. Diese Arbeitsregistrierung ersetzt keine bislang gültige Rollenregistrierung. Nummern werden erst nach Quellenabgleich und Human Gate als kanonisch markiert.
Ein Markdown allein erzwingt kein Verhalten. Verbindliche Integration benötigt installierte Agentenanweisungen plus technisch kontrollierte Start-/Abschlussgates. Ein freier Chat außerhalb der kontrollierten Runtime kann nicht zentral zum Lesen gezwungen werden.
## 2. Identität sauber trennen
| Objekt | Inhalt | Änderungsrate |
|---|---|---|
| human_authority | Julian Zotter; letzte Freigabeinstanz | langsam |
| role_id | Aufgabe/Funktion; unabhängig von Provider | langsam |
| account_id | Business/Privat/Tenant/Anmeldung; keine Secrets | mittel |
| provider_id | OpenAI, Google, Anthropic usw. | mittel |
| model_id | tatsächlich verwendete Modellkennung/Version; UNKNOWN falls nicht offengelegt | schnell |
| instance_id | konkrete Session/Worker/Runtime | je Lauf |
| capability | erlaubte UND nachgewiesene Operation im konkreten Ziel | mit Testdatum |
| availability | freie Slots, Budget/Quota, Heartbeat, Ablaufzeit | kurzlebig |
GPT-1/GPT-2 sind vom Nutzer verwendete Account-Aliase; sie sind nicht automatisch NEXUS-Rollen-IDs.
## 3. Vorläufige Account-/Capability-Matrix
Keine pauschalen Provider-Stärken oder Modellversionen erfunden. USER_REPORTED ist kein bestandener Zugriffstest.
| Vorgeschlagener Account-Alias | Beschreibung | Rollen-ID | Raw-MD lesen/schreiben | GitHub | Ace Knowledge Graph | Evidenz |
|---|---|---|---|---|---|---|
| ACC-CGPT-BIZ | GPT-1 / ChatGPT Business laut Nutzer | UNRESOLVED | NOT_TESTED | NOT_TESTED | USER_REPORTED_FAIL | aktuelle Nutzerangabe; kein Fehlerlog |
| ACC-CGPT-PRIVATE | GPT-2 / privater ChatGPT-Account laut Nutzer | UNRESOLVED | NOT_TESTED | NOT_TESTED | USER_REPORTED_WRITE | aktuelle Nutzerangabe; kein Instanztest |
| ACC-GEMINI | Gemini, Account/Plan noch zu bestätigen | UNRESOLVED | NOT_TESTED | USER_REPORTED_LIMITATION | NOT_TESTED | aktueller Nutzerhinweis |
| ACC-CLAUDE | Claude, Account/Runtime noch zu bestätigen | UNRESOLVED | NOT_TESTED | NOT_TESTED | NOT_TESTED | Registrierungsziel, kein Capability-Nachweis |
| ACC-PERPLEXITY | Account/Runtime noch zu bestätigen | UNRESOLVED | NOT_TESTED | NOT_TESTED | NOT_TESTED | Registrierungsziel |
| ACC-DEEPSEEK | Account/Runtime noch zu bestätigen | UNRESOLVED | NOT_TESTED | NOT_TESTED | NOT_TESTED | Registrierungsziel |
| INSTANCE-CURRENT | aktuelle ChatGPT-Codex-Session; Business/Privat-Zuordnung unbekannt | bisheriges Sitzungslabel ID-03; kanonische Zuordnung offen | Drive WORK: READ/CREATE/UPDATE+Readback in dieser Sitzung belegt | READ belegt; Write separat protokollieren | NOT_TESTED | Bootstrap-Regeln + FRONT/LOG aus vorigem Run |
Die Account-Aliase sind neue Vorschläge, keine entdeckten kanonischen IDs. Andere Accounts können aus dieser Session nicht impersoniert oder überprüft werden.
## 4. Pflichtumfrage als WorkOrder WO-REG-CAP-001
Status: PREPARED_IN_SHARED_FOLDER. Empfänger: jede tatsächlich beteiligte Account-/Runtime-Instanz. Zustellung und ACK pro Instanz sind derzeit NOT_CONFIRMED. Keine E-Mail oder externe Nachricht versandt.
Jede Instanz beantwortet in eigener neuer Raw-MD-Datei:
1. Behauptete Rollen-ID, deren Quelllink/Version und tatsächliche Rolle.
2. Provider, Account-Alias, Workspace/Tenant, Client/Runtime, Modellkennung; UNKNOWN statt Modellraten.
3. Direkt verfügbare Tools mit Namen und erlaubten Zielen; installierter Connector allein ist kein Zugriffsbeweis.
4. Kann sie WORK/_FRONT.md und die geltende Regel tatsächlich lesen? Datei-ID, gelesene Version/Hash, Zeit und ACK liefern.
5. Kann sie einen neuen Raw-Markdown-Testbericht im Registrierungsordner erzeugen, wieder lesen und UTF-8/Hash vergleichen? Vorhandene Dateien nicht überschreiben.
6. GitHub: Lesen / Branch-Write / PR-Erstellung / Merge jeweils separat. Schreibtests nur im ausdrücklich freigegebenen Testziel, niemals Test-Merge auf main.
7. Ace: Graph-/Workspace-ID und harmlose Leseprobe. Schreibtest nur im freigegebenen Testgraph. Graphsichtbarkeit prüfen; keine privaten Inventare in öffentliche Graphen schreiben.
8. Fallback: direkter MD-Zugriff, autorisierter Broker oder kein Transport. Privilegien und Herkunft bleiben sichtbar.
9. Kompetenz-Tags mit Benchmark/Testreferenz: coding, architecture, governance_review, innovation_architecture, long_context, multimodal, data_analysis, web_research usw. Selbsteinschätzung separat markieren.
10. Aktuelle freie Slots, gemeldete Quota/Budget, Parallelitätsgrenze, zuletzt geprüft und expires_at; wenn nicht abrufbar UNKNOWN. Abonnement != belegte freie API-Kapazität.
Antwortschema: role_claim, role_source, account_alias, provider, model_id, instance_id, client, tools[], capability_tests[], competence_evidence[], availability, restrictions[], fallback, ack_policy_ref, timestamp.
Datei: YY_MM_DD_HH_mm_<tatsaechliche-ID-oder-UNASSIGNED>_CAPABILITY-RESPONSE_vX.Y.Z.md.
Abnahme: Quellen- und Zielidentität, beobachtete Operation, Ergebnis, Datei-/Run-ID und Testzeit; erst dann VERIFIED. Rollenmapping benötigt zusätzlich ID01-Entscheidung.
## 5. Technische Zulassung und Abschluss
START_GATE prüft auf Serverseite:
- Rollen-/Account-/Runtime-Zuordnung gültig oder für den engen Auftrag ausdrücklich provisorisch erlaubt.
- Aktuelle Policy-/Front-Version an Run gebunden; Read-Receipt/ACK gespeichert. Das belegt Abruf, nicht vollständiges Verständnis.
- Für benötigte Aktion existiert frischer Ziel-/Scope-bezogener Capability-Test.
- Datenklasse, Freigabe, Budget und Worker-Lease gültig.
Scheitert eine Bedingung: BLOCKED oder begrenzte Beraterrolle. Keine produktiven Seiteneffekte über den Dispatcher.
COMPLETION_GATE: Resultat und Raw-MD-Bericht gespeichert → Readback/Hash → Log → Front → Pflichtprüfungen. Erst dann COMPLETED. Vertragsrelease verlangt weiterhin drei unabhängige Stellungnahmen, DELTA, erneute Prüfung und Human Gate.
Clientseitige Custom Instructions/AGENTS.md sind zusätzliche Anleitung. Technische Erzwingung entsteht nur, wenn privilegierte Schreib-/Release-Tools ausschließlich durch das Gate erreichbar sind. Diese Gates sind hier spezifiziert, nicht implementiert.
## 6. Gemeinsamer Transport statt identischer Rechte
Nicht jede Instanz benötigt GitHub-Schreibrechte. Empfohlener Weg: Agent liefert MD-Auftrag in autorisierte Inbox → Broker validiert Herkunft, Schema, Policy, Idempotenz und Ziel → eng berechtigter Writer legt Review-Branch/PR an → CI/Reviews/Human Gate → Receipt zurück nach Drive.
OneDrive kann ein Transportadapter sein, sofern Quelle, Empfänger, Hash, Richtung, Konfliktregel und tatsächlicher Scheduler nachgewiesen sind. Kein ungeprüfter Zwei-Wege-Sync; kein Versuch, Business-Policies durch den privaten Account zu umgehen.
Kein Zugriff auf Drive UND keinen Broker: Instanz bleibt unintegriert; manueller Export ist gekennzeichneter Workaround, kein automatischer Erfolg.
GitHub und Drive führen je Objekt genau einen Master. Dieses Dokument wird vorerst als Drive-Draft geführt; GitHub-Snapshot ist Review-Kopie mit Drive-ID und Hash. Nach Bearbeitung an einer Stelle muss Abgleich erfolgen; keine parallele Masterpflege.
## 7. Routing nach Bedarf und gemessener Eignung
1. WorkOrder in erforderliche Fähigkeiten, Datenklasse, Tools, Umfang und Abnahme übersetzen.
2. Kandidaten nach erlaubtem Zugriff, Capability-Test, Policy und Konfliktfreiheit filtern.
3. Frische Verfügbarkeitsdaten prüfen; UNKNOWN nicht als frei behandeln. Reserve/Lease vergeben, damit nicht zwei Dispatcher dieselbe freie Kapazität verplanen.
4. Unter zugelassenen Kandidaten task-spezifische Benchmarkqualität, Latenz, Kosten und Kontextbedarf vergleichen. Keine universelle Bestmodell-Rangliste und keine erfundenen Gewichte.
5. Kleinste geeignete Kombination auswählen; unabhängige Reviewer separat vom Autor und voneinander ausführen.
6. Tatsächliche Ergebnisse zurückmessen; Kompetenzprofile nur anhand belastbarer neuer Evidenz ändern.
Workload, Reasoning Effort und Datenanalyse sind auftragsabhängige Anforderungen. Verfügbarkeit/Quotas sind Laufzeitzustand, keine statischen Skill-Eigenschaften. Diese Routingautomatik ist noch NOT_IMPLEMENTED.
## 8. Troubleshooting-Liste
| Ticket | Symptom / Quelle | Status | Nächster Test |
|---|---|---|---|
| REG-TB-001 | GPT-1 Business hat Ace-Connector, Zugriff scheitert; Nutzerangabe | OPEN_NOT_REPRODUCED | im betroffenen Account exakten Toolaufruf, Zeitpunkt, Fehlercode, Workspace/Graph und App-Policy aufnehmen |
| REG-TB-002 | GPT-2 privat kann laut Nutzer Ace schreiben | USER_REPORTED_NOT_RETESTED | getrennte Testgraph-Probe mit sichtbarer Graph-ID und Receipt; nicht auf Business übertragen |
| REG-TB-003 | Gemini GitHub-Write unklar; OneDrive-Umweg berichtet | OPEN_NOT_REPRODUCED | Scheduler/Script/Allowlist/Commit und Rückreceipt nachweisen |
| REG-TB-004 | ID01/ID02/ID03 widersprüchlich benutzt | BLOCKS_CANONICAL_ROLE_MAPPING | gefundene Rollenquellen vergleichen; Human-Mapping entscheiden; keine automatische Umnummerierung |
| REG-TB-005 | Freie Tokens/Credits/Slots nicht durchgehend lesbar | OPEN | Telemetrie je Provider/Account testen; UNKNOWN + TTL verwenden |
| REG-TB-006 | Markdown-Regel allein erzwingt kein Read/Write | OPEN_IMPLEMENTATION | fehlendes Start-Receipt und fehlendes Abschlussartefakt im Dispatcher ablehnen |
Mögliche Ursachen von REG-TB-001 sind Prüf-Hypothesen, keine Diagnose: getrennte Account-Anmeldung, Workspace-Freigabe, Connector-Autorisierung, fehlende Graphberechtigung oder Toolverfügbarkeit. Keine dieser Ursachen ist aktuell nachgewiesen.
## 9. Pace Layers als NEXUS-Entwurf
Korrektur des Versprechers: langsame Layer ändern sich selten; schnelle häufig. Priorität P0 ist unabhängig von Änderungsgeschwindigkeit; Layers deshalb L0–L5 nennen.
| Layer | Inhalt | Änderung |
|---|---|---|
| L0 Grundlagen | Human Authority, Systemgrenzen, Evidenzgrundsatz | selten; begründete Entscheidung |
| L1 Verträge | ID-Namensräume, Schemas, Schnittstellen, Freigabevertrag | kontrolliert mit Migration |
| L2 Infrastruktur | Gateway, Auth, Speicher, Runtime, Scheduler | getestet mit Wiederherstellung |
| L3 Fähigkeiten | Skills, Adapter, Solvermodule, Kompetenznachweise | versioniert nach Tests |
| L4 Koordination | Routing, WorkOrders, Budgets, Reviewplanung | je Bedarf innerhalb L0–L3 |
| L5 Laufzeit | Sessions, Queues, Heartbeats, verfügbare Slots | häufig; mit TTL |
Das ist eine NEXUS-Übertragung, nicht Brands originale Sechserliste. Langsame Layer sind änderbar, aber mit höherer Prüfung; „Never Change“ wäre keine geeignete absolute Regel. Schnelle Experimente dürfen Grundregeln nicht selbst umschreiben.
Quelle: Stewart Brand / Long Now, https://longnow.org/ideas/pace-layers/ — schnelle Ebenen lernen, langsame bewahren und stabilisieren.
## 10. Quellen und ungelöste Autoritätsfragen
- Aktueller Nutzerauftrag: Accountprobleme und Modell-/Kompetenzmatrix; USER_REPORTED, keine Zugriffstests.
- WORK-Front: https://drive.google.com/file/d/11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH/view
- CPLM-Regeln: https://drive.google.com/file/d/1zzimyJXqId7VUwrASRN0AZizhgabngPL/view
- Governance-Entwurf: https://drive.google.com/file/d/1blTm4G9UKSXoxUR7yoJaKn3e_O-iz1Vz/view — REGISTRY_DRAFT; Human [1], A1–A12, GitHub-Mirror-Regel. Kein freigegebener aktueller Account-ID-Nachweis.
- Ältere ACL: https://drive.google.com/file/d/1u6yDzfdqDrKsCb_MYCkYeKBbfVCQTMhA/view — Funktionsrollen, keine aktuelle LLM-Account-ID-Matrix.
- Repo-Agentcontract: https://github.com/julianzotter/nexus-platform/blob/66bd013fa32b71b78ea10e3f39cecb6a218e9f60/development_cycle/agent_contracts.json — REVIEW_CANDIDATE; Human ID01, QA-Rolle ID03, actual_executor null.
- Sync-Sammlung: https://drive.google.com/file/d/17bJuKzj9sgRMu1bHIJRAHSAPKzSaugHi/view — mehrere Sollpfade/Repos; keine belastbare eindeutige aktive OneDrive→GitHub-Konfiguration.
- OneDrive-Konzept: https://drive.google.com/file/d/1IiX5KwoQYwcqUh_oQairusUOOPXMHTbC/view — Konzept- und Integrationsbeschreibung, kein hier beobachteter Schedulerlauf.
- Rollenportfolio https://drive.google.com/file/d/1TliLh3eUCX72xKGM93PaHkcOObeWBDTt/view ist ein Archetypen-/Kompetenzentwurf und keine aktuelle nummerierte Accountregistrierung.
## 11. Abnahme / Status dieses Auftrags
Vorbereitung einer getrennten Registrierungsablage, Umfrage und Troubleshooting: erstellt; Ablage/Hash/Readback separat im Run-Receipt belegen. Agentenantworten und Übernahme der Regeln: offen. Direkte Zustellung an andere Accounts: nicht ausgeführt. Broker und Start-/Completion-Gates: nicht implementiert. Kein produktives Routing und kein universelles Read/Write zugesichert.

