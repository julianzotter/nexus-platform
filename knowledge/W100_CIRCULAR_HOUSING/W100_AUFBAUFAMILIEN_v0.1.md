---
name: W100-AUFBAUFAMILIEN
version: 0.1.0
created_at: 2026-11-12T19:31:40+01:00
agent_id: ID02
executor: OpenAI Codex
executor_instance: /root
ticket_id: WO-20261112-W100-CHAT-TO-KB
ledger_id: null
review_status: REVIEW_PENDING
engineering_release: NOT_GRANTED
---
# Aufbaufamilien — Retrieval-Karten
Schematische Familien; keine Statistik und keine freigegebenen Aufbauten. Dicken nur in AS-Projektdatensätzen.

## AF-AW-01 Mineralisch mit WDVS
AUSSENWAND | innen nach außen bzw. Wohnung zu Nachbarwohnung | DERIVED_FAMILY_REVIEW_PENDING
Oberfläche/Innenputz → Stahlbeton oder Mauerwerk → Dämmstoffsystem → Armierung → Oberputz
Variantenfamilie; verklebte Schichten erschweren stofflich getrennten Rückbau.
Quellen: [S26](https://fify-dynamo-assets.sos-at-vie-1.exo.io/b7ec257816f19f936bcfe8babbcd4789.pdf)

## AF-AW-02 Vorgefertigter Holzrahmen
AUSSENWAND | innen nach außen bzw. Wohnung zu Nachbarwohnung | DERIVED_FAMILY_REVIEW_PENDING
Innenbekleidung → optionale Installationsebene → Luftdichtungs-/Dampfbremskonzept → Holzrahmen mit Gefachdämmung → Außenbeplankung/Winddichtung → Putzsystem ODER Hinterlüftung und Bekleidung
Schema, keine einzelne geprüfte Variante. Nichttragende Ausführung kann Hülle und Tragwerk entflechten.
Quellen: [S01](https://drive.google.com/file/d/1ynUHuKWRd25J3P4pSPqG31bBPO-le76q/view); [S04](https://gernergernerplus.com/projekte/rote-emma/); [S13](https://acms-architekten.de/detailseiten-projekte/variowohnungen-wuppertal); [S27](https://www.dataholz.eu/bauteile/mehrgeschossiger-wohnbau.htm)

## AF-AW-03 Beton-Sandwich/Thermowand
AUSSENWAND | innen nach außen bzw. Wohnung zu Nachbarwohnung | DERIVED_FAMILY_REVIEW_PENDING
Innere Betonschale → Ortbetonkern falls Halbfertigteil → Dämmung → Äußere Betonschale
Fugen, Verbinder, Dämmstoff und selektiven Rückbau prüfen.
Quellen: [S01](https://drive.google.com/file/d/1ynUHuKWRd25J3P4pSPqG31bBPO-le76q/view)

## AF-WT-01 Mineralische Wohnungstrennwand
WOHNUNGSTRENNWAND | innen nach außen bzw. Wohnung zu Nachbarwohnung | DERIVED_FAMILY_REVIEW_PENDING
Oberfläche → schwere Beton- oder Schallschutzmauerwerkswand → optionale gedämmte entkoppelte Vorsatzschale → Oberfläche
Tragende Wand begrenzt Zusammenlegung; Vorsatzschale nach Fachnachweis.
Quellen: [S26](https://fify-dynamo-assets.sos-at-vie-1.exo.io/b7ec257816f19f936bcfe8babbcd4789.pdf)

## AF-WT-02 Trockenbau-Wohnungstrennwand
WOHNUNGSTRENNWAND | innen nach außen bzw. Wohnung zu Nachbarwohnung | DERIVED_FAMILY_REVIEW_PENDING
mehrlagige Gipsplatten → gedämmte akustisch getrennte Ständerkonstruktion → mehrlagige Gipsplatten
Schematische Alternative; nicht mit einfacher Wohnungsinnenwand verwechseln; exakte Systemzulassung offen.
Quellen: [S27](https://www.dataholz.eu/bauteile/mehrgeschossiger-wohnbau.htm); [S28](https://www.proholz.at/zuschnitt/80/konstruktive-faktoren-und-stellschrauben)

## AF-WT-03 Mehrschalige Massivholztrennwand
WOHNUNGSTRENNWAND | innen nach außen bzw. Wohnung zu Nachbarwohnung | DERIVED_FAMILY_REVIEW_PENDING
Bekleidung/Vorsatzschale je System → Massivholzschale → entkoppelte Zwischenlage bzw. zweites Wandsystem → Bekleidung je System
Eibengasse 2x80mm betrifft Tragwerksangabe, kein kompletter Schall-/Brandnachweis.
Quellen: [S02](https://drive.google.com/file/d/1Rq3mbiywZ0k0w-rFBzhsbKBszitlSVkt/view); [S27](https://www.dataholz.eu/bauteile/mehrgeschossiger-wohnbau.htm); [S28](https://www.proholz.at/zuschnitt/80/konstruktive-faktoren-und-stellschrauben)

## AF-DE-01 Stahlbetondecke mit schwimmendem Estrich
DECKE | oben nach unten | DERIVED_FAMILY_REVIEW_PENDING
Bodenbelag → schwimmender Estrich → Trennlage → Trittschalldämmung → Ausgleichs-/Installationsschüttung → Stahlbetontragdecke → Spachtelung oder Unterdecke
Vorhandene Folienlagen projektbezogen; Reihenfolge keine universelle Ausführungsfreigabe.
Quellen: [S01](https://drive.google.com/file/d/1ynUHuKWRd25J3P4pSPqG31bBPO-le76q/view); [S26](https://fify-dynamo-assets.sos-at-vie-1.exo.io/b7ec257816f19f936bcfe8babbcd4789.pdf)

## AF-DE-02 Holz-/CLT-Decke mit Akustikaufbau
DECKE | oben nach unten | DERIVED_FAMILY_REVIEW_PENDING
Bodenbelag → Nass- ODER Trockenestrich → Trennlagen nach System → Trittschalldämmung → Beschwerung/Ausgleich → Holztragdecke → Sichtoberfläche ODER entkoppelte Unterdecke
Flanken, Fugen, Schüttung und elastische Lager projektbezogen prüfen.
Quellen: [S02](https://drive.google.com/file/d/1Rq3mbiywZ0k0w-rFBzhsbKBszitlSVkt/view); [S27](https://www.dataholz.eu/bauteile/mehrgeschossiger-wohnbau.htm); [S28](https://www.proholz.at/zuschnitt/80/konstruktive-faktoren-und-stellschrauben)
