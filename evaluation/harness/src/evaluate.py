"""Bounded loop: OBSERVE->EVALUATE->REFINE(<=3)->STOP. Deterministic stub solver."""
from __future__ import annotations
import hashlib, json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import gates
MAX_REFINEMENTS = 3

def input_hash(inp: dict) -> str:
    return hashlib.sha256(json.dumps(inp, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def stub_solve(inp: dict, refinement: int) -> str | None:
    """Deterministic stand-in for the LLM. refinement=1 fixes a unit fault once."""
    if "sources" in inp:
        return None if inp.get("authority_rule") is None else str(inp["sources"][0]["k"])
    f, fu = gates.parse_qty(inp["F"]); l, _ = gates.parse_qty(inp["L"])
    if refinement >= 1 and inp.get("injected_fault", "").startswith("unit"):
        f = f / 1000.0  # one delta: N->kN correction
    return f"{f * l / 4:.1f} kNm"

def run_case(case: dict, run_id: str) -> dict:
    inp, exp = case["input"], case["expected"]
    rec = {"run_id": run_id, "case_id": case["case_id"], "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
           "input_hash": input_hash(inp), "gates": {}, "refinements": 0, "deltas": 0,
           "failure_class": None, "status": "FAIL", "escalation": None, "auto_apply": False,
           "model_id": "stub-solver", "prompt_hash": "0" * 64, "context_manifest_hash": input_hash({"cases": "evals/cases.jsonl"}),
           "toolset_hash": input_hash({"gates": "src/gates.py"}), "token_in": 0, "token_out": 0}
    g1, g2 = gates.g1_permissions(inp), gates.g2_provenance(inp)
    for r in range(MAX_REFINEMENTS + 1):
        ans = stub_solve(inp, r)
        if ans is None:
            g3, fc = "FAIL", "F-SOURCE"
        else:
            g3, fc = gates.g3_units(inp, ans, exp.get("value", ans))
        rec["gates"] = {"G1": g1, "G2": g2, "G3": g3, "G4": "PASS"}
        rec["refinements"], rec["failure_class"] = r, fc
        if all(v == "PASS" for v in rec["gates"].values()):
            rec["status"] = "PASS"; break
        if r == MAX_REFINEMENTS:
            if "sources" in inp and inp.get("authority_rule") is None:
                rec["status"], rec["escalation"] = "SOURCE_CONFLICT", "HUMAN_GATE"
            else:
                rec["status"], rec["escalation"] = "NEEDS_REVIEW", "HUMAN_GATE"
            break
        rec["deltas"] += 1  # exactly one delta per refinement cycle
    return rec

def main(cases: str, out: str, run_id: str) -> list[dict]:
    recs = [run_case(json.loads(l), run_id) for l in Path(cases).read_text().splitlines() if l.strip()]
    with open(out, "a") as fh:
        for r in recs: fh.write(json.dumps(r, sort_keys=True) + "\n")
    return recs

if __name__ == "__main__":
    for r in main(sys.argv[1], sys.argv[2], sys.argv[3]): print(json.dumps(r))
