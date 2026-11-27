---
name: 26_11_20_0901_ID02_NEXUS-KNOWLEDGE-IMPLEMENTIERUNGSPLAN_LEDGER-PENDING.md
version: 1.0.0
status: REVIEW_PENDING
timestamp: '2026-11-20T09:01:35+01:00'
timezone: Europe/Vienna
agent_id: ID02
role_id: ID02
owner: Julian Zotter (ID01)
executor: OpenAI Codex
provider: OpenAI
model_id: null
artifact_id: null
provider_file_id: null
canonical_uri: null
provenance: Direktauftrag ID01; WORK-Handbuch und Gates 2026-11-20
verification_status: PLAN_ONLY
registration_status: REGISTRATION_PENDING
registered_at: null
ledger_id: null
ticket_id: null
related_issue: julianzotter/nexus-platform#73
hash_scope: body_utf8_after_closing_frontmatter_lf
content_hash_sha256: 304a850f991283932eefc1d81f198795a7464272fc9a6f009b29b009b1937f86
hash: 304a850f991283932eefc1d81f198795a7464272fc9a6f009b29b009b1937f86
---
# Vom Dateibaum zum belegten Wissensobjekt
## Implementierungsplan für das NEXUS AI Knowledge System

**Entscheidungsvorschlag an ID01.** Der erste nutzbare Ausbau beantwortet eine begrenzte Frage: „In welcher freigegebenen Dokumentrevision steht diese Aussage, und wie öffne ich genau ihre Fundstelle?“ Erst wenn der lokale Durchlauf einschließlich Wiederherstellung gelingt, folgen Modellanbindung und automatischer Austausch. Ein manueller Dokument-Snapshot bleibt während der Betriebsreparatur möglich.

### 1 · Ausgangslage und Systemgrenzen

| Quelle und Stand | Konsequenz für den Ausbau |
|---|---|
| [Praxis-Handbuch in WORK, v1.0.0](https://drive.google.com/open?id=1HpducdBEOf9RGPZkkVw8p70sds_HQ8td) und [Gemini-Windows-Guide](https://drive.google.com/open?id=1ie4-fozcnoYNHkikwql2ZqFtmsXs9TVF), 19.11. | Die drei Handbuchfälle Quelleninventar, Fachworkflow und GitHub-Snapshot werden zu drei separat prüfbaren Betriebswegen. Installierte DSH-Version und effektive Konfiguration am Windows-Rechner erheben. |
| [Systemanalyse vom 20.11., Entwurf v0.1](https://drive.google.com/open?id=1XGu8oTVEJ2awHujHkI_joBiB0K-SkDkq) | Erreichbarkeit allein belegt keine Vollständigkeit. Für jeden Piloten vorab ein Sollinventar festlegen. Berichte über fertige Solver sind Hinweise für spätere Einzelabnahmen. |
| [Betriebsbericht 20.11., 08:27 MEZ](https://drive.google.com/open?id=1KXhtfSyEU--2RocZNRQwd0kxB7HuGpnj) | Dokumentierter Stand: Monitor-Coverage unvollständig, Poller-Tokenrefresh fehlgeschlagen, Delivery übersprungen. CI meldet eine fehlende dlubal-Abhängigkeit. WORK und Registry mit allgemeinem Schreibrecht. Freigabezustand ABWEICHUNG_NO_RELEASE. [Monitor](https://github.com/julianzotter/nexus-platform/actions/runs/44666486516) · [Poller](https://github.com/julianzotter/nexus-platform/actions/runs/44691542520) · [Delivery](https://github.com/julianzotter/nexus-platform/actions/runs/44666539475) |
| [AGB v007.1](https://drive.google.com/open?id=10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg), [WORK-Regel](https://drive.google.com/open?id=1nDjF78dq3l8PGpXsauzBz1bzHescDSwv), [Frontmatter v006, Entwurf](https://drive.google.com/open?id=1rKnQMZbhO6ii0ThnJLhUCRYrXFcDvRbi) | Drive ist Dokument-SSOT. GitHub versioniert Code und freigegebene Review-Snapshots. Der autorisierte Registerschreiber verwaltet die kanonischen Identitäten. SQLite ist ein lokal wiederaufbaubarer Such- und Arbeitsbestand. |

### 2 · Umsetzungsfolge und Abnahme

| Lauf | Konkrete Arbeit | Abnahmetest und aufzubewahrender Beleg |
|---|---|---|
| 01 · Inventar, lokal | Einen abgegrenzten, lesefreigegebenen AEC-Ordner wählen. Windows-PowerShell inventarisiert rekursiv Pfad, Typ, Größe, Änderungszeit, Scanfehler und Offline-Verfügbarkeit. Python übernimmt Metadaten und hasht erst lesbare Bytes. TreeSize-, TreeList- und DIRLIST-Exporte als datierte Importquellen mit Formatkennung behandeln. „DIE LUST“ ist unaufgelöst; DIRLIST ist ein Kandidat. | Soll-/Ist-Anzahl und Liste der ausgelassenen Pfade ausgeben. Zwei gleichnamige Dateien in verschiedenen Ordnern bleiben getrennt. Fehlender Offline-Inhalt erscheint als OFFEN. Dateibaum bleibt unverändert. [Vorhandenes TreeSize-Konzept](https://drive.google.com/open?id=1PrkXNgq2cvEV3Arh_KDmFL4kap8gMT0J) |
| 02 · Extraktion und SQLite | Schema migrieren, dann Text, Markdown, ODT und ODS aus dem Pilotbestand verarbeiten. ODT mit Überschriftenpfad und Absatzindex adressieren, ODS mit Blatt und Zelle. Formeln und gespeicherte Werte getrennt führen, PDF mit physischer Seite. Nicht unterstützte oder beschädigte Dateien im Fehlerregister erfassen. | Testkorpus aus identischer Wiederholung, Umbenennung, neuer Revision und defektem Dokument abarbeiten. Rerun erzeugt keine neuen Revisionen. Frühere Fundstelle bleibt abrufbar. Fehlgeschlagene Dateien erhalten keinen Erfolgscheckpoint. |
| 03 · Atomare Wissensobjekte und Suche | Je prüfbarer Aussage ein Objekt mit Evidenzanker anlegen. Zuerst exakte ID-/Pfadsuche, anschließend lokale FTS5-Volltextsuche. Project-/Rechtefilter vor Ergebnisausgabe anwenden. | Pilotfrage: „Wo steht die freigegebene Normengrundlage?“ Erwartete Quelle und Revision vorab manuell festlegen. Treffer aufrufen und mit Original abgleichen. Gegenproben: fehlende Freigabe, falsches Projekt, ersetzte Ausgabe. Suchprotokoll speichert geordnete Treffer und Indexstand. |
| 04 · API, MCP und Modelle | Python-Kern gemeinsam über CLI und FastMCP-stdio anbieten. Zuerst ausschließlich lesende Operationen. Optional lokale HTTP-API an Loopback. DeepSeek Harness als Windows-Client, Ollama mit explizit gewähltem Qwen-Open-Weight-Modell als lokales Profil anbinden. Versions-/Modell-Digest, Modelllizenz, Kontextlimit und Ressourcenbedarf je Pilot erfassen. | Selbe Anfrage über CLI und MCP ergibt dieselben Quellen-IDs. Modellantwort zitiert zulässige Anker. Fehlendes Modell → eindeutiger Fehler; lokales Profil bleibt ohne ausgehende Modellanfrage nutzbar. Windows-Lauf mit Testdatei und redigiertem Protokoll abnehmen. |
| 05 · Refresh, Diagnose und GitHub | Separaten lokalen Refresh mit Windows-Aufgabenplanung auslösen. Sperre gegen parallele Writer, Checkpoint nach Commit. GitHub Monitor, Drive-Poller und Delivery als eigene Jobs führen. Übernahme per Review-PR an konkrete Drive-Revision und Rohbytehash binden. | Abbruch vor und nach Commit simulieren. Wiederanlauf verliert keine Revision und dupliziert kein Objekt. Backup auf frischem Pfad wiederherstellen und dieselbe Pilotfrage beantworten. Für Betriebsfreigabe drei aufeinanderfolgende echte Schedule-Erfolge je Monitor/Poller nachweisen, Delivery samt Ziel-Readback und separatem Empfänger-ACK prüfen. [Issue #73](https://github.com/julianzotter/nexus-platform/issues/73) |

**Parallel zu Lauf 01:** ID01 bzw. autorisierte Administration prüft wirksame WORK-ACL einschließlich benannter Couric-Schreibrechte sowie OAuth-Client/Token-Zuordnung. Berechtigungsänderungen und Secret-Rotation separat autorisieren. Technische Maintainer beheben Monitor-Coverage und reproduzieren den CI-Fehler in der zum Projekt gehörenden Testumgebung. Lokale Tests mit freigegebenen Pilotkopien können unabhängig fortschreiten.

### 3 · Datenverträge für die Implementierung

| Entität | Identität und Pflichtinhalt |
|---|---|
| Quelle und Revision | Stabile Provider-ID oder explizit vergebene lokale Quell-ID; Pfad als veränderliches Merkmal. Revision mit Quell-ID, Versionskennung, SHA-256 der gelesenen Repräsentation, Datentyp, Abrufzeit, Rechtekontext und Parser-Version. Für native Cloud-Dokumente Exportformat und Providerversion mitführen. |
| Fundstelle | Revisions-ID, Lokatortyp und präziser Seiten-/Absatz-/Zellbezug. Eindeutiger Schlüssel aus Revision, Parser-Version und Locator. Byteidentische Dateien dürfen unterschiedliche Herkunft und Rechte besitzen. |
| Intelligentes atomares Wissensobjekt | Objekt-ID, Projekt, Subjekt, Eigenschaft, Wert/Text, Einheit falls anwendbar, Geltungsbereich, mindestens ein Evidenzanker, Verantwortlicher, Prüfstatus und optionale Vorgänger-ID. Eine geänderte Aussage erzeugt eine neue Version. Konfligierende Aussagen bleiben parallel sichtbar und verhindern PASS bis zur Entscheidung. |
| Lauf, Freigabe und Zustellung | Run-ID, Trigger, Eingabestand, Kernel-/Regelversion, Anfang/Ende, Ergebnis, Fehlerschritt. Freigabe bindet handelnde Person, Aktion, Ziel und Payloadhash. Zustellung speichert Quellrevision, Commit, Ziel-ID und zurückgelesenen Hash. Technischer Erfolg und fachliche Freigabe erhalten getrennte Felder. |

**Kernelvertrag.** Ein Python-Einstiegspunkt führt Schema-, Quellen-, Einheiten- und Statusprüfungen aus. PowerShell und optional Batch reichen Argumente und Exitcode durch. SQLite vergibt Unique Constraints auf Revisions- und Fundstellenschlüssel; Objekte und Checkpoint werden in derselben Transaktion geschrieben. Einen produktiven SQLite-Bestand vor Schemaänderung konsistent sichern und Restore prüfen. SQLite-Datei auf lokaler Disk halten. Für Sync ausschließlich geschlossene, verifizierte Snapshots oder Exporte ablegen. Bei gescheiterter Migration den vorherigen geprüften Snapshot aktivieren.

**Zugriff.** Vorgeschlagene Leseoperationen: `search(query, project, revision)`, `get_object(id, version)`, `get_source_anchor(id)`, `get_run_status(id)`. Antwort enthält Schema-Version, Quelle/Revision, Locator, Prüfstatus und Indexstand. Rechte aus der authentisierten Sitzung bestimmen. CLI, MCP und HTTP nutzen dieselbe Durchsetzung. GitHub- und Drive-Schreiben einem getrennten Dienstkonto bzw. ausdrücklich freigegebenen Vorgang vorbehalten. Ohne zulässigen Treffer liefert der Kern OFFEN. Der Harness darf Suchterme vorschlagen und Ergebnisse formulieren. Fachberechnungen laufen ausschließlich über validierte Solver; Review und ID01-Freigabe bleiben eigenständige Schritte.

**Open Access und externe APIs.** Ein kuratiertes URL-Register führt Betreiber, Domain, Fachgebiet, Lizenz/Nutzungsrecht, Version, zuletzt geprüften Stand und Abrufstatus. Erst Metadaten aufnehmen; Volltextübernahme nur im erlaubten Umfang. Geänderte Inhalte als Revision speichern. Externe Modell-APIs als gesondertes Opt-in-Profil mit Datenklasse, Kostenlimit und protokollierter Zieladresse konfigurieren. Freigegebene öffentliche Testdokumente für den Vergleich lokal/extern verwenden. Open-Weight-Lizenz am konkreten Modellartefakt prüfen.

### 4 · Diagnoseoberfläche und Übergabe

Erste Ansicht: letzte erfolgreiche vollständige Verarbeitung je Datenquelle, Alter der Daten, Inventarabdeckung (erfolgreich verarbeitet / erwartete Quellen), Fehler nach Stufe, aktueller Indexstand. Zweite Ansicht: je Monitor/Poller/Delivery Trigger, Startzeit, Commit, Run-ID, Attempt, Checkpoint, übersprungene Schritte, Fehlertyp und Evidenzlink. Dritte Ansicht: Objekt → Fundstelle → unveränderte Quellrevision → dokumentierte Freigabe. Ohne Nenner bleibt Abdeckung UNVERIFIED. Alter seit letztem Erfolg und Alter seit letztem Versuch getrennt anzeigen.

**Übergabe je Lauf:** Eingabemanifest, ausgeführte Versionen, Testprotokoll, Fehlerliste und Ausgangshash beilegen; anschließend unabhängige Prüfung. Erste Nutzerabnahme ist eine aus dem Index geöffnete, manuell wiedergefundene Originalfundstelle bei abgeschaltetem Modell. Erst danach Vektorsuche oder zusätzliche Agenten mit einem vorab festgelegten Fragensatz gegen die FTS-Baseline bewerten. Die Umsetzung der Läufe, Installationen und Produktionsfreigabe sind Folgeaufträge.

**Steuerquellen:** [Manifest](https://drive.google.com/open?id=1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn) · [Baseline](https://drive.google.com/open?id=1CdwNHr6i8lMG3k8A939kiznLMw8q7J69) · [Ticketregister](https://docs.google.com/spreadsheets/d/1o1ZCZUgsCGTDOwdbJ7EbUCKOKJng1LcJLFnrRiPjYTE/edit) · [Repository-Anweisungen](https://github.com/julianzotter/nexus-platform/blob/main/AGENTS.md).
