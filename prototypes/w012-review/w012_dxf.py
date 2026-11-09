"""Source-controlled axis/position sketch; no FEM model or design calculation."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
import tempfile
from pathlib import Path
from typing import Any
import ezdxf
from ezdxf import units


def numbers(values: list[Any], count: int) -> list[float]:
    if len(values) != count or any(type(v) not in (int, float) or not math.isfinite(v) for v in values):
        raise ValueError("Finite numeric coordinates required")
    return [float(v) for v in values]


def validate(data: dict[str, Any]) -> dict[str, tuple[float, float]]:
    if data.get("schema_version") != "1.0" or data.get("units") != "m":
        raise ValueError("schema_version=1.0 and units=m required")
    if data.get("drawing_status") != "REVIEW" or not isinstance(data.get("revision"), str) or not data['revision'].strip():
        raise ValueError("Explicit REVIEW drawing revision required")
    if data.get('engineering_release', False) is not False:
        raise ValueError('Review drawing cannot carry an engineering release')
    if data.get("drawing_selection_confirmed") is not True:
        raise ValueError("Drawing geometry selection is not confirmed")
    if not all(isinstance(data.get(k), str) and data[k].strip() for k in ("project", "plan_revision", "level_id", "coordinate_basis")):
        raise ValueError("Project, plan revision, selected level and coordinate basis required")
    sources = data.get("source_register", [])
    if not sources or any(not all(isinstance(s.get(k), str) and s[k].strip() for k in ("id", "url", "revision")) for s in sources):
        raise ValueError("Source register with identity, URL and revision required")
    source_ids = {s["id"] for s in sources}
    if len(source_ids) != len(sources):
        raise ValueError("Duplicate source IDs")
    if not data.get("nodes") or not data.get("members") or not data.get("axes"):
        raise ValueError("Nodes, members and axes required; missing data cannot be drawn")
    identifiers: set[str] = set()
    nodes: dict[str, tuple[float, float]] = {}
    for group in ("nodes", "axes", "members", "columns"):
        for obj in data.get(group, []):
            key = obj.get("id")
            if not isinstance(key, str) or not key.strip() or key in identifiers:
                raise ValueError("Unique nonempty IDs required across all entities")
            identifiers.add(key)
            if not all(isinstance(obj.get(k), str) and obj[k].strip() for k in ("source_id", "locator")):
                raise ValueError("Every entity requires a source and locator")
            if obj.get("source_status") != "VERIFIED_SOURCE":
                raise ValueError("Unverified geometry blocked")
            if obj["source_id"] not in source_ids:
                raise ValueError("Unresolved source ID")
    for node in data["nodes"]:
        if node.get("level_id") != data["level_id"]:
            raise ValueError("Only the selected single level may be drawn")
        nodes[node["id"]] = tuple(numbers(node["xy_m"], 2))
    for axis in data["axes"]:
        if axis.get("direction") not in ("X", "Y"):
            raise ValueError("Axis direction must be X or Y")
        numbers([axis["ordinate_m"]], 1)
    for member in data["members"]:
        if member.get("start") not in nodes or member.get("end") not in nodes:
            raise ValueError("Unknown member endpoint")
        if nodes[member["start"]] == nodes[member["end"]]:
            raise ValueError("Zero-length member")
    for column in data.get("columns", []):
        if column.get("rotation_deg", 0) != 0:
            raise ValueError("Rotated columns are outside generator scope")
        if column.get("node") not in nodes or min(numbers(column["section_xy_m"], 2)) <= 0:
            raise ValueError("Invalid column node or section")
    return nodes


def draw_axes(msp: Any, data: dict[str, Any], points: dict[str, tuple[float, float]]) -> None:
    xs, ys = zip(*points.values())
    lo_x, hi_x, lo_y, hi_y = min(xs)*1000, max(xs)*1000, min(ys)*1000, max(ys)*1000
    for axis in data["axes"]:
        value = axis["ordinate_m"]*1000
        a, b = ((lo_x-700, value), (hi_x+700, value)) if axis["direction"] == "X" else ((value, lo_y-700), (value, hi_y+700))
        msp.add_line(a, b, dxfattribs={"layer": "ACHSEN"})
        msp.add_text(axis["id"], dxfattribs={"height": 120, "layer": "TEXT"}).set_placement(b)
    for direction, ordinate in (("X", hi_y+1100), ("Y", hi_x+1100)):
        values = sorted({a["ordinate_m"]*1000 for a in data["axes"] if a["direction"] != direction})
        for start, end in zip(values, values[1:]):
            p1, p2 = ((start, lo_y), (end, lo_y)) if direction == "X" else ((lo_x, start), (lo_x, end))
            base = (0, ordinate) if direction == "X" else (ordinate, 0)
            msp.add_linear_dim(base=base, p1=p1, p2=p2, angle=0 if direction == "X" else 90,
                               override={"dimtxt": 100, "dimasz": 80}, dxfattribs={"layer": "MASSE"}).render()


def check_geometry(doc: Any, data: dict[str, Any], points: dict[str, tuple[float, float]]) -> None:
    msp = doc.modelspace()
    lines = list(msp.query('LINE[layer=="TRAEGER"]'))
    columns = list(msp.query('LWPOLYLINE[layer=="STUETZEN"]'))
    if len(lines) != len(data['members']) or len(columns) != len(data.get('columns', [])):
        raise RuntimeError('Entity count mismatch')
    axes = list(msp.query('LINE[layer=="ACHSEN"]'))
    if len(axes) != len(data['axes']):
        raise RuntimeError('Axis count mismatch')
    xs, ys = zip(*points.values())
    for line, axis in zip(axes, data['axes']):
        value = axis['ordinate_m']*1000
        start, end = (((min(xs)*1000-700, value), (max(xs)*1000+700, value))
                      if axis['direction'] == 'X' else
                      ((value, min(ys)*1000-700), (value, max(ys)*1000+700)))
        assert_point(line.dxf.start, start, 'Axis coordinate mismatch')
        assert_point(line.dxf.end, end, 'Axis coordinate mismatch')
    for line, member in zip(lines, data['members']):
        for attr, key in ((line.dxf.start, 'start'), (line.dxf.end, 'end')):
            expected = [v*1000 for v in points[member[key]]]
            assert_point(attr, expected, 'Member coordinate mismatch')
    for poly, column in zip(columns, data.get('columns', [])):
        if not poly.closed:
            raise RuntimeError('Open column contour')
        x, y = (v*1000 for v in points[column['node']])
        dx, dy = (v*500 for v in column['section_xy_m'])
        expected = [(x-dx,y-dy), (x+dx,y-dy), (x+dx,y+dy), (x-dx,y+dy)]
        vertices = list(poly.get_points('xyb'))
        if len(vertices) != 4 or any(v[2] != 0 for v in vertices) or poly.dxf.elevation != 0:
            raise RuntimeError('Invalid column contour')
        for actual, wanted in zip(vertices, expected):
            assert_point(actual[:2], wanted, 'Column coordinate mismatch')
    check_dimensions(msp, data)


def check_dimensions(msp: Any, data: dict[str, Any]) -> None:
    expected: list[tuple[int, float]] = []
    for direction, angle in (('Y', 0), ('X', 90)):
        values = sorted({a['ordinate_m']*1000 for a in data['axes'] if a['direction'] == direction})
        expected.extend((angle, b-a) for a, b in zip(values, values[1:]))
    actual = list(msp.query('DIMENSION[layer=="MASSE"]'))
    if len(actual) != len(expected):
        raise RuntimeError('Dimension count mismatch')
    for dimension, (angle, length) in zip(actual, expected):
        value = dimension.get_measurement()
        if not math.isfinite(value) or abs(value-length) > 1e-6 or dimension.dxf.angle != angle:
            raise RuntimeError('Dimension measurement mismatch')


def assert_point(actual: Any, expected: Any, message: str) -> None:
    values = tuple(actual)
    if any(not math.isfinite(v) for v in values):
        raise RuntimeError(message)
    if any(abs(values[i]-expected[i]) > 1e-6 for i in (0, 1)):
        raise RuntimeError(message)
    if len(values) == 3 and abs(values[2]) > 1e-6:
        raise RuntimeError(message)


def publish(doc: Any, data: dict[str, Any], target: Path, points: dict[str, tuple[float, float]]) -> dict[str, Any]:
    target.parent.mkdir(parents=True, exist_ok=True)
    checks = target.with_suffix('.checks.json')
    if target.exists() or checks.exists():
        raise FileExistsError('Drawing or checks already exists')
    with tempfile.TemporaryDirectory(dir=target.parent) as folder:
        raw = Path(folder)/'drawing.dxf'
        doc.saveas(raw)
        reopened = ezdxf.readfile(raw)
        if reopened.units != units.MM or reopened.audit().has_errors:
            raise RuntimeError('DXF readback failed')
        check_geometry(reopened, data, points)
        result = {'status': 'CAD_AUDIT_AND_GEOMETRY_PASS', 'engineering_release': False,
                  'ezdxf': ezdxf.__version__, 'sha256': hashlib.sha256(raw.read_bytes()).hexdigest(),
                  'input_sha256': hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False, allow_nan=False).encode()).hexdigest(),
                  'units': 'mm', 'level_id': data['level_id'], 'revision': data['revision']}
        receipt = Path(folder)/'checks.json'
        receipt.write_text(json.dumps(result, indent=2))
        os.link(raw, target)
        try:
            os.link(receipt, checks)
        except Exception:
            if target.exists() and os.path.samefile(raw, target):
                target.unlink()
            raise
    return result


def generate(data: dict[str, Any], target: Path) -> dict[str, Any]:
    points = validate(data)
    if target.exists():
        raise FileExistsError("Refusing to overwrite an existing drawing")
    doc = ezdxf.new("R2010")
    doc.units = units.MM
    for name, color in (("ACHSEN", 1), ("STUETZEN", 3), ("TRAEGER", 5), ("TEXT", 7), ("MASSE", 2)):
        doc.layers.new(name, dxfattribs={"color": color})
    msp = doc.modelspace()
    draw_axes(msp, data, points)
    for member in data["members"]:
        a, b = [tuple(v*1000 for v in points[member[k]]) for k in ("start", "end")]
        msp.add_line(a, b, dxfattribs={"layer": "TRAEGER", "lineweight": 35})
        msp.add_text(member["id"], dxfattribs={"height": 120, "layer": "TEXT"}).set_placement(((a[0]+b[0])/2, (a[1]+b[1])/2+150))
    for column in data.get("columns", []):
        x, y = (v*1000 for v in points[column["node"]])
        dx, dy = (v*500 for v in column["section_xy_m"])
        msp.add_lwpolyline([(x-dx,y-dy),(x+dx,y-dy),(x+dx,y+dy),(x-dx,y+dy)], close=True,
                           dxfattribs={"layer": "STUETZEN"})
        msp.add_text(column["id"], dxfattribs={"height": 100, "layer": "TEXT"}).set_placement((x+dx+50,y))
    low = min(v[1] for v in points.values())*1000-1400
    msp.add_text(f"{data['project']} {data['revision']} | REVIEW - KEINE STATIKFREIGABE | mm",
                 dxfattribs={"height": 130, "layer": "TEXT"}).set_placement((0,low))
    return publish(doc, data, target, points)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = generate(json.loads(args.input.read_text()), args.output)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
