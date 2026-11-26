---
name: NEXUS-AI-MASTERDOSSIER-BLOCK01
version: 1.0.0-candidate
status: DRAFT_IN_PROGRESS
created_date: 2026-11-26
author_role: ID03
approved_scope: ID01_APPROVED_WORKPLAN_AND_TOC
release_approval: PENDING
registration_status: REGISTRATION_PENDING
source_set: [AGBS-v007.2, MANIFEST-CURRENT-2026-09-28, BASELINE-CURRENT-2026-09-28, ID06-PEERREVIEW-v1.0.0, DOSSIER-v0.2.0]
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
