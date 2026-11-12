"""RFEM 5/6 adapter boundary; default mode cannot mutate application models."""
from __future__ import annotations

from typing import Any


def rfem5_manifest(geometry: dict[str, Any]) -> dict[str, Any]:
    """Offer neutral COM transfer data; the existing RFEM5 COM bridge owns writes."""
    return {
        "adapter": "RFEM5_COM", "mode": "TRANSFER_PREVIEW_ONLY",
        "requires": "RFEM5.Application + LockLicense + verified working-copy bridge",
        "nodes": geometry["nodes"], "members": geometry["members"],
        "readback": "NOT_RUN", "solver": "NOT_RUN",
    }


def rfem6_objects(geometry: dict[str, Any], rfem: Any) -> list[Any]:
    """Map validated geometry to documented Dlubal API II objects."""
    core = rfem.structure_core
    objects = [core.Material(no=1, name=geometry["material"])]
    objects.extend((
        core.CrossSection(no=1, name=geometry["section_columns"], material=1),
        core.CrossSection(no=2, name=geometry["section_beams"], material=1),
    ))
    for node in geometry["nodes"]:
        objects.append(core.Node(no=node["no"], coordinate_1=node["x_m"],
                                 coordinate_2=node["y_m"], coordinate_3=node["z_m"]))
    next_line = 1
    for member in geometry["members"]:
        objects.append(core.Line(no=next_line, definition_nodes=[member["start"], member["end"]]))
        section = 1 if member["kind"] == "column" else 2
        objects.append(core.Member(no=member["no"], line=next_line, cross_section_start=section))
        next_line += 1
    return objects


def rfem6_new_model(geometry: dict[str, Any], model_name: str, app: Any, rfem: Any,
                    *, allow_new_model: bool = False) -> Any:
    """Explicitly gated NEW-model write; requires host-side uniqueness check."""
    if not allow_new_model:
        raise PermissionError("Live model creation requires separate explicit approval")
    if not model_name.startswith("NEXUS_W012_TEST_"):
        raise ValueError("Model name must carry isolated test prefix")
    if geometry["status"] != "GEOMETRY_ONLY_NO_SOLVER":
        raise ValueError("Unexpected geometry state")
    # Explicitly fail closed until host-side model-name collision checks and
    # model-ID-bound object readback are implemented and tested on Windows.
    raise NotImplementedError("Live API-II creation blocked pending host preflight and readback")
