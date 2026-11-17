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
    dict(id="K02", name="EIS26 – Rückweg IFC → NSM → neues RF5 → Rücklesen", klasse="Kundendaten – nur lokal",
         quellen=[r"D:\RFEM\EIS_Gesamt_26_BETONBAU.ifc"],
         pruefung={"IFC↔RF5neu": cmp(r"EIS26\cmp_ifc_aus_ifc_rueck.json"), "RF5orig↔RF5neu": cmp(r"EIS26\cmp_rf5_aus_ifc_rueck.json")},
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
    dict(id="K07", name="DWG-Erkennung", klasse="Kundendaten – nur lokal", quellen=[r"D:\RFEM\26_02_06_EIS_TWP_jul.dwg"],
         pruefung={"DWG": dict(status="BLOCKED_ERWARTET", hinweis="AC1032 erkannt, kein Konverter (ODA/LibreDWG) installiert")}),
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
