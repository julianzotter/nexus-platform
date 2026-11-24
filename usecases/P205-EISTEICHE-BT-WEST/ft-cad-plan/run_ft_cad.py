#!/usr/bin/env python3
"""CLI: FT-Matrix (xlsx) -> kanonisches JSON -> DXF -> PDF/PS -> QA-Readback -> RUNLOG (append-only).

Beispiele:
  python run_ft_cad.py MATRIX.xlsx --sheets 4OG-2 --out OUT        # Golden-Slice-Pilot
  python run_ft_cad.py MATRIX.xlsx --all --out OUT                 # EG–4OG, Achsgruppen ABC + 765
  python run_ft_cad.py MATRIX.xlsx --all --storey EG 1OG --out OUT
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from ftcad.qa import readback, summary
from ftcad.reader import load_workbook_sheets
from ftcad.render import render
from ftcad.sheetset import build_dxf


def run(xlsx: Path, sheets: list[str] | None, storeys: list[str] | None, out: Path,
        approved_by: str | None, postscript: bool) -> list[dict]:
    out.mkdir(parents=True, exist_ok=True)
    results = []
    for bs in load_workbook_sheets(xlsx, sheets):
        if storeys and bs.storey not in storeys:
            continue
        if not bs.openings or not bs.contour:
            results.append({"sheet": bs.sheet, "status": "SKIP – keine Durchbrüche", "issues": bs.issues})
            continue
        (out / f"{bs.sheet}_FTBeam.json").write_text(json.dumps(bs.to_dict(), ensure_ascii=False, indent=1),
                                                     encoding="utf-8")
        meta = build_dxf(bs, out / f"P205_FT_{bs.sheet}.dxf", approved_by)
        files = render(out / meta["dxf"], out, postscript)
        results.append({**meta, **summary(bs), **readback(out / meta["dxf"], bs),
                        "files": [f.name for f in files]})
    return results


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("xlsx", type=Path)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--sheets", nargs="+")
    g.add_argument("--all", action="store_true")
    ap.add_argument("--storey", nargs="+", choices=["EG", "1OG", "2OG", "3OG", "4OG"])
    ap.add_argument("--out", type=Path, default=Path("OUT_FT_CAD"))
    ap.add_argument("--approved-by", help="nur ID01 nach Prüfung – sonst Stempel VORABZUG")
    ap.add_argument("--no-ps", action="store_true")
    a = ap.parse_args()
    res = run(a.xlsx, None if a.all else a.sheets, a.storey, a.out, a.approved_by, not a.no_ps)
    stamp = datetime.now().astimezone().isoformat(timespec="seconds")
    (a.out / "RUN_RESULT.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(a.out / "RUNLOG.md", "a", encoding="utf-8") as log:
        log.write(f"- {stamp} | ft-cad-plan | {a.xlsx.name} | {len(res)} Blätter | "
                  f"readback FAIL: {sum(r.get('readback') == 'FAIL' for r in res)} | "
                  f"freigegeben: {sum(r.get('status') == 'FREIGEGEBEN' for r in res)}\n")
    for r in res:
        print(f"{r['sheet']:>16} | {r.get('openings', 0):>3} DB | η {r.get('eta', {})} | "
              f"{r.get('readback', '-')} | {r.get('status')}")


if __name__ == "__main__":
    main()
