---
title: "NEXUS - Reparaturplan, Status, nächste Schritte"
version: 1.0.0
date: 2026-10-26
author_role: ID-03
status: REVIEW_SNAPSHOT
source_of_truth: DRIVE_WORK
---

# NEXUS - Reparaturplan, Status, nächste Schritte

Stand 26.10.2026 | v1.0.0 | Plan / Review-Snapshot, keine Betriebsfreigabe

**TL;DR: Vorhandene Übergänge schließen und einen Auftrag vollständig durchlaufen lassen.**

## Präzisierte Fassung / Status

- Vorhanden: ID-Rollen, Governance, WORK-Ablage, nexus-platform, Softwarebausteine und Zeitpläne. Zuverlässiger autonomer Gesamtbetrieb noch nicht nachgewiesen.
- Drei getrennte Abnahmen: Auftragsbetrieb zuerst, danach Dokumentensuche und Engineering-Berechnungen. Neue Frameworks, Datenbanken und Ablagewechsel bleiben Vorschläge.

## Die eigentliche Ursache: unterbrochene Übergänge

- Abgelegt ist nicht erkannt, übernommen, geprüft oder abgeschlossen. Ein grüner Zeitplan beweist keinen erfolgreichen Auftrag.
- Rollenbeschreibung ist kein erreichbarer Agent; Chat-Zusage ist kein gespeichertes Ergebnis. Offen bleiben Übergaben, Readback, ACK und Wiederanlauf.

## Priorität 1: Transport und Zugriffsschutz reparieren

- A. Falsches Grün beseitigen: Fehlende Zugangsdaten und Übergabefehler als BLOCKIERT/FEHLER melden. ERLEDIGT erst nach Prüfung und Readback.
- B. Initialbestand und Änderungen gemeinsam behandeln: Vorhandene Aufträge erfassen, Änderungen nachführen, nach Ausfällen nachholen; Doppelbearbeitung verhindern.
- C. WORK-Berechtigungen kontrolliert härten: Früher festgestellten öffentlichen Schreibzugriff erneut prüfen; legitime Zugänge sichern, überbreite Rechte autorisiert begrenzen und testen.

## Priorität 2: Einen kleinen Betriebsvertrag durchsetzen

- Pflichtfelder: Auftrags-ID, Version, Auftraggeber, zuständige Rolle, Eingaben, Ergebnis und Abnahmekriterien. Eine aktive Zuständigkeit je Auftrag.
- Zustände: NEU > ÜBERNOMMEN > IN ARBEIT > PRÜFUNG > ERLEDIGT; zusätzlich BLOCKIERT/FEHLER. Gültige Freigabe geht vor neuerem Entwurf.
- Routineaktionen innerhalb festgelegter Rechte; Human Gate für definierte Freigaben. Grenzen für Kosten, Laufzeit, Wiederholungen und Folgeaufträge.

## Priorität 3: Einen vorhandenen Auftrag vollständig abschließen

- Ungefährlichen Auftrag wählen: WORK > Erkennung > Übernahme > Bearbeitung > Prüfung > Ergebnisablage > Readback > ACK > Abschluss; durchgehend dieselbe ID.
- Doppelzustellung, Agentenausfall und Schreibfehler testen. Erfolg: nachvollziehbares Ergebnis, keine doppelte Ausführung, funktionierender Wiederanlauf.

## Dauerbetrieb: bestehende Komponenten gezielt verbinden

- Zentraler Dispatcher prüft WORK und verteilt an verfügbare Agenten. Bestehenden Prüfzyklus reparieren, erst danach bei Bedarf häufiger prüfen.
- Drive: Austausch/Artefakte; Registry: Auftragszustand; GitHub: Code, Tests, Versionen und Reviews. Gemini arbeitet über Drive; berechtigte Rolle übernimmt GitHub.
- Logs fortschreiben, Synchronisierung überwachen, Backup und Wiederherstellung testen. Meldungen bei Abschluss, Fehler oder Entscheidungsbedarf.

## Konkrete nächste Arbeitspakete

- 1 Transport reparieren  |  2 Zugriffe prüfen  |  3 Betriebsvertrag fixieren
- 4 Einen Auftrag abschließen  |  5 Störungen/Wiederherstellung testen  |  6 Such- und Berechnungspilot separat abnehmen.

Grundlage: vorangegangene Statusanalyse; Perplexity-Bericht und Claude-Chatprotokolle (DOCX vom 26.10.2026). Keine erneute Live-Prüfung durch diese Zusammenfassung.
