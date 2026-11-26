---
name: NEXUS-AI_SYSTEMDOSSIER
version: 1.0.0-REVIEW-CANDIDATE
status: DRAFT_IN_PROGRESS
date: 2026-11-26
author_role: ID03
owner_role: ID01
review_status: PENDING
registration_status: REGISTRATION_PENDING
human_release: PENDING
source_blocks: 01-05
---

# NEXUS-AI Engineering Knowledge Operations System
## Masterdossier · Strategie, Theorie, Anwendung und Implementierung
### Redaktionsblock 01 – Einleitung und Kapitel 1–5

**Dokumentstatus:** Ausarbeitung nach ID01-Freigabe des Arbeitsplans und Inhaltsverzeichnisses. Dieser Block ist kein freigegebenes Produkt, keine normative Fachbemessung und keine Aussage, dass die beschriebenen Zielkomponenten bereits produktiv integriert sind.

## Vorwort – Orientierung für Leserinnen und Leser

NEXUS-AI ist ein technisches Arbeits- und Wissenssystem für die Architektur-, Ingenieur- und Bauwirtschaft (AEC). Es soll verstreute Informationen und wiederkehrende Aufgaben so verbinden, dass Menschen und KI-Assistenten nicht jedes Mal von vorne beginnen müssen. Das System verknüpft fachliche Quellen, strukturierte Wissensobjekte, geprüfte Berechnungswerkzeuge, KI-gestützte Planung und unabhängige Kontrolle. Ein Ingenieur oder eine andere fachlich verantwortliche Person entscheidet, wann ein Ergebnis verwendet oder freigegeben wird.

Der Begriff „AI Operating System“ bezeichnet hier ein *Operations- und Governance-Framework*, nicht ein Betriebssystem im Sinne von Windows oder Linux. NEXUS ist weder eine neue Norm noch eine eigenständige Rechenautorität. Seine Aufgabe besteht darin, den Weg von der Anfrage bis zum überprüfbaren Arbeitsergebnis zu organisieren.

Das Dokument richtet sich an drei Lesergruppen: Anwender sollen die Arbeitsweise rasch verstehen; Ingenieure sollen Quellen-, Rechen- und Prüfprinzipien beurteilen können; Entwickler sollen daraus konkrete Komponenten und Schnittstellen implementieren. Es folgt dem Prinzip zunehmender Detailtiefe: zuerst Orientierung, danach Theorie und Architektur, zuletzt Implementierung und technische Anhänge.

**Lesewege:** Wer NEXUS erstmals nutzt, beginnt mit Vorwort, Kapitel 1, 4, 5 und dem späteren Kapitel „Getting Started“. Fachlich Prüfende ergänzen Kapitel 2, 3 sowie die Rechen- und Verifikationskapitel. Entwickler benötigen zusätzlich Architektur, Datenmodelle, Implementierungsleitfaden und Anhänge.

## Inhaltsübersicht der Gesamtausgabe

1. Anwendungsbereich und Systemgrenzen
2. Maßgebende Bezugsdokumente
3. Begriffe, Abkürzungen und Taxonomie
4. Ausgangslage, Problemstellung und Hauptziele
5. Grundprinzipien, Methodik und Denklogik
6. Systemarchitektur und Datenflüsse
7. Wissens- und Datenarchitektur
8. Rechen- und Nachweislogik
9. Getting Started und User Manual
10. Engineering-Use-Cases und Referenzabläufe
11. Implementation Guide und Softwareanforderungen
12. Verifikation, Evaluation und Qualitätssicherung
13. Entwicklungsstand, Statusmatrix und Roadmap
14. Diskussion, Zusammenfassung und Ausblick
A–F. Technische Anhänge: Steuerdateien, Begriffe, Quellen, Verzeichnisatlas, Schemas und Referenz-Use-Cases.

# 1. Anwendungsbereich und Systemgrenzen

**Kurzfassung.** NEXUS-AI organisiert wissens- und rechenintensive Arbeiten im AEC-Umfeld. Es unterstützt fachliche Entscheidungen durch wiederverwendbare Quellen, Werkzeuge und Prüfverfahren; es ersetzt keine fachliche Verantwortung.

## 1.1 Zweck

Das System soll für Aufgaben wie Tragwerksplanung, Normenrecherche, Baustoff- und Bauteildatenverwaltung, nachhaltiges Bauen, BIM/IFC-Datenintegration, Ausschreibung und technische Dokumentation eine konsistente Arbeitsumgebung bereitstellen. Die einzelne Aufgabe wird als *Use Case* beschrieben: eine konkrete Problemstellung mit Eingangsdaten, Quellen, Arbeitsschritten, Werkzeugen, Prüfbedingungen und Ergebnisartefakten. Der Use Case ist die Brücke zwischen abstrakter Systemarchitektur und messbarem Nutzen.

NEXUS bündelt bestehende Leistungen und Anwendungen, statt sie zwangsläufig zu ersetzen. Ein vorhandenes Python-Skript, eine Fachsoftware, eine Datenbank oder ein bereits geprüfter Workflow soll wiederverwendet werden, wenn seine Eignung und Version nachgewiesen sind. Eine neue Implementierung ist nur dann zweckmäßig, wenn eine bestehende Lösung fehlt oder ihre Grenzen belegt sind.

## 1.2 Systemgrenzen

Das System umfasst die Steuerung und Dokumentation von Arbeitsabläufen, das Auffinden und Strukturieren von Wissen, die Auswahl geeigneter Rechen- und Prüfwerkzeuge, die Vorbereitung und Bewertung von Ergebnissen sowie deren nachvollziehbare Ablage. Es kann lokal, cloudgestützt oder hybrid betrieben werden; der konkrete Integrationsgrad muss pro Komponente geprüft werden.

Nicht zum zugesicherten Funktionsumfang gehören: eine allgemeine Garantie richtiger LLM-Aussagen; die automatische rechtliche Gültigkeit eines Normenauszugs; eine ungeprüfte Übernahme von Projekt- oder Memory-Daten als Primärquelle; die Freigabe von Standsicherheitsnachweisen allein durch LLM-Konsens; oder eine pauschal behauptete Echtzeitsynchronisierung sämtlicher Google-Drive- und GitHub-Bestände.

## 1.3 Verantwortung und Geltung

ID01 ist innerhalb der NEXUS-Governance die strategische und finale Freigabeinstanz. Für konkrete Ingenieurleistungen verbleiben die jeweils geltenden fachlichen, vertraglichen und rechtlichen Verantwortlichkeiten bei den zuständigen Personen und Organisationen. Die interne Freigabe eines Softwareartefakts ist nicht gleichbedeutend mit der baurechtlichen oder fachtechnischen Freigabe einer Konstruktion.

Die Anwendung von Eurocodes, nationalen Anhängen, OIB-Richtlinien und anderen Regeln setzt eine Prüfung von Ausgabe, Rechtsraum, Anwendungsfall und Geltungsstand voraus. Dieses Handbuch erläutert die Systematik; es reproduziert keine nicht geprüften normativen Bemessungsvorschriften.

## 1.4 Produktumfang und Reifegrade

Für jede Komponente ist zu unterscheiden zwischen **vorhandenem Artefakt**, **ausgeführter Funktion**, **bestandener Prüfung** und **freigegebener produktiver Anwendung**. Eine Datei im Repository belegt ihre Existenz, nicht die erfolgreiche Ausführung. Ein bestandener lokaler Test beweist nur seinen dokumentierten Testumfang. Diese Trennung gilt ebenso für Datenbanken, Agenten, Connectoren, Dashboards und Solver.

# 2. Maßgebende Bezugsdokumente

**Kurzfassung.** NEXUS unterscheidet Systemsteuerung, fachliche Regelwerke und technische Implementierungsquellen. Für jede Aussage muss erkennbar sein, welche Quelle in welcher Rolle herangezogen wurde.

## 2.1 Interne Systemdokumente

Die aktuelle Systemsteuerung wird aus den von ID01 angenommenen NEXUS-Originalen abgeleitet. Im vorliegenden Redaktionslauf wurden folgende Dokumente tatsächlich gelesen:

- **NEXUS-AGBs v007.2**, Google Drive `10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg`: operative Start-, Kommunikations-, Ablage- und Registrierungsregeln. Der Text enthält einen zu klärenden Unterschied zwischen ausgewiesener Version und Aktivierungs-/Übernahmevermerk; die vorliegende Fassung ist daher als gelesener Dokumentstand, nicht als unabhängig bestätigter Rohbyte-Release zu verstehen.
- **CURRENT Manifest**, Google Drive `1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn`, Basis 2026-09-28, Rollenregister v1.2 vom 24.11.2026: Ziele, Autorität, Rollen, Grundprinzipien und Grenzen.
- **CURRENT Baseline Instructions**, Google Drive `1CdwNHr6i8lMG3k8A939kiznLMw8q7J69`: ausführbare Anforderungen an Datenidentität, Speicherung, Evidenz, Änderungen und Prüfung.
- **WORK Folder.md**, Google Drive `1nDjF78dq3l8PGpXsauzBz1bzHescDSwv`, v0.4.0-pilot: operativer Arbeitsraum und bekannte Integrationsgrenzen.
- **ID06 Peer Review v1.0.0**, Google Drive `1vS3KBK9nnBoDVucMqX5OzoEW8_r0KU0M`: redaktionelle Empfehlungen für normähnlichen Aufbau, Lesbarkeit und durchgehende Beispiele; nicht selbst eine Steuerdatei.
- **Systemdossier v0.2.0-candidate**, Google Drive `1SJQ4WeU5AWWQgLRVQDNxUA9FKujUqWKT`: vorausgehende fachliche Entwurfsbasis, nicht als Rev. 1.0 freigegeben.

Die genauen Pfade, Versionsnachweise und ergänzenden Frontmatter-Dateien werden im technischen Anhang zusammengestellt. Die Originale bleiben maßgeblich; ein Auszug im Anhang dient nur der Nachlesbarkeit des dokumentierten Stands.

## 2.2 Fachliche Regelwerke

Für die priorisierten AEC-Anwendungsfälle sind insbesondere die Familien **EN 1990** (Grundlagen), **EN 1991** (Einwirkungen), **EN 1992** (Beton), **EN 1995** (Holz), die jeweiligen österreichischen Anwendungsdokumente, **CEN/TS 19103** (Holz-Beton-Verbund) und die einschlägigen **OIB-Richtlinien** als *Quellenkandidaten* zu berücksichtigen. Die rechtliche oder normative Verbindlichkeit einzelner Fassungen wird nicht aus diesem Handbuch abgeleitet. Die konkrete Quelle muss im jeweiligen Use Case mit Ausgabe, Abschnitt, nationaler Umsetzung und Anwendungsbereich verifiziert werden.

## 2.3 Quellenkategorien und Nachweislogik

Systemregeln steuern, *wie* gearbeitet wird. Fachnormen und Rechtsquellen bestimmen, *welche* Anforderungen im konkreten Anwendungsfall gelten. Wissenschaftliche Publikationen liefern Methoden und Erkenntnisse, Herstellerdokumente produktspezifische Daten, Projektdokumente konkrete Randbedingungen und Testprotokolle Ausführungsnachweise. LLM-Ausgaben dürfen diese Kategorien nicht stillschweigend vermischen.

Ein belastbarer Nachweis besteht nicht nur aus einem Link, sondern aus einem identifizierbaren Dokument, seiner Fassung, einem konkreten Fundort und der nachvollziehbaren Verwendung im Arbeitsergebnis. Bei widersprüchlichen Quellen ist der Konflikt sichtbar zu machen und nach Zuständigkeit, Geltungsbereich und Beleglage zu klären.

# 3. Begriffe, Abkürzungen und Taxonomie

**Kurzfassung.** Eine gemeinsame Sprache ist Voraussetzung für zuverlässige Zusammenarbeit zwischen Menschen, Agenten und Software. NEXUS führt stabile Objektidentitäten und unterscheidet sie von frei veränderbaren Schlagworten und semantischen Beziehungen.

## 3.1 Grundbegriffe

| Begriff | Definition im NEXUS-Kontext |
|---|---|
| AEC | Architecture, Engineering and Construction; Anwendungsdomäne des Systems |
| Use Case | Konkret abgegrenzter Anwendungsfall mit Eingaben, Methode, Ergebnis und Prüfziel |
| Workflow | Wiederholbare, geordnete Folge von Arbeitsschritten und Zuständen |
| Skill | Wiederverwendbare, beschriebene Fähigkeit mit Ausführungsvoraussetzungen und Ressourcen |
| Agent | Ausführende oder prüfende KI-Instanz mit Rolle, Laufzeit und definiertem Zugriff |
| SSOT | Single Source of Truth: festgelegte führende Quelle für eine Objektklasse |
| Source | Identifizierte Originalquelle mit Herkunft und stabiler Referenz |
| Knowledge Object | Strukturierte Wissenseinheit mit Typ, Identität, Herkunft und Status |
| Chunk | Referenzierbarer Ausschnitt einer Quelle, nicht automatisch eine eigenständige Wahrheit |
| Knowledge Graph | Netz aus typisierten Objekten und belegten Beziehungen |
| RAG | Retrieval-Augmented Generation: Generierung auf Basis abgerufener Inhalte |
| Solver | Ausführendes, für den jeweiligen Zweck geprüftes Rechenprogramm |
| Peer Review | Fachliche Prüfung durch eine tatsächlich unabhängige Prüfinstanz |
| WorkOrder | Beauftragte, statusgeführte Arbeit mit definiertem Ergebnis |
| Artifact | Persistentes Arbeitsergebnis wie Bericht, Code, Modell, Tabelle oder Datensatz |
| Ledger/Registry | Nachvollziehbare Aufzeichnung beziehungsweise Registrierung von Vorgängen und Objekten |
| Baseline | Zu einem definierten Zeitpunkt freigegebener, versionierter Referenzstand |
| Provenienz | Dokumentierte Herkunft und Ableitung einer Information oder eines Ergebnisses |

## 3.2 Taxonomische Ebenen

Die fachliche Klassifikation folgt einer hierarchischen Achse: **Wissenschaft/Technik → Ingenieurwissenschaften → Bauingenieurwesen → Konstruktiver Ingenieurbau → Fachanwendung → Bauteil → Werkstoff/System → Regelwerksfamilie → Methode → Nachweis**. Diese Achse beschreibt fachliche Zugehörigkeit, aber nicht sämtliche Beziehungen.

Projekt, Standort, Norm, Person, Werkzeug, Quelle, Use Case und Status sind ergänzende, orthogonale Dimensionen. Beispielsweise kann eine Holz-Beton-Verbunddecke zugleich einem Tragwerks-Use-Case, einem Schulbauprojekt, einer Materialkombination, mehreren Normenfamilien und einem Python-Solver zugeordnet sein. Das erfordert nicht fünf konkurrierende Dateiidentitäten.

## 3.3 Semantische Relationen und Identität

Die Beziehungen `USES_METHOD`, `REQUIRES`, `REFERENCES`, `DERIVED_FROM`, `IMPLEMENTS`, `PRODUCES`, `VALIDATED_BY` und `STORED_AT` erfüllen unterschiedliche Zwecke. Eine Datei kann eine Methode erwähnen, ohne sie zu implementieren; zwei Dokumente können thematisch ähnlich sein, ohne identisch zu sein. Die Relation `SYNCED_TO` darf nur gesetzt werden, wenn der tatsächliche Transfer nachgewiesen wurde.

Die im Vorgängerdossier vorgeschlagenen Domänen D01–D20 und Routinglabels KV01–KV20 sind **Arbeitsklassifikationen**. Sie ersetzen keine bestehende kanonische Registry und werden erst nach Abgleich mit vorhandenen Indizes und Freigaben zu verbindlichen IDs. Das Glossar des Systems ist die zuständige Stelle für abgestimmte Begriffe; dieses Kapitel ist eine lesbare Einführung, keine parallele Glossardatenbank.

## 3.4 Begriffsdisziplin in der Praxis

Jeder Agent soll zwischen *Quelle gefunden*, *Quelle gelesen*, *Inhalt geprüft*, *Berechnung ausgeführt* und *Ergebnis freigegeben* unterscheiden. Gleichlautende Bezeichnungen dürfen keine Identität vortäuschen. Nicht geklärte Synonyme werden als Kandidaten geführt, bis ihre Bedeutung fachlich oder organisatorisch bestätigt ist.

# 4. Ausgangslage, Problemstellung und Hauptziele

**Kurzfassung.** NEXUS reagiert auf fragmentierte Ingenieurdaten, wiederholte manuelle Arbeit und die begrenzte Verlässlichkeit freier LLM-Generierung. Die Lösung ist nicht ein größeres Sprachmodell, sondern eine integrierte Arbeitskette mit nachvollziehbaren Quellen und Prüfungen.

## 4.1 Ausgangslage

Fachwissen liegt verteilt in Normen, Zulassungen, wissenschaftlichen Arbeiten, Datenbanken, technischen Berichten, E-Mails, Excel-Berechnungen, Skripten, CAD-/BIM-Modellen und Projektarchiven. Zusätzlich existieren persönliche Arbeitshinweise, Promptvorlagen und Agentenkonfigurationen. Diese Informationen haben unterschiedliche Eigentümer, Dateiformate, Aktualisierungszyklen und Verlässlichkeitsgrade.

Ein LLM kann Dokumente zusammenfassen, Suchbegriffe zuordnen und Arbeitspläne vorschlagen. Es kann aber aus einer sprachlich plausiblen Aussage keinen Normnachweis machen. Ohne eindeutige Quellen, Versionskontrolle, Rechenautorität und unabhängige Prüfung drohen falsche Kennwerte, unbemerkte Annahmen, Doppelentwicklungen und unklare Freigaben.

## 4.2 Kernproblem

Das zentrale Problem ist die fehlende durchgängige Verbindung zwischen **Anfrage, Begriff, Quelle, Methode, ausführendem Werkzeug, Prüfnachweis und archiviertem Ergebnis**. Eine Sammlung guter Einzelkomponenten reicht nicht aus, wenn der Übergang zwischen ihnen nicht kontrolliert ist.

Hinzu kommt eine organisatorische Herausforderung: Google Drive, GitHub, lokale Dateien und ChatGPT-Erinnerungen erfüllen unterschiedliche Aufgaben. Werden diese Ebenen ohne klare Zuständigkeit vermischt, entstehen konkurrierende Wahrheitsstände. Deshalb trennt NEXUS persönliche Präferenzen von fachlichen Originalquellen und operative Arbeitsdokumente von freigegebenen Baselines.

## 4.3 Hauptziele

Die im Vorgängerdossier genannten Ziele werden als Arbeitsziele übernommen: **Engineering Accuracy**, **Knowledge Sovereignty**, **System Reliability**, **Workflow Automation**, **Resource Efficiency**, **Continuous Improvement** und **Sustainable Construction**. Sie sind keine nachgewiesenen Leistungskennzahlen, sondern Bewertungsmaßstäbe für die weitere Implementierung.

Für den produktiven Nutzen ist entscheidend, ob ein Use Case vollständig durchlaufen werden kann: mit passenden Eingaben, identifizierten Quellen, ausgeführter Berechnung oder Verarbeitung, nachvollziehbarer Prüfung und einem nutzbaren Artefakt. Ein Konzept ohne diese Kette bleibt ein Konzept.

## 4.4 Forschungs- und Entwicklungsfragen

1. Wie wird aus einer natürlichsprachlichen Anfrage eine stabile technische Aufgabenbeschreibung?
2. Wie lassen sich fachliche Begriffe mit Quellen, Normen, Methoden und vorhandenen Tools verknüpfen?
3. Wie wird die Rechen- und Datenverarbeitung von der LLM-Textgenerierung getrennt?
4. Wie werden Fehler und widersprüchliche Ergebnisse erkannt, ohne jeden Arbeitsvorgang unnötig zu blockieren?
5. Wie wird ein End-to-End-Ergebnis reproduzierbar und für spätere Projekte wiederverwendbar?

## 4.5 Erfolgskriterien

Geeignete Kennzahlen sind unter anderem die Auflösbarkeit von Quellenverweisen, die korrekte Zuordnung zu Fachdomänen und Regelwerken, bestandene Einheiten- und Regressionstests, die Wiederholbarkeit von Rechenläufen, der Anteil tatsächlich abgeschlossener Workflows und die Zahl ungelöster Konflikte. Ohne Messung werden keine Verbesserungsprozente behauptet.

# 5. Grundprinzipien, Methodik und Denklogik

**Kurzfassung.** Das LLM organisiert Vorschläge, die Wissensbasis liefert prüfbare Grundlagen, geeignete Software führt Berechnungen aus, unabhängige Prüfungen suchen Fehler, und der Mensch entscheidet. Governance ist der gemeinsame Rahmen – nicht eine zusätzliche Fachschicht.

## 5.1 Der methodische Kern

NEXUS ist ein *deterministisch geführtes* System mit probabilistischen LLM-Komponenten. Das bedeutet: Arbeitszustände, Quellenidentitäten, Prüfbedingungen und Freigabeschritte können formal definiert und überprüft werden. Es bedeutet nicht, dass ein LLM bei Temperatur 0 stets identische oder richtige Aussagen erzeugt.

Das übergreifende Verfahren lautet:

**Anfrage → Intent/Klassifikation → Quellenauflösung → Methodenauswahl → Tool-/Solverausführung → Verifikation → fachliche Freigabe → Dokumentation und Wiederverwendung.**

Der Ablauf ist als Steuerungsmodell zu verstehen. Ein reiner Recherche-Use-Case benötigt keinen Solver; ein statischer Bemessungsfall benötigt dagegen belastbare Rechen- und Normprüfungen. Der Orchestrator wählt die erforderlichen Schritte nach Aufgabenart, nicht nach einem starren Maximalprozess.

## 5.2 Vier funktionale Ebenen

**Wissensebene:** Verwaltet Dokumente, Metadaten, strukturierte Wissensobjekte, Suchindizes und semantische Relationen. Der Abruf muss die Originalquelle sichtbar lassen.

**Rechen- und Verarbeitungsebene:** Führt deterministische Parser, Python-Skripte, Fachsolver, numerische Methoden und gegebenenfalls CAD-/BIM-Transformationen aus. Ergebnisse werden mit Eingaben, Einheiten und Softwareversionen verbunden.

**Prüfebene:** Prüft Quellen, Eingaben, Annahmen, Konsistenz, numerische Resultate und Verfahrenskonformität. Ein zweites LLM kann Fehlerkandidaten aufzeigen; es ersetzt keine unabhängige technische Nachrechnung.

**Orchestrierungs- und Interaktionsebene:** Versteht den Auftrag, wählt vorhandene Skills, verwaltet Arbeitszustände und kommuniziert mit Benutzern, Werkzeugen und weiteren Agenten. Sie protokolliert den tatsächlichen Ausführungsstand.

Die NEXUS-Governance umfasst alle vier Ebenen: Zuständigkeiten, Freigaben, Ablage, Provenienz, Zugriffsgrenzen und Änderungen.

## 5.3 Reuse-first und Vertical-first

**Reuse-first** bedeutet, vor einer Neuentwicklung in den vorhandenen Indizes, Registries, Skills und Repositories nach geeigneten Komponenten zu suchen. Die Wiederverwendung setzt eine Prüfung ihrer Eignung voraus; ein ähnlicher Dateiname genügt nicht.

**Vertical-first** bedeutet, zuerst einen konkreten Use Case vom Eingang bis zum überprüften Ergebnis zu vervollständigen, bevor zusätzliche generische Infrastruktur entwickelt wird. Das reduziert das Risiko, viele isolierte Komponenten zu besitzen, aber keinen zuverlässig funktionierenden Gesamtprozess.

## 5.4 Umgang mit Fehlern

NEXUS unterscheidet zwischen normalen Entwicklungsabweichungen und kritischen Freigabeproblemen. Ein fehlender Datenbankzugang kann einen einzelnen Retrieval-Schritt blockieren, ohne die Dokumentation anderer Ergebnisse zu verhindern. Ein fehlender Normnachweis verhindert dagegen die Behauptung einer normkonformen Bemessung. Fehler werden sichtbar gemacht und dem betroffenen Schritt zugeordnet; sie lösen nicht automatisch einen Systemstillstand aus.

## 5.5 Durchgehendes Referenzbeispiel

Als didaktischer Leitfall eignet sich eine Holz-Beton-Verbunddecke: Ein Benutzer formuliert Geometrie, Belastung und Zielnachweise. NEXUS identifiziert den fachlichen Use Case, ruft relevante Originalquellen ab, prüft die Eingaben, wählt ein vorhandenes Berechnungsmodul, führt die Rechnung in einer geeigneten Rechenumgebung aus und kontrolliert Ergebnis und Fundstellen. Anschließend entsteht ein Bericht mit Herkunft und Status. **Dies beschreibt den beabsichtigten Workflow, keinen hier ausgeführten oder bereits abgenommenen Bemessungslauf.**

## 5.6 Persönlicher Kontext als Assistenz, nicht als technische Quelle

Persönliche Hinweise und ChatGPT-Erinnerungen können Stil, Prioritäten und typische Arbeitsweisen beeinflussen. Projektkennwerte, Normversionen, Codezustände oder aktuelle Integrationsstände müssen dagegen aus den zuständigen Originalquellen abgerufen werden. Ein Gedächtniseintrag ist keine technische Primärevidenz. So bleibt die Zusammenarbeit persönlich effizient, ohne die Nachweisführung zu verwässern.

## Redaktioneller Prüfvermerk Block 01

**Gelesene Grundlagen:** AGBs v007.2, Manifest CURRENT, Baseline CURRENT, WORK Folder.md, ID06 Peer Review v1.0.0, Dossier v0.2.0-candidate. **Nicht nachgewiesen:** vollständiger Normvolltext, vollständige aktuelle Registry-/Skill-Inventur, unabhängiges Peer Review dieses neuen Blocks, Ledgerregistrierung, Word-Export, PDF-Freigabe. **Fortsetzung:** Block 02 – Kapitel 6 bis 8 (Architektur, Daten- und Rechenlogik); danach Kapitel 9–11, 12–14 und Anhänge.

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

