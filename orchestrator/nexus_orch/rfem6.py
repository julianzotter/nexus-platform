"""RFEM6 API II adapter: typed objects; explicit new-model identity; no solver."""
from __future__ import annotations

import re
from importlib.metadata import version
from typing import Any, Callable
from uuid import uuid4

from .geometry import validate_topology

TESTED_SDK = "2.16.6"


def objects(model: dict[str, Any]) -> list[Any]:
    from dlubal.api import rfem
    validate_topology(model)
    c = rfem.structure_core
    cat = model["catalog"]
    return [c.Material(no=1, name=cat["rfem6_material"]),
            c.CrossSection(no=1, material=1, name=cat["section_columns"]),
            c.CrossSection(no=2, material=1, name=cat["section_beams"]),
            *[c.Node(no=n["no"], coordinate_1=n["x_m"], coordinate_2=n["y_m"],
                     coordinate_3=n["z_m"]) for n in model["nodes"]],
            *[c.Line(no=l["no"], definition_nodes=l["nodes"]) for l in model["lines"]],
            *[c.Member(no=m["no"], line=m["line"], cross_section_start=m["section"],
                       type=c.Member.TYPE_BEAM) for m in model["members"]]]


def sdk_check(model: dict[str, Any]) -> dict[str, Any]:
    installed = version("dlubal.api")
    if installed != TESTED_SDK:
        raise RuntimeError(f"Requires tested SDK {TESTED_SDK}; installed {installed}")
    objs = objects(model)
    for obj in objs:
        if type(obj).FromString(obj.SerializeToString(deterministic=True)) != obj:
            raise RuntimeError("Protobuf roundtrip mismatch")
    return {"sdk_version": installed, "protobuf_objects": len(objs), "roundtrip": "PASS"}


def verify_readback(app: Any, model_id: Any, planned: dict[str, Any]) -> None:
    from dlubal.api import rfem
    c = rfem.structure_core
    nodes = app.get_object_list(objs=[c.Node()], model_id=model_id)
    actual = {n.no: (n.coordinate_1, n.coordinate_2, n.coordinate_3) for n in nodes}
    expected = {n["no"]: (n["x_m"], n["y_m"], n["z_m"]) for n in planned["nodes"]}
    if actual != expected: raise RuntimeError("RFEM6 node readback mismatch")
    for kind, records, fields in (
        (c.Line, planned["lines"], lambda r: {"definition_nodes": r["nodes"]}),
        (c.Member, planned["members"], lambda r: {"line": r["line"],
          "cross_section_start": r["section"], "type": c.Member.TYPE_BEAM}),
    ):
        got = app.get_object_list(objs=[kind()], model_id=model_id)
        if {v.no for v in got} != {v["no"] for v in records}:
            raise RuntimeError("RFEM6 object IDs differ")
        by_id = {v.no: v for v in got}
        for rec in records:
            for field, expected_value in fields(rec).items():
                value = getattr(by_id[rec["no"]], field)
                if isinstance(expected_value, list): value = list(value)
                if value != expected_value: raise RuntimeError("RFEM6 reference readback mismatch")


def write_new(model: dict[str, Any], receipt: dict[str, Any], *, port: int = 9000,
              checkpoint: Callable[[], None] = lambda: None) -> None:
    from dlubal.api import rfem
    sdk_check(model)
    with rfem.Application(url="127.0.0.1", port=port) as app:
        info = app.get_application_info()
        build = f"{info.version} {info.full_version}".strip()
        if not re.search(r"(?<!\d)6\.16(?=\D|$)", build):
            raise RuntimeError("Tested adapter requires RFEM 6.16; verify SDK/app pair")
        receipt["application_build"] = build
        name = f"NEXUS_GEOMETRY_{uuid4().hex}"
        if any(entry.name == name for entry in app.get_model_list().model_info):
            raise RuntimeError("New-model name collision; no write attempted")
        receipt.update(status="CREATE_REQUESTED", model_name=name)
        checkpoint()
        model_id = app.create_model(name=name)
        receipt.update(status="CREATED_PARTIAL_UNSAVED", model_id=str(model_id), model_name=name)
        checkpoint()
        # Keep a partially created model identifiable; never delete or silently retry it.
        app.create_object_list(objs=objects(model), model_id=model_id, skip_invalid_attributes=False)
        verify_readback(app, model_id, model)
        receipt.update(status="GEOMETRY_READBACK_PASS_UNSAVED", calculation="NOT_RUN")


def preflight(port: int = 9000) -> dict[str, Any]:
    from dlubal.api import rfem
    with rfem.Application(url="127.0.0.1", port=port) as app:
        info = app.get_application_info()
        models = app.get_model_list()
        return {"status": "READ_ONLY_CONNECTION_PASS", "sdk_version": version("dlubal.api"),
                "application_version": info.version, "application_full_version": info.full_version,
                "open_models": [{"name": m.name, "guid": m.guid} for m in models.model_info],
                "calculation": "NOT_RUN"}
