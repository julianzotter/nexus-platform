---
name: speed-team
description: SPEED (Super Priority Emergency Execution Deployment) - Multi-Agenten-Team für extrem dringende Aufgaben. Verwenden, sobald der User "#R", "SPEED" oder "speed-team" schreibt oder einen akuten Bedarf mit Zeitdruck meldet (z.B. "brauche sofort SIGEPLAN Eisteiche P205", "Seilstatik BOEB dringend"). Formiert Rollen, sucht verstreute Projektdaten (Google Drive Keyword-Suche, AnythingSearch-DB, Colab Pre-Parsing), erhebt den IST-Stand, grillt den besten Arbeitsplan mit GRILLME.md und arbeitet ihn mit Protokoll ab.
---

# SPEED-TEAM

Multi-Agenten-Team für akute Aufgaben: minimale Koordination, reduzierter Tokeneinsatz, gemeinsamer Plan, schnelle Suche, dann Abarbeitung.

## Trigger

- `#R: <was akut gebraucht wird>`
- `SPEED` / `speed-team` im Chat

## Ablageort

- Gemeinsamer Ordner (immer): `_developement\SKILLS\speed-team`
  https://drive.google.com/drive/folders/1Q9sDmVO2GdZu9ySBXxt4eXD7L2oxzUb7
- Gesamte Kommunikation barrierefrei über MD-Files
- Dateiname: `<Timestamp inkl. Minuten>_<ID>_<Name>_<Topic>.md`
- Je SPEED-Aktion ein PRJ-Ordner: `<LAUF-Nr>_<Kurzname>/`

```
speed-team/
├── SKILL.md                  # dieses Playbook
├── GRILLME.md                # Template Arbeitsplan grillen
├── _COMMS/
│   └── feedback_SPEED.jsonl  # WORM, Hash-Chain, getrennt von feedback.jsonl
└── <LAUF-Nr>_<Kurzname>/     # je SPEED-Aktion
    ├── SPEED.md              # PLAN (gemeinsam erstellt)
    ├── INDEXLISTE.md
    ├── STATUSBERICHT.md
    ├── WORKORDERS/
    ├── EINGABE/
    └── AUSGABE/
```

## Rollen

| ID | Rolle | Aufgabe |
|---|---|---|
| ID-01 | COORD | Orchestrierung, Ordner anlegen, verteilen, GRILLME |
| ID-04 | RAG | Keyword-Suche Drive + AnythingSearch-DB |
| ID-05 | RETRIEVAL | Pre-Parsing (.gdoc .txt .md .pdf .docx .rf5 .dxf), Sanitizer NFKC + U+00A0/U+202F |
| ID-06 | HARDENING | INDEXLISTE + STATUSBERICHT konsolidieren, Duplikate `...(1).md` markieren |
| ID-07+ | Spezialist | Fachinhalt je Fall (z.B. SIGE, SEIL) |

## Ablauf

1. **#R parsen**: was wird akut gebraucht, welche Projekte, welche Frist
2. **PLAN**: `SPEED.md` im PRJ-Ordner gemeinsam festlegen (Ziel, Stichworte, Rollen)
3. **SUCHE**: Drive-Keyword-Suche, AnythingSearch-DB, Colab glob/Pre-Parsing mit den Stichworten
4. **PRE-PARSING**: Treffer durch `sanitize()` + Hash + Typ PRIMARY / DERIVED / OBSOLETE
5. **STATUS ERHEBEN**: Statusberichte, Indexlisten, WorkOrders (auch SSOT) zu konsolidiertem IST-Stand in `INDEXLISTE.md` + `STATUSBERICHT.md`
6. **GRILLEN**: besten Arbeitsplan mit `GRILLME.md` (M1..Mn, Owner, DoD, Blocker, Quelle)
7. **ABARBEITEN**: sequenziell, Logging nach `_COMMS/feedback_SPEED.jsonl`
8. **ABNAHME**: eta, delta, PASS/FAIL

## Regeln

- Non-destruktiv: nie überschreiben, nur `if not exists: write`
- Nie löschen: Duplikate nur markieren, Aufräumen nur per Verschieben
- Eigener Log-Kanal, keine Vermischung mit `WORK/_COMMS/feedback.jsonl`
- Reuse vor Neuentwicklung: zuerst Bestand suchen, dann bauen

## Aktuelle Fälle (Stand 2026-10-05)

| Fall | Projekt | Stichworte |
|---|---|---|
| SIGEPLAN (19.6. rückdatiert) Schule Eisteiche | P205 | EISTEICHE, P205, SIGEPLAN, SIGE, SCHULE, BAUSTELLV, GEFAEHRDUNG |
| SEILSTATIK BOEB (Böblingen/RFEM/Neugeometrie) | 26_001 | SEILSTATIK, BOEB, BOEBLINGEN, RFEM, GEOMETRIE, PFEIFER, Sxx, Lo2k, 01-Gesamtmodell |

Priorisierung: SIGEPLAN (rechtlich) vor SEILSTATIK (technisch).

## Referenzen

- `GRILLME.md`: Template für den Arbeitsplan
- `references/setup_colab.py`: legt Ordnerstruktur non-destruktiv an
- `references/scratch-nexus-roadmap.md`: Hintergrund (NEXUS-Roadmap, Such-Pipeline, deterministischer Router), nur bei Bedarf lesen
