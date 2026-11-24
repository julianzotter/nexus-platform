"""Durchbrüche + Bemaßung (Modell), Positionstabelle + Halb-FT-Querschnitte 1:20 (Papier)."""
from __future__ import annotations

from ezdxf.enums import TextEntityAlignment

from .dxfplan import dimov, eta_layer, eta_txt
from .model import BeamSheet, Opening


def draw_openings(msp, bs: BeamSheet, th: float) -> None:
    """Durchbruch b,d × h,d auf h,u,d (Z19–21); Nr. + η über Träger; Maß h,u,d; Kette Achse → DB-Mitte."""
    hmax = max(c[1] for c in bs.contour) * 10
    for i, o in enumerate(bs.openings, 1):
        cx, w, hh, y0 = o.station_m * 1000, o.db_b_cm * 10, o.db_h_cm * 10, o.hu_cm * 10
        msp.add_lwpolyline([(cx - w / 2, y0), (cx + w / 2, y0), (cx + w / 2, y0 + hh), (cx - w / 2, y0 + hh)],
                           close=True, dxfattribs={"layer": "FT_DURCHBRUCH"})
        for txt, dy, k in ((f"DB{i}", 1.5, 1.1), (eta_txt(o), 3.2, 0.8)):
            msp.add_text(txt, height=th * k, dxfattribs={"layer": eta_layer(o)}).set_placement(
                (cx, hmax + dy * th), align=TextEntityAlignment.BOTTOM_CENTER)
        msp.add_linear_dim(base=(cx + w / 2 + 2 * th, 0), p1=(cx + w / 2, 0), p2=(cx + w / 2, y0), angle=90,
                           dimstyle="EZDXF", override=dimov(th), dxfattribs={"layer": "FT_BEMASSUNG"}).render()
        ax = max((x for _, x in bs.axes if x <= o.station_m + 1e-6), default=bs.x_min_m) * 1000
        if cx - ax > 1:
            msp.add_linear_dim(base=(ax, -(3 + 1.6 * (i % 2)) * th), p1=(ax, 0), p2=(cx, 0), dimstyle="EZDXF", override=dimov(th),
                               dxfattribs={"layer": "FT_BEMASSUNG"}).render()


def _t(psp, s: str, x: float, y: float, h: float = 1.9, layer: str = "FT_TABELLE") -> None:
    psp.add_text(s, height=h, dxfattribs={"layer": layer}).set_placement((x, y))


COLS = [("DB", 9), ("Sp.", 9), ("x [m]", 14), ("b/h DB", 15), ("h_u", 10), ("h_o", 10), ("h1", 9),
        ("Pos.1 Aufh.", 20), ("Pos.2 Bü o", 22), ("Pos.3 Lä o", 20), ("Pos.4 Lä u", 20), ("Pos.5 Bü u", 22),
        ("η", 14), ("Status", 15)]


def draw_table(psp, rows: list[tuple[int, Opening]], y_top: float = 122.0) -> None:
    """Positionstabelle; Pos-Texte unverändert aus Matrix (Z161–169), Katalogfehler (!)."""
    rh, x = 4.6, 12.0
    for name, w in COLS:
        _t(psp, name, x + 0.8, y_top - 3.4, 1.9)
        x += w
    psp.add_lwpolyline([(12, y_top), (x, y_top), (x, y_top - rh * (len(rows) + 1)),
                        (12, y_top - rh * (len(rows) + 1))], close=True, dxfattribs={"layer": "FT_TABELLE"})
    for r, (i, o) in enumerate(rows, 1):
        y = y_top - rh * r - 3.4
        vals = [f"DB{i}", o.col, f"{o.station_m:.2f}", f"{o.db_b_cm:g}/{o.db_h_cm:g}", f"{o.hu_cm:g}",
                f"{o.ho_cm:g}", f"{o.h1_cm:g}", *[p.label for p in o.pos], eta_txt(o)[2:].strip(), o.eta_cls]
        xx = 12.0
        for (name, w), v in zip(COLS, vals):
            _t(psp, v, xx + 0.8, y, 1.8, eta_layer(o) if name in ("η", "Status") else "FT_TABELLE")
            xx += w
        psp.add_line((12, y - 1.2), (xx, y - 1.2), dxfattribs={"layer": "FT_TABELLE"})
    _t(psp, "η = GESAMTAUSLASTUNG; η* = max(Pos.1–5-Nachweis), Teil-η (Blatt ohne Gesamtzeile). "
            "h1 = Höhe Vergussfuge (Ortbeton).", 12, y_top - rh * (len(rows) + 1) - 4, 1.6, "FT_QA")


def draw_sections(psp, sections: list[dict], x0: float = 262.0, y0: float = 62.0) -> None:
    """Halb-FT-Querschnitte 1:20: Fertigteil b×h mit Vergussfuge bi×h1 oben (Ortbeton, schraffiert)."""
    k, x = 0.5, x0  # 1:20 → cm × 0,5 = mm Papier
    _t(psp, "QUERSCHNITTE 1:20 (BT-Katalog MRd Z11–16)", x0, 122, 2.2, "FT_ANNO")
    for s in sections[:4]:
        b, h, h1 = s["b"] * k, s["h"] * k, s["h1"] * k
        bi = (s["bi"] or 0) * k
        psp.add_lwpolyline([(x, y0), (x + b, y0), (x + b, y0 + h), (x, y0 + h)], close=True,
                           dxfattribs={"layer": "FT_SCHALUNG"})
        if s["bi"] is None and s["issue"].startswith("bi"):
            _t(psp, "Fuge ?", x + 1, y0 + h - 4, 1.6, "FT_QA")
        if s["bi"] and s["bi"] > 0.1:
            xi = x + (b - bi) / 2
            pts = [(xi, y0 + h - h1), (xi + bi, y0 + h - h1), (xi + bi, y0 + h), (xi, y0 + h)]
            psp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "FT_ORTBETON"})
            hat = psp.add_hatch(color=5, dxfattribs={"layer": "FT_ORTBETON"})
            hat.set_pattern_fill("ANSI31", scale=0.25)
            hat.paths.add_polyline_path(pts, is_closed=True)
        lines = [f"{s['b']:g}/{s['h']:g}", f"h1 {s['h1']:g}" + (f" bi {s['bi']:g}" if s["bi"] else " bi ?"),
                 ",".join(s["bts"][:3]) or "BT ?", s["issue"][:18]]
        for j, ln in enumerate(lines):
            _t(psp, ln, x, y0 - 4 - j * 2.6, 1.6, "FT_QA" if j == 3 else "FT_ANNO")
        x += max(b, 22) + 12
