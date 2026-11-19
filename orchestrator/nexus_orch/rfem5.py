"""Windows RFEM5 COM: exact-path preflight and empty-model geometry transfer."""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Callable

from .geometry import validate_topology


def connect(type_library: Path) -> tuple[Any, Any]:
    if sys.platform != "win32": raise RuntimeError("RFEM5 COM requires Windows")
    if not type_library.is_file(): raise RuntimeError("RFEM5 type library not found")
    import comtypes.client
    types = comtypes.client.GetModule(str(type_library.resolve()))
    app = comtypes.client.GetActiveObject("RFEM5.Application", interface=types.IApplication)
    return app, types


def _same_path(actual: str, expected: Path) -> bool:
    return os.path.normcase(os.path.abspath(actual)) == os.path.normcase(str(expected.resolve()))


def inspect(app: Any, expected: Path) -> tuple[Any, dict[str, Any]]:
    model = app.GetActiveModel()
    if not model or not _same_path(model.GetPath(), expected):
        raise RuntimeError("RFEM5 active-model path differs from expected working copy")
    data = model.GetModelData()
    counts = {name: int(getattr(data, f"Get{name}Count")())
              for name in ("Node", "Line", "Member", "Surface", "Solid", "Material", "CrossSection")}
    return model, {"model_path": str(expected.resolve()), "counts": counts}


def preflight(type_library: Path, expected: Path) -> dict[str, Any]:
    app, _ = connect(type_library)
    app.LockLicense()
    try:
        _, result = inspect(app, expected)
        return {"status": "READ_ONLY_IDENTITY_PASS", **result, "calculation": "NOT_RUN"}
    finally:
        app.UnlockLicense()


def _records(types: Any, model: dict[str, Any]) -> list[tuple[str, Any]]:
    def array(cls: Any, rows: list[dict[str, Any]]) -> Any:
        result = (cls * len(rows))()
        for obj, row in zip(result, rows):
            fields = {f[0].casefold(): f[0] for f in cls._fields_}
            for key, val in row.items():
                if key.casefold() not in fields:
                    raise RuntimeError(f"RFEM5 typelib field missing: {cls.__name__}.{key}")
                setattr(obj, fields[key.casefold()], val)
        return result
    material = [{"No": 1, "TextID": model["catalog"]["rfem5_material_text_id"]}]
    section = [{"No": i, "MaterialNo": 1, "TextID": model["catalog"][key]}
               for i, key in ((1, "section_columns"), (2, "section_beams"))]
    nodes = [{"No": n["no"], "RefObjectNo": 0, "X": n["x_m"], "Y": n["y_m"], "Z": n["z_m"]}
             for n in model["nodes"]]
    lines = [{"No": l["no"], "NodeList": ",".join(map(str, l["nodes"])), "Type": types.PolylineType}
             for l in model["lines"]]
    members = [{"No": m["no"], "LineNo": m["line"], "StartCrossSectionNo": m["section"]}
               for m in model["members"]]
    return [(name, array(getattr(types, cls), rows)) for name, cls, rows in (
        ("Materials", "Material", material), ("CrossSections", "CrossSection", section),
        ("Nodes", "Node", nodes), ("Lines", "Line", lines), ("Members", "Member", members))]


def write_empty(type_library: Path, expected: Path, model: dict[str, Any], receipt: dict[str, Any],
                *, checkpoint: Callable[[], None] = lambda: None) -> None:
    validate_topology(model)
    app, types = connect(type_library)
    app.LockLicense()
    try:
        active, inspected = inspect(app, expected)
        if any(inspected["counts"].values()):
            raise RuntimeError("RFEM5 transfer requires an entirely empty, identified working model")
        data = active.GetModelData()
        rows = _records(types, model)  # Resolve every typelib field before the first write.
        receipt.update(status="MODIFICATION_STARTED_PARTIAL", **inspected)
        checkpoint()
        data.PrepareModification()
        try:
            for name, values in rows: getattr(data, "Set" + name)(values)
        finally:
            data.FinishModification()
        actual = {n.No: (n.X, n.Y, n.Z) for n in data.GetNodes()}
        wanted = {n["no"]: (n["x_m"], n["y_m"], n["z_m"]) for n in model["nodes"]}
        if actual != wanted: raise RuntimeError("RFEM5 node readback mismatch")
        lines = {l.No: tuple(int(n.strip()) for n in l.NodeList.split(",")) for l in data.GetLines()}
        if lines != {l["no"]: tuple(l["nodes"]) for l in model["lines"]}:
            raise RuntimeError("RFEM5 line readback mismatch")
        members = {m.No: (m.LineNo, m.StartCrossSectionNo) for m in data.GetMembers()}
        if members != {m["no"]: (m["line"], m["section"]) for m in model["members"]}:
            raise RuntimeError("RFEM5 member readback mismatch")
        receipt.update(status="GEOMETRY_READBACK_PASS_UNSAVED", calculation="NOT_RUN")
    finally:
        app.UnlockLicense()
