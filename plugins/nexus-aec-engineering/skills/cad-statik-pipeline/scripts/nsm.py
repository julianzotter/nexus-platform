"""
nsm.py – NEXUS Neutral Structural Model (NSM) v0.1: ein einziges, formatunabhängiges Stabwerks-Datenmodell.

Alle Leser (DXF, IFC, RF5, RF6, CSV, SQLite, JSON) liefern ein NSM, alle Schreiber nehmen ein NSM.
Einheiten intern immer SI: m, N, Nm. Achse: meta.z_axis = "up" | "down" (wie in der Quelle).
Deterministisch: sortierte Ausgabe, Koordinaten auf 1e-6 m gerundet, Fingerabdruck über die Geometrie.

Nur Standardbibliothek (json, csv, sqlite3, hashlib).
"""
from __future__ import annotations
import csv, datetime as dt, hashlib, json, os, sqlite3
from dataclasses import dataclass, field, asdict

SCHEMA = "nexus.nsm/0.1"
ROUND = 6                                     # Nachkommastellen für Koordinaten [m]


@dataclass
class Node:
    id: int
    x: float
    y: float
    z: float


@dataclass
class Member:
    id: int
    n1: int
    n2: int
    section: str = ""
    material: str = ""
    type: str = "beam"                         # beam | cable | truss | rigid | ...


@dataclass
class Support:
    node: int
    fix: str = "xyz"                           # Freiheitsgrade fest: Teilmenge von "xyz" + "XYZ" (Rotationen)


@dataclass
class Surface:
    id: int
    nodes: list = field(default_factory=list)
    thickness: float | None = None
    material: str = ""


@dataclass
class Model:
    meta: dict = field(default_factory=dict)
    nodes: list = field(default_factory=list)
    members: list = field(default_factory=list)
    supports: list = field(default_factory=list)
    surfaces: list = field(default_factory=list)
    # Lasten (SI, globales System der Quelle): {"cases": [{id, name, category}],
    #   "items": [{case, kind: nodal|member|line|surface, targets: [ids], dir: X|Y|Z|PX|PY|PZ|MX|MY|MZ, value, dist, note}]}
    #   value in N (nodal), Nm (nodal M*), N/m (member/line), N/m² (surface); P* = projizierte Richtung
    loads: dict = field(default_factory=lambda: {"cases": [], "items": []})
    extra: dict = field(default_factory=dict)  # formatspezifische Zusatzinfos (Zählungen, Rohdaten-Hinweise)

    # ---------- Hilfen ----------
    def node_map(self):
        return {n.id: n for n in self.nodes}

    def summary(self):
        return dict(nodes=len(self.nodes), members=len(self.members), supports=len(self.supports),
                    surfaces=len(self.surfaces), sections=len({m.section for m in self.members if m.section}),
                    materials=len({m.material for m in self.members if m.material}),
                    load_cases=len(self.loads.get("cases", [])), load_items=len(self.loads.get("items", [])))

    def fingerprint(self):
        """SHA-256 über sortierte, gerundete Geometrie+Topologie (unabhängig von Nummerierung der Quelle nicht!)."""
        h = hashlib.sha256()
        for n in sorted(self.nodes, key=lambda n: n.id):
            h.update(f"N{n.id}:{n.x:.{ROUND}f},{n.y:.{ROUND}f},{n.z:.{ROUND}f};".encode())
        for m in sorted(self.members, key=lambda m: m.id):
            h.update(f"M{m.id}:{m.n1}-{m.n2}:{m.section}:{m.material};".encode())
        return h.hexdigest()

    def validate(self):
        """Plausibilitätsprüfung – liefert Liste von Befunden (leer = ok)."""
        f, ids = [], set()
        for n in self.nodes:
            if n.id in ids:
                f.append(f"DOPPELTE_KNOTENNR:{n.id}")
            ids.add(n.id)
            if any(v != v or abs(v) > 1e6 for v in (n.x, n.y, n.z)):
                f.append(f"KOORDINATE_UNGUELTIG:{n.id}")
        for m in self.members:
            if m.n1 not in ids or m.n2 not in ids:
                f.append(f"STAB_OHNE_KNOTEN:{m.id}")
            elif m.n1 == m.n2:
                f.append(f"STAB_NULLLAENGE:{m.id}")
        for s in self.supports:
            if s.node not in ids:
                f.append(f"LAGER_OHNE_KNOTEN:{s.node}")
        seen = {}
        for n in sorted(self.nodes, key=lambda n: n.id):            # koordinatengleiche Knoten (RFEM fasst sie zusammen)
            k = (round(n.x, 4), round(n.y, 4), round(n.z, 4))
            if k in seen:
                f.append(f"DOPPELTE_KOORDINATEN:{seen[k]}={n.id}")
            seen.setdefault(k, n.id)
        used = {m.n1 for m in self.members} | {m.n2 for m in self.members}
        free = len(ids - used - {s.node for s in self.supports} - {k for sf in self.surfaces for k in sf.nodes})
        if free:
            f.append(f"INFO_FREIE_KNOTEN:{free}")
        return f


def new_meta(source, fmt, z_axis="up", **kw):
    meta = dict(schema=SCHEMA, source=os.path.abspath(source) if source else None, format=fmt,
                units=dict(length="m", force="N", moment="Nm"), z_axis=z_axis,
                created=dt.datetime.now().astimezone().isoformat(timespec="seconds"))
    if source and os.path.isfile(source):
        meta["source_sha256"] = sha256_file(source)
        meta["source_bytes"] = os.path.getsize(source)
    meta.update(kw)
    return meta


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def r(v):
    return round(float(v), ROUND)


# ---------------------------------------------------------------- JSON
def to_json(m: Model, path):
    d = dict(meta=m.meta, summary=m.summary(), fingerprint=m.fingerprint(), findings=m.validate(),
             nodes=[asdict(n) for n in sorted(m.nodes, key=lambda n: n.id)],
             members=[asdict(x) for x in sorted(m.members, key=lambda x: x.id)],
             supports=[asdict(s) for s in sorted(m.supports, key=lambda s: s.node)],
             surfaces=[asdict(s) for s in sorted(m.surfaces, key=lambda s: s.id)], loads=m.loads, extra=m.extra)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    return path


def from_json(path) -> Model:
    d = json.load(open(path, encoding="utf-8"))
    if not str(d.get("meta", {}).get("schema", "")).startswith("nexus.nsm/"):
        raise ValueError(f"kein NSM-JSON: {path}")
    return Model(meta=d["meta"], nodes=[Node(**n) for n in d["nodes"]], members=[Member(**x) for x in d["members"]],
                 supports=[Support(**s) for s in d.get("supports", [])],
                 surfaces=[Surface(**s) for s in d.get("surfaces", [])],
                 loads=d.get("loads") or {"cases": [], "items": []}, extra=d.get("extra", {}))


# ---------------------------------------------------------------- CSV (neutral, Semikolon, UTF-8)
def to_csv(m: Model, folder):
    os.makedirs(folder, exist_ok=True)
    def w(name, head, rows):
        with open(os.path.join(folder, name), "w", newline="", encoding="utf-8") as f:
            c = csv.writer(f, delimiter=";"); c.writerow(head); c.writerows(rows)
    w("nodes.csv", ["id", "x_m", "y_m", "z_m"], [(n.id, n.x, n.y, n.z) for n in sorted(m.nodes, key=lambda n: n.id)])
    w("members.csv", ["id", "n1", "n2", "section", "material", "type"],
      [(x.id, x.n1, x.n2, x.section, x.material, x.type) for x in sorted(m.members, key=lambda x: x.id)])
    w("supports.csv", ["node", "fix"], [(s.node, s.fix) for s in sorted(m.supports, key=lambda s: s.node)])
    w("surfaces.csv", ["id", "nodes", "thickness_m", "material"],
      [(s.id, " ".join(map(str, s.nodes)), "" if s.thickness is None else s.thickness, s.material) for s in sorted(m.surfaces, key=lambda s: s.id)])
    w("load_cases.csv", ["id", "name", "category"], [(c["id"], c.get("name", ""), c.get("category", "")) for c in m.loads.get("cases", [])])
    w("load_items.csv", ["case", "kind", "targets", "dir", "value", "dist", "a_m", "b_m", "line_nodes", "note"],
      [(i["case"], i["kind"], " ".join(map(str, i["targets"])), i["dir"], i["value"], i.get("dist", "uniform"),
        i.get("a", ""), i.get("b", ""), "|".join(" ".join(map(str, ln)) for ln in i.get("line_nodes", [])), i.get("note", ""))
       for i in m.loads.get("items", [])])
    with open(os.path.join(folder, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(m.meta, f, ensure_ascii=False, indent=1)
    return folder


def from_csv(folder) -> Model:
    def rd(name):
        p = os.path.join(folder, name)
        if not os.path.exists(p):
            return []
        with open(p, encoding="utf-8") as f:
            return list(csv.DictReader(f, delimiter=";"))
    meta = json.load(open(os.path.join(folder, "meta.json"), encoding="utf-8")) if os.path.exists(
        os.path.join(folder, "meta.json")) else new_meta(None, "csv")
    return Model(meta=meta,
                 nodes=[Node(int(a["id"]), r(a["x_m"]), r(a["y_m"]), r(a["z_m"])) for a in rd("nodes.csv")],
                 members=[Member(int(a["id"]), int(a["n1"]), int(a["n2"]), a["section"], a["material"], a["type"])
                          for a in rd("members.csv")],
                 supports=[Support(int(a["node"]), a["fix"]) for a in rd("supports.csv")],
                 surfaces=[Surface(int(a["id"]), [int(x) for x in a["nodes"].split()],
                                   float(a["thickness_m"]) if a["thickness_m"] else None, a["material"]) for a in rd("surfaces.csv")],
                 loads={"cases": [dict(id=a["id"], name=a["name"], category=a["category"]) for a in rd("load_cases.csv")],
                        "items": [_load_item(a) for a in rd("load_items.csv")]})


def _load_item(a):
    it = dict(case=a["case"], kind=a["kind"], targets=[int(x) for x in a["targets"].split()], dir=a["dir"],
              value=float(a["value"]), dist=a["dist"], note=a.get("note", ""))
    if a.get("a_m"):
        it["a"], it["b"] = float(a["a_m"]), float(a["b_m"])
    if a.get("line_nodes"):
        it["line_nodes"] = [[int(x) for x in s.split()] for s in a["line_nodes"].split("|")]
    return it


# ---------------------------------------------------------------- SQLite (abfragbar, z. B. für Agenten/Dashboards)
DDL = """
CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE nodes(id INTEGER PRIMARY KEY, x REAL, y REAL, z REAL);
CREATE TABLE members(id INTEGER PRIMARY KEY, n1 INTEGER REFERENCES nodes(id), n2 INTEGER REFERENCES nodes(id),
                     section TEXT, material TEXT, type TEXT);
CREATE TABLE supports(node INTEGER REFERENCES nodes(id), fix TEXT);
CREATE VIEW member_geometry AS
  SELECT m.id, m.section, m.material, m.type,
         a.x AS x1, a.y AS y1, a.z AS z1, b.x AS x2, b.y AS y2, b.z AS z2,
         sqrt((b.x-a.x)*(b.x-a.x)+(b.y-a.y)*(b.y-a.y)+(b.z-a.z)*(b.z-a.z)) AS length_m
  FROM members m JOIN nodes a ON a.id=m.n1 JOIN nodes b ON b.id=m.n2;
"""


def to_sqlite(m: Model, path):
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(path)
    con.executescript(DDL)
    con.executemany("INSERT INTO meta VALUES(?,?)", [(k, json.dumps(v, ensure_ascii=False)) for k, v in m.meta.items()]
                    + [("fingerprint", json.dumps(m.fingerprint()))])
    con.executemany("INSERT INTO nodes VALUES(?,?,?,?)", [(n.id, n.x, n.y, n.z) for n in m.nodes])
    con.executemany("INSERT INTO members VALUES(?,?,?,?,?,?)",
                    [(x.id, x.n1, x.n2, x.section, x.material, x.type) for x in m.members])
    con.executemany("INSERT INTO supports VALUES(?,?)", [(s.node, s.fix) for s in m.supports])
    con.commit(); con.close()
    return path


def from_sqlite(path) -> Model:
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    meta = {k: json.loads(v) for k, v in con.execute("SELECT key,value FROM meta") if k != "fingerprint"}
    m = Model(meta=meta,
              nodes=[Node(*row) for row in con.execute("SELECT id,x,y,z FROM nodes ORDER BY id")],
              members=[Member(*row) for row in con.execute("SELECT id,n1,n2,section,material,type FROM members ORDER BY id")],
              supports=[Support(*row) for row in con.execute("SELECT node,fix FROM supports ORDER BY node")])
    con.close()
    return m
