"""
Beispiel 1 – Modelldaten des aktiven RFEM-5-Modells vollständig als JSON exportieren (NUR LESEN).

  python bsp01_modell_lesen.py                    # -> <Modellname>_MODELLDATEN.json im aktuellen Ordner
  python bsp01_modell_lesen.py --out X:\\daten.json

Inhalt: Knoten, Linien, Materialien, Querschnitte, Stäbe, Knotenlager, Gelenke, Lastfälle/-kombinationen
(+ Knoten-/Stablasten je Lastfall). Zahlen unverändert aus RFEM (SI: m, N, N/m).
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from rfem_connect import rfem_session, to_dict          # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    with rfem_session() as (app, R):
        m = app.GetActiveModel()
        d, L = m.GetModelData(), m.GetLoads()
        out = dict(modell=m.GetPath(), version=app.GetVersion(), z_achse=int(m.GetGlobalZAxisOrientation()))
        for key, fn in [("knoten", d.GetNodes), ("linien", d.GetLines), ("materialien", d.GetMaterials),
                        ("querschnitte", d.GetCrossSections), ("staebe", d.GetMembers),
                        ("knotenlager", d.GetNodalSupports), ("stabendgelenke", d.GetMemberHinges),
                        ("lastfaelle", L.GetLoadCases), ("lastkombinationen", L.GetLoadCombinations),
                        ("ergebniskombinationen", L.GetResultCombinations)]:
            try:
                out[key] = to_dict(list(fn() or []))
            except Exception as e:                       # einzelne Tabellen können fehlen
                out[key] = f"FEHLER {type(e).__name__}: {e}"
        out["lasten_je_lf"] = {}
        for lc in L.GetLoadCases():
            ilc = L.GetLoadCase(lc.Loading.No, R.AtNo)
            out["lasten_je_lf"][lc.Loading.No] = dict(
                knotenlasten=to_dict(list(ilc.GetNodalLoads() or [])),
                stablasten=to_dict(list(ilc.GetMemberLoads() or [])))
        name = os.path.splitext(os.path.basename(m.GetPath()))[0] or "MODELL"
    path = a.out or f"{name}_MODELLDATEN.json"
    json.dump(out, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{path}: Knoten {len(out['knoten'])}, Stäbe {len(out['staebe'])}, LF {len(out['lastfaelle'])}")


if __name__ == "__main__":
    main()
