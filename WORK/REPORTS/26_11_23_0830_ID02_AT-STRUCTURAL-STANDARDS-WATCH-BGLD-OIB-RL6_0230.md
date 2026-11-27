---
artifact_type: standards_watch_report
title: AT Structural Standards Watch — Burgenland LGBl. 75/2026 / OIB-Richtlinie 6:2025
created_at: 2026-11-23T08:30:23+01:00
refined_at: 2026-11-23T09:26:31+01:00
revision: 2
monitor_window_start: 2026-11-16
role_id: ID02
agent_name: ChatGPT Private / ChatGPT Chief Orchestrator
executor: OpenAI Codex
executor_instance: /root
provider: OpenAI
model_id: null
ticket_id: null
registration_status: REGISTRATION_PENDING
verification_status: SOURCE_CROSSCHECK_PASS_AFTER_CORRECTION
peer_review_status: PASS_AFTER_REFINEMENT
peer_review_executor_instance: /root/standards_peer_review
peer_review_role_id: null
review_status: SEPARATE_INSTANCE_REVIEW_COMPLETED_SAME_MODEL_FAMILY
authority: ID01 direct request
scope: Austria / Burgenland / energy, life-cycle GWP, solar readiness, documentation and approval workflow
---

# AT Structural Standards Watch — Burgenland LGBl. 75/2026 / OIB-Richtlinie 6:2025

## Entscheidungskern

1. 🔴 **Sofort berücksichtigen:** Neue Gebäude müssen seit Inkrafttreten so geplant und ausgeführt werden, dass ihr Solarenergiepotenzial optimiert und eine spätere kosteneffiziente Installation ermöglicht wird. Das kann Tragwerkskonzept, Dach-, Fassaden- und Balkonflächen, Lastannahmen, Befestigungen und Durchdringungen beeinflussen.
2. 🟡 **GWP-Prozess planen:** Das Lebenszyklus-Treibhauspotenzial wird bei neuen Gebäuden über 1.000 m² für Bauansuchen nach dem 31.12.2027 und bei allen neuen Gebäuden für Bauansuchen nach dem 31.12.2029 verpflichtender Inhalt des Energieausweises.
3. 🟡 **Einreich- und Kontrollprozess umstellen:** OIB-Richtlinie 6:2025 samt Begleitdokumenten, digitale Energieausweise, Datenbankregistrierung und unabhängige Kontrolle sind in der neuen Rechtslage verankert.

## Rechts- und Normstatus

| Ereignis | Datum | Status |
|---|---:|---|
| Verordnung der Burgenländischen Landesregierung | 22.10.2026 | Beschluss-/Verordnungsdatum; dieses Datum führt auch die OIB-Übersicht in ihrer Rubrik „Inkrafttreten“ |
| LGBl. Nr. 75/2026 | 04.11.2026 | authentisch kundgemacht |
| §§ 34–34k, § 36 Abs. 1 und weitere geänderte Bestimmungen | 05.11.2026 | Inkrafttreten gemäß § 43 Abs. 10 am Tag nach der Kundmachung |
| Solarenergieanlage: neue Nichtwohngebäude > 250 m² | 01.01.2027 | Errichtungspflicht, soweit technisch geeignet sowie wirtschaftlich und funktional realisierbar |
| Gebäude-GWP: neue Gebäude > 1.000 m² | Bauansuchen nach 31.12.2027 | Berechnung und Angabe im Energieausweis verpflichtend |
| Solarenergieanlage: bestimmte bestehende Nichtwohngebäude > 500 m² | 01.01.2028 | bei größerer Renovierung oder bestimmten bewilligungspflichtigen Dach-/Systemmaßnahmen, vorbehaltlich § 34f |
| Gebäude-GWP: alle neuen Gebäude | Bauansuchen nach 31.12.2029 | Berechnung und Angabe im Energieausweis verpflichtend |
| Solarenergieanlage: neue Wohngebäude und bestimmte neue überdachte Parkplätze | 01.01.2030 | Errichtungspflicht, soweit technisch geeignet sowie wirtschaftlich und funktional realisierbar |

**Datumsregel:** Die OIB-Webübersicht nennt für Burgenland den 22.10.2026 unter „Inkrafttreten“. Der authentische Rechtsakt ist jedoch am 04.11.2026 ausgegeben worden und bestimmt das Inkrafttreten am Folgetag. Für Rechtsanwendung und NEXUS-Status sind daher Verordnungsdatum, Kundmachung und Inkrafttreten getrennt zu speichern.

## Treffer 1 — Lebenszyklus-GWP im Energieausweis

**Dokument/Klauseln:** LGBl. Nr. 75/2026, § 34 Abs. 3 und § 34b Abs. 4 Z 5.

**Rechtsstatus:** veröffentlicht und seit 05.11.2026 in Kraft; die konkrete Nachweispflicht greift gestaffelt nach dem Datum des Bauansuchens.

**Betroffener Workflow:** frühe Variantenplanung, Mengenmodell, Material- und Produktdaten, Ausschreibung, As-built-Dokumentation, Energieausweis und Behördenprozess.

**Fachliche Auswirkung:**

- ab 01.01.2028 für neue Gebäude mit Nutzfläche > 1.000 m²;
- ab 01.01.2030 für alle neuen Gebäude;
- Berechnung nach Anhang III der Richtlinie (EU) 2024/1275 in der jeweils maßgebenden Fassung;
- das unionsrechtliche Berechnungsframework verwendet relevante Teile von EN 15978, einen Referenzzeitraum von 50 Jahren sowie gemäß CPR bereitgestellte Produktdaten, wenn verfügbar;
- EN-15804-EPDs bleiben wichtige Produktdatenquellen, dürfen aber nicht ohne Prüfung der Datenhierarchie, Systemgrenzen und nationalen Berechnungsvorgaben als alleiniger Rechtsnachweis behandelt werden;
- prEN 15978:2025 ist als Entwurfsreferenz nicht wie eine veröffentlichte verbindliche Norm anzuwenden.

**Priorität:** 🟡 planen; für Projekte > 1.000 m² mit Einreichung ab 2028 bereits jetzt in Leistungsbild, BIM/Mengenstruktur und Ausschreibung vorbereiten.

**Action Points:**

1. Berechnungsvorlagen um `jurisdiction`, `permit_application_date`, `useful_floor_area`, `reference_study_period`, Lebenszyklusmodule, Mengenquelle, Produktdatentyp, Datenstand und Prüfer ergänzen.
2. Nachweisberichte zwischen Vorentwurfs-LCA, Ausschreibungsstand und verpflichtendem As-built-GWP im Energieausweis unterscheiden.
3. Ausschreibungen auf nachvollziehbare Produktdaten, EPD-/DoPC-Identität, Gültigkeitsstand und CPR-Regime vorbereiten.
4. NEXUS/SSOT: Rechtsauslöser 2028/2030, EN-15978-Bezug, CPR-Datenhierarchie und noch festzulegende nationale Detailparameter getrennt modellieren.

## Treffer 2 — Solarbereitschaft und gestaffelte Errichtungspflichten

**Dokument/Klausel:** LGBl. Nr. 75/2026, § 34f; amtliche Erläuterungen zu § 34f.

**Rechtsstatus:** § 34f seit 05.11.2026 in Kraft; einzelne Errichtungspflichten beginnen 2027, 2028 beziehungsweise 2030.

**Betroffener Workflow:** Tragwerkskonzept, Dach-/Fassaden-/Balkonplanung, Nutzlast- und Einwirkungsannahmen, Befestigungen, Durchdringungen, Brandschutzschnittstellen, Ausschreibung und Einreichpläne.

**Fachliche Auswirkung:** Die amtlichen Erläuterungen nennen ausdrücklich die statische Eignung für spätere Solarenergieanlagen. Dach-, Fassaden- und Balkonflächen sollen so geplant werden, dass spätere Installationen ohne kostspielige strukturelle Änderungen möglich sind; Durchdringungen sollen gebündelt und geeignete Flächen freigehalten werden. Projektabhängig sind zusätzliche ständige Lasten, Wind- und Schneeeinwirkungen, lokale Einleitungen, Befestigungs- und Abdichtungsdetails zu berücksichtigen. Die Eurocode-Formeln ändern sich nicht, wohl aber das projektspezifische Einwirkungs- und Anschlussmodell.

**Priorität:** 🔴 sofort für neue Burgenland-Projekte; 🟡 terminbezogen für die gestaffelten Errichtungspflichten.

**Action Points:**

1. Tragwerkskonzept und Lastenheft um reservierte Solarflächen, Systemgewicht, Wartungswege, Befestigungszonen und Nachrüstlastfall ergänzen.
2. Nachweisberichte explizit kennzeichnen, ob nur Solarbereitschaft oder bereits eine konkrete Anlage nachgewiesen wird.
3. Einreich- und Ausschreibungspläne mit nutzbaren Dach-/Fassaden-/Balkonflächen, Durchdringungen und Tragreserven koordinieren.
4. Für Bestands-Nichtwohngebäude > 500 m² ab 2028 bei größerer Renovierung, bei bewilligungspflichtigen Arbeiten am Dach oder bei Installation eines gebäudetechnischen Systems die Solarpflicht und Ausnahmen projektbezogen prüfen.

## Treffer 3 — OIB-Richtlinie 6:2025, Energieausweis und Kontrolle

**Dokument/Klauseln:** § 34b, § 34e, § 34g und § 36 Abs. 1 Z 9 Bgld. BauVO 2008.

**Rechtsstatus:** seit 05.11.2026 in Kraft und für Burgenland verbindlich.

Verbindlich einbezogen sind:

- OIB-Richtlinie 6 „Energieeinsparung und Wärmeschutz“, Ausgabe 2025;
- Leitfaden „Energietechnisches Verhalten von Gebäuden“, September 2025;
- Berechnung des kostenoptimalen Anforderungsniveaus, März 2023/Fassung Juni 2026;
- OIB-Dokument „Nationales Begleitdokument zu ISO-Anhängen“, Juli 2026;
- OIB-Dokument „Unabhängiges Kontrollsystem für Energieausweise“, April 2026.

Energieausweise sind digital auszustellen, in der Energieausweisdatenbank zu registrieren und dem unabhängigen Kontrollsystem unterworfen. Nach § 34e Abs. 2 sind der vollständige Energieausweis sowie alle für die Berechnung der Gesamtenergieeffizienz erforderlichen Daten und Unterlagen elektronisch zu übermitteln.

**Priorität:** 🟡 planen.

**Action Points:**

1. Für Vorhaben, die nach der seit 05.11.2026 geltenden Rechtslage zu beurteilen sind, Energieausweis- und Einreichprozess umstellen; anhängige Verfahren und spezielle Übergangsfragen gesondert prüfen.
2. Schnittstellen zwischen Tragwerk, Bauphysik und Haustechnik nachvollziehbar versionieren; Wärmebrücken- und Feuchtewirkungen nur projektbezogen ableiten.
3. Bewertungen geänderter gebäudetechnischer Systeme dokumentieren und dem Eigentümer übergeben, soweit § 34g greift.

## Abgrenzung zur Tragwerksnormung

- Keine nachgewiesene Änderung der Bemessungsformeln oder Nationalen Anhänge von EC2, EC5 oder CEN/TS 19103 durch LGBl. Nr. 75/2026.
- OIB-Richtlinien 1 bis 5 bleiben in § 36 Abs. 1 als Ausgabe 2019 genannt; der Nationale Plan zur OIB-Richtlinie 6 bleibt Ausgabe 2018.
- Projektlastmodelle und Anschlussdetails können sich durch Solarbereitschaft oder konkrete Solarenergieanlagen dennoch ändern.
- Abweichungen: § 36 Abs. 4 verlangt bei Abweichung ein gleichwertiges Schutzniveau; § 36 Abs. 5 ermöglicht darüber hinaus begründete Einzelfallabweichungen bei örtlichen oder sachlichen Verhältnissen, sofern § 1 weiterhin erfüllt ist.

## Evidenz / Primärquellen

1. RIS, authentisches Landesgesetzblatt — Trefferliste LGBl. Nr. 75/2026: https://www.ris.bka.gv.at/Ergebnis.wxe?Abfrage=LgblAuth
2. Amtliche Informationskopie des Landes Burgenland, LGBl. Nr. 75/2026: https://apps.bgld.gv.at/web/landesrecht.nsf/xsp/.ibmmodres/domino/OpenAttachment/web/landesrecht.nsf/5BF3608F44587EBBC1258EA50045797D/fldFile/LGBl%2075-2026_sig.pdf
3. Anlage 9 / OIB-Richtlinie 6:2025: https://apps.bgld.gv.at/web/landesrecht.nsf/xsp/.ibmmodres/domino/OpenAttachment/web/landesrecht.nsf/008E856C041CCC57C1258EA50045B429/fldFile/LGBl%2075-2026%20Anlage%209_sig.pdf
4. Amtliche Erläuterungen: https://apps.bgld.gv.at/web/landesrecht.nsf/xsp/.ibmmodres/domino/OpenAttachment/web/landesrecht.nsf/7DCAF53090B39C49C1258EA500457D03/fldFileErlaeuterungen/LGBl%2075-2026%20Erl%C3%A4uterungen_sig.pdf
5. RIS, konsolidierte Bgld. BauVO 2008: https://www.ris.bka.gv.at/GeltendeFassung.wxe?Abfrage=LrBgld&Gesetzesnummer=20000684
6. OIB-Übernahmeübersicht: https://www.oib.or.at/kernaufgaben/oib-richtlinien/
7. OIB-Richtlinie 6:2025 und Begleitdokumente: https://www.oib.or.at/richtlinien/oib-richtlinien-2025/oib-richtlinie-6/
8. Richtlinie (EU) 2024/1275, konsolidierter Text/Anhang III: https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:02024L1275-20260524
9. Delegierte Verordnung (EU) 2026/52: https://eur-lex.europa.eu/eli/reg_del/2026/52/oj

## Peer Review und Refinement

**Erstrunde:** FAIL_WITH_FINDINGS.

Behobene Befunde:

1. Falsche Aussage „keine Gebäude-GWP-/LCA-Nachweispflicht“ entfernt und durch die gesetzlichen Stichtage 2028/2030 ersetzt.
2. Strukturell relevante Solarbereitschaft und Errichtungspflichten ergänzt.
3. 22.10.2026 als Verordnungsdatum präzisiert; Kundmachung und Inkrafttreten getrennt.
4. Abweichungsregeln nach § 36 Abs. 4 und 5 vollständig dargestellt.
5. Pauschale Einreichungs- und Wärmebrückenaussagen auf den projektbezogenen Geltungsbereich begrenzt.
6. Direkte Links zu Rechtsakt, Anlage und Erläuterungen ergänzt.

**Re-Review-Status:** PASS_AFTER_REFINEMENT. Materielle Befunde und vier redaktionelle Präzisierungen in Revision 2 umgesetzt; separate Instanz, gleiche Modellfamilie. Keine externe fachliche oder behördliche Freigabe behauptet.

## Ergebnisvertrag

- FINDINGS: drei materielle Workflowänderungen — Solar, Gebäude-GWP, digitaler Energieausweis/Kontrolle.
- EVIDENCE/SOURCES: neun amtliche Primärquellen beziehungsweise amtliche Informationskopien.
- ARTIFACTS: dieses Markdown-Artefakt; Drive-ID und GitHub-PR sind im Übergabebeleg dokumentiert.
- RISKS: falsche Datumssemantik; verspätete GWP-Datenstruktur; nicht berücksichtigte Solar-Nachrüstlasten; Vermischung von Entwurf und verbindlicher Norm.
- NEXT_ACTION: Burgenland-Projektmatrix, Lastenhefte, LCA-Datenmodell, Berichtsvorlagen und Ausschreibungsklauseln aktualisieren; Registereintrag durch autorisierten Ledger-Schreiber.
