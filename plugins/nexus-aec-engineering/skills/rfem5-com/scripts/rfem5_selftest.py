"""
rfem5_selftest.py – deterministischer Selbsttest des vollständigen COM-Verbindungswegs (LESEN + SCHREIBEN).

Arbeitet NUR an einem eigens erzeugten Testmodell (CreateModel) und speichert es in einen SANDBOX-Ordner.
Bestehende Modelle werden nur gelesen (T06). Ergebnis: PASS/FAIL/SKIP je Schritt, JSON + Markdown.

  python rfem5_selftest.py                                   # Ausgabe nach %TEMP%\\RFEM5_SELFTEST_SANDBOX\\<Zeit>
  python rfem5_selftest.py --out "G:\\...\\SANDBOX_SELFTEST"   # Ordner muss "SANDBOX" enthalten
  python rfem5_selftest.py --keep-open                        # Testmodell danach nicht schließen

Schritte: T01 Python/comtypes · T02 Typbibliothek · T03 Verbindung · T04 Lizenz · T05 Version · T06 aktives Modell lesen
T07 Testmodell anlegen · T08 Modelldaten schreiben + zurücklesen · T09 Lastfall/Last schreiben + zurücklesen
T10 rechnen · T11 Ergebnisse + Gleichgewicht (ΣLagerkraft vs. ΣLast) · T12 Knoten ändern + zurücklesen
T13 Objekt löschen (eigener Block) · T14 speichern + SHA-256 · T15 Testmodell schließen · T16 Lizenz freigeben
"""
import argparse, datetime as dt, json, os, sys, tempfile, time, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rfem_connect import load_typelib, sha256          # noqa: E402

RES = []


def step(tid, name, fn, needs=()):
    if any(r["status"] != "PASS" for r in RES if r["id"] in needs):
        RES.append(dict(id=tid, name=name, status="SKIP", detail=f"Voraussetzung {needs} nicht erfüllt", ms=0))
        return None
    t0 = time.perf_counter()
    try:
        val, detail = fn()
        RES.append(dict(id=tid, name=name, status="PASS", detail=detail, ms=round((time.perf_counter() - t0) * 1000)))
        return val
    except Exception as e:
        RES.append(dict(id=tid, name=name, status="FAIL", detail=f"{type(e).__name__}: {e}",
                        trace=traceback.format_exc(limit=2), ms=round((time.perf_counter() - t0) * 1000)))
        return None


def S(R, name, **kw):
    s = getattr(R, name)()
    for k, v in kw.items():
        setattr(s, k, v)
    return s


def block(obj, fn):
    obj.PrepareModification()
    try:
        fn(); obj.FinishModification()
    except Exception:
        obj.CancelModification(); raise


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(tempfile.gettempdir(), "RFEM5_SELFTEST_SANDBOX"))
    ap.add_argument("--keep-open", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if "sandbox" not in os.path.abspath(a.out).lower():
        sys.exit("Abbruch: --out muss 'SANDBOX' im Pfad enthalten.")
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    out = os.path.join(os.path.abspath(a.out), stamp); os.makedirs(out, exist_ok=True)
    ctx = {}

    step("T01", "Python 64 bit + comtypes", lambda: (None, f"Python {sys.version.split()[0]}, "
         f"{'64' if sys.maxsize > 2**32 else '32'} bit, comtypes {__import__('comtypes').__version__}")
         if sys.maxsize > 2**32 else (_ for _ in ()).throw(RuntimeError("32-bit-Python")))
    lib = step("T02", "Typbibliothek laden", lambda: (load_typelib(), "RFEM5_64.dll → comtypes.gen.RFEM5"), ("T01",))
    if lib:
        cc, R = lib; ctx["R"] = R
    app = step("T03", "Verbindung GetActiveObject", lambda: (cc.GetActiveObject(R.Application, interface=R.IApplication),
               "an laufende Instanz angehängt"), ("T02",))
    locked = step("T04", "LockLicense + IsComLicensed", lambda: (app.LockLicense() or True,
                  f"COM-Lizenz {bool(app.IsComLicensed())}, Programmlizenz {bool(app.IsAppLicensed())}"), ("T03",))
    try:
        step("T05", "Version / Programmpfad", lambda: (None, f"{app.GetVersion()} | {app.GetPath()}"), ("T04",))

        def t06():
            n = app.GetModelCount()
            if n == 0:
                return None, "kein Modell offen (nur Zählung)"
            m = app.GetActiveModel(); d = m.GetModelData()
            return None, f"{n} Modell(e) offen; aktiv: {m.GetName()} – Kn {d.GetNodeCount()}, St {d.GetMemberCount()}, LF {m.GetLoads().GetLoadCaseCount()}"
        step("T06", "aktives Modell lesen (unverändert)", t06, ("T04",))

        def t07():
            m = app.CreateModel(f"SELFTEST_{stamp}"); ctx["m"] = m
            return m, f"Modell {m.GetName()} angelegt"
        m = step("T07", "Testmodell anlegen", t07, ("T04",))

        def t08():
            d = m.GetModelData(); ctx["d"] = d
            nodes = {1: (0.0, 0.0, 0.0), 2: (3.0, 0.0, 0.0), 3: (3.5, 0.0, 0.0), 4: (0.0, 0.0, 2.0)}
            def w():
                for no, (x, y, z) in nodes.items():
                    d.SetNode(S(R, "Node", No=no, X=x, Y=y, Z=z))
                d.SetMaterial(S(R, "Material", No=1, TextID="NameID|Baustahl S 235 JR@TypeID|STEEL@NormID|DIN EN 10025-2@Norm|DIN EN 10025-2:2005-04"))
                d.SetCrossSection(S(R, "CrossSection", No=1, MaterialNo=1, Description="RO 88.9x3.2"))
                for no, nl in [(1, "1,2"), (2, "2,3"), (3, "4,2")]:
                    d.SetLine(S(R, "Line", No=no, NodeList=nl, Type=R.PolylineType))
                for no in (1, 2, 3):
                    d.SetMember(S(R, "Member", No=no, LineNo=no, Type=R.Beam, StartCrossSectionNo=1, EndCrossSectionNo=1))
                d.SetNodalSupport(S(R, "NodalSupport", No=1, NodeList="1,4", SupportConstantX=-1.0, SupportConstantY=-1.0,
                                    SupportConstantZ=-1.0, RestraintConstantX=0.0, RestraintConstantY=0.0, RestraintConstantZ=-1.0))
            block(d, w)
            rb = {n.No: (n.X, n.Y, n.Z) for n in d.GetNodes()}
            assert rb == nodes, f"Rücklesen Knoten {rb}"
            assert (d.GetMemberCount(), d.GetLineCount(), d.GetNodalSupportCount()) == (3, 3, 1)
            return d, "4 Knoten, 1 Material, 1 Querschnitt, 3 Linien, 3 Stäbe, 1 Lager – Rücklesen identisch"
        d = step("T08", "Modelldaten schreiben + zurücklesen", t08, ("T07",))

        F = (500.0, 0.0, 5000.0)
        def t09():
            L = m.GetLoads()
            lc = S(R, "LoadCase", ActionCategory=R.Permanent, Description="SELFTEST Einzellast")
            lc.Loading.No, lc.Loading.Type = 1, R.LoadCaseType
            block(L, lambda: L.SetLoadCase(lc))
            ilc = L.GetLoadCase(1, R.AtNo)
            nl = S(R, "NodalLoad", No=1, NodeList="3")
            nl.Component.Force.X, nl.Component.Force.Y, nl.Component.Force.Z = F
            block(ilc, lambda: ilc.SetNodalLoad(nl))
            rb = ilc.GetNodalLoads()[0]
            got = (rb.Component.Force.X, rb.Component.Force.Y, rb.Component.Force.Z)
            assert got == F and rb.NodeList == "3", f"Rücklesen Last {got} @ {rb.NodeList}"
            return None, f"LF1 + Knotenlast an Knoten 3 F={F} N – Rücklesen identisch"
        step("T09", "Lastfall + Knotenlast schreiben + zurücklesen", t09, ("T08",))

        def t10():
            C = m.GetCalculation()
            errs = list(C.Calculate(R.LoadCaseType, 1) or [])
            assert not errs, "; ".join(f"{e.ErrorNo} {e.Description}" for e in errs)
            assert m.GetLoads().HasAnyResults()
            return C, "Calculate(LF1) ohne Fehlermeldung, Ergebnisse vorhanden"
        C = step("T10", "rechnen", t10, ("T09",))

        def t11():
            r = C.GetResultsInFeNodes(R.LoadCaseType, 1)
            P = [0.0, 0.0, 0.0]
            for s in r.GetAllNodalSupportForces(False):
                P[0] += s.Forces.X; P[1] += s.Forces.Y; P[2] += s.Forces.Z
            nf = len(list(r.GetMembersInternalForces(True))); nu = len(list(r.GetAllNodalDeformations()))
            tol = 1e-3 * max(abs(f) for f in F)
            same = all(abs(p - f) <= tol for p, f in zip(P, F)); opp = all(abs(p + f) <= tol for p, f in zip(P, F))
            assert same or opp, f"ΣLagerkraft {P} passt nicht zu ΣLast {F} (Toleranz {tol} N)"
            return None, (f"ΣLagerkraft = ({P[0]:.3f}, {P[1]:.3f}, {P[2]:.3f}) N {'= +' if same else '= −'}ΣLast; "
                          f"{nf} Schnittgrößenzeilen, {nu} Verformungszeilen")
        step("T11", "Ergebnisse lesen + Gleichgewicht", t11, ("T10",))

        def t12():
            ni = d.GetNode(3, R.AtNo); nd = ni.GetData(); nd.Z = 0.1
            block(d, lambda: ni.SetData(nd))
            z = d.GetNode(3, R.AtNo).GetData().Z
            assert abs(z - 0.1) < 1e-12, z
            return None, "Knoten 3: Z 0.0 → 0.1 m, Rücklesen identisch"
        step("T12", "Knoten ändern (GetData/SetData) + zurücklesen", t12, ("T08",))

        def t13():
            no = d.GetLastObjectNo(R.NodeObject) + 1
            block(d, lambda: d.SetNode(S(R, "Node", No=no, X=9.0, Y=9.0, Z=9.0)))
            n1 = d.GetNodeCount()
            block(d, lambda: d.DeleteObjects(R.NodeObject, str(no)))
            n2 = d.GetNodeCount()
            assert (n1, n2) == (5, 4), (n1, n2)
            return None, f"Hilfsknoten {no} angelegt (5) und in eigenem Block gelöscht (4)"
        step("T13", "Objekt anlegen + löschen (getrennte Blöcke)", t13, ("T08",))

        def t14():
            p = os.path.join(out, f"SELFTEST_{stamp}.rf5"); m.Save(p)
            assert os.path.isfile(p)
            ctx["file"] = p
            return None, f"{os.path.basename(p)} | {os.path.getsize(p):,} B | SHA-256 {sha256(p)[:16]}…".replace(",", ".")
        step("T14", "speichern (Save mit Pfad) + Hash", t14, ("T08",))

        if not a.keep_open:
            step("T15", "Testmodell schließen", lambda: (m.Close(), "IModel.Close()"), ("T07",))
        else:
            RES.append(dict(id="T15", name="Testmodell schließen", status="SKIP", detail="--keep-open", ms=0))
    finally:
        if locked:
            step("T16", "UnlockLicense", lambda: (app.UnlockLicense(), "Lizenz freigegeben"))
        else:
            RES.append(dict(id="T16", name="UnlockLicense", status="SKIP", detail="nicht gesperrt", ms=0))

    n = {k: sum(r["status"] == k for r in RES) for k in ("PASS", "FAIL", "SKIP")}
    overall = "PASS" if n["FAIL"] == 0 and n["SKIP"] <= (1 if a.keep_open else 0) else "FAIL"
    rep = dict(selftest="rfem5-com", zeit=dt.datetime.now().astimezone().isoformat(timespec="seconds"),
               rechner=os.environ.get("COMPUTERNAME"), python=sys.version.split()[0], gesamt=overall, zaehler=n,
               ausgabe_ordner=out, testmodell=ctx.get("file"), schritte=RES)
    json.dump(rep, open(os.path.join(out, "SELFTEST.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    md = [f"# RFEM-5-COM Selbsttest {stamp} – **{overall}** ({n['PASS']} PASS / {n['FAIL']} FAIL / {n['SKIP']} SKIP)", "",
          "| ID | Schritt | Status | ms | Detail |", "|---|---|---|---|---|"]
    md += [f"| {r['id']} | {r['name']} | {r['status']} | {r['ms']} | {r['detail']} |" for r in RES]
    open(os.path.join(out, "SELFTEST.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md)); print(f"\nProtokoll: {out}")
    sys.exit(0 if overall == "PASS" else 1)


if __name__ == "__main__":
    main()
