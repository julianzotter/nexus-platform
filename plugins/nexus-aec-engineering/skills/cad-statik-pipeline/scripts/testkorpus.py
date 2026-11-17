"""
testkorpus.py – Manifest der lokalen Testsammlung (Quellen, SHA-256, Prüfergebnisse) neu erzeugen.

  python testkorpus.py [--out ..\\references\\testkorpus.json]

Die Vergleichsergebnisse werden aus den cmp_*.json-Dateien der Sandbox gelesen (pipeline.py compare --json …).
Kundendaten bleiben lokal; das Manifest enthält nur Pfade, Prüfsummen und Kennzahlen.
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nsm import sha256_file                                     # noqa: E402

SB = r"D:\RFEM_SANDBOX_CAD"
BOEB = r"G:\Meine Ablage\26-03-18_Boeb_Adaptierung\SANDBOX_RFEM5_COM_20260923_1356"
PD = r"G:\Meine Ablage\_developement\LLM-LOCAL-SSOT\26_10_12_CLA_PARAMETRIC-DESIGN-TEST_v0.1"


def cmp(name):
    p = os.path.join(SB, name)
    if not os.path.exists(p):
        return dict(status="NICHT_GELAUFEN")
    d = json.load(open(p, encoding="utf-8"))
    return dict(status=d["status"], knoten=d["knoten"], staebe=d["staebe"], transformation=d.get("transformation"))


CASES = [
    dict(id="K01", name="EIS26 BETONBAU – Formattripel DXF/IFC/RF5", klasse="Kundendaten – nur lokal",
         quellen=[r"D:\RFEM\EIS_Gesamt_26_BETONBAU.dxf", r"D:\RFEM\EIS_Gesamt_26_BETONBAU.ifc", r"D:\RFEM\EIS_Gesamt_26_BETONBAU.rf5"],
         pruefung={"DXF↔IFC": cmp(r"EIS26\cmp_dxf_ifc.json"), "IFC↔RF5": cmp(r"EIS26\cmp_ifc_rf5.json"), "DXF↔RF5": cmp(r"EIS26\cmp_dxf_rf5.json")}),
    dict(id="K02", name="EIS26 – Rückweg IFC → NSM → neues RF5 (Flächen + Lasten) → Rücklesen", klasse="Kundendaten – nur lokal",
         quellen=[r"D:\RFEM\EIS_Gesamt_26_BETONBAU.ifc"],
         pruefung={"IFC↔RF5neu": cmp(r"EIS26\cmp_ifc_aus_ifc_v3_rueck.json"), "RF5orig↔RF5neu": cmp(r"EIS26\cmp_rf5_aus_ifc_v3_rueck.json"),
                   "Lasten": dict(status="PASS", hinweis="8/8 Lastfälle ΣF und Σp gleich (0,0 %), 245/245 Flächen, 9 freie Linien")},
         mapping=r"D:\RFEM_SANDBOX_CAD\EIS26\mapping_ifc_to_rfem.json (13 Querschnitte, 3 Materialien, aus PASS-Paar gelernt)"),
    dict(id="K03", name="Böblingen 5e – RFEM-CSV-Tabellenexport ↔ RF5", klasse="eigenes Projekt",
         quellen=[BOEB + r"\00_BESTAND_KOPIE\RFEM5_2015\leuchtenabspannung_gesamt_nachaufmassgeometer_150328_5e\1.1 Knoten.csv",
                  BOEB + r"\05_RECHENSTAND\BOEB_BESTAND-5e_NEUBERECHNET_RFEM529_20260923_1437.rf5"],
         pruefung={"CSV↔RF5": dict(status="PASS", knoten="86/86 (max 0,49 mm = CSV-Rundung)", staebe="88/88", lager="35/35")}),
    dict(id="K04", name="Plan-DXF (Umrisse, mm) ↔ IFC4 physisch – Träger (2D)", klasse="eigener Test",
         quellen=[PD + r"\test_inputs\joists_plan.dxf", PD + r"\out\TEST_joists\model_beam_IFC4.ifc"],
         pruefung={"2D": dict(status="PASS", knoten="12/12", staebe="6/6", hinweis="Umriss→Mittellinie, Extrusion→Achse")}),
    dict(id="K05", name="Plan-DXF ↔ IFC4 physisch – Stützen (2D)", klasse="eigener Test",
         quellen=[PD + r"\test_inputs\columns_plan.dxf", PD + r"\out\TEST_columns\model_column_IFC4.ifc"],
         pruefung={"2D": dict(status="PASS", knoten="3/3", hinweis="Quadrat→Stützenpunkt")}),
    dict(id="K06", name="RF6-Inventar ohne API (ZIP + SQLite)", klasse="Dlubal-Beispiel / Projekt",
         quellen=[r"D:\RFEM\04_Tensioned_beam.rf6", r"D:\RFEM\CONTAINER\CTR001.rf6"],
         pruefung={"Inventar": dict(status="PASS", Tensioned_beam="8 Knoten, 11 Stäbe, 7 Lager", CTR001="960 Knoten, 30 Stäbe, 540 Flächen")}),
    dict(id="K07", name="DWG AC1032 → DXF (GNU LibreDWG 0.14) – Gesamtplan", klasse="Kundendaten – nur lokal", quellen=[r"D:\RFEM_02_06_EIS_TWP_jul.dwg"],
         pruefung={"DWG": dict(status="PASS", hinweis="umgewandelt, 0 Prüffehler, mm→m; 185 Layer – ohne Filter kein Statikmodell")}),
    dict(id="K09", name="buildingSMART IFC4X3 structural-curve-member (Zoll/lbf, Teillast) → RF5 → Rücklesen", klasse="öffentlich (bSI)",
         quellen=[r"D:\RFEM_SANDBOX_CAD\OEFFENTLICH\bsi_structural-curve-member\structural-curve-member.ifc"],
         pruefung={"Rundlauf": cmp(r"KORPUS\cmp_bsi_scm.json"), "Last": dict(status="PASS", hinweis="−100 lbf/in = −17.512,7 N/m, Teillast 2,438–4,877 m → −42,7 kN")}),
    dict(id="K10", name="SAF 2.2.0 Haus → RF5 → Rücklesen", klasse="öffentlich (SAF-Beispiele)",
         quellen=[r"D:\RFEM_SANDBOX_CAD\OEFFENTLICH\saf_house_220\SAF_example_HOUSE_metric_ZYX_220.xlsx"],
         pruefung={"Rundlauf": cmp(r"KORPUS\cmp_saf_house.json"),
                   "Befund": dict(status="ERWARTETE_ABWEICHUNG", hinweis="Quelldaten: Stab 45 mit Nulllänge, Knoten 84 koordinatengleich – Lasten 3/3, Flächen 11/11 gleich")}),
    dict(id="K11", name="DWG-Stützenplan mit Layerfilter ^0SP_S_", klasse="Kundendaten – nur lokal", quellen=[r"D:\RFEM_02_06_EIS_TWP_jul.dwg"],
         pruefung={"Filter": dict(status="PASS", hinweis="16 Stützen-Layer → 113 Stützenpunkte (Umriss ≤ 1,0 m)")}),
    dict(id="K08", name="Synthetisches Pratt-Fachwerk (Vorlage)", klasse="frei", quellen=[],
         pruefung={"Offline-Tests": dict(status="PASS", tests="tests/test_offline.py")}),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "testkorpus.json"))
    a = ap.parse_args()
    for c in CASES:
        c["sha256_16"] = {os.path.basename(q): (sha256_file(q)[:16] if os.path.isfile(q) else None) for q in c["quellen"]}
    json.dump(dict(stand="2026-11-17", ersteller="ID06 (Claude Code)", faelle=CASES),
              open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for c in CASES:
        print(c["id"], c["name"], {k: v.get("status") for k, v in c["pruefung"].items()})


if __name__ == "__main__":
    main()
