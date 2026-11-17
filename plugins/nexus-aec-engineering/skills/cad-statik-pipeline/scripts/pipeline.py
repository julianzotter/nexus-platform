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
import argparse, collections, json, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nsm import to_json, to_csv, to_sqlite                       # noqa: E402
from formats import load, write_dxf, write_rf5, read_rf5, NodeIndex, norm_name   # noqa: E402


def _surface_matches(a, b, amap):
    """Flächen gleich, wenn gleiche Nummer und die Randknoten der einen Seite in der anderen enthalten sind
    (IFC teilt Ränder an jedem Knoten, RFEM speichert durchgehende Randlinien)."""
    bs = {s.id: set(s.nodes) for s in b.surfaces}
    n = 0
    for s in a.surfaces:
        if s.id in bs and all(x in amap for x in s.nodes):
            sa = {amap[x] for x in s.nodes}
            n += sa <= bs[s.id] or bs[s.id] <= sa
    return n


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
               flaechen=dict(A=len(a.surfaces), B=len(b.surfaces),
                             zugeordnet=_surface_matches(a, b, amap)),
               lasten=compare_loads(a, b, flip) if (a.loads.get("cases") or b.loads.get("cases")) else None,
               beispiele=dict(staebe_ohne_partner=m_miss[:10], querschnitt=sec_diff[:10]),
               zuordnung=dict(sections=majority(pairs_s), materials=majority(pairs_m),
                              mehrdeutig=sorted({k for (k, v) in pairs_s} - {k for k in majority(pairs_s)} )))
    res["status"] = ("PASS" if len(amap) == len(a.nodes) == len(b.nodes) and m_ok == len(a.members) == len(b.members)
                     else "ABWEICHUNG")
    return res


def _area(pts):
    """Fläche eines (ebenen) Polygons über Newell-Normale [m²]."""
    nx = ny = nz = 0.0
    for (x1, y1, z1), (x2, y2, z2) in zip(pts, pts[1:] + pts[:1]):
        nx += (y1 - y2) * (z1 + z2); ny += (z1 - z2) * (x1 + x2); nz += (x1 - x2) * (y1 + y2)
    return 0.5 * math.sqrt(nx * nx + ny * ny + nz * nz)


def load_resultants(m, flip=False):
    """Je Lastfall zwei geometrieunabhängige Kennwerte:
    F = Σ Knotenkräfte + Σ q·L (Stab-/Linienlasten) [N]; P = Σ p · Anzahl Zielflächen (Flächenlasten) [N/m²].
    P*-Richtungen werden wie die wahre Richtung gezählt. flip=True: Drehung 180° um X (y, z negieren)."""
    nm = {n.id: (n.x, n.y, n.z) for n in m.nodes}
    mem = {x.id: (x.n1, x.n2) for x in m.members}
    out = {c["id"]: dict(n=0, F=[0.0] * 3, P=[0.0] * 3, name=c.get("name", ""), unbekannt=0) for c in m.loads.get("cases", [])}
    for i in m.loads.get("items", []):
        o = out.setdefault(i["case"], dict(n=0, F=[0.0] * 3, P=[0.0] * 3, name="", unbekannt=0)); o["n"] += 1
        if i["dir"].startswith("M") or i["dir"][-1] not in "XYZ":
            continue
        k = "XYZ".index(i["dir"][-1])
        if i["kind"] == "surface":
            o["P"][k] += i["value"] * len(i["targets"]); continue
        if i["kind"] == "nodal":
            o["F"][k] += i["value"] * len(i["targets"])
        elif i["kind"] == "member":
            for t in i["targets"]:
                if i.get("dist") == "partial" and "a" in i:
                    o["F"][k] += i["value"] * (i["b"] - i["a"])
                elif t in mem and all(n in nm for n in mem[t]):
                    o["F"][k] += i["value"] * math.dist(nm[mem[t][0]], nm[mem[t][1]])
                else:
                    o["unbekannt"] += 1
        elif i["kind"] == "line":
            o["F"][k] += sum(i["value"] * math.dist(nm[ns[0]], nm[ns[-1]]) for ns in i.get("line_nodes", [])
                             if len(ns) >= 2 and ns[0] in nm and ns[-1] in nm)
    if flip:
        for o in out.values():
            for v in (o["F"], o["P"]):
                v[1], v[2] = -v[1], -v[2]
    return out


def compare_loads(a, b, flip):
    """Lastfälle über die Nummer im Namen zuordnen (LF3 ↔ LC3); F und P je Lastfall vergleichen (Toleranz 0,1 %)."""
    key = lambda s: (re.search(r"(\d+)$", str(s)) or [None, s])[1]
    A, B = load_resultants(a), load_resultants(b, flip)
    Bk = {key(k): (k, v) for k, v in B.items()}
    rel = lambda u, w: max(abs(x - y) for x, y in zip(u, w)) / (max(abs(x) for x in u + w) or 1.0)
    rows, ok = [], 0
    for k, v in sorted(A.items(), key=lambda t: int(key(t[0])) if str(key(t[0])).isdigit() else 0):
        kb, w = Bk.get(key(k), (None, None))
        if w is None:
            rows.append(dict(A=k, B=None, nA=v["n"], nB=None, FA=v["F"], FB=None, PA=v["P"], PB=None, relF=None, relP=None)); continue
        rf, rp = rel(v["F"], w["F"]), rel(v["P"], w["P"])
        ok += rf <= 0.001 and rp <= 0.001
        rows.append(dict(A=k, B=kb, nA=v["n"], nB=w["n"], FA=[round(x / 1e3, 2) for x in v["F"]], FB=[round(x / 1e3, 2) for x in w["F"]],
                         PA=[round(x / 1e3, 2) for x in v["P"]], PB=[round(x / 1e3, 2) for x in w["P"]], relF=round(rf, 6), relP=round(rp, 6)))
    return dict(faelle_A=len(A), faelle_B=len(B), gleich=ok, zeilen=rows)


def report_md(res):
    k, s, l = res["knoten"], res["staebe"], res["lager"]
    return "\n".join([
        f"# NSM-Vergleich – **{res['status']}**", "", f"- A: `{res['A']}`", f"- B: `{res['B']}`",
        f"- Toleranz {res['toleranz_m']} m · Koordinatentransformation B→A: {res['transformation']}", "",
        "| Objekt | A | B | zugeordnet | Bemerkung |", "|---|---|---|---|---|",
        f"| Knoten | {k['A']} | {k['B']} | {k['zugeordnet']} | max. Abweichung {k['max_abweichung_m']} m |",
        f"| Stäbe | {s['A']} | {s['B']} | {s['zugeordnet']} | ohne Partner {s['ohne_partner']}, Querschnittsname abweichend {s['querschnitt_abweichend']} |",
        f"| Lager | {l['A']} | {l['B']} | {l['gleich']} | gleicher Knoten + gleiche Fixierung |",
        f"| Flächen | {res['flaechen']['A']} | {res['flaechen']['B']} | {res['flaechen']['zugeordnet']} | gleiche Randknoten |", ""]
        + (["## Lasten je Lastfall", "",
            f"Lastfälle A {res['lasten']['faelle_A']} · B {res['lasten']['faelle_B']} · F und p gleich (≤ 0,1 %): **{res['lasten']['gleich']}**", "",
            "| A | B | Einträge A/B | ΣF A [kN] | ΣF B [kN] | Σp·n A [kN/m²] | Σp·n B [kN/m²] | rel. F / p |", "|---|---|---|---|---|---|---|---|"]
           + [f"| {z['A']} | {z['B']} | {z['nA']}/{z['nB']} | {z['FA']} | {z['FB']} | {z['PA']} | {z['PB']} | {z['relF']} / {z['relP']} |" for z in res["lasten"]["zeilen"]] + [""]
           if res.get("lasten") else [])) + "\n"


def main():
    ap = argparse.ArgumentParser(description="NEXUS CAD-Statik-Pipeline (NSM)")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("inspect"); p.add_argument("src"); p.add_argument("--tol", type=float, default=0.005)
    p.add_argument("--layers", help="Regex: nur passende DXF/DWG-Layer")
    p = sp.add_parser("convert"); p.add_argument("src"); p.add_argument("dst"); p.add_argument("--map")
    p.add_argument("--layers", help="Regex: nur passende DXF/DWG-Layer")
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
    if getattr(a, "layers", None):
        kw["layers"] = a.layers
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
