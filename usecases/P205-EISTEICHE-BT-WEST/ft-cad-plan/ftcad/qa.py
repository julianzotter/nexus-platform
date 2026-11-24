"""Readback-QA: DXF-Geometrie gegen kanonisches Modell (Toleranz 1 mm) + Plausibilität."""
from __future__ import annotations

from pathlib import Path

import ezdxf

from .model import BeamSheet

TOL_MM = 1.0


def readback(dxf_path: Path, bs: BeamSheet) -> dict:
    """Prüft: Anzahl Durchbruch-Polylinien, Lage/Größe je DB, Layer vorhanden. Binär PASS/FAIL."""
    doc = ezdxf.readfile(dxf_path)
    rects = []
    for e in doc.modelspace().query('LWPOLYLINE[layer=="FT_DURCHBRUCH"]'):
        xs, ys = zip(*[(p[0], p[1]) for p in e.get_points()])
        rects.append(((min(xs) + max(xs)) / 2, min(ys), max(xs) - min(xs), max(ys) - min(ys)))
    fails = []
    if len(rects) != len(bs.openings):
        fails.append(f"Anzahl DB: DXF {len(rects)} ≠ Modell {len(bs.openings)}")
    for o, (cx, y0, w, h) in zip(bs.openings, sorted(rects)):
        exp = (o.station_m * 1000, o.hu_cm * 10, o.db_b_cm * 10, o.db_h_cm * 10)
        if any(abs(a - b) > TOL_MM for a, b in zip((cx, y0, w, h), exp)):
            fails.append(f"{o.col}: DXF {cx:.0f}/{y0:.0f}/{w:.0f}/{h:.0f} ≠ {exp}")
    return {"sheet": bs.sheet, "readback": "PASS" if not fails else "FAIL", "fails": fails,
            "layouts": [n for n in doc.layouts.names_in_taborder() if n != "Model"]}


def summary(bs: BeamSheet) -> dict:
    """η-Ampel-Zählung + Datenbefunde je Blatt (für Statuszettel/Ledger)."""
    cnt: dict[str, int] = {}
    for o in bs.openings:
        cnt[o.eta_cls] = cnt.get(o.eta_cls, 0) + 1
    return {"sheet": bs.sheet, "storey": bs.storey, "axis": bs.axis, "axis_group": bs.axis_group,
            "openings": len(bs.openings), "eta": cnt,
            "eta_max": max((o.eta for o in bs.openings if o.eta is not None), default=None),
            "data_issues": sum(len(o.issues) for o in bs.openings), "sheet_issues": bs.issues}
