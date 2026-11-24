"""Planblätter A3: Übersicht + Feldausschnitt (2 Felder) je Blatt, Tabelle, Querschnitte, Plankopf, Gate."""
from __future__ import annotations

from datetime import date
from pathlib import Path

import ezdxf

from .annot import draw_openings, draw_sections, draw_table, _t
from .dxfplan import (A3_H, A3_W, LAYERS, OFFICE, PROJECT, VP_MAIN, VP_OVER, draw_body, pick_scale)
from .model import BeamSheet

ANNO_LAYERS = ["FT_ANNO", "FT_BEMASSUNG", "FT_ETA_OK", "FT_ETA_GELB", "FT_ETA_ROT", "FT_ETA_FEHLT", "FT_KONSOLE"]


def gate(bs: BeamSheet, approved_by: str | None) -> tuple[str, list[str]]:
    """FREIGEGEBEN nur: alle η (Gesamt) ≤ 1,05, 0 Datenbefunde, kein Teil-η, Human Gate ID01."""
    r = []
    bad = [o for o in bs.openings if o.eta_cls not in ("OK", "GELB")]
    if bad:
        r.append(f"{len(bad)} DB mit η ROT/FEHLT/NEGATIV")
    if any(o.eta_src != "GESAMT" for o in bs.openings):
        r.append("Teil-η (keine GESAMTAUSLASTUNG)")
    n = sum(len(o.issues) for o in bs.openings) + len(bs.issues)
    if n:
        r.append(f"{n} Datenbefunde")
    if not approved_by:
        r.append("kein Human Gate ID01")
    return ("FREIGEGEBEN" if not r else "VORABZUG – NICHT FREIGEGEBEN"), r


def segments(bs: BeamSheet) -> list[tuple[str, float, float]]:
    """Ausschnitte über je 2 Felder zwischen Achsen (Z12); nur Ausschnitte mit Durchbrüchen."""
    ax = bs.axes if len(bs.axes) >= 2 else [("Anf", bs.x_min_m), ("Ende", bs.x_max_m)]
    if ax[-1][1] < bs.x_max_m - 1e-6:
        ax = ax + [("Ende", bs.x_max_m)]
    segs = [(f"{ax[i][0]}–{ax[min(i + 2, len(ax) - 1)][0]}", ax[i][1], ax[min(i + 2, len(ax) - 1)][1])
            for i in range(0, len(ax) - 1, 2)]
    return [s for s in segs if any(s[1] - 1e-6 <= o.station_m <= s[2] + 1e-6 for o in bs.openings)]


def _viewport(psp, vp: dict, xa: float, xb: float, ya: float, yb: float, scale: float, frozen=()) -> None:
    v = psp.add_viewport(center=(vp["cx"], vp["cy"]), size=(vp["w"], vp["h"]),
                         view_center_point=((xa + xb) / 2, (ya + yb) / 2), view_height=vp["h"] * scale)
    v.dxf.layer = "FT_RAHMEN"
    if frozen:
        v.frozen_layers = list(frozen)


def _titleblock(psp, bs: BeamSheet, seg: str, sc: tuple[int, int], k: int, n: int, status: str, why) -> None:
    psp.add_lwpolyline([(8, 8), (A3_W - 5, 8), (A3_W - 5, A3_H - 5), (8, A3_H - 5)], close=True,
                       dxfattribs={"layer": "FT_RAHMEN", "const_width": 0.5})
    x0 = A3_W - 5 - 150
    psp.add_lwpolyline([(x0, 8), (A3_W - 5, 8), (A3_W - 5, 48), (x0, 48)], close=True, dxfattribs={"layer": "FT_RAHMEN"})
    lines = [(PROJECT, 2.8), (f"FT-Träger {bs.sheet} · Achse {seg} · Blatt {k}/{n}", 2.5),
             (f"Geschoss {bs.storey} · Achsgruppe {bs.axis_group} · M 1:{sc[0]} (Übersicht 1:{sc[1]})", 2.0),
             (f"Quelle {bs.source_file}", 1.6), (f"SHA256 {bs.source_sha256[:20]}… · Plot {date.today():%d.%m.%Y}", 1.6),
             (OFFICE, 1.6)]
    y = 43.0
    for s, h in lines:
        _t(psp, s, x0 + 2, y, h, "FT_RAHMEN")
        y -= h + 3.2
    _t(psp, status, 12, 30, 4.5, "FT_ETA_OK" if status == "FREIGEGEBEN" else "FT_ETA_ROT")
    for j, r in enumerate(why[:4]):
        _t(psp, f"Gate: {r}", 12, 24 - j * 3.0, 1.8, "FT_QA")


def build_dxf(bs: BeamSheet, out: Path, approved_by: str | None = None) -> dict:
    """DXF mit 1 Layout je Ausschnitt (2 Felder). Ein Detailmaßstab je Blatt → einheitliche Texthöhen."""
    if not bs.openings or not bs.contour:
        raise ValueError(f"{bs.sheet}: keine Durchbrüche/Kontur gelesen")
    doc = ezdxf.new("R2018", setup=True, units=4)
    for name, color in LAYERS.items():
        doc.layers.add(name, color=color)
    segs = segments(bs)
    hmax = max(c[1] for c in bs.contour) * 10
    sc = max(pick_scale((b - a) * 1000 + 1500, hmax, VP_MAIN) for _, a, b in segs)
    so = pick_scale((bs.x_max_m - bs.x_min_m) * 1000 + 2000, hmax, VP_OVER, 1.6)
    th = 2.2 * sc
    msp = doc.modelspace()
    draw_body(msp, bs, th)
    draw_openings(msp, bs, th)
    status, why = gate(bs, approved_by)
    idx = list(enumerate(bs.openings, 1))
    for k, (name, a, b) in enumerate(segs, 1):
        psp = doc.layouts.new(f"Blatt{k}_{name}")
        psp.page_setup(size=(A3_W, A3_H), margins=(0, 0, 0, 0), units="mm")
        _viewport(psp, VP_MAIN, a * 1000 - 700, b * 1000 + 700, -10 * th, hmax + 5 * th, sc)
        _viewport(psp, VP_OVER, bs.x_min_m * 1000 - 1000, bs.x_max_m * 1000 + 1000, -500, hmax + 500, so,
                  ANNO_LAYERS)
        draw_table(psp, [(i, o) for i, o in idx if a - 1e-6 <= o.station_m <= b + 1e-6])
        draw_sections(psp, bs.sections)
        _titleblock(psp, bs, name, (sc, so), k, len(segs), status, why)
    if "Layout1" in doc.layouts:
        doc.layouts.delete("Layout1")
    doc.saveas(out)
    return {"sheet": bs.sheet, "dxf": out.name, "scale": sc, "scale_overview": so, "layouts": len(segs),
            "openings": len(bs.openings), "status": status, "gate_reasons": why}
