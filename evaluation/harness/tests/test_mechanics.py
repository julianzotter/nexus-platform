import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import evaluate, jsonschema
SCHEMA = json.loads((ROOT / "schemas/eval_run.schema.json").read_text())
CASES = {json.loads(l)["case_id"]: json.loads(l) for l in (ROOT / "evals/cases.jsonl").read_text().splitlines()}

def _run(cid): 
    r = evaluate.run_case(CASES[cid], "T"); jsonschema.validate(r, SCHEMA); return r

def test_m1_happy_path():
    r = _run("M1"); assert r["status"] == "PASS" and r["refinements"] == 0 and r["deltas"] == 0
    assert all(v == "PASS" for v in r["gates"].values())

def test_m2_fault_injection():
    r = _run("M2"); assert r["status"] == "PASS" and r["refinements"] == 1 and r["deltas"] == 1

def test_m3_source_conflict():
    r = _run("M3"); assert r["status"] == "SOURCE_CONFLICT" and r["refinements"] == 3
    assert r["escalation"] == "HUMAN_GATE" and r["auto_apply"] is False

def test_determinism():
    a = [_run(c) for c in CASES]; b = [_run(c) for c in CASES]
    strip = lambda r: {k: v for k, v in r.items() if k not in ("run_id", "timestamp")}
    assert [strip(x) for x in a] == [strip(x) for x in b]
