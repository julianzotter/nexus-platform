---
name: NEXUS-AI-MASTERDOSSIER-BLOCK04
version: 1.0.0-candidate
status: DRAFT_IN_PROGRESS
created_date: 2026-11-26
author_role: ID03
owner_role: ID01
scope: "Kapitel 12–14: Verifikation, Entwicklungsstand, Roadmap und Schlussfolgerungen"
source_authority: "ID01-freigegebener Arbeitsplan; CURRENT Manifest/Baseline; AGB v007.2 als abgerufene Fassung; WORK Folder.md v0.4.0-pilot"
review_status: REVIEW_PENDING
registration_status: REGISTRATION_PENDING
human_release: PENDING
---
# NEXUS-AI Engineering Knowledge Operations System
## Masterdossier · Redaktionsblock 04 – Kapitel 12–14

**Redaktionsstatus:** Wissenschaftlich-technische Erstfassung, keine Systemfreigabe. Die Kapitel bauen auf den Blöcken 01–03 auf und unterscheiden nachgewiesene Artefakte, historisch berichtete Ergebnisse und noch zu implementierende Funktionen. Die in den Quellen genannten Tests wurden für dieses Kapitel nicht erneut ausgeführt. Das Dossier ist eine Produktbeschreibung mit Implementierungsleitfaden; es ersetzt keine Fachnorm, Bemessungssoftware oder projektspezifische Freigabe.

# 12. Verifikation, Evaluation und Qualitätssicherung

**Kurzfassung.** NEXUS-AI soll nicht daran gemessen werden, wie überzeugend ein LLM eine Lösung beschreibt, sondern daran, ob eine fachlich richtige, reproduzierbare und quellengebundene Lösung entsteht. Dazu werden Quellenprüfung, Datenintegrität, Rechenprüfung, unabhängiges Review und die tatsächliche Ausführung getrennt nachgewiesen. Ein bestandenes Software-Unit-Testset ist kein Ersatz für einen bauingenieurtechnischen Bemessungsnachweis.

## 12.1 Prüfgegenstände und Prüftiefe

Ein technisches System kann auf mehreren Ebenen funktionieren und auf einer anderen versagen. Für NEXUS werden sechs voneinander unterscheidbare Prüfgegenstände geführt:

1. **Quelle und Geltung:** Die verwendete Norm, Richtlinie, Materialangabe oder Projektdokumentation ist identifizierbar; Ausgabe, nationaler Anhang, Datum, Geltungsbereich und Fundstelle sind geklärt. Bei fehlender Normverfügbarkeit bleibt die normative Bewertung offen.
2. **Daten und Semantik:** Quellrepräsentation, extrahierte Werte, Einheiten, Typen, Objektidentitäten und Graphrelationen sind rückverfolgbar. Ein semantischer Treffer ist keine fachliche Bestätigung.
3. **Algorithmus:** Der implementierte Rechenkern erfüllt einen beschriebenen Vertrag aus Eingaben, Annahmen, Randbedingungen, Formeln, Ausgabegrößen und Fehlermeldungen.
4. **Numerische Ergebnisse:** Dimensionsprüfung, Plausibilität, Gleichgewicht, Grenzfälle und unabhängige Referenzrechnungen stimmen innerhalb vorab festgelegter Toleranzen überein.
5. **Systemintegration:** Ein tatsächlicher End-to-End-Lauf verbindet Retrieval, Compute, Review, Archivierung und Reporting. Teilweise funktionierende Schnittstellen werden nicht als Gesamtsystemnachweis ausgegeben.
6. **Betrieb und Governance:** Berechtigungen, Registry, Versionsstand, Writeback, Audit-Trail und menschliche Freigabe sind für die betreffende Aktion nachweisbar.

Diese Ebenen werden getrennt bewertet. Ein Artefakt kann gespeichert, aber nicht registriert sein; ein Solver kann technisch getestet, aber fachlich nicht freigegeben sein; ein Bericht kann veröffentlicht, aber von einem anderen Agenten noch nicht empfangen worden sein.

## 12.2 Evidenzklassen im Produkthandbuch

Für den Haupttext genügen drei verständliche Reifehinweise: **vorhanden**, **in Entwicklung**, **geplant**. Im technischen Nachweis wird genauer differenziert:

| Nachweisstatus | Bedeutung | Nicht daraus ableiten |
|---|---|---|
| `SOURCE_REPORTED` | Ein lesbares Bestandsdokument behauptet oder protokolliert einen früheren Zustand | Kein heute erneut gemessener Zustand |
| `INVENTORIED` | Datei, Ordner oder Codepfad wurde gefunden | Keine funktionierende Ausführung |
| `CONNECTED` | Ein konkreter Zugriff wurde erfolgreich durchgeführt | Keine allgemeine Read-/Write-Freigabe |
| `TESTED` | Ein spezifizierter Test wurde mit Ergebnis ausgeführt | Keine umfassende Fachfreigabe |
| `VERIFIED` | Der konkret bezeichnete Sachverhalt ist durch geeigneten Beleg geprüft | Keine unbeschränkte Systemfreigabe |
| `REVIEW_PENDING` | Unabhängige Prüfung fehlt | Keine Akzeptanz |
| `RELEASED` | Der dafür zuständige Mensch hat den definierten Umfang freigegeben | Keine Geltung für andere Revisionen oder Projekte |

Statusangaben sind **objekt- und zeitgebunden**. Ein früheres `PASS` wird bei Änderungen der Normfassung, Eingabedaten, Implementierung oder Testumgebung erneut relevant. Eine Anzeige im Control Panel darf die Statusbegriffe nicht zu einem einzigen „grünen Gesamtstatus“ zusammenziehen.

## 12.3 Verifikationskette für ein Engineering-Ergebnis

Ein belastbarer Nachweis durchläuft folgende prüfbare Kette:

`Auftrag → Identität der Eingabedaten → Norm-/Quellenauflösung → Modellannahmen → Rechenkern → Rohresultat → Plausibilität → Referenzvergleich → Peer Review → Bericht → Ablage → Registrierung → ID01-/Fachfreigabe`.

Für jeden Übergang wird mindestens festgehalten, *welche* Version eines Artefakts beteiligt war und *welche* Prüfung tatsächlich stattgefunden hat. Eine eindeutige WorkOrder- oder Datei-ID ist dafür hilfreicher als ein bloßer Dateiname. Der Traceability-Pfad bleibt auch dann nachvollziehbar, wenn spätere Revisionsstände hinzukommen.

Bei ingenieurtechnischen Rechnungen werden unter anderem folgende Prüfungen benötigt:

- **Dimensionskontrolle:** Alle Rechengrößen sind mit Einheiten und gegebenenfalls einer expliziten Umrechnung versehen; die Gleichung ist dimensionsrichtig.
- **Mechanische Plausibilität:** Lastabtrag, Vorzeichen, Schnittgrößen, Randbedingungen, Verformungsbild und Gleichgewicht passen zum statischen Modell. Die Beziehungen `ΣF = 0` und `ΣM = 0` sind für passende Gleichgewichtssysteme notwendig, aber kein vollständiger Nachweis.
- **Normativer Vergleich:** Einwirkungen, Kombinationen, Widerstände, Teilsicherheitsbeiwerte, nationale Festlegungen, GZT/GZG und ggf. Brand/Schwingung sind für den konkreten Fall geklärt.
- **Unabhängige Kontrolle:** Ein Referenzmodell oder ein zweiter methodisch unabhängiger Rechenweg wird verwendet, sofern Risiko und Umfang dies erfordern. Die gleiche Formel zweimal im selben Code auszuführen ist keine unabhängige Validierung.
- **Fehlerverhalten:** Fehlende Normeditionen, unzulässige Eingaben, nicht konvergente Solver, unvollständige Quellen und unklare Einheiten führen zu expliziten, nicht beschönigten Fehlerzuständen.

## 12.4 Software-Tests und fachliche Tests unterscheiden

**Software-Tests** prüfen zum Beispiel Parser, Schemas, API-Verträge, Zustandsübergänge, Dateizugriffe, Serialisierung und deterministische Hilfsfunktionen. **Fachtests** prüfen physikalische und normative Richtigkeit: Handrechnungen, Benchmarks, Grenzfälle, Modellvarianten und Gegenprüfung durch einen befugten Fachverantwortlichen. **Integrationstests** prüfen, ob der gesamte Workflow mit realen Quellen und Schnittstellen endet, wo er enden soll.

Die Mindest-Testpyramide für einen freigabefähigen Solver ist:

1. Schema- und Einheitentests für gültige und ungültige Eingaben.
2. Unit-Tests für die elementaren Rechenoperationen.
3. Golden Cases mit unabhängigen Referenzwerten und begründeten Toleranzen.
4. Regressionstests bei jeder Änderung an Algorithmus, Parametern oder Datenadapter.
5. End-to-End-Test mit realer Quellenidentität, gespeichertem Resultat und geprüftem Writeback.
6. Fachliche Prüfung und ausdrückliche Freigabe für den definierten Einsatzbereich.

Ein Beispiel für eine maschinenlesbare Prüfaussage ist:

```json
{
  "test_id": "EXAMPLE-HBV-GOLDEN-001",
  "run_id": null,
  "source_revision": null,
  "solver_version": null,
  "input_sha256": null,
  "expected_result": null,
  "actual_result": null,
  "unit": "mm",
  "tolerance": null,
  "status": "NOT_RUN",
  "reviewer": null
}
```

Dieses Objekt ist ein **illustrativer Datenvertrag**, kein ausgeführter Test und kein Eintrag in einer bestehenden Registry. In einem echten Lauf müssen Ergebnisgrößen, Toleranzen und Nachweise aus einem verifizierten Referenzfall stammen.

## 12.5 Durchgehender Prüfpfad: HBV-Deckenbemessung

Das im Handbuch eingeführte Beispiel einer Holz-Beton-Verbunddecke verknüpft die Systemebenen. Die Aufgabe ist nicht, aus einem Prompt unmittelbar eine Tragfähigkeit zu behaupten. Zunächst wird das Systemmodell festgelegt: Geometrie, Lagerung, Lasten, Werkstoffe, Verbundmechanismus, Kriechen und zu prüfende Grenzzustände. Danach wird die jeweils anwendbare Ausgabe der technischen Regeln einschließlich österreichischer Festlegungen ermittelt. Die Verbindungseigenschaften werden anhand ihrer konkreten Quelle und ihres Geltungsbereichs angesetzt.

Die Rechenmethoden – etwa vereinfachte Verbundmodelle oder diskrete numerische Verfahren – dürfen nicht ohne Begründung als gleichwertig behandelt werden. Ein Referenzvergleich muss die Modellannahmen offenlegen. Erst dann können Steifigkeiten, Schnittgrößen, Verformungen, Schwingungskennwerte oder Kervenkräfte beurteilt werden. Bei Abweichungen ist die Ursache zu untersuchen: Eingabewerte, Diskretisierung, Randbedingungen, Verbindungsmodell, Einheiten, Normparameter oder Solverversion.

**Grenze dieses Redaktionsblocks:** Es wurden keine HBV-Rechenkerne ausgeführt und keine neuen Normkennwerte validiert. Das Kapitel beschreibt die methodische Abnahme, nicht einen fertigen Bemessungsnachweis.

## 12.6 Unabhängigkeit und Self-Refinement

Self-Refinement verbessert den Entwurf durch Gegenfragen, Fehlerhypothesen, Gegenbeispiele und gezielte Nachprüfung. Es ersetzt jedoch nicht die Unabhängigkeit eines Peer Reviews. Die Rollenbezeichnungen `ID03` und `ID06` allein belegen weder unterschiedliche Laufzeitinstanzen noch die tatsächliche Zustellung eines Prüfauftrags. Die unabhängige Prüfung ist erst nachgewiesen, wenn Reviewer, Runtime, Prüfgegenstand, verwendete Quellen und Rückmeldung feststehen.

Für den Dossier-Review sind insbesondere fünf Fragen maßgebend:

1. Ist die Produktbeschreibung für neue Anwender ohne internes Vorwissen verständlich?
2. Stimmen Begriffe, Taxonomie und Verantwortlichkeiten über alle Kapitel überein?
3. Sind bestehende Funktionen, historische Berichte und Zukunftsarchitektur erkennbar getrennt?
4. Sind sicherheitsrelevante Aussagen normativ und fachlich ausreichend begründet?
5. Ist die Implementierung mit konkreten Daten-, Test- und Übergabeverträgen nachvollziehbar?

Die Stellungnahme von ID06 vom 26.11.2026 ist als **Peer Review des Arbeitsplans** dokumentiert. Sie ist keine Prüfung der später verfassten Kapitel 1–14. Dieser Unterschied bleibt im Freigabestatus sichtbar.

# 13. Entwicklungsstand, Statusmatrix und stufenweise Roadmap

**Kurzfassung.** NEXUS verfügt bereits über eine dokumentierte Governance, eine nutzbare Drive-/GitHub-Struktur und zahlreiche Fach- und Softwareartefakte. Der Bestand ist jedoch nicht mit einer vollständig getesteten, durchgängig integrierten Produktionsplattform gleichzusetzen. Die Roadmap priorisiert deshalb wenige vollständige vertikale Anwendungsabläufe vor weiteren parallelen Architekturentwürfen.

## 13.1 Stichtag, Prüfgrenzen und Lesart

**Bestandsstichtag:** 26.11.2026. Für diese Fassung wurden ausgewählte Primärdateien direkt aus Google Drive eingelesen: `_AGBS.md` v007.2 als abrufbare Fassung, CURRENT Manifest (Revision 28.09.2026 mit Rollenregister v1.2), CURRENT Baseline, WORK `Folder.md` v0.4.0-pilot, der ID06-Review, die USECASE_REGISTRY sowie konkrete Use-Case- und Statusdokumente. Vorhandene frühere Berichte werden als Berichte zitiert; ihre dort genannten Testläufe wurden nicht wiederholt. GitHub-Commits der Redaktionsblöcke belegen deren Ablage, nicht die Produktionsreife von NEXUS.

Der Befund der AGB-Fassung ist vorsichtig zu lesen: Die Datei weist im Kopf `v007.2` aus und enthält zugleich einen Hinweis auf noch ausstehende Rohbyte-Übernahme beziehungsweise Registrierung. Eine formale Aktivierungs-/Identitätsklärung gehört in die operative Governance, nicht in den Erzähltext des Produkthandbuchs. Die Dokumentation benutzt die gelesene Fassung als Quelle, ohne den ungeprüften Aktivierungsschritt zu behaupten.

## 13.2 Quick Task Development & Implementation Status Matrix

Die Matrix trennt **existierendes Artefakt**, **nachgewiesene Funktion** und **offene Abnahme**. „Vorhanden“ bedeutet hier: direkt gefundenes Dokument, Datei oder Ordner. „Historisch berichtet“ bezeichnet Aussagen eines älteren Prüfberichts. „Geplant“ ist eine Soll-Architektur, kein Funktionsnachweis.

| Komponente | Belegter Ist-Stand zum Stichtag | Status | Wichtigster nächster Schritt | Evidenz |
|---|---|---|---|---|
| Governance, Rollen, Baseline | Manifest, Baseline, AGB v007.2 und WORK Folder.md gelesen; Rollen v1.2 ausgewiesen; Aktivierungs-/Registrierungsdetails teilweise offen | 🟡 Vorhanden / Konsistenzprüfung offen | Quellversionen und widersprüchliche Aktivierungshinweise bereinigen, ohne historische Dateien zu überschreiben | Q01–Q04 |
| Google Drive / WORK | Kanonische Ordner und Dateien direkt abrufbar; WORK-Folder-Regel dokumentiert | 🟢 Lesen nachgewiesen, 🟡 globale Sync-Integrität offen | Objektklassen, Pfade und Zugriffsnachweise im Anhang abschließen | Q04 |
| GitHub / Versionierung | Dossier-Blöcke 01–03 auf Review-Branch versioniert; bestehender PR #147 aus Vorlauf | 🟢 Redaktionsablage, 🟡 kein Release | Konsolidierten Dossierstand gegenprüfen, CI und PR-Review abwarten | Q10 |
| Workflow-Registry | `USECASE_REGISTRY.md` mit WFL-2026-0001 bis -0017 direkt gelesen; dort stehen gemischte DRAFT/ACTIVE/DONE/PAUSED-Status | 🟢 Inventar, 🟡 Funktionsstände nicht neu getestet | Einträge auf echte Pfade, ausführbare Skills und Nachweise rückführen | Q05 |
| MCP-ACCESS-TOOLS | README, Skript-/Assetnamen und Ordnerstruktur im Drive belegt; historische lokale Scans dokumentiert | 🟢 Dateien vorhanden, 🟡 Laufzeitnachweis offen | Je Tool tatsächliche Runtime, Input/Output und Connector-Rechte prüfen | Q06 |
| FT-Träger-Matrix / EC2 | Bestandsanalyse meldet vier sicherheitsrelevante Abweichungen und keinen freigegebenen Pilotträger; Workbook-Neuberechnung teilweise blockiert | 🔴 Fachfreigabe offen | Sicherheitsbefunde N1–N4 abarbeiten, native Recalc und Golden Cases nachweisen | Q07 |
| Materialkatalog / LCA | Pilot v0.1.1 mit HTML, lokaler Sucharchitektur, Datenvertrag und Dokumentation; Installation auf G: nicht ausgeführt | 🟡 Pilot / REVIEW_REQUIRED | Echte Nutzer- und Rechenläufe, Datenrechte und QA für definierte Materialfälle | Q08 |
| Control Panel | Implementierungsplan und UI-/Adapter-Artefakte vorhanden; automatischer End-to-End-Abgleich und vollständige Agentensteuerung nicht belegt | 🟡 Teilimplementierung | Ein verlässlicher JSON-Import mit belegter Aktualisierung und Statusanzeige als Pilot | Q09 |
| Knowledge Graph / RAG | Datenmodell, semantische Taxonomie und Index-/Graph-Entwürfe dokumentiert | 🟡 Architektur und Kandidaten | Einen kleinen geprüften Wissensgraphen aus identifizierten Quellen und Relationen erzeugen | Q10 |
| Solver- und Engineering-Skills | Einzelne Python-/JSON-/Testartefakte vorhanden; keine pauschale Aussage zu allen Rechenkernen möglich | 🟡 Teilbestand | Pro Skill Input-/Output-Vertrag, Golden Case, Version und Reproduktionslauf | Q06–Q08 |
| Multi-LLM-Orchestrierung | Rollen und Kommunikationsverträge beschrieben; ACK/Delivery und End-to-End-Sync sind nicht global nachgewiesen | 🟡 Integrationslücke | Ein vollständiger WorkOrder-Lauf über echte Runtime mit ACK und Rückmeldung | Q01–Q04, Q09 |
| Dossier / Handbuch | Kapitel 1–11 als Redaktionsblöcke erstellt; dieser Block ergänzt Kapitel 12–14 | 🟢 Erstfassungen, 🟡 fachlicher Review offen | Anhänge, Konsolidierung, Formatierung und unabhängige Kapitelprüfung | Q11–Q13 |

**Bewertungshinweis:** Die Ampelfarbe bezeichnet ausschließlich den hier genannten Prüfgegenstand. Insbesondere ist ein roter fachlicher Freigabestatus kein Beweis, dass alle unterstützenden Werkzeuge unbrauchbar sind. Umgekehrt ist ein grüner Datei-Abruf kein Beweis für produktionsreife Engineering-Berechnungen.

## 13.3 Priorisierung nach Nutzen, Risiko und Abhängigkeiten

Die Entwicklungsreihenfolge wird nicht allein durch Anzahl der vorhandenen Dateien oder Aufmerksamkeit eines Agenten bestimmt. Vorrang haben fachliche Sicherheit, vollständige Nutzbarkeit und Abhängigkeiten. Eine vereinfachte Entscheidungsmatrix dient als Orientierung:

| Kriterium | Leitfrage | Konsequenz |
|---|---|---|
| Fachrisiko | Kann ein Fehler eine unsichere ingenieurtechnische Entscheidung fördern? | Norm- und Solverprüfung vor Automatisierung |
| Nutzwert | Löst die Funktion einen wiederkehrenden realen Auftrag? | Vertikalen Pilot priorisieren |
| Evidenzlage | Gibt es prüfbare Eingaben, Quellfassungen und Referenzwerte? | Golden Case vor Produktversprechen |
| Wiederverwendung | Kann ein vorhandenes Skript/Skill sicher weiterverwendet werden? | Bestehendes Modul vor Neubau |
| Integrationsaufwand | Wie viele ungeklärte externe Systeme müssen gleichzeitig funktionieren? | Unabhängige Kopplungen entflechten |
| Betrieb | Kann ein Nutzer die Funktion ohne Entwicklerhilfe starten und den Status verstehen? | User Guide und Fehlerpfad mitliefern |

Ein priorisierter Kandidat ist **nicht automatisch ein freigegebener Produktionsworkflow**. Für die FT-Träger-Matrix liegt wegen der berichteten sicherheitsrelevanten Abweichungen zunächst ein Korrektur- und Prüfauftrag nahe; der Materialkatalog bietet sich für einen abgegrenzten Demonstrationslauf an, sofern Datenrechte und Rechenumfang beachtet werden. Das Control Panel kann parallel als schmale, lesende Statusoberfläche dienen, ohne bereits alle externen Systeme zu synchronisieren.

## 13.4 Stufenweise Implementierungs-Roadmap

**Stufe A – Konsistente Orientierung und kontrollierter Einstieg.** Ein gemeinsames Glossar, eindeutige Systemverweise, nachvollziehbare Use-Case-Steckbriefe und ein funktionierender Schnellstart. Akzeptanz: Ein neuer Anwender findet Quellen, startet einen dokumentierten Testfall und kann „vorhanden“, „geplant“ und „freigegeben“ unterscheiden.

**Stufe B – Ein vollständiger vertikaler Pilot.** Ein konkreter Use Case erhält versionierte Eingaben, geprüfte Quelle, ausführbares Tool, Testfälle, Ergebnisbericht und nachweisbare Ablage. Akzeptanz: Ein unabhängiger Dritter kann den Lauf anhand derselben Eingaben reproduzieren und die Grenzen erkennen. Fachliche Freigabe nur nach den jeweiligen Norm- und Prüfanforderungen.

**Stufe C – Wiederverwendbare Systembausteine.** Die im Pilot bewährten Komponenten werden als Skills, Datenadapter und standardisierte Verträge für weitere Anwendungsfälle nutzbar. Akzeptanz: Ein zweiter Use Case verwendet mindestens einen geprüften Baustein ohne Kopie der Kernlogik.

**Stufe D – Integrierte Wissens- und Betriebsoberfläche.** Das Control Panel zeigt reale Artefakte, Quellenstatus, WorkOrders, Reviewzustände und dokumentierte Aktualisierungen an. Akzeptanz: Der sichtbare Zustand lässt sich auf Originaldateien und tatsächliche Ereignisse zurückführen; fehlende Verbindung wird als solche angezeigt.

**Stufe E – Erweiterte Orchestrierung und kontrollierter Betrieb.** Multi-LLM-Delegation, lokale/private Modelle, Retrieval-Graph, kontinuierliche Tests und Änderungsfolgenanalyse werden nur dort automatisiert, wo die notwendigen Zugriffe und Abnahmekriterien bestehen. Akzeptanz: Reproduzierbarer Workflow mit eindeutiger Zustellung, tatsächlichem ACK, Review, Writeback und menschlicher Freigabe.

Die Stufen sind **fachliche Reifeabschnitte, keine erfundenen Kalenderfristen**. Sie können in Teilen parallel laufen, sofern sie nicht gegenseitig ungeprüfte Zustände voraussetzen. Ein neuer Pilot darf keine bestehende Registry oder Governance-Struktur duplizieren.

## 13.5 Quick Task Development Matrix – priorisierte nächste Arbeitspakete

| Priorität | Task | Ergebnisartefakt | Done-Kriterium | Verantwortlichkeit |
|---|---|---|---|---|
| P0 | Dossier-Kapitel und technische Anhänge konsolidieren | Durchgehende Word-/MD-Reviewfassung | Einheitliche Nummerierung, Glossar, Quellenatlas, keine unmarkierten Soll-Behauptungen | ID03 Redaktion; ID01 Freigabe |
| P0 | Fachliche Risiken FT-Träger adressieren | Befundliste mit korrigierten Rechenfällen | N1–N4 fachlich geprüft; mindestens ein reproduzierbarer Pilotträger | Zuständigkeit per WorkOrder zuweisen |
| P1 | Echte Tool-/Skill-Inventur | Registry-verknüpfte Capability-Matrix | Pro Eintrag Locator, Input, Output, Runtime, Teststatus | Zuständigkeit per WorkOrder zuweisen |
| P1 | Materialkatalog Golden Slice | Reproduzierbarer Material-/Bauteilvergleich | Referenzdaten, Rechenlogik, Datenrechte und Output überprüft | Zuständigkeit per WorkOrder zuweisen |
| P1 | Control Panel JSON-Statuspilot | Lesende, verifizierbare Statusansicht | Aktualisierung und Fehlerzustände anhand echter Daten gezeigt | Zuständigkeit per WorkOrder zuweisen |
| P2 | Knowledge-Object-Graphpilot | Kleiner typisierter Quellgraph | Stabile Identitäten, Fundstellen, QA und Graphabfrage | Zuständigkeit per WorkOrder zuweisen |
| P2 | Multi-LLM-Kommunikationspilot | WorkOrder-/ACK-/Review-/Report-Kette | Tatsächliche Zustellung und Empfang nachgewiesen | Zuständigkeit per WorkOrder zuweisen |

P0–P2 sind **redaktionelle Priorisierungsvorschläge** für die nächste Umsetzungsplanung, keine hiermit neu verteilten Arbeitsaufträge. Sie erzeugen keine Termine, keine neue Ledger-ID und keine implizite Agentenzustellung.

## 13.6 Entwicklungsmetriken ohne Scheingenauigkeit

Ein Prozentwert für „NEXUS insgesamt fertig“ wäre ohne vollständiges Inventar, einheitliche Gewichtung und überprüfte Akzeptanzkriterien nicht belastbar. Stattdessen werden pro abgegrenztem Modul wenige messbare Größen verwendet:

- **Quellenauflösung:** Anteil der benötigten Quellen, für die Identität, Ausgabe und Locator tatsächlich geklärt wurden.
- **Golden-Case-Abdeckung:** Anzahl bestandener fachlicher Referenzfälle bezogen auf den vorab definierten Testsatz.
- **Reproduzierbarkeit:** Anteil wiederholter Läufe mit nachvollziehbar gleichen Eingaben, Softwareständen und Ergebnissen innerhalb definierter Toleranzen.
- **End-to-End-Abschluss:** Anteil der Workflows mit tatsächlichem Ergebnis, Archivierung und erforderlicher Review-/Freigabekette.
- **Integrationszustand:** Verifizierte Zugriffe getrennt nach Lesen, Schreiben, Aktualisieren und Zustellen.
- **Datenqualität:** Anteil der fachlich relevanten Knowledge Objects mit Quellspan, Geltungsbereich und Prüfbefund.

Wo Nenner oder Messlauf fehlen, lautet die Kennzahl **NOT_MEASURED** und nicht 0 % oder ein geschätzter Fertigstellungsgrad. Das ermöglicht eine ehrliche, reproduzierbare Statusmatrix ohne zusätzliche Bürokratie.

# 14. Diskussion, Zusammenfassung und Ausblick

**Kurzfassung.** Die Stärke des NEXUS-Konzepts liegt nicht in einem einzelnen Sprachmodell, sondern in der Kombination aus geordnetem Wissen, überprüfbaren Rechenverfahren, unabhängiger Kontrolle und zielgerichteter Orchestrierung. Die größte praktische Herausforderung ist derzeit die belastbare Verbindung bereits vorhandener Komponenten zu vollständigen Arbeitsabläufen. Die strategische Leitlinie lautet daher: Konsistenz herstellen, Bestand wiederverwenden, einen Pilot vollständig abschließen und erst danach skalieren.

## 14.1 Wissenschaftlich-technische Einordnung

NEXUS-AI ist ein Human-AI-Engineering-Framework für die Bearbeitung wiederkehrender Aufgaben der AEC-Industrie. Das System soll die Stärken probabilistischer Sprachmodelle – Sprachverstehen, semantische Klassifikation, Rechercheunterstützung und Dokumentation – mit regelbasierten Kontrollstrukturen und deterministischen Fachrechnungen kombinieren. Dabei bleibt der Mensch für fachlich und rechtlich relevante Entscheidungen verantwortlich.

Der Begriff **deterministisch geführt** ist bewusst präziser als „deterministische KI“. LLM-Ausgaben können auch bei niedriger Temperatur variieren. Verbindlich reproduzierbar werden nur diejenigen Teile, deren Eingaben, Regeln, Versionen und Ausführungsumgebung kontrolliert und getestet sind. Der Human-AI-Loop dient der fachlichen Urteilsbildung, nicht der Delegation menschlicher Verantwortung an ein Sprachmodell.

## 14.2 Wesentliche Ergebnisse des Dossierentwurfs

**Erstens – gemeinsame Sprache.** Die Architektur braucht eine konsistente Taxonomie mit stabilen Identitäten, definierten Beziehungen und nachvollziehbaren Quellen. Begriffe wie „Quelle“, „Wissensobjekt“, „Skill“, „WorkOrder“, „Run“, „Review“ und „Release“ dürfen nicht synonym verwendet werden. Eine semantische Beziehung ist ein überprüfbarer Wissensvorschlag und keine automatische Tatsachenbehauptung.

**Zweitens – getrennte Autoritäten.** Google Drive, GitHub, technische Fachsolver, LLM-Agenten und persönliche Präferenzen erfüllen unterschiedliche Aufgaben. Die Governance steuert Zuständigkeiten und Versionierung, ersetzt aber keine fachliche Quellenprüfung. Persönliche Erinnerungen helfen beim Routing und bei der Bedienung; sie sind keine technische Primärquelle.

**Drittens – vier funktionale Ebenen.** Wissensmanagement, deterministischer Compute, Verifikation/Peer Review und Orchestrierung bilden ein integriertes System. Governance, Persistenz und menschliche Freigabe wirken quer dazu. Diese Trennung verhindert, dass eine erfolgreiche Textantwort mit einer geprüften Berechnung verwechselt wird.

**Viertens – Umsetzungsdisziplin.** Wiederverwendung vorhandener Artefakte und vertikale Pilotentwicklung haben Vorrang vor zusätzlichen parallelen Frameworks. Ein kleines, vollständig geprüftes Engineering-Ergebnis besitzt höheren praktischen Wert als eine große, nur teilweise verbundene Zielarchitektur.

## 14.3 Grenzen und offene Forschungsfragen

Die dokumentierte Architektur beantwortet noch nicht sämtliche technischen Fragen. Insbesondere bleiben offen: die automatische Auflösung lizenzierter Normquellen; die robuste Extraktion von Formeln und Tabellen aus heterogenen Dokumenten; die maschinelle Geltungsbereichsprüfung bei geänderten Normeditionen; die fachlich sichere Kopplung unterschiedlicher Solver; die Skalierung eines überprüften Knowledge Graph; und die belastbare, konfliktfreie Synchronisation zwischen mehreren Agenten und Speicherorten.

Auch der Nutzen ist noch empirisch zu messen. Aussagen über Zeitersparnis, geringere Fehlerquote, CO₂-Reduktion oder höhere Nachweisqualität benötigen einen definierten Vergleichsfall, eine Messmethode und geeignete Daten. Das Dossier formuliert hierfür ein Evaluationsprogramm, aber keine bereits gemessene Wirkung.

## 14.4 Ausblick und Revisionsprinzip

Das Masterdossier soll nach Integration, unabhängiger Prüfung und ID01-Freigabe als **Strategie-Baseline Revision 1.0** gelten. Seine Funktion ist die dauerhafte Orientierung: Was ist NEXUS, warum wurde es so konzipiert, wie ist es aufgebaut und wie soll es angewendet und weiterentwickelt werden? Die Implementierungsartefakte – Code, Tests, Workflows, Skills, Datenmodelle und Betriebsberichte – bleiben unabhängig versionierbar und entwickeln sich fort.

Eine spätere Revision des Strategiepapiers ist möglich, wenn sich grundlegende Ziele, Architekturprinzipien, Anwendungsgrenzen oder Systemverantwortlichkeiten ändern. Laufende Statusänderungen oder neue Skriptversionen führen dagegen nicht automatisch zu einer Neufassung des Strategiepapiers. Diese Trennung wahrt Stabilität ohne Überregulierung.

## 14.5 Schlussfolgerung

NEXUS-AI wird dann zu einem verlässlichen Engineering-System, wenn aus einer natürlichsprachlichen Aufgabenstellung ein **nachvollziehbarer, quellengebundener und reproduzierbarer Arbeitsprozess** entsteht: mit klarer Semantik, geeignetem Werkzeug, überprüftem Ergebnis, dokumentierter Herkunft und menschlicher Entscheidung. Die Architektur muss dafür nicht maximal komplex sein. Entscheidend ist, dass ihre wenigen tragenden Prinzipien konsequent und praktisch umgesetzt werden.

**Leitsatz:** *Eine gemeinsame Wissensordnung. Ein überprüfbarer Rechenweg. Ein klarer Verantwortungs- und Freigabepfad. Ein nutzbares Ergebnis.*

# Quellen- und Evidenzregister dieses Redaktionsblocks

| Ref. | Direkt gelesene Quelle | Zweck und Einordnung |
|---|---|---|
| Q01 | [CURRENT Manifest](https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view) | Autorität, Rollen, Prinzipien, Entwicklungszustände |
| Q02 | [CURRENT Baseline](https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view) | SSOT, Evidenz, WorkOrders, Persistenz, QA |
| Q03 | [AGB v007.2 – abgerufene Fassung](https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view) | Betriebsregeln; Aktivierungs-/Registrierungswiderspruch offen |
| Q04 | [WORK Folder.md v0.4.0-pilot](https://drive.google.com/file/d/1nDjF78dq3l8PGpXsauzBz1bzHescDSwv/view) | Ablage, Sync-Grenzen und historische Test-/Integrationsbefunde |
| Q05 | [USECASE_REGISTRY.md](https://drive.google.com/file/d/1kkB5prWZ7mf6a0HcJwBOoANRtDbTWS9w/view) | Historisches Use-Case-Inventar, WFL-2026-0001…0017 |
| Q06 | [MCP-ACCESS-TOOLS README](https://drive.google.com/file/d/1a6nh2KwpcI3kVNHJc1okt4ibL7YErDFA/view) | Werkzeugbank, Skriptinventar und dokumentierte lokale Scanmethodik; historische Angaben |
| Q07 | [FT-Träger-Matrix – Bestandsanalyse](https://drive.google.com/file/d/1LrvcfaFBcS6bal3iAC_Codd0Um7Up1tP/view) | Berichte zu sicherheitsrelevanten Fehlern, Tests und fehlender Fachfreigabe |
| Q08 | [Materialkatalog Usermanual v0.1.1](https://drive.google.com/file/d/1vGaFX_S6qMhiZsvva8F-D-S4Qd9uRrh8/view) | Pilotumfang, Grenzen, Installation und QA |
| Q09 | [Control-Panel-Implementierungsplan](https://drive.google.com/file/d/1_nosLpezSN8i-fzTSaNjtnkA-yf11Qfq/view) | Zielarchitektur, vorhandene Teile und offene End-to-End-Integration |
| Q10 | [Systemdossier v0.2.0 – Review](https://drive.google.com/file/d/1SJQ4WeU5AWWQgLRVQDNxUA9FKujUqWKT/view) | Vorarbeit und Querverweise; keine freigegebene Baseline |
| Q11 | [ID06 Peer Review des Arbeitsplans](https://drive.google.com/file/d/1vS3KBK9nnBoDVucMqX5OzoEW8_r0KU0M/view) | Didaktik, Normgliederung, Reviewempfehlungen; nicht Kapitelabnahme |
| Q12 | [Dossier Block 01](https://drive.google.com/file/d/1WvnRBuHXFBbjSzlgIkU_U95oEno6BOmr/view) | Einleitung, Kapitel 1–5 |
| Q13 | [Dossier Block 02](https://drive.google.com/file/d/1Pk29q-NlyCMDGXRbTSgRWx2zhIhhJyCt/view) | Architektur, Wissens-/Datenarchitektur, Rechenlogik |
| Q14 | [Dossier Block 03](https://drive.google.com/file/d/1-x1A4kfM5jVRda193jtMxPxVlMObdaHU/view) | Getting Started, Use Cases, Implementierungsleitfaden |

# Redaktions-QA und Übergabe

- **Kohärenz:** Kapitelnummern 12–14 schließen an die Kapitel 1–11 der vorangegangenen Redaktionsblöcke an.
- **Evidenz:** Aktuell abgerufene Quellen und historisch berichtete Ergebnisse sind sprachlich getrennt; keine neuen Engineering-Tests als ausgeführt behauptet.
- **Umfang:** Dieser Block enthält die Kapitel 12–14 einschließlich Quick Task Development & Implementation Status Matrix und stufenweiser Roadmap.
- **Offen:** Unabhängiges Kapitelreview, vollständige Quellen-/Normeditionen, technische Anhänge, Word-Gesamtausgabe, Ledger/Registry, ID01-Freigabe und Release.
- **Nächster TrueRun:** Technische Anhänge und anschließend redaktionelle Gesamtkonsolidierung der Blöcke 01–04.
