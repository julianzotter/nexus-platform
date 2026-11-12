"""Read-only RFEM 6 API II model inventory and strict geometry comparison."""
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path

from geometry import build_geometry, load_spec


def unique_model_id(model_list: object, name: str, common: object) -> object:
    matches = [m for m in model_list.model_info if m.name == name]
    if len(matches) != 1 or not matches[0].guid:
        raise ValueError(f"Model identity ambiguous or absent (matches={len(matches)})")
    return common.ModelId(guid=matches[0].guid)


def compare_nodes(expected: list[dict], observed: list[object], tolerance_m: float) -> dict:
    actual = {n.no: (n.coordinate_1, n.coordinate_2, n.coordinate_3) for n in observed}
    missing, changed = [], []
    for node in expected:
        n = node["no"]
        if n not in actual:
            missing.append(n)
        elif any(not math.isclose(v, actual[n][i], rel_tol=0, abs_tol=tolerance_m)
                 for i, v in enumerate((node["x_m"], node["y_m"], node["z_m"]))):
            changed.append(n)
    extras = sorted(actual.keys() - {n["no"] for n in expected})
    return {"status": "MATCH" if not (missing or changed or extras) else "MISMATCH",
            "expected": len(expected), "observed": len(observed),
            "missing_ids": missing, "changed_ids": changed, "extra_ids": extras}


def compare_member_topology(expected: list[dict], observed_members: list[object],
                            observed_lines: list[object]) -> dict:
    lines = {line.no: tuple(line.definition_nodes) for line in observed_lines}
    actual = {}
    for member in observed_members:
        ends = lines.get(member.line)
        if ends is not None:
            actual[member.no] = ends
    expected_map = {m["no"]: (m["start"], m["end"]) for m in expected}
    changed = [no for no, ends in expected_map.items() if actual.get(no) != ends]
    extras = sorted(actual.keys() - expected_map.keys())
    return {"status": "MATCH" if not changed and not extras else "MISMATCH",
            "changed_or_missing_ids": changed, "extra_ids": extras}


def readback(spec_path: Path, model_name: str, tolerance_m: float) -> dict:
    from dlubal.api import rfem, common
    geometry = build_geometry(load_spec(spec_path))
    if tolerance_m < 0 or not math.isfinite(tolerance_m):
        raise ValueError("Invalid geometric tolerance")
    # No create, update, save, calculate, delete, or model-close operations.
    with rfem.Application(api_key_value=os.environ.get("RFEM6_API_KEY") or None) as app:
        mid = unique_model_id(app.get_model_list(), model_name, common)
        nodes = list(app.get_object_list(objs=[rfem.structure_core.Node()],
                                         only_selected=False, model_id=mid))
        members = list(app.get_object_list(objs=[rfem.structure_core.Member()],
                                           only_selected=False, model_id=mid))
        lines = list(app.get_object_list(objs=[rfem.structure_core.Line()],
                                         only_selected=False, model_id=mid))
        node_check = compare_nodes(geometry["nodes"], nodes, tolerance_m)
        topology = compare_member_topology(geometry["members"], members, lines)
        return {"model_name": model_name, "model_guid": mid.guid,
                "nodes": node_check, "topology": topology,
                "members_expected": len(geometry["members"]), "members_observed": len(members),
                "status": "PASS_GEOMETRY" if node_check["status"] == "MATCH" and topology["status"] == "MATCH"
                          else "MISMATCH",
                "limitations": "Supports, loads, axis orientation and design suitability not verified",
                "solver": "NOT_RUN", "writes": "NONE"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("--model-name", required=True)
    parser.add_argument("--tolerance-m", type=float, default=1e-6)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = readback(args.spec, args.model_name, args.tolerance_m)
    except Exception as exc:
        # Only error class, never exception text (which may contain credentials).
        result = {"status": "BLOCKED", "error_class": type(exc).__name__, "solver": "NOT_RUN"}
    with args.out.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
