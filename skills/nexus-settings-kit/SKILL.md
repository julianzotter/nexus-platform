---
name: nexus-settings-kit
description: Julians NEXUS-Steuerdateien (SOUL, _AGBS, _FRONTMATTER) auf die KI-Einstellungen abbilden - Anweisungstext, Projektanweisungen und Skills daraus ableiten. Bei "Einstellungen konfigurieren", "SOUL", "AGBs".
version: 0.1.0
owner: Julian Zotter
status: ENTWURF
timestamp: 2026-11-10T15:35:00+01:00
---

# nexus-settings-kit

Zweck: aus den bestehenden NEXUS-Steuerdateien die Konfiguration des Assistenten ableiten. Quelle bleibt die SSOT im Drive; die Einstellungen sind eine abgeleitete Kurzfassung.

## Grundsatz
- Reuse vor Neubau: zuerst bestehende Steuerdateien in LLM-LOCAL-SSOT und WORK lesen (AGBS, Manifest, Baseline, WO-NEXUS-BOOTSTRAP-PERSONAL-SETTINGS). Keine neue Steuerdatei anlegen, wenn eine besteht.
- Steuerdateien: Name beginnt mit `_`, kein Timestamp im Namen, Version nur im Frontmatter.
- Freigabe nur durch ID01. Entwürfe tragen `status: ENTWURF`.

## Abbildung
| NEXUS-Datei | Inhalt | Ziel |
|---|---|---|
| SOUL.md | Rolle, Haltung, Stil, Prioritäts-Axiom | Globale Anweisungen (Kurzfassung, max. ca. 1500 Zeichen) |
| _AGBS.md | verbindliche Regeln (kein Löschen, keine E-Mails, Archiv-/Reportpflicht) | Globale Anweisungen (3-5 Kernregeln) + Verweis auf SSOT |
| _FRONTMATTER | Kopf-Schema für Artefakte | Skill-Inhalt / Vorlage, nicht globale Anweisung |
| Projektregeln | Fachkontext (EC2, EC5, HBV, Projekt-Nr.) | Projektanweisung im jeweiligen Projekt |
| Abläufe | wiederholbare Workflows | eigener Skill |

## Ablauf
1. Quellen lesen, je Datei Drive-ID + Version notieren. Fehlt eine Datei: "nicht belegt" melden, nicht erfinden.
2. Widersprüche zwischen Dateien listen, nicht selbst auflösen.
3. Entwurf "Globale Anweisungen" schreiben: nur Regeln, die in jedem Chat gelten. Fachregeln gehören in Projekte.
4. Entwurf je Projektanweisung nur für die genannten Projekte.
5. Ausgabe als Kopiertext. Eintragen in die Einstellungen erst nach GO von ID01.

## Nicht aufnehmen
Anweisungen, die Widerspruch, Prüfung oder Warnhinweise unterdrücken; Zugangsdaten; Kontonummern.

## Frontmatter-Vorlage
```
---
name: <slug>
description: <1 Zeile>
version: <X.Y.Z>
status: ENTWURF | GEPRUEFT | FREIGEGEBEN
timestamp: <ISO 8601>
---
```

## Ausgabe
```
QUELLEN: <Datei | Drive-ID | Version>
WIDERSPRÜCHE: <Liste oder "keine">
ENTWURF: <Kopiertext>
LOG: <Ablageort oder "kein Protokoll">
```
