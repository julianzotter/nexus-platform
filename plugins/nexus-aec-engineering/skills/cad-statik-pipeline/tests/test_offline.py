"""Offline-Regressionstests der CAD-Statik-Pipeline – ohne RFEM, ohne Netzwerk, ohne Kundendaten.

  python -m pytest tests/test_offline.py -q      (oder: python tests/test_offline.py)
"""
import json, os, sys, tempfile, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import nsm                                        # noqa: E402
from nsm import Model, Node, Member, Support, new_meta   # noqa: E402
import formats, pipeline                          # noqa: E402

TEMPLATE = os.path.join(HERE, "..", "templates", "beispiel_fachwerk.nsm.json")


def fachwerk():
    """Pratt-Fachwerk 4 Felder à 3 m, Höhe 3 m (Vorlage – identisch mit templates/beispiel_fachwerk.nsm.json)."""
    nodes = [Node(i + 1, 3.0 * i, 0.0, 0.0) for i in range(5)] + [Node(6 + i, 3.0 * (i + 1), 0.0, 3.0) for i in range(3)]
    e = [(1, 2), (2, 3), (3, 4), (4, 5), (6, 7), (7, 8), (1, 6), (8, 5), (2, 6), (3, 7), (4, 8), (6, 3), (8, 3)]
    mem = [Member(i + 1, a, b, "RO 88.9x3.2" if b <= 5 or a >= 6 else "RO 76.1x3.2", "S235", "truss") for i, (a, b) in enumerate(e)]
    return Model(meta=new_meta(None, "synthetisch", z_axis="up"), nodes=nodes, members=mem,
                 supports=[Support(1, "xyz"), Support(5, "yz")])


class Roundtrip(unittest.TestCase):
    def setUp(self):
        self.m = fachwerk(); self.tmp = tempfile.mkdtemp()

    def test_validate_clean(self):
        self.assertEqual([f for f in self.m.validate() if not f.startswith("INFO")], [])

    def test_json_csv_sqlite_identical_fingerprint(self):
        fp = self.m.fingerprint()
        j = nsm.from_json(nsm.to_json(self.m, os.path.join(self.tmp, "a.json")))
        c = nsm.from_csv(nsm.to_csv(self.m, os.path.join(self.tmp, "csv")))
        s = nsm.from_sqlite(nsm.to_sqlite(self.m, os.path.join(self.tmp, "a.sqlite")))
        self.assertEqual({fp}, {j.fingerprint(), c.fingerprint(), s.fingerprint()})

    def test_sqlite_view_lengths(self):
        import sqlite3
        p = nsm.to_sqlite(self.m, os.path.join(self.tmp, "b.sqlite"))
        L = sorted(round(x[0], 6) for x in sqlite3.connect(p).execute("SELECT length_m FROM member_geometry"))
        self.assertEqual(L.count(3.0), 9)                 # 4 UG + 2 OG + 3 Pfosten
        self.assertEqual(L.count(round(18 ** 0.5, 6)), 4) # 4 Diagonalen

    def test_dxf_roundtrip_compare_pass(self):
        p = formats.write_dxf(self.m, os.path.join(self.tmp, "f.dxf"))
        back = formats.read_dxf(p)
        res = pipeline.compare(self.m, back)
        self.assertEqual(res["status"], "PASS", res)
        self.assertEqual(len(back.supports), 2)            # Lagerort bleibt erhalten, Fixierung kodiert DXF nicht

    def test_compare_detects_shift_and_flip(self):
        moved = fachwerk(); moved.nodes[0].x += 0.05
        self.assertEqual(pipeline.compare(self.m, moved)["status"], "ABWEICHUNG")
        flipped = fachwerk(); flipped.meta["z_axis"] = "down"       # RFEM-System: Drehung 180° um X
        for n in flipped.nodes:
            n.y, n.z = -n.y + 1.0, -n.z                               # +1.0 in y: Drehung, nicht Spiegelung prüfen
        self.assertEqual(pipeline.compare(self.m, flipped)["status"], "ABWEICHUNG")
        for n in flipped.nodes:
            n.y -= 1.0
        r = pipeline.compare(self.m, flipped)
        self.assertTrue(r["z_gespiegelt"]); self.assertEqual(r["status"], "PASS")

    def test_validate_finds_broken_topology(self):
        bad = fachwerk(); bad.members.append(Member(99, 1, 42)); bad.members.append(Member(100, 3, 3))
        f = bad.validate()
        self.assertIn("STAB_OHNE_KNOTEN:99", f); self.assertIn("STAB_NULLLAENGE:100", f)

    def test_template_matches_generator(self):
        self.assertEqual(nsm.from_json(TEMPLATE).fingerprint(), self.m.fingerprint())

    def test_expand_list(self):
        self.assertEqual(formats.expand_list("1-3, 7,9-10"), [1, 2, 3, 7, 9, 10])

    def test_loads_roundtrip_and_resultants(self):
        m = fachwerk()
        m.loads = {"cases": [dict(id="LF1", name="Test", category=1)],
                   "items": [dict(case="LF1", kind="nodal", targets=[7], dir="Z", value=-10000.0, dist="uniform", note=""),
                             dict(case="LF1", kind="member", targets=[5, 6], dir="Z", value=-2000.0, dist="uniform", note=""),
                             dict(case="LF1", kind="member", targets=[1], dir="Z", value=-1000.0, dist="partial", a=1.0, b=2.5, note="")]}
        F = pipeline.load_resultants(m)["LF1"]["F"]
        self.assertAlmostEqual(F[2], -10000 - 2000 * 6 - 1000 * 1.5)        # 2 Obergurtstäbe à 3 m, Teillast 1,5 m
        for back in (nsm.from_json(nsm.to_json(m, os.path.join(self.tmp, "l.json"))),):
            self.assertEqual(back.loads["items"][2]["a"], 1.0)
            self.assertEqual(pipeline.compare(m, back)["lasten"]["gleich"], 1)
        c = nsm.from_csv(nsm.to_csv(m, os.path.join(self.tmp, "lcsv")))
        self.assertEqual(len(c.loads["items"]), 3)

    def test_rotation_applies_to_loads(self):
        m = fachwerk(); m.loads = {"cases": [dict(id="LF1")], "items": [dict(case="LF1", kind="nodal", targets=[7], dir="Z", value=-5.0, dist="uniform")]}
        r = pipeline.load_resultants(m, flip=True)["LF1"]["F"]
        self.assertEqual(r[2], 5.0)

    def test_duplicate_coordinates_flagged(self):
        m = fachwerk(); m.nodes.append(Node(99, 0.0, 0.0, 0.0))
        self.assertTrue(any(f.startswith("DOPPELTE_KOORDINATEN:1=99") for f in m.validate()))

    def test_chain_polygon(self):
        self.assertEqual(formats._chain([[1, 2], [3, 2], [3, 4], [4, 1]]), [1, 2, 3, 4])


if __name__ == "__main__":
    unittest.main(verbosity=2)
