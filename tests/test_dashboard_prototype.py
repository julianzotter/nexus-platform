import json, shutil, subprocess, unittest
from pathlib import Path

DIR = Path(__file__).resolve().parents[1] / "prototypes" / "nexus-dashboard-v3"


def node(code):
    out = subprocess.run(["node", "-e", code], capture_output=True, text=True, check=True, cwd=DIR)
    return json.loads(out.stdout)


@unittest.skipUnless(shutil.which("node"), "node not available")
class DashboardPrototype(unittest.TestCase):
    def test_syntax_valid(self):
        for f in ("ec5_solver.js", "osr9_mmr.js"):
            subprocess.run(["node", "--check", f], check=True, cwd=DIR)

    def test_material_drives_constants_and_gate(self):
        r = node("const {ec5Buckling:f}=require('./ec5_solver');"
                 "const a={b:100,h:100,L:3000,N:20};"
                 "console.log(JSON.stringify([f({...a,material:'C24'}),f({...a,material:'GL24h'})]))")
        self.assertNotEqual(r[0]["fc0d"], r[1]["fc0d"])
        self.assertNotEqual(r[0]["kc"], r[1]["kc"])

    def test_gate_can_fail_and_pass(self):
        r = node("const {ec5Buckling:f}=require('./ec5_solver');"
                 "const a={material:'C24',b:100,h:100,L:3000};"
                 "console.log(JSON.stringify([f({...a,N:5}),f({...a,N:200})]))")
        self.assertEqual(r[0]["gate"], "PASS")
        self.assertEqual(r[1]["gate"], "FAIL")
        self.assertGreater(r[1]["utilization"], 1)

    def test_mmr_prefers_diverse(self):
        r = node("const {mmrSelect}=require('./osr9_mmr');"
                 "const it=[{id:'a',relevance:1,vec:[1,0]},{id:'b',relevance:.95,vec:[1,0]},{id:'c',relevance:.8,vec:[0,1]}];"
                 "console.log(JSON.stringify(mmrSelect(it,2,0.5).map(x=>x.id)))")
        self.assertEqual(r, ["a", "c"])


if __name__ == "__main__":
    unittest.main()
