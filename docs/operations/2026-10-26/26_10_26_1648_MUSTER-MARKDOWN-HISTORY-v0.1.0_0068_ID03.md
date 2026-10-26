---
name: MUSTER-MARKDOWN-HISTORY
version: 0.1.0
status: REVIEW
timestamp: '2026-10-26T16:48:23+01:00'
agent_id: ID03
executor_instance: /root
executor: OpenAI Codex
owner_id: ID01
ticket_id: WO-20261026-NEXUS-REPAIR-01
run_id: DOCSYNC-20261026T164823+0100
artifact_id: 0068
gate: PENDING (Human Gate ID01)
development_status: PROPOSED
evidence_status: SOURCE_BACKED_DOCUMENT
canonical_source: Google Drive / LLM-LOCAL-SSOT
source_scope: sichtbarer Chat und explizit gelesene Quellen; keine vollständige Rückerfassung
  aller Accounts
source_refs:
- https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view
- https://docs.google.com/document/d/1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg/edit
- https://docs.google.com/document/d/1Ig0YFqbWji6B5-oOFcxuVpHb5GEBk0HlbJVz51rf9ho/edit
- https://drive.google.com/file/d/1y7jmHlyxq7Ja2xA2FM6MJapOjIkIMlqZ/view
- https://drive.google.com/file/d/1KeHVM_VC9nGHZTVyJd_5vBE6xBCG9KwX/view
hash_scope: body_utf8_after_closing_frontmatter_lf
content_hash_sha256: 6b0fb475a6e80c31e14c9c3804fc78e51b51887b828bd97fd8b100ac6c45877a
hash: 6b0fb475a6e80c31e14c9c3804fc78e51b51887b828bd97fd8b100ac6c45877a
---
# Markdown-Dokumentmuster — Feldvertrag und Prüfroutine

Status PROPOSED; Konkretisierung von AIM-0009, kein global installierter Validator. Schemaänderungen am Kanon sind nicht aus dieser Vorlage abzuleiten.

## Feldgruppen
| Gruppe | Felder | Regel |
|---|---|---|
| Identität | name, artifact_id, version, canonical_source | Registry vor Semantik; Name ist keine eindeutige Quellenidentität |
| Ausführung | timestamp, timezone, agent_id, executor_instance, provider/model_id | tatsächliche bekannte Werte, sonst UNKNOWN/null |
| Bezug | ticket_id, run_id, source_refs, supersedes | Vorgängerversion und ggf. Snapshot-ID/Hash, nicht nur Live-ID |
| Status | status, development_status, task_status, evidence_status, gate | getrennte Achsen, keine automatische Promotion |
| Integrität | hash_scope, content_hash_sha256, externes Fullfilemanifest | kein Selbsthash der Gesamtdatei |

## Inhalt in Reihenfolge
Zweck/Scope → Quellenstand → Fakten/Annahmen/Vorschläge → Entscheidung/Änderung → Artefakte/Prüfungen → Risiken/Blocker → nächste Aktion → Historie. Keine erfundenen Uhrzeiten und keine unaufgelösten Quellenplatzhalter.

## Praktische Prüfroutine
1 Frisch lesen und bisherige Bytes einfrieren. 2 YAML und Quellenauflösung prüfen. 3 Änderung gegen konkrete Vorgängerversion vergleichen. 4 Originalgedanken/IDs erhalten und neue Aussagen markieren. 5 Bodyhash berechnen. 6 Datei speichern und vollständige Bytes zurücklesen. 7 externen SHA-256 vergleichen. 8 Ledger/Wegweiser/Ticket aktualisieren. 9 GitHub-Snapshot mit gleicher Byteidentität bereitstellen. 10 tatsächliche Kenntnisnahme/Freigabe gesondert protokollieren.
Frischlesevergleich ist kein atomarer CAS. Bei unbekannter konkurrierender Änderung abbrechen und Konflikt melden. Unabhängige Rückläufe getrennt, zentrale Konsolidierung durch eine zuständige Instanz.

## Abnahmestatus
Die Dokumente dieser Lieferung benutzen das Muster und prüfen YAML/Hash/Quellenzeilen. Allgemeiner Validator, globaler Rollout, Nutzerinstallation und unabhängige Abnahme bleiben offen. AIM-0009 wird durch diese Teilumsetzung nicht automatisch auf Status3 gesetzt.

## Quellenverzeichnis
- agbs: https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view
- fm: https://drive.google.com/file/d/1rKnQMZbhO6ii0ThnJLhUCRYrXFcDvRbi/view
- manifest: https://docs.google.com/document/d/1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg/edit
- baseline: https://docs.google.com/document/d/1Ig0YFqbWji6B5-oOFcxuVpHb5GEBk0HlbJVz51rf9ho/edit
- aim: https://drive.google.com/file/d/1y7jmHlyxq7Ja2xA2FM6MJapOjIkIMlqZ/view
- wo: https://drive.google.com/file/d/1KeHVM_VC9nGHZTVyJd_5vBE6xBCG9KwX/view
- audit: https://drive.google.com/file/d/1wN8kOZ_Qe5QZFvQzEc7SUCI1EJi2Zyi2/view
- whitepaper: https://drive.google.com/file/d/16apTjdDsVy-cEK_A6552FJVgnZv8DHnQ/view
- linklist: https://drive.google.com/file/d/135k1DB7KIC9xMaoFBBBEHl6GuObsd2OH/view
- eval: https://drive.google.com/file/d/1PN9FKKPtujQMfTMFZTh4GsX-sSGHV8TR/view
- ledger: https://drive.google.com/file/d/1Uvb89wWOpte3iXWKm3qrg42dEwBb7nuG/view
- manualold: https://docs.google.com/document/d/1OCkf0HslAhXIMmsKzu2zdBr2VyYc3Juxi6ILE1lLJg0/edit
- entry: https://drive.google.com/file/d/1u1lqlQ0zn2HcauvEPc63mk8Kvu3sNC74/view
