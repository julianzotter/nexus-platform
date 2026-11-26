---
name: NEXUS-AI-AEC-SYSTEMDOSSIER
version: 0.2.0-candidate
document_type: TECHNICAL_DOSSIER
status: REVIEW_PENDING
created_at: 2026-11-26T09:21:00+01:00
author_role: ID03
owner: ID01
language: de
canonical_destination_candidate: gdrive:1sNPiZgSOL2g-RQgOdVzBShWaF5sIlni2
operational_reporting: gdrive:1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP
registration_status: REGISTRATION_PENDING
human_gate: PENDING
source_evidence: live_drive_github_and_conversation
---
# NEXUS-AI AEC Engineering Knowledge Operations System
## Wissenschaftlich-technisches Dossier · Theorie · Architektur · Betrieb · Implementierung

**Lesestatus:** Konsolidierte, quellengebundene **Review-Fassung**. Beschriebene Zielarchitektur ≠ implementierter Dienst. `VERIFIED` bedeutet einen im angegebenen Lauf tatsächlich gelesenen/ausgeführten Teilnachweis, `SOURCE_REPORTED` eine historische Quellenangabe, `PROPOSED` eine Empfehlung und `BLOCKED` einen fehlenden kritischen Nachweis. Keine normative Bemessungsfreigabe, keine automatische Freigabe durch Modellkonsens.

## Abstract
NEXUS-AI ist ein deterministisch **geführtes** Human-AI-Engineering- und Knowledge-Operations-Framework für die AEC-Industrie, nicht ein klassisches Betriebssystem. Es koppelt (1) hierarchisch und quellengebunden verwaltetes Fachwissen, (2) deterministische Berechnung durch überprüfte Skripte/Fachsolver, (3) unabhängige Prüf- und Evidenzverfahren und (4) die Orchestrierung von Aufgaben, Rollen und Ergebnissen. Eine fünfte, übergreifende **Governance- und Persistenzachse** erzwingt nicht automatisch Wahrheit, sondern dokumentiert Herkunft, Verantwortlichkeit, Status und Grenzen. Das Systemziel ist nicht möglichst viel generierter Text, sondern die wiederholbare Lösung konkreter AEC-Use-Cases mit menschlicher Freigabe und maschinenprüfbaren Nachweisen. Das Dossier führt Problemstellung, Theorie, Taxonomie, Ablauf, Datenorte, Bedienung, Implementierung und Referenzquellen zusammen.

## Inhaltsverzeichnis
1. Problemstellung und Forschungs-/Entwicklungsfragen
2. Zielsystem, Geltungsbereich und Prioritäten
3. Terminologie und epistemische Grundlagen
4. Fachliche Ontologie und semantische Taxonomie
5. Architektur: vier funktionale Schichten und Governance
6. Steueralgorithmus und Zustandsmaschine
7. Datenarchitektur Google Drive / GitHub / Retrieval
8. Knowledge-Object- und Relationsmodell
9. Persönliche Baseline und ChatGPT-Konfiguration
10. Bedienung, Agent-Onboarding und User Manual
11. Engineering-Use-Cases und Beispielrouten
12. Implementierungs- und Migrationsguide
13. Verifikation, Qualität, Risiko und Abnahme
14. Betrieb, Reporting, Versionierung, Recovery
15. Diskussion, Limitationen und Roadmap
A. Nachgewiesene Drive-/GitHub-Hauptrouten
B. Open-Access-Web-Suchlink-Listen für drei priorisierte Use-Cases
C. Quellenregister, Versions- und Evidenzmatrix
D. Semantische Screenshot-Mapping-Inventur

## 1. Problemstellung und Forschungs-/Entwicklungsfragen
### 1.1 Ausgangslage
Ingenieurwissen ist verteilt auf Normen, nationale Anhänge, Richtlinien, Fachliteratur, Herstellerinformationen, eigene Rechenblätter, Projekte, E-Mails, Skripte und Modellarchive. LLMs sind für semantische Zuordnung und Texttransformation nützlich, aber keine belastbare alleinige Autorität für Normgeltung, Rechenrichtigkeit oder Freigabe. Parallel entwickelte Agenten, Skills und Datenbanken führen ohne Identitäts- und Versionsmodell zu Dubletten, Statusdrift und unbewiesener Synchronisation.
### 1.2 Leitfragen
- Wie lässt sich aus kurzer natürlicher Sprache eine reproduzierbare Folge `INTENT → DOMAIN → STANDARD → METHOD → SOLVER → REVIEW → ARTIFACT` ableiten?
- Wie werden technische Aussagen auf konkrete, zulässige Quellfassungen und Fundstellen zurückgeführt?
- Wie trennt man mathematisch deterministische Rechenkerne von probabilistischen LLM-Komponenten und menschlicher Entscheidung?
- Wie lassen sich persönliche Präferenzen nutzen, ohne Projektkennwerte oder historische Memory-Aussagen zu einer konkurrierenden technischen SSOT zu erheben?
- Wie wird der Nachweis eines realen End-to-End-Laufs von einer bloßen Architekturbehauptung unterschieden?
### 1.3 Hypothese und Messung
Ein regelbasiertes, quellengebundenes Routing mit geprüften Kernmodulen reduziert unbelegte Aussagen und Wiederholungsaufwand gegenüber freier LLM-Generierung. **Hypothese, kein Messergebnis.** Prüfgrößen: Source-Resolution-Rate, korrekte Domain-/Normzuordnung, Unit-PASS, Golden-Case-Übereinstimmung, Replay-Identität, echte End-to-End-Completion, Zeit bis zu nutzbarem Output, fehlende Registrierung, ungelöste Konflikte.

## 2. Zielsystem, Geltungsbereich und Prioritäten
### 2.1 Main Goals
`MG01 ENGINEERING_ACCURACY`, `MG02 KNOWLEDGE_SOVEREIGNTY`, `MG03 SYSTEM_RELIABILITY`, `MG04 WORKFLOW_AUTOMATION`, `MG05 RESOURCE_EFFICIENCY`, `MG06 CONTINUOUS_IMPROVEMENT`, `MG07 SUSTAINABLE_CONSTRUCTION`.
### 2.2 Fachliche Priorisierung aus dieser Sitzung
- **P1:** OIB-Richtlinie 1, mechanische Festigkeit und Standsicherheit; Beton-/Stahlbetonbau und Bauteilbemessung, insbesondere EN 1992 / ÖNORM B 1992; allgemeine Grundlagen EN 1990 und Einwirkungen EN 1991 samt österreichischen Anwendungsdokumenten.
- **P1 fachliche Ergänzung:** Holz-Beton-Verbund (HBV/TCC), CEN/TS 19103, EC5/ÖNORM B 1995, Kerven, Schubverbund, Gamma-/diskrete Methode, GZT/GZG und Schwingung.
- **P2:** OIB-Richtlinie 7, nachhaltige Nutzung natürlicher Ressourcen, Circular Construction, ReUse, LCA, EPD, ressourcenoptimierte Konstruktionen. EC3, BIM/IFC, Ausschreibung und Baubetrieb sind vernetzte Fachzweige.
Diese Priorisierung ist ein **Nutzerinteressen-Ranking**, keine gesetzliche Normenrangfolge. Normen und OIB-Fassungen gelten nur innerhalb ihres sachlichen, zeitlichen und territorialen Geltungsbereichs. Wiener Bauordnung, Bautechnikverordnung und jeweils umgesetzte OIB-Fassung sind vor Rechtsaussagen zu prüfen.
### 2.3 Systemische Priorität
`VERTICAL_FIRST` vor weiterer horizontaler Architektur; `LOOKUP_FIRST` vor Neuentwicklung; `SOURCE_FIRST` vor Normbehauptung; `HUMAN_GATE` vor fachlicher Freigabe. Ergebnis muss benutzbar, testbar und archiviert sein; reine Konzepte erhalten keinen Produktionsstatus.

## 3. Terminologie und epistemische Grundlagen
### 3.1 Begriffe
**SSOT** = kanonischer Ort einer definierten Objektklasse; **Source** = unveränderte Eingangsrepräsentation mit Locator/Hash; **Knowledge Object** = identifizierte semantische Einheit mit Provenienz; **Chunk** = Quellsegment mit stabiler Text-/Seitenposition; **Graph Edge** = typisierte, begründete Relation; **WorkOrder** = beauftragte, statusgeführte Arbeit; **Run** = nachweislich ausgeführte Instanz; **ACK** = echte Empfangs-/Übernahmebestätigung; **Review** = unabhängige fachliche Prüfung; **Release** = ausdrücklich freigegebene Version. `DRAFT`, `TESTED`, `REVIEWED`, `ADOPTED`, `RELEASED` sind nicht austauschbar.
### 3.2 Wissensautorität
Physikalische/mathematische Konsistenz ist zwingend; rechtlich verbindliche Regelungen und anwendbare Normen werden nach Geltung, Ausgabe, nationalem Anhang und projektspezifischer Vereinbarung geprüft. Peer-reviewed Papers und Praxisdaten dienen als Evidenz, nicht als Ersatz für rechtlich/normativ verbindliche Texte. Historische Manifest-Formeln wie „Physik > Norm > Technik > Paper > Praxis > LLM“ sind als **epistemische Prüfreihenfolge** zu lesen, nicht als automatische rechtliche Kollisionsnorm. LLM-Ausgaben sind Kandidaten, niemals Primärbelege.
### 3.3 Determinismus
Temperatur 0 garantiert weder deterministisches LLM-Verhalten noch Wahrheit. Reproduzierbarkeit verlangt versionierte Eingaben, Software-/Solverversion, Parameter, Rechenumgebung, Algorithmus, Prüftoleranz und einen Replay-Nachweis. Einheitenkonvention: Rechenkern N–mm–N/mm²; Benutzer-Ein-/Ausgabe kN, m, cm etc. mit dokumentierter Transformation. `ΣV=0`, `ΣM=0` sind notwendige Gleichgewichtschecks für passende statische Modelle, aber keine hinreichende Normprüfung.

## 4. Fachliche Ontologie und semantische Taxonomie
### 4.1 Kanonische fachliche Achse
`WISSENSCHAFT/TECHNIK → INGENIEURWISSENSCHAFTEN → BAUINGENIEURWESEN → KONSTRUKTIVER INGENIEURBAU → FACHANWENDUNG → BAUTEIL → WERKSTOFF/SYSTEM → NORMENFAMILIE → NATIONALER ANHANG → ABSCHNITT/TABELLE/GLEICHUNG → METHODE → NACHWEIS`.
Recht, OIB, Projekt, Methode, Tool, Quelle, Artefakt und Agent sind **orthogonale Relationen**, keine erzwungenen Unterordner der Fachachse. Die historische Entscheidung DEC-KG-TECHNIKACHSE (Ledger 0059, referenziert im Dossier 2026-10-26) ist maßgeblicher Prüfanker.
### 4.2 Hauptdomänen (Klassifikationsdimension)
`D01 GOVERNANCE`, `D02 KNOWLEDGE_MANAGEMENT`, `D03 RETRIEVAL`, `D04 QUALITY_ASSURANCE`, `D05 AI_ORCHESTRATION`, `D06 ENGINEERING_COMPUTE`, `D07 STRUCTURAL_ENGINEERING`, `D08 BUILDING_SCIENCE`, `D09 BUILDING_SYSTEMS`, `D10 CIRCULAR_CONSTRUCTION`, `D11 REGULATORY_COMPLIANCE`, `D12 PROCUREMENT`, `D13 PROJECT_MANAGEMENT`, `D14 DIGITAL_ENGINEERING`, `D15 SOFTWARE_ENGINEERING`, `D16 INFRASTRUCTURE`, `D17 VISUALIZATION`, `D18 RESEARCH`, `D19 KNOWLEDGE_TRANSFER`, `D20 BUSINESS_OPERATIONS`.
**Status:** vorgeschlagene semantische Sichten, nicht als neue Master-Registry ausrollen. Bestehende `KV-01…KV-20` sind Routing-Labels und bleiben identitätsstabil; die D-Codes sind keine Ersatz-IDs.
### 4.3 Object Types und Relationen
Objekttypen: `DOMAIN`, `SUBDOMAIN`, `CONCEPT`, `STANDARD`, `LEGAL_REQUIREMENT`, `MATERIAL`, `COMPONENT`, `LOAD`, `FORMULA`, `PARAMETER`, `METHOD`, `DESIGN_CHECK`, `USECASE`, `PROJECT`, `WORKFLOW`, `SKILL`, `AGENT`, `TOOL`, `SOURCE`, `CHUNK`, `EVIDENCE`, `ARTIFACT`, `WORKORDER`, `RUN`, `DECISION`, `FINDING`, `LESSON`, `STATUS`, `PERSON`, `ORGANIZATION`.
Relationen: `IS_A`, `HAS_CHILD`, `PART_OF`, `APPLIES_TO`, `GOVERNED_BY`, `REFERENCES`, `DERIVED_FROM`, `HAS_SOURCE_SPAN`, `USES_METHOD`, `REQUIRES`, `IMPLEMENTS`, `EXECUTED_BY`, `PRODUCES`, `VALIDATED_BY`, `SUPERSEDES`, `CONFLICTS_WITH`, `STORED_AT`, `SYNCED_TO`, `ADDRESSES`, `BELONGS_TO`. Jede fachliche Kante braucht Evidenz oder `REVIEW_PENDING`.
### 4.4 Trigger- und Alias-Normalisierung
`Durchstanzen / punching shear` → D07 Beton → EC2/ÖNORM B 1992 → Nachweis Durchstanzen. `Holzbetonverbund / timber-concrete composite / TCC / HBV` → D07 + D09 → CEN/TS 19103 → Verbindungssteifigkeit, Kerven, diskrete/γ-Methode. `OIB 1 / mechanische Festigkeit / Standsicherheit` → D11 + D07; `OIB 7 / Kreislaufwirtschaft / Materialpass / ReUse` → D11 + D10. Synonyme aktivieren **Kandidaten-Routen**, nicht automatisch konkrete Paragraphen oder Werte.
### 4.5 Konfliktregeln
Eine Ressource kann mehrere Domänen/Labels haben; genau eine stabile Identität und dokumentierte Herkunft. Gleichlautende Dateinamen sind kein Duplikatbeweis. `SAME_AS` nur nach Identitätsprüfung; `RELATED_TO` ist schwächer als `DERIVED_FROM`; `SYNCED_TO` nur mit nachgewiesenem Transport. Quelltext nie still korrigieren; Korrekturen als versionierte Ableitungen.

## 5. Architektur: vier funktionale Schichten und Governance
### 5.1 L1 Knowledge Layer
Quellenregister, Normbibliothek, MD-Volltext, JSON-Objekte, Graph-Relationen, Suchindizes und optional Vektorindex. Source Identity und Provenienz vor semantischer Anreicherung. Ingest: Quelle → Hash/Lizenz → Extraktion/OCR → Struktur → Formel-/Tabellenlokatoren → Kandidaten → QA → registrierte Objekte → Indexprojektionen.
### 5.2 L2 Compute Layer
Geprüfte Python-/Fachsolver, RFEM oder gleichwertige Rechenautoritäten, Symbolik, Matrixmethoden, FEM, Parametrik, Dimensionierung, Material- und Einheitenprüfungen. LLM darf Rechenweg vorschlagen und Ergebnisse erklären, nicht numerische Freigabe ersetzen. Solver-Adapter erhalten versionierte Input-/Output-Verträge.
### 5.3 L3 Verification and Peer Review Layer
Unabhängige Prüfungen von Normgeltung, Quellen, Datenqualität, Modellannahmen, Einheiten, Gleichgewicht, Vergleichsrechnungen, Reproduzierbarkeit, Grenzzuständen und Sicherheitsanforderungen. Unterschiedliche Agentenrollen allein begründen keine unabhängigen Runtime-Instanzen. Kritische Befunde → `BLOCKED/REVIEW_REQUIRED` mit Evidenz.
### 5.4 L4 Orchestration and Interaction Layer
Input-Adapter für Voice/Chat/Dokumente; Intent-Parser, MoE-Router, WorkOrder-FSM, Skill-Auswahl, Fortschrittsstatus, Dashboard, Reports, menschliche Freigabe. Kosten-/Token-/Zeitbudget und Stopbedingungen sind explizit.
### 5.5 Querschnitt: Governance/Persistenz
Manifest, Baseline, AGBs, Rollenmatrix, Registry, WORK, History, Checksum, Status, ACL und Release-Entscheidungen wirken über alle vier Ebenen. **Architekturkorrektur:** Der aktuelle ID06-Diktatentwurf v0.1.0 ließ die vierte Ebene offen; die hier gewählte Wissensschicht ist durch das ältere Manifest und die explizite heutige ID01-Klärung begründet. Governance/Human Gate sind keine ersetzte Wissensschicht, sondern übergreifende Steuerung.

## 6. Steueralgorithmus und Zustandsmaschine
### 6.1 Normativer Betriebsvertrag (Zielzustand)
`BOOTSTRAP → INPUT → INTENT → SOURCE_RESOLUTION → PLAN → HUMAN_GATE_IF_NEEDED → RETRIEVE → EXECUTE_SOLVER_IF_REQUIRED → VERIFY → INDEPENDENT_REVIEW_IF_REQUIRED → ARCHIVE → REGISTER → REPORT → HUMAN_RELEASE`.
Jeder Übergang hat `preconditions`, `evidence`, `run_id`, `owner`, `failure_state`. `PUBLISH` ≠ `ACK` ≠ `REVIEW` ≠ `RELEASE`.
### 6.2 Schrittweise Regeln
1. **Bootstrap:** aktuelle kanonische MD-Regeln lesen; tatsächliche Rollen-ID, Provider, Runtime, Modell und getrennte Read/Write-Capabilities protokollieren. Fehlender Zugriff → `BOOTSTRAP_BLOCKED` für betroffenen kritischen Schritt.
2. **Request Contract:** `scope`, `intent`, `main_goal`, `deliverables`, `constraints`, `source_requirements`, `risk_class`, `budget`, `human_gate` erfassen; nur essentielle Rückfragen.
3. **Reuse Check:** vorhandene WorkOrders, Register, Fachobjekte, Skills, Solver, Manuals und Indexe nachschlagen. Keine konkurrierende SSOT erzeugen.
4. **Route:** `DOMAIN → SUBDOMAIN → USECASE → STANDARD → METHOD → WORKFLOW → SKILL/TOOL` unter Berücksichtigung von Geltungsbereich und verfügbarem Quelltext.
5. **Compute:** mathematisches Modell, Eingaben, Einheiten und Randbedingungen prüfen; deterministischen Solver ausführen; Rohoutput mit Code-/Input-Hash archivieren.
6. **QA:** Source Locator, Einheit, Gleichgewicht, Material, Normstand, Benchmarks, Grenzzustände; unabhängigen Review bei kritischem Scope einholen.
7. **Writeback:** Artefakt speichern, Datei-ID ermitteln, Readback/Hash, Registry (append-only), WORK-Report und Status aktualisieren; GitHub-Snapshot nur mit nachvollziehbarem Commit.
8. **Closure:** Done-Kriterien gegen Evidenz prüfen. Bei offenen Punkten `PARTIAL`, `REVIEW_PENDING` oder `BLOCKED` statt `DONE`.
### 6.3 Pseudocode
```text
on_request(q):
  governance = read_canonical_rules()
  if not governance.available: return BOOTSTRAP_BLOCKED
  contract = parse_and_validate(q)
  reuse = lookup_existing_assets(contract)
  sources = resolve_sources_and_legal_scope(contract)
  route = classify_and_route(contract, reuse, sources)
  if route.requires_norm and not sources.verified: return SOURCE_BLOCKED
  plan = select_versioned_workflow(route)
  result = execute_verified_tool(plan) if plan.needs_compute else synthesize_evidence(sources)
  qa = validate(result, contract, sources)
  if qa.critical_fail: return REVIEW_REQUIRED
  review = independent_review_if_required(result, qa)
  artifact = persist_with_readback(result, qa, review)
  registration = append_existing_registry(artifact)
  report = append_work_status(artifact, registration)
  return status_with_evidence(report, human_gate_state)
```
### 6.4 Fehlerbehandlung
Idempotenzschlüssel aus Quellidentität, Version, Auftrag und Scope; `retry` begrenzt; keine stille Korrektur an fremden Quellen; keine automatische Übernahme nicht registrierter Normdaten; `UNKNOWN` bleibt `UNKNOWN`. Doppelübernahme kann toleriert werden, solange sie als gleicher Vorgang erkannt wird; divergierende Bytes/IDs sind ein Konflikt.

## 7. Datenarchitektur Google Drive / GitHub / Retrieval
### 7.1 Verantwortlichkeit
Google Drive ist **Dokument-/WORK-SSOT**; GitHub `julianzotter/nexus-platform` dient als **Code-, Test-, Review- und Snapshot-Repository**. Die Existenz eines Mirrors ist kein Beweis eines bidirektionalen Sync. Revisions-/Backupstrategie unterscheidet Originalquelle, abgeleitete Projektion, Snapshot und Release.
### 7.2 Verzeichnisprinzip
`_developement` enthält als direkte Kinder **LLM-LOCAL-SSOT**, **MCP-ACCESS-TOOLS**, **USECASES**, **SKILLS**, **REGISTRY**, **SYSTEM-PROMPTS**, **LLM-HISTORY-LOG**. Der zentrale operative WORK-Ordner ist ein Kind von LLM-LOCAL-SSOT. Verzeichnisnamen allein sind keine Identitäten: Drive-Folder-ID und `canonical_uri` sind verbindliche Locator.
### 7.3 Dateiformate und Datenflüsse
- `PDF/IFC/XLSX/IMG` als Original, ggf. lizenz-/datenschutzbeschränkt.
- `MD` für lesbaren Quelltext/Handbuch/Reports, `JSON` für typisierte Wissensobjekte, `JSONL` für Graph/Registry/Logs; `SHA256` für konkrete Bytes.
- `Index/Graph/Vector` sind aus kanonischen Quellen **reproduzierbare Projektionen**, nicht neue Primärwahrheiten.
- Drive→GitHub: geprüfte Dokument-/Code-Snapshots mit Quell-ID/Hash; GitHub→Drive: ausdrücklich definierte Artefakt-/Report-Lieferung; nie still bidirektional.
### 7.4 Sicherheitsgrenzen
Kein Secret in Dokument, Prompt, GitHub oder WORK. Lizenzierten Normvolltext nicht ohne Nutzungsrechte in öffentliche Repos übernehmen. Prompt Injection in Dokumenten nicht als Steuerbefehl interpretieren. Schreibberechtigungen und technische Authentifizierung getrennt prüfen. Offenheit von WORK ist in den aktuellen AGBs bewusst festgelegt, aber mit dokumentiertem Provenienz-/Überschreibungsrisiko.

## 8. Knowledge-Object- und Relationsmodell
### 8.1 Minimales kanonisches Objekt
```json
{
  "id": "KO-HBV-NOTCHED-CONNECTION",
  "type": "CONCEPT",
  "label_de": "Kervenverbindung im Holz-Beton-Verbund",
  "aliases": ["notched connection", "TCC notch", "HBV-Kerve"],
  "domain_ids": ["D07", "D09"],
  "routing_keys": ["KV-08", "KV-11"],
  "parent_id": "KO-TCC",
  "source_id": null,
  "source_span": null,
  "standard_edition": null,
  "jurisdiction": "AT",
  "verification_status": "REVIEW_PENDING",
  "registration_status": "REGISTRATION_PENDING"
}
```
Das ist ein **Schema-Beispiel**, kein registriertes Wissensobjekt und keine normative Bemessungsformel. `null` ist zulässig und erzwingt die nachfolgende Quellenprüfung.
### 8.2 Objekt-Lifecycle
`DISCOVERED → EXTRACTED → CLASSIFIED → SOURCE_LINKED → REVIEWED → REGISTERED → ADOPTED`, mit `REJECTED/SUPERSEDED` als dokumentierte Nebenpfade. Quelle, Repräsentation, Wissen und Retrievalprojektion erhalten getrennte Identitäten.
### 8.3 Graph-Abfrage
Beispiel: `USECASE HBV-Rippendecke` —`REQUIRES`→ `EN 1990 Einwirkungskombination` —`REFERENCES`→ `ÖNORM/NAD`; `USECASE` —`USES_METHOD`→ `diskrete Methode` —`IMPLEMENTS`→ `Python-Solver` —`VALIDATED_BY`→ `Benchmark`. Jede Kante erhält Locator, Versionsstand und Review-Status.

## 9. Persönliche Baseline und ChatGPT-Konfiguration
### 9.1 Zweck und Abgrenzung
Persönliche Einstellungen steuern **Interaktion und Präferenzen**; sie ersetzen weder Governance noch Fachnormen, Projektakten oder Live-Status. Das Profil wird nur nach expliziter Nutzerprüfung als dauerhaftes Memory-Summary übernommen. Projektkennwerte bleiben im jeweiligen Projekt/SSOT; historische Memory-Screenshots sind Quellenkandidaten, keine autoritativen Statusbelege.
### 9.2 Destilliertes Profil (Kandidat)
**Rolle:** Tragwerksplaner, Structural Designer und AI-/Prompt-Engineering-Systementwickler, AEC-Schwerpunkt Österreich. **Fachprofil:** Beton/Stahlbeton, OIB-RL1, EC2/ÖNORM B1992; HBV/TCC CEN/TS19103, EC5/ÖNORM B1995, Einwirkungen EN1990/1991; OIB-RL7, Low-Carbon, ReUse, Holz-Hybrid, BIM, Vorfertigung. **Arbeitsstil:** präzise, knapp, quellennah, auditierbar; mathematisch korrekt; `LOOKUP_FIRST`, `VERTICAL_FIRST`, `REUSE_FIRST`, `NO_UNVERIFIED_SUCCESS`; Solverautorität, Einheitencheck, Peer-Review und Human Gate. **Ziel:** personalisiertes NEXUS-AI-Routing aus kurzen Intents, robuste Wissensvernetzung, automatisierbare prüfbare Workflows, mehr Zeit für Entwurf und kritisches Denken. **Kommunikation:** Deutsch, TL;DR zuerst, Details auf Abruf; keine Floskeln, keine erfundenen Status-/Quellenangaben.
### 9.3 Account-Konfiguration
ChatGPT-Personalization: User Profile und Custom Instructions für kurze stabile Präferenzen; Memory Summary für langlebige Kontextsignale; Projekte für scoped context; Work/Plugins für längere Tool-Ausführung; NEXUS-SSOT für versionierte Fakten, Normen und WorkOrders. Kein API-Parameter wie `top_p`, `top_k` oder `temperature` ist durch bloße Personal Instructions garantiert einstellbar; diese sind runtime-/API-spezifisch. Frühere Memory-Aussagen `top_p=0.03` und ID06-Diktat `top_p=1` sind **nicht** als globale Hardrule zu harmonisieren: pro Provider explizite Parameter und reproduzierbare Tests.
### 9.4 Bereinigungsvorschlag
`KEEP`: Fachschwerpunkte, Antwortstil, Qualitätsprinzipien, Systemziele. `MOVE_TO_NEXUS`: konkrete Projekte, Normkennwerte, Geräte, APIs, Templates, Ledger, Modellversionen. `ARCHIVE`: historische Entscheidungen/Fehlerberichte. `REVIEW`: Widersprüche, private/zeitgebundene Details. Keine automatische Löschung der ChatGPT-Memory; Änderung durch Nutzer in Einstellungen → Personalisierung → Memory summary → Manage und ggf. Ursprungsquellen.

## 10. Bedienung, Agent-Onboarding und User Manual
### 10.1 Schnellstart
1. Kanonische AGB, Manifest, Baseline, WORK/Folder.md lesen; `START_ACK` mit Runtime, Rolle, Modell, Zugriff, Zeit und Auftrag erstellen.
2. Nutzeranfrage auf `MAINGOAL`, `INTENT`, `DOMAIN`, `DELIVERABLE`, `EVIDENCE` normalisieren.
3. Vorhandene Registry/Skills/Quellen suchen, Route bestätigen, ausführbaren Workflow starten.
4. Ergebnis mit echten Prüfbelegen, Hash und Status zurückgeben; WORK-Report/Registrierung nach Freigabevertrag.
### 10.2 Ergonomische Trigger (Semantik, nicht magische Befehle)
`#NEXUS-START` Bootstrap; `#KURZ` TL;DR; `#QUELLE` Quellen-/Versionscheck; `#PEER-REVIEW` unabhängige Prüfung beauftragen; `#TRUE-RUN` echte Ausführung mit Beleg; `#WORKORDER` Auftrag übernehmen; `#REGISTRY` vorhandene Objekte nachschlagen; `#OIB1` Tragwerks-/Standsicherheitsrouting; `#OIB7` Ressourcen-/LCA-Routing; `#HBV` TCC-Workflow; `#STATUS` belegte Completion-Matrix. Wirkung nur, wenn die jeweilige Runtime/Orchestrierung den Trigger tatsächlich implementiert.
### 10.3 Agent-Bootstrap-Contract
`agent_role_id`, `provider`, `model_id`, `runtime_instance`, `read_capabilities`, `write_capabilities`, `governance_version`, `workorder_id`, `run_id`, `source_refs`, `constraints`, `output_contract`, `stop_conditions`. Unbekannte Felder `null`; keine Rolle aus Selbstaussage ableiten.
### 10.4 Menschliche Bedienung
Kurze Anfrage genügt für eine Kandidatenroute. Bei fehlender Geometrie, Normfassung oder Einwirkung darf ein System keine belastbare Bemessung behaupten. Ein Statusbericht soll stets zwischen `Datei erzeugt`, `gespeichert`, `registriert`, `unabhängig geprüft`, `freigegeben` und `produktiv` unterscheiden.

## 11. Engineering-Use-Cases und Beispielrouten
### UC-01: Betonbauteilbemessung und OIB-RL1
**Input:** Bauteiltyp, Geometrie, Lagerung, Material, Lastfälle, Einwirkungskombinationen, Nutzung, Standort, Normfassungen. **Route:** D11 OIB1 → D07 Beton → EN1990/1991/1992 + ÖNORM/NAD → Biegung/Querkraft/Durchstanzen/Bewehrung/GZT/GZG → verifizierter Solver → unabhängiger Check. **Output:** Eingabeprotokoll, Gleichungen mit Fundstellen, Einheiten, Auslastungen, Rechenbericht, Prüfstatus. **Fail:** fehlende Normfassung oder Lastgrundlagen → keine Freigabe.
### UC-02: Holz-Beton-Verbund-Rippendecke
**Input:** Holz-/Betonquerschnitt, Kervenabstände/Steifigkeiten, L_eff, Lasten, Material-/Kriechparameter, Brand/Schwingung. **Route:** D07/D09 HBV → EC5 + CEN/TS19103 + EC2/EN1990/1991 → diskrete Methode und Vergleich γ/FEM → ULS/SLS/Schwingung/Brand. **Output:** Kervenkräfte, Schnittgrößen, Durchbiegung, Schwingungsprüfung, Benchmark-Differenzen und Evidenz. Historische Eisteiche-Zahlen sind **keine** allgemeingültigen Bemessungsparameter.
### UC-03: OIB-RL7 und Circular Construction
**Input:** Bauteilliste, Mengen, Lebenszyklusmodule, Materialherkunft, EPDs, Rückbau-/ReUse-Szenarien, Geltungsbereich. **Route:** D10/D11 → OIB7, EN15804/EN15978 soweit anwendbar → EPD/ÖKOBAUDAT/IBO und ReUse-Kataloge → LCA-/Ressourceneffizienz-Tool → Vergleich. **Output:** nachvollziehbare Mengen-/Emissions-/Materialbilanz, Szenarien, Quellen, Unsicherheiten, rechtliche Abgrenzung.
### 11.4 Querschnittsanwendungen
IFC/BIM-Mapping; FT-Träger- und LV-Prüfung; OIB-/Baurechts-Check; Baustoff-ReUse-Katalog; Dokumenten-/Excel-Parsing; Normenbibliothekar; parametrisierte CAD-/FEM-Generierung; Wissensdashboard; Office/Reporting. Diese sind im Taxonomiegraphen vernetzt, aber nicht automatisch gleich priorisiert.

## 12. Implementierungs- und Migrationsguide
### 12.1 Phase 0: Quellen-/Governance-Gate
Kanonische MD-Versionen, aktuelle Drive-IDs, WORK-Folder, GitHub-Commit/PR, Ledger und Registries lesen. Abweichungen dokumentieren, nicht still überschreiben.
### 12.2 Phase 1: Datenidentität und Taxonomie
Bestehende Registry erweitern, keine Parallelregistry. Source→Representation→Object→Relation, normierte Labels/Aliases, Parent-Child-Graph, Provenienz und Prüffelder. Validierung: Eindeutigkeit, auflösbare Parent-IDs, kein zyklischer `HAS_CHILD`-Pfad, Quell-Locator und Hash.
### 12.3 Phase 2: Drei Golden Slices
Je UC-01/02/03 ein vollständiger, kleiner, rechtlich zulässiger, fachlich geprüfter End-to-End-Test mit eingefrorenem Input, Quellen, Solver-/Analyseoutput, QA, Readback, Registry, Bericht, menschlicher Abnahme. Erst dann mehr Agenten/Plugins.
### 12.4 Phase 3: Operative Integration
Versionierte Workflow-/Skill-Registry; getrennte Read/Write-Capability-Checks; WORK-ACK und Status; GitHub-Review-Snapshot auf Branch/PR; CI-Tests; kontrollierter Wiederanlauf. OAuth-Fehler und Konflikte nicht durch behaupteten Sync überdecken.
### 12.5 Phase 4: Nutzer-/Agenten-Onboarding
Masterdossier als Referenz; daraus Kurz-User-Manual und maschinenlesbares Agent-Bootstrap-Contract **ableiten**, nicht drei unabhängige Wahrheiten. Änderungen an Governance nur über dafür autorisierte Versionierung.

## 13. Verifikation, Qualität, Risiko und Abnahme
### 13.1 Akzeptanzmatrix
| Gate | Test | PASS nur wenn |
|---|---|---|
| G01 Bootstrap | Live-Regeln gelesen | Drive-ID, Version, Zeit, Runtime belegt |
| G02 Identität | Quelle/Objekt | eindeutige IDs, Quellhash, Locator |
| G03 Semantik | Fachrouting | erwartete Labels und Normkandidaten im Golden Set |
| G04 Norm | Geltung | Ausgabe, NA, Ort, Datum und Rechte belegt |
| G05 Compute | Solver | deterministische Ausführung + Einheiten + Benchmarks |
| G06 Review | Unabhängigkeit | andere tatsächliche Instanz/Reviewer mit Beleg |
| G07 Persistenz | Save/Readback | Drive-ID, Rohbytes und SHA256 identisch |
| G08 Registry | Append | kanonische Registry aktualisiert und gelesen |
| G09 Transport | GitHub | Branch/Commit/PR/SHA, Quellbezug |
| G10 Release | ID01 | dokumentierte Freigabe und Scope |
### 13.2 Risiken
(1) Fehlende/alte Normfassungen; (2) Halluzination trotz scheinbarer Zitate; (3) stille Einheiten- oder Lastfallverwechslung; (4) falsche Agentenidentität; (5) ungeprüfter OAuth/Sync; (6) ungesicherte Mehrschreiber-Konflikte; (7) Memory als technische Primärquelle; (8) Scope Creep und ausbleibende E2E-Abnahme; (9) Secrets in historischen Uploads; (10) falsche Produktionsreife durch Dokumentpräsenz. Gegenmaßnahmen: Fail-Closed am kritischen Schritt, Evidence Contract, getrennte Zustandsachsen, Secrets-Rotation, vertikale Piloten.

## 14. Betrieb, Reporting, Versionierung, Recovery
### 14.1 Reporting Contract
`STATUS | CHANGED | TESTS | SOURCES | ARTIFACTS | RISKS_GAPS | NEXT_ACTION | QA_STATUS | LOG`. Frontmatter mit Timestamp (Europe/Vienna), Rolle, Run-ID, Ticket, Version und Quellverweisen. Dateinamensschema nach aktueller AGB/WORK-Regel; Ledgernummer **nicht erfinden**.
### 14.2 Archivierung
Fachartefakt im autorisierten Use-Case-Ziel; operativer Nachweis in WORK; Maintenance-Logs im LLM-HISTORY-LOG; GitHub-Snapshot als überprüfbare Version. Drei Aktionen nicht gleichsetzen: Upload, Hash-Readback, Registry-Eintrag. Bei nicht möglichem Byte-Readback `WRITTEN_UNVERIFIED`.
### 14.3 Recovery
Letzte registrierte Version mit Quell-ID und SHA wählen; Snapshot getrennt wiederherstellen; Vergleichstest; keine automatische Überschreibung; Statusbericht mit verbleibenden Abweichungen.

## 15. Diskussion, Limitationen und Roadmap
Die Vier-Schichten-Architektur ist ein methodisches Modell; tatsächliche Agenten, APIs und Solver sind je Runtime unterschiedlich verfügbar. Knowledge Graph, bidirektionale Synchronisation und „selbstlernende“ Routinen sind nur dort implementiert, wo Quellcode, Tests, echte Ausführung und Adoption belegt sind. `Temperature=0` und Peer-Konsens sind keine Beweise. Das Zielbild bleibt ein persönlich zugeschnittenes, reproduzierbares Engineering-System mit eng definierten Autoritätsgrenzen. **Nächster fachlicher Meilenstein:** UC-01 Beton/OIB1 mit vollständig belegtem Golden Slice; anschließend UC-02 HBV und UC-03 OIB7. Das Dossier ist erst nach ID01-Review, Registry, Readback und optionalem unabhängigem Review ein freigegebenes Handbuch.

## Anhang A. Nachgewiesene Drive-/GitHub-Hauptrouten
| Bereich | Rolle | Locator | Evidenzstand |
|---|---|---|---|
| `_developement` | gemeinsame Hauptablage | https://drive.google.com/drive/folders/1OIyJI6rljIi8zNsT-iwg47NsuguoZqTB | LIVE_LISTED 2026-11-26 |
| `LLM-LOCAL-SSOT` | kanonische Dokument-/Governance-Ablage | https://drive.google.com/drive/folders/1j3FLJkWpQv6xGA_KO0D9sMyA11f0vxBV | LIVE_LISTED |
| `WORK` | Aufträge, ACK, Artefakte, Status | https://drive.google.com/drive/folders/1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP | LIVE_LISTED |
| `USECASES` | Fachanwendungen / Dokumentation | https://drive.google.com/drive/folders/1sNPiZgSOL2g-RQgOdVzBShWaF5sIlni2 | LIVE_LISTED; direkt unter `_developement` |
| `MCP-ACCESS-TOOLS` | Connector-/Tool-Assets | https://drive.google.com/drive/folders/1fRa7rQvKi-BkhVIzjXPcY_u8iIJ4Vn5J | LIVE_LISTED |
| `SKILLS` | Skills-Assets | https://drive.google.com/drive/folders/1yai_XOq-RiV_9JPl7LaS6AtPjKio9rsb | LIVE_LISTED |
| `REGISTRY` | Registry-Ordner | https://drive.google.com/drive/folders/10nI9Z9MOmN4z1Ji0cXM1fPw8ND1Y7j3V | LIVE_LISTED |
| `SYSTEM-PROMPTS` | Prompt-Bibliothek | https://drive.google.com/drive/folders/1aeL3p1fuFjOcQ1VrOVTs7LcaJxGZz-ci | LIVE_LISTED |
| `LLM-HISTORY-LOG` | Historienordner unter `_developement` | https://drive.google.com/drive/folders/1IbVFNxTWSRrX10GQpxxwr3rUyF6U4jud | LIVE_LISTED; **abweichend** vom AGB-Verweis 1uavEf5g_ZisiEMsksrGi_KYzMsx37DWc, Identität prüfen |
| `_AGBS.md` | operative Steuerdatei | https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view | LIVE_FETCH; Frontmatter v007.2, Aktivierungsnachweis widersprüchlich |
| `Manifest` | Rollen/Governance | https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view | LIVE_FETCH, NEXUS-ROLES-v1.2 |
| `Baseline` | MUST-Regeln | https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view | LIVE_FETCH |
| `WORK/Folder.md` | WORK-Policy | https://drive.google.com/file/d/1nDjF78dq3l8PGpXsauzBz1bzHescDSwv/view | LIVE_FETCH, v0.4.0-pilot |
| `file-registry.jsonl` | kanonische File-Registry | https://drive.google.com/file/d/15m8T5cWbogIup9snzFwiB1g9HqNCoGow/view | früherer TRUE RUN: 472 parsebare Einträge |
| `nexus-platform` | Code/Tests/Review-Snapshots | https://github.com/julianzotter/nexus-platform | GitHub-Suche; Branch-Stand separat zu fixieren |
| `Systemdossier 2026-10-26` | Vorgängerdossier | https://drive.google.com/file/d/1sOFYGijEDvNITEPfZihe6jlCUK69X06Q/view | LIVE_FETCH, v1.0.0 REVIEW |
| `User Manual 2026-11-26` | Diktat/Bedienungsentwurf | https://drive.google.com/file/d/1A4TEKgDfO2gnznzaVfPr6vt1BE-qnZTA/view | LIVE_FETCH, v0.1.0 DRAFT |

**Wichtig:** Die Ordnerliste ist ein nachgewiesener **Hauptachsen-Ausschnitt**, keine vollständige rekursive Inventur. Der doppelte HISTORY-LOG-Locator und die widersprüchliche AGB-Aktivierungsmetadatenlage werden nicht still harmonisiert.

## Anhang B. Priorisierte Open-Access-Web-Suchlink-Listen
**Methodik:** Reihenfolge je Frage neu bestimmen: (1) verbindliche/offizielle Regel- und Primärquellen, (2) fachliche Peer-Review-/Hochschulquellen, (3) verifizierte Fach-/Materialdaten, (4) offene Implementierungsbeispiele. `öffentlich erreichbar` bedeutet nicht automatisch `Open Access` im Sinne lizenzfrei wiederverwendbaren Volltexts. Die URLs sind **Quellenkandidaten aus den vorliegenden Referenzen**, nicht in diesem Lauf einzeln per HTTP auf Verfügbarkeit/Lizenz geprüft.
### B1. UC-01 Tragwerksplanung / Beton / HBV / OIB-RL1
| Rang | Quelle | URL | Funktion |
|---|---|---|---|
| 1 | OIB | https://www.oib.or.at | OIB-Richtlinien/Leitfäden; Ausgabe und Landesumsetzung prüfen |
| 2 | Austrian Standards | https://www.austrian-standards.at | ÖNORM-Katalog, Geltungs-/Ausgabeermittlung; Volltexte oft lizenziert |
| 3 | JRC Eurocodes | https://eurocodes.jrc.ec.europa.eu | offizielle Eurocode-Informationen, Handbooks, Worked Examples |
| 4 | TU Wien Repositum | https://repositum.tuwien.at | Dissertationen, Methoden, Prüfberichte |
| 5 | TU Graz Open Access | https://graz.pure.elsevier.com | Forschung zu Tragwerken/HBV/Materialien |
| 6 | OpenAlex | https://openalex.org | DOI-/Literatur-Metadaten, Zitationsnetz |
| 7 | Semantic Scholar | https://www.semanticscholar.org/product/api | Paper- und Zitationssuche |
| 8 | arXiv | https://arxiv.org | frei verfügbare Preprints, nicht generell peer-reviewed |
| 9 | Dlubal Dokumentation | https://www.dlubal.com | Fachsolver-/RFEM-Dokumentation; Herstellerquelle |
| 10 | dataholz | https://www.dataholz.eu | geprüfte Holzbauteil- und Bauteildaten; Geltung prüfen |
**Queries:** `ÖNORM B 1992-1-1 Durchstanzen österreichischer NA`; `CEN/TS 19103 timber concrete composite notched connection stiffness`; `OIB Richtlinie 1 Tragwerk Österreich Ausgabe`; `TCC ribbed slab vibration discrete method benchmark`.
### B2. UC-03 OIB-RL7 / Circular Construction / Materialdaten
| Rang | Quelle | URL | Funktion |
|---|---|---|---|
| 1 | OIB | https://www.oib.or.at | Richtlinie 7, Ausgabe, rechtlicher Kontext |
| 2 | EU-Kommission EU-Taxonomie | https://finance.ec.europa.eu/sustainable-finance/tools-and-standards/eu-taxonomy-sustainable-activities_en | amtliche Nachhaltigkeitskriterien |
| 3 | ÖKOBAUDAT | https://www.oekobaudat.de | LCA-/EPD-Datensätze, Versions-/Lizenzprüfung |
| 4 | IBO | https://www.ibo.at | österreichische Bauökologie und Materialinformationen |
| 5 | EU JRC | https://joint-research-centre.ec.europa.eu | Forschung zu Umweltwirkungen und Lebenszyklus |
| 6 | EU Level(s) | https://environment.ec.europa.eu/topics/circular-economy/levels_en | europäischer Gebäudenachhaltigkeitsrahmen |
| 7 | Zenodo | https://zenodo.org | offene Forschungsdaten/Materialdatensätze |
| 8 | OpenAlex | https://openalex.org | Forschungsmetadaten zu ReUse/LCA |
| 9 | dataholz | https://www.dataholz.eu | Holzbau-Aufbauten und Materialreferenzen |
| 10 | buildingSMART | https://www.buildingsmart.org | IFC-/BIM-Datenstandards, Materialpass-Mapping |
**Queries:** `OIB Richtlinie 7 nachhaltige Nutzung natürlicher Ressourcen`; `EN 15804 EPD Modul D Reuse`; `IFC4 material passport building components`; `reclaimed concrete structural reuse life cycle assessment`.
### B3. UC-04 Digitale Modelle / Knowledge Graph / AI-Engineering
| Rang | Quelle | URL | Funktion |
|---|---|---|---|
| 1 | buildingSMART | https://www.buildingsmart.org | IFC/IDS/BCF Standards und Spezifikationen |
| 2 | GitHub nexus-platform | https://github.com/julianzotter/nexus-platform | vorhandene Code-/Skill-/Workflow-Assets, zuerst Lookup |
| 3 | OpenAlex API | https://docs.openalex.org | strukturierte Forschungs-Metadaten |
| 4 | Semantic Scholar API | https://www.semanticscholar.org/product/api | Literaturgraph, Empfehlungen |
| 5 | CORE | https://core.ac.uk | OA-Volltextrecherche, Nutzungsbedingungen prüfen |
| 6 | GROBID | https://github.com/kermitt2/grobid | wissenschaftliches PDF→TEI Parsing |
| 7 | Microsoft GraphRAG | https://github.com/microsoft/graphrag | Open-Source-GraphRAG-Methode |
| 8 | Neo4j GraphRAG | https://pypi.org/project/neo4j-graphrag/ | Graph-/Retrieval-Schnittstellen |
| 9 | Cytoscape.js | https://js.cytoscape.org | interaktive Knowledge-Graph-Visualisierung |
| 10 | IfcOpenShell | https://ifcopenshell.org | Open-Source-IFC-Verarbeitung |
**Queries:** `IFC4 semantic building component knowledge graph`; `engineering document formula extraction GROBID`; `GraphRAG source provenance ontology`; `Python deterministic structural engineering pipeline benchmark`.
### B4. Retrieval- und Qualitätsvertrag
Pro Treffer `query_id`, `retrieved_at`, `url`, `publisher`, `source_type`, `jurisdiction`, `version`, `license`, `locator`, `relevance`, `verification_status` erfassen. Ohne Volltextzugang keine Normformel behaupten. Quellenlisten priorisieren und aktualisieren, aber nicht als automatisch geprüfte Normbibliothek ausgeben.

## Anhang C. Quellenregister und Konfliktmatrix
**Primär für die Systembeschreibung:** `_AGBS.md` v007.2 (Drive-ID 10Tz…), Manifest NEXUS-ROLES-v1.2 (1POf…), Baseline (1Cdw…), WORK Folder.md v0.4.0-pilot (1nDj…), Systemdossier 2026-10-26 v1.0.0 (1sOF…), ID06-User-Manual 2026-11-26 v0.1.0 (1A4T…), GitHub nexus-platform (aktuelle Suche). **Sekundär:** historische hochgeladene Manifest-/Human-AI-Loop-Dateien 2026-04-07 und Claude-Memory-Screenshots. **Nicht belegt:** universell aktive bidirektionale Synchronisierung, normativ freigegebene Formeln, Vollständigkeit der Registry-Semantik, produktive Cross-LLM-Orchestrierung.
**Konflikte:** (K1) AGB Frontmatter v007.2 versus Abschnitt 12 „bis Rohbyte-Readback v006“; (K2) HISTORY-LOG-ID im AGB versus sichtbarer Root-Ordner; (K3) historische Top-P-Parameter; (K4) älterer Vier-Layer-Diktatentwurf ohne Wissensschicht; (K5) alte GitHub/Drive-Statuswerte versus neue Live-Prüfung; (K6) `USECASES` ist Root-Kind und nicht SSOT-Kind. Konflikte im WORK-Status führen, nicht im Dossier still lösen.

## Anhang D. Semantische Screenshot-Mapping-Inventur
Vorliegendes lokales Mapping `2026-11-26_ID03_memory_mapping_candidate.json`: Einzelbild-SHA, Bild→Objekt-Kandidaten, Parent-Child-Kanten und Registry-Namensmatching. Das Mapping ist **PARTIAL_REVIEW_PENDING**; es ist keine vollständige wortgetreue Extraktion aller sichtbaren Sätze und keine abschließend verifizierte Identitätszusammenführung. Die 20 Routing-KVs bleiben bestehen. Ein nachgelagerter True Run muss je Objekt die Quellbild-Position, tatsächliche Textaussage, Dublettenentscheidung, Primärquellenreferenz und Reviewerentscheidung ergänzen. Der JSON-Anhang ist ein eigener Prüfdatensatz, keine normative KB-Befüllung.

## Änderungs-/Freigabevermerk
Erstellt als **konsolidierender Kandidat** auf ausdrücklichen Nutzerauftrag 2026-11-26. Vorgängerquellen werden referenziert, nicht überschrieben. Keine automatische Änderung der persönlichen ChatGPT-Memory, der AGBs, des Manifests oder bestehender Masterregister. Registrierung, unabhängiger Review und ID01-Freigabe sind getrennte nachfolgende Gates.

**Lokales Mapping-Inventar:** 72 Bildquellen, 257 Wissensobjekt-Kandidaten, 591 Kanten; Zuordnung nicht vollständig auf Aussageebene validiert.
