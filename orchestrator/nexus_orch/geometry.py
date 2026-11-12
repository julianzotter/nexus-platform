"""Deterministic SI frame geometry. No loads, supports or solver decisions."""
from __future__ import annotations

import hashlib
import json
import math
from itertools import accumulate
from typing import Any


class GeometryError(ValueError):
    """Input or topology violates the geometry contract."""


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False,
                       allow_nan=False, separators=(",", ":")) + "\n").encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _dimensions(value: Any, key: str) -> list[float]:
    if not isinstance(value, list) or not value or len(value) > 100:
        raise GeometryError(f"{key}: require 1..100 positive dimensions")
    if any(type(v) not in (int, float) or not 1e-4 <= v <= 1000
           or not math.isfinite(v) for v in value):
        raise GeometryError(f"{key}: finite metres in [0.0001,1000] required")
    return [float(v) for v in value]


def validate_spec(spec: dict[str, Any]) -> dict[str, Any]:
    required = {"schema_version", "scope", "units", "coordinate_system", "name",
                "bays_x_m", "bays_y_m", "storey_heights_m", "catalog", "source_refs"}
    if not isinstance(spec, dict) or set(spec) != required:
        raise GeometryError("Spec fields must match geometry schema exactly")
    if (spec["schema_version"] != "1.0.0" or spec["units"] != "m"
            or spec["coordinate_system"] != "RFEM_GLOBAL_Z_DOWN"):
        raise GeometryError("Require schema 1.0.0, metres, RFEM_GLOBAL_Z_DOWN")
    if spec["scope"] not in ("SYNTHETIC", "PROJECT"):
        raise GeometryError("Unknown scope")
    if not isinstance(spec["name"], str) or not 1 <= len(spec["name"]) <= 80:
        raise GeometryError("Require a model name of 1..80 characters")
    refs = spec["source_refs"]
    if not isinstance(refs, list) or any(not isinstance(v, str) or not v.strip() for v in refs):
        raise GeometryError("source_refs must contain nonempty source locators")
    if spec["scope"] == "PROJECT" and not refs:
        raise GeometryError("PROJECT geometry requires source locators; approval remains external")
    catalog = spec["catalog"]
    keys = {"rfem6_material", "rfem5_material_text_id", "section_columns", "section_beams"}
    if (not isinstance(catalog, dict) or set(catalog) != keys
            or any(not isinstance(v, str) or not v.strip() for v in catalog.values())):
        raise GeometryError("Require explicit RFEM6 material, RFEM5 TextID and section")
    clean = {**spec, "catalog": dict(catalog), "source_refs": list(refs)}
    for key in ("bays_x_m", "bays_y_m", "storey_heights_m"):
        clean[key] = _dimensions(spec[key], key)
    n = math.prod(len(clean[k]) + 1 for k in ("bays_x_m", "bays_y_m", "storey_heights_m"))
    if n > 10000:
        raise GeometryError("Model exceeds 10000-node pilot limit")
    return clean


def generate(spec: dict[str, Any]) -> dict[str, Any]:
    """Generate columns and floor beams; no ground beams or slabs are assumed."""
    spec = validate_spec(spec)
    xs = [0.0, *accumulate(spec["bays_x_m"])]
    ys = [0.0, *accumulate(spec["bays_y_m"])]
    zs = [0.0, *(-z for z in accumulate(spec["storey_heights_m"]))]
    nodes, lines, members, lookup = [], [], [], {}
    for k, z in enumerate(zs):
        for j, y in enumerate(ys):
            for i, x in enumerate(xs):
                no = len(nodes) + 1
                lookup[i, j, k] = no
                nodes.append({"no": no, "x_m": x, "y_m": y, "z_m": z})
    for k in range(1, len(zs)):
        for j in range(len(ys)):
            for i in range(len(xs)):
                edges = [((i, j, k-1), "column")]
                if i: edges.append(((i-1, j, k), "beam_x"))
                if j: edges.append(((i, j-1, k), "beam_y"))
                for start, role in edges:
                    no = len(lines) + 1
                    lines.append({"no": no, "nodes": [lookup[start], lookup[i, j, k]]})
                    members.append({"no": no, "line": no, "section": 1 if role == "column" else 2, "role": role})
    result = {"schema_version": "1.0.0", "units": "m", "scope": spec["scope"],
              "coordinate_system": spec["coordinate_system"], "name": spec["name"],
              "source_refs": spec["source_refs"], "normalized_spec_sha256": digest(spec),
              "catalog": spec["catalog"], "nodes": nodes, "lines": lines, "members": members,
              "analysis_state": "GEOMETRY_ONLY_NO_SUPPORTS_OR_LOADS"}
    validate_topology(result)
    return result


def validate_topology(model: dict[str, Any]) -> None:
    nodes = {n["no"]: (n["x_m"], n["y_m"], n["z_m"]) for n in model["nodes"]}
    if len(nodes) != len(model["nodes"]) or len(set(nodes.values())) != len(nodes):
        raise GeometryError("Duplicate node IDs or coordinates")
    edges = set()
    for line in model["lines"]:
        a, b = line["nodes"]
        if a not in nodes or b not in nodes or a == b or nodes[a] == nodes[b]:
            raise GeometryError("Invalid line endpoints")
        edge = tuple(sorted((a, b)))
        if edge in edges: raise GeometryError("Duplicate edge")
        edges.add(edge)
    line_ids = {v["no"] for v in model["lines"]}
    if len(line_ids) != len(model["lines"]): raise GeometryError("Duplicate line IDs")
    member_ids = {m["no"] for m in model["members"]}
    if len(member_ids) != len(model["members"]): raise GeometryError("Duplicate member IDs")
    if any(m["line"] not in line_ids or m["section"] not in (1, 2) for m in model["members"]):
        raise GeometryError("Invalid member reference")
