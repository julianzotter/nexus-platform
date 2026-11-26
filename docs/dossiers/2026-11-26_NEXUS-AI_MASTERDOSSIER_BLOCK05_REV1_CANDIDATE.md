---
name: NEXUS-AI-MASTERDOSSIER-BLOCK05
version: 1.0.0-candidate
status: DRAFT_IN_PROGRESS
created_date: 2026-11-26
author_role: ID03
owner_role: ID01
scope: Technische Anhänge A–G, Quellenatlas, Taxonomie, Dokumentationsvertrag und Quellenverzeichnis
review_status: REVIEW_PENDING
registration_status: REGISTRATION_PENDING
human_release: PENDING
---

# NEXUS-AI Engineering Knowledge Operations System
## Redaktionsblock 05 – Technische Anhänge A–G

> **Leseschlüssel.** Dieser Anhang ist eine verifizierbare Orientierung über Quellen, Begriffe und Schnittstellen. Die hier angegebenen Pfade und IDs wurden aus den bezeichneten Google-Drive-Quellen bzw. dem vorhandenen Redaktionsbestand entnommen. Ein Dateifund beweist noch keine Funktion, keinen ausführbaren Workflow und keine fachliche Freigabe. Die originalen Governance-Dateien werden weder geändert noch durch diesen Anhang ersetzt.

# Anhang A – Begriffe und Taxonomie

## A.1 Terminologische Grundordnung

| Begriff | Arbeitsdefinition | Abgrenzung |
|---|---|---|
| NEXUS-AI | Quellengebundenes, durch Regeln geführtes Engineering-Knowledge- und Operations-System | Kein eigenständiger Ersatz für Fachsoftware oder menschliche Tragwerksplanung |
| SSOT | Für eine definierte Objektklasse maßgebende Quelle | Nicht gleichbedeutend mit einem einzigen physischen Speicher |
| Quelle / Source | Identifizierbare Originalrepräsentation mit Herkunft, Version und Fundstelle | Nicht automatisch fachlich verifiziert |
| Wissensobjekt / Knowledge Object | Identifizierte, semantisch erschlossene Aussage oder Einheit mit Provenienz | Nicht mit Rohdatei oder Textchunk gleichzusetzen |
| Chunk | Aus einer Quelle abgeleitetes, lokalisierbares Text-/Datensegment | Kein selbstständiger Primärbeleg |
| Taxonomie | Hierarchisches und facettiertes Ordnungssystem für Begriffe und Klassen | Nicht mit der gesamten Ontologie gleichzusetzen |
| Ontologie | Definierte Klassen und typisierte Beziehungen einschließlich Geltungsregeln | Nicht bloß ein Ordnerbaum |
| Knowledge Graph | Netz aus identifizierten Objekten und begründeten Relationen | Visualisierung allein beweist keine Graph-Validität |
| Retrieval | Gezielter Abruf von Quellen und Wissenseinheiten | Vor der Antwortgenerierung, nicht mit generativer Plausibilität verwechseln |
| RAG | Generierung unter Verwendung abgerufener Kontexte | Kein Ersatz für Quellprüfung und Normgeltung |
| Workflow | Wiederholbare Folge von Tätigkeiten mit Zuständen, Ein-/Ausgaben und Abnahme | Nicht identisch mit einem einzelnen Skript |
| Skill | Gekapselte Fähigkeit mit definierter Anwendung, Inputs, Outputs und Ressourcen | Kein Beweis der Lauffähigkeit ohne Test |
| Solver | Rechenprogramm für ein explizites mathematisches Modell | Fachliche Modellannahmen und Normgeltung bleiben prüfpflichtig |
| Agent | Beauftragte Funktion bzw. Rolle mit definiertem Scope | Rollen-ID, Provider, Modell und Runtime sind verschiedene Angaben |
| WorkOrder | Nachvollziehbar beauftragte, zustandsgeführte Arbeitseinheit | Ablage allein beweist keine Zustellung |
| TrueRun | Tatsächlich ausgeführter Lauf mit nachvollziehbaren Eingaben und Ergebnissen | Kein bloß formulierter Testplan |
| Evidence | Überprüfbarer Beleg für eine konkrete Aussage | Behauptung oder Memory ist kein Ausführungsbeleg |
| Review | Fachlich unabhängige Prüfung von Ergebnis, Annahmen und Evidenz | Unterschiedliche Rollenbezeichnungen garantieren keine Unabhängigkeit |
| Human Gate | Ausdrückliche menschliche Entscheidung an einem definierten Punkt | Nicht automatisch durch grüne Testanzeige ersetzt |
| Registry | Bestehendes Verzeichnis stabil identifizierter Objekte/Artefakte | Kein paralleles Register nur für dieses Dossier |
| Ledger | Kanonische Ereignis-/Registrierungsfolge gemäß aktueller Governance | Keine frei erfundenen laufenden Nummern |
| Snapshot | Zeitgebundene, unveränderte Kopie einer bestimmten Quellfassung | Nicht selbst die laufend verbindliche Quelle |
| Provenienz | Dokumentierte Herkunft und Transformationskette | Inhaltliche Richtigkeit erfordert zusätzliche Prüfung |

**Quellenbasis:** [Shared Language & Glossary](https://drive.google.com/file/d/1MnHMlbPgKRNUlSiW7SzRk20EvLrSLEOJ/view) (abgerufene Fassung `2026-11-02-supplement-1`, Status Kandidat); [CURRENT Manifest](https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view); [Baseline Instructions](https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view).

## A.2 Taxonomische Achsen und Beziehungsmodell

Eine Fachanwendung wird nicht allein nach Dateispeicherort klassifiziert. Vorgeschlagenes multidimensionales Modell:

1. **Fachachse:** Ingenieurwissenschaft → Bauwesen → konstruktiver Ingenieurbau → Werkstoff/System → Bauteil → Nachweis.
2. **Regelachse:** Jurisdiktion → Rechtsakt/Richtlinie → Normenfamilie → Ausgabe → nationaler Anhang → Abschnitt → anwendbare Bedingung.
3. **Prozessachse:** Ziel → Use Case → Workflow → Skill/Tool → Solver → Prüfschritt → Artefakt.
4. **Wissensachse:** Quelle → Quellrepräsentation → Chunk → Wissensobjekt → Graphrelation → Retrievalprojektion.
5. **Betriebsachse:** WorkOrder → Agent/Rolle → Runtime → Run → Evidenz → Review → Freigabe → Status.

Beziehungen wie `REFERENCES`, `REQUIRES`, `USES_METHOD`, `PRODUCES`, `VALIDATED_BY`, `STORED_AT` und `SUPERSEDES` sind **typisierte Vorschläge**. Die tatsächliche produktive Graphschema-Übernahme bedarf Registry-Abgleich. Die in früheren Dossierfassungen beschriebenen `D01–D20` sind semantische Kandidaten, keine hier neu vergebenen Register-IDs. Gleiches gilt für Routing-Labels `KV-01–KV-20`.

## A.3 Fachliche Beispielklassifikation

| Beispielbegriff | Fachbezug | Regel-/Methodenbezug | Ergebnisobjekt |
|---|---|---|---|
| Holz-Beton-Verbund-Rippendecke | Holz-/Verbundbau, Geschossdecke | EC5, CEN/TS 19103, nationale Festlegungen je Geltung | Bemessungs- und Prüfbericht |
| Stahlbeton-Fertigteilträger | Beton-/Stahlbetonbau | EC2, Einwirkungen, Bauteil- und Fugennachweise | Nachweismatrix, Fehler-/Freigabeprotokoll |
| Materialkatalog | Materialkunde, Bauökologie, Ressourcen | EPD, LCA, Produkt-/Bauteilidentität, Datenrechte | Materialdatensatz, Vergleich, Materialpassentwurf |
| Control Panel | Software-/Operations-Engineering | Status-, Registry-, WORK- und Zugriffsverträge | Kontrollansicht, evidenzgebundener Status |
| IFC-Gebäudemodell | BIM / Digital Engineering | IFC-Schema, Objekt-IDs, Klassifikation, Austausch | Modell- und Mengenreferenzen |

# Anhang B – Verifizierter Google-Drive-Verzeichnisatlas

## B.1 Struktur und Quellhoheit

| Ressource | Tatsächliche Drive-ID | Direktlink | Funktion |
|---|---|---|---|
| `_developement` | `1OIyJI6rljIi8zNsT-iwg47NsuguoZqTB` | https://drive.google.com/drive/folders/1OIyJI6rljIi8zNsT-iwg47NsuguoZqTB | Gemeinsamer Entwicklungs-Root |
| `LLM-LOCAL-SSOT` | `1j3FLJkWpQv6xGA_KO0D9sMyA11f0vxBV` | https://drive.google.com/drive/folders/1j3FLJkWpQv6xGA_KO0D9sMyA11f0vxBV | Kanonische Steuer- und Wissensorganisation |
| `LLM-LOCAL-SSOT/WORK` | `1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP` | https://drive.google.com/drive/folders/1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP | Aufträge, Berichte, Review-Artefakte |
| `_developement/USECASES` | `1sNPiZgSOL2g-RQgOdVzBShWaF5sIlni2` | https://drive.google.com/drive/folders/1sNPiZgSOL2g-RQgOdVzBShWaF5sIlni2 | Fachliche Anwendungen und Strategiepapier |
| `_developement/MCP-ACCESS-TOOLS` | `1fRa7rQvKi-BkhVIzjXPcY_u8iIJ4Vn5J` | https://drive.google.com/drive/folders/1fRa7rQvKi-BkhVIzjXPcY_u8iIJ4Vn5J | Zugangswerkzeuge und zugehörige Dokumentation |

**Befund:** Der benutzte USECASES-Ordner ist ein direktes Kind von `_developement`, nicht von `LLM-LOCAL-SSOT`. Die von ID06 gemeldete zweite gleichnamige Ablage ist nicht durch einen aktuellen Vergleich beider Ordner vollständig aufgelöst; die Identität wird deshalb stets über die Folder-ID angegeben.

## B.2 Maßgebende Dokumente

| Dokument | Nachgewiesener Stand/Status | Drive-ID / Link |
|---|---|---|
| `_AGBS.md` | Inhalt trägt `v007.2`; Aktivierung/Übernahme in den kanonischen Dateikörper laut eigener Frontmatter noch zu prüfen | https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view |
| CURRENT Manifest | Konsolidierung 2026-09-28, Rollenregister v1.2 als späterer Nachtrag | https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view |
| CURRENT Baseline Instructions | Stand 2026-09-28 mit Rollen-Nachtrag | https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view |
| `WORK/Folder.md` | `0.4.0-pilot` | https://drive.google.com/file/d/1nDjF78dq3l8PGpXsauzBz1bzHescDSwv/view |
| Shared Language & Glossary | `2026-11-02-supplement-1`, Kandidatenstatus | https://drive.google.com/file/d/1MnHMlbPgKRNUlSiW7SzRk20EvLrSLEOJ/view |
| `file-registry.jsonl` | Registrierungsziel; Inhalt in diesem Lauf nicht als aktuelle vollständige Sequenz verifiziert | https://drive.google.com/file/d/15m8T5cWbogIup9snzFwiB1g9HqNCoGow/view |
| ID06 Peer Review | Stellungnahme vom 26.11.2026, nicht bindende Empfehlung | https://drive.google.com/file/d/1vS3KBK9nnBoDVucMqX5OzoEW8_r0KU0M/view |
| Dossier v0.2.0 | Historischer Kandidat, kein Release | https://drive.google.com/file/d/1SJQ4WeU5AWWQgLRVQDNxUA9FKujUqWKT/view |

## B.3 Nachgewiesene USECASES-Unterordner (Stichprobe vom 26.11.2026)

| Fachordner | Drive-ID | Einordnung |
|---|---|---|
| `FT_TRÄGER_MATRIX` | `1STCwWk7pewkqpDb-9QaRav-VmKK9ZSWX` | Stahlbeton-Fertigteilträger / EC2 |
| `HTML-DASHBOARD-INVENTAR` | `1vE2K8DuyWGH_lIoGctBG96di_iKBjo_J` | Weboberflächen und App-Inventar |
| `Interactive-AI-Studio-Apps` | `1l12SPI3xZ5jS82hy1H2n-Y-qpsDG7YT_` | Prototypen/Anwendungen |
| `CONTROL-PANEL` | `1t7T-KWn2s9HUctXGg-HY04z3xLamRJ5g` | Steuerungs- und Monitoringoberfläche |
| `OLLAMA` | `1CgL31Hr_iclym9qFxGBpmV7cBqR2VfW4` | Lokale LLM-Laufzeitintegration |
| `LV_EISTEICHE_LB-HB` | `1RxvwnsimHK8TTJ6zpe6YI4Uj-RG41mfb` | Ausschreibung/Leistungsbeschreibung |
| `MATERIALKATALOG` | `1nLBc4Ij5ZpxX-N75dH_CUq_B5BnqOmNt` | Materialdaten und Varianten |
| `Galleria_EKZ_BZ` | `180ITGCoOJy1ko8l78AfxybxXIc33HVSB` | Projektbezogene Fachanwendung |
| `SQE_L1` | `1Jl3IaQWMq-BbcKM9GSrsHk_HE-FYJyPN` | Projektbezogene Fachanwendung |

Die vollständige Live-Inventur der Unterverzeichnisse ist eine eigene Aufgabe. Für `Galleria_EKZ_BZ` und `SQE_L1` werden keine fachlichen Implementierungsdetails aus dem Ordnernamen abgeleitet.

# Anhang C – GitHub- und Software-Referenzatlas

## C.1 Repository und Versionierung

**Repository:** https://github.com/julianzotter/nexus-platform  
**Dossier-Review-Branch:** `docs/id03-nexus-dossier-20261126`  
**Bestehender Draft-PR:** https://github.com/julianzotter/nexus-platform/pull/147

GitHub ist für Code, Tests, technische Verträge und nachvollziehbare Änderungen vorgesehen. Ein Commit bestätigt die Versionierung eines bestimmten Inhalts, nicht die technische Funktion oder die automatische Synchronisierung mit Drive. Für einen echten Sync-Nachweis sind Quell-/Ziel-ID, Bytegleichheit, Run-Receipt und gegebenenfalls CI-/Deploy-Nachweise erforderlich.

## C.2 Nachgewiesene Werkzeugdateien in MCP-ACCESS-TOOLS

| Datei | Drive-ID | Gegenstand / Prüfgrenze |
|---|---|---|
| `nexus_tower.py` | `1xX3htWBYx-68y5l2_2lgMUtFzLDx4BVU` | Steuerungs-/Tower-Skript; Lauf nicht geprüft |
| `nexus_status.py` | `1IZCvxHdHXrCxnztpMwIHbE7ZoUUFasHj` | Statusskript; Lauf nicht geprüft |
| `nexus_ssot_mcp.py` | `1pfHmoeAABJKtvh7AIYBQmw0TpsSVqzcE` | SSOT-MCP-Integration; Lauf nicht geprüft |
| `nexus_catalog_sync.py` | `1E2NeNd8zWeSdsJKg2K8qU7-OgsK5c4B-` | Katalog-Sync; Lauf nicht geprüft |
| `sync_to_github_artifacts.py` | `1Szgy8UUrKdziq3fql_zHt6ZcAFCjH0-h` | GitHub-Artefakt-Sync; Lauf nicht geprüft |
| `RFEM6_MCP_Bridge_Extended.py` | `1akNI_TEPT_cKEUx3aFdA6Xh_5emDqYn_` | RFEM-Bridge; Live-Verbindung nicht geprüft |
| `mcp_dispatcher.py` | `1z13nzZ-7jWnY0TEtTDz39nWDuS7VStjN` | Dispatcher; Lauf nicht geprüft |
| `test_hbv_ribbed.json` | `1H741DcgK43eCgaDzYqIeqF82mtixb6t6` | Testdaten-Datei; kein Testlaufbeweis |
| `test_precast_beam.json` | `1KH5Eu581tFaa0z2H-cMcwUBbxuBPGryM` | Testdaten-Datei; kein Testlaufbeweis |
| `ASSET_REGISTRY.csv` | `1GiP2OOU9FsNsgX7geyDCoO5NJU4s8UyP` | Vorhandenes Asset-Verzeichnis |

**Quelle:** https://drive.google.com/drive/folders/1fRa7rQvKi-BkhVIzjXPcY_u8iIJ4Vn5J. Die Dateiexistenz wurde im Ordnerinventar geprüft; keine Behauptung einer lauffähigen Gesamtintegration.

# Anhang D – Governance und Dokumentationsvertrag

## D.1 Hierarchie und Nutzung

Die Reihenfolge wird im Handbuch **erläutert**, nicht neu geregelt: ID01-Entscheidung → CURRENT Manifest → CURRENT Baseline → operative AGBs/WORK-Regeln → WorkOrder und aufgabenspezifische Dokumentation. Bei Konflikten ist der konkrete Geltungsbereich zu prüfen. Der Text des Handbuchs setzt die Originaldateien nicht außer Kraft.

Die vorhandenen Steuerdateien bleiben an ihren Orten. Dieser Anhang bietet Links und beschreibende Auszüge; vollständige, wortgetreue Snapshots sind nur bei Bedarf mit einer eindeutig bezeichneten Quellrevision zu ergänzen.

## D.2 Minimaler Ablaufvertrag für dokumentierte Ausführungen

```text
START_ACK
  actor_role, provider, model_id, runtime_instance,
  read_capabilities, write_capabilities, source_versions

WORKORDER
  intent, scope, inputs, required_evidence,
  deliverables, owner, acceptance_criteria

RUN
  run_id, tool_version, input_identity,
  method, output_identity, checks, failures

REVIEW
  reviewer_identity, independence_basis,
  findings, corrections, residual_risks

PERSISTENCE
  provider_file_id, canonical_uri, version,
  readback_status, hash_scope, registration_status

CLOSURE
  result_status, open_items, human_gate,
  report_link, next_action
```

Das Schema ist eine didaktische Darstellung des bestehenden Vertrags, **kein neues Registry-Schema**. Tatsächlich verbindliche Feldnamen und Statuswerte sind in den Originalen nachzulesen.

## D.3 Dokumentationsregeln für das Strategiepapier

- Haupttext: verständliche Produktbeschreibung und Methodenlogik.
- Tabellen: reale Quellen, Beispiele und Abgrenzungen von Ist-/Soll-Zuständen.
- Anhang: exakte Pfade, Schemas, Status-/Quellenverzeichnis.
- Revisionsmanagement: Strategie-Baseline nach ID01-Freigabe stabil; spätere Änderungen als explizite Revision.
- Keine zusätzlichen kritischen Gates nur wegen dieses Dokuments.
- `REVIEW_PENDING`, `REGISTRATION_PENDING` und `HUMAN_RELEASE_PENDING` bleiben sichtbar, bis die jeweilige Aktion tatsächlich belegt ist.

# Anhang E – Daten- und Schnittstellenmodelle

## E.1 Minimales Quell- und Wissensobjektmodell (didaktischer Kandidat)

```json
{
  "source": {
    "provider": "google_drive",
    "provider_file_id": null,
    "canonical_uri": null,
    "representation_version": null,
    "sha256": null,
    "license_scope": null
  },
  "knowledge_object": {
    "id": null,
    "type": "METHOD",
    "label_de": "Holz-Beton-Verbund – Kervenbemessung",
    "source_locator": null,
    "applicable_standard_edition": null,
    "jurisdiction": "AT",
    "review_status": "REVIEW_PENDING"
  }
}
```

Das Beispiel ist **nicht** in die bestehende Registry geschrieben. `null` ist bewusst gewählt, wo der echte Locator fehlt. Für produktive Nutzung muss der vorhandene Datenvertrag geprüft werden.

## E.2 Berechnungsvertrag (Schnittstellenbeispiel)

```json
{
  "workflow": "engineering_compute",
  "input": {
    "model_id": null,
    "load_cases": [],
    "units": "explicit",
    "material_parameters": [],
    "standard_refs": []
  },
  "execution": {
    "solver_name": null,
    "solver_version": null,
    "method": null,
    "run_id": null
  },
  "output": {
    "results": [],
    "unit_checks": [],
    "equilibrium_checks": [],
    "limit_state_checks": [],
    "validation_status": "NOT_RUN"
  }
}
```

Die Fachsoftware bleibt Rechenautorität. Ein generiertes JSON-Objekt ist keine statische Berechnung; ein numerischer Nachweis verlangt tatsächliche Eingaben, einen ausgeführten Solver und Prüfprotokolle.

## E.3 Prozesslogik: Nachweis vor Status

`SOURCE_IDENTIFIED → INPUT_VALIDATED → METHOD_SELECTED → SOLVER_EXECUTED → CHECKED → INDEPENDENTLY_REVIEWED → ARTIFACT_STORED → REGISTERED → HUMAN_APPROVED`.

Die Pfeile bezeichnen die **fachlich gewünschte Nachweiskette**, nicht einen in diesem TrueRun vollständig nachgewiesenen automatisierten End-to-End-Dienst. Ein Teilprozess darf separat abgeschlossen werden, ohne andere Zustände zu fingieren.

# Anhang F – Open-Access-Rechercheatlas für drei priorisierte Use Cases

**Methodischer Hinweis:** Dies ist eine priorisierte **Quellenstartliste**, keine in diesem Lauf vollständig überprüfte Linkverfügbarkeits- oder Lizenzprüfung. Offizielle Portale und Institutionen werden bevorzugt. Öffentliche Landingpages implizieren keine frei nutzbaren Normvolltexte oder automatischen Downloadrechte.

## F.1 UC-A: Tragwerksplanung / EC2, EC5 und Holz-Beton-Verbund

| Priorität | Quelle | Recherchegegenstand | URL |
|---|---|---|---|
| P1 | JRC Eurocodes | Eurocode-Überblick, Implementierung und offizielle technische Hintergrunddokumentation | https://eurocodes.jrc.ec.europa.eu/ |
| P1 | OIB | Österreichische bautechnische Richtlinien und veröffentlichte Dokumente | https://www.oib.or.at/ |
| P1 | Austrian Standards | Normenidentifikation und Ausgabenrecherche; Volltextzugang gesondert | https://www.austrian-standards.at/ |
| P2 | dataholz.eu | Geprüfte Holzbauteile und bauphysikalische Informationen | https://www.dataholz.eu/ |
| P2 | Informationsdienst Holz | Fachinformationen und Holzbaupublikationen | https://informationsdienst-holz.de/ |
| P2 | Lignum | Schweizer Holzbau-Fachinformationen; nationale Geltung getrennt prüfen | https://www.lignum.ch/ |

**Rechercheprotokoll:** Dokumenttitel, Ausgabe, Geltungsland, Abschnitt, Nutzungsrechte, Quell-ID, Abrufdatum, fachlicher Reviewer. Normenstand vor konkreten EC2-/EC5-/HBV-Bemessungsaussagen prüfen.

## F.2 UC-B: Nachhaltigkeit, Materialdaten, LCA und ReUse

| Priorität | Quelle | Recherchegegenstand | URL |
|---|---|---|---|
| P1 | ÖKOBAUDAT | Ökobilanzdatensätze für Bauprodukte | https://www.oekobaudat.de/ |
| P1 | IBO | Österreichische Bauökologie, Produkt-/Baustoffinformationen | https://www.ibo.at/ |
| P1 | EUR-Lex | EU-Rechtsakte, insbesondere Taxonomie und Nachhaltigkeitsrecht | https://eur-lex.europa.eu/ |
| P2 | EU Level(s) | Europäischer Bewertungsrahmen für nachhaltige Gebäude | https://environment.ec.europa.eu/topics/circular-economy/levels_en |
| P2 | European Platform on LCA | Methodik und Datenkontext der Lebenszyklusanalyse | https://eplca.jrc.ec.europa.eu/ |
| P2 | EC3 / Building Transparency | Embodied-Carbon-Daten- und Vergleichsportal; Nutzungsbedingungen beachten | https://www.buildingtransparency.org/ |

**Datenvertrag:** Produktidentität, deklarierte Einheit, Lebenszyklusmodule, geografische/zeitliche Geltung, EPD-Programm, Datenqualität, Berechnungsmethode und Rechte getrennt dokumentieren. Modul D nicht stillschweigend mit A1–A3 saldieren.

## F.3 UC-C: BIM, IFC, Wissensgraph und Automation

| Priorität | Quelle | Recherchegegenstand | URL |
|---|---|---|---|
| P1 | buildingSMART International | IFC-Standards und openBIM-Spezifikationen | https://www.buildingsmart.org/ |
| P1 | IFC 4.3 Documentation | Schema- und Entitätsreferenz | https://ifc43-docs.standards.buildingsmart.org/ |
| P1 | W3C RDF | Graph-Datenmodell und Web-Semantik | https://www.w3.org/RDF/ |
| P1 | W3C SHACL | Validierung von RDF-Graphen | https://www.w3.org/TR/shacl/ |
| P2 | Python Documentation | Reproduzierbare Python-Ausführung und Standardbibliothek | https://docs.python.org/3/ |
| P2 | GitHub Docs | Versionierung, Pull Requests, Actions und API | https://docs.github.com/ |
| P2 | SQLite Documentation | Datenmodell, Transaktionen, FTS und Backups | https://www.sqlite.org/docs.html |

**Integrationsregel:** IFC-GUID, Provider-Datei-ID, Knowledge-Object-ID und Graph-Node-ID nicht vermischen. Beziehungen sind nur mit geprüfter Semantik und nachvollziehbarer Herkunft produktiv zu übernehmen.

# Anhang G – Quellenregister, Status und offene Nachweise

## G.1 Redaktionsquellen

| Quellenkennung | Beleg | Verwendung |
|---|---|---|
| Q-GOV-01 | [CURRENT Manifest](https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view) | Prinzipien, Rollen, Hierarchie |
| Q-GOV-02 | [CURRENT Baseline](https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view) | Betriebs- und Datenverträge |
| Q-GOV-03 | [AGBs v007.2 – abgerufener Inhalt](https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view) | Operative Regeln, mit Aktivierungsprüfung |
| Q-GOV-04 | [WORK Folder.md](https://drive.google.com/file/d/1nDjF78dq3l8PGpXsauzBz1bzHescDSwv/view) | WORK-Geltungsbereich |
| Q-SEM-01 | [Shared Language & Glossary](https://drive.google.com/file/d/1MnHMlbPgKRNUlSiW7SzRk20EvLrSLEOJ/view) | Begriffe und Statussemantik |
| Q-REV-01 | [ID06 Peer Review](https://drive.google.com/file/d/1vS3KBK9nnBoDVucMqX5OzoEW8_r0KU0M/view) | Normorientierte Gliederung, Didaktik |
| Q-UC-01 | [FT-Träger-Matrix-Bestandsanalyse](https://drive.google.com/file/d/1LrvcfaFBcS6bal3iAC_Codd0Um7Up1tP/view) | Konkrete Entwicklungs- und QA-Befunde |
| Q-UC-02 | [Materialkatalog Usermanual v0.1.1](https://drive.google.com/file/d/1vGaFX_S6qMhiZsvva8F-D-S4Qd9uRrh8/view) | Pilot und Funktionsgrenzen |
| Q-UC-03 | [Control-Panel-Implementierungsplan](https://drive.google.com/file/d/1_nosLpezSN8i-fzTSaNjtnkA-yf11Qfq/view) | Zielarchitektur, Status- und Integrationsgrenzen |
| Q-TOOL-01 | [MCP-ACCESS-TOOLS](https://drive.google.com/drive/folders/1fRa7rQvKi-BkhVIzjXPcY_u8iIJ4Vn5J) | Werkzeugbestand |
| Q-DOS-01 | [Dossier v0.2.0](https://drive.google.com/file/d/1SJQ4WeU5AWWQgLRVQDNxUA9FKujUqWKT/view) | Vorherige Redaktionsbasis |
| Q-REG-01 | [file-registry.jsonl](https://drive.google.com/file/d/15m8T5cWbogIup9snzFwiB1g9HqNCoGow/view) | Registrierungsziel, nicht verändert |

## G.2 Abnahmevorbehalte vor Baseline Rev. 1.0

1. **Fachliche Vollständigkeit:** Redaktionsblöcke 01–05 als einheitliches Dokument integrieren; doppelte Definitionen, Gliederung, Querverweise und normative Formulierungen redaktionell prüfen.
2. **Quellen und Systemstatus:** Alle Aussagen mit realen Fundstellen verknüpfen; historische Testberichte und Zielkonzepte nicht zu Live-Nachweisen hochstufen.
3. **Freigabe und Persistenz:** unabhängiges Kapitelreview, ID01-Freigabe, endgültige Word-Formatierung, Rohbyte-Readback/Hash soweit technisch möglich, Registrierung durch autorisierten Ledger-Schreiber.

## G.3 Abschlusskennzeichnung

**Redaktionsstatus:** `DRAFT_IN_PROGRESS`  
**Technische Freigabe:** `NOT_GRANTED`  
**Registry:** `REGISTRATION_PENDING`  
**Unabhängiger Review dieses Blocks:** `PENDING`  
**ID01-Strategie-Freigabe Rev. 1.0:** `PENDING`

Das Dokument ist als Strategie-, Produkt- und Systemhandbuch konzipiert. Es ersetzt weder gesetzliche Anforderungen noch anwendbare Normen, Fachplanungsleistungen, Solvervalidierung oder projektbezogene Freigaben.
