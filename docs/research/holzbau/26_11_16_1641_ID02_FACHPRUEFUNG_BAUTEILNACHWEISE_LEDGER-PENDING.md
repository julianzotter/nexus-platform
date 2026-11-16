---
title: "Fachliche Einzelprüfung Bauteilnachweise – serieller Geschosswohnbau"
document_type: NEXUS_TECHNICAL_EVIDENCE_AUDIT
version: "1.0.0"
date: 2026-11-16
time_zone: Europe/Vienna
agent_id: ID02
scope: "Bauteilspezifische Quellenprüfung, nicht projektspezifische Bemessung"
status: SOURCE_AUDIT_COMPLETE_TECHNICAL_APPROVAL_BLOCKED
technical_approval: false
registry_status: REGISTRATION_PENDING
ledger_number: null
review_status: INDEPENDENT_HUMAN_REVIEW_PENDING
work_root: https://drive.google.com/drive/folders/1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP
---

# FACHPRÜFBERICHT — Bauteilnachweise im seriellen Geschosswohnbau

## 1. Prüfvertrag / Geltungsgrenze

- **Untersucht:** sechs konkrete dataholz-Bauteilvarianten mit Originaldatenblättern/Original-HTML, plus zwei ergänzende Planungs-/Forschungsquellen. Relevanz: mehrgeschossiger geförderter Wohnbau, Holzriegelwand, Holztafel- und HBV-Decken, Dach und Systemplanung.
- **Prüftiefe:** Identität, Ausgabestand, auf dem Datenblatt deklarierte U-/REI-/Schall-/Flächenmassenwerte und **explizite Last-, Spannweiten- und Geometriegrenzen**. Nicht geleistet: Drittprüfung der HFA-Prüfberichte/Klassifikationen, projektbezogene Statik, Brandfall-/Flankenberechnung, Bauprodukt-/Ausschreibungsfreigabe.
- **Evidenzcodes:** `VERIFIED_ORIGINAL_PDF` = Original-PDF als lesbarer Volltext geöffnet; `VERIFIED_ORIGINAL_HTML` = Original-Variante mit Kennwerten geprüft, PDF beim Webzugriff nicht lesbar; `PROCESS_ONLY` = keine technische Bauteilklassifizierung; `DERIVED_MISMATCH` = dokumentierte Randbedingungen stimmen mit Vergleichsfall nicht überein.
- **Schichtabgleich:** Ohne vollständige Identität aller Produkte, Schichtdicken, Fixierungen, Abhängung, Last- und Brandseite sind die folgenden Kennwerte **nicht auf abweichende Aufbauten übertragbar**. Nicht vorhandene Kennwerte werden nicht geschätzt.

## 2. Verifizierte Bauteilmatrix

| Bauteil-ID | Herausgeber/Stand; Primärfundstelle | Ausgewiesene Kennwerte (genau für diese Variante) | Kritische Randbedingungen | Evidenz / Projekttauglichkeit |
|---|---|---|---|---|
| **AW awrhhi01a-04** | dataholz/Holzforschung Austria, **02.08.2023, Rev #7**; [Original-PDF, S. 1](https://www.dataholz.eu/download/de/awrhhi01a-4.pdf) | REI **innen 45 / außen 30**; U = **0,16 W/(m²K)**; Rw(C;Ctr) = **52(-3;-10) dB**; m = **48,40 kg/m²** | h ≤ **3 m**; Ed,fi ≤ **32,0 kN/m**; Holztafel/Holzrahmen mit hinterlüfteter Holzfassade, 240 mm Konstruktionsholz. Bei abweichend verschraubter Lattung gemäß MA39-Bewertung Rw nur **43(-1;-5) dB**. | `VERIFIED_ORIGINAL_PDF` / **ROT**: kein REI90; keine Übernahme auf Holz-Stroh-Lehm-Wand. |
| **AW awropi31b-01** | dataholz/HFA, **02.08.2023, Rev #35**; [Original-PDF, S. 1](https://www.dataholz.eu/download/de/awropi31b-1.pdf) | REI **innen 90 / außen 30**; U = **0,11 W/(m²K)**; Rw(C;Ctr) = **57(-5;-12) dB**; m = **72,40 kg/m²** | h ≤ **3 m**; Ed,fi ≤ **32,0 kN/m**; außen Putz mit **100 mm EPS-F**, 200-mm-Holzrahmen, Holzfasergefach, OSB, innen zweilagige Gipsbekleidung und definierte Unterkonstruktion. | `VERIFIED_ORIGINAL_PDF` / **GELB**: REI90 nur innen, außen 30; nicht identisch mit hinterlüfteter Holzfassade. |
| **GD gdhbvnxa01a-00** | dataholz/HFA, **30.01.2025, Rev #2**; [Original-PDF, S. 1](https://www.dataholz.eu/download/de/gdhbvnxa01a-0.pdf) | REI **90**; U = **0,29 W/(m²K)**; Rw(C;Ctr) = **85(-5;-13) dB**; Ln,w(CI) = **29(3) dB**; m = **448,40 kg/m²** | Spannweite ≤ **4,7 m**; Ed,fi ≤ **5,5 kN/m²**, ohne Fußbodenaufbau. 80 mm Aufbeton + 160 mm CLT, Schüttung, Estrich, abgehängte Bekleidung. | `VERIFIED_ORIGINAL_PDF` / **ROT für 7,8-m-Vergleich**: Brandklassifikation gilt nicht über die angegebene Spannweite hinaus. |
| **GD gdhbvnxa02b-00** | dataholz/HFA, **30.09.2024, Rev #4**; [Original-PDF, S. 1](https://www.dataholz.eu/download/de/gdhbvnxa02b-0.pdf) | REI **90**; U = **0,28 W/(m²K)**; Rw(C;Ctr) = **89(-5;-13) dB**; Ln,w(CI) = **25(3) dB**; m = **524,00 kg/m²** | Spannweite ≤ **4,7 m**; Ed,fi ≤ **5,5 kN/m²**, ohne Fußbodenaufbau. 80 mm Aufbeton + 160 mm CLT, zweilagige Gipsbekleidung; Schüttungs-/Bekleidungsvariante anders als #01a. | `VERIFIED_ORIGINAL_PDF` / **ROT für 7,8-m-Vergleich**. |
| **GD gdrnxa07b-00** | dataholz/HFA, **02.08.2023**; [Original-HTML](https://www.dataholz.eu/bauteile/geschossdecke/variante/kz/gdrnxa07b/nr/00.htm) · [Datenblatt-PDF](https://www.dataholz.eu/download/de/gdrnxa07b-0.pdf) | REI **60**; bedingt REI90 mit **≥ 80/220 mm Balken und 3 × 15 mm GKF-/GF-Bekleidung**; U = **0,26 W/(m²K)**; Rw = **70 dB**; Ln,w = **41 dB**; m = **224,4 kg/m²** | Spannweite ≤ **5 m**, Ed,fi ≤ **3,66 kN/m²** (ohne Fußbodenaufbau); diese Variante von dataholz nicht für deutschen Geltungsbereich ausgewiesen. | `VERIFIED_ORIGINAL_HTML`, PDF hier nicht eigenständig ausgelesen / **GELB/ROT**. |
| **DA fdrhbi06b-00** | dataholz/HFA, **02.08.2023, Rev #7**; [Original-PDF, S. 1](https://www.dataholz.eu/download/de/fdrhbi06b-0.pdf) | REI **60**; bedingt REI90 bei **≥ 80/220 mm Sparren und 3 × 15 mm GKF-/GF-Bekleidung**; U = **0,18 W/(m²K)**; Rw(C;Ctr) = **48(-3;-7) dB**; m = **56,4 kg/m²** | Spannweite ≤ **5 m**, Ed,fi ≤ **3,0 kN/m²** (geprüft ohne Dacheindeckung/Vollschalung/Konterlattung); Unterdach nach Dachneigung/nationaler Regelung. | `VERIFIED_ORIGINAL_PDF` / **GELB/ROT**: REI90 nicht pauschal. |

**Wichtiger Schallhinweis:** Die katalogisierten Laborgrößen `Rw` und `Ln,w` sind keine Gebäudegrößen `R'w`, `L'n,w` oder `L'nT,w`. Flankenübertragungen, Stoßstellen, Fugen und Geometrie fehlen. Der U-Wert ist ebenfalls exakt auf den katalogisierten Aufbau und die modellierten Randbedingungen bezogen.

## 3. Ergänzende Quellen — nicht mit Bauteilprüfungen verwechseln

| Primärquelle | Tatsächlicher Status / Nutzen | Nachweisgrenze |
|---|---|---|
| [TUM EDUwood – Bauteilmatrix (PDF, 2024)](https://www.arc.ed.tum.de/fileadmin/w00cgv/holz/04_Forschung/01_Laufend/Forschungsprojekt_EDUwood_2024_Anhang_A_Bauteilmatrix.pdf) und [Raum-/Bauteilkatalog](https://www.arc.ed.tum.de/fileadmin/w00cgv/holz/04_Forschung/01_Laufend/Forschungsprojekt_EDUwood_2024_Anlage_Raum-und_Bauteilkatalog.pdf) | Forschungs-/Typologiequelle für DfMA-/Modul-/Systemvarianten | `PROCESS_RESEARCH_ONLY`: kein projektspezifisches Prüfzeugnis/keine österreichische Bemessungsfreigabe. |
| [HFA – Leitfaden Gewerke-Schnittstellen im Holzhochbau (Original-PDF)](https://www.holzforschung.at/fileadmin/user_upload/Downloads/Broschueren/gratisdownloads/Leitfaden/Leitfaden-Gewerke-Schnittstellen-Holzhochbau.pdf) | **Ausgabe 12/2025**, 75 PDF-Seiten einschließlich Anhängen, Leitfadenkern 22 Seiten; Planungs-/Koordinationshilfe | `PROCESS_ONLY`: keine REI-/Rw-/U-Klassifizierung einzelner Projektsysteme. **Bibliografische Berichtigung zu Weblinkliste v1**: dort irrtümlich als „2026“ bezeichnet. |

## 4. Projektbezogene Anwendbarkeits-Gates

1. **Keine Pauschalübertragung auf serielle Wohnanlagen in Wien:** Bauklasse/Gebäudeklasse, Brandbeanspruchungsrichtung, geprüfte Detail-/Produkt-/Schichtidentität, Verwendungsbereich und Bundesland/Normstichtag fehlen. Kennwerte des dataholz-Katalogs sind für exakte Variantspezifikation wertvoll, aber kein Nachweis für ein abweichendes Produkt oder Elementstoßdetail.
2. **Beispiel AHS Eisteichen (nur zuvor überlieferte Projektdaten, NICHT aus aktueller Planrevision geprüft):** L_eff etwa **7,8 m**; beide geprüften HBV-Brandvarianten dokumentieren maximal **4,7 m** und entsprechen zudem nicht der beschriebenen Rippen-/Kerven-HBV-Konstruktion. `DERIVED_MISMATCH`, keine REI90-Übernahme; ingenieurmäßige Brandfall-/Verbund- und Schwingungsnachweise getrennt erforderlich.
3. **Für freigabefähige Wohnbau-Aufbauten nachfordern:** Bauteil-/Plan-ID und Revision, echte Stückliste (Schichtdicken, Produkte, Befestigungen), Prüf-/Klassifizierungsberichte, Zulässigkeit für AT/Wien, R/E/I je Brandseite, Feuerlast/Nutzungs-/Bemessungslast, Fugen-/Leibungs-/Deckenranddetails, Schallprüfwerte einschließlich Flanken, U/Feuchte/Wärmebrücken, LCA/EPD-Referenzversion.

## 5. Ergebnisse und QA

- **Fachlicher Ergebnisstatus:** `SOURCE_EVIDENCE_VERIFIED_FOR_5_PDFS_AND_1_HTML`; 6 Varianten gelesen/abgeglichen; 2 Zusatzquellen begrenzt auf Planung/Forschung klassifiziert. Kein verifiziertes Projektfreigabepaket: `TECHNICAL_APPROVAL_BLOCKED`.
- **Befund-Korrektur:** Die früher im Begleitchat genannte Ausgabe der HBV-Decke `gdhbvnxa01a-00` **13.01.2025** war falsch; das Original-PDF zeigt **30.01.2025 / #2**. In diesem Bericht korrigiert.
- **Vorlage:** [Weblinkliste v2.0](https://drive.google.com/file/d/1yEcWuZZenBvUrKCF5bKh_nLcki7AUB3g/view) und [Statusreport v2.0](https://drive.google.com/file/d/18zgKfjPqsiBv3v1ChyasvfMXbiWRzbu2/view).
- **Unabhängige reale human-fachliche Freigabe:** `NOT_RUN`. Eine in derselben Chat-Infrastruktur durchgeführte zweite KI-Sichtung ist keine unabhängige Prüfstatik oder reale ID03-ACK.
- **NEXUS:** Das Dokument ist vorläufig ohne bestätigte Ledgernummer/Registry-Eintrag; `REGISTRATION_PENDING`. ID03-WORK-Order folgt getrennt, Quelltext nicht löschen/überschreiben.
