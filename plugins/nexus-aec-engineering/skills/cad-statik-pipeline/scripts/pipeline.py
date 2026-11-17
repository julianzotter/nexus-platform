"""
pipeline.py – Kommandozeile der CAD-Statik-Pipeline (NSM).

  python pipeline.py inspect  <datei|ordner>                 # Zusammenfassung, Befunde, Fingerabdruck
  python pipeline.py convert  <quelle> <ziel>                # Ziel nach Endung: .json .sqlite .dxf .rf5 oder Ordner/ (CSV)
  python pipeline.py compare  <A> <B> [--tol 0.005] [--report bericht.md]
  python pipeline.py rf5-active <ziel.json>                  # aktives RFEM-5-Modell (nur lesen) als NSM speichern

Quellen: .dxf .dwg .ifc .rf5 .rf6 .json .sqlite/.db, Ordner mit nodes.csv (NSM) oder "1.1 Knoten.csv" (RFEM-Export).
Ziel .rf5 legt über COM ein NEUES Modell an (Stufe G2) – nur in Ordnern mit "SANDBOX"; Querschnitte/Materialien
über --map mapping.json (sonst Platzhalter + Befund).
"""
import argparse, collections, json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nsm import to_json, to_csv, to_sqlite                       # noqa: E402
from formats import load, write_dxf, write_rf5, read_rf5, NodeIndex, norm_name   # noqa: E402


def compare(a, b, tol=0.005, plan2d=False):
    """Vergleicht zwei NSM geometrisch (Knoten per Koordinate, Stäbe per Endknoten-Paar) – nummerierungsunabhängig.
    plan2d=True: Grundrissvergleich – z wird ignoriert (Plan-DXF gegen 3D-Modell)."""
    if plan2d:
        import copy
        a, b = copy.deepcopy(a), copy.deepcopy(b)
        for m in (a, b):
            for n in m.nodes:
                n.z = 0.0
            m.meta["z_axis"] = "up"
            seen, keep = {}, []                      # in 2D zusammenfallende Knoten zusammenführen
            idx = NodeIndex(tol); remap = {}
            for n in sorted(m.nodes, key=lambda n: n.id):
                hit = idx.find((n.x, n.y, 0.0))
                if hit is None:
                    idx.add(n.id, (n.x, n.y, 0.0)); keep.append(n); remap[n.id] = n.id
                else:
                    remap[n.id] = hit
            m.nodes = keep
            for x in m.members:
                x.n1, x.n2 = remap[x.n1], remap[x.n2]
            m.members = [x for x in m.members if x.n1 != x.n2]
    za, zb = str(a.meta.get("z_axis", "")), str(b.meta.get("z_axis", ""))

    # Z-down (RFEM) ↔ Z-up (Welt/IFC) = Drehung 180° um X: (x, y, z) → (x, −y, −z) – rechtshändig, keine Spiegelung
    def run(flip):
        idx = NodeIndex(tol)
        for n in b.nodes:
            idx.add(n.id, (n.x, -n.y, -n.z) if flip else (n.x, n.y, n.z))
        amap = {}
        for n in a.nodes:
            hit = idx.find((n.x, n.y, n.z))
            if hit is not None:
                amap[n.id] = hit
        return idx, amap
    cands = [False, True] if not (za in ("up", "down") and zb in ("up", "down")) else [za != zb]
    best = max(((flip,) + run(flip) for flip in cands), key=lambda t: len(t[2]))
    flip, idx, amap = best
    bmap = {n.id: n for n in b.nodes}
    def pb(q):
        return (q.x, -q.y, -q.z) if flip else (q.x, q.y, q.z)
    maxdev = max((math.dist((n.x, n.y, n.z), pb(bmap[amap[n.id]])) for n in a.nodes if n.id in amap), default=0.0)
    bpairs = {frozenset((x.n1, x.n2)): x for x in b.members}
    m_ok, m_miss, sec_diff = 0, [], []
    for x in a.members:
        if x.n1 in amap and x.n2 in amap and frozenset((amap[x.n1], amap[x.n2])) in bpairs:
            m_ok += 1
            y = bpairs[frozenset((amap[x.n1], amap[x.n2]))]
            if norm_name(x.section).lower().replace(" ", "") != norm_name(y.section).lower().replace(" ", ""):
                sec_diff.append((x.id, x.section, y.id, y.section))
        else:
            m_miss.append(x.id)
    pairs_s, pairs_m = collections.Counter(), collections.Counter()
    for x in a.members:
        if x.n1 in amap and x.n2 in amap and frozenset((amap[x.n1], amap[x.n2])) in bpairs:
            y = bpairs[frozenset((amap[x.n1], amap[x.n2]))]
            pairs_s[(x.section, y.section)] += 1; pairs_m[(x.material, y.material)] += 1
    def majority(c):
        best = {}
        for (k, v), n in sorted(c.items(), key=lambda t: (-t[1], t[0])):
            best.setdefault(k, (v, n))
        return {k: v for k, (v, n) in sorted(best.items())}
    a_sup = {(amap.get(s.node), s.fix) for s in a.supports}
    b_sup = {(s.node, s.fix) for s in b.supports}
    res = dict(A=a.meta.get("source"), B=b.meta.get("source"), toleranz_m=tol, z_gespiegelt=flip,
               transformation="Drehung 180° um X (y→−y, z→−z)" if flip else "keine",
               knoten=dict(A=len(a.nodes), B=len(b.nodes), zugeordnet=len(amap), max_abweichung_m=round(maxdev, 6)),
               staebe=dict(A=len(a.members), B=len(b.members), zugeordnet=m_ok, ohne_partner=len(m_miss),
                           querschnitt_abweichend=len(sec_diff)),
               lager=dict(A=len(a.supports), B=len(b.supports), gleich=len(a_sup & b_sup)),
               flaechen=dict(A=len(a.surfaces), B=len(b.surfaces)),
               beispiele=dict(staebe_ohne_partner=m_miss[:10], querschnitt=sec_diff[:10]),
               zuordnung=dict(sections=majority(pairs_s), materials=majority(pairs_m),
                              mehrdeutig=sorted({k for (k, v) in pairs_s} - {k for k in majority(pairs_s)} )))
    res["status"] = ("PASS" if len(amap) == len(a.nodes) == len(b.nodes) and m_ok == len(a.members) == len(b.members)
                     else "ABWEICHUNG")
    return res


def report_md(res):
    k, s, l = res["knoten"], res["staebe"], res["lager"]
    return "\n".join([
        f"# NSM-Vergleich – **{res['status']}**", "", f"- A: `{res['A']}`", f"- B: `{res['B']}`",
        f"- Toleranz {res['toleranz_m']} m · Koordinatentransformation B→A: {res['transformation']}", "",
        "| Objekt | A | B | zugeordnet | Bemerkung |", "|---|---|---|---|---|",
        f"| Knoten | {k['A']} | {k['B']} | {k['zugeordnet']} | max. Abweichung {k['max_abweichung_m']} m |",
        f"| Stäbe | {s['A']} | {s['B']} | {s['zugeordnet']} | ohne Partner {s['ohne_partner']}, Querschnittsname abweichend {s['querschnitt_abweichend']} |",
        f"| Lager | {l['A']} | {l['B']} | {l['gleich']} | gleicher Knoten + gleiche Fixierung |",
        f"| Flächen | {res['flaechen']['A']} | {res['flaechen']['B']} | – | nur Anzahl |", ""]) + "\n"


def main():
    ap = argparse.ArgumentParser(description="NEXUS CAD-Statik-Pipeline (NSM)")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("inspect"); p.add_argument("src"); p.add_argument("--tol", type=float, default=0.005)
    p = sp.add_parser("convert"); p.add_argument("src"); p.add_argument("dst"); p.add_argument("--map")
    p.add_argument("--tol", type=float, default=0.005)
    p = sp.add_parser("compare"); p.add_argument("a"); p.add_argument("b"); p.add_argument("--tol", type=float, default=0.005)
    p.add_argument("--report"); p.add_argument("--json"); p.add_argument("--2d", dest="plan2d", action="store_true",
                                                                         help="Grundrissvergleich (z ignorieren)")
    p = sp.add_parser("rf5-active"); p.add_argument("dst")
    p = sp.add_parser("learn-map", help="Namenszuordnung A→RFEM-Bibliothek aus geprüftem Paar ableiten (B = RF5-NSM)")
    p.add_argument("a"); p.add_argument("b"); p.add_argument("out"); p.add_argument("--tol", type=float, default=0.005)
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    kw = {"tol": a.tol} if getattr(a, "tol", None) and getattr(a, "src", "").lower().endswith((".dxf", ".ifc")) else {}
    if a.cmd == "inspect":
        m = load(a.src, **kw)
        print(json.dumps(dict(meta=m.meta, summary=m.summary(), fingerprint=m.fingerprint(), befunde=m.validate(),
                              extra=m.extra), ensure_ascii=False, indent=1, default=str))
    elif a.cmd == "convert":
        m = load(a.src, **kw); d = a.dst; dl = d.lower()
        if dl.endswith(".json"):
            to_json(m, d)
        elif dl.endswith((".sqlite", ".db")):
            to_sqlite(m, d)
        elif dl.endswith(".dxf"):
            write_dxf(m, d)
        elif dl.endswith(".rf5"):
            mp = json.load(open(a.map, encoding="utf-8")) if a.map else {}
            bef = write_rf5(m, d, mp.get("materials"), mp.get("sections"))
            print("Befunde:", *bef, sep="\n  ")
        elif d.endswith(("/", "\\")) or os.path.isdir(d):
            to_csv(m, d)
        else:
            sys.exit("Zielformat unbekannt (.json .sqlite .dxf .rf5 oder Ordner/)")
        print(f"{a.src} → {d} | {m.summary()} | Fingerabdruck {m.fingerprint()[:16]}")
    elif a.cmd == "compare":
        res = compare(load(a.a), load(a.b), a.tol, a.plan2d)
        md = report_md(res); print(md)
        if a.report:
            open(a.report, "w", encoding="utf-8").write(md)
        if a.json:
            json.dump(res, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
        sys.exit(0 if res["status"] == "PASS" else 2)
    elif a.cmd == "rf5-active":
        m = read_rf5(None); to_json(m, a.dst); print(a.dst, m.summary())
    elif a.cmd == "learn-map":
        A, B = load(a.a), load(a.b)
        res = compare(A, B, a.tol)
        if res["status"] != "PASS":
            sys.exit("Abbruch: Paar ist nicht deckungsgleich – Zuordnung nur aus PASS-Vergleich ableiten.")
        lib = B.extra.get("rfem_bibliothek", {})
        z = res["zuordnung"]
        mp = {"_quelle": f"abgeleitet aus PASS-Vergleich {A.meta.get('source')} ↔ {B.meta.get('source')}",
              "_hinweis": "G2: vor Verwendung durch Tragwerksplaner bestätigen",
              "materials": {k: lib.get("materials", {}).get(v) or v for k, v in z["materials"].items()},
              "sections": {k: lib.get("sections", {}).get(v) or v for k, v in z["sections"].items()}}
        json.dump(mp, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"{a.out}: {len(mp['sections'])} Querschnitte, {len(mp['materials'])} Materialien; mehrdeutig: {z['mehrdeutig']}")


if __name__ == "__main__":
    main()
