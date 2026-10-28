---
name: NEXUS-AI-AEC-OS-CONSOLIDATED-MANUAL
version: v0.4.0-review
status: REVIEW
created_at: '2026-10-27T15:17:43+01:00'
timezone: Europe/Vienna
actor_role_id: UNVERIFIED
executor_instance: ChatGPT text/document production
owner_id: ID01
artifact_id: UNREGISTERED_LEDGER_CONFLICT
human_gate: PENDING
source_of_truth: Google Drive / _developement / LLM-LOCAL-SSOT / WORK
source_policy: GOVERNANCE_REFERENCE_ONLY; NO_SILENT_ADOPTION
---
# NEXUS AI-AEC-OS — System- und Betriebshandbuch / Implementation Guide
**Kurzfassung v0.4.0 REVIEW · 2026-10-27T15:17:43+01:00 · Status: NON-PRODUCTION / HUMAN-GATE-PENDING**  
**Scope:** tragwerksplanerische Workflows EN/ÖNORM (AT) mit LLM-Orchestrierung, deterministischem Fachsolver, unabhängiger QA und ID01-Freigabe.  
**Evidenz:** `[Gxx]` NEXUS-Steuerdaten, `[Dxx]` Dokumentationssammlungen, `[Nxx]` Norm-/Rechtsportale. Originaldaten gelten je angegebenem Versionsstand, nicht global. Vollständiges Quellenverzeichnis: Kap. 15.

## 0. Dokumentenkontrolle, Grenzen, Startstatus
- **Dieses Dokument:** abgeleitete, kontrollbedürftige Synthese; **keine neue Governance-Adoption** und kein Ersatz für `_AGBS.md`/CURRENT Manifest/Baseline. Vorrang: konkrete ID01-Entscheidung und freigegebene `_AGBS.md` v003 *für den explizit geregelten Scope*, übrige Konflikte mit Manifest/Baseline kennzeichnen. `[G01–G03]`
- **Aktueller Betriebsbefund (quellenberichtet):** `INCOMPLETE`, `POLLER_FALSE_GREEN`, `NATIVE_SYNC_BLOCKED`, `LEDGER_CONFLICT`, `HUMAN_GATE_REQUIRED`; Version v0.147 um 13:50. Keine aktuelle umfassende Runtimeprüfung in dieser Dokumentenerstellung. `[G07–G08]`
- **Dokument-/Codeautorität:** Drive `LLM-LOCAL-SSOT` für kanonische Governance/WORK-Nachweise; GitHub `nexus-platform` für versionierten Code, CI, Reviews und identifizierte Snapshots. GitHub-`success` allein ist kein Engineering-/Delivery-PASS. `[G03, G04]`
- **Sicherheit:** READ-ONLY/FAIL-CLOSED als Standard; Secrets, lizenzierte Normvolltexte, persönliche und vertrauliche Daten nicht unkontrolliert in Git/GPT-Kontext übertragen. Eindeutige ACLs, tatsächliche Toolrechte, Idempotenz und Human Gate nötig. `[G02–G04]`

## 1. Systemzweck und Abnahmegrundsätze
**Leitsatz:** Quelle/Normprofil → typisierter Informations-/Objektvertrag → geprüfter Rechenkern → Evidenz → unabhängige Fachprüfung → ID01-Freigabe. Sprachmodelle interpretieren, strukturieren, suchen, koordinieren und erläutern; **keine ungeprüfte Numerik**. Ein deterministischer Algorithmus kann bei fehlerhaften Annahmen dennoch falsch sein. `[G03, D02]`
**Main Goals:** (M1) eindeutige Evidenz/Provenienz; (M2) reproduzierbare normgebundene Berechnung; (M3) überprüfbare operative E2E-Kommunikation/Freigabe.
**Bewertung der Arbeitsstände:** `VERIFIED` selbst beobachteter Nachweis; `SOURCE_REPORTED` aus Quelle übernommen; `CALCULATED` deterministischer Lauf; `INFERRED` gekennzeichnete Ableitung; `PROPOSED` Entwurf; `UNVERIFIED` ohne Beleg. Quelle/Code vorhanden != getestet != deployed != zugestellt != abgenommen.

## 2. Kanonische Architektur und Zuständigkeiten
| Schicht | Verantwortung | Autoritätsgrenze | Status |
|---|---|---|---|
| H0 Human/Governance | ID01 Priorität, Scope, Normprofil, Freigabe | ID01-Entscheid + `_AGBS.md` v003 + Manifest/Baseline | dokumentiert |
| L0 Identität/Registry | Quell-ID, Version, Fingerprint, Location, Zustände | Drive-original/Registry; Index nur Projektion | teilweise |
| L1 Knowledge Engineering | CERM→CIM→COM→Ontologie→Parser→KO→Retrieval | stabile Quellen/Locator, keine semantischen Vermutungen als Fakten | konzeptionell |
| L2 Orchestration/Runtime | TASK→ROUTE→CLAIM→EXECUTE→FEEDBACK | konkrete Runtime und Berechtigung, nicht bloß Rollenlabel | E2E offen |
| L3 Engineering Compute | Python/SymPy/FEM/Excel über typisierte I/O | fixierte Eingaben, Normprofil, Version, deterministische Referenzen | projektspezifisch prüfen |
| L4 QA/Reporting | unabhängige Prüfung, Readback, Audit | Review ≠ Human Gate; keine automatisierte normative Autorität | teilweise |
| L5 Interface/Export | Markdown, PDF, API, HTML, IFC, bSDD | Ausgabe/Spiegel nie neue Norm-SSOT | Kandidaten |
**Achtung:** Die Begriffe `L0–L5` hier bezeichnen Verantwortungslagen, keine still übernommene globale Layer-ID; ältere 4- bzw. 7-Schicht-Grafiken sind unterschiedliche Sichten. `[D01–D02,G06]`

**Rollen (einzige Autorität: Manifest §4):** ID01 Mensch/Freigabe; ID02 ChatGPT Chief Orchestrator; ID03 ChatGPT Assistant/Peer; ID04 Gemini Evidenz/Protokoll; ID05 Perplexity Recherche; ID06 Claude Entwicklung; ID07 DeepSeek unabhängiges Audit; ID08 lokales Ollama. Eine Codex-Ausführung ist nicht automatisch „Claude“. Reale `executor_instance`, `provider`, `model_id`, Berechtigungen und unabhängige Reviews separat erfassen. Alle abweichenden Rollenmatrizen alter Manuals sind **SUPERSEDED_IN_ROLE_SCOPE**. `[G02,D08]`

## 3. Gemeinsame Sprache / Top-down-Fachhierarchie
**Sprache = de-AT (default), englische Labels nur Mappings auf identische stabile Konzept-IDs.** Originaltexte bleiben in Ausgangssprache; Übersetzung erzeugt separate Repräsentation. Der folgende Baum ist eine **fachliche Klassifikation**, kein Nachweis normativer Rechtsgeltung. `[G09,G10]`
```text
WISSENSCHAFT / TECHNIK
├── Naturwissenschaften (Mathematik, Physik, Chemie)
└── Ingenieurwissenschaften
    └── Bauingenieurwesen
        ├── Grundlagen: Mechanik, Dynamik, Festigkeitslehre, Baustatik
        └── Konstruktiver Ingenieurbau
            ├── Werkstoff-/Bauweisen: Betonbau, Holzbau, Stahlbau,
            │   Holz-Beton-Verbund, Stahlverbund, Massivbau, Leichtbau
            ├── Systemmodell: Bauteil, Querschnitt, Verbindung, Lager, Lastpfad
            ├── Verfahren: analytisch, numerisch, experimentell
            │   └── FEM / matrixbasierte Strukturmechanik
            └── Anwendung: EC-Normfamilie → Ausgabe → NAD → Klausel/Tab./Gl.
```
**Mechanischer Grundvertrag:** Im linearen statischen Diskretisierungsmodell `K · u = F` (mit Randbedingungen, konsistenter Einheitenbasis). `K` = globale Systemsteifigkeitsmatrix, `u` = Knotenfreiheitsgrade, `F` = äquivalenter Lastvektor. Für nichtlineare Systeme gelten iterations-/zustandsabhängige Gleichgewichtsformulierung und zusätzliche Konvergenz-/Stabilitätsgates; `K u=F` ist dort kein pauschales Gesamtmodell. `[G09]`
**Rechts- und Normspur unabhängig:** `JURISDICTION=AT/WIEN` → Bauordnung Wien/WBTV/OIB-Ausgabe/Verbindlichkeit → tatsächlich projektgültige EN/ÖNORM/NAD/TS/ETA. Wissenschaftsstand und Stand der Technik werden als technische Erkenntniskriterien gesondert geführt; sie überschreiben **nicht automatisch zwingendes Recht**. Quellenhierarchie nach Aussagezweck: **Rechtsgeltung:** amtliche Rechtsquelle; **Normparameter:** gültige Originalnorm/NA; **technische Erkenntnis:** verifizierte Fachregel/Peer Review/Versuch/Hersteller-Evidenz nach fachlicher Aussagekraft. **Keine globale Rangformel** „Stand der Technik > Norm“ ohne Geltungsprüfung. `[G09,N03,N05,N06]`

## 4. Speicherorte, Pfade, Dateien und Funktionen
| Identität / Pfad | Führender Zweck | Kritische Dateien/Verweis | Schreibregel |
|---|---|---|---|
| Drive `_developement` | Entwicklung, SKILLS, MCP-ACCESS-TOOLS | Folder-ID `1OIyJI6rljIi8zNsT-iwg47NsuguoZqTB` | taskbezogen |
| Drive `LLM-LOCAL-SSOT` | Governance/Registry-Dokument-SSOT | ID `1j3FLJkWpQv6xGA_KO0D9sMyA11f0vxBV` | versionsgebunden |
| Drive `LLM-LOCAL-SSOT/WORK` | WOs, Replys, RUNLOG, Evidenz/Status | ID `1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP` | nicht automatisch leeren |
| Drive `MCP-ACCESS-TOOLS` | Tool-Bridges, Adapter, Schemata, Logs | ID `1fRa7rQvKi-BkhVIzjXPcY_u8iIJ4Vn5J` | no secrets |
| Drive `_developement/SKILLS` | wiederverwendbare, geprüfte Arbeitsabläufe | ID `1aeL3p1fuFjOcQ1VrOVTs7LcaJxGZz-ci` | keine zweite Governance |
| Drive `LLM-LOCAL-SSOT/SKILLS` | separat vorhandener Skill-Bestand | ID `1sUxxD6DGGsdJcf5seKZPnJNuNVhkgzJu` | vergleichen, nicht doppeln |
| Drive `_INDEX.MASTER` / `_INDEX_LNK` | Discovery/Wegweiser/Benchmarks | `_INDEX_LNK` ID `1GcIKgilIzIh8TZsD0y9p0MMfjd5hW7SR` | read/index-only |
| Drive `NEXUS.HISTORICAL` | Vorgänger/Sicherung | ID `1Q0CYzEccpL6nfUetHHQjyU4BjAZgmJ7k` | Snapshot/Immutable-Nachweis gesondert |
| Drive `NEXUS.REPORTS` | dauerhafte Berichte | ID `1mmLJyc8TpTqxPFhXASb4tmHI7515xpJn` | WORK-Verknüpfung |
| Drive `INDEX/00_ARTEFAKTE-BIBLIOTHEK` | Vorlagen/Methoden | ID `1jXreTO8oEDblDcTCXAEHVWvioMFJPMXz` | Referenzmaster |
| Drive `AI-PYTHON-PARSE` | Parser/Normquellen, Lizenzen | ID `1nbSlOQkCQ7Yhro3RxtIXW3QLP5yj9nBc` | Originale nicht in Git |
| Windows `G:\Meine Ablage\_developement\LLM-LOCAL-SSOT\WORK` | lokale Sync-Ansicht | Laufwerk/Mount nur hostbezogen | **nicht** als remote überprüft annehmen |
| GitHub `julianzotter/nexus-platform` | Orchestrierung, Control Plane, Tests, Docs/Review-Snapshots | `orchestrator/`, `mcp_bridge/`, `.github/workflows/`, `docs/` | Branch/PR, getrennt von Drive |
| GitHub `julianzotter/AI-ENGINEERING-SYSTEM` | Parser/Fachcode-Hauptzweig | PR4 als Kandidat; `tools`/Parser | kein zweiter Codemaster |
| GitHub `julianzotter/skills` | Skillpakete (nach Ownership-Entscheid) | `skills/NexusFileSearch` u.a. | deduplizierte Referenzen |
**Kanonische Steuerdateien**
| Datei | Funktion | Status/Identität |
|---|---|---|
| `_AGBS.md` | 12 übergeordnete Regeln; gültige Namenssyntax | v003 / ID `10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg` / ID01-Freigabe `[G01]` |
| `00_NEXUS_MANIFEST__CURRENT__2026-09-28` | kanonisches Rollenregister, Systemprinzipien | GDrive `1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg` `[G02]` |
| `00_NEXUS_BASELINE_INSTRUCTIONS__CURRENT__2026-09-28` | MUST-01–159, Storage/WOs/Reporting/Gates | GDrive `1Ig0YFqbWji6B5-oOFcxuVpHb5GEBk0HlbJVz51rf9ho` `[G03]` |
| `Folder.md` (WORK) | ordnerlokale Policy/Pilot und offene Gates | Original ID `11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH` `[G04]` |
| `_FRONTMATTER.md` | Metadatenstandard / Validator-Kandidat | **ENTWURF**, nicht pauschal freigegeben `[G01]` |
| Ticket Registry (Google Sheet) | operative WO-Status-SSOT | ID `1o1ZCZUgsCGTDOwdbJ7EbUCKOKJng1LcJLFnrRiPjYTE` |
| `00_ID_LEDGER.csv` | eindeutige Artefakt-IDs/Versionen | aktuell berichteter Ledgerkonflikt; keine ID selbst vergeben `[G08]` |
| `AIM-NEXUS-KONZEPTREGISTER` | eine Liste, AIM-0001–0009 | v0.3.3 / ID `1y7jmHlyxq7Ja2xA2FM6MJapOjIkIMlqZ` `[G06]` |
| `WO-NEXUS-RUNTIME-REVIEW` | Arbeitsteilung A–D, E2E-Repair | Art.0097 / ID `1uniI-8U2rUDh7Y4zTQ3nuMuN4nqJmpjf` `[G05]` |
| `nexus_contracts_v0_1/` | bestehende QA-/Analyseeingangsverträge | zuerst wiederverwenden, nicht neue parallele Implementierung `[G05]` |
| `tools/drive_changes_poll.py`, `nexus-drive-poll.yml` | Changefeed/Wake-up-Prototyp | FALSE_GREEN-Blocker; CI ≠ Run/ACK `[G07,G08]` |
| `FORMULA_REGISTRY_*`, `SYMBOL_REGISTRY`, `KNOWLEDGE_CHUNKS` | vorhandene Formel-/Wissensartefakte | Quelle/Version/Bytehash erst beim produktiven Binding prüfen `[D04]` |
**Wichtig:** Pfadliste ist eine priorisierte Funktionslandkarte bekannter Orte, **keine rekursiv verifizierte Vollinventur**. Bei Ordner-/Dateinamensabweichung ist die aufgelöste Drive-ID vorzuziehen. Relative Windows-Pfade sind kein Zugriffsnachweis.

## 5. Governance, Dateinamen, Idempotenz und Reporting
**Führend für neue reguläre Markdown-Artefakte:** `YY_MM_DD_HHMM_ID##_THEMA_###.md` (`Europe/Vienna`, Rolle ID## unmittelbar nach HHMM, nachgestellte vergebene Ledger-ID). `_AGBS.md` und andere mit Underscore benannte Steuerdateien behalten stabile Namen; Code/Testkonfiguration funktionsbezogene Namen. Bestehende historische Artefakte nicht massenweise umbenennen. **Kein erfundener Ledger-Identifier**, bei Konflikt `UNREGISTERED / REVIEW` mit dokumentierter Abweichung. `[G01,G08]`
**Frontmatter minimal:** `name`, `version`, `status`, `timestamp`, `role_id`, `executor_instance`, `ticket_id`, `run_id`, `artifact_id`, `gate`, `source_refs`, `hash_scope`, `source_identity`; bei fehlender Identität `UNKNOWN/UNVERIFIED`. Bodyhash SHA-256 über kanonisch definierte UTF-8-Bytes; Vollfilehash extern, nach endgültigem Speichern und Byte-Readback.
**State-Achsen strikt:** Dokument (`DRAFT/REVIEW/CURRENT/...`), Entwicklung (`PROPOSED/IMPLEMENTED/TESTED/ADOPTED`), Task (`OPEN/CLAIMED/RUNNING/REVIEW_REQUIRED/BLOCKED/FAILED/DONE`), Evidenz (`UNVERIFIED/SOURCE_REPORTED/VERIFIED/CALCULATED`), Delivery (`PUBLISHED/DELIVERED/ACKED`) und Human Gate separat. Keine automatische Promotion aus `workflow=success`, `SHA MATCH` oder zwei LLM-Meinungen. `[G03,G07]`
**Run-Envelope:** `STATUS | CHANGED | TESTS | SOURCE_STATUS | RISKS_GAPS | NEXT | QA_STATUS | LOG`; plus Input-/Output-Hashes, Solver-/Normversion, Exitcodes, verantwortliche Runtime und unabhängiger Review-Hash.
**Transaktion:** Input freeze → CLAIM/Lease (atomar oder gesondert getestet) → Execute → Validate → Write → Raw-Readback → Ledger/Registry → Deliver → ACK → Human Gate. Bei `BLOCKED`, defektem JSON, abgelaufenem Claim, fehlenden Credentials, Schreibkonflikt oder unbekanntem Status: **fail-closed**; `INITIALIZED` (Cursor angelegt) ≠ Datenabruf abgeschlossen. `[G05,G07]`

## 6. CERM/CIM/COM, Ontologie und Ubiquitous Language
**CERM** (Canonical Engineering Reference Model) definiert technische Achsen/Jurisdiktion/Normprofile. **CIM** (Canonical Information Model) definiert Klassen; **COM** (Canonical Object Model) typisiert Instanzen. **Ontology** kontrolliert Konzepte und gerichtete Beziehungen; **Metadata** beschreibt jedes Objekt; **Chunk** ist eine rekonstruierbare Retrieval-Einheit, nicht Source of Truth; **KG** ist abgeleitete Projektion. `[G10]`
**Wiederverwendeter 23-Klassen-Core:** `Source, Document, Standard, StandardClause, Definition, Requirement, Rule, Formula, Parameter, Symbol, Unit, Material, StructuralSystem, StructuralElement, Connection, Action, AnalysisModel, Calculation, Verification, Result, Evidence, Decision, Solver`. Dies ist der bestehende Kandidatenbestand; Vererbung **nur** bei nachgewiesener `IS_A`-Beziehung (z.B. Solver ist **nicht** Subklasse der Verification). `[G10,D09]`
**Relationskontrolle:** `IS_A, PART_OF, CONTAINS, HAS_PROPERTY, HAS_PARAMETER, HAS_UNIT, APPLIES_TO, REQUIRES, USES, GOVERNED_BY, DEFINED_BY, DERIVED_FROM, REFERENCES, IMPLEMENTS, IMPLEMENTED_BY, PRODUCES, VERIFIED_BY, SUPPORTED_BY, SUPERSEDES, OVERRIDES, CONFLICTS_WITH`. `OVERRIDES` nur bei konkretem dokumentiertem nationalem Parameter-/Ausgabenkonflikt; keine globale B-Serie-Überschreibung aller EN-Klauseln. `CONFIRMED` Relations müssen evidence source_id + Locator besitzen.
**IDs:** Rollen-ID ≠ Ticket-ID ≠ Artefakt-/Ledger-ID ≠ Source-ID ≠ Chunk-ID ≠ Objekt-ID ≠ Code-Commit; `source_id` bleibt stabil pro Quellidentität, Bytehash repräsentations-/versionsgebunden. Snapshot ist nicht Original.

## 7. Semantisches Parsing → Klassifizierung → Knowledge Object (KO)
**Pipeline:** `GOAL/USECASE → SOURCE_REQUIREMENTS → SOURCE_FREEZE → ID/PROVENANCE → CERM/CIM/COM → STRUCTURE-AWARE EXTRACT → KO_CANDIDATE → VOCAB+RELATIONS → QA → REGISTRY → HYBRID_RETRIEVAL → SOLVER → EVIDENCE`. Schema-First; **nicht** Token-First. Relevante Parsermodi: born-digital PDF/Text; Bild/OCR nur bei Bedarf; Tabellenstruktur-/Zellenlokatoren und Gleichungen gesondert QA. Ohne vollständige Lesereihenfolge/Tabellen/Formeln → `REVIEW_REQUIRED`. `[G03,G10]`
**Taxonomie-Achsen getrennt:**
| Achse | Zweck | Beispiele/Regeln |
|---|---|---|
| `domain_id` | oberste Fachwelt | `ingenieurwissenschaften`, `bauingenieurwesen`, `konstruktiver_ingenieurbau` |
| `subdomain_id` | Spezialdisziplin | `betonbau`, `holzbau`, `verbundbau`, `baustatik`, `FEM` |
| `tech_path[]` | vollständiger Top-down-Pfad | Eltern→Kind, kontrollierte Werte/IDs |
| `object_type` | fachliche Klasse | `Formula`, `StandardClause`, `Verification` |
| `concept_ids[]` | eindeutige Fachbedeutung | `structural:bending`, `timber:service_class` |
| `label_de` | menschenlesbarer Begriff | `Biegetragfähigkeit`; kein Schlüssel |
| `mapping_en` | optionale Sprachabbildung | `Bending resistance`; gleiche Concept-ID |
| `keyword_aliases` | Retrieval-Synonyme | `Biegung`, `Momentenwiderstand` |
| `hashtag` | Anzeige-/Navigationstag | `#HOLZBAU`, kein Beleg |
| `signal` | Priorisierungs-/Routingfeature | `exact_id_match=true`; nie Quelle/Autorität |
| `keyvalue` | typisierter Parameter | `{value,unit,source_ref}`; Dimensionscheck |
| `relation` | gerichtet und evidence-bound | `Formula REQUIRES Parameter` |
| `norm_profile` | Projektgültigkeit | Standard + Edition + EC_GEN + AT + NAD + Clause + Gültigkeitsnachweis |
**Chunking:** kleinste semantisch vollständige Aussage (Definition/Regel/Formel/Tabelle/Ausnahme/Nachweis), Parent-Kontext inklusive Anwendungsgrenzen. Lange Tabellen können zell-/zeilenweise zerlegt werden; jede Einheit behält `source_id`, `section/clause`, `locator`, `sequence`, `parent_id`, Quell-/Parserhash. Für große Inhalte sekundäre technische Chunk-Limits *nach* Strukturierung, nie Trennung von Formel und Bedingungen.
**Indexstrategie:** deterministischer ID-/Register-/Metadatenlookup zuerst; danach graphbasiertes Relationsretrieval, Vektor-Fallback, Reranking und Zitierprüfung; ungeklärte Normgeltung/unsichere Einheit → Abstention. Doppelte PDFs/Chunks dürfen nicht zu mehrfacher „unabhängiger“ Evidenz führen. `[G03]`

### 7.1 JSON-Schema v0.4.0 — separater kontrollierter Kandidat
**Datei:** `nexus_knowledge_object_schema_v0.4.0_REVIEW.json` (Draft 2020-12). 23 Objekttypen, 21 gerichtete Relationstypen, 16 Corefelder + Unterobjekte. `additionalProperties=false` auf Root/Vertragsteilen; Pflicht-Provenienz; mehrdimensionale Status; konditionale Profile für Formeln/Parameter/Solver/Verifications; bestätigte Relation nur mit Locator; Human Gate `GRANTED` nur mit Approval-Referenz. **Schema valide ≠ Norm oder fachliche Richtigkeit**. Das Schema verändert keine bestehende Source-/Formula-Registry und ist bis zur ID01-Adoption `REVIEW`.
**MVP-Prozess:** (1) vorhandenes Schema inventarisieren und Felder/IDs mappen; (2) 25–50 repräsentative Quellen in eigenen abgesperrten Testdaten kopieren; (3) Schema-Contract-/Negativtests; (4) Draft-KO/Relations gegen Original; (5) E2E-Evidence/Golden Cases; (6) Peer+ID01-Adoption; (7) erst dann bestehende Registry gezielt erweitern.

## 8. Eurocode-basierter Bemessungsworkflow (EC2, EC5, HBV/TCC)
**Auftragsvertrag:** `project_id, element_id, geometry_revision, actions, material, design_situation, limit_state, jurisdiction, standard_id, edition, NAD, assumptions, expected_outputs, stop_conditions, owner, reviewer`. `undefined` ist **BLOCKED**, nie impliziter Default. `[G03]`
**Solverkette:**
```text
User MainGoal → Orchestrator/Schema Intake → Source/Norm profile lookup
→ Eng. Input freeze + dimensional validation → L3 verified Python/FEM
→ units/checks/reference comparison → independent review
→ evidence package (inputs/code/norm/outputs/logs) → ID01 release
```
**Generisches Nachweisobjekt:** `E_d` = Bemessungswert einer Einwirkungsauswirkung; `R_d` = Bemessungswiderstand, jeweils vergleichbare physikalische Größe; Einzelcheck `E_d ≤ R_d` nur **wenn** Verfahrensnorm diese Darstellung vorsieht. Dimensionsgleichheit, Lastkombinations-/Kombinationsbeiwertprofile, Randbedingungen und Eurocode-NAD müssen explizit geprüft werden. SLS/Interaktionen erfordern ggf. andere Prüfkriterien.
**EC2:** EN 1992 Teil/Edition + passendes österreichisches B-Dokument; ULS Biegung/Querkraft/Durchstanzen sowie SLS Riss/Verformung, Bauzustand und Brandfall nur soweit im Solververtrag implementiert/validiert.
**EC5:** EN 1995 Teil/Edition + österreichische nationale Festlegungen; Material-/Nutzungsklasse, Lasteinwirkungsdauer, `k_mod`, `k_def`, Verbindungsmittel, ULS/SLS, Brandfall je Projekt.
**HBV/TCC:** gesondertes Verbund-/Schubfugenmodell mit Langzeitverhalten/Kriechen/Schwinden/Bauzustand, charakteristischem Verbindungsgesetz (ggf. Schlupfmodul), Steifigkeits-/Materialprofil und Referenzgeometrie. Nicht pauschal Stahl-Beton-EC4 als Holz-Beton-Norm ersetzen.
**FEM-Gate:** Freiheitsgrade/Lager, Modelltopologie, Materialgesetze, Elemente/Netzkonvergenz, Lastfälle/Kombinationen, Stabilität, Solverkonvergenz, Plausibilität der Reaktions-/Schnittgrößen und Sensitivität. Solver darf numerisch laufen und trotzdem **ENGINEERING_SOLVER_READY=NO** sein. `[D09]`

## 9. Wien / Österreich — normative Dokumente, Geltungsprüfung
**Verbindliche Reihenfolge im Projekt:** (a) aktuelles Wiener Landesrecht/WBTV, maßgebliche OIB-Anhänge und Übergangsrecht; (b) angenommene Projekt-Normausgaben und passende nationale Regeln; (c) Produkt-ETA/EAD/DoP/CE für **konkretes** Kit und Einsatzbereich; (d) Nachweise/Herstellerdetails/Versuche; (e) begleitende allgemeine Dokumente. Keine stillen Normfaktoren. `[N01–N07]`
| Kategorie | Relevante Dokumentfamilien | Gültigkeitskontrolle |
|---|---|---|
| Landesrecht Wien | Bauordnung für Wien; WBTV 2023 (LGBl.14/2024 idF LGBl.26/2026) | Stand Projektgenehmigung, Übergangsrecht, Bauwerksklasse `[N06]` |
| OIB | RL1 Tragfähigkeit, RL2 Brandschutz, RL5 Schallschutz (wo relevant), RL6 Wärmeschutz, Leitfäden | Wien RL1–5 Ausgabe 2023, RL6 Ausgabe 2025 laut OIB (15.07.2026 Inkraftsetzung), Ausnahmen prüfen `[N05]` |
| Basissicherheit/Last | ÖNORM EN 1990, EN 1991 relevante Teile + zugehörige ÖNORM-B-Festlegungen | GEN1/GEN2, Objekt/Nutzung/Bauzustand |
| Betonkomponente | ÖNORM EN 1992-1-1/-1-2, EN 206 / ÖNORM B 4710-1, EN 13670; weitere projektspezifische Produkt-/Ausführungsnormen | Ausgaben, NA, Beton/Exposition/Verbund |
| Holzkomponente | ÖNORM EN 1995-1-1/-1-2, EN 14080/EN 16351/EN 338/EN 14592 nach Bauteil | Festigkeit, Feuchte/Lasteinwirkungsdauer, Produktnachweis |
| HBV technische Spezifikation | **ONR CEN/TS 19103:2022** und **ONR CEN/TS 19103/NA:2025-01-15** (NDP/NCCI) | Anwendbarkeit und Projektadoption explizit `[N02,N03]` |
| HBV Gen2 | **ÖNORM EN 1995-1-3:2026-05-01** im ASI-Shop sowohl als „Norm“ als auch „Normentwurf“ ausgewiesen | **PORTAL_STATUS_CONFLICT**; rechtliche/technische Projekteinführung und passende NAD vor Bemessung prüfen `[N01]` |
| HBV Kit / CE | **EAD 130018-00-0303** + produktkonkrete ETA/DoP; u.a. ETA 25/0928 als Beispiel, **kein Universalnachweis** | EAD ist Bewertungsgrundlage für Bauprodukte, nicht selbst die gesamte Bemessungsnorm `[N04,N07]` |
| Brand / Schall | EN 13501-1/-2, OIB-RL2/RL5, akustische/normative Nachweise projektspezifisch | Tragschicht/Verbund/Konstruktion prüfen |
| Ausführung | ÖNORM EN 13670, ÖNORM B 2215, einschlägige Ausführung und Qualitätssicherung | Bauablauf/Vorfertigung/Zulassung, Normteile+Ausgabe prüfen |
**Korrekturen gegenüber importierter Liste:** `ONR CEN/TS 19103/NA:2025` ist österreichisch, nicht DIN; zurückgezogener Entwurf `ONR CEN/TS 19103/A:2023` nicht als derzeit führend; EN 1994 (Stahl-Beton) nur bei geeigneter expliziter Anwendbarkeit; `ÖNORM EN 1995-1-3:2026` **nicht ungeprüft** als rechtsverbindlich bezeichnen. ASI hat widersprüchliche DE-/EN-Produktlabels; `PROJECT_VERIFIED` erfordert Volltext/Ausgaben-/Nationaladoptionsprüfung. `[N01–N03]`
**Normstatus-Klassifikation:** `CANDIDATE | EDITION_VERIFIED | JURISDICTION_VERIFIED | PROJECT_ADOPTED | SUPERSEDED | REVOKED`; `edition` und `national_document` verpflichtend für freizugebende normbasierte KO; Lizenzrechte separat sichern. Keine Normparameter aus Sekundär-Zusammenfassungen übernehmen.

## 10. Bedienung — von Work Order zum freigegebenen Ergebnis
1. **Bootstrap:** aktuelle `_AGBS.md` → Manifest/Baseline → WORK `Folder.md` → Ticket Registry/WO → Capability-Check; Quell-IDs/Versionshashes, tatsächliche Runtime, erlaubte Tools, Rechte deklarieren. Fehlende Pflichtquelle ⇒ `BLOCKED`.
2. **Intake:** vorhandenen WO mit Scope, Input-/Output-Schema, Abnahmekriterien, Budget, Stop-Regel `CLAIM`en (wenn wirksame Lease/Exklusivität). `AIM`-Idee ist noch kein WO.
3. **Source Freeze:** Quellenoriginale mit Rechte-/Version-/Hash-/Locatorbindung; Konflikte und fehlende Normentexte sichtbar.
4. **Execution:** nur freigegebene Toolroute und deterministische geprüfte Programme; keine automatische Änderung normativer Annahmen durch LLM.
5. **QA:** Schema, Dimensions-/Methoden-/Referenz-/Sensitivity-Checks, unabhängiger Peer-Review, negative Fixtures; `FAIL/BLOCKED` dokumentieren.
6. **Delivery:** Ziel-Datei speichern → Rohbytes lesen → Vollhash vergleichen → Registry/History → belegter Transport → Empfänger-ACK.
7. **Freigabe:** ID01 entscheidet anhand Evidenz und offener Gates; `DONE` nur bei vollständiger Abnahme. Restore/Retry separat testen. `[G03,G05]`

## 11. Monitoring, Betriebsdiagnostik und Wiederherstellung
**Betriebspanel** muss getrennt zeigen: Trigger/scheduled, Prozess gestartet, `status.json` inhaltlich, Input-Read, geänderte Objekte, Ausführung, Output-Write, Hash-Readback, Ticket-Claim, Delivery, ACK, fachliche QA, Human-Gate. **Ampel** pro Ebene, nicht ein gesamtes Grün. `[G07]`
**Negative Pfade:** missing OAuth/invalid JSON/unknown state, `INITIALIZED`, stale cursor, doppelte Zustellung, Race/Lease-Expiry, API-Timeout, Konflikt über Versionshash, beschädigte PDF-Formel, falsche Dimension, gekennzeichnete Normedition, fehlerhafte Source-Authority, Credential-Leak.
**Recovery:** letzter geprüfter Ledger-Checkpoint + Artefaktmanifest → isolierter Rebuild → Bytehashvergleich → Link-/Registryintegrität → Wiederanlaufprobe → ID01-Autorisierung für produktives Rücksetzen. GitHub Actions Artifact Retention ist keine nachgewiesene langfristige WORM-Sicherung.

## 12. Messbarer System-Evaluierungsvertrag
| Evaluierungsachse | Messverfahren / Nenner | PASS-Bedingung (vorgeschlagen) |
|---|---|---|
| Governance | Konflikte aus AGB/Manifest/Baseline/Rollen/IDs | keine kritischen ungeklärten Autoritätskollisionen |
| Security | ACL/Secrets/Least-Privilege, blockierter Schreibversuch | zero unautorisierte Writer im freigegebenen Scope |
| Identity/Registry | stable IDs, versioned hashes, no duplicate allocation | jeder registrierte Identitätsschlüssel eindeutig, referenziert |
| Parser/Knowledge | Golden set für Tabellen/Formeln/Normausgaben/Chunk-Herkunft | keine kritischen Quellankerfehler; Recall über datierten Referenznenner |
| Retrieval | unabhängige Fragen, Reranking, No-source-Abstention | Quelle + exakter Locator oder bewusste Enthaltung |
| Routing | validierte Toolzuordnung / Privacy / Kosten / Eskalation | kein verbotener Dispatch; robuste Negativfälle |
| Solver | normprofilgebundene Referenzen/Boundary-/Dimensionstests | fachlich definierte Toleranzen und vollständige Replays |
| Delivery | WO→ACK→Human Gate, Replay und Retry | echter Rohbyte-Readback, keine Duplikat-DONE |
| Scalability/Latency | fixierter Last-/Kontextkorpus, Hardware/Commit/Statistik | messbare Perzentile, keine unkalibrierten % |
| Resilience/Recovery | Crash/restart/Lease/Restore Drills | Datenintegrität/Rekonstruktion nachweisbar |
| Documentation & UX | aktuelle Manuals/Glossar/Dateiliste/Accessibility | eindeutige CURRENT-Quelle, keine Layout-/Versionskonflikte |
**Freigabestrategie:** zuerst Betriebsgoldenslice, anschließend Norm-/Solvergoldenslice; Referenztest vor Peer; Peer vor Human Gate. Keine „Accuracy 100 %“ oder sonstige numerische Scores ohne Messdefinition und Nenner. `[G03,G07]`

## 13. Verbesserungsprogramm (REUSE-FIRST)
| Pri. | Work Package | Ergebnis und Abnahme |
|---|---|---|
| P0-01 | AGB/Manifest-/Namen-/Ledger-Audit | `v003`-gebundener Validator, additiver Ledger-Snapshot, eindeutige Zustände, ID-Konflikte geklärt |
| P0-02 | ACL/Secrets/OAuth/False-Green | aktuelle Rechte+Negativtest, sichere Credentials, `BLOCKED` wird non-zero |
| P0-03 | End-to-End-One-WO / native Sync | Intake→Claim→Run→Readback→ACK; Retry/Lease/Restore und vollständiges Evidence Package |
| P1-04 | CERM/CIM/COM+KO-Schema | Feld-Mapping bestehender Register, Schema/Fixtures, Ontologie und Source-Locators |
| P1-05 | Golden EC2/EC5/HBV | ein fixierter (nicht automatisch produktiver) Designfall mit Normadoption und unabhängiger Solver-/Fachprüfung |
| P1-06 | Log-/Status-/Dashboard-Aggregation | Delta-only Report mit gemessener Coverage, kein zweiter SSOT |
| P2-07 | Interoperabilität / IFC-/bSDD-Export | revisions-/semantikgebundenes Mapping nach nachgewiesenem Bedarf |
**Change Policy:** Entwurf als PR/Drive-Reviewkopie; nicht ohne ID01-Adoption in produktive Validator-/Governance-/Solverkonfiguration übernehmen.

## 14. Ubiquitous Language / Glossar (kanonische Bedeutung im vorliegenden Review)
| Begriff | Definition / Abgrenzung |
|---|---|
| AI-OS | AI Operation System; Governance-/Orchestrierungs-/Daten- und Ausführungsrahmen |
| AEC | Architecture, Engineering, Construction |
| SSOT / SSoT | Single Source of Truth; kanonisches Objekt je definiertem Scope |
| WORK | operative Arbeits- und Kommunikationsablage, **kein** automatisch zu leerender Temp-Pfad |
| WO / Ticket | registrierter ausführbarer Arbeitsauftrag; AIM-Idee ist kein WO |
| AIM | Advanced Idea Management, ein versioniertes Ideenregister |
| ID01–ID08 | kanonische Rollen-IDs, kein Provider- oder Login-Beweis |
| AGBS | führende NEXUS-Steuerregeln; v003 gültig für explizite Benennungsregel |
| Baseline | versionierter Satz operativer MUST-Regeln |
| Frontmatter | maschinenlesbarer Dokumentkopf, ohne automatische Release-Wirkung |
| Ledger | unveränderlich nachverfolgbares Identitäts-/Historyregister; Write-Autorität prüfen |
| Hash / SHA-256 | Byteintegritätsfingerprint, **kein** Nachweis fachlicher Richtigkeit |
| WORM | Write Once Read Many; erfordert technisch nachgewiesene Schreibsperre |
| Claim / Lease / CAS | Aufgabenübernahme / befristete Exklusivität / atomarer Compare-And-Swap |
| ACK | expliziter Empfangsnachweis eines tatsächlich erreichten Empfängers |
| Human Gate | ausdrückliche menschliche Freigabe für definierten Scope |
| FALSE_GREEN | technischer Workflow „success“ trotz inhaltlichem `BLOCKED/INCOMPLETE` |
| CI / CD | Continuous Integration / Delivery (unabhängig von Fachfreigabe) |
| CERM / CIM / COM | Canonical Engineering Reference / Information / Object Model |
| KO / KG | Knowledge Object / Knowledge Graph; Quelle ≠ Chunk ≠ KO ≠ Relation |
| Ontologie | formal definierte Konzeptklassen und Beziehungen |
| Controlled Vocabulary | geprüfte Begriffs-IDs mit DE-Labels/optionalen EN-Aliases |
| Domain/Subdomain | fachliche Haupt- bzw. Unterdisziplin; getrennt von Usecase/Intent |
| Label / Alias / Hashtag | Displayname / Suchsynonym / UI-Navigation; keine Autorität |
| Signal / KeyValue | Rankingmerkmal / typisierter Parameter samt Einheit und Quelle |
| Locator | reproduzierbarer Fundort bis Seite/Klausel/Tab./Gleichung/Zeile |
| RAG | Retrieval-Augmented Generation; Index-/Vector/Graph-Projektionen bleiben nachgeordnet |
| Parser / Chunk | deterministische Repräsentationsextraktion / rekonstruierbare semantische Einheit |
| MVC/MVP | Minimum Viable Context / Minimum Viable Product/Proof |
| MoE | Mixture of Experts; hier externe Rollen-/Modellroutinglogik, nicht interne Modellgewichte |
| MCP/A2A | Model Context Protocol für Tool-/Ressourcenzugriff / Agent2Agent für Interagenten-Kommunikation |
| FEM | Finite-Elemente-Methode; Näherungs-/Diskretisierungsverfahren; Matrixsystem mit Randbedingungen |
| ULS / SLS | Ultimate / Serviceability Limit State; GZT/GZG |
| EC2 / EC5 | Eurocode 2 (Betonbau) / Eurocode 5 (Holzbau), Ausgabeteil prüfen |
| EN/ÖNORM/ONR | Europäische Norm / österreichische Norm / österreichische Regel |
| NAD/NA, NDP/NCCI | nationaler Anhang / national festgelegter Parameter / ergänzende, nicht widersprechende Information |
| HBV/TCC | Holz-Beton-Verbund / Timber-Concrete Composite |
| TS / EAD / ETA / DoP | Technische Spezifikation / European Assessment Document / European Technical Assessment / Declaration of Performance |
| Gen1/Gen2 | Generation einer Eurocode-Norm; Projektgültigkeit und Mischverbote dokumentieren |
| IFC / bSDD | Industry Foundation Classes / buildingSMART Data Dictionary: optionale Austausch-/Terminologiemappings |
| E_d / R_d / η | Bemessungsbeanspruchung / Bemessungswiderstand / dimensionsloser Ausnutzungsgrad nach anwendbarer Normregel |
| k_mod / k_def | Holzbau-Modifikations- / Kriech-Verformungsfaktor, norm- und anwendungsabhängig |

## 15. Originalquellen und Referenzen (Identität, Stand, Locator)
**Leseregel:** NEXUS-Dokumente sind Quellen über gemeldete Zustände; aktuelle technische Freigaben nur aus zugehöriger Primärevidenz. `[Nxx]` sind offizielle Verzeichnis-/Originalseiten; lizensierte Normentexte wurden hier nicht übernommen.
| ID | Quelle / Funktion | geprüfter/bekannter Stand | Original-URL |
|---|---|---|---|
| G01 | _AGBS.md v003 | 2026-10-27 | https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view |
| G02 | CURRENT Manifest §2/§4/§10 | 2026-09-28 | https://docs.google.com/document/d/1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg/edit |
| G03 | CURRENT Baseline MUST-01–159 | 2026-09-28 | https://docs.google.com/document/d/1Ig0YFqbWji6B5-oOFcxuVpHb5GEBk0HlbJVz51rf9ho/edit |
| G04 | WORK Folder.md (Original) | 2026-10-18 | https://drive.google.com/file/d/11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH/view |
| G05 | WO NEXUS RUNTIME REVIEW 0097 | 2026-10-27 | https://drive.google.com/file/d/1uniI-8U2rUDh7Y4zTQ3nuMuN4nqJmpjf/view |
| G06 | AIM v0.3.3 0101 | 2026-10-27 | https://drive.google.com/file/d/1y7jmHlyxq7Ja2xA2FM6MJapOjIkIMlqZ/view |
| G07 | CPLM Audit v0.147 | 2026-10-27T13:50+01:00 | https://drive.google.com/file/d/1lxypi81ab8H6XiuCE7zW24FfRsx4Ro57/view |
| G08 | Rollout Status v1.86 | 2026-10-27T10:32+01:00 | https://drive.google.com/file/d/1ndFbtX4kT9RyQGNPROZ7k2V4orJ1OoI_/view |
| G09 | ID01 zusätzlicher Usermanual-/Normen-Seed | 2026-10-27 | https://drive.google.com/file/d/106Dy6s4_Czg0Mg4ciQkA1MZJadcmmD_x/view |
| G10 | CERM/CIM/COM Work Order v0.1 | 2026-09-29 | https://docs.google.com/document/d/11EoflLXJ9dIdWftIGKGvYpfB-15wmgNLuclA1GMdGD4/edit |
| D01 | Systemarchitektur v1.0 (CANDIDATE) | 2026-10-26 | https://drive.google.com/file/d/1sCp9zlLC3Dt7cd_AekGN2CxJMf-IwtRo/view |
| D02 | Systemdesign/Signalmatrix v1.0.0 (REVIEW) | 2026-10-26 | https://drive.google.com/file/d/1BDelX0b82TxU5-fjM7glWOgJMYX8rzeN/view |
| D03 | Gemini considered config v2 (KANDIDAT) | 2026-10-26 | https://drive.google.com/file/d/1i3TbheOX2nJCM6rCm7riUs6O_P4JPrN6/view |
| D04 | AEC WMS Framework Status | 2026-10-27 | https://drive.google.com/file/d/1kcGbcnaDkK3PqZgW2G8vGhVkB5vbVk6b/view |
| D05 | Reparaturplan ID03 | 2026-10-26 | https://drive.google.com/file/d/1ky77WzuO0fmxtBQBNpSDsWrwlshJ6ZQI/view |
| D06 | Engineering Workflow + Benchmark ID01 | 2026-10-26 | https://drive.google.com/file/d/1CThs6_ALDB5yXvGk9BCRnZpD6PEw7OQD/view |
| D07 | Ablage + Routing ID01 (Konzept) | 2026-10-26 | https://drive.google.com/file/d/1weCgkXnoifVSOaEeOFT_KUbeCYNsggRo/view |
| D08 | User Manual v1.0.0 (Konzept) | 2026-10-26 | https://drive.google.com/file/d/1xTkpw_C251lt0-2I_GKd_ZE2xRqXECqv/view |
| D09 | 418-Seiten-Sammlung Rootfolder | 2026-10-27 | https://drive.google.com/file/d/1Br7tLNyMQLtS33GWFCuQvxOo2LwyELjc/view |
| N01 | ASI ÖNORM EN 1995-1-3:2026 | 2026-10-27 Abruf | https://www.austrian-standards.at/de/shop/onorm-en-1995-1-3-2026-05-01~p4849354 |
| N02 | ASI ONR CEN/TS 19103/NA:2025 | 2026-10-27 Abruf | https://www.austrian-standards.at/de/shop/onr-cen-ts-19103-na-2025-01-15~p4009141 |
| N03 | ASI Eurocodes Übersicht | 2026-10-27 Abruf | https://www.austrian-standards.at/de/standardisierung/standards-verstehen/eurocodes |
| N04 | EOTA EAD 130018-00-0303 Original | 2014 Dokument/2026 Abruf | https://www.eota.eu/download?file=/2019/19-13-0555/for%20ojeu/ead%20130018-00-0303_ojeu%202023.pdf |
| N05 | OIB Richtlinien und Bundeslandinkrafttreten | 2026-10-27 Abruf | https://www.oib.or.at/kernaufgaben/oib-richtlinien/ |
| N06 | RIS Wiener Bautechnikverordnung 2023 | 2026-10-27 Abruf | https://www.ris.bka.gv.at/GeltendeFassung.wxe?Abfrage=LrW&Gesetzesnummer=20000702 |
| N07 | EOTA ETA 25/0928 EAD Basis | 2026-10-27 Abruf | https://www.eota.eu/etassessments/21990 |

## 16. Offene Nachweise / Release-Entscheidung
**STOP / Human Gate:** offene Ledger-ID, fehlender aktueller Reviewer-/ACL-/Credential-/native-E2E-Nachweis, unprüfte Produkt-/Normausgaben oder nicht belegte Datenabdeckung ⇒ KEINE SYSTEM-/ENGINEERING-ADOPTION. Das Handbuch/Schema/Report sind **Version v0.4.0-REVIEW**; neue Dateien erhalten erst nach gelöstem Ledgerkonflikt kanonische Nummer und ID01-Freigabe. `[G07,G08]`
