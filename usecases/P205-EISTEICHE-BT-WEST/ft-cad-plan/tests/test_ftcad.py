"""pytest: synthetische Mappe im echten Zeilenmodell (Labels Spalte E/A, MRd-Katalog Z9–16).
Geometrie/Pos 4OG-2 U/X/AA aus RevE; Fehlerfälle (4d23, #REF!, η>1,05) künstlich."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

pytest.importorskip("ezdxf")
from openpyxl import Workbook

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ftcad.model import beam_from_dict, eta_class, parse_rebar  # noqa: E402
from run_ft_cad import run  # noqa: E402

LAB = {15: (5, "Konsole (1…links; 2…rechts)"), 16: (5, "Breite"), 17: (5, "Gesamthöhe"),
       18: (5, "Höhe Vergussfuge"), 19: (5, "Breite Durchbruch"), 20: (5, "Höhe Durchbruch"),
       21: (5, "Höhe unten"), 161: (1, "Pos.1"), 163: (1, "Pos.2"), 165: (1, "Pos.3 "), 167: (1, "Pos.4"),
       169: (1, "Pos.5"), 245: (1, "GESAMTAUSLASTUNG")}
DB = {  # Spalte: (b,d, h,d, h,u,d, p1..p5, η)
    21: (45, 15, 31, "4d10", "2d10/20", "4d12", "4d10", "2d10/18", 0.951),
    24: (45, 15, 31, "6d10", "2d10/10", "4d16", "4d12", "2d10/11", 1.03),
    27: (45, 15, 16, "4d10", "2d10/10", "4d23", "4d10", "2d10/16", 1.12),
    30: (45, 15, 16, "4d10", "2d10/10", "4d14", "4d10", "2d10/16", "#REF!"),
}


def _sheet(wb, name: str, eta_row: bool) -> None:
    ws = wb.create_sheet(name)
    for r, (c, t) in LAB.items():
        if r != 245 or eta_row:
            ws.cell(r, c, t)
    for i, c in enumerate(range(7, 44)):          # G..AQ, Raster 1,35 m, Achsen alle 6 Stationen
        ws.cell(10, c, round(i * 1.35, 2))
        if i % 6 == 0:
            ws.cell(12, c, "ABCDEFG"[i // 6])
        h = 0 if i == 18 else (80 if i < 24 else 65)  # Lücke bei i=18 → 2 FT-Elemente
        ws.cell(16, c, 40), ws.cell(17, c, h), ws.cell(18, c, 15)
    ws.cell(15, 8, 1), ws.cell(15, 30, 2)
    for c, v in DB.items():
        for r, x in zip((19, 20, 21, 161, 163, 165, 167, 169, 245), v):
            ws.cell(r, c, x)
        for r in (162, 164, 166, 168, 170):
            ws.cell(r, c, 0.5)


def _fixture(p: Path) -> Path:
    wb = Workbook()
    wb.active.title = "Übersicht"
    m = wb.create_sheet("MRd")
    for r, vals in {9: ["BT02", "BT04", "BT21"], 11: [40, 40, 40], 12: [80, 65, 80], 13: [15, 15, 15],
                    14: [24, 24, 32], 15: [35, 35, 35], 16: [10, 10, 10]}.items():
        for j, v in enumerate(vals):
            m.cell(r, 7 + j, v)
    _sheet(wb, "4OG-2", True)
    _sheet(wb, "3OG-IJ_RO260821", False)
    wb.save(p)
    return p


def test_rebar_parser():
    assert abs(parse_rebar("2d10/20").as_cm2 - 7.854) < 1e-3 and abs(parse_rebar("4d12").as_cm2 - 4.524) < 1e-3
    assert not parse_rebar("4d23").valid and not parse_rebar("4d10/30/33").valid


@pytest.mark.parametrize("eta,cls", [(0.99, "OK"), (1.0, "OK"), (1.04, "GELB"), (1.051, "ROT"),
                                     (None, "FEHLT"), (-0.2, "NEGATIV")])
def test_eta_class(eta, cls):
    assert eta_class(eta) == cls


def test_pipeline(tmp_path: Path):
    r = {x["sheet"]: x for x in run(_fixture(tmp_path / "t.xlsx"), None, None, tmp_path / "o", None, True)}
    a, b = r["4OG-2"], r["3OG-IJ_RO260821"]
    assert a["readback"] == "PASS" and a["openings"] == 4
    assert a["eta"] == {"OK": 1, "GELB": 1, "ROT": 1, "FEHLT": 1}
    assert a["status"].startswith("VORABZUG") and a["axis_group"] == "765" and b["axis_group"] == "ABC"
    assert any("Teil-η" in g for g in b["gate_reasons"])
    assert (tmp_path / "o" / "P205_FT_4OG-2.pdf").stat().st_size > 5000
    assert list((tmp_path / "o").glob("P205_FT_4OG-2_Blatt1_*.ps"))


def test_model_content(tmp_path: Path):
    run(_fixture(tmp_path / "t.xlsx"), ["4OG-2"], None, tmp_path / "o", None, False)
    bs = beam_from_dict(json.loads((tmp_path / "o" / "4OG-2_FTBeam.json").read_text(encoding="utf-8")))
    assert [a[0] for a in bs.axes] == list("ABCDEFG") and bs.corbels == [(1.35, 1), (31.05, 2)]
    from ftcad.dxfplan import runs
    assert len(runs(bs.contour)) == 2
    sec = {(s["b"], s["h"]): s for s in bs.sections}
    assert sec[(40.0, 65.0)]["bi"] == 24 and sec[(40.0, 80.0)]["bi"] is None
    assert bs.openings[2].pos[2].issue.startswith("d=23") and bs.openings[0].h1_cm == 15
