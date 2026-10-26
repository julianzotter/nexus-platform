---
name: LINKLISTE_WISSENSGRAPH-QUELLEN_AEC
version: v0.1
status: ENTWURF
timestamp: 2026-10-26T12:50:00+01:00
agent_id: ID-05
hash: LEDGER-REF provisorisch
gate: PENDING (Human Gate ID-01)
---

# Quellen-Linkliste Wissensgraph AEC (v0.1)

Zugriff: Auszüge aus Suchtreffern vom 2026-10-26, Seiten nicht vollständig gelesen. Vertrauen nach Domänenbewertung der Suche (authoritative, trusted, credible, unrated). Sekundärquellen sind keine Belege für Normgeltung (Baseline MUST-64).

## A. Hauptachse: Eurocode und nationale Festlegungen (H5, H6)

| Quelle | Typ | Vertrauen | Link |
|---|---|---|---|
| JRC Eurocodes: Eurocode 5 (Teile, Neuigkeiten) | Primär/Institution | authoritative | https://eurocodes.jrc.ec.europa.eu/EN-Eurocodes/eurocode-5-design-timber-structures |
| JRC: Second Generation Eurocodes, EN 1995 (Workshop 2025) | Primär/Institution | authoritative | https://eurocodes.jrc.ec.europa.eu/sites/default/files/2025-08/250603-JRC_Eurocode_5_Dietsch_Frangi_Schenk_website.pdf |
| Austrian Standards: ÖNORM B 1992-1-1 (2018-01-01) | Normenshop | trusted | https://www.austrian-standards.at/de/shop/onorm-b-1992-1-1-2018-01-01~p2354397 |
| Austrian Standards: ÖNORM B 1995-1-1 | Normenshop | trusted | https://www.austrian-standards.at/de/shop/onorm-b-1995-1-1-2015-06-15~p2140867 |
| DIN Media: ÖNORM B 1992-1-1 | Normenshop (Dritt) | trusted | https://www.dinmedia.de/en/standard/oenorm-b-1992-1-1/284130921 |
| Eurocode-Online: Eurocode 2 (2. Generation, Listen) | Fachportal (DE) | trusted | https://www.eurocode-online.de/de/eurocode-inhalte/eurocode-2 |
| DBV: Die 2. Generation des Eurocode 2 | Fachverband (DE) | unrated | https://www.betonverein.de/die-2-generation-des-eurocode-2 |
| DIBt: Die zweite Generation der Eurocodes | Fachinstitut (DE) | unrated | https://jahresbericht.dibt.de/de/zweite-generation-eurocodes |
| iTeh: EN 1995-1-1:2025 (Katalogeintrag) | Sekundär | unrated | https://standards.iteh.ai/catalog/standards/cen/29adde25-d6f2-4067-ae05-5f0b2a0c5516/en-1995-1-1-2025 |
| en-standard.eu: Eurocode 5 | Sekundär (Händler) | unrated | https://www.en-standard.eu/eurocodes/eurocode-5/ |

## B. Nebenpfad: Recht (R1 bis R3)

| Quelle | Typ | Vertrauen | Link |
|---|---|---|---|
| OIB: OIB-Richtlinien 2023 (Übersicht, Gesamtfassung) | Primär/Institution | trusted | https://www.oib.or.at/kernaufgaben/oib-richtlinien1/richtlinien/oib-richtlinien-2023/ |
| OIB: Harmonisierung der Bauvorschriften, Inkrafttreten | Primär/Institution | trusted | https://www.oib.or.at/kernaufgaben/oib-richtlinien/ |
| Land Tirol: OIB-RL 1 Ausgabe Mai 2023 (PDF) | Behörde | authoritative | https://www.tirol.gv.at/fileadmin/themen/bauen-wohnen/baupolizei/OIB-2023/oib-rl_1_ausgabe_mai_2023.pdf |
| Land Tirol: OIB-Richtlinien 1-6, Verbindlichkeit | Behörde | authoritative | https://www.tirol.gv.at/bauen-wohnen/zentrale-baudienste/baupolizei/oib-richtlinien-1-6-ausgabe-mai-2023/ |
| Austrian Standards: OIB-Richtlinie 1 (2023-05) | Normenshop | trusted | https://www.austrian-standards.at/de/shop/oib-richtlinie-1-2023-05~p2824187 |
| Austrian Standards: OIB-RL 1 Leitfaden (bestehende Tragwerke) | Normenshop | trusted | https://www.austrian-standards.at/de/shop/oib-richtlinie-1-leitfaden-2023-05~p2824189 |
| Austrian Standards: OIB-RL 1 Erläuternde Bemerkungen | Normenshop | trusted | https://www.austrian-standards.at/de/shop/oib-richtlinie-1-erlauternde-bemerkungen-2023-05~p2824191 |
| WKO OÖ: OIB-Richtlinien 2023 (Überblick) | Interessenvertretung | trusted | https://www.wko.at/ooe/gewerbe-handwerk/bau/oib-richtlinien.pdf |
| RIS: Bauordnung für Wien (konsolidiert) | Rechtsdatenbank | authoritative | https://www.ris.bka.gv.at/GeltendeFassung.wxe?Abfrage=LrW&Gesetzesnummer=20000006 |

## C. Methodik: Datenmodell und Graph

| Quelle | Zweck | Vertrauen | Link |
|---|---|---|---|
| W3C SKOS Reference | Begriffssysteme | authoritative | https://www.w3.org/TR/skos-reference/ |
| W3C PROV-O | Herkunftsmodell | authoritative | https://www.w3.org/TR/prov-o/ |
| LinkML: JSON-Schema-Generator | Schema-Generierung | trusted | https://linkml.io/linkml/generators/json-schema.html |
| ISO 23387 | Datenvorlagen Bauobjekte | authoritative | https://www.iso.org/standard/75403.html |
| buildingSMART IDS (GitHub) | Informationsanforderungen | unrated | https://github.com/buildingsmart/ids |
| dataholz.eu: IDS-Datensatz Holzbauteile | Holzbau-Daten | trusted | https://www.dataholz.eu/bauteile/ids.htm |
| W3C LBD: Building Topology Ontology (BOT) | Gebäudetopologie | authoritative | https://www.semantic-web-journal.net/content/bot-building-topology-ontology-w3c-linked-building-data-group |

## D. Interne Bezüge (Drive, LLM-LOCAL-SSOT)

- 00_NEXUS_MANIFEST__CURRENT__2026-09-28 (Drive-ID 1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg)
- 00_NEXUS_BASELINE_INSTRUCTIONS__CURRENT__2026-09-28 (Drive-ID 1Ig0YFqbWji6B5-oOFcxuVpHb5GEBk0HlbJVz51rf9ho)
- NEXUS_MANIFEST_DELTA_2026-09-28 (Drive-ID 1vLzqh10DEm9jM6mvm25anoMklyvnuXBn-PMPyhZsEiM)
- WO-20260929-03_SEMANTIC-PARSER-CHUNKING-RETRIEVAL_v0.1 (Drive-ID 1LKlwHXoHXMfNy6ykG93_z8QK_7ow1hDkM34osdYRPe8)
