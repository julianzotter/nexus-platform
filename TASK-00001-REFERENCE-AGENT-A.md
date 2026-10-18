# TASK-00001: REFERENZ — Agent A / Reference

**Status:** DRAFT (Entwurf, nicht freigegeben; Scope teilweise ungeklärt)
**Owner:** Agent A (Reference) — Person/Kennung **[OFFEN]**
**Reviewer / Gate:** ID-01 (Human Gate)
**depends_on:** TASK-00004

> Dieser Entwurf stützt sich nur auf Repository-Dokumente. Nur `TASK-00004-INVENTORY-AGENT-D.md:156` erwähnt TASK-00001 (blockiert bis Merge durch ID-01). Alles Weitere ist als **[OFFEN]** markiert und nicht erfunden.

## Dependency ID-01-Merge (konkret)

- Gemeint ist laut TASK-00004 (Governance, Abschnitt 3 und Dependencies): der **PR von `feature/TASK-00004-inventory` nach `main`**, geprüft und gemergt durch den Human Gate ID-01. Tooling wurde in PR #2 gemergt; der reale Scan steht aus (Status `TOOLING_MERGED_SCAN_PENDING`).
- **[OFFEN]** Genügt der Tooling-Merge (PR #2) als Startbedingung, oder erst der Merge mit realem Scan (Coverage nicht mehr `INCOMPLETE`)? Entscheidung durch ID-01.
- „ID-01“ bezeichnet die **Rolle Human Gate** (docs/GLOSSARY.md), nicht automatisch eine bestimmte Person.

## Ziel [OFFEN]

Inhaltliches Ziel von Agent A (Reference) ist im Repository nicht spezifiziert. Arbeitshypothese (zu bestätigen): Referenzbestand aus dem Inventar (`registry/`) als `knowledge-item` mit Normbezug aufbauen.

## Umfang / Nicht-Umfang

- Im Umfang (Hypothese): Anlage von Knowledge Items nach `schemas/knowledge-item.schema.json`, Normbezug mit Norm, Ausgabe, nationalem Anhang und Klausel.
- Nicht im Umfang: Berechnung von Ingenieurergebnissen durch LLM; keine Änderungen an Quellrepos; kein automatischer Merge.

## Ein-/Ausgaben

| | Inhalt |
|---|---|
| Input | `registry/file-registry.jsonl`, `registry/coverage-per-source.json` (nur gemessene Werte) |
| Output | `registry/knowledge/*.json` (ein Item je Datei, schema-valide) **[Pfad zu bestätigen]** |

## Abnahmekriterien (messbar)

- [ ] Jedes Item besteht `python tools/validate_knowledge.py` (CI-Schritt).
- [ ] Jedes `norm_clause`-Item hat `norm.standard`, `norm.edition`, `norm.clause`; `national_annex` falls anwendbar.
- [ ] Items mit `engineering_result: true` und Status `VALID` haben `signoff` (Prüfer, Entscheidung `APPROVED`, Zeitpunkt, `result_version` = `version` des Items).
- [ ] Ändert sich `version`, ist das Sign-off ungültig, bis neu freigegeben.
- [ ] Ingenieurergebnisse stammen aus deterministischen Solvern, Quelle als Evidence (`kind`) hinterlegt.
- [ ] Keine Metriken vorbefüllt; Quellen mit `INCOMPLETE` bleiben markiert.
- [ ] PR gegen `main`, Reviewer ID-01, `AWAITING_REVIEW`, kein automatischer Merge.

## Offene Punkte

1. Ziel/Scope von Agent A und Owner-Kennung.
2. Startbedingung (siehe ID-01-Merge oben).
3. **Scanner:** `julianzotter/julianzotter/tools/01_scan_registry.py` liegt nicht in diesem Repo. Anbindung bleibt offen, bis Originalskript bzw. Ergebnisdateien geprüft und der Schnittstellenvertrag (Ausgabefelder laut `schemas/file-record.schema.json`) abgeglichen sind.
4. Ob Sign-off zusätzlich als `human_review`-Evidence geführt wird (Feld `signoff.evidence_id` vorgesehen, optional).
