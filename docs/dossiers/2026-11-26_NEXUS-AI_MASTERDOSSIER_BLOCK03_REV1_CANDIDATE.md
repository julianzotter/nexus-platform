---
name: NEXUS-AI-MASTERDOSSIER-BLOCK03
version: 1.0.0-candidate
status: DRAFT_IN_PROGRESS
created_date: 2026-11-26
author_role: ID03
approved_scope: ID01_APPROVED_WORKPLAN_AND_TOC
release_approval: PENDING
registration_status: REGISTRATION_PENDING
preceding_blocks:
  - 26_11_26_ID03_NEXUS_MASTERDOSSIER_BLOCK01_REV1_CANDIDATE.md
  - 26_11_26_ID03_NEXUS_MASTERDOSSIER_BLOCK02_REV1_CANDIDATE.md
source_set:
  - AGBS-v007.2 (Drive 10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg)
  - MANIFEST-CURRENT-2026-09-28 (Drive 1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn)
  - BASELINE-CURRENT-2026-09-28 (Drive 1CdwNHr6i8lMG3k8A939kiznLMw8q7J69)
  - WORK-Folder-v0.4.0-pilot (Drive 1nDjF78dq3l8PGpXsauzBz1bzHescDSwv)
  - ID06-PEERREVIEW-v1.0.0 (Drive 1vS3KBK9nnBoDVucMqX5OzoEW8_r0KU0M)
  - MCP-ACCESS-TOOLS-USECASE_REGISTRY (Drive 1kkB5prWZ7mf6a0HcJwBOoANRtDbTWS9w)
  - MCP-ACCESS-TOOLS-README (Drive 1a6nh2KwpcI3kVNHJc1okt4ibL7YErDFA)
  - USECASES-FOLDER-INVENTORY (Drive 1sNPiZgSOL2g-RQgOdVzBShWaF5sIlni2)
---
# NEXUS-AI Engineering Knowledge Operations System
## Masterdossier · Redaktionsblock 03 – Kapitel 9–11

**Redaktionsstand:** 26. November 2026. Dieser Block beschreibt einen nachvollziehbaren Einstieg, nachgewiesene Bestandsobjekte und einen abnahmefähigen Implementierungspfad. Die Existenz einer Datei, eines Skripts oder einer Registerzeile beweist noch keine ausführbare Ende-zu-Ende-Integration. Ausgewiesene Teststände sind quellenbezogene Berichte, keine in diesem Redaktionslauf wiederholten Funktionstests.

# 9. Getting Started – Benutzerhandbuch

**Kurzfassung.** Der Einstieg in NEXUS-AI beginnt nicht mit der Installation einer weiteren Plattform, sondern mit einer konkreten Aufgabe. Das System hilft, vorhandene Quellen und Werkzeuge wiederzufinden, die Aufgabe in einen überprüfbaren Ablauf zu überführen und Ergebnisse mitsamt ihrer Herkunft zu dokumentieren. Der Anwender muss dafür weder die gesamte Ordnerstruktur noch die technischen Schnittstellen kennen.

## 9.1 Was ein Anwender als Erstes wissen muss

NEXUS-AI ist ein Assistenz- und Operationsrahmen für Engineering und Wissensarbeit. Eine Anfrage kann eine Normenrecherche, ein Bauteilnachweis, eine Variantenstudie, die Kontrolle einer Excel-Matrix, ein Datenbankabgleich oder ein Softwareentwicklungsauftrag sein. Die Bearbeitung folgt derselben Grundlogik:

1. **Aufgabe benennen.** Was soll entschieden, berechnet, geprüft oder erzeugt werden?
2. **Kontext und Quellen klären.** Welches Projekt, welche Dokumentfassung, welche Fachdomäne und welcher räumlich-zeitliche Geltungsbereich sind maßgebend?
3. **Vorhandenes suchen.** Gibt es bereits ein geeignetes Dokument, einen Workflow, eine Berechnung, einen Skill oder eine Softwarekomponente?
4. **Geeignetes Werkzeug ausführen.** LLMs helfen beim Verstehen, Suchen und Strukturieren; Fachsolver und geprüfter Code übernehmen die jeweils geeignete deterministische Berechnung.
5. **Ergebnis prüfen.** Sind Eingangsdaten, Annahmen, Formeln, Quellen, Einheiten und Ausgaben nachvollziehbar? Wo ist eine unabhängige Kontrolle nötig?
6. **Ergebnis sichern und Status nennen.** Ein Artefakt ist erst dann eine belegte Lieferung, wenn sein Speicherort und seine Identität feststehen. Registrierung, Review und fachliche Freigabe sind zusätzliche, voneinander getrennte Zustände.

Die Schritte sind keine Pflicht, für jede einfache Wissensfrage einen vollständigen Softwareprozess auszulösen. Die Prüftiefe richtet sich nach Risiko und Zweck. Eine unverbindliche Begriffsdefinition braucht weniger Kontrolle als eine tragwerksrelevante Bemessung oder ein produktiver Code-Release.

## 9.2 Schnellstart in fünf Minuten

**Beispielanfrage:** „Prüfe für eine HBV-Rippendecke die vorhandenen Berechnungsgrundlagen, ermittle den maßgebenden Normen- und Methodenstand und erstelle einen nachvollziehbaren Prüfplan. Keine Bemessungsfreigabe.“

Das System sollte zuerst das vorhandene HBV-/EC5-Material auffinden, statt sofort eine neue Rechenformel zu erfinden. Es trennt dabei drei Ergebnisse:

- **Gefunden:** Ein Dokument, eine Tabelle oder ein Skript wurde mit konkreter Datei-ID beziehungsweise Repository-Pfad lokalisiert.
- **Geprüft:** Die Eignung der Quelle oder der Code wurde im angegebenen Umfang tatsächlich überprüft.
- **Freigegeben:** Die fachlich verantwortliche Stelle hat das Ergebnis für einen bestimmten Verwendungszweck ausdrücklich angenommen.

Der Anwender erhält eine kurze Antwort mit Quellen und dem nächsten erforderlichen Schritt. Bei fehlenden Eingaben, Normfassungen oder Prüfnachweisen wird die Lücke benannt, nicht mit plausibel klingenden Werten gefüllt.

## 9.3 Wo finde ich was?

| Frage | Einstieg | Tatsächlich geprüfter Bezug | Grenze |
|---|---|---|---|
| Welche Systemregeln gelten? | `LLM-LOCAL-SSOT` | Manifest, Baseline und AGBs; Quellen [S01–S03] | Aktivierungs-/Versionskonflikte bleiben zu prüfen |
| Welche Arbeiten laufen? | `LLM-LOCAL-SSOT/WORK` | WORK-Folder-Regel [S04] | Dateiabgabe ≠ Agenten-ACK |
| Welche Anwendungsfälle gibt es? | `_developement/USECASES` | Verzeichnis [S05] | Zwei gleichnamige Ordner sind nicht durch Namen unterscheidbar |
| Welche MCP-Werkzeuge gibt es? | `_developement/MCP-ACCESS-TOOLS` | README und Dateiinventar [S06] | Vorhandener Quellcode ≠ funktionierender Connector |
| Welche Software ist versioniert? | GitHub `julianzotter/nexus-platform` | Repository [S07] | Ein Branch/PR beweist keinen Deploy |
| Wie werden Use Cases klassifiziert? | `USECASE_REGISTRY.md` | Historisches kollaboratives Register [S08] | Historische ACTIVE-Labels sind kein Live-Run-Nachweis |

**Praktische Regel:** Für eine Fachfrage zunächst Fachquelle und Use Case prüfen; für einen Systemauftrag zuerst die aktuellen Steuerdateien und den WORK-Kontext. Ein Benutzerhandbuch muss die Regeltexte nicht vollständig im Hauptteil wiederholen.

## 9.4 Bedienung für Anwender, Ingenieure und Entwickler

**Anwender:** Formuliert ein Ziel und verlangt ein überprüfbares Ergebnis. Die Orchestrierung identifiziert die wahrscheinlich passende Route. Fehlende Pflichtdaten werden gezielt nachgefragt.

**Ingenieur:** Prüft zusätzlich Tragmodell, Material, Lastannahmen, Normausgabe, nationale Festlegungen, Grenzzustände und die Qualität der Rechenverfahren. Die Verantwortung für die fachliche Verwendung bleibt beim zuständigen Ingenieur.

**Entwickler:** Prüft zusätzlich Schema, API-Vertrag, Fehlerfälle, Abhängigkeiten, Testdaten, Codeversion, CI-Ergebnisse und die sichere Rückgabe in die NEXUS-Ablage. Ein neues Skript wird nicht allein durch das Ablegen im Repository zu einer freigegebenen Systemfunktion.

## 9.5 Durchgehender Referenzablauf: Holz-Beton-Verbunddecke

Der folgende Ablauf illustriert die Systemlogik. Er ist **kein ausgeführter Tragfähigkeitsnachweis** und keine Aussage, dass ein vollständiger HBV-Solver produktiv verbunden ist.

**A. Intent und Scope.** Zu untersuchen ist eine HBV-Rippendecke. Zunächst wird festgelegt, ob die Aufgabe eine Quellenrecherche, ein Rechenmodell, ein Vergleich zweier Verfahren oder eine vollständige Bemessung betrifft.

**B. Wissensabruf.** Gesucht werden Geometrie, Materialkennwerte, Einwirkungen, Nachweisziele, Verbunddetails, maßgebende Normen und die für das Projekt gültigen Ausgaben. EN 1990/1991, EC5 mit österreichischen Festlegungen sowie CEN/TS 19103 sind Kandidaten; ihre konkrete Anwendbarkeit wird im Projektkontext geprüft. Normvolltext wird nicht aus dem Gedächtnis rekonstruiert.

**C. Methodenauswahl.** Für geeignete Systeme werden analytische Näherungen (beispielsweise die Gamma-Methode) und diskrete Verbindermodelle als mögliche Vergleichswege beurteilt. Die Wahl setzt die Modellvoraussetzungen und die richtige Verbundsteifigkeit voraus.

**D. Deterministische Berechnung.** Geprüfter Code oder Fachsoftware verarbeitet versionierte Eingaben. Einheiten und Modellannahmen werden explizit kontrolliert; Ergebnisse werden mit dem passenden Rechenkern und dessen Versionsstand verknüpft.

**E. Kontrolle.** Geometrie, Randbedingungen, Lastkombinationen, Spannungen, Verformungen, Schwingung und gegebenenfalls Brandbeanspruchung werden gegen die jeweils anwendbaren Nachweiskriterien geprüft. Eine unabhängige Vergleichsrechnung oder Peer Review ist bei tragwerksrelevanten Ergebnissen erforderlich.

**F. Artefakt und Entscheidung.** Das Ergebnis wird mit Fundstellen, Input- und Codeversion, Berechnung, Findings und Status gespeichert. Ohne tatsächliche Ausführung lautet der Status „Konzept/Prüfplan“, nicht „Bemessung bestanden“.

## 9.6 Was NEXUS bewusst nicht verspricht

NEXUS ersetzt keine aktuelle Normenlizenz, keine verantwortliche Tragwerksplanung, keine Baustellenprüfung und keine verbindliche Rechtsauskunft. Ein LLM kann eine Fachfrage plausibel beantworten und trotzdem eine falsche Normfassung, unzutreffende Formel oder veraltete Projektzahl verwenden. Deshalb sind Quellenidentität, gültige Eingaben und verifizierbare Ausführung wichtiger als die sprachliche Sicherheit der Antwort.

# 10. Engineering-Use-Cases und Referenzabläufe

**Kurzfassung.** Die vorhandene Ablage zeigt reale fachliche Projekte und Softwarepiloten. Sie zeigt aber nicht automatisch einen vollständigen, einheitlich freigegebenen Use-Case-Katalog. NEXUS ordnet deshalb **Ordnerobjekte**, **registrierte Workflows**, **Quellartefakte** und **tatsächlich ausgeführte Funktionen** getrennt zu. Erst die belegte Verbindung macht aus einer Sammlung von Dateien einen wiederholbaren Use Case.

## 10.1 Bestandsinventar: der tatsächlich gelesene USECASES-Ordner

Für dieses Dossier wurde der Drive-Ordner mit der ID `1sNPiZgSOL2g-RQgOdVzBShWaF5sIlni2` gelesen [S05]. Er enthält zum Stichtag der Abfrage **neun direkte Unterordner und zwei Markdown-Dateien**. Die Unterordner lauten:

| Ordner | Nachgewiesener Gegenstand | Quellenstatus | Nächster fachlicher Prüfschritt |
|---|---|---|---|
| `FT_TRÄGER_MATRIX` | Bestandsanalyse der Fertigteilträger-Matrix | Analyse-Datei gelesen [S09] | Solver-/Workbook-Golden-Cases prüfen |
| `HTML-DASHBOARD-INVENTAR` | Dashboard-Inventar | Ordner nachgewiesen [S05] | Inhalt und Deployment nachprüfen |
| `Interactive-AI-Studio-Apps` | AI-Studio-Anwendungen | Ordner nachgewiesen [S05] | Apps und Laufzeitstatus erfassen |
| `CONTROL-PANEL` | NEXUS Control Panel | Implementierungsplan gelesen [S10] | Feed, E2E und Hosting belegen |
| `OLLAMA` | Lokale LLM-Umgebung | Ordner nachgewiesen [S05] | Installierte Modelle/Runtime nachprüfen |
| `LV_EISTEICHE_LB-HB` | Ausschreibungs-/Leistungsbeschreibungsunterlagen | Ordner und zwei Dateien nachgewiesen [S05] | Projektspezifische Inhalte und Berechtigung prüfen |
| `MATERIALKATALOG` | Materialatlas und Kreislaufdaten | Handbuch v0.1.1 gelesen [S11] | Pilot gegen reale Daten und Tests abnehmen |
| `Galleria_EKZ_BZ` | Projekt-/Use-Case-Ablage | Ordner nachgewiesen [S05] | Projektauftrag und Inhalte erfassen |
| `SQE_L1` | Projekt-/Use-Case-Ablage | Ordner nachgewiesen [S05] | Projektauftrag und Inhalte erfassen |

Zusätzlich liegen im Ordner die ID06-Peer-Review-Stellungnahme und ein früheres NEXUS-Systemdossier. Beide sind **Dokumentationsartefakte**, nicht automatisch Engineering-Anwendungsfälle. Der vom Benutzer erwähnte zweite gleichnamige USECASES-Ordner ist hier nicht als identisch oder konkurrierend klassifiziert; seine ID und Beziehung müssen gesondert belegt werden.

## 10.2 Ergänzende historische Workflow-Registry

Das tatsächlich gelesene `MCP-ACCESS-TOOLS/USECASE_REGISTRY.md` enthält **17 Workflows** mit Kennungen `WFL-2026-0001` bis `WFL-2026-0017` [S08]. Beispiele sind Cloud-Inventar, FT-Planprüfung, Excel-Nachweis-Audit, Seilstatik, Windlast-Inventar, Eurocode-GPT-Knowledge-Pack, DXF-Zeichnung, Literaturrecherche und Multi-LLM-Gateway. Die Registereinträge sind ein **historischer, kollaborativer Stand vom September 2026**. Der dortige Zustand `ACTIVE` ist keine aktuelle Betriebszertifizierung. Das Register wird nicht durch eine neue parallele Liste ersetzt; dieses Kapitel ist nur eine lesbare Projektion.

## 10.3 Referenzfall A: FT-Träger-Matrix – EC2 und Datenprüfung

**Ziel.** Eine bestehende Excel-Bemessungsmatrix für Fertigteilträger systematisch auf Daten-, Formel-, Referenz- und Normenkonsistenz untersuchen.

**Identität.** `_developement/USECASES/FT_TRÄGER_MATRIX`, Drive-ID `1STCwWk7pewkqpDb-9QaRav-VmKK9ZSWX`. Darin wurde `P205-FT-Trager-Matrix-Bestandsanalyse.md` gelesen [S09]. Die historische Workflow-Registry führt ergänzend `WFL-2026-0005` (EC-Nachweis-Audit in Excel-Workbooks).

**Daten und Methode.** Eingänge sind die bezeichnete Workbook-Fassung, Plan-/Trägerinformationen, Normenfamilie EN 1992 mit österreichischen Festlegungen sowie das Prüfskript. Der Analysebericht verwendet laut eigener Darstellung `openpyxl`, gespeicherte Zellwerte und Formeltexte. Die Rechen- und Freigabequalität ist strikt von einer Excel-Neuberechnung zu trennen.

**Belegter Befund.** Der gelesene Bericht nennt vier sicherheitsrelevante Abweichungen N1–N4 und meldet für den EC2-Rechenkern beziehungsweise einen vollständigen Pilotträger **keinen Golden Case**. Als Beispiele werden ein nicht konservativer Mittelwert zweier Auflagerquerkräfte, fehlerhafte Querschnittsreferenzen und Unstimmigkeiten bei der Schubfugen-/Durchbruchlogik aufgeführt. Diese Zahlen sind **Berichtsaussagen**, keine in diesem Redaktionslauf nachgerechneten Befunde.

**Erforderlicher Abnahmepfad.** (1) maßgebende Workbook-Originalbytes und Editionen sichern; (2) Formeln und Referenzen deterministisch extrahieren; (3) sicherheitsrelevante Findings einzeln reproduzieren; (4) fachlich geprüfte Korrekturen getrennt vom Original entwickeln; (5) Golden Cases, Grenzwerttests und unabhängige Kontrolle; (6) erst danach Statusänderung.

**Status:** Bestandsanalyse vorhanden; fachliche Rechenfreigabe **nicht belegt**.

## 10.4 Referenzfall B: Materialkatalog – LCA, ReUse und Bauteildaten

**Ziel.** Bauteile und Materialien mit identifizierbaren Quellen, Mengen, technischen Kennwerten und Umweltinformationen vergleichen, ohne fehlende Nachweise zu fingieren.

**Identität.** `_developement/USECASES/MATERIALKATALOG`, Drive-ID `1nLBc4Ij5ZpxX-N75dH_CUq_B5BnqOmNt`. Das Handbuch `NEXUS_Materialkatalog_Leitfaden_und_Usermanual_v0.1.1.md` ist im Ordner vorhanden und wurde inhaltlich gelesen [S11].

**Pilotumfang laut Handbuch.** Die Pilotanwendung verbindet einen lokalen Materialkatalog mit einer Standalone-HTML-Oberfläche, Quellenregister und begrenzten deterministischen Berechnungsmodulen. Als erste Vergleichsaufgabe nennt sie Geschossdecken und Außenwände eines beispielhaften Wohngebäudes mit 21 m × 21 m Grundriss und zehn oberirdischen Geschossen. Diese Geometrie ist eine Pilotvorgabe, kein nachgewiesener Projektbestand.

**Funktionen laut Handbuch.** Schichtaufbauten, Materialparameter, Flächenmasse, idealisierte thermische Schichtwiderstände und U-Werte, EPD-bezogene Skalierung sowie Export/Materialpass-Entwurf. Für Tragwerksnachweise, Brand, Schall und Feuchte nennt das Handbuch ausdrücklich Grenzen. Die lokale Browser-Variante und der optionale Python-/SQLite-FTS5-Dienst sind zu unterscheiden; `file://`-Speicherung und Mehrgeräte-Synchronisation sind nicht garantiert.

**Datenvertrag.** Materialidentität, Hersteller-/Datensatzidentität, Einheit, Kennwert, Datensatzrevision, Geltungsbereich, EPD-Modul, Datenrechte und Fundstelle werden getrennt geführt. Ökologische Kennwerte werden nicht ohne kompatible Bezugseinheiten addiert; Modul D bleibt getrennt von den bilanzierten Lebenszyklusmodulen. ReUse-Eignung erfordert zusätzliche Prüfung von Zustand, Verfügbarkeit, Logistik und rechtlicher/technischer Verwendbarkeit.

**Status:** dokumentierter Pilot v0.1.1 / `REVIEW_REQUIRED` laut Handbuch; kein hier ausgeführter Live-Test.

## 10.5 Referenzfall C: NEXUS Control Panel – Betriebs- und Wissensübersicht

**Ziel.** Vorhandene Quellen, WorkOrders, Skills, Agenten und Testnachweise an einem Ort auffindbar machen, ohne eine neue konkurrierende Registry aufzubauen.

**Identität.** `_developement/USECASES/CONTROL-PANEL`, Drive-ID `1t7T-KWn2s9HUctXGg-HY04z3xLamRJ5g`. Im Ordner befindet sich ein Implementierungsplan, dessen Inhalt gelesen wurde [S10], sowie HTML-Entwürfe, Adapter- und Testdateien.

**Architekturvorschlag des Plans.** Control Plane für Aufträge, Agenten und Monitoring; Knowledge Plane für Quellen und Wissensobjekte; Engineering Execution Plane für Skills, Rechenkerne und Fachanwendungen. Das ist eine alternative **Betriebs-/UI-Sicht** auf die vier funktionalen Referenzebenen aus Kapitel 6, kein Widerspruch und keine zusätzliche neue Systemschicht.

**Wichtige Unterscheidung.** Ein sichtbares Dashboard oder ein erzeugter JSON-Feed ist noch kein Beleg für automatische Echtzeit-Synchronisation. Ein WORK-Auftrag, ein bestätigter ACK, ein erfolgreicher CI-Lauf und ein Release sind verschiedene Nachweise. Der Plan selbst bezeichnet zahlreiche Routen als **Zielstruktur** und nicht als implementierte Funktionen.

**Abnahme.** Ein minimaler End-to-End-Pilot sollte einen tatsächlich vorhandenen WorkOrder-Datensatz über den definierten Datenpunkt laden, den Status korrekt anzeigen, einen reproduzierbaren Aktualisierungslauf durchführen und die Verbindung zum entsprechenden Quellartefakt nachweisen. Erst anschließend werden Automatisierung und Agentensteuerung erweitert.

**Status:** Implementierungsplan und technische Entwürfe vorhanden; produktionsreife Gesamtorchestrierung **nicht durch diesen Redaktionslauf nachgewiesen**.

## 10.6 Weitere Use Cases und ihre Beziehungen

**Ausschreibung Eisteiche:** `LV_EISTEICHE_LB-HB` ist eine vorhandene Fachablage. Eine zukünftige Workflow-Route kann Norm-/Leistungsbeschreibung, Positionslogik, Mengen, Quellen, Prüfprotokoll und Freigabestatus verknüpfen. Ob die vorhandenen PDF-/URL-Dateien diese vollständige Kette tragen, ist noch zu prüfen.

**Seilstatik:** `WFL-2026-0006` dokumentiert eine historische Aufgabenidee für Lastfallaufbau und unabhängige Nachrechnung. Der Eintrag `DRAFT` ist zu respektieren; eine produktive RFEM-Anbindung wird nicht daraus abgeleitet.

**Windlast und Normenrecherche:** `WFL-2026-0007` und `WFL-2026-0012` bilden ein sinnvolles Paar aus Normen-/Quelleninventar und Literaturrecherche. Für einen gültigen Nachweis sind Ausgabe, nationaler Anhang, Fundstelle und konkrete Projektparameter zusätzlich nötig.

**CAD und Planprüfung:** `WFL-2026-0004` und `WFL-2026-0010` können später dieselbe Bauteilidentität über Plan-PDF, Trägerachse, Bemessungsdaten und DXF-Ausgabe verbinden. Die fachliche Prüfung und der geometrische Export sind getrennte Schritte.

**Lokale LLMs und AI Studio:** Die Ordner `OLLAMA` und `Interactive-AI-Studio-Apps` sind als Bestand nachgewiesen. Modellversion, Runtime, Connector und tatsächliche Funktion müssen je Anwendung geprüft werden.

## 10.7 Kanonischer Use-Case-Steckbrief

Für jede weiter ausgearbeitete Anwendung wird dieselbe **fachliche Beschreibung** genutzt, ohne ein neues Register einzuführen:

| Feld | Bedeutung |
|---|---|
| Identität | Vorhandene Drive-ID, Registry-ID oder Repo-Pfad |
| Zweck | Fachliche Entscheidung beziehungsweise Ergebnis |
| Scope | Anwendungsgrenzen, Nutzer und Risiko |
| Input | Projektunterlagen, Geometrie, Material, Datenrevision |
| Quellen | Normen, Literatur, Hersteller, Projektoriginale mit Locator |
| Route | Domäne → Methode → Workflow → Skill/Tool |
| Compute | Solververtrag, Codeversion, Eingabeeinheiten |
| QA | Prüfregeln, Benchmark, unabhängiger Review |
| Output | Bericht, Tabelle, CAD/BIM, JSON, Status, Artefakt |
| Reife | `DRAFT`, `PILOT`, `TESTED`, `REVIEWED`, `RELEASED` mit Evidenz |

Diese Struktur ist eine Lesesicht auf vorhandene Informationen. Die eigentliche Registrierung bleibt bei den bestehenden kanonischen Systemregistern.

# 11. Implementation Guide und Softwareanforderungen

**Kurzfassung.** NEXUS wird am zuverlässigsten durch kleine, vollständig prüfbare Anwendungsketten erweitert. Die Implementierung beginnt mit dem vorhandenen Asset- und Workflowbestand, legt explizite Eingabe-/Ausgabeverträge fest und testet zuerst eine reale End-to-End-Route. Neue Frameworks oder Datenbanken sind nur dann sinnvoll, wenn ein konkret nachgewiesener Bedarf besteht.

## 11.1 Implementierungsstrategie: vertikal vor horizontal

Die Reihenfolge ist **Use Case → Daten → Methode → Schnittstelle → Implementierung → Test → Betriebsnachweis**. Sie vermeidet, dass umfangreiche Ontologien, Dashboards oder Agentensteuerungen entstehen, bevor ein einziger fachlicher Ablauf vollständig funktioniert. Vor jedem Neuentwurf werden `ASSET_REGISTRY.csv`, `USECASE_REGISTRY.md`, die relevanten Drive-Ordner und der GitHub-Codebestand durchsucht.

Das ältere `MCP-ACCESS-TOOLS/README.md` nennt ausdrücklich einen „Minimal Viable Access Layer“ und warnt vor mehrfach vorhandenen Scannern, Masterindizes und Lessons-Dateien [S06]. Dieser Befund stammt aus einem älteren Stand; seine methodische Konsequenz bleibt sinnvoll: **bestehende Komponenten verbinden statt parallel neu aufzubauen**.

## 11.2 Software Requirements – funktionale Anforderungen

Die nachfolgenden Kennungen `REQ-DOS-...` sind **Anforderungskennungen dieses Dossiers**, keine neu registrierten NEXUS-IDs.

| ID | Anforderung | Minimaler Akzeptanznachweis |
|---|---|---|
| REQ-DOS-01 | Eine Anfrage erhält Scope, Intent und Zielartefakt | Maschinenlesbarer Request Contract |
| REQ-DOS-02 | Kanonische Steuerdateien sind vor kritischer Ausführung lesbar | Dokumentierte Quelle, Version und Zugriff |
| REQ-DOS-03 | Vorhandene Assets werden vor Neuentwicklung gesucht | Registry-/Index-Abfrage mit Ergebnis |
| REQ-DOS-04 | Quellen und Normfassungen sind referenzierbar | Provider-ID, Revision, Locator, Geltungsbereich |
| REQ-DOS-05 | Berechnungen nutzen explizite Input-/Output-Verträge | Versionierter Testfall mit Einheiten |
| REQ-DOS-06 | Fachliche und technische Prüfungen sind unterscheidbar | QA-Protokoll und separater Review-Status |
| REQ-DOS-07 | Artefakte werden identifizierbar persistiert | Drive-ID/Repo-Pfad, Readback, ggf. Hash |
| REQ-DOS-08 | Ein Status darf nur mit Evidenz als DONE gelten | Statusbericht mit Nachweislink |
| REQ-DOS-09 | Fehlende Quellen oder Zugriffe führen zu definiertem Teilstatus | Negativtest ohne erfundene Erfolgsmeldung |
| REQ-DOS-10 | Bestehende Use Cases sind auffindbar und verknüpft | Verzeichnis-/Registry-Abgleich |

## 11.3 Nichtfunktionale Anforderungen

**Korrektheit:** SI-Einheiten, nachvollziehbare Formeln, Dimensions- und Grenzwertkontrollen; für relevante Tragwerksmodelle zusätzlich Gleichgewicht und unabhängige Vergleichsrechnung.

**Reproduzierbarkeit:** Identische versionierte Eingaben, identifizierte Solver-/Bibliotheksversionen, definierte Toleranzen und ein dokumentierter Replay-Lauf. Ein Hash bestätigt nur konkrete Bytes, nicht die fachliche Richtigkeit.

**Sicherheit:** Geheimnisse gehören in geeignete Secret-Verwaltung, nicht in Prompts, öffentliche Repositories oder WORK-Dokumente. Externe Dokumenttexte sind Daten, keine neuen Systemanweisungen.

**Verfügbarkeit:** Bei Connector-Ausfall bleiben read-only Recherche, lokale Tests oder dokumentierte Teilresultate möglich, soweit keine kritische Quelle oder Berechtigung fehlt. Ein blockierter Sync darf nicht als erfolgreich dargestellt werden.

**Wartbarkeit:** Kleine Module mit klaren Verträgen, Tests und Quellverweisen; keine unnötige Duplizierung der Steuerdateien oder Register.

**Benutzbarkeit:** Einsteiger sehen Ziel, Ergebnis und nächsten Schritt. Entwickler finden API, Schemas, Fehlercodes und Testfälle in der technischen Referenz.

## 11.4 Daten- und Schnittstellenverträge

Ein Fachworkflow benötigt mindestens vier logisch getrennte Verträge:

1. **Request Contract:** Auftrag, Domäne, Eingabedokumente, gewünschte Ergebnisse, Risiko und Abnahmekriterien.
2. **Source Contract:** Quellidentität, Revision, Geltungsbereich, Lizenz und konkrete Fundstellen.
3. **Compute Contract:** Parameter mit Einheiten, Modellannahmen, Softwareversion, numerische Ergebnisse, Warnungen und Fehlercodes.
4. **Evidence Contract:** Testnachweise, Review-Status, Artefakt-Identität, Registrierungsstatus und menschliche Freigabe.

Ein JSON-Schema oder eine Python-Dataclass kann diese Verträge formal ausdrücken. Das konkrete Schema ist gegen bereits vorhandene `contracts/` und `schemas/` im Repository abzugleichen, bevor neue Dateien angelegt werden.

## 11.5 Beispiel einer deterministischen Solver-Schnittstelle

Die folgende Python-Skizze ist **didaktischer Pseudocode**, kein implementierter oder normativ freigegebener HBV-Rechenkern:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Input:
    span_m: float
    load_kn_per_m: float
    flexural_rigidity_kn_m2: float

@dataclass(frozen=True)
class Output:
    deflection_m: float
    model: str


def simply_supported_uniform_load(inp: Input) -> Output:
    assert inp.span_m > 0
    assert inp.flexural_rigidity_kn_m2 > 0
    assert inp.load_kn_per_m >= 0
    w = 5 * inp.load_kn_per_m * inp.span_m**4 / (384 * inp.flexural_rigidity_kn_m2)
    return Output(deflection_m=w, model="Euler-Bernoulli, constant EI, simply supported")
```

Die bekannte Balkenformel illustriert eine reproduzierbare Rechenfunktion, **nicht** die Eignung für eine schubnachgiebige HBV-Rippendecke. Für reale HBV-Anwendungen sind Verbundmodell, Anschlusssteifigkeiten, Zeitverhalten, Einwirkungen und Nachweisverfahren gesondert zu implementieren und zu validieren. Schon das Beispiel verlangt Tests für Einheiten, Grenzfälle, zulässige Werte und unabhängige Vergleichsresultate.

## 11.6 MCP, Python, Frameworks und lokale Laufzeit

Im live gelesenen Ordner `MCP-ACCESS-TOOLS` wurden unter anderem `nexus_ssot_mcp.py`, `mcp_dispatcher.py`, `nexus_catalog_sync.py`, `sync_to_github_artifacts.py`, `RFEM6_MCP_Bridge_Extended.py`, `nexus_tower.py` und Test-JSON-Dateien für HBV und Fertigteilträger gefunden [S12]. **Nachgewiesen ist die Datei-Existenz, nicht ihre Ausführbarkeit, Sicherheit oder Integrationsreife.**

Für eine Implementierung wird jede Komponente anhand derselben Fragen geprüft: Welcher Input wird akzeptiert? Welche Abhängigkeiten sind erforderlich? Welche externen Rechte besitzt sie? Was passiert bei Timeout, fehlender Normquelle, Schemafehler oder doppelt eingehendem Auftrag? Wo liegen Logs und Tests? Welche Version wurde tatsächlich ausgeführt?

**Python:** geeignet für numerische Kerne, Tabellenanalyse, Normdaten-Parsing, Datenverträge und ETL. `openpyxl` kann Excel-Formeln lesen, berechnet sie aber nicht selbst. Ein Excel-Nachweis verlangt gegebenenfalls eine native Recheninstanz und ein Ergebnis-Readback.

**JavaScript/HTML:** geeignet für interaktive lokale Werkzeuge, Dashboards und Browseranwendungen. Ein HTML-Dokument in Drive ist nicht automatisch eine gehostete Web-App; die tatsächliche Hosting- und Aktualisierungsstrecke ist separat zu belegen.

**SQLite/FTS5:** praktikabler lokaler Such- und Metadatenkern für ein begrenztes MVP. Vektorindizes und Graphdatenbanken sind mögliche Erweiterungen, nicht zwingende Voraussetzungen für den ersten nutzbaren Workflow.

**MCP/Connectoren:** Zugriffsschicht für identifizierte Quellen und Aktionen. Berechtigungen sind pro Runtime und Operation nachzuweisen; „verbunden“ ist nicht gleich „read/write getestet“.

**GitHub:** Quellcode, Tests, Reviews, Branches und nachvollziehbare Commits. Ein erfolgreicher Commit beweist Dateispeicherung, nicht eine produktive Freigabe oder einen automatischen Drive-Sync.

## 11.7 Implementierungsablauf eines neuen Skills

Ein Skill beschreibt eine wiederverwendbare Aufgabe mit Eingangsvoraussetzungen, Vorgehensweise, Werkzeugen, Ergebnissen und Fehlergrenzen. Die konkrete Struktur richtet sich nach dem jeweils verwendeten Skill-Framework; Frontmatter, Body und Assets sind eine hilfreiche redaktionelle Analogie, keine Behauptung einer universellen Norm.

1. **Bedarf und Bestand:** Use Case identifizieren; vorhandene Skills, Skripte und Workflows prüfen.
2. **Kontrakt:** Trigger, Voraussetzungen, Eingaben, Outputs, Risiken, Stopbedingungen und Berechtigungen definieren.
3. **Implementierung:** Kleine Module, explizite Datenmodelle und keine versteckten Seiteneffekte.
4. **Tests:** Positiv-, Negativ-, Grenzwert- und Regressionsfälle; bei Berechnung unabhängiger Golden Case.
5. **Review:** Quell-/Codeprüfung durch tatsächlich unabhängige Instanz, nicht nur andere Rollenbezeichnung.
6. **Integration:** In bestehende Registry und Workflows einbinden; keinen konkurrierenden Index schaffen.
7. **Betriebsnachweis:** Echte Ausführung, Artefakt, Status, Readback und gegebenenfalls ID01-Freigabe.

## 11.8 Implementierung in überschaubaren Entwicklungsstufen

**Stufe A – Auffindbarkeit:** Kanonische Quellidentitäten und ein funktionierender Lookup für die priorisierten Use Cases.

**Stufe B – Ein vollständiger Vertical Slice:** Ein Engineering-Workflow mit dokumentierten Eingaben, geprüfter Rechenfunktion, QA, Ergebnis und WORK-Report.

**Stufe C – Wiederverwendung:** Dieselben Verträge für weitere Use Cases und wiederkehrende Aufgaben nutzen.

**Stufe D – Orchestrierung:** Multi-LLM-Routing, Scheduling und Dashboard auf nachgewiesene Komponenten aufsetzen.

**Stufe E – Erweiterung:** Knowledge-Graph-Abfragen, zusätzliche Solver, BIM/IFC und externe Datenquellen erst nach erfolgreicher Kernabnahme ausbauen.

Diese Stufen sind eine **Roadmap-Empfehlung**, keine bereits beschlossene oder umgesetzte Produktplanung. Der tatsächliche Stichtagsstatus wird in Kapitel 13 getrennt bewertet.

## 11.9 Abnahmekriterien und Grenzen dieses Blocks

Ein Kapitel gilt redaktionell als ausgearbeitet, wenn Begriffe zu den vorangehenden Kapiteln passen, seine wesentlichen Aussagen auf nachprüfbare Quellen zurückgehen und geplante Funktionen nicht als bereits produktiv erscheinen. Eine Softwarekomponente gilt dagegen erst als implementiert und geprüft, wenn reale Tests und ein reproduzierbarer Lauf vorliegen. Ein Peer-Review ist erst dann abgeschlossen, wenn die Stellungnahme tatsächlich eingeholt, dokumentiert und bearbeitet wurde.

Die vorliegende Fassung erfüllt den Zweck einer **quellengebundenen Erstredaktion** für Kapitel 9–11. Sie beansprucht weder vollständige Use-Case-Inventur aller gleichnamigen Ordner noch eine fachliche Bemessungsabnahme oder eine produktive End-to-End-Demonstration.

# Quellen- und Evidenzregister dieses Redaktionsblocks

- **[S01]** NEXUS `_AGBS.md`, v007.2, Drive: https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view – aktuelle gelesene Textfassung; interne Aktivierungsfrage offen.
- **[S02]** NEXUS Current Manifest, Revision 2026-09-28 mit Rollenregister v1.2: https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view.
- **[S03]** NEXUS Baseline Instructions CURRENT 2026-09-28: https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view.
- **[S04]** WORK `Folder.md`, Policy 0.4.0-pilot: https://drive.google.com/file/d/1nDjF78dq3l8PGpXsauzBz1bzHescDSwv/view.
- **[S05]** `_developement/USECASES` (direktes Verzeichnisinventar): https://drive.google.com/drive/folders/1sNPiZgSOL2g-RQgOdVzBShWaF5sIlni2.
- **[S06]** `MCP-ACCESS-TOOLS/README.md`, MVAL v1.0 (historischer Stand 15.09.2026): https://drive.google.com/file/d/1a6nh2KwpcI3kVNHJc1okt4ibL7YErDFA/view.
- **[S07]** GitHub Repository: https://github.com/julianzotter/nexus-platform.
- **[S08]** `MCP-ACCESS-TOOLS/USECASE_REGISTRY.md`, 17 historische Workflows: https://drive.google.com/file/d/1kkB5prWZ7mf6a0HcJwBOoANRtDbTWS9w/view.
- **[S09]** `P205-FT-Trager-Matrix-Bestandsanalyse.md`: https://drive.google.com/file/d/1LrvcfaFBcS6bal3iAC_Codd0Um7Up1tP/view.
- **[S10]** `26_11_26_NEXUS · AEC Control Panel · Implementation-Plan-Draft.md`: https://drive.google.com/file/d/1_nosLpezSN8i-fzTSaNjtnkA-yf11Qfq/view.
- **[S11]** `NEXUS_Materialkatalog_Leitfaden_und_Usermanual_v0.1.1.md`: https://drive.google.com/file/d/1vGaFX_S6qMhiZsvva8F-D-S4Qd9uRrh8/view.
- **[S12]** `_developement/MCP-ACCESS-TOOLS` (direktes Verzeichnisinventar): https://drive.google.com/drive/folders/1fRa7rQvKi-BkhVIzjXPcY_u8iIJ4Vn5J.
- **[S13]** ID06 Peer Review zum Masterdossier: https://drive.google.com/file/d/1vS3KBK9nnBoDVucMqX5OzoEW8_r0KU0M/view.

**Redaktioneller Abschluss:** Kapitel 9, 10 und 11 erstellt. **Offen:** Block 04 (Kapitel 12–14), technische Anhänge, Gesamtkonsistenz, unabhängig bestätigter Peer-Review, Ledger/Registry, finale Word-Baseline und ID01-Release.
