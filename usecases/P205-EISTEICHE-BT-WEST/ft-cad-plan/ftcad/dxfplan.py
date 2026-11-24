"""BeamSheet -> Modellbereich (mm): Kontur, Fugenlinie Halb-FT, Achsen, Auflager, Konsolen, Durchbrüche, Maße."""
from __future__ import annotations

from ezdxf.enums import TextEntityAlignment

from .model import BeamSheet, Opening

LAYERS = {"FT_SCHALUNG": 7, "FT_FUGE": 5, "FT_ACHSE": 8, "FT_KONSOLE": 140, "FT_DURCHBRUCH": 1,
          "FT_ANNO": 7, "FT_BEMASSUNG": 4, "FT_ETA_OK": 3, "FT_ETA_GELB": 30, "FT_ETA_ROT": 1,
          "FT_ETA_FEHLT": 6, "FT_QA": 6, "FT_RAHMEN": 7, "FT_TABELLE": 8, "FT_ORTBETON": 5}
SCALES = (20, 25, 50, 75, 100, 150, 200, 250, 300, 400, 500, 750, 1000)
A3_W, A3_H = 420.0, 297.0
VP_MAIN = {"cx": 212.5, "cy": 190.0, "w": 385.0, "h": 112.0}
VP_OVER = {"cx": 212.5, "cy": 270.0, "w": 385.0, "h": 30.0}
PROJECT = "P205 Schule an den Eisteichen – Bauteil West"
OFFICE = "Tragwerksplanung: Zotter Litschauer ZT GmbH"


def dimov(th: float) -> dict:
    """Maßzahlen in cm (Modell mm): dimlfac 0,1; ganzzahlig."""
    return {"dimtxt": th * 0.8, "dimasz": th * 0.6, "dimlfac": 0.1, "dimdec": 0, "dimexo": th * 0.3}


def pick_scale(len_mm: float, h_mm: float, vp: dict, h_factor: float = 3.0) -> int:
    for s in SCALES:
        if len_mm / s <= vp["w"] and h_mm * h_factor / s <= vp["h"]:
            return s
    return SCALES[-1]


def eta_layer(o: Opening) -> str:
    return {"OK": "FT_ETA_OK", "GELB": "FT_ETA_GELB", "ROT": "FT_ETA_ROT"}.get(o.eta_cls, "FT_ETA_FEHLT")


def eta_txt(o: Opening) -> str:
    star = "" if o.eta_src == "GESAMT" else "*"
    return "η —" if o.eta is None else f"η{star} {o.eta * 100:.0f}%"


def _steps(cont: list[tuple[float, float, float]], idx: int, sub: int = 0) -> list[tuple[float, float]]:
    """Stufenlinie über Stationen (Wechsel in Feldmitte zwischen zwei Stationen). y = (h − h1·sub) [mm]."""
    pts = []
    for i, (x, h, h1) in enumerate(cont):
        y = (h - (h1 if sub else 0)) * 10
        xa = x if i == 0 else (cont[i - 1][0] + x) / 2
        xb = x if i == len(cont) - 1 else (x + cont[i + 1][0]) / 2
        pts += [(xa * 1000, y), (xb * 1000, y)]
    return pts


def runs(cont: list[tuple[float, float, float]]) -> list[list[tuple[float, float, float]]]:
    """Kontur in FT-Elemente teilen: Lücke (Stationen mit h = 0) > 1,6 × Stationsraster = neues Element."""
    if len(cont) < 2:
        return [cont] if cont else []
    step = sorted(b[0] - a[0] for a, b in zip(cont, cont[1:]))[len(cont) // 2 - 1]
    out, cur = [], [cont[0]]
    for a, b in zip(cont, cont[1:]):
        if b[0] - a[0] > 1.6 * step:
            out.append(cur)
            cur = []
        cur.append(b)
    return out + [cur]


def draw_body(msp, bs: BeamSheet, th: float) -> None:
    """Je FT-Element: Schalungskontur (h je Station, Z17) + Fugenlinie FT/Ortbeton (h − h1, Z18); Achsen (Z12)."""
    for n, run in enumerate(runs(bs.contour), 1):
        x0, x1 = run[0][0] * 1000, run[-1][0] * 1000
        msp.add_lwpolyline([(x0, 0)] + _steps(run, 1) + [(x1, 0)], close=True, dxfattribs={"layer": "FT_SCHALUNG"})
        fuge = msp.add_lwpolyline(_steps(run, 1, sub=1), dxfattribs={"layer": "FT_FUGE", "linetype": "DASHED",
                                                                      "ltscale": 0.12 * th})
        fuge.dxf.flags |= 128  # PLINEGEN: Linientyp über Stützpunkte fortlaufend
        msp.add_text(f"FT{n}  x {run[0][0]:.2f}–{run[-1][0]:.2f} m", height=th * 0.8,
                     dxfattribs={"layer": "FT_ANNO"}).set_placement(((x0 + x1) / 2, -6 * th),
                                                                   align=TextEntityAlignment.MIDDLE_CENTER)
    hmax = max(c[1] for c in bs.contour) * 10
    for name, x in bs.axes:
        xm = x * 1000
        msp.add_line((xm, -6 * th), (xm, hmax + 2 * th), dxfattribs={"layer": "FT_ACHSE", "linetype": "DASHDOT",
                                                                       "ltscale": 0.12 * th})
        msp.add_lwpolyline([(xm, 0), (xm - th, -1.5 * th), (xm + th, -1.5 * th)], close=True,
                           dxfattribs={"layer": "FT_SCHALUNG"})
        msp.add_circle((xm, -8 * th), th * 1.3, dxfattribs={"layer": "FT_ACHSE"})
        msp.add_text(name, height=th * 1.3, dxfattribs={"layer": "FT_ANNO"}).set_placement(
            (xm, -8 * th), align=TextEntityAlignment.MIDDLE_CENTER)
    for x, side in bs.corbels:
        xm, d = x * 1000, (-1 if side == 1 else 1)
        msp.add_lwpolyline([(xm, 0), (xm + d * 2 * th, 0), (xm + d * 2 * th, -th), (xm, -2 * th)], close=True,
                           dxfattribs={"layer": "FT_KONSOLE"})
        msp.add_text("K", height=th, dxfattribs={"layer": "FT_KONSOLE"}).set_placement(
            (xm + d * th, -3.2 * th), align=TextEntityAlignment.MIDDLE_CENTER)
