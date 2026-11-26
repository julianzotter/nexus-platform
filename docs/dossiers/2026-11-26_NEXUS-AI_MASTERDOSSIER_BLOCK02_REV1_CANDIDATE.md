---
name: NEXUS-AI-MASTERDOSSIER-BLOCK02
version: 1.0.0-candidate
status: DRAFT_IN_PROGRESS
created_date: 2026-11-26
author_role: ID03
approved_scope: ID01_APPROVED_WORKPLAN_AND_TOC
release_approval: PENDING
registration_status: REGISTRATION_PENDING
preceding_block: 26_11_26_ID03_NEXUS_MASTERDOSSIER_BLOCK01_REV1_CANDIDATE.md
source_set: [AGBS-v007.2, MANIFEST-CURRENT-2026-09-28, BASELINE-CURRENT-2026-09-28, WORK-Folder-v0.4.0-pilot, ID06-PEERREVIEW-v1.0.0, DOSSIER-v0.2.0]
---
# NEXUS-AI Engineering Knowledge Operations System
## Masterdossier · Redaktionsblock 02 – Kapitel 6–8

**Geltung:** Wissenschaftlich-technischer Entwurf. Die Beschreibung unterscheidet konsequent bestehende Dokumente, konzeptionelle Architektur und verifizierte Laufzeitfunktionen. Der Block führt die Terminologie und Kapitelzählung von Block 01 fort; er ersetzt keine Norm, keine aktuelle Steuerdatei und keine technische Freigabe.

# 6. Systemarchitektur und Datenflüsse

**Kurzfassung.** NEXUS-AI organisiert den Weg von einer menschlichen Aufgabenstellung zu einem überprüfbaren technischen Ergebnis. Vier funktionale Ebenen – Wissen, Berechnung, Verifikation und Orchestrierung – arbeiten unter einer gemeinsamen Governance. Das System ist nicht dadurch zuverlässig, dass ein Sprachmodell besonders überzeugend antwortet, sondern dadurch, dass Quellen, Berechnungen und Entscheidungen getrennt identifizierbar und prüfbar bleiben.

## 6.1 Architektonisches Grundmodell

Die NEXUS-Architektur ist eine **logische Referenzarchitektur**. Sie definiert Verantwortlichkeiten und Schnittstellen, nicht zwingend vier getrennte Server oder Programme. Eine Implementierung kann mehrere Funktionen in einer Runtime bündeln, solange ihre Eingaben, Ausgaben, Zustände und Prüfgrenzen nachvollziehbar bleiben.

| Ebene | Aufgabe | Typische Bausteine | Autorität und Grenze |
|---|---|---|---|
| L1 – Knowledge | Auffinden, strukturieren und verknüpfen von Quellen | Drive, Dokumente, Registry, Suchindex, RAG, Knowledge Graph | Liefert Quellen und Kandidaten; bestimmt keine Normgeltung allein |
| L2 – Compute | Berechnung und Transformation nach expliziten Verfahren | Python, SymPy, Matrixverfahren, Fachsolver, RFEM-Adapter | Rechenautorität nur im validierten Anwendungsbereich |
| L3 – Verification | Unabhängige und regelgebundene Prüfung | Unit-/Integrationstests, Benchmarks, Peer Review, Evidenzprüfung | Prüft Ergebnisse; ersetzt keine menschliche Fachverantwortung |
| L4 – Orchestration | Auftrag verstehen, Komponenten auswählen und Prozess steuern | LLMs, Router, WorkOrders, Agenten, UI, Statussystem | Koordiniert; darf Prüf- und Freigabegates nicht fingieren |

**Governance ist ein Querschnitt** über alle Ebenen: Manifest, Baseline, AGBs, Rollenmatrix, Sicherheitsgrenzen, Ablage- und Berichtsregeln. Die Freigabe durch ID01 ist ein Human Gate und keine fünfte technische Berechnungsebene. Die Formulierung „deterministisches AI-System“ bezeichnet eine deterministisch *geführte* Prozess- und Rechenarchitektur; das Sprachmodell selbst bleibt probabilistisch und kann irren.

## 6.2 End-to-End-Datenfluss

Der Referenzfluss beginnt bei einer Anfrage und endet erst mit einem überprüfbaren Status. Die Prozessschritte sind logisch, nicht immer zeitlich strikt linear: Ein Nutzer kann eine Quelle nachreichen, ein Reviewer kann eine neue Berechnung verlangen, und ein Auftrag kann mit dokumentiertem Teilresultat enden.

```text
ID01 / Anwender / Projektakte
         |
         v
Auftrag und Intent -> Scope, Risiko, Deliverables, Abnahmekriterien
         |
         v
Bootstrap und Source Resolution -> AGBs, Manifest, Baseline, Register
         |
         v
L4 Orchestrierung -> Domäne / Use Case / Workflow / Skill
         |
         +----> L1 Wissen -> Quellen + Fundstellen + Versionen
         |                    |
         +----> L2 Rechnen <--+ Eingaben / Annahmen / Solververtrag
         |                    |
         +----> L3 QA / unabhängiger Review -> Befunde / Grenzen
         |                    |
         v                    v
Ergebnisartefakt + Evidenz + Status + Provenienz
         |
         v
Drive WORK / Fachablage -> Registry -> ggf. GitHub-Review-Snapshot
         |
         v
ID01 / fachliche Freigabe (wenn erforderlich)
```

Die Richtungen `Drive → GitHub` und `GitHub → Drive` sind keine implizite Echtzeitsynchronisation. Jede behauptete Übertragung benötigt einen konkreten Ausführungsbeleg. Das ältere Dossier v0.2.0 nennt denselben Kernfluss als `BOOTSTRAP → INPUT → INTENT → SOURCE_RESOLUTION → PLAN → ... → VERIFY → ... → ARCHIVE → REGISTER → REPORT → HUMAN_RELEASE` [S06].

## 6.3 Steuerlogik als Zustandsmaschine

Eine Zustandsmaschine (Finite State Machine, FSM) verhindert, dass eine Textantwort versehentlich als erfolgreich ausgeführte Aktion gilt. Ein Auftrag kann beispielsweise `OPEN`, `CLAIMED`, `RUNNING`, `REVIEW_REQUIRED`, `BLOCKED`, `DONE` oder `FAILED` sein. Die genaue operative Syntax ist in den aktuellen Originalen zu prüfen; die nachfolgende Darstellung beschreibt die fachliche Logik.

1. **Bootstrap:** Rollen-/Runtime-Identität und aktuelle Steuerquellen prüfen. Bei fehlender kritischer Quelle den betroffenen Schritt als blockiert kennzeichnen.
2. **Auftragsvertrag:** Problem, Ziel, fachliche Domäne, benötigte Quellen, erwartete Ergebnisse und Prüftiefe festlegen.
3. **Reuse-first:** Bestehende Dokumente, Skills, Solver, WorkOrders und Artefakte suchen; keine zweite Wahrheit erzeugen.
4. **Routing:** Fachbegriffe normalisieren und geeignete Domäne, Normenfamilie, Methode und Werkzeuge bestimmen. Mehrdeutige Zuordnungen offenlassen.
5. **Ausführung:** Daten lesen und, falls erforderlich, geprüfte Rechen- oder Transformationstools mit definierten Eingaben ausführen.
6. **Prüfung:** Quelle, Einheiten, Modellannahmen, numerische Ergebnisse und Vollständigkeit kontrollieren; unabhängigen Review dort anfordern, wo Risiko und Regeln es verlangen.
7. **Persistenz:** Artefakt speichern, Ziel und Dateidentität prüfen, Status berichten und Registrierung durch den zuständigen Schreiber veranlassen.
8. **Abschluss:** Nur den belegten Zustand melden. `FILE_CREATED`, `REVIEWED`, `REGISTERED` und `RELEASED` sind verschiedene Ereignisse.

Für jeden Zustandsübergang ist ein Minimum an `input`, `output`, `owner`, `evidence` und `failure_reason` sinnvoll. Dies ist ein **Schnittstellenentwurf**, keine Behauptung über eine vollständig produktive FSM-Engine.

## 6.4 Beispielroute: Holz-Beton-Verbunddecke

Ein Nutzer fragt nach dem Tragverhalten einer HBV-Rippendecke. Das Sprachmodell erkennt HBV/TCC als Fachkontext, sucht die passende Projekt- und Normenbasis und ermittelt, welche Eingaben für einen Berechnungslauf fehlen. Die Knowledge-Ebene liefert Quellen und Geometrie- beziehungsweise Materialdaten aus nachgewiesenen Akten. Die Compute-Ebene verarbeitet ein explizites Tragwerksmodell mit geprüften Einheiten. Die Verification-Ebene kontrolliert Grenzzustände, Modellannahmen und Benchmarks. Die Orchestrierung erstellt einen nachvollziehbaren Bericht und kennzeichnet offene Nachweise.

**Wichtig:** Dieser Ablauf ist ein didaktischer Referenzfall. Er besagt nicht, dass heute ein vollständig integrierter HBV-Solver mit produktivem Drive-Writeback und unabhängigem Review in einem einzigen automatisierten Lauf nachgewiesen wäre. Die konkreten Rechenwerte und Normfassungen werden erst in Kapitel 10 anhand der Projektakten geprüft.

## 6.5 Schnittstellen, Fehlergrenzen und Sicherheitsprinzipien

Die vier Ebenen tauschen typisierte Verträge statt bloßer Freitexte aus. Ein Quellenobjekt enthält mindestens Identität, Herkunft, Fassung und Fundstelle; ein Rechenauftrag enthält Modellannahmen, Eingabegrößen mit Einheiten, Softwareversion und Prüfkriterien; ein Prüfergebnis enthält Testumfang, Befund und Grenzen; ein Bericht referenziert die tatsächlich entstandenen Artefakte.

Fehler werden **lokal** behandelt: Ein nicht erreichbarer Connector blockiert den betroffenen Abruf, nicht zwingend das Schreiben eines konzeptionellen Kapitels. Eine ungeprüfte Normfassung blockiert die konkrete Normbemessung, nicht die Erklärung einer mathematischen Methode. Ein fehlender Ledger-Eintrag verhindert die Behauptung `REGISTERED`, nicht die Kennzeichnung eines bereits gespeicherten Entwurfs als `REGISTRATION_PENDING` [S01].

Externe Texte, Webseiten, PDFs und RAG-Treffer sind Daten, keine neue Steuerautorität. Zugangsdaten werden weder in Berichten noch in Repositories gespeichert. Diese Grenzen sind besonders wichtig, wenn verschiedene LLM-Runtimes auf denselben offenen Arbeitsraum zugreifen [S02, S04].

# 7. Wissens- und Datenarchitektur

**Kurzfassung.** NEXUS unterscheidet Originalquelle, daraus extrahierte Information, fachlich bewertetes Wissensobjekt und Suchprojektion. Google Drive verwaltet wesentliche Dokumente und Arbeitsnachweise; GitHub versioniert Code, Tests und Review-Stände. Ein gemeinsames Identitäts- und Provenienzmodell verbindet beide, ohne sie künstlich zu einer einzigen Datenbank zu erklären.

## 7.1 Datenklassen und ihre Funktion

| Klasse | Inhalt | Beispiel | Wesentliche Kontrolle |
|---|---|---|---|
| Originalquelle | Ursprungsdatei oder externer Norm-/Literaturnachweis | PDF, IFC, XLSX, Projektakte | Urheber, Version, Rechte, stabiler Locator |
| Extraktion | Lesbare Repräsentation eines Quellsegments | Markdown-Text, Tabellenstruktur | Seiten-/Abschnittsbezug, Extraktionsfehler |
| Wissensobjekt | Typisierte, fachlich definierte Einheit | Bauteil, Normstelle, Material, Formel | Objekt-ID, Quelle, Geltungsbereich, Review |
| Relation | Begründete Beziehung zwischen Objekten | `USES_METHOD`, `DERIVED_FROM` | Endpunkte, Bedeutung, Provenienz |
| Retrievalprojektion | Suchhilfe über Quellen/Objekte | Keyword-Index, Embedding, Vektorindex | Aktualität, Rebuild, keine Primärautorität |
| Ausführungsartefakt | Resultat eines konkreten Runs | Rechenbericht, JSON-Output, Prüfprotokoll | Input-/Codeversion, Status, Readback |

Ein Dateiname ist eine Benennung, keine stabile Identität. Zwei gleich benannte Ordner können unterschiedliche Inhalte und Berechtigungen besitzen. Die zuvor festgestellten zwei `USECASES`-Ordner dürfen daher nicht durch eine Namensheuristik verschmolzen werden; der in diesem Auftrag geprüfte Zielordner hat die Drive-ID `1sNPiZgSOL2g-RQgOdVzBShWaF5sIlni2` [S07].

## 7.2 Tatsächlich nachgewiesene Hauptspeicherorte

| Ort | Funktion | Verifizierter Locator |
|---|---|---|
| `_developement` | Projektroot | `gdrive:1OIyJI6rljIi8zNsT-iwg47NsuguoZqTB` |
| `LLM-LOCAL-SSOT` | Steuerdateien und gemeinsame Systemreferenzen | `gdrive:1j3FLJkWpQv6xGA_KO0D9sMyA11f0vxBV` |
| `LLM-LOCAL-SSOT/WORK` | WorkOrders, Reports, Review- und Arbeitsartefakte | `gdrive:1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP` |
| `USECASES` (direktes Kind des Roots) | Fachliche Anwendungsfälle und dieses Dossier | `gdrive:1sNPiZgSOL2g-RQgOdVzBShWaF5sIlni2` |
| `MCP-ACCESS-TOOLS` | Zugriffs-/Tool-Integrationsbereich | `gdrive:1fRa7rQvKi-BkhVIzjXPcY_u8iIJ4Vn5J` |
| `julianzotter/nexus-platform` | Repository für Code, Tests, Dokumentations-Reviews | `https://github.com/julianzotter/nexus-platform` |

Diese Tabelle beschreibt die **nachgewiesenen Speicherorte**, nicht eine pauschale Bestätigung, dass alle Unterordner, Skills oder Automationen synchronisiert sind. Für `REGISTRY`, `SKILLS`, `SCRIPTS` und Indizes müssen die tatsächlichen Eltern-IDs und aktuellen Inventare im späteren Implementierungs- und Verzeichnisatlas-Kapitel separat verifiziert werden. Der Dateipfad allein beweist weder Laufzeitfunktion noch Synchronisation.

## 7.3 Autorität nach Objektklasse

NEXUS benötigt keine einzige physische Datenbank für alle Informationen. Eine sinnvollere Lösung ist eine **föderierte SSOT** mit klarer Zuständigkeit: Originale und fachliche Dokumente in ihren kanonischen Drive-Orten; Code und Tests im versionierten Repository; Arbeits- und Statusartefakte in WORK; Suchindizes als ableitbare Projektionen. Die konkreten Steuerdateien bestimmen, welche Objektklasse wo verbindlich ist [S01–S04].

Ein persönlicher ChatGPT-Memory-Eintrag ist ein **Kontextsignal** für Präferenzen oder Interessen, kein Beweis für einen aktuellen Projektstand. Die LLM-Ausgabe ist ein **Interpretationskandidat**, kein Ersatz für den Originalquelltext. Bei widersprüchlichen Versionen entscheidet nicht das jüngste Dateidatum allein, sondern die von ID01 freigegebene Autoritätskette [S02–S03].

## 7.4 Ingest und Retrieval

Die geplante Wissenspipeline umfasst die folgenden Verarbeitungsschritte:

1. **Discovery:** Dokument oder Datensatz identifizieren und auf vorhandene Registereinträge prüfen.
2. **Provenienz:** Quell-ID, Repräsentation, Ausgabe, Rechte, Sprache, Speicherort und gegebenenfalls Prüfsumme erfassen.
3. **Extraktion:** Text, Tabellen, Formeln und strukturierte Felder mit stabilen Lokatoren erschließen.
4. **Segmentierung:** Abschnitte in sinnvolle, nachvollziehbare Einheiten aufteilen; Tabellen und Formeln nicht willkürlich zerstückeln.
5. **Kandidatenbildung:** Begriffe, Bauteile, Materialien, Normen, Methoden und Relationen als Vorschläge extrahieren.
6. **Prüfung:** Identität, fachliche Bedeutung, Geltungsbereich, Dubletten und Quellverknüpfung prüfen.
7. **Registrierung:** Freigegebene Objekte im vorhandenen Register nachführen, nicht in einem konkurrierenden neuen Masterindex.
8. **Indexprojektion:** Keyword-, Graph- oder Vektorsuche auf Basis registrierter Inhalte aktualisieren; Rebuild-Fähigkeit vorsehen.

Die Reihenfolge `IDENTITY_BEFORE_SEMANTICS` schützt vor einem typischen Fehler: Zwei ähnlich klingende Begriffe sind nicht automatisch dieselbe Normstelle. Ein Vektor-Treffer ist ein Kandidat für den Quellenabruf; erst die überprüfte Fundstelle kann eine technische Aussage stützen. `RETRIEVAL_BEFORE_RAG` bedeutet deshalb: vorhandene verlässliche Verzeichnisse und exakte Suche vor aufwendiger semantischer Neugenerierung [S02–S03].

## 7.5 Wissensobjekte und Knowledge Graph

Ein Knowledge Object erhält eine stabile ID, einen Typ, eine kanonische Bezeichnung, Synonyme, Fachdomänen, einen Quellenbezug und einen Prüfstatus. Typen können `STANDARD`, `MATERIAL`, `COMPONENT`, `METHOD`, `USECASE`, `WORKFLOW`, `SKILL`, `SOURCE`, `EVIDENCE` oder `ARTIFACT` sein. Die Relationen müssen semantisch unterscheidbar bleiben: `IS_A` beschreibt eine Klassenzugehörigkeit, `PART_OF` eine Teil-Ganzes-Beziehung, `DERIVED_FROM` eine belegte Ableitung und `VALIDATED_BY` einen konkreten Prüfnachweis [S06].

Beispiel einer **konzeptionellen** Relation:

```text
USECASE: HBV-Rippendecke
  REQUIRES      -> SOURCE: Projektgeometrie
  REFERENCES    -> STANDARD: zutreffende EC-/TS-Fassung
  USES_METHOD   -> METHOD: Verbundmodell
  EXECUTES_WITH -> TOOL: geprüfter Rechenkern
  VALIDATED_BY  -> EVIDENCE: Benchmark/Peer-Review
  PRODUCES      -> ARTIFACT: Nachweisbericht
```

Die Pfeile sind ein Vorschlag für ein Datenmodell, keine Behauptung, dass genau diese Kanten bereits produktiv registriert sind. Quellenlose Kanten bleiben `REVIEW_PENDING`; `SAME_AS` verlangt eine echte Identitätsprüfung.

## 7.6 Datenintegrität, Versionierung und Synchronisation

Für einen überprüfbaren Artefakttransfer sind mindestens Ausgangsidentität, Zielidentität, Quellversion, Transportereignis und ein Readback erforderlich. Für den vollen Rohbyte-Nachweis ist ein SHA-256-Vergleich über exakt dieselbe Repräsentation notwendig. Eine GitHub-Blob-SHA ist nicht identisch mit einer SHA-256-Prüfsumme des Dateiinhalts. Auch ein erfolgreicher Textvergleich ersetzt keine vollständige Byteprüfung [S01].

Das bestehende `file-registry.jsonl` ist als Registrierungsziel vorgesehen. Die aktuelle AGB-Fassung bezeichnet einen einzigen delegierten Ledger-Schreiber; dieser Redaktionslauf erzeugt **keine eigene Ledger-Nummer**. `REGISTRATION_PENDING` ist ein zulässiger ehrlicher Status. Ein neues globales Indexsystem oder eine automatische bidirektionale Sync-Behauptung ist ausdrücklich nicht Bestandteil dieses Dossiers.

## 7.7 Zugriff, Rechte und Schutzbedarf

Nicht jedes Dokument darf in denselben öffentlichen Kanal. Normvolltexte, projektspezifische Unterlagen, personenbezogene Daten und Zugangsdaten unterliegen unterschiedlichen Rechten. Eine öffentliche Codeablage darf nur solche Quelltexte und Auszüge enthalten, für die die erforderlichen Nutzungsrechte bestehen. Die WORK-Folder-Dokumentation beschreibt bewusst offene Zusammenarbeit und daraus folgende Risiken bei Provenienz und Überschreibbarkeit [S04]. Die Systemarchitektur muss diese Risiken offen benennen, ohne aus dem Benutzerhandbuch ein neues Berechtigungsreglement zu machen.

# 8. Rechen- und Nachweislogik

**Kurzfassung.** Eine technische Berechnung wird erst dann belastbar, wenn Modell, Eingaben, Einheiten, Rechenmethode, Softwareversion und Prüfergebnis zusammenpassen. NEXUS verwendet LLMs für Interpretation und Orchestrierung; die mathematische Ausführung erfolgt in nachvollziehbarem Code oder geeigneter Fachsoftware. Die fachliche Abnahme bleibt ein eigener Schritt.

## 8.1 Trennung der Verantwortlichkeiten

Ein Sprachmodell kann eine Aufgabenstellung strukturieren, fehlende Randbedingungen erkennen, relevante Methoden vorschlagen und einen Bericht sprachlich aufbereiten. Es soll jedoch weder einen nicht ausgeführten Solverlauf behaupten noch aus plausibel klingenden Zahlen einen geprüften Standsicherheitsnachweis ableiten. Ein Python-Programm kann mathematisch deterministisch sein und trotzdem ein falsches Tragwerksmodell oder unzutreffende Normannahmen enthalten. Deshalb braucht NEXUS sowohl **Compute** als auch **Verification** [S02–S03].

## 8.2 Rechenvertrag (Compute Contract)

Jeder numerische Run sollte einen expliziten Vertrag besitzen:

| Feld | Bedeutung |
|---|---|
| `model_id` / `model_version` | Geometrie, Lagerung, Freiheitsgrade, Systemgrenzen |
| `input_set` | Lasten, Materialien, Querschnitte, Verbindungen, Parameter |
| `unit_system` | Deklarierte Größen und Umrechnungen |
| `standard_refs` | Anwendbare Normen, nationale Anhänge, Ausgaben und Fundstellen |
| `method_id` | Gleichungssystem, numerisches Verfahren oder Solvermodell |
| `software_version` / `code_sha` | Tatsächlich verwendeter Rechenkern |
| `run_id` / `timestamp` | Identität der Ausführung |
| `result_set` | Rohwerte, Grenzwerte, Ausnutzungen und Fehlermeldungen |
| `qa_evidence` | Testfälle, Residuen, Vergleichsrechnung, Review |

Dies ist ein **empfohlenes Schnittstellenschema**, nicht der Nachweis, dass sämtliche vorhandenen Python-Skripte bereits dieselben Felder implementieren.

## 8.3 Mathematische Konsistenz und Einheiten

Eine Dimensionierung beginnt mit der Festlegung von Größen, Symbolen, Einheiten und Vorzeichenkonventionen. Für lineare statische Systeme sind Gleichgewichtsbedingungen grundlegende Prüfungen, beispielsweise `ΣF_x = 0`, `ΣF_y = 0` und `ΣM = 0` für ein ebenes Modell. Für räumliche Systeme treten die entsprechenden drei Kraft- und drei Momentengleichgewichte hinzu. Eine kleine Gleichgewichtsabweichung belegt noch nicht die Richtigkeit von Steifigkeiten, Lagerannahmen oder Bemessungsregeln.

Die interne Wahl von N–mm–N/mm² oder konsistenten SI-Einheiten ist eine Implementierungsentscheidung. Kritisch ist, dass Umrechnungen explizit, dimensionsrichtig und getestet sind. Beispielsweise gilt `1 kN = 1 000 N` und `1 MPa = 1 N/mm²`. Ein Wert ohne eindeutige Einheit wird nicht stillschweigend als Normeingabe verwendet.

## 8.4 Normbezogene Prüfung

Für Tragwerksaufgaben in Österreich sind Normenfamilie, Ausgabe, nationale Festlegungen, rechtlicher Geltungsbereich und projektspezifische Randbedingungen getrennt zu bestimmen. Für die exemplarische HBV-Decke können EN 1990, EN 1991, EN 1995, CEN/TS 19103 sowie projektspezifische Vorgaben relevant sein. Daraus folgt **nicht**, dass jede dieser Fassungen im konkreten Projekt automatisch verbindlich ist. Für Beton- und Holzanteile sowie die Verbindung sind die tatsächlich anwendbaren Regelwerke und Nachweismethoden anhand der Originalquellen zu bestätigen [S05].

Die Prüfung gliedert sich in: (a) Lastannahmen und Kombinationen; (b) Tragmodell und Werkstoffannahmen; (c) Tragfähigkeit und Gebrauchstauglichkeit; (d) konstruktive Randbedingungen; (e) Robustheit und gegebenenfalls Brand-/Schwingungsanforderungen; (f) nachvollziehbare Ergebnisdarstellung. Die Reihenfolge ist ein allgemeines Prüfgerüst und keine Wiedergabe eines konkreten Eurocode-Abschnitts.

## 8.5 Mehrstufige Validierung

**Stufe A – Eingabeprüfung:** Geometrie plausibel, Materialkennwerte mit Quelle, Vorzeichen und Einheiten konsistent, Pflichtfelder vollständig. **Stufe B – Rechenprüfung:** Reproduzierbarer Lauf, Residuen, Konvergenz und numerische Stabilität. **Stufe C – fachlicher Vergleich:** Handrechnung, unabhängiges Verfahren, validierter Referenzfall oder geeigneter Benchmark. **Stufe D – Norm-/Projektprüfung:** maßgebende Kombinationen, Grenzwerte und Geltungsbereich. **Stufe E – Peer Review:** unabhängige fachliche Beurteilung von Annahmen und Ergebnissen, soweit der Risikoumfang dies verlangt. **Stufe F – Freigabe:** fachlich zuständige Person entscheidet über die Verwendbarkeit.

Ein Toleranzziel wie `Δ ≤ 5 %` kann für einen definierten Vergleich sinnvoll sein, ist aber **kein universeller Grenzwert** für jede FE-Berechnung, jedes Bauteil und jede Norm. Toleranzen sind methoden- und anwendungsabhängig festzulegen. Tests müssen zudem erkennen, wenn zwei Rechenwege dieselbe fehlerhafte Annahme teilen.

## 8.6 Reproduzierbarkeit und deterministische Ausführung

Reproduzierbarkeit erfordert mehr als `temperature = 0` für ein LLM. Für Rechenkerne müssen Eingabedateien, Codeversion, Bibliotheken, Solveroptionen, Plattformabhängigkeiten und Rundungskonventionen hinreichend fixiert werden. Numerische Parallelisierung oder iterative Algorithmen können kleine Abweichungen verursachen; daher werden geeignete Toleranzen und Prüfgrößen dokumentiert. Ein Rechenbericht sollte die tatsächliche Ausführungsumgebung nennen und darf nicht aus einer geplanten Skriptdatei auf einen erfolgreichen Lauf schließen.

## 8.7 HBV-Beispiel als durchgehender Prüfpfad

Das HBV-Beispiel aus Kapitel 6 wird in eine konkrete Prüfsequenz übersetzt:

1. **Input:** Spannweite, Platten- und Rippengeometrie, Materialien, Verbindergeometrie, Lasten und Lagerung aus identifizierten Projektquellen.
2. **Source Resolution:** gültige Normen und projektspezifische Bemessungsgrundlagen mit Ausgabe und Fundstelle bestimmen.
3. **Method:** Tragmodell für den nachgiebigen Verbund auswählen und die Annahmen der gewählten Methode offenlegen.
4. **Compute:** Steifigkeiten, Schnittgrößen, Spannungen, Verbinderkräfte und Verformungen mit dokumentiertem Rechenkern berechnen.
5. **Verification:** Grenzzustände, Einheiten, Gleichgewicht, Plausibilität, Vergleichsverfahren und gegebenenfalls Schwingung/Brand prüfen.
6. **Output:** Rechenbericht mit Eingaberegister, Quellen, Formeln, Ergebnissen, QA-Befunden, offenen Punkten und fachlichem Freigabestatus.

Hier werden bewusst **keine Bemessungszahlen** erfunden. Der ausführliche Referenzfall in Kapitel 10 wird erst mit verifizierten Projektdateien, Normfassungen und einem echten Solverlauf vervollständigt. So bleibt der Leitfaden anschaulich, ohne eine simulierte Rechnung als TrueRun auszugeben.

## 8.8 Fehlerbilder und Abnahmekriterien

Häufige Fehler sind verwechselte Lastfälle, falsche Einheiten, unklare nationale Anhänge, fehlende Lagerannahmen, unzulässige Interpolation, unvollständige Grenzzustände, veraltete Solverversionen oder falsch zugeordnete Benchmark-Ergebnisse. Die Software soll solche Fehler möglichst früh erkennen, verständlich melden und den jeweiligen Prüfstatus begrenzen.

Als Mindestnachweis für die **Abnahme eines konkreten Rechenkerns** gelten: definierter Scope, dokumentierte Eingaben, reproduzierbarer Testlauf, fachlich geeignete Referenzfälle, bestandene Einheiten-/Plausibilitätschecks, Versionierung, nachvollziehbare Fehlerbehandlung und verantwortliche Freigabe. Das ist eine vorgeschlagene Engineering-QA-Baseline; sie ersetzt nicht projektspezifische gesetzliche oder normative Anforderungen.

# Quellen- und Evidenzverzeichnis für Block 02

- **[S01]** NEXUS-AGBs v007.2 (gelesener Stand, Aktivierungsvermerk noch zu klären): https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view
- **[S02]** CURRENT Manifest, Basis 2026-09-28, Rollenregister v1.2: https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view
- **[S03]** CURRENT Baseline Instructions: https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view
- **[S04]** WORK Folder.md v0.4.0-pilot: https://drive.google.com/file/d/1nDjF78dq3l8PGpXsauzBz1bzHescDSwv/view
- **[S05]** ID06 Peer Review v1.0.0, Empfehlungen: https://drive.google.com/file/d/1vS3KBK9nnBoDVucMqX5OzoEW8_r0KU0M/view
- **[S06]** NEXUS-Systemdossier v0.2.0-candidate, vorheriger Entwurf: https://drive.google.com/file/d/1SJQ4WeU5AWWQgLRVQDNxUA9FKujUqWKT/view
- **[S07]** USECASES, im Auftrag verwendeter Drive-Ordner: https://drive.google.com/drive/folders/1sNPiZgSOL2g-RQgOdVzBShWaF5sIlni2

# Redaktions-QA und Übergabe

- **Kapitelabdeckung:** 6, 7, 8 vollständig als konzeptionelle Erstfassung; Kapitel 1–5 bleiben in Block 01.
- **Fachliche Grenze:** Keine Live-Bemessung und kein vollständiger Solver-E2E-Test durchgeführt; keine Produktionsreife behauptet.
- **Konsistenz:** Vier Ebenen; Governance als Querschnitt; gleiche SSOT- und Quellenbegriffe wie Block 01.
- **Offene Punkte:** Exakte Inventur aller SKILLS-/SCRIPTS-/REGISTRY-Pfade; kanonische Governance-Aktivierung; tatsächliche HBV-Solver- und Benchmarkdateien; Ledgerregistrierung; unabhängiger Review; Word-Baseline.
- **Fortsetzung:** Block 03 – Kapitel 9–11: Getting Started, reale Use Cases, Implementation Guide.
