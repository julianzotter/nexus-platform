---
project: P205 / FT-Träger
created_vienna: 2026-11-23T13:20:50+01:00
issuer_role: ID02
status: PENDING_AGENT_ACK
engineering_release: false
---
# P205 FT-Träger · atomische Multiagent-Arbeitsaufträge

Gemeinsames Evidence Pack: [WORK-Manifest](https://drive.google.com/file/d/1kYIlVQCckGoK496FJN3MBhLtM3JbTjKm/view) · [Peer Review v1.2](https://drive.google.com/file/d/1P-1GjkltbLJ0dB8_Jy7Y_H3dy2NssSxY/view) · [True-Run-Workflow](https://drive.google.com/file/d/12wWMpiKjCLHraSYxlp7j74rfuNwOiBIN/view) · [Draft-PR #116](https://github.com/julianzotter/nexus-platform/pull/116)

Jede Runtime liest vor dem Start `_AGBS.md`, Baseline, Manifest, Ticket-/Rollenregister und bestätigt ihren tatsächlichen Actor, Modell/Runtime, Run-ID, Eingabehashes und Outbox-Pfad. Kein Agent schreibt in den Pfad eines anderen. Kein LLM erzeugt nachweisrelevante Rechenwerte.

## ID03 · unabhängiger Peer Review

- Startbedingung: ID06 liefert vollständigen Excel-E2E-Output mit Hash und Readback.
- Auftrag: prüfe Eingabeidentität, Rechenprotokoll, Fehlerliste, >105-%-Inventar, Geometrie-/RFEM-Zuordnung und Abweichungen zu v1.2 ohne Einsicht in ID07 vor eigener Abgabe.
- Output: `YY_MM_DD_HHMMSS_ID03_P205_FT-INDEPENDENT-REVIEW_RUN-R09_v001.{json,md}`.
- Gate: keine Freigabe; Findings `VERIFIED|CALCULATED|UNVERIFIED`, Quellenlocator und Exit-Kriterium je Finding.
- Status: `PENDING_ACK`.

## ID04 · Quelle, Plan und RFEM-Zuordnung

- Sofortauftrag: benenne bindende Planrevisionen/Positionslisten oder melde `BLOCKED_ID01`; ordne `1OG-J`/`2OG-J` je Station 36,45/37,80/39,15/40,50 m zu Modellrevision, Stab-ID, lokaler x-Stelle, EK/Kombination, lokalen Achsen, Einheit und Vorzeichen zu.
- Geometrie: EG-F abschnittsweise; 2OG-3!BC Eigenbezug und BC/BD-Querbezüge mit Originalplan belegen.
- Output: `..._ID04_P205_FT-SOURCE-GEOMETRY-RFEM-MAP_RUN-R03-R04_v001.{json,md}`.
- Stop: kein eindeutiger Originalbeleg oder keine Stab-/x-Abbildung.
- Status: `PENDING_ACK`.

## ID05 · Primärquellenrecherche

- Start nur mit atomischer Norm-/Herstellerfrage aus R05; keine allgemeine Webrecherche.
- Output: Quelle, Ausgabe/Datum, Geltungsbereich, Seiten-/Abschnittslocator und wörtlich minimales Belegfragment; keine Bemessung.
- Status: `WAITING_FOR_TICKET`.

## ID06 · Windows Excel Desktop E2E

- Sofortauftrag: vollständige v1.2-PS1 als Datei ausführen, nicht blockweise einfügen. Quelle ausschließlich über exakt einen SHA-Treffer wählen; Baseline `a921f5…10f9` oder RevF `c47a1b…33ee` ausdrücklich festlegen und getrennte Ausgaben erzeugen.
- Pflicht: Excel-Build/Locale/Add-ins/Links/UDFs/Queries protokollieren; FullRebuild; SaveCopyAs; Close; Reopen-manual; Formel-/Fehleraudit; unabhängiger OOXML-Formel-/Cache-Readback; Quellhash unverändert.
- Output: `..._ID06_P205_FT-EXCEL-NATIVE-RECALC_RUN-R02_v001/` mit JSON, CSV, XLSX-Arbeitskopie und Maschinenlog.
- Status: `BLOCKED_LOCAL_EXECUTION` bis tatsächlicher Windows-Lauf startet.

## ID07 · Red-Team-Audit

- Startbedingung: gefrorener ID06-Output und Eingabehash liegen vor.
- Auftrag: prüfe Hashkette, Cachepersistenz, Formel-/Wertwidersprüche, versteckte Alternativzweige, 106-Blatt-/239.689-Formel-Invarianten sowie Vollständigkeit aller Nachweisgruppen. Diese Invarianten sind kein EC2-Nachweis.
- Output: `..._ID07_P205_FT-RED-TEAM-AUDIT_RUN-R09_v001.{json,md}`.
- Status: `PENDING_ID06`.

## ID08 · lokale Inventur

- Sofortauftrag: read-only Directory-Listing mit Größe, mtime und SHA-256 für den FT-Arbeitsordner und relevante RFEM-/Planquellen; Online-only-Dateien und Dubletten separat kennzeichnen. Keine Datei verschieben/umbenennen.
- Output: `..._ID08_P205_FT-LOCAL-INVENTORY_RUN-R01_v001.{csv,json}`.
- Status: `PENDING_ACK`.

## Nicht registrierte Modelle

Kimi, Qwen, Gemma, Meta AI und weitere bleiben `UNASSIGNED`. ID01/ID02 müssen zuerst Rolle, atomisches Ticket, zulässige Quellen, isolierten Outbox-Pfad, Review und Human Gate registrieren.

## Eskalationen an ID01

1. Bindende Planrevision und Positionsliste bestimmen.
2. L1–L4-Layouts je betroffenem Abschnitt entscheiden, nachdem R02–R05 belegt sind.
3. Technische Schlussfreigabe ausschließlich nach R09; aktuell `STOP`.
