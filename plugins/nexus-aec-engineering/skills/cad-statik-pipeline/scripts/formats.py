"""
formats.py – Leser/Schreiber zwischen Dateiformaten und dem neutralen Modell (NSM, siehe nsm.py).

Lesen  : DXF (RFEM-Export + generisch) · IFC (Structural Analysis View + Achsen physischer Bauteile)
         RF5 (RFEM 5 über COM, immer an einer Kopie) · RF6 (ZIP+SQLite, nur Inventar, ohne API)
         RFEM-Tabellenexport CSV (1.1 Knoten.csv …) · NSM-CSV · JSON · SQLite · DWG (über externen Konverter)
Schreiben: JSON · CSV · SQLite (nsm.py) · DXF (RFEM-kompatible Layer) · RF5 (neues Modell über COM, nur SANDBOX)

Grundsätze: deterministisch (sortierte IDs, feste Toleranzen), Quelle wird nie verändert, jede
Unsicherheit wird als Befund in model.extra["hinweise"] festgehalten statt still korrigiert.
"""
from __future__ import annotations
import collections, glob, math, os, re, shutil, sqlite3, subprocess, sys, tempfile, zipfile
from nsm import Model, Node, Member, Support, Surface, new_meta, r, sha256_file, from_json, from_csv, from_sqlite

TOL = 0.005                                    # Fangradius Knoten [m]
HERE = os.path.dirname(os.path.abspath(__file__))
RF5_SCRIPTS = os.path.normpath(os.path.join(HERE, "..", "..", "rfem5-com", "scripts"))
MEMBER_TYPES = {0: "unknown", 1: "beam", 2: "rigid", 3: "rib", 4: "truss", 5: "truss_only_n", 6: "tension",
                7: "compression", 8: "buckling", 9: "cable", 10: "cable_on_pulleys", 11: "result_beam",
                12: "definable_stiffness", 17: "spring", 18: "null"}


# ------------------------------------------------------------------ Hilfen
class NodeIndex:
    """Raster-Hash für Knotenfang mit Toleranz (O(1) je Abfrage) – deterministisch."""
    def __init__(self, tol=TOL):
        self.tol, self.grid, self.nodes = tol, collections.defaultdict(list), []

    def _k(self, p):
        return tuple(int(math.floor(c / self.tol)) for c in p)

    def find(self, p):
        k, best = self._k(p), None
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for nid, q in self.grid.get((k[0] + dx, k[1] + dy, k[2] + dz), ()):
                        d = math.dist(p, q)
                        if d <= self.tol and (best is None or d < best[0]):
                            best = (d, nid)
        return best[1] if best else None

    def add(self, nid, p):
        self.grid[self._k(p)].append((nid, tuple(p)))

    def get_or_add(self, p):
        nid = self.find(p)
        if nid is None:
            nid = len(self.nodes) + 1
            self.nodes.append(Node(nid, r(p[0]), r(p[1]), r(p[2])))
            self.add(nid, p)
        return nid


def renumber(points):
    """Punkte deterministisch sortieren (x, y, z) und 1..n nummerieren."""
    return [Node(i + 1, r(p[0]), r(p[1]), r(p[2])) for i, p in enumerate(sorted(points, key=lambda p: (round(p[0], 6), round(p[1], 6), round(p[2], 6))))]


def expand_list(txt):
    """RFEM-Nummernliste '1-3,7' -> [1,2,3,7]"""
    out = []
    for part in str(txt or "").replace(" ", "").split(","):
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-")[:2]
            if a.isdigit() and b.isdigit():
                out += list(range(int(a), int(b) + 1))
        elif part.isdigit():
            out.append(int(part))
    return out


def norm_name(s):
    return (s or "").replace("(SLASH)", "/").strip()


# ------------------------------------------------------------------ DXF
def read_dxf(path, tol=TOL):
    import ezdxf
    from ezdxf import recover
    doc, auditor = recover.readfile(path)
    msp = doc.modelspace()
    hin, cnt = [], collections.Counter()
    for e in msp:
        cnt[(e.dxf.layer, e.dxftype())] += 1
    m = Model(meta=new_meta(path, "dxf", z_axis="up", dxf_version=doc.dxfversion,
                            insunits=doc.header.get("$INSUNITS"), audit_errors=len(auditor.errors)))
    rfem_style = any(l == "DL_NODES" for l, _ in cnt)
    if rfem_style:
        # RFEM-DXF-Export schreibt Koordinaten im RFEM-Modellsystem (Z-Richtung wie im Modell, meist nach unten)
        m.meta["z_axis"] = "unbekannt (RFEM-Modellsystem, meist down)"
        # Knoten = Würfel aus 12 achsparallelen Kanten (Kantenlänge s) bzw. POINTs auf DL_NODES.
        # Erkennung über die "untere Ecke": Punkt, von dem Kanten in +x, +y und +z ausgehen → Mitte = Ecke + s/2.
        # Robust auch bei sich berührenden/überlappenden Würfeln (dicht benachbarte Knoten).
        dirs, lens = collections.defaultdict(set), collections.Counter()
        for e in msp.query('LINE[layer=="DL_NODES"]'):
            a = tuple(round(c, 6) for c in e.dxf.start); b = tuple(round(c, 6) for c in e.dxf.end)
            lo, hi = (a, b) if a <= b else (b, a)
            d = [i for i in range(3) if abs(hi[i] - lo[i]) > 1e-9]
            if len(d) == 1:
                ax = d[0]
                if hi[ax] < lo[ax]:
                    lo, hi = hi, lo
                dirs[lo].add(ax); lens[round(abs(hi[ax] - lo[ax]), 6)] += 1
        s = lens.most_common(1)[0][0] if lens else 0.0
        # nur VOLLSTÄNDIGE Würfel (12/12 Kanten) – zwischen benachbarten Würfeln entstehen sonst Scheinecken
        E = {ax: NodeIndex(0.001) for ax in range(3)}        # Kantenanfänge je Richtung, 1 mm Fangradius
        for p, ds in dirs.items():
            for ax in ds:
                E[ax].add(0, p)
        need = [((0, 0, 0), 0), ((0, 0, 0), 1), ((0, 0, 0), 2), ((s, 0, 0), 1), ((s, 0, 0), 2), ((0, s, 0), 0),
                ((0, s, 0), 2), ((0, 0, s), 0), ((0, 0, s), 1), ((s, s, 0), 2), ((s, 0, s), 1), ((0, s, s), 0)]
        def complete(p):
            return all(E[ax].find(tuple(p[i] + d[i] for i in range(3))) is not None for d, ax in need)
        cand = [p for p, ds in dirs.items() if ds == {0, 1, 2}]
        pts = [tuple(c + s / 2 for c in p) for p in cand if complete(p)]
        if len(pts) < len(cand):
            hin.append(f"{len(cand) - len(pts)} unvollständige Scheinwürfel (zwischen Nachbarknoten) verworfen")
        if lens and len(lens) > 1:
            hin.append(f"DL_NODES-Kantenlängen uneinheitlich {dict(lens.most_common(3))} – Würfelgröße s={s}")
        pts += [tuple(e.dxf.location) for e in msp.query('POINT[layer=="DL_NODES"]')]
        dd, uniq = NodeIndex(0.002), []                  # Rundungsdubletten (Kanten 0.200001 m) zusammenfassen
        for p in sorted(pts):
            if dd.find(p) is None:
                dd.add(len(uniq), p); uniq.append(p)
        if len(uniq) < len(pts):
            hin.append(f"{len(pts) - len(uniq)} doppelt erkannte Knotenwürfel (Abstand < 2 mm) zusammengefasst")
        nodes = renumber(uniq)
        idx = NodeIndex(max(tol, 0.01))
        for n in nodes:
            idx.add(n.id, (n.x, n.y, n.z))
        idx.nodes = list(nodes)
        mid, unmatched = 0, 0
        for e in sorted(msp.query("LINE"), key=lambda e: (e.dxf.layer, tuple(e.dxf.start), tuple(e.dxf.end))):
            if "$" not in e.dxf.layer:
                continue
            sec, mat = (norm_name(x) for x in e.dxf.layer.split("$", 1))
            a, b = tuple(e.dxf.start), tuple(e.dxf.end)
            na, nb = idx.find(a), idx.find(b)
            if na is None or nb is None:
                unmatched += 1
                na, nb = idx.get_or_add(a), idx.get_or_add(b)
            mid += 1
            m.members.append(Member(mid, na, nb, sec, mat, "beam"))
        m.nodes = idx.nodes
        for e in msp.query('POINT[layer=="DL_NODAL_SUPPORT"]'):
            nid = idx.find(tuple(e.dxf.location))
            if nid:
                m.supports.append(Support(nid, "xyz"))
        if unmatched:
            hin.append(f"{unmatched} Stab-Endpunkte ohne Knotenwürfel – Knoten ergänzt")
        m.extra["dxf_konvention"] = "RFEM-Export (DL_NODES-Würfel, Stäbe auf Layer 'Querschnitt$Material')"
        m.extra["DL_TOPOLOGY_linien"] = cnt.get(("DL_TOPOLOGY", "LINE"), 0)
        circ = sum(v for (l, t), v in cnt.items() if t == "CIRCLE" and "$" in l)
        if circ:
            hin.append(f"{circ} CIRCLE auf Querschnitts-Layern (Darstellung, nicht als Stab gewertet)")
        if not any(cnt.get(("DL_NODAL_SUPPORT", t)) for t in ("POINT",)):
            hin.append("Lager im DXF nicht als POINT kodiert – Lagerbedingungen fehlen (aus RF5/IFC übernehmen)")
    else:
        # generisch: LINE/LWPOLYLINE/POLYLINE-Segmente -> Stäbe, Layer -> Querschnitt
        units = {1: 0.0254, 2: 0.3048, 4: 0.001, 5: 0.01, 6: 1.0, 14: 0.1}   # $INSUNITS → Meter
        k = units.get(m.meta["insunits"], 1.0)
        m.meta["length_scale_to_m"] = k
        idx, mid = NodeIndex(tol), 0
        skip = re.compile(r"(?i)(dim|bema|text|hatch|schraff|achs|axis|defpoints|^section$|^schnitt$|rahmen|frame_title)")
        segs = []
        for e in msp:
            if skip.search(e.dxf.layer):
                continue
            t = e.dxftype()
            if t == "LINE":
                segs.append((e.dxf.layer, tuple(e.dxf.start), tuple(e.dxf.end)))
            elif t in ("LWPOLYLINE", "POLYLINE"):
                pts = [tuple(p) for p in (e.get_points("xy") if t == "LWPOLYLINE" else [v.dxf.location for v in e.vertices])]
                z = e.dxf.elevation if t == "LWPOLYLINE" and e.dxf.hasattr("elevation") else 0.0
                pts = [(p[0], p[1], p[2] if len(p) > 2 else z) for p in pts]
                if e.closed:
                    pts.append(pts[0])
                segs += [(e.dxf.layer, pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
        segs = [(lay, tuple(c * k for c in a), tuple(c * k for c in b)) for lay, a, b in segs]
        segs, outl = _outlines_to_axes(segs, tol)          # Umriss-Rechtecke → Mittellinie / Quadrate → Punkt
        if outl["rechtecke"] or outl["quadrate"]:
            hin.append(f"Umriss-Modus: {outl['rechtecke']} Rechtecke → Mittellinien, {outl['quadrate']} Quadrate → Stützenpunkte "
                       f"(Layer {outl['layer']}); Höhe z aus Plan unbekannt")
        for lay, a, b in sorted(segs, key=lambda s: (s[0], s[1], s[2])):
            if b is None:                                  # Stützenpunkt aus Quadrat
                idx.get_or_add(a); continue
            if math.dist(a, b) <= tol:
                continue
            mid += 1
            m.members.append(Member(mid, idx.get_or_add(a), idx.get_or_add(b), norm_name(lay), "", "beam"))
        m.nodes = idx.nodes
        m.extra["dxf_konvention"] = "generisch (Linien/Polylinien = Stabachsen, Layer = Querschnitt)"
        hin.append("Material/Lager im generischen DXF nicht kodiert – nachpflegen (Mapping-Tabelle)")
        if k != 1.0:
            hin.append(f"$INSUNITS={m.meta['insunits']} → Koordinaten mit Faktor {k} in Meter umgerechnet")
        elif m.meta["insunits"] in (0, None):
            hin.append("$INSUNITS fehlt – Meter angenommen, Maßstab prüfen")
    m.extra["hinweise"] = hin
    return m


def _outlines_to_axes(segs, tol):
    """Je Layer: bilden ALLE Segmente geschlossene Rechtecke (Bauteilumrisse im Plan), werden sie ersetzt durch
    Mittellinie (längere Seite) bzw. – bei Quadraten (Stützenquerschnitt) – den Mittelpunkt (b=None)."""
    out, stat = [], dict(rechtecke=0, quadrate=0, layer=[])
    by = collections.defaultdict(list)
    for s in segs:
        by[s[0]].append(s)
    for lay, ss in sorted(by.items()):
        key = lambda p: tuple(round(c / tol) for c in p)
        adj = collections.defaultdict(list)
        for _, a, b in ss:
            adj[key(a)].append((a, b)); adj[key(b)].append((b, a))
        if not ss or len(ss) % 4 or any(len(v) != 2 for v in adj.values()):
            out += ss; continue
        seen, rects = set(), []
        for _, a, b in ss:                            # Zyklen über Endpunkte verfolgen
            if key(a) in seen:
                continue
            cyc, cur, prev = [a], b, a
            while key(cur) != key(a) and len(cyc) < 6:
                cyc.append(cur)
                nxt = [q for p, q in adj[key(cur)] if key(q) != key(prev)]
                prev, cur = cur, (nxt[0] if nxt else a)
            seen |= {key(p) for p in cyc}
            if len(cyc) != 4:
                rects = None; break
            e = [(cyc[i], cyc[(i + 1) % 4]) for i in range(4)]
            v = [tuple(q[j] - p[j] for j in range(3)) for p, q in e]
            if any(abs(sum(v[i][j] * v[(i + 1) % 4][j] for j in range(3))) > 1e-6 * (1 + math.hypot(*v[i]) * math.hypot(*v[(i + 1) % 4])) for i in range(4)):
                rects = None; break                   # kein rechter Winkel
            rects.append(e)
        if not rects:
            out += ss; continue
        stat["layer"].append(lay)
        for e in rects:
            l0, l1 = math.dist(*e[0]), math.dist(*e[1])
            mp = lambda s: tuple((s[0][j] + s[1][j]) / 2 for j in range(3))
            if abs(l0 - l1) <= tol:
                c = tuple((e[0][0][j] + e[2][0][j]) / 2 for j in range(3))
                out.append((lay, c, None)); stat["quadrate"] += 1
            else:
                short = (e[0], e[2]) if l0 < l1 else (e[1], e[3])
                out.append((lay, mp(short[0]), mp(short[1]))); stat["rechtecke"] += 1
    return out, stat


def write_dxf(m: Model, path):
    import ezdxf
    doc = ezdxf.new("R2013"); doc.header["$INSUNITS"] = 6
    msp = doc.modelspace(); nm = m.node_map()
    for name in ("DL_NODES", "DL_NODAL_SUPPORT"):
        doc.layers.add(name)
    for n in sorted(m.nodes, key=lambda n: n.id):
        msp.add_point((n.x, n.y, n.z), dxfattribs={"layer": "DL_NODES"})
    for x in sorted(m.members, key=lambda x: x.id):
        lay = f"{x.section or 'OHNE'}${x.material or 'OHNE'}".replace("/", "(SLASH)")
        if lay not in doc.layers:
            doc.layers.add(lay)
        a, b = nm[x.n1], nm[x.n2]
        msp.add_line((a.x, a.y, a.z), (b.x, b.y, b.z), dxfattribs={"layer": lay})
    for s in m.supports:
        n = nm[s.node]; msp.add_point((n.x, n.y, n.z), dxfattribs={"layer": "DL_NODAL_SUPPORT"})
    doc.saveas(path)
    return path


# ------------------------------------------------------------------ IFC
def read_ifc(path, tol=TOL):
    import ifcopenshell, ifcopenshell.geom, ifcopenshell.util.placement as up   # geom VOR open() laden (sonst leere Geometrie)
    f = ifcopenshell.open(path)
    m = Model(meta=new_meta(path, "ifc", z_axis="up", ifc_schema=f.schema))
    hin, idx = [], NodeIndex(tol)

    def mat_of(o):
        mat = getattr(o, "ObjectPlacement", None) and up.get_local_placement(o.ObjectPlacement)
        return mat

    def tf(o, xyz):
        M = mat_of(o)
        if M is None:
            return tuple(float(c) for c in xyz)
        x, y, z = (list(xyz) + [0.0])[:3]
        return tuple(float(M[i][0] * x + M[i][1] * y + M[i][2] * z + M[i][3]) for i in range(3))

    scale = 1.0
    for u in f.by_type("IfcSIUnit"):
        if u.UnitType == "LENGTHUNIT" and u.Prefix == "MILLI":
            scale = 0.001
    for u in f.by_type("IfcConversionBasedUnit"):
        if u.UnitType == "LENGTHUNIT":
            scale = float(u.ConversionFactor.ValueComponent.wrappedValue); hin.append(f"Längeneinheit {u.Name} → Faktor {scale}")
    m.meta["length_scale_to_m"] = scale

    def rel_name(o, kind):
        for rel in f.get_inverse(o):
            if kind == "mat" and rel.is_a("IfcRelAssociatesMaterial"):
                rm = rel.RelatingMaterial
                return getattr(rm, "Name", None) or (rm.is_a() if rm else "")
            if kind == "prof" and rel.is_a("IfcRelAssociatesProfileProperties") and rel.RelatingProfileProperties:
                return rel.RelatingProfileProperties.ProfileName or ""
        if kind == "prof":                       # IFC4: Profil über IfcMaterialProfileSet
            for rel in f.get_inverse(o):
                if rel.is_a("IfcRelAssociatesMaterial") and rel.RelatingMaterial.is_a("IfcMaterialProfileSetUsage"):
                    ps = rel.RelatingMaterial.ForProfileSet.MaterialProfiles
                    return ps[0].Profile.ProfileName if ps and ps[0].Profile else ""
        return ""

    pcs = f.by_type("IfcStructuralPointConnection")
    if pcs:
        # Knoten-ID aus Name ("Free node 12" / "Node 12") übernehmen, sonst laufend
        for i, p in enumerate(pcs):
            verts = [v for v in f.traverse(p.Representation) if v.is_a("IfcVertexPoint")] if p.Representation else []
            if not verts:
                continue
            c = tf(p, [x * scale for x in verts[0].VertexGeometry.Coordinates])
            mnum = re.search(r"(\d+)\s*$", p.Name or "")
            nid = int(mnum.group(1)) if mnum else 100000 + i
            if idx.find(c) is None:
                idx.nodes.append(Node(nid, r(c[0]), r(c[1]), r(c[2]))); idx.add(nid, c)
            cond = p.AppliedCondition
            if cond and cond.is_a("IfcBoundaryNodeCondition"):
                fx = ""
                for ax, att in (("x", "TranslationalStiffnessX"), ("y", "TranslationalStiffnessY"), ("z", "TranslationalStiffnessZ"),
                                ("X", "RotationalStiffnessX"), ("Y", "RotationalStiffnessY"), ("Z", "RotationalStiffnessZ")):
                    v = getattr(cond, att, None)
                    if v is None and ax.islower():                                    # IFC2X3: LinearStiffnessX/Y/Z
                        v = getattr(cond, "LinearStiffness" + att[-1], None)
                    val = getattr(v, "wrappedValue", v)
                    if val is True or (isinstance(val, (int, float)) and not isinstance(val, bool) and (val < 0 or val >= 1e10)):
                        fx += ax
                if fx:
                    m.supports.append(Support(nid, fx))
        mid = 0
        for c in f.by_type("IfcStructuralCurveMember"):
            verts = [v for v in f.traverse(c.Representation) if v.is_a("IfcVertexPoint")] if c.Representation else []
            if len(verts) < 2:
                continue
            a = tf(c, [x * scale for x in verts[0].VertexGeometry.Coordinates])
            b = tf(c, [x * scale for x in verts[-1].VertexGeometry.Coordinates])
            mnum = re.search(r"(\d+)\s*$", c.Name or ""); mid = int(mnum.group(1)) if mnum else mid + 1
            m.members.append(Member(mid, idx.get_or_add(a), idx.get_or_add(b), rel_name(c, "prof"), rel_name(c, "mat"),
                                    str(c.PredefinedType or "beam").lower()))
        sid = 0
        for s in f.by_type("IfcStructuralSurfaceMember"):
            verts = [v for v in f.traverse(s.Representation) if v.is_a("IfcVertexPoint")] if s.Representation else []
            ids = sorted({idx.get_or_add(tf(s, [x * scale for x in v.VertexGeometry.Coordinates])) for v in verts})
            sid += 1
            m.surfaces.append(Surface(sid, ids, float(s.Thickness) * scale if s.Thickness else None, rel_name(s, "mat")))
        m.nodes = idx.nodes
        def cnt(t):
            try:
                return len(f.by_type(t))
            except RuntimeError:                  # Entität im Schema nicht vorhanden (z. B. IFC2X3)
                return None
        m.extra["ifc_inhalt"] = {t: cnt(t) for t in ("IfcStructuralAnalysisModel", "IfcStructuralLoadGroup",
                                                     "IfcStructuralPointAction", "IfcStructuralLinearAction",
                                                     "IfcStructuralCurveAction", "IfcStructuralPlanarAction",
                                                     "IfcStructuralSurfaceAction", "IfcBoundaryNodeCondition")}
        m.extra["ifc_modus"] = "Structural Analysis View (Statikmodell)"
    else:
        # physisches Modell: Systemlinien aus 'Axis'-Darstellung von IfcBeam/IfcColumn/IfcMember
        mid, approx = 0, 0
        for o in sorted(f.by_type("IfcBeam") + f.by_type("IfcColumn") + f.by_type("IfcMember"), key=lambda o: o.GlobalId):
            rep = next((x for x in (o.Representation.Representations if o.Representation else [])
                        if x.RepresentationIdentifier == "Axis"), None)
            pts = [p.Coordinates for it in rep.Items if it.is_a("IfcPolyline") for p in it.Points] if rep else []
            if len(pts) >= 2:
                a = tf(o, [x * scale for x in pts[0]]); b = tf(o, [x * scale for x in pts[-1]])
            else:
                ab = _principal_axis(o, scale)          # Näherung: Achse des Extrusionsquaders (Weltkoordinaten, m)
                if not ab:
                    continue
                a, b = ab; approx += 1
            mid += 1
            m.members.append(Member(mid, idx.get_or_add(a), idx.get_or_add(b), rel_name(o, "prof"), rel_name(o, "mat"), o.is_a()[3:].lower()))
        if approx:
            hin.append(f"{approx} Stabachsen aus Volumenkörper-Hauptachse abgeleitet (Näherung, Systemlinie/Exzentrizität prüfen)")
        m.nodes = idx.nodes
        m.extra["ifc_modus"] = "physisches Modell (Achsen aus 'Axis'-Darstellung)"
        phys = {t: len(f.by_type(t)) for t in ("IfcBeam", "IfcColumn", "IfcMember", "IfcSlab", "IfcWall", "IfcBuildingElementProxy")}
        m.extra["ifc_bauteile"] = phys
        if not mid:
            hin.append("keine Statik-/Achsgeometrie – IFC als SAV (Statikmodell) exportieren oder Achsen nachbilden")
    m.extra["hinweise"] = hin
    return m


def _principal_axis(o, scale=1.0):
    """Systemlinie eines physischen Bauteils ohne Geometriekernel: IfcExtrudedAreaSolid mit Rechteck-/Kreisprofil →
    Quader → Achse durch die Mitte entlang der längsten Kante (Weltkoordinaten, m). Sonst None."""
    import numpy as np, ifcopenshell.util.placement as up
    body = next((r for r in (o.Representation.Representations if o.Representation else [])
                 if r.RepresentationIdentifier == "Body"), None)
    solid = next((i for i in (body.Items if body else []) if i.is_a("IfcExtrudedAreaSolid")), None)
    if solid is None:
        return None
    pr = solid.SweptArea
    if pr.is_a("IfcRectangleProfileDef"):
        hx, hy = pr.XDim / 2, pr.YDim / 2
    elif pr.is_a("IfcCircleProfileDef"):
        hx = hy = pr.Radius
    else:
        return None
    P2 = np.eye(3)
    if getattr(pr, "Position", None):                          # 2D-Lage des Profils
        loc = pr.Position.Location.Coordinates; ref = pr.Position.RefDirection.DirectionRatios if pr.Position.RefDirection else (1, 0)
        c, s = ref[0] / math.hypot(*ref[:2]), ref[1] / math.hypot(*ref[:2])
        P2 = np.array([[c, -s, loc[0]], [s, c, loc[1]], [0, 0, 1]])
    d = np.array(solid.ExtrudedDirection.DirectionRatios, float); d /= np.linalg.norm(d)
    corners = []
    for sx in (-hx, hx):
        for sy in (-hy, hy):
            q = P2 @ np.array([sx, sy, 1.0])
            for t in (0.0, solid.Depth):
                corners.append(np.array([q[0], q[1], 0.0]) + d * t)
    M = up.get_axis2placement(solid.Position) if solid.Position else np.eye(4)
    W = up.get_local_placement(o.ObjectPlacement) if o.ObjectPlacement else np.eye(4)
    v = np.array([(W @ M @ np.append(p, 1.0))[:3] * scale for p in corners])
    c = v.mean(axis=0); u = np.linalg.svd(v - c, full_matrices=False)[2][0]
    t = (v - c) @ u
    a, b = c + u * t.min(), c + u * t.max()
    if tuple(np.round(a, 6)) > tuple(np.round(b, 6)):
        a, b = b, a                                    # deterministische Richtung
    return tuple(float(x) for x in a), tuple(float(x) for x in b)


# ------------------------------------------------------------------ RF5 (COM)
def _rfem5():
    sys.path.insert(0, RF5_SCRIPTS)
    from rfem_connect import rfem_session, find_model
    return rfem_session, find_model


def read_rf5(path=None):
    """RF5 über COM lesen. path=None: aktives Modell (nur lesen). Sonst wird eine KOPIE geöffnet und wieder geschlossen."""
    rfem_session, find_model = _rfem5()
    copy = None
    if path:
        sb = os.path.join(tempfile.gettempdir(), "NSM_SANDBOX"); os.makedirs(sb, exist_ok=True)
        copy = os.path.join(sb, f"{sha256_file(path)[:12]}_{os.path.basename(path)}")
        shutil.copy2(path, copy)
    with rfem_session() as (app, R):
        mo = (find_model(app, copy) or app.OpenModel(copy)) if copy else app.GetActiveModel()
        try:
            d = mo.GetModelData()
            z = "up" if int(mo.GetGlobalZAxisOrientation()) == 1 else "down"
            m = Model(meta=new_meta(path or mo.GetPath(), "rf5", z_axis=z, rfem_version=app.GetVersion(),
                                    gelesen_aus="Kopie " + copy if copy else "aktives Modell"))
            m.nodes = [Node(n.No, r(n.X), r(n.Y), r(n.Z)) for n in d.GetNodes()]
            lines = {l.No: expand_list(l.NodeList) for l in d.GetLines()}
            mat_objs, cs_objs = list(d.GetMaterials()), list(d.GetCrossSections())
            mats = {x.No: x.Description for x in mat_objs}
            cs = {x.No: (x.Description, mats.get(x.MaterialNo, "")) for x in cs_objs}
            m.extra["rfem_bibliothek"] = dict(materials={x.Description: x.TextID for x in mat_objs},
                                              sections={x.Description: x.TextID for x in cs_objs})
            for x in d.GetMembers():
                ln = lines.get(x.LineNo, [])
                if len(ln) < 2:
                    continue
                sec, mat = cs.get(x.StartCrossSectionNo, ("", ""))
                m.members.append(Member(x.No, ln[0], ln[-1], sec, mat, MEMBER_TYPES.get(int(x.Type), str(int(x.Type)))))
            springs = 0
            for s in d.GetNodalSupports():
                fx = "".join(a for a, v in (("x", s.SupportConstantX), ("y", s.SupportConstantY), ("z", s.SupportConstantZ),
                                            ("X", s.RestraintConstantX), ("Y", s.RestraintConstantY), ("Z", s.RestraintConstantZ)) if v < 0)
                springs += sum(1 for v in (s.SupportConstantX, s.SupportConstantY, s.SupportConstantZ) if v > 0)
                for nid in expand_list(s.NodeList):
                    m.supports.append(Support(nid, fx))
            for sf in d.GetSurfaces():
                ids = sorted({n for ln in expand_list(sf.BoundaryLineList) for n in lines.get(ln, [])})
                m.surfaces.append(Surface(sf.No, ids, sf.Thickness.Constant, mats.get(sf.MaterialNo, "")))
            m.extra["hinweise"] = [f"{springs} Federlager-Komponenten (nicht als fest gewertet)"] if springs else []
            m.extra["zwischenknoten_polylinien"] = sum(1 for v in lines.values() if len(v) > 2)
        finally:
            if copy:
                mo.Close()
    return m


def write_rf5(m: Model, target, material_map=None, section_map=None, guard="SANDBOX"):
    """Neues RF5-Modell aus NSM anlegen (G2!) – nur in Ordner mit 'SANDBOX'. Unbekannte Querschnitte/Materialien →
    Platzhalter aus der Mapping-Tabelle (Befund wird zurückgegeben). Geometrie/Topologie 1:1, IDs übernommen."""
    if guard.lower() not in os.path.abspath(target).lower():
        raise PermissionError(f"Ziel muss '{guard}' im Pfad enthalten: {target}")
    rfem_session, _ = _rfem5()
    material_map = material_map or {}
    section_map = section_map or {}
    default_mat = material_map.get("*", "NameID|Baustahl S 235 JR@TypeID|STEEL@NormID|DIN EN 10025-2@Norm|DIN EN 10025-2:2005-04")
    default_sec = section_map.get("*", "RO 88.9x3.2")
    befunde = []
    os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
    with rfem_session() as (app, R):
        mo = app.CreateModel(os.path.splitext(os.path.basename(target))[0])
        d = mo.GetModelData()
        zdown = int(mo.GetGlobalZAxisOrientation()) == 0
        src_up = m.meta.get("z_axis") == "up"
        rot = src_up == zdown                     # Achsen unterschiedlich → Drehung 180° um X (y→−y, z→−z)
        def S(name, **kw):
            s = getattr(R, name)()
            for k, v in kw.items():
                setattr(s, k, v)
            return s
        mats = sorted({x.material for x in m.members}); secs = sorted({(x.section, x.material) for x in m.members})
        mat_no = {name: i + 1 for i, name in enumerate(mats)}
        sec_no = {key: i + 1 for i, key in enumerate(secs)}
        d.PrepareModification()
        try:
            for n in m.nodes:
                d.SetNode(S("Node", No=n.id, X=float(n.x), Y=float(-n.y if rot else n.y), Z=float(-n.z if rot else n.z)))
            for name, no in mat_no.items():
                tid = material_map.get(name)
                if not tid:
                    befunde.append(f"MATERIAL_PLATZHALTER:{name or '-'}")
                d.SetMaterial(S("Material", No=no, TextID=tid or default_mat, Comment=(name or "")[:60]))
            for (sec, mat), no in sec_no.items():
                desc = section_map.get(sec)
                if not desc:
                    befunde.append(f"QUERSCHNITT_PLATZHALTER:{sec or '-'}")
                desc = desc or default_sec
                kw = dict(TextID=desc) if "|" in desc else dict(Description=desc)   # Bibliotheks-TextID oder Bezeichnung
                d.SetCrossSection(S("CrossSection", No=no, MaterialNo=mat_no[mat], Comment=(sec or "")[:60], **kw))
            for x in m.members:
                d.SetLine(S("Line", No=x.id, NodeList=f"{x.n1},{x.n2}", Type=R.PolylineType))
                d.SetMember(S("Member", No=x.id, LineNo=x.id, Type=R.Beam, StartCrossSectionNo=sec_no[(x.section, x.material)],
                              EndCrossSectionNo=sec_no[(x.section, x.material)]))
            groups = collections.defaultdict(list)
            for s in m.supports:
                groups[s.fix].append(s.node)
            for i, (fx, nodes) in enumerate(sorted(groups.items())):
                g = lambda a: -1.0 if a in fx else 0.0
                d.SetNodalSupport(S("NodalSupport", No=i + 1, NodeList=",".join(map(str, sorted(nodes))),
                                    ReferenceSystem=R.GlobalSystemType, SupportConstantX=g("x"), SupportConstantY=g("y"),
                                    SupportConstantZ=g("z"), RestraintConstantX=g("X"), RestraintConstantY=g("Y"), RestraintConstantZ=g("Z")))
            d.FinishModification()
        except Exception:
            d.CancelModification(); raise
        if m.surfaces:
            befunde.append(f"FLAECHEN_NICHT_UEBERTRAGEN:{len(m.surfaces)}")
        mo.SetDescription(f"NSM-Import aus {m.meta.get('format')} {os.path.basename(str(m.meta.get('source')))} – Platzhalter prüfen")
        mo.Save(os.path.abspath(target))
        mo.Close()
    if rot:
        befunde.append("ACHSEN_GEDREHT: Quelle Z nach oben → RFEM Z nach unten, Drehung 180° um X (y_RFEM = −y, z_RFEM = −z)")
    return befunde


# ------------------------------------------------------------------ RF6 (ohne API: ZIP + SQLite, nur Inventar)
def read_rf6(path):
    z = zipfile.ZipFile(path)
    names = {i.filename: i.file_size for i in z.infolist()}
    fmt = z.read("format.txt").decode("utf-8", "replace").split() if "format.txt" in names else []
    m = Model(meta=new_meta(path, "rf6", z_axis="unbekannt", rf6_format=fmt, status="INVENTAR_OHNE_GEOMETRIE"))
    inv = {}
    if "model.db" in names:
        tmp = tempfile.mkdtemp(prefix="nsm_rf6_")
        try:
            z.extract("model.db", tmp)
            con = sqlite3.connect(f"file:{os.path.join(tmp, 'model.db')}?mode=ro", uri=True)
            for t in ("Node", "Line", "Member", "Surface", "Material", "Section", "NodalSupport", "LoadCase"):
                try:
                    inv[t] = con.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
                except sqlite3.Error:
                    inv[t] = None
            inv["tabellen"] = con.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
            con.close()
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    m.extra = dict(rf6_inventar=inv, zip_inhalt={k: v for k, v in names.items() if not k.endswith("/")},
                   hinweise=["RF6-Datenbankschema ist nicht dokumentiert: nur Zählung/Fingerabdruck. Geometrie über "
                             "RFEM-6-API (dlubal.api), IFC- oder SAF-Export holen."])
    return m


# ------------------------------------------------------------------ RFEM-Tabellenexport (CSV, cp1252)
def read_rfem_csv(folder):
    def rows(name):
        p = os.path.join(folder, name)
        if not os.path.exists(p):
            return []
        raw = open(p, "rb").read().decode("cp1252")
        out = []
        for line in raw.splitlines()[2:]:
            c = line.split(";")
            if c and c[0].strip().isdigit() and sum(1 for x in c if x.strip()) >= 2:
                out.append(c)
        return out
    m = Model(meta=new_meta(folder, "rfem_csv", z_axis="unbekannt (RFEM-Standard: down)"))
    m.meta["source_files"] = {f: sha256_file(os.path.join(folder, f)) for f in sorted(os.listdir(folder))
                              if f[:2] in ("1.", "2.") and f.endswith(".csv")}
    m.nodes = [Node(int(c[0]), r(c[4]), r(c[5]), r(c[6])) for c in rows("1.1 Knoten.csv") if len(c) > 6 and c[4].strip()]
    lines = {int(c[0]): expand_list(c[2]) for c in rows("1.2 Linien.csv") if len(c) > 2}
    mats = {int(c[0]): c[1].strip() for c in rows("1.3 Materialien.csv") if len(c) > 1}
    cs = {int(c[0]): (c[1].strip(), mats.get(int(c[2]) if c[2].strip().isdigit() else 0, "")) for c in rows("1.13 Querschnitte.csv") if len(c) > 2}
    typ = {"Seilstab": "cable", "Balkenstab": "beam", "Fachwerkstab": "truss", "Starrstab": "rigid", "Zugstab": "tension"}
    for c in rows("1.17 Stäbe.csv"):
        ln = lines.get(int(c[1]) if c[1].strip().isdigit() else -1, [])
        if len(ln) >= 2:
            sec, mat = cs.get(int(c[3]) if c[3].strip().isdigit() else -1, ("", ""))
            m.members.append(Member(int(c[0]), ln[0], ln[-1], sec, mat, typ.get(c[2].strip(), c[2].strip().lower())))
    for c in rows("1.7 Knotenlager.csv"):
        if len(c) > 9 and c[1].strip():
            fx = "".join(a for a, v in zip("xyzXYZ", c[4:10]) if v.strip() == "+")
            m.supports += [Support(n, fx) for n in expand_list(c[1])]
    m.extra["hinweise"] = ["Lager: '+' = fest; Federwerte/Achsensysteme nicht ausgewertet", "Z-Richtung aus RFEM-Modell bestätigen"]
    return m


# ------------------------------------------------------------------ DWG (externer Konverter)
def read_dwg(path):
    ver = open(path, "rb").read(6).decode("ascii", "replace")
    conv = glob.glob(r"C:\Program Files\ODA\*\ODAFileConverter.exe") or glob.glob(r"C:\Program Files*\LibreDWG*\dwg2dxf.exe")
    if not conv:
        raise RuntimeError(f"DWG ({ver}) erkannt, aber kein Konverter installiert. Optionen: ODA File Converter "
                           "(nur nicht-kommerziell ohne ODA-Mitgliedschaft) oder GNU LibreDWG dwg2dxf (GPL-3). "
                           "Alternativ in CAD als DXF R2013 exportieren.")
    out = tempfile.mkdtemp(prefix="nsm_dwg_")
    if conv[0].lower().endswith("odafileconverter.exe"):
        subprocess.run([conv[0], os.path.dirname(path), out, "ACAD2013", "DXF", "0", "1", os.path.basename(path)], check=True, timeout=600)
        dxf = os.path.join(out, os.path.splitext(os.path.basename(path))[0] + ".dxf")
    else:
        dxf = os.path.join(out, "out.dxf")
        subprocess.run([conv[0], "-o", dxf, path], check=True, timeout=600)
    m = read_dxf(dxf)
    m.meta.update(format="dwg", dwg_version=ver, source=os.path.abspath(path), source_sha256=sha256_file(path), konverter=conv[0])
    return m


# ------------------------------------------------------------------ Dispatcher
def load(path, **kw) -> Model:
    p = path.lower()
    if os.path.isdir(path):
        if os.path.exists(os.path.join(path, "nodes.csv")):
            return from_csv(path)
        if os.path.exists(os.path.join(path, "1.1 Knoten.csv")):
            return read_rfem_csv(path)
        raise ValueError(f"Ordner ohne bekannte CSV-Struktur: {path}")
    if p.endswith(".json"):
        return from_json(path)
    if p.endswith((".sqlite", ".db", ".nsm.db")):
        return from_sqlite(path)
    if p.endswith(".dxf"):
        return read_dxf(path, **kw)
    if p.endswith(".dwg"):
        return read_dwg(path)
    if p.endswith(".ifc"):
        return read_ifc(path, **kw)
    if p.endswith(".rf5"):
        return read_rf5(path)
    if p.endswith(".rf6"):
        return read_rf6(path)
    raise ValueError(f"Format nicht unterstützt: {path}")
