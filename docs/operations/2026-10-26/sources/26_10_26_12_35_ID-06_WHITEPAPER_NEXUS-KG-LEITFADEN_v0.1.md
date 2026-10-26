---
name: whitepaper-nexus-kg-leitfaden
version: v0.1
status: REVIEW
timestamp: 2026-10-26T12:35+01:00
agent_id: ID-06
hash: sha256:88ef1d267c5ef4b078681f7a3c38f17ae75bbf789ed001b88200c7a1b363c4d0 (Body vor Hash-Eintrag)
gate: PENDING
owner_id: ID-01
description: Leitfaden Wissensdatenbank-Architektur + Klassifizierung NEXUS Knowledge Engineering System (konstruktiver Ingenieurbau) + Quellen-Linkliste
source_basis: Manifest Wissensgraph (Voice-Session 2026-10-26 07:23, Memory-Notiz); Kandidat Primärquelle: 29_09_29_NEXUS-AI-MANIFEST-KNOWLEDGE-ENGINEERING-SYSTEM.pdf (Drive 1dZX3RYZ-nAEpQD7-30jxdPmA-xxy0N1k, 00-AI-IMAGES; >10 MB, Textabruf nicht möglich) → Inhalt UNVERIFIZIERT, Lücke L1
scope: Rollout-Vorlage für alle LLM-Rollen ID02–ID08
---

# WHITE PAPER — NEXUS KNOWLEDGE ENGINEERING: HIERARCHIE, KLASSIFIZIERUNG, MAPPING (v0.1)

## 0 TL;DR
- Intern EINE Hauptachse: Technik (Wissenschaft → … → EC-Teil → NAD-AT). Recht = Nebenpfad. Schnittmenge = verbindlich erklärte Normen (OIB/ÖNORM).
- Keine 4 gleichrangigen Facetten. Externe Standards (IFC, bSDD, ISO 12006) = Mapping-Layer, nie interne Struktur.
- Wissensdaten nach deutscher EC-Fassung (Austrian Standards); kein DE/EN-Mix.
- Pipeline: SSoT-Markdown → strukturierter LLM-Call → Pydantic-Validierung → JSON Knowledge-Chunk (ID + Hash + Quelle).

## 1 Leitprinzipien
1. Use-Case-first intern, Standards-first extern (Mapping).
2. Jeder Chunk: genau 1 Pfad auf Hauptachse + optional Recht-Tag + optional Mapping-Tags.
3. Quelle Pflicht (Norm/§/Ausgabe) sonst `unbelegt`.
4. LLM strukturiert, Code validiert, Git/Hash beweist.
5. Begriffe/Formelzeichen = Glossar aus EN 1990 + B 1990-1 (Basis), nicht aus IFC.

## 2 Hauptachse TECHNIK (Label-Hierarchie L0–L8)
| L | Label | Beispiel-Werte |
|---|---|---|
| L0 | DOMAIN | Naturwissenschaft / Mathematik / Physik |
| L1 | SCIENCE | Ingenieurwissenschaften |
| L2 | FIELD | Bauingenieurwesen |
| L3 | DISCIPLINE | Konstruktiver Ingenieurbau |
| L4 | SUBJECT | Baustatik · Tragwerksplanung · Mechanik · Festigkeitslehre · Bauphysik(Schnittstelle) |
| L5 | MATERIAL | Beton · Holz · Stahl · Mauerwerk · Verbund (HBV) |
| L6 | CODE_PART | EC0 EN 1990 · EC1 EN 1991-x · EC2 EN 1992-1-1 · EC5 EN 1995-1-1 · EC8 … |
| L7 | NAD | ÖNORM B 1990-1 · B 1991-x · B 1992-1-1 · B 1995-1-1 (AT) · DIN-NA (DE, nur Projektbezug) |
| L8 | CLAUSE | §-Nr., Tabelle, Gleichung, NDP |

Pfad-String (Beispiel): `TECH/ING/BAU/KIB/STATIK/HOLZ/EC5-1-1/B1995-1-1/§6.1.2`

## 3 Nebenpfad RECHT (Label R0–R5, nachgeordnet)
| R | Label | Werte |
|---|---|---|
| R0 | INTL | internationales Recht |
| R1 | EU | EU-Verordnungen/Richtlinien (CPR 305/2011) |
| R2 | NATIONAL | Bundesrecht AT |
| R3 | LAND | Bauordnung Wien/NÖ/… |
| R4 | BINDING_RULE | OIB-RL 1–6 (verbindlich erklärt) |
| R5 | NORM_REF | EN/ÖNORM via OIB "Zitierte Normen" |

Schnittmenge-Regel: Objekt mit R4/R5 UND L6/L7 → Tag `BINDING=true` (Stand der Technik + Rechtsquelle). Beide Pfade zulässig, Primärpfad bleibt TECHNIK.

## 4 Knowledge-Chunk-Schema (Pydantic → JSON)
```python
class KnowledgeChunk(BaseModel):
    id: str                 # KC-YYYYMMDD-NNNN
    type: Literal["SOURCE","CLAUSE","FORMULA","TERM","MATERIAL","COMPONENT","NDP","RULE"]
    tech_path: str          # L0..L8 Pfad-String (Pflicht)
    law_path: str | None    # R0..R5 (optional)
    binding: bool = False
    source: Source          # norm_id, edition, clause, page, lang="de"
    text_de: str            # Originalwortlaut/Paraphrase, DE
    symbols: list[Symbol]   # Formelzeichen aus EN 1990 Glossar
    mappings: Mappings      # ifc: list[str]; bsdd: list[str]; iso12006: str|None
    evidence: Literal["belegt","unbelegt"]
    hash: str               # sha256(text_de+source)
    ledger_id: str | None
```
Validierungsregeln: tech_path Pflicht + gültig gegen Taxonomie-Datei; source.edition Pflicht; lang=="de"; evidence=="belegt" nur mit clause.

## 5 Mapping-Layer (extern, austauschbar)
| Ziel | Zweck | Mapping-Regel |
|---|---|---|
| IFC 4.x (ISO 16739-1) | Geometrie/Bauteil-Export | L5/COMPONENT → IfcBeam/IfcSlab/… + Pset |
| bSDD | Eigenschafts-/Klassifikationsaustausch | TERM/MATERIAL → bSDD-URI |
| ISO 12006-2 / -3 | Klassifikationsrahmen | L3–L5 → Tabellen (Element, Work Result) |
| ÖNORM A 6241 / ÖBA-Klassifikation | AT-Bauteilgliederung | COMPONENT → Code |
| IDS (bSI) | Anforderungsprüfung | RULE → IDS-Specification |
Grundsatz: Mapping-Tabellen sind eigene Dateien (CSV/JSON), versioniert; interne IDs bleiben stabil.

## 6 Pipeline (SSoT → Chunks)
1. Ingest: Norm-PDF → `pdftotext -layout` → MD (Run-0-Zählung: Wörter, Begriffe, NDP, Tabellen)
2. Chunking: nach §-Struktur (Clause-Level), nicht nach Token-Fenster
3. Strukturierter LLM-Call: Schema-Prompt → JSON (nur Klassifizieren/Extrahieren, nicht Rechnen)
4. Pydantic-Validate → bei Fehler `REVIEW_REQUIRED`
5. Registry (SQLite): id, tech_path, source, hash, status; Hash-Chain
6. Peer-Review EXEC≠REVIEW; Freigabe ID01 → Status VERIFIED
7. Export: Mapping-Layer on demand

## 7 Konflikt Recht vs Technik — Entscheidung
- Frage: "Ist EC2 ein Rechts- oder Technikobjekt?" → Antwort: TECHNIK-Primärpfad (L6), Recht-Tag R5 + `BINDING=true` wenn via OIB zitiert.
- Doppelablage verboten; Mehrfach-Tags erlaubt.
- Landesrecht liefert nur den Geltungs-Trigger, nie den Inhalt.

## 8 Rollout-Regeln für alle LLM-Rollen
- Taxonomie-Datei `NEXUS-KG-TAXONOMY_v0.1.json` = einzige Quelle für Labels (zu erstellen, WO folgt)
- Kein LLM erfindet Labels; unbekannt → `UNCLASSIFIED` + Review
- Jede Chunk-Ausgabe mit RESULT-Block (findings/evidence/qa_status)

## 9 Quellen-Linkliste (Normative Grundlagen & Begriffsdefinitionen)
Format: #NR, NAME, URL — Domain-Ebene geprüft (stabil); Dokumentebene teils kostenpflichtig.
- #01, EC-Portal JRC, https://eurocodes.jrc.ec.europa.eu/
- #02, JRC NDP-Datenbank, https://eurocodes.jrc.ec.europa.eu/ndp
- #03, Austrian Standards, https://www.austrian-standards.at/
- #04, OIB-Richtlinien, https://www.oib.or.at/
- #05, OIB Zitierte Normen, https://www.oib.or.at/de/oib-richtlinien/richtlinien (Unterseite "Zitierte Normen", unbelegt-exakt)
- #06, RIS Bauordnung Wien, https://www.ris.bka.gv.at/
- #07, CEN Eurocodes, https://www.cen.eu/
- #08, buildingSMART, https://www.buildingsmart.org/
- #09, bSDD, https://search.bsdd.buildingsmart.org/
- #10, IFC 4.3 Doku, https://ifc43-docs.standards.buildingsmart.org/
- #11, ISO 12006-2, https://www.iso.org/standard/61753.html
- #12, ISO 16739-1 (IFC), https://www.iso.org/standard/84123.html
- #13, IDS bSI, https://technical.buildingsmart.org/projects/information-delivery-specification-ids/
- #14, EU CPR 305/2011, https://eur-lex.europa.eu/eli/reg/2011/305/oj
- #15, DIN NA Bau, https://www.din.de/
- #16, holzbau handbuch (DE), https://www.informationsdienst-holz.de/
- #17, proHolz Austria, https://www.proholz.at/
- #18, TU Graz Holzbau, https://www.tugraz.at/institute/lignum/
- #19, ÖBV Beton, https://www.bautechnik.pro/ (unbelegt-exakt)
- #20, Zotter Diss. TU Graz 2008, intern (Drive, Kategorie A Wissensquellen-Inventar)

## 10 Offene Punkte / Lücken
- L1: Manifest-PDF (1dZX3RYZ…, Variante 1akYL7OC…) gefunden, >10 MB, Bild-PDF, nicht extrahierbar via Connector → ID01: als Anhang/Textfassung liefern oder Device-Bridge; Abgleich Achsen offen
- L2: Taxonomie-JSON v0.1 erstellen (WO)
- L3: EN 1990 Glossar-Run (NORMTEXT) ausstehend
- L4: Links #05, #19 exakte Unterseite unverifiziert
- L5: Mapping-Tabellen IFC/bSDD leer

## LOG
- 2026-10-26 12:35 ID-06: v0.1 erstellt auf Memory-Basis; WORK; Ledger-ID PENDING; RUNLOG nicht fortgeschrieben
