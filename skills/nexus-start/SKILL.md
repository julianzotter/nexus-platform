---
name: nexus-start
description: Session-Einstieg für Julian - bei "/nexus-start", "start", "Einstieg" oder "was steht an" einen rotierenden Tipp, den Stand der geplanten Aufgaben und ein Kurzmenü ausgeben.
version: 0.1.0
owner: Julian Zotter
status: ENTWURF
timestamp: 2026-11-10T15:35:00+01:00
---

# nexus-start

Zweck: kompakter Einstieg in eine Sitzung (Web oder Desktop-App). Ausgabe max. 12 Zeilen, Stichworte, keine Floskeln.

## Ablauf
1. Datum holen. Tipp-Index = Tag des Jahres mod Anzahl Tipps (deterministisch, täglich wechselnd). Bei "anderer Tipp" Index +1.
2. Geplante Aufgaben listen (falls Werkzeug vorhanden): Name, nächster Lauf, letzter Status. Nur Auffälligkeiten nennen (fehlgeschlagen, deaktiviert, doppelt).
3. Kurzmenü ausgeben.
4. Nichts schreiben, nichts löschen, keine E-Mails. Reiner Lesemodus.

## Ausgabeformat
```
TIPP #<n>: <Kurzname> --> <Anleitung in 3-5 Stichworten>
TASKS: <n aktiv> | Auffällig: <Liste oder "keine">
MENÜ: 1 Ordnung (workspace-housekeeping) | 2 Einstellungen (nexus-settings-kit) | 3 SPEED (#R) | 4 Morning Brief
LOG: kein Protokoll (Lesemodus)
```

## Tipp-Liste (rotierend)
1. Ein Thema = ein Projekt --> Projektanweisung + Wissen dort, nicht im Chat
2. Chat-Titel nach Schema --> `<PROJEKT>_<THEMA>_<JJMMTT>`
3. Globale Regeln --> Einstellungen > Anweisungen, kurz halten
4. Wiederkehrender Ablauf --> Skill bauen statt Prompt kopieren
5. Geplante Aufgabe --> Prompt muss eigenständig sein, frische Sitzung ohne Vorwissen
6. Ein Run = ein Hauptziel --> Zusatzaufgaben eigener Run
7. Vor Neubau --> Bestand prüfen (WORK, _INDEX_LNK, Colab-Register)
8. Status ohne Anker --> "nicht beurteilbar - nicht dokumentiert"
9. Definition of Done --> Artefakt + Report-Log + Statusbericht
10. Drive --> nie löschen, nur verschieben/verlinken
11. Kontext wird knapp --> Checkpoint als Markdown, neuer Run
12. Übergabe an Agenten --> erst erledigt nach bestätigtem Empfang

## Pflege
Neue Tipps nur anhängen, Nummern nicht umsortieren.
