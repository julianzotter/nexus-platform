"""Hard gates G1-G4 as pure functions. No LLM, no norms."""
from __future__ import annotations
import re
UNIT_SI = {"N": 1.0, "kN": 1e3, "MN": 1e6, "Nm": 1.0, "kNm": 1e3, "m": 1.0, "mm": 1e-3}

def parse_qty(s: str) -> tuple[float, str]:
    m = re.fullmatch(r"\s*([-+]?\d+(?:[.,]\d+)?)\s*([A-Za-z/²]+)\s*", s)
    if not m:
        raise ValueError(f"bad quantity: {s!r}")
    return float(m.group(1).replace(",", ".")), m.group(2)

def g1_permissions(inp: dict) -> str:
    return "PASS" if inp.get("auto_write") is not True else "FAIL"

def g2_provenance(inp: dict) -> str:
    if "sources" in inp:
        return "PASS" if inp["sources"] else "FAIL"
    return "PASS" if inp.get("source_id") and inp.get("norm_ref") else "FAIL"

def g3_units(inp: dict, answer: str, expected: str) -> tuple[str, str | None]:
    try:
        av, au = parse_qty(answer); ev, eu = parse_qty(expected)
    except ValueError:
        return "FAIL", "F-NUM"
    if au not in UNIT_SI or eu not in UNIT_SI:
        return "FAIL", "F-NUM"
    if abs(av * UNIT_SI[au] - ev * UNIT_SI[eu]) > 1e-6 * max(1.0, abs(ev * UNIT_SI[eu])):
        return "FAIL", "F-NUM"
    return "PASS", None

def g4_regression(prev_status: str | None, status: str) -> str:
    return "FAIL" if prev_status == "PASS" and status != "PASS" else "PASS"
