"""
rfem_connect.py – allgemeine Verbindung zu RFEM 5 (getestet 5.29.01.161059, 64 bit) über die COM-Schnittstelle.

NUR LESEND: verbindet, sperrt kurz die Lizenz, liest Version/Modelle/Kennzahlen, gibt die Lizenz in jedem Fall frei.
Kein Rechnen, kein Speichern, keine Modelländerung.

Voraussetzungen
  - RFEM 5 läuft (oder --start), Lizenz mit RF-COM (prüfen: Ausgabe "com_licensed")
  - Python 64 bit + comtypes  (pip install comtypes)  – NICHT win32com (RFEM5 hat kein IDispatch)
  - Python NICHT mit -I starten (sonst fehlen User-site-packages wie comtypes)

Aufruf
  python rfem_connect.py                      # Version, Lizenz, alle offenen Modelle mit Kennzahlen
  python rfem_connect.py --open "X:\\pfad\\modell.rf5"   # zusätzlich Modell öffnen (wird nicht gespeichert)
  python rfem_connect.py --guard SANDBOX --open ...       # öffnet nur Pfade, die den Text enthalten
  python rfem_connect.py --start              # RFEM starten, falls keine Instanz läuft
  python rfem_connect.py --json               # Ausgabe als JSON (maschinenlesbar)
  python rfem_connect.py --typelib "C:\\...\\RFEM5_64.dll"  # Typbibliothek explizit

Als Modul
  from rfem_connect import rfem_session, model_summary, to_dict, sha256
  with rfem_session() as (app, R):           # Lizenz wird im finally freigegeben
      m = app.GetModel(0); print(model_summary(m, R))
"""
import argparse, contextlib, json, os, sys

TYPELIB_DEFAULT = r"C:\Program Files\Common Files\Dlubal\RFEM5_64.dll"   # "Dlubal RFEM Type Library"


def load_typelib(path=None):
    import comtypes.client as cc
    p = path or os.environ.get("RFEM5_TYPELIB") or TYPELIB_DEFAULT
    if not os.path.exists(p):
        raise FileNotFoundError(f"Typbibliothek fehlt: {p} (RFEM 5 installiert? COM-Server registriert?)")
    return cc, cc.GetModule(p)


def connect(start=False, typelib=None):
    """Hängt sich an laufendes RFEM 5 an; mit start=True wird sonst eine Instanz gestartet."""
    cc, R = load_typelib(typelib)
    try:
        return cc.GetActiveObject(R.Application, interface=R.IApplication), R
    except OSError as e:
        if not start:
            raise RuntimeError("Keine laufende RFEM-5-Instanz gefunden. RFEM starten oder --start verwenden. "
                               "Falls RFEM läuft: COM-Server neu registrieren (RFEM64.exe /RegServer als Admin).") from e
        app = cc.CreateObject(R.Application, interface=R.IApplication)
        app.Show()
        return app, R


@contextlib.contextmanager
def rfem_session(start=False, typelib=None):
    """Verbindung + LockLicense; UnlockLicense garantiert (sonst bleibt die RFEM-Oberfläche gesperrt)."""
    app, R = connect(start, typelib)
    app.LockLicense()
    try:
        yield app, R
    finally:
        app.UnlockLicense()


def to_dict(o, depth=0):
    """COM-Struktur (ctypes) rekursiv in dict/list umwandeln – für JSON-Export."""
    if depth > 8:
        return str(o)
    if hasattr(o, "_fields_"):
        return {f[0]: to_dict(getattr(o, f[0]), depth + 1) for f in o._fields_}
    if isinstance(o, (list, tuple)):
        return [to_dict(x, depth + 1) for x in o]
    if o is None or isinstance(o, (str, int, float, bool)):
        return o
    return str(o)


def sha256(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def find_model(app, path):
    """Bereits offenes Modell per Pfad finden (case-insensitiv), sonst None."""
    for i in range(app.GetModelCount()):
        m = app.GetModel(i)
        if m.GetPath().lower() == os.path.abspath(path).lower():
            return m
    return None


def model_summary(m, R):
    d, L = m.GetModelData(), m.GetLoads()
    def safe(fn):
        try:
            return fn()
        except Exception as e:                       # einzelne Tabellen können je nach Modell fehlen
            return f"ERR {type(e).__name__}"
    return dict(name=m.GetName(), path=m.GetPath(), description=safe(m.GetDescription),
                nodes=safe(d.GetNodeCount), lines=safe(d.GetLineCount), members=safe(d.GetMemberCount),
                surfaces=safe(d.GetSurfaceCount), solids=safe(d.GetSolidCount),
                materials=safe(lambda: len(d.GetMaterials())), cross_sections=safe(lambda: len(d.GetCrossSections())),
                nodal_supports=safe(lambda: len(d.GetNodalSupports())),
                load_cases=safe(lambda: len(L.GetLoadCases())), load_combinations=safe(lambda: len(L.GetLoadCombinations())),
                result_combinations=safe(lambda: len(L.GetResultCombinations())),
                has_results=safe(lambda: bool(L.HasAnyResults())),
                global_z_axis=safe(lambda: int(m.GetGlobalZAxisOrientation())))


def main():
    ap = argparse.ArgumentParser(description="RFEM 5 COM – nur lesende Verbindungsprüfung")
    ap.add_argument("--open", help="Modell zusätzlich öffnen (.rf5), wird nicht gespeichert")
    ap.add_argument("--guard", help="--open nur erlauben, wenn der Pfad diesen Text enthält (z. B. SANDBOX)")
    ap.add_argument("--start", action="store_true", help="RFEM starten, falls keine Instanz läuft")
    ap.add_argument("--typelib", help=f"Pfad Typbibliothek (Standard {TYPELIB_DEFAULT})")
    ap.add_argument("--json", action="store_true", help="JSON-Ausgabe")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if a.open and a.guard and a.guard.lower() not in os.path.abspath(a.open).lower():
        sys.exit(f"Abbruch: Pfad enthält '{a.guard}' nicht – Originale nicht öffnen.")
    out = {}
    with rfem_session(a.start, a.typelib) as (app, R):
        out.update(version=app.GetVersion(), program_path=app.GetPath(), com_licensed=bool(app.IsComLicensed()))
        if a.open:
            m = find_model(app, a.open) or app.OpenModel(os.path.abspath(a.open))
            out["opened"] = m.GetPath()
        out["models"] = [model_summary(app.GetModel(i), R) for i in range(app.GetModelCount())]
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return
    print(f"RFEM {out['version']} | {out['program_path']} | COM-Lizenz: {out['com_licensed']}")
    if "opened" in out:
        print(f"geöffnet: {out['opened']}")
    print(f"offene Modelle: {len(out['models'])}")
    for i, s in enumerate(out["models"]):
        print(f" [{i}] {s['name']} | Kn {s['nodes']} St {s['members']} Fl {s['surfaces']} | "
              f"LF {s['load_cases']} LK {s['load_combinations']} RK {s['result_combinations']} | "
              f"Ergebnisse {s['has_results']} | {s['path']}")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, FileNotFoundError) as e:
        sys.exit(f"FEHLER: {e}")
