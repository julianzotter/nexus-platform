from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import ezdxf
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle


LAYERS = [
    "FT_RAHMEN", "FT_SCHALUNG", "FT_KONSOLE", "FT_DURCHBRUCH",
    "FT_BEW_POS1", "FT_BEW_POS2", "FT_BEW_POS3", "FT_BEW_POS4", "FT_BEW_POS5",
    "FT_BEMASSUNG", "FT_TEXT", "FT_QA",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_spec(spec: dict[str, Any]) -> None:
    required = ["beam_id", "drawing_level", "outline_mm", "openings", "rebar", "provenance"]
    missing = [k for k in required if k not in spec]
    if missing:
        raise ValueError(f"missing fields: {missing}")
    if spec["drawing_level"] not in {"SCHEMATIC", "TENDER", "REBAR_DETAIL"}:
        raise ValueError("invalid drawing_level")
    if len(spec["outline_mm"]) < 4:
        raise ValueError("outline_mm must contain a closed-capable polygon")
    if spec["drawing_level"] == "REBAR_DETAIL":
        unresolved = [x.get("id", "?") for x in spec["rebar"]
                      if x.get("geometry_status") != "VERIFIED"]
        if unresolved:
            raise ValueError(f"REBAR_DETAIL blocked; unresolved rebar geometry: {unresolved}")


def _dim_h(msp, x1: float, x2: float, z: float, label: str) -> None:
    tick = 35.0
    msp.add_line((x1, z), (x2, z), dxfattribs={"layer": "FT_BEMASSUNG"})
    msp.add_line((x1, z-tick), (x1, z+tick), dxfattribs={"layer": "FT_BEMASSUNG"})
    msp.add_line((x2, z-tick), (x2, z+tick), dxfattribs={"layer": "FT_BEMASSUNG"})
    msp.add_text(label, dxfattribs={"height": 45, "layer": "FT_BEMASSUNG"}).set_placement(((x1+x2)/2, z+55))


def make_dxf(spec: dict[str, Any], out: Path) -> None:
    doc = ezdxf.new("R2010", setup=True)
    for name in LAYERS:
        if name not in doc.layers:
            doc.layers.add(name)
    doc.header["$INSUNITS"] = 4  # millimetres
    msp = doc.modelspace()

    outline = [(float(x), float(z)) for x, z in spec["outline_mm"]]
    msp.add_lwpolyline(outline, close=True, dxfattribs={"layer": "FT_SCHALUNG"})
    x_min, x_max = min(x for x, _ in outline), max(x for x, _ in outline)
    z_min, z_max = min(z for _, z in outline), max(z for _, z in outline)
    frame = [(x_min-500, z_min-700), (x_max+500, z_min-700), (x_max+500, z_max+1200), (x_min-500, z_max+1200)]
    msp.add_lwpolyline(frame, close=True, dxfattribs={"layer": "FT_RAHMEN"})
    _dim_h(msp, x_min, x_max, z_min-250, f"L={x_max-x_min:.0f} mm")

    for corbel in spec.get("corbels", []):
        pts = [(float(x), float(z)) for x, z in corbel["outline_mm"]]
        msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "FT_KONSOLE"})

    for op in spec["openings"]:
        x = float(op["station_mm"])
        w = float(op["width_mm"])
        h = float(op["height_mm"])
        z0 = float(op["bottom_mm"])
        pts = [(x-w/2, z0), (x+w/2, z0), (x+w/2, z0+h), (x-w/2, z0+h)]
        msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "FT_DURCHBRUCH"})
        _dim_h(msp, x-w/2, x+w/2, z0-100, f"{w:g}")
        label = f"{op['id']} {w:g}x{h:g} @ {x/1000:.2f}m"
        msp.add_text(label, dxfattribs={"height": 60, "layer": "FT_TEXT"}).set_placement((x-w/2, z0+h+80))

    for rb in spec["rebar"]:
        pos = str(rb.get("position_id", "OTHER"))
        layer = f"FT_BEW_{pos}" if f"FT_BEW_{pos}" in LAYERS else "FT_QA"
        label = str(rb.get("designation_raw", ""))
        geom = rb.get("polyline_mm")
        if geom:
            pts = [(float(x), float(z)) for x, z in geom]
            msp.add_lwpolyline(pts, close=bool(rb.get("closed", False)), dxfattribs={"layer": layer})
        anchor = rb.get("label_anchor_mm", [0, 0])
        msp.add_text(f"{pos}: {label}", dxfattribs={"height": 55, "layer": layer}).set_placement(tuple(anchor))

    qa = spec.get("qa", {})
    status = qa.get("status", "PENDING")
    msp.add_text(
        f"{spec['beam_id']} | {spec['drawing_level']} | QA={status}",
        dxfattribs={"height": 90, "layer": "FT_QA"},
    ).set_placement((min(x for x, _ in outline), max(z for _, z in outline) + 450))

    if spec["drawing_level"] == "SCHEMATIC":
        msp.add_text(
            "SCHEMATIC / NOT FOR CONSTRUCTION",
            dxfattribs={"height": 140, "layer": "FT_QA"},
        ).set_placement((min(x for x, _ in outline), max(z for _, z in outline) + 650))

    doc.saveas(out)


def render_vector(spec: dict[str, Any], out: Path, paper: str) -> None:
    mm = {"A3": (420, 297), "A2": (594, 420)}
    if paper not in mm:
        raise ValueError("paper must be A3 or A2")
    w_mm, h_mm = mm[paper]
    fig = plt.figure(figsize=(w_mm / 25.4, h_mm / 25.4))
    ax = fig.add_axes([0.06, 0.10, 0.90, 0.80])

    outline = [(float(x), float(z)) for x, z in spec["outline_mm"]]
    ax.add_patch(Polygon(outline, closed=True, fill=False, linewidth=1.2))

    for corbel in spec.get("corbels", []):
        ax.add_patch(Polygon(corbel["outline_mm"], closed=True, fill=False, linewidth=1.0))

    for op in spec["openings"]:
        x, w = float(op["station_mm"]), float(op["width_mm"])
        z0, h = float(op["bottom_mm"]), float(op["height_mm"])
        ax.add_patch(Rectangle((x-w/2, z0), w, h, fill=False, linewidth=1.0))
        ax.text(x-w/2, z0+h+60, f"{op['id']} {w:g}x{h:g}", fontsize=6)

    for rb in spec["rebar"]:
        geom = rb.get("polyline_mm")
        if geom:
            xs, zs = zip(*geom)
            ax.plot(xs, zs, linewidth=0.8)
        a = rb.get("label_anchor_mm", [0, 0])
        ax.text(a[0], a[1], f"{rb.get('position_id','')}: {rb.get('designation_raw','')}", fontsize=6)

    xs, zs = zip(*outline)
    xpad = max((max(xs)-min(xs))*0.03, 300)
    zpad = max((max(zs)-min(zs))*0.20, 500)
    ax.set_xlim(min(xs)-xpad, max(xs)+xpad)
    ax.set_ylim(min(zs)-zpad, max(zs)+zpad)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x [mm]")
    ax.set_ylabel("z [mm]")
    ax.grid(True, linewidth=0.2)
    ax.set_title(f"{spec['beam_id']} · {spec['drawing_level']} · source {spec['provenance'].get('source_id','?')}", fontsize=9)

    if spec["drawing_level"] == "SCHEMATIC":
        fig.text(0.5, 0.04, "SCHEMATIC / NOT FOR CONSTRUCTION", ha="center", fontsize=10)

    fmt = out.suffix.lstrip(".").lower()
    if fmt == "pdf":
        fig.savefig(out, format=fmt, metadata={"Title": spec["beam_id"]})
    else:
        fig.savefig(out, format=fmt)
    plt.close(fig)


def write_manifest(spec_path: Path, outputs: list[Path], out: Path) -> None:
    data = json.loads(spec_path.read_text(encoding="utf-8"))
    manifest = {
        "schema_version": "ft-cad-run-0.1",
        "beam_id": data["beam_id"],
        "drawing_level": data["drawing_level"],
        "source": data["provenance"],
        "spec_sha256": sha256_file(spec_path),
        "outputs": [{"path": str(p), "sha256": sha256_file(p)} for p in outputs],
        "qa_status": data.get("qa", {}).get("status", "PENDING"),
    }
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--paper", choices=["A3", "A2"], default="A3")
    ap.add_argument("--formats", default="dxf,pdf")
    args = ap.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    validate_spec(spec)
    args.out.mkdir(parents=True, exist_ok=True)

    outputs: list[Path] = []
    for fmt in [x.strip().lower() for x in args.formats.split(",") if x.strip()]:
        p = args.out / f"{spec['beam_id']}.{fmt}"
        if fmt == "dxf":
            make_dxf(spec, p)
        elif fmt in {"pdf", "ps"}:
            render_vector(spec, p, args.paper)
        else:
            raise ValueError(f"unsupported format: {fmt}")
        outputs.append(p)

    write_manifest(args.spec, outputs, args.out / "manifest.json")
    print("\n".join(str(p) for p in outputs))


if __name__ == "__main__":
    main()
