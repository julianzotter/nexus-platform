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
    """Legacy preview shape delegated to the shared deterministic geometry core.

    Legacy input lacks source locators: it remains an unverified synthetic preview.
    The newer CLI/schema is required for a sourced PROJECT input.
    """
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "orchestrator"))
    from nexus_orch.geometry import generate
    model = generate({"schema_version": "1.0.0", "scope": "SYNTHETIC", "units": "m",
        "coordinate_system": "RFEM_GLOBAL_Z_DOWN", "name": "LEGACY_UNVERIFIED_PREVIEW",
        "bays_x_m": list(spec.spans_x_m), "bays_y_m": list(spec.spans_y_m),
        "storey_heights_m": list(spec.storeys_m), "source_refs": [],
        "catalog": {"rfem6_material": spec.material,
                    "rfem5_material_text_id": "UNRESOLVED_NOT_FOR_COM_TRANSFER",
                    "section_columns": spec.section_columns, "section_beams": spec.section_beams}})
    lines = {line["no"]: line["nodes"] for line in model["lines"]}
    members = [{"no": m["no"], "start": lines[m["line"]][0],
                "end": lines[m["line"]][1], "kind": m["role"]} for m in model["members"]]
    return {"project": spec.project, "unit": "m", "nodes": model["nodes"], "members": members,
            "base_nodes": [n["no"] for n in model["nodes"] if n["z_m"] == 0],
            "material": spec.material, "section_columns": spec.section_columns,
            "section_beams": spec.section_beams, "loads": "UNDEFINED", "supports": "UNDEFINED",
            "scope": "LEGACY_UNVERIFIED_PREVIEW", "coordinate_system": "RFEM_GLOBAL_Z_DOWN",
            "status": "GEOMETRY_ONLY_NO_SOLVER"}


def load_spec(path: Path) -> FrameSpec:
    return FrameSpec.from_dict(json.loads(path.read_text(encoding="utf-8")))
