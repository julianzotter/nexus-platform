---
name: source-governance
description: "Klassifiziert jede Quelle als public, internal, confidential, restricted oder unknown und erzwingt zulässige Verarbeitung, Speicherung und Weitergabe. Fail-closed: unknown gilt als restricted. Verpflichtend vor Ingestion, Cloud, Drittanbieter-Upload, Git-Export und Backup."
version: '0.1.0'
status: PLANNED
timestamp: "2026-10-13"
priority: 1
depends_on: []
replaces:
- license-router
---

# source-governance

## Zweck
Schutzschicht des Gesamtsystems. Jede Quelle erhält vor jeder weiteren Verarbeitung einen maschinenlesbaren Entscheid (`governance-decision.json`), der festlegt, wo sie verarbeitet, gespeichert und weitergegeben werden darf. Alle anderen Skills und alle Connectoren prüfen diesen Entscheid selbst (Defense in Depth).

## Wann verwenden
- Jede neue Eingabedatei (PDF, DOCX, Markdown, später Audio/Scan).
- Vor jedem Zugriff auf ein externes Ziel: Cloud-Worker, Drittanbieter-API (auch LLM-API mit Dokumentinhalt), Git-Export, Backup.
- Vor Registry-Aufnahme oder RAG-Paketierung (erneute Prüfung durch `knowledge-quality-gate`).

## Grundsätze
1. **Fail-closed**: Fehlt eine Information, gilt `unknown`; `unknown` wird als `restricted` behandelt.
2. **Heuristiken stufen nie auf public hoch.** `public` entsteht nur durch eine explizite Allow-Regel (Herausgeber plus Domain) oder einen dokumentierten manuellen Override.
3. **Höchster Schutz gewinnt**: Mehrere Treffer (Regel, Lizenzhinweis) ergeben die höhere Schutzstufe. Reihenfolge: public < internal < confidential < restricted.
4. **Overrides nur durch Menschen**, mit `approved_by` und `reason`, und sie werden im Audit-Log markiert.
5. **Keine Inhalte in Berichten**: Entscheid und Log enthalten Dateiname, Hash, Regel-IDs, keine Textauszüge.

## Inputs
| Input | Pflicht | Beschreibung |
|---|---|---|
| Datei | ja | Quelle (wird nur gehasht, nicht inhaltlich gelesen) |
| `origin` | nein | Herkunft: URL oder Herausgeber (`issuer`, `source_domain` werden daraus abgeleitet) |
| `owner` | nein | Eigentümer/Autor |
| `license_hint` | nein | Lizenzhinweis (`internal`, `confidential`, `restricted`, `cc0`, `cc-by-4.0` ...) |
| `target` | nein | gewünschtes Zielsystem (`local_processing`, `cloud`, `third_party`, `git`, `backup`) |
| `--sidecar` | nein | `<datei>.meta.yaml` mit obigen Feldern |
| `--override-file` | nein | YAML mit `classification`, `approved_by`, `reason` |
| Regeln | ja | `config/license-rules.yaml` |

## Klassen
| Klasse | Bedeutung |
|---|---|
| `public` | frei zugänglich und Weitergabe/Verarbeitung durch Dritte unbedenklich (explizit freigegeben) |
| `internal` | eigene oder nicht vertrauliche Arbeitsdokumente, nicht für Dritte |
| `confidential` | vertraglich oder fachlich vertraulich (z. B. Kundenunterlagen) |
| `restricted` | lizenzpflichtige oder geschützte Volltexte (z. B. DIN, ÖNORM) |
| `unknown` | Eingabewert bei fehlender Information; wirkt wie `restricted` |

## Workflow
1. Datei hashen (SHA-256), Metadaten aus Sidecar und Parametern lesen.
2. Regelauswertung in fester Reihenfolge: Deny-Regeln, Allow-Regeln, Eigentümerregel, Lizenzhinweis, Default `unknown`.
3. Höchste Schutzstufe bestimmen; `unknown` auf `restricted` abbilden (`original_classification` bleibt erhalten).
4. Override anwenden, falls vorhanden und vollständig (`approved_by`, `reason`); sonst Fehler.
5. Policy-Matrix anwenden: erlaubte, bedingte, nur-Metadaten- und verbotene Ziele ableiten.
6. `governance-decision.json` schreiben und Zeile an das Audit-Log anhängen.

## Policy-Matrix (Standard, aus `license-rules.yaml`)
| Klasse | local_processing | cloud | third_party | git | backup |
|---|---|---|---|---|---|
| public | erlaubt | erlaubt | erlaubt | erlaubt | erlaubt |
| internal | erlaubt | bedingt (privater Mandant) | verboten | bedingt (privates Repo, keine fremden Volltexte) | bedingt (verschlüsselt) |
| confidential | erlaubt | verboten | verboten | nur Metadaten | bedingt (verschlüsselt, Offsite, nicht GitHub) |
| restricted (inkl. unknown) | erlaubt | verboten | verboten | nur Metadaten (Struktur, Hash, kurze Zitate mit Seite) | bedingt (verschlüsselt, nicht GitHub) |

Ein externes LLM, das Dokumentinhalt erhält, zählt als `third_party`. Lokale Modelle zählen als `local_processing`.

## Output `governance-decision.json`
```json
{
  "schema_version": "1.0",
  "decision_id": "gd-3f9a1c2e7b4d5a60",
  "source": {"file_name": "OENORM_B_1995-1.pdf", "sha256": "<64 hex>", "origin": null, "owner": null, "license_hint": null},
  "classification": "restricted",
  "original_classification": "unknown",
  "allowed_targets": ["local_processing"],
  "conditional_targets": [{"target": "backup", "condition": "verschlüsselt, lokal oder Offsite, nicht GitHub"}],
  "metadata_only_targets": ["git"],
  "prohibited_actions": ["cloud_processing", "third_party_upload", "git_fulltext"],
  "retention": "gemäß Lizenzbedingungen des Herausgebers",
  "decision_reason": "Kein Lizenzhinweis und keine Allow-Regel: unknown, fail-closed als restricted",
  "rule_ids": ["R-DEFAULT-UNKNOWN"],
  "override": null,
  "decision_hash": "<64 hex>",
  "timestamp": "2026-10-13T12:00:00+02:00"
}
```
Schema: `docs/CONTRACTS.md` (`GovernanceDecision`). `decision_id` leitet sich aus dem `decision_hash` ab (erste 16 Zeichen).

**Audit-Log** `audits/governance_log.jsonl`: eine Zeile je Entscheid mit `prev_hash` und `entry_hash` (SHA-256-Kette). Anhängen ist atomar; vorhandene Zeilen werden nie verändert.

## CLI
```
nexus classify <datei> [--origin URL|Herausgeber] [--owner NAME] [--license-hint HINT]
                       [--sidecar FILE] [--override-file FILE] [--out governance-decision.json]
nexus gate <governance-decision.json> --target <local_processing|cloud|third_party|git|backup>
nexus verify-log [--log audits/governance_log.jsonl]
```
`nexus gate` ist die Prüfung, die Connectoren und andere Skills vor jeder Übertragung aufrufen.

## Exit-Codes
| Code | Bedeutung |
|---|---|
| 0 | Entscheid erzeugt bzw. Ziel erlaubt |
| 10 | Ziel nicht erlaubt (verboten oder nur Metadaten) |
| 11 | Ziel nur bedingt erlaubt (Bedingung manuell bestätigen) |
| 20 | Konfigurations- oder Eingabefehler (z. B. Override ohne `approved_by`) |
| 21 | Log-Kette verletzt (`verify-log`) |

## Hard Gates
- `unknown` wird `restricted`; keine Ausnahme per Heuristik.
- Kein Drittanbieter-Upload ohne Klasse `public` (oder explizit bestätigte Bedingung bei bedingten Zielen).
- Keine geschützten Volltexte in Git (`restricted`/`confidential`: nur Metadaten).
- Ein `GovernanceDecision` mit `restricted` und `third_party` in `allowed_targets` ist ungültig (Schema-Validator).

## Zusammenspiel
- `knowledge-ingestion` verlangt den Entscheid, prüft `source.sha256` gegen die Datei und `local_processing` in den erlaubten Zielen.
- `knowledge-quality-gate` prüft den Entscheid erneut gegen das gewünschte Exportziel (Check Q06).
- Connectoren (Transkription, Human-OCR, Cloud-Worker) rufen `nexus gate` selbst auf.
- CI: `pytest -m governance` ist Pflicht-Check für Merges.

## Tests (MVP-Testfälle)
| # | Fall | Erwartung |
|---|---|---|
| T1 | Öffentliche Publikation (OIB-Richtlinie, `origin=oib.or.at`, `issuer=OIB`) | `public`, alle Ziele erlaubt |
| T2 | DIN/ÖNORM-Volltext (`issuer=Austrian Standards` oder Dateiname `ÖNORM_...`) | `restricted`, nur lokal, Git nur Metadaten |
| T3 | Internes Projektdokument (`owner=ZOTTERCONSULT`, kein Hinweis) | `internal`, `third_party` verboten |
| T4 | Quelle ohne Lizenzhinweis (keine Metadaten) | `unknown` -> `restricted`, wie T2 |
| T5 | Allow-Treffer, aber `license_hint=confidential` | `confidential` (höchster Schutz gewinnt) |
| T6 | Override auf `public` ohne `approved_by` | Exit 20, kein Entscheid |
| T7 | Gate: `restricted` mit `--target third_party` | Exit 10 |
| T8 | Eine Zeile des Logs verändern | `verify-log` Exit 21 |
| T9 | Fuzz: zufällige Metadaten ohne Allow-Regel und ohne Override | nie `third_party` erlaubt |
| T10 | Zwei Läufe mit gleicher Eingabe | identischer `decision_hash` |

## Abnahme
Kein `restricted`- oder `unknown`-Testfall erreicht einen externen Connector oder einen Git-Export. Jede `public`-Entscheidung nennt eine Allow-Regel oder einen Override mit Person und Begründung.

## Offene Punkte (Entscheidung Mensch)
- Deny-/Allow-Listen in `license-rules.yaml` sind Platzhalter und zu prüfen; der Skill trifft keine rechtliche Bewertung.
- Aufbewahrungstexte (`retention`) sind beschreibend und fachlich zu bestätigen.
- Ob `internal` den Cloud-Pfad (privater Mandant) im MVP überhaupt nutzen darf.

## Log
- 2026-10-13: Vollständige Spezifikation erstellt (Status PLANNED).
