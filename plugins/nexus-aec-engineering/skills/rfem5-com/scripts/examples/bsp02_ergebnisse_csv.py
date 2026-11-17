"""
Beispiel 2 – vorhandene Ergebnisse des aktiven Modells als CSV exportieren (NUR LESEN, rechnet nicht).

  python bsp02_ergebnisse_csv.py --typ LK --nr 1      # Lastkombination 1
  python bsp02_ergebnisse_csv.py --typ RK --nr 2      # Ergebniskombination 2 (mehrere Zeilen je Ort: Max/Min)
  python bsp02_ergebnisse_csv.py --typ LF --nr 1 --out X:\\ordner

Schreibt drei Dateien (Semikolon, UTF-8 mit BOM für Excel):
  <typ><nr>_STABSCHNITTGROESSEN.csv  Stab, Ort x [m], N/Vy/Vz [kN], MT/My/Mz [kNm]  (Stabachsen)
  <typ><nr>_LAGERKRAEFTE.csv         Knoten, Px/Py/Pz [kN], Mx/My/Mz [kNm]          (global)
  <typ><nr>_VERFORMUNGEN.csv         Knoten, ux/uy/uz [mm], phi [mrad]
Umrechnung nur Einheiten (N -> kN, m -> mm); keine weitere Rechnung.
"""
import argparse, csv, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from rfem_connect import rfem_session          # noqa: E402

TYP = {"LF": "LoadCaseType", "LK": "LoadCombinationType", "RK": "ResultCombinationType"}


def write(path, head, rows):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(head); w.writerows(rows)
    print(f"{path}: {len(rows)} Zeilen")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--typ", choices=TYP, required=True)
    ap.add_argument("--nr", type=int, required=True)
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    os.makedirs(a.out, exist_ok=True)
    with rfem_session() as (app, R):
        m = app.GetActiveModel()
        if not m.GetLoads().HasAnyResults():
            sys.exit("Keine Ergebnisse im Modell – zuerst in RFEM rechnen (oder Beispiel 3).")
        r = m.GetCalculation().GetResultsInFeNodes(getattr(R, TYP[a.typ]), a.nr)
        p = os.path.join(a.out, f"{a.typ}{a.nr}_")
        write(p + "STABSCHNITTGROESSEN.csv", ["Stab", "x_m", "N_kN", "Vy_kN", "Vz_kN", "MT_kNm", "My_kNm", "Mz_kNm", "Typ"],
              [(f.MemberNo, round(f.Location, 4), f.Forces.X / 1e3, f.Forces.Y / 1e3, f.Forces.Z / 1e3,
                f.Moments.X / 1e3, f.Moments.Y / 1e3, f.Moments.Z / 1e3, int(f.Type))
               for f in r.GetMembersInternalForces(True)])          # True = Stabachsen
        write(p + "LAGERKRAEFTE.csv", ["Knoten", "Px_kN", "Py_kN", "Pz_kN", "Mx_kNm", "My_kNm", "Mz_kNm", "Typ"],
              [(s.NodeNo, s.Forces.X / 1e3, s.Forces.Y / 1e3, s.Forces.Z / 1e3,
                s.Moments.X / 1e3, s.Moments.Y / 1e3, s.Moments.Z / 1e3, int(s.Type))
               for s in r.GetAllNodalSupportForces(False)])          # False = globales System
        write(p + "VERFORMUNGEN.csv", ["Knoten", "ux_mm", "uy_mm", "uz_mm", "phix_mrad", "phiy_mrad", "phiz_mrad", "Typ"],
              [(u.NodeNo, u.Displacements.X * 1e3, u.Displacements.Y * 1e3, u.Displacements.Z * 1e3,
                u.Rotations.X * 1e3, u.Rotations.Y * 1e3, u.Rotations.Z * 1e3, int(u.Type))
               for u in r.GetAllNodalDeformations()])


if __name__ == "__main__":
    main()
