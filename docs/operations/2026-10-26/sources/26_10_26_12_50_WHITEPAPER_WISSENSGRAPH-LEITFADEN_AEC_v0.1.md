---
name: WHITEPAPER_WISSENSGRAPH-LEITFADEN_AEC
version: v0.1
status: ENTWURF
timestamp: 2026-10-26T12:50:00+01:00
agent_id: ID-05
hash: LEDGER-REF provisorisch (SHA-256 der gespeicherten Datei wird im Ledger geführt)
gate: PENDING (Human Gate ID-01)
---

# Wissensgraph-Leitfaden AEC: konstruktiver Ingenieurbau (White Paper v0.1)

**Status:** ENTWURF / PROPOSED. Kein CURRENT-Artefakt (Baseline MUST-133).
**Herkunft der Achsenordnung:** Vorgabe von ID-01 im Chat vom 2026-10-26 (Hauptachse intern technisch, Nebenpfad Recht). Diese Ordnung steht nicht im CURRENT-Manifest, in der Baseline, im Manifest-Delta, in WO-20260929-03 und im Masterplan vom 2026-09-28 (durchsucht). Sie ist hier erstmals schriftlich gefasst und braucht eine datierte Adoption durch ID-01 (Baseline MUST-130, MUST-131).

## 1. Zweck und Abgrenzung

- Leitfaden für den Aufbau eines Wissensgraphen im konstruktiven Ingenieurbau mit zwei Pfaden: technische Hauptachse, rechtlicher Nebenpfad.
- Der Graph verweist auf Quellen. Er ersetzt weder Normtext (Lizenz) noch Bemessung (Berechnung nur durch Python/Solver, Baseline MUST-155).
- Bindende Vorgaben aus dem CURRENT-Stand: Quellenpflicht (MUST-60 bis MUST-68), Ablauf Source → Identity → Registry → Extraktion → Objekt → Anreicherung → Graph (MUST-70, MUST-153), Pilotabnahme (MUST-155), Objekt- und Relationsvertrag sowie Kantenvokabular (Manifest-Delta 2026-09-28).

## 2. Domänenachsen (Vorschlag)

### Hauptachse: intern technisch

| Ebene | Inhalt | Knotenart (Vorschlag) | Beispiel für die Einordnung |
|---|---|---|---|
| H0 | Wissenschaft: Mechanik, Werkstoffkunde, Mathematik | Concept | Grundbegriffe, Herleitungen |
| H1 | Technik: Ingenieurwesen allgemein | Concept | Zuverlässigkeit, Nachweiskonzepte |
| H2 | Bauingenieurwesen | Concept | Lastabtragung, Bauphasen |
| H3 | Konstruktiver Ingenieurbau | Concept, KnowledgeItem | Einwirkungen, Tragwerksnachweise |
| H4 | Werkstoff: Beton, Holz (Stahl und weitere später) | Concept | Betonbau, Holzbau |
| H5 | Eurocode-Teil | SourceDocument | EN 1992-1-1, EN 1995-1-1 |
| H6 | Nationaler Anhang / nationale Festlegungen | SourceDocument | ÖNORM B 1992-1-1, ÖNORM B 1995-1-1 |

Eine Aussage gehört dem tiefsten Knoten, aus dem sie belegt ist. Tiefere Ebenen erben die Zuordnung zu den höheren über PART_OF.

### Nebenpfad: Recht

| Ebene | Inhalt | Knotenart (Vorschlag) |
|---|---|---|
| R1 | Landesrecht (Bauordnung des Landes, RIS) | SourceDocument |
| R2 | OIB-Richtlinie, zum Beispiel OIB-RL 1 Mechanische Festigkeit und Standsicherheit | SourceDocument |
| R3 | Schnittmenge OIB und ÖNORM: Verweis auf zitierte Normen | Relation |

### Trennregeln

- Verbindungen zwischen Hauptachse und Nebenpfad entstehen nur als explizite Relation mit Beleg.
- Recht erzeugt keine technischen Kennwerte. Technik erzeugt keine Rechtsaussage.
- Gleiche Schlagwörter oder semantische Nähe erzeugen nur Relationskandidaten (Manifest-Delta).

## 3. Datenmodell

Kantenvokabular laut Manifest-Delta: PART_OF, REFERENCES/REFERS_TO, RESOLVES_TO, DEPENDS_ON, DERIVED_FROM, SUPERSEDES, RELATED_TO, IMPLEMENTS, VALIDATES, CONTRADICTS.

| Beziehung | Kantenart | Ableitung | Beleg |
|---|---|---|---|
| H5 gehört zu H4 (Eurocode-Teil zum Werkstoff) | PART_OF | RULE | Titel des Eurocode-Teils |
| H6 verweist auf H5 (NAD zur EN) | REFERENCES | RULE | Titel der ÖNORM nennt die zugehörige EN |
| Ausgabe alt → Ausgabe neu (1. → 2. Generation) | SUPERSEDES | HUMAN | Veröffentlichungs- und Rückzugsangaben, validity_date |
| OIB-RL → zitierte Norm (R3) | REFERENCES | RULE | Dokument OIB-Richtlinien, Zitierte Normen |
| Widersprüchliche Quellen | CONTRADICTS | HUMAN | beide Fundstellen |

Chunk-Typen laut WO-20260929-03: DEFINITION, REQUIREMENT, RULE, FORMULA, PARAMETER_DEFINITION, TABLE, APPLICABILITY, EXCEPTION, CALCULATION_STEP, EXAMPLE, VERIFICATION, DECISION.

Normen brauchen mindestens: standard_id, edition, national_annex, clause, table/equation, validity_date (MUST-65). Das Wissensschema auf dem Branch `fix/knowledge-validation-ci-20261026` enthält dafür optionale Felder (classification, labels, anchors, relations); der Branch ist noch nicht gemergt.

## 4. Normen- und Rechtsschicht: Stand laut Fundstellen

Zugriff: Suchtreffer-Auszüge, Seiten nicht vollständig gelesen. Vor Verwendung als Beleg im Graphen ist die Primärquelle zu öffnen.

| Dokument | Angabe laut Fundstelle | Prüfstatus |
|---|---|---|
| ÖNORM B 1992-1-1 | Ausgabe 2018-01-01; nationale Parameter, Erläuterungen und Ergänzungen zu ÖNORM EN 1992-1-1, gemeinsam mit dieser anzuwenden | Shop-Eintrag |
| EN 1992-1-1:2023 (2. Generation) | In Deutschland als DIN EN 1992-1-1 (2025-09) gelistet; Rückzug der aktuellen Generation durch CEN laut DBV für März 2028 geplant | Österreichische Übernahme und NAD nicht geprüft |
| ÖNORM B 1995-1-1 | Ausgabe 2015-06-15 mit nationalen Festlegungen zu ÖNORM EN 1995-1-1; zusätzlich Einträge 2019-06-01 (konsolidierte Version) und 2023-08-15 | Geltende Ausgabe prüfen |
| EN 1995-1-1:2025 | Sekundärquellen nennen Veröffentlichung im November 2025; die Eurocode-Seite des JRC listet noch EN 1995-1-1:2004 | Widerspruch, nicht harmonisiert (MUST-68) |
| OIB-Richtlinie 1 (Mai 2023) | OIB-330.1-004/23; Neuerrichtung gilt als erfüllt, wenn der Stand der Technik eingehalten wird; Leitfaden OIB-330.1-005/23 für bestehende Tragwerke | Shop- und Behördenseite |
| OIB-Richtlinien 2023 | Fünfte Ausgabe; in Tirol seit 16.07.2026 verbindlich; OIB-RL 6 (2025) am 29.08.2025 beschlossen | Verbindlichkeit je Bundesland |
| Bauordnung für Wien | Landesrecht konsolidiert im RIS | Welche OIB-Ausgabe in Wien gilt: nicht geprüft |

Folgerung für den Graphen: Beide Eurocode-Generationen und ihre nationalen Festlegungen sind als getrennte Knoten mit validity_date zu führen. Welche Generation für ein Projekt gilt, entscheidet nicht der Graph.

## 5. Pipeline und Qualitätstore

- Ablauf: Quelle → Identität (Version, Repräsentation, SHA-256) → Registry → Extraktion → Objektkandidat → Labels, Anker, Relationen → verifizierter Graph → Retrieval.
- Pilotabnahme (MUST-155): schema-gültige Objekte, stabile IDs, keine ungelösten Quell-IDs, Belegstelle für jede bestätigte Relation, identischer Replay ohne Duplikate, Testfragen liefern Quelle und Stelle oder enthalten sich.
- Lizenz: Normen nicht im Volltext reproduzieren; Lizenzrouting (public, restricted, unknown) laut Analyse vom 2026-10-13.
- Vorschlag Golden Slice: je ein Paar EN + NAD für Beton und Holz, dazu OIB-RL 1 mit zitierten Normen für den Nebenpfad.

## 6. Offene Entscheidungen (ID-01)

- Q1: Adoption der Achsenordnung als Domänenprofil (Anlage A) mit datierter Revision des Manifests (Abschnitt 8) oder als eigenes Artefakt unter LLM-LOCAL-SSOT.
- Q2: Behandlung der Eurocode-Generationen im Graphen (parallel mit validity_date).
- Q3: Geltungsbereich Landesrecht: nur Wien oder weitere Länder.
- Q4: Aufnahmezeitpunkt weiterer Werkstoffe (Stahl, Mauerwerk).
- Q5: Speicherklasse für Auszüge aus lizenzierten Normen.

## Anlage A: Entwurf Domänenprofil (YAML, PROPOSED)

```yaml
domain_profile:
  id: DOMAIN-AEC-STRUCT
  version: v0.1
  status: PROPOSED
  main_axis: [H0_science, H1_engineering, H2_civil, H3_structural, H4_material, H5_eurocode_part, H6_national_annex]
  side_path: [R1_state_law, R2_oib_guideline, R3_oib_oenorm_intersection]
  materials_initial: [concrete, timber]
  rules:
    - relations between main_axis and side_path require explicit evidence
    - law produces no technical values; engineering produces no legal statements
    - edition and validity_date mandatory for every standard node
    - conflicting sources are surfaced, not harmonized
```
