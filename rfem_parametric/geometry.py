"""Deterministic 3D frame geometry for NEXUS; no structural analysis."""
from __future__ import annotations

from dataclasses import dataclass
from itertools import accumulate
import json
import math
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class FrameSpec:
    project: str
    spans_x_m: tuple[float, ...]
    spans_y_m: tuple[float, ...]
    storeys_m: tuple[float, ...]
    material: str
    section_columns: str
    section_beams: str

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "FrameSpec":
        fields = ("spans_x_m", "spans_y_m", "storeys_m")
        lengths = {key: tuple(float(x) for x in raw[key]) for key in fields}
        for key, values in lengths.items():
            if not values or len(values) > 50 or any(not math.isfinite(x) or x <= 0 for x in values):
                raise ValueError(f"Invalid positive finite lengths: {key}")
        strings = ("project", "material", "section_columns", "section_beams")
        for key in strings:
            if not isinstance(raw.get(key), str) or not raw[key].strip():
                raise ValueError(f"Missing project-controlled field: {key}")
        if raw["project"] != "W012_EIBENGASSE_HOFTRAKT":
            raise ValueError("Scope mismatch: W012 pilot required")
        return cls(**{**lengths, **{key: raw[key] for key in strings}})


def positions(lengths: tuple[float, ...]) -> tuple[float, ...]:
    """Coordinates in metres, including the origin."""
    return (0.0, *accumulate(lengths))


def build_geometry(spec: FrameSpec) -> dict[str, Any]:
    """Create numbered nodes and members in an orthogonal frame grid."""
    xs, ys, zs = (positions(v) for v in (spec.spans_x_m, spec.spans_y_m, spec.storeys_m))
    ids: dict[tuple[int, int, int], int] = {}
    nodes: list[dict[str, Any]] = []
    for k, z in enumerate(zs):
        for j, y in enumerate(ys):
            for i, x in enumerate(xs):
                no = len(nodes) + 1
                ids[i, j, k] = no
                nodes.append({"no": no, "x_m": x, "y_m": y, "z_m": z})
    members: list[dict[str, Any]] = []
    def add(a: tuple[int, int, int], b: tuple[int, int, int], kind: str) -> None:
        members.append({"no": len(members) + 1, "start": ids[a], "end": ids[b], "kind": kind})
    for k in range(len(zs)):
        for j in range(len(ys)):
            for i in range(len(xs)):
                if k + 1 < len(zs):
                    add((i, j, k), (i, j, k + 1), "column")
                if k > 0 and i + 1 < len(xs):
                    add((i, j, k), (i + 1, j, k), "beam_x")
                if k > 0 and j + 1 < len(ys):
                    add((i, j, k), (i, j + 1, k), "beam_y")
    return {
        "project": spec.project, "unit": "m", "nodes": nodes, "members": members,
        "base_nodes": [ids[i, j, 0] for j in range(len(ys)) for i in range(len(xs))],
        "material": spec.material, "section_columns": spec.section_columns,
        "section_beams": spec.section_beams, "loads": "UNDEFINED",
        "supports": "UNDEFINED", "status": "GEOMETRY_ONLY_NO_SOLVER",
    }


def load_spec(path: Path) -> FrameSpec:
    return FrameSpec.from_dict(json.loads(path.read_text(encoding="utf-8")))
