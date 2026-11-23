from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

from openpyxl import load_workbook

ROW_MAP = {
    "station_m": 10,
    "beam_b_cm": 16,
    "beam_h_cm": 17,
    "opening_b_cm": 19,
    "opening_h_cm": 20,
    "opening_hu_cm": 21,
    "pos1": 161,
    "pos2": 163,
    "pos3": 165,
    "pos4": 167,
    "pos5": 169,
    "eta": 252,
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def num(v: Any) -> float | None:
    if isinstance(v, (int, float)) and math.isfinite(float(v)):
        return float(v)
    return None


def txt(v: Any) -> str:
    return "" if v is None else str(v).strip()


def extract(path: Path, sheet: str, expected_sha256: str) -> dict[str, Any]:
    actual = sha256_file(path)
    if actual.lower() != expected_sha256.lower():
        raise ValueError(f"SHA256 mismatch: expected {expected_sha256}, got {actual}")

    wb = load_workbook(path, data_only=True, read_only=True)
    if sheet not in wb.sheetnames:
        raise KeyError(f"sheet not found: {sheet}")
    ws = wb[sheet]

    records: list[dict[str, Any]] = []
    stations: list[float] = []
    for c in range(1, ws.max_column + 1):
        st = num(ws.cell(ROW_MAP["station_m"], c).value)
        if st is not None:
            stations.append(st)
        dbb = num(ws.cell(ROW_MAP["opening_b_cm"], c).value)
        dbh = num(ws.cell(ROW_MAP["opening_h_cm"], c).value)
        if st is None or dbb is None or dbh is None or dbb <= 0 or dbh <= 0:
            continue
        records.append({
            "column": ws.cell(1, c).column_letter,
            "station_mm": st * 1000.0,
            "beam_b_mm": (num(ws.cell(ROW_MAP["beam_b_cm"], c).value) or 0.0) * 10.0,
            "beam_h_mm": (num(ws.cell(ROW_MAP["beam_h_cm"], c).value) or 0.0) * 10.0,
            "opening_b_mm": dbb * 10.0,
            "opening_h_mm": dbh * 10.0,
            "opening_hu_mm": (num(ws.cell(ROW_MAP["opening_hu_cm"], c).value) or 0.0) * 10.0,
            "pos": {
                "P1": txt(ws.cell(ROW_MAP["pos1"], c).value),
                "P2": txt(ws.cell(ROW_MAP["pos2"], c).value),
                "P3": txt(ws.cell(ROW_MAP["pos3"], c).value),
                "P4": txt(ws.cell(ROW_MAP["pos4"], c).value),
                "P5": txt(ws.cell(ROW_MAP["pos5"], c).value),
            },
            "eta": num(ws.cell(ROW_MAP["eta"], c).value),
        })

    return {
        "schema_version": "p205-ft-matrix-semantics-0.1",
        "source": {
            "path": str(path),
            "sha256": actual,
            "sheet": sheet,
            "row_map": ROW_MAP,
            "read_mode": "openpyxl data_only=True read_only=True",
            "warning": "cached workbook values only; this script does not recalculate Excel",
        },
        "beam_axis": sheet,
        "station_range_mm": [
            min(stations) * 1000.0 if stations else None,
            max(stations) * 1000.0 if stations else None,
        ],
        "openings": records,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("workbook", type=Path)
    ap.add_argument("--sheet", required=True)
    ap.add_argument("--expected-sha256", required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    data = extract(args.workbook, args.sheet, args.expected_sha256)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()
