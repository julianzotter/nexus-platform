# W100 — Zusatzstand 14 deklarierte Familien / 3 dokumentierte Varianten
Version 0.1.0 | UNVERIFIED_INDICATIVE_VALUES | Engineering release NOT_GRANTED
Quelle: [20261112_1934_NEXUS_TIMBERLOOP_BAUTEILMATRIX.md](https://docs.google.com/document/d/1EwMAA4i9yQ8jUfF6NDOR-dyYdFT2L1Pu6ReLaiMEluQ/edit) | 2026-11-12T18:35:33.367Z

- Datei ist ein natives Google Doc mit .md im Titel, keine Raw-Markdown-Datei.
- Dokument enthält drei Varianten, nicht die vollständige Liste der 14 Familien.
- 4,5/5 ohne Einzelkriterien, Gewichtung oder Berechnungsprotokoll.
- Dicken, U-Wert und Massen sind indikativ und ohne konkrete Schicht-/EPD-Nachweise.
- SQL INSERT ohne Konfliktbehandlung nicht wiederholbar; Werte als TEXT ohne getrennte Einheiten.
- m_A setzt Dicke in m und Rohdichte in kg/m3 voraus; bei Gefachen Flächenanteile berücksichtigen.
- R_reuse muss Potenzial und tatsächlich wiederverwendete Masse unterscheiden; Systemgrenze und Nachweisstatus fehlen.
- Prioritäten sind Nutzer-/Artefaktvorschläge, keine nachgewiesenen Empfehlungen des Forschungsprojekts TimberLoop.

## Trennung der IDs
8 bestehende AF-Familien bleiben eigenständig. Drei externe AW/WTW/GD-Varianten werden als EXT-* geführt: verwandt, nicht identisch. Keine elf fehlenden Familien erfunden.

## Schichtweises Prüfschema
variant_id, project_id, revision, ordinal, direction, material, product, thickness_m, density_kg_m3, area_fraction, mass_kg_m2, connection, epd_id, epd_version, contamination_status, dismantling_method, reuse_route, source_id, locator, evidence_status. Unbekannt = null.

## KPI-Vertrag — Vorschlag, nicht berechnet
m_A = Summe(d_i [m] × rho_i [kg/m3] × Flächenanteil_i) [kg/m2]. Parallele Gefachmaterialien anteilig; örtliche Rippen separat. R_reuse,potential = 100 × belegte potenziell wiederverwendbare Masse / Gesamtmasse im gleichen Bilanzraum. Tatsächliche Wiederverwendungsquote separat nach realen Mengen. GWP: gleiche funktionelle Einheit und Bilanzmodule, Modul D separat. Verifizierter Score bleibt null bis Kriterien/Gewichte und Nachweise dokumentiert sind.

