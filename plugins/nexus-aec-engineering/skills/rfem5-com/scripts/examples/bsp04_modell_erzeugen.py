"""
Beispiel 4 – neues Modell per Skript erzeugen (Python-Übersetzung des offiziellen Dlubal-Beispiels
"RFEMModeller", SDK\\Examples\\RFEM\\C#\\RFEMModeller\\MainForm.cs): 4 Knoten, 3 Stäbe, Lager, Lastfall, Knotenlast,
Berechnung LF1, Schnittgrößen ausgeben.

  python bsp04_modell_erzeugen.py --ziel X:\\SANDBOX\\Testmodell.rf5

STATUS: Namen/Typen gegen die Typbibliothek geprüft; live erfolgreich in RFEM 5.29.01 (17.11.2026).
Einzel-Setter (SetNode, SetLine …) statt Array-Setter (SetNodes) – Arrays von Strukturen über comtypes sind
umständlicher und in diesem Projekt nicht geprüft.
"""
import argparse, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from rfem_connect import rfem_session          # noqa: E402


def struct(R, name, **kw):
    s = getattr(R, name)()
    for k, v in kw.items():
        setattr(s, k, v)
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ziel", required=True, help=".rf5-Pfad für das neue Modell")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    with rfem_session() as (app, R):
        m = app.CreateModel("COM_Beispiel")
        d = m.GetModelData()
        d.PrepareModification()
        try:
            for no, x, y, z in [(1, 0, 0, 0), (2, 3, 0, 0), (3, 3.5, 0, 0), (4, 0, 0, 2)]:
                d.SetNode(struct(R, "Node", No=no, X=x, Y=y, Z=z))
            d.SetMaterial(struct(R, "Material", No=1, TextID=(
                "NameID|Baustahl S 235 JR@TypeID|STEEL@NormID|DIN EN 10025-2@Norm|DIN EN 10025-2:2005-04")))
            d.SetCrossSection(struct(R, "CrossSection", No=1, MaterialNo=1, Description="RO 88.9x3.2"))
            for no, nl in [(1, "1,2"), (2, "2,3"), (3, "4,2")]:
                d.SetLine(struct(R, "Line", No=no, NodeList=nl, Type=R.PolylineType))
            d.SetMemberHinge(struct(R, "MemberHinge", No=1, TranslationalConstantX=-1, TranslationalConstantY=-1,
                                    TranslationalConstantZ=-1, RotationalConstantX=-1,
                                    RotationalConstantY=0, RotationalConstantZ=0))
            for no in (1, 2, 3):
                d.SetMember(struct(R, "Member", No=no, LineNo=no, Type=R.Beam, StartCrossSectionNo=1,
                                   EndCrossSectionNo=1, EndHingeNo=1 if no == 3 else 0))
            # -1 = starr, 0 = frei (sonst Federsteifigkeit in N/m bzw. Nm/rad)
            d.SetNodalSupport(struct(R, "NodalSupport", No=1, NodeList="1,4", SupportConstantX=-1,
                                     SupportConstantY=-1, SupportConstantZ=-1, RestraintConstantX=0,
                                     RestraintConstantY=0, RestraintConstantZ=-1))
            d.FinishModification()
        except Exception:
            d.CancelModification(); raise
        L = m.GetLoads()
        lc = struct(R, "LoadCase", ActionCategory=R.Permanent, Description="Einzellast")
        lc.Loading.No, lc.Loading.Type = 1, R.LoadCaseType
        L.PrepareModification()
        try:
            L.SetLoadCase(lc); L.FinishModification()
        except Exception:
            L.CancelModification(); raise
        ilc = L.GetLoadCase(1, R.AtNo)
        nl = struct(R, "NodalLoad", No=1, NodeList="3")
        nl.Component.Force.X, nl.Component.Force.Z = 500.0, 5000.0          # N
        ilc.PrepareModification()
        try:
            ilc.SetNodalLoad(nl); ilc.FinishModification()
        except Exception:
            ilc.CancelModification(); raise
        errs = m.GetCalculation().Calculate(R.LoadCaseType, 1) or []
        for e in errs:
            print("Berechnung:", e.ErrorNo, e.Description)
        r = m.GetCalculation().GetResultsInFeNodes(R.LoadCaseType, 1)
        for f in r.GetMembersInternalForces(True):
            print(f"Stab {f.MemberNo} x={f.Location:.2f} m  N={f.Forces.X / 1e3:8.3f} kN  My={f.Moments.Y / 1e3:8.3f} kNm")
        os.makedirs(os.path.dirname(os.path.abspath(a.ziel)), exist_ok=True)   # Ordner muss existieren
        m.Save(os.path.abspath(a.ziel))
        print("gespeichert:", os.path.abspath(a.ziel))


if __name__ == "__main__":
    main()
