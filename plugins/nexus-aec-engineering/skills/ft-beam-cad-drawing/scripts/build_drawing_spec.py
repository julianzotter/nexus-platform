from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def nearest_opening(
    station_mm: float,
    geometry_openings: list[dict[str, Any]],
    tolerance_mm: float,
) -> dict[str, Any]:
    candidates = sorted(
        geometry_openings,
        key=lambda x: abs(float(x["station_mm"]) - station_mm),
    )
    if not candidates:
        raise ValueError("geometry contains no openings")
    best = candidates[0]
    delta = abs(float(best["station_mm"]) - station_mm)
    if delta > tolerance_mm:
        raise ValueError(
            f"opening at {station_mm} mm has no geometry match within {tolerance_mm} mm"
        )
    return best


def build_spec(
    matrix: dict[str, Any],
    geometry: dict[str, Any],
    drawing_level: str,
    tolerance_mm: float,
) -> dict[str, Any]:
    if drawing_level not in {"SCHEMATIC", "TENDER", "REBAR_DETAIL"}:
        raise ValueError("invalid drawing level")
    if drawing_level != "SCHEMATIC" and geometry.get("verification_status") != "VERIFIED":
        raise ValueError("TENDER/REBAR_DETAIL requires VERIFIED geometry")

    openings: list[dict[str, Any]] = []
    rebar: list[dict[str, Any]] = []
    for i, item in enumerate(matrix.get("openings", []), start=1):
        st = float(item["station_mm"])
        g = nearest_opening(st, geometry.get("openings", []), tolerance_mm)
        op_id = str(g.get("id") or f"DB{i}")
        openings.append({
            "id": op_id,
            "station_mm": float(g["station_mm"]),
            "width_mm": float(g["width_mm"]),
            "height_mm": float(g["height_mm"]),
            "bottom_mm": float(g["bottom_mm"]),
            "matrix_column": item.get("column"),
            "eta": item.get("eta"),
        })
        for pos_id, raw in item.get("pos", {}).items():
            rebar.append({
                "id": f"{op_id}-{pos_id}",
                "position_id": pos_id,
                "opening_id": op_id,
                "designation_raw": raw,
                "geometry_status": "RAW_ONLY",
                "label_anchor_mm": [
                    float(g["station_mm"]) - float(g["width_mm"]) / 2,
                    float(g["bottom_mm"]) + float(g["height_mm"]) + 120 + 70 * (int(pos_id[1:]) - 1),
                ],
            })

    return {
        "schema_version": "p205-ft-drawing-spec-0.1",
        "beam_id": str(geometry["beam_id"]),
        "drawing_level": drawing_level,
        "outline_mm": geometry["outline_mm"],
        "corbels": geometry.get("corbels", []),
        "openings": openings,
        "rebar": rebar,
        "provenance": {
            "source_id": matrix["source"].get("path"),
            "source_sha256": matrix["source"].get("sha256"),
            "source_sheet": matrix.get("beam_axis"),
            "geometry_source_id": geometry.get("source_id"),
            "geometry_source_sha256": geometry.get("source_sha256"),
        },
        "qa": {
            "status": "PENDING",
            "notes": [
                "Pos.1-5 remain symbolic until bar geometry, anchorage and cover are resolved.",
                "Structural calculation is outside this drawing adapter.",
            ],
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("matrix_json", type=Path)
    ap.add_argument("geometry_json", type=Path)
    ap.add_argument("--drawing-level", choices=["SCHEMATIC", "TENDER", "REBAR_DETAIL"], default="SCHEMATIC")
    ap.add_argument("--station-tolerance-mm", type=float, default=5.0)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    matrix = json.loads(args.matrix_json.read_text(encoding="utf-8"))
    geometry = json.loads(args.geometry_json.read_text(encoding="utf-8"))
    spec = build_spec(matrix, geometry, args.drawing_level, args.station_tolerance_mm)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()
