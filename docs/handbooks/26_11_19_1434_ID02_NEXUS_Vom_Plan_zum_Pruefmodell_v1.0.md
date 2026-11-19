---
title: "Vom Plan zum Prüfmodell"
subtitle: "NEXUS-Benutzerhandbuch und Implementierungsguide für CAD, RFEM und nachvollziehbare Wissensablage"
version: "1.0"
created_at: "2026-11-19T14:34:43+01:00"
owner: ID02
executor: OpenAI Codex
status: PROPOSED
registration_status: REGISTRATION_PENDING
ticket_id: null
canonical_folder_id: 1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP
---

# Vom Plan zum Prüfmodell
**Benutzerhandbuch und Implementierungsguide für NEXUS · Ausgabe 1.0 · 19. November 2026**

Dieses Handbuch begleitet einen konkreten Auftrag: Aus einem Planstand ein Bauteil eindeutig identifizieren, seine Geometrie prüfen und einen reproduzierbaren Modellvergleich vorbereiten. Der erste nutzbare Zwischenstand ist ein Quellenbeleg mit Planrevision, Objektkennung, Prüffrage und offener Entscheidung. Bereits dieser Stand lässt sich in WORK übergeben.

## 1 · Als Anwender einen Prüflauf vorbereiten

1. **Auftrag eingrenzen.** Im [Ticketregister](https://docs.google.com/spreadsheets/d/1o1ZCZUgsCGTDOwdbJ7EbUCKOKJng1LcJLFnrRiPjYTE/edit) nach Projekt, Bauteil und Prüffrage suchen. Vorhandenen Auftrag öffnen. Für einen neuen Auftrag das Ziel im Klartext festhalten, bis das Register eine Kennung liefert. Zulässige Aktionen angeben, etwa Lesen, Modellkopie erstellen oder Berechnung starten.
2. **Planstand feststellen.** Über den bestehenden Index das Original öffnen. Drive-ID, Revision, Exportformat, Geschoss, Achse und Bauteilposition erfassen. Bei DXF/IFC-Paaren Planindex und Koordinatenbezug beider Exporte vergleichen. Eine Dateiliste wie „RFEM 5.29 AnythingSearchResults“ hilft beim Auffinden. Modellinhalt und Ergebnisstand erst nach Öffnen des konkreten Modells bestätigen.
3. **Ein Bauteil auswählen.** Für den Einstieg genügt ein Randbalken mit zwei eindeutig bezeichneten Auflagern. Im Plan Achsabstand, Bezugshöhe und Querschnitt ablesen, jeweils mit Fundstelle und Einheit. Lagerwirkung, Gelenke und Exzentrizitäten aus freigegebenen Detailunterlagen ergänzen. Fehlt eine Angabe, die davon abhängige Modellannahme offen ausweisen.
4. **Vergleich bestellen.** Einheiten, Modellversion, Lastfall, lokale Achsen, Vorzeichen und Ergebnisstelle festlegen. Einen unabhängigen Referenzwert und eine projektspezifische Toleranz vor dem Lauf vereinbaren. Der Bearbeiter liefert Modellkopie, Eingabeprotokoll, Ergebnisexport und Abweichungsliste. Die fachliche Entscheidung liegt bei der verantwortlichen Person.
5. **Ergebnis wiederfinden.** In WORK die angegebene Datei-ID öffnen. Vom Ergebnis zur Modellrevision und von dort zum Planobjekt zurückgehen. Für die Wiederverwendung jede Korrektur als neue Revision mit Vorgängerreferenz dokumentieren.

**Kopierbarer Arbeitsauftrag für den ersten Durchlauf**

> Vergleiche am ausgewählten Randbalken die beiden Auflagerachsen im IFC mit dem bemaßten DXF-Grundriss desselben Planstands. Protokolliere GlobalId, DXF-Layer und Handle, Ausgangseinheit, Lagebezug und Fundstelle der Kontrollmaße. Liste Widersprüche einzeln auf. Liefere zunächst den Geometrievergleich. Warte für die Übertragung von Lagerbedingungen und Lasten auf die fachliche Bestätigung.

## 2 · Die Ideen des Control-Tower-Entwurfs in WORK einsetzen

| Aufgabe | Operative Umsetzung | Prüfbarer Abschluss |
|---|---|---|
| Quellen aufnehmen und früheres Wissen nutzen | Bestehendes Register und Index zuerst nach stabiler ID, danach nach Projekt und Position durchsuchen. Fundstellen aus Chat, OneDrive oder lokaler Suche als Kandidaten erfassen. | Original und verwendete Revision lassen sich erneut öffnen. |
| Extrahieren und kuratieren | Aus einer Quelle einen Datensatz pro Objekt und Aussage ableiten. Eltern-ID, Locator und Transformationsschritt mitführen. Widersprüchliche Werte nebeneinander zur Entscheidung vorlegen. | Ein Reviewer kann jeden Wert im Original finden. |
| Freigeben und verteilen | ID02 koordiniert. Zuständiger Registerschreiber registriert. Fachprüfer beurteilt die technische Aussage. ID01 entscheidet über organisatorische Übernahme. | Registrierung, Review, Freigabe, Zustellung und ACK haben getrennte Belege. |
| Wiki, Dashboard oder RAG betreiben | Ansichten aus belegten Datensätzen erzeugen. Suchtreffer verlinken das Original und zeigen Version und Prüfstatus. | Bei geändertem Original wird die abgeleitete Aussage zur erneuten Prüfung markiert. |

Der Rollout-Entwurf beschreibt A1–A5 und eine eigene Workflow-Registry. Für den laufenden Betrieb gelten Manifest §4, Baseline MUST-20–25 sowie WORK-AGBs v007.1 §§5–7. A1–A5 lassen sich als Aufgabenbeschreibungen verwenden. Eine Übertragung auf aktuelle Schreibrechte erfordert einen belegten Rollenentscheid. Dokumente und Aufträge gehören nach WORK, Lauf- und Wartungslogs in das vorgesehene History-Verzeichnis. Für dieses Handbuch steht die Registrierung aus.

## 3 · Implementierung in drei prüfbaren Schritten

### Schritt A · Lesenden Quellenlauf aufbauen

Mit einer unveränderten lokalen Exportkopie beginnen. Das folgende Hilfsprogramm verwendet nur die Python-Standardbibliothek. Als `quellbeleg.py` speichern. Der zweite Parameter bezeichnet die fachliche Fundstelle im Original.

```python
import argparse
import hashlib
import json
from pathlib import Path


def source_record(path: Path, locator: str) -> dict[str, str | int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
            size += len(chunk)
    return {"filename": path.name, "size_bytes": size,
            "sha256": digest.hexdigest(), "locator": locator}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("locator")
    args = parser.parse_args()
    print(json.dumps(source_record(args.source, args.locator), ensure_ascii=False))
```

Beispiel für den im CAD-Arbeitspapier genannten Export, sobald er lokal vorliegt:

```powershell
python .\quellbeleg.py ".\Mylius.ifc" "Dateiebene vor IFC-Objektauswahl"
```

Erwartet wird ein JSON-Objekt mit Dateiname, Byteumfang, SHA-256 und Fundstelle. Für die NEXUS-Übergabe zusätzlich Quell-ID, Revisionsstand, Abrufzeit und verantwortlichen Bearbeiter erfassen. Der Digest identifiziert die gelesenen Bytes. Nach einer Änderung muss der frühere Beleg der früheren Revision zugeordnet bleiben. Für den späteren Schema-Validator Pflichtfelder und Typen gemäß WORK-AGBs §6 abbilden. Fehlende Sachverhalte als offen führen. [JSON-Schema-Tutorial mit Validierungsbeispiel](https://json-schema.org/learn/getting-started-step-by-step) · [W3C PROV mit Beispielen für Quelle, Bearbeitung und Verantwortlichen](https://www.w3.org/TR/prov-primer/)

### Schritt B · IFC und DXF gegeneinander prüfen

| Eingabe | Implementierung | Abnahme am Referenzbauteil |
|---|---|---|
| IFC | Mit IfcOpenShell öffnen. Passende IFC-Klasse auswählen, GlobalId und Geschoss ermitteln. Projektlängeneinheit und Platzierungskette bis zum gemeinsamen Koordinatensystem auflösen. | Zwei überprüfbare Punkte und Bauteilbezeichnung mit dem Plan vergleichen. Unklare Zuordnung als offenen Befund ausgeben. |
| DXF R12 und DXF 2018 | Mit ezdxf den Modellbereich prüfen. Layer, Entitätstyp, Handle und Blockreferenzen erfassen. Verschachtelte Blocktransformationen vor der Auswertung auflösen. Bei fehlender Einheitsangabe ein bemaßtes Kontrollmaß heranziehen und Quelle dokumentieren. | Beide Exporte am selben Ausschnitt prüfen. Fehlende Kontur, Beschriftung oder Blockauflösung festhalten. Den Export wählen, der die erforderlichen Merkmale reproduzierbar erhält. |
| IFC ↔ DXF | Zuordnung über Geschoss, Achsen und Lage mit Maßkontrolle. Quelleinheit dokumentieren, Koordinaten in Meter überführen und erst dann vergleichen. | Mehrdeutige Kandidaten, doppelte Objekte und ungeklärte Verschiebungen bleiben im Prüfprotokoll. |

Die Anlagen nennen Mylius als Vergleichsfall. Für tatsächliche Messwerte sind die Modell- und Zeichnungsoriginale erforderlich. Die vorgesehene Abnahme umfasst auch einen negativen Test mit vertauschter Einheit. [IfcOpenShell-Codebeispiele](https://docs.ifcopenshell.org/ifcopenshell-python/code_examples.html) · [ezdxf-Tutorial zu Daten und Layouts](https://ezdxf.readthedocs.io/en/stable/tutorials/getting_data.html)

### Schritt C · Den RFEM-Pilot betreiben

1. **Schnittstelle wählen.** Bei RFEM 5.29 den vorhandenen Windows-Arbeitsplatz, Modellversion, Lizenz und tatsächlich verfügbare Leseschnittstelle feststellen. Ein Referenzergebnis aus der Oberfläche exportieren. Für bestehende RFEM-6-Projekte mit `RFEM_Python_Client` den zugehörigen Clientstand isoliert reproduzieren. Für eine neue Integration den dokumentierten gRPC-Einstieg von Dlubal verwenden. Der in den internen Notizen verwendete Port ist projekt- und schnittstellenspezifisch.
2. **Umgebung verifizieren.** RFEM-Build, Python-Interpreter, Paketversion, API-Typ und Berechtigung festhalten. Installation, Authentifizierung und Serverstart nach der passenden Herstellerversion durchführen. Schlüssel über den vorgesehenen lokalen Geheimnisspeicher bereitstellen. Erst den Verbindungsaufbau prüfen, anschließend eine ausdrücklich gewählte Modellkopie öffnen.
3. **Vertikalen Durchstich begrenzen.** Ein Bauteil, ein Lastfall, eine definierte Ergebnisstelle. Zunächst Knoten, Stab und Querschnitt auslesen und mit der Oberfläche vergleichen. Erst nach bestätigter Eingabe Modellgenerierung oder Solverlauf auslösen. Für das serielle FT-Skelett danach Material, Stützen, Randträger, Decken und Verbindungen in dieser Abhängigkeit ergänzen.
4. **Ergebnis abnehmen.** Solverstatus und Warnungen sichern. Modellobjekt, Lastfall und Ergebnisstelle erneut lesen. Als Vergleich gilt die signierte Differenz `API-Wert − Referenzwert` in derselben Einheit. Abnahme erfolgt bei erfüllter vorher vereinbarter Toleranz und geklärtem Vorzeichen. Eine erfolgreiche Verbindung belegt ausschließlich den Schnittstellenzugriff.

**Vorlagen direkt beim Hersteller** · [Installation, Authentifizierung und Serverstart](https://apidocs.dlubal.com/getting_started.html) · [Quick Start](https://apidocs.dlubal.com/quick_start.html) · [Ausführbare Anwendungsbeispiele](https://apidocs.dlubal.com/examples.html) · [Bisheriger RFEM Python Client und Examples](https://github.com/dlubal-software/RFEM_Python_Client). Geprüfter Dokumentationsstand des neuen API-Portals am 19.11.2026: Version 2.16.7 vom 16.11.2026. Die lokal installierte Version ist beim jeweiligen Lauf zu ermitteln.

## 4 · Fehler behandeln und nach Unterbrechung fortsetzen

| Beobachtung | Aktion | Bedingung für Fortsetzung |
|---|---|---|
| Treffer im Suchindex, Original fehlt | Datei-ID oder autorisierten Projektpfad auflösen. | Original und Planstand lesbar. |
| CAD-Abmessung weicht um Größenordnungen ab | Quelldimension, Exportmaßstab, Kontrollmaß und Blocktransformation prüfen. | Mindestens zwei unabhängige Kontrollstrecken im vereinbarten Toleranzband. |
| RFEM-Verbindung scheitert | Schnittstellengeneration, Serverzustand, Paketversion und Berechtigung einzeln mit dem zugehörigen Quick Start prüfen. | Lesetest am identifizierten Modell erfolgreich. |
| Zwei Agenten übernehmen dieselbe Arbeit | Ticket erneut lesen, bestehenden Claim prüfen, parallele Ergebnisse als Entwürfe erhalten. | Zuständigkeit geklärt, genau ein Schreiber für das maßgebliche Register. |
| Drive erfolgreich, GitHub fehlgeschlagen | Drive-ID beibehalten. Repository-Pfad und vorhandene Version prüfen, aus bestätigten Drive-Bytes erneut spiegeln. | Lesetest am konkreten Commit liefert dieselben Bytes. |
| Hashabweichung | Version, Zeichencodierung und Zeilenenden vergleichen. Abweichende Fassungen sichern. | Beide geprüften Repräsentationen und die Entscheidung sind dokumentiert. |

## 5 · Veröffentlichung und Wiederherstellung prüfen

Markdown als UTF-8-Datei in den kanonischen WORK-Ordner laden. Name, Parent-ID, MIME-Typ, Dateiversion und Drive-ID übernehmen. Datei als Rohbytes zurücklesen und SHA-256 mit dem lokalen Stand vergleichen. Dieselben Bytes als Review-Snapshot in GitHub sichern. Commit und Pfad notieren, Datei über diese unveränderliche Revision erneut lesen und den Hash vergleichen. Beim Wiederanlauf zuerst anhand der beiden Kennungen prüfen, welche Teiloperation schon erfolgreich war. So lässt sich ein unterbrochener Lauf ohne zweite Drive-Datei fortsetzen. [Google Drive Upload Guide mit Beispielen](https://developers.google.com/workspace/drive/api/guides/manage-uploads) · [GitHub Contents API mit Lese- und Schreibbeispielen](https://docs.github.com/en/rest/repos/contents)

Eine Wiederherstellungsprobe liest die Datei aus dem Commit in ein temporäres Verzeichnis und vergleicht sie mit dem letzten bestätigten Hash. Ein Schreibversuch allein genügt für diese Probe nicht. Die Bindung an das bestehende Register erfolgt über die echte Drive-ID. Ein bestätigter Registereintrag und eine technische Freigabe sind getrennte Entscheidungen.

## 6 · Herkunft und Geltungsbereich

- **Operative Vorgaben.** [Manifest §4](https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view), [Baseline §§4–12](https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view), [WORK-AGBs v007.1 §§4–10](https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view), [WORK Folder.md](https://drive.google.com/file/d/1nDjF78dq3l8PGpXsauzBz1bzHescDSwv/view), [Repository-Einstieg](https://github.com/julianzotter/nexus-platform/blob/main/AGENTS.md).
- **Konzeptquellen aus dem Auftrag.** „ROLLOUT AI-OS-CONTROL-REFINEMENT“, Abschnitte AUTHORITY_MATRIX und OBJECT_PIPELINE. „DXF+IFC-CAD-Datenextraktion“, Aufgaben 3–4 zu den Mylius-Exporten. „RFEM6-API-KEY-CLAUDE-Steuerung“, Abschnitte Integrationsarchitektur und FT-Wohnbaumodul. „RFEM Python Client Repo from Github“, BasicExample. „RFEM 5.29 AnythingSearchResults“ vom 17.11.2026 als Suchverzeichnis.
- **Abnahmestand.** Dieses Handbuch spezifiziert einen Pilotbetrieb. Geometrievergleich, RFEM-Verbindung, Solverresultate, unabhängiger Review und fachliche Freigabe sind am jeweiligen Projekt durchzuführen. Es enthält keine freigegebene Bemessung.
