---
name: workspace-housekeeping
description: Ordnung im KI-Arbeitsbereich - Chats, Projekte und geplante Aufgaben inventarisieren, Duplikate und Altlasten melden, Benennung vorschlagen. Bei "aufräumen", "Ordnung", "Inventar Chats/Projekte/Tasks".
version: 0.1.0
owner: Julian Zotter
status: ENTWURF
timestamp: 2026-11-10T15:35:00+01:00
---

# workspace-housekeeping

Zweck: Inventar + Aufräumvorschlag. Der Skill ändert nichts ohne ausdrückliches GO je Maßnahme.

## Harte Regeln
- Nichts löschen. Nur Vorschläge: umbenennen, in Projekt verschieben, pausieren.
- Keine E-Mails senden.
- Nur belegte Aussagen. Was nicht gelistet werden konnte: "nicht geprüft".
- Ein Run = ein Bereich (A, B oder C). Bei "alles": mit C beginnen, Rest als Folgeruns nennen.

## Bereiche
### A Chats
1. Letzte Chats listen (max. 5 Seiten à 20). Bei Abbruch: "Inventar unvollständig".
2. Je Chat: Titel, Datum, vermutetes Projekt (nur aus Titel, als Vermutung kennzeichnen).
3. Melden: Chats ohne Projekt, Titel ohne Aussage, Dubletten nach Thema.
4. Benennungsvorschlag: `<PROJEKT>_<THEMA>_<JJMMTT>`.

### B Projekte
1. Projektliste vom User übernehmen oder aus dem Kontext lesen.
2. Clustern: Statik-Projekte | Normen/Wissen | NEXUS/AI | Büro/Finanzen | Sonstiges.
3. Melden: thematische Überschneidungen, Projekte ohne Anweisung (nur wenn prüfbar).
4. Vorschlag: Zusammenlegen oder Präfix (`P_`, `KB_`, `NEXUS_`, `OFFICE_`).

### C Geplante Aufgaben
1. Alle Aufgaben listen: Name, Zeitplan (mit Zeitzone), Modell, letzter Lauf, Status.
2. Prüfen: inhaltliche Überschneidung, Zeitplan ohne Zeitzone (läuft in UTC), mehr Konnektoren als der Prompt braucht, Rollen-ID gegen Rollenregister.
3. Je Befund: `#P<n> --> Kurzname --> Maßnahme`.

## Ausgabe
```
STAND: <Quelle + Zeitstempel> | geprüft: <Bereich> | nicht geprüft: <Rest>
BEFUNDE: #P1 --> ... (max. 10)
MASSNAHMEN: nummeriert, jede einzeln freizugeben
LOG: <Ablageort oder "kein Protokoll">
```

## Archivierung
Auf GO: Inventar als Markdown mit Frontmatter (name, description, version, status, timestamp) im WORK-Ordner ablegen, Dateiname nach gültigem Schema, ID aus dem Ledger.
