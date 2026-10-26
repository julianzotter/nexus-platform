---
name: DEC-KG-TECHNIKACHSE
version: 1.0.0
status: ID01_DECISION_RECORDED
timestamp: 2026-10-26T15:45:04+01:00
agent_id: ID03
executor: OpenAI Codex
runtime_instance: /root
owner_id: ID01
ticket_id: WO-20261026-NEXUS-REPAIR-01
content_hash_sha256: 2dd191900da7b1fc2ddea5d5fbca9e8e16780e655be43de4e8fbfb44e6d1f2db
hash_scope: body_utf8
canonical_location: LLM-LOCAL-SSOT/
---

# KG-Achse: dokumentierte ID01-Festlegung

## Entscheidung und Geltungsbereich
Quelle: ausdrückliche Nutzerfestlegung in dieser Voice-Konversation vom 26.10.2026; anschließend Auftrag zur sofortigen Ablage und Registrierung. Kein angeblich wiedergefundenes historisches Achsen-Manifest.
Interne Hauptachse: Wissenschaft / Technik -> Ingenieurwissenschaften -> Bauingenieurwesen -> konstruktiver Ingenieurbau -> Fachanwendung -> Werkstoff (zuerst Beton/Holz) -> Eurocode-Teil -> nationaler Anhang / NAD -> Abschnitt, Tabelle oder Gleichung.
Recht ist ein ergänzender Nebenpfad. OIB-/ÖNORM-Verknüpfungen referenzieren technische Objekte; keine doppelte kanonische Ablage. Externe IFC/bSDD/ISO-Mappings sind eigenständige referenzierende Projektionen.

## Zustände und Abgrenzung
Diese Datei dokumentiert die jetzt ausdrücklich bestätigte Architekturentscheidung. Sie erteilt weder Parser-Produktionsfreigabe noch fachliche Freigabe extrahierter Norminhalte. Ob damit die historische Voice-Notiz vollständig wiedergegeben ist, bleibt getrennt; die aktuelle Festlegung ist direkt belegt.
White Paper v0.1 bleibt REVIEW: https://drive.google.com/file/d/1AhSCkG73Dnu7CArWRyrgPC9DVFBd2_it/view
Insbesondere kein automatisches BINDING=true allein aus OIB-/Norm-Tags; Rechtsgeltung und Anwendungsstand bleiben gesondert nachzuweisen. Dies ist eine Nachweisanforderung, kein Rechtsgutachten.

## Quellengebundene Daten-Pipeline
1. Rohdatei unverändert sichern; source_id/object_id, Herkunft, Darstellung, Version und vollständigen Datei-SHA256 erfassen.
2. Bestehendes Ressourcenregister aktualisieren, bevor semantische Bearbeitung beginnt. Ledger-ID ist Artefaktidentität, keine Absatz-ID.
3. Deterministische Extraktion: PDF/native Text/OCR -> gemeinsames Seiten-/Blockmodell; Original und Derivate getrennt.
4. Quellengebundene Kandidaten mit source_id und Seiten-/Block-/Zeichen-Locator erzeugen. Struktursegmentierung; semantische Grenzen nur mit dokumentiertem Modell/Parametern.
5. tech_path verpflichtend zuordnen; law_path optional. Unbekannte Labels UNCLASSIFIED/REVIEW_REQUIRED, keine erfundenen Normausgaben.
6. Schema-, Hash-, Quellen- und Inhaltsprüfung; unabhängige Prüfung und Human Gate von bloßer Verarbeitung unterscheiden.
7. Verifizierte Registry -> Graphprojektion und optional Vektorindex mit gleicher Quellenidentität. Exaktes Register-/Index-Retrieval vor Vektorfallback.
8. Engineering-Reuse liefert Quellen/Locator oder enthält sich; Rechnen erfolgt nur durch geprüften deterministischen Solver.

## Ist-Stand
Parser rc2 vorhanden und getestet, jedoch neue Integritätsbefunde in Bearbeitung. Keine produktive Graph-/Vektor-Integration oder fachliche Normabnahme durch diese Datei behauptet.
Grundlage: CURRENT Baseline MUST-20/21/30–34/70–76/150–159, https://docs.google.com/document/d/1Ig0YFqbWji6B5-oOFcxuVpHb5GEBk0HlbJVz51rf9ho/edit

## Ergänzende ID01-Festlegung: Sprache und Kommunikation
- Deutsch ist die verbindliche interne Fach- und Kommunikationssprache. Englische Benennungen sind sekundäre Mappings auf dieselbe stabile Begriffs-ID, keine zweite Taxonomie. Originalquellen behalten ihre Originalsprache; Übersetzungen als eigene Repräsentation markieren.
- Technische API-/Schemafeldnamen werden nicht allein wegen der Sprachregel umbenannt. Fachlabels bevorzugt Deutsch, englische Gegenstücke als mapping_en/aliases_en.
- Entwicklungsmodus: zentraler WORK-Prüfzyklus mit Zielintervall 60 Sekunden. Das ist eine Betriebsanforderung, kein Nachweis laufender Agenten. Voraussetzung: Credentials, laufender Watcher, erreichbare Ausführungsinstanzen, persistente Cursor/Claims und Fehlerstatus.
- Zeitformat: Europe/Vienna mit ISO-8601-Offset in Metadaten; Dateiprefix YY_MM_DD_HH_mm_ID-XX. Event-/Run-ID trennt gleichzeitige Ereignisse; eine Rolle ist keine Runtime-ID.
- Maßgeblicher Abgleich: CURRENT Manifest §§6–10 und Baseline MUST-20/21/30–34/40–55/70–76/90–96/150–159. Kein neuer autonomer Vollbetrieb aus einer Regel abgeleitet.
