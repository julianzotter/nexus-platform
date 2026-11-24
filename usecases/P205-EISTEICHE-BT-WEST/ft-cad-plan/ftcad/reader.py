"""Excel FT-Matrix -> BeamSheet. Read-only, gespeicherte Werte, SHA256 + Zellbezug je Wert, Label-Lookup."""
from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter as L

from .model import BeamSheet, Opening, parse_rebar

CFG_DEFAULT = Path(__file__).resolve().parent.parent / "config" / "rowmap_layoutB.json"
RE_SHEET = re.compile(r"^(EG|[1-4]OG)-([A-Z]+|\d+)(?:_RO\d+)?$")
FIRST_COL = 7  # Spalte G = erste Ergebnisspalte (Station 0)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def classify_sheet(name: str) -> tuple[str, str, str] | None:
    """'4OG-2' -> ('4OG','2','765'); '3OG-IJ_RO260821' -> ('3OG','IJ','ABC'). Annahme: Ziffern=765, Buchst.=ABC."""
    m = RE_SHEET.match(name)
    if not m:
        return None
    return m.group(1), m.group(2), ("765" if m.group(2).isdigit() else "ABC")


def _num(v: object) -> float | None:
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    return float(v) if math.isfinite(float(v)) else None


def _is_err(v: object) -> bool:
    return isinstance(v, str) and v.strip().startswith("#")


class Grid:
    """Wertematrix eines Blatts (1-basiert), einmal gelesen."""
    def __init__(self, ws, max_row: int):
        self.v = [list(r) for r in ws.iter_rows(min_row=1, max_row=max_row, values_only=True)]
        self.ncol = max((len(r) for r in self.v), default=0)

    def get(self, r: int, c: int) -> object:
        return self.v[r - 1][c - 1] if 0 < r <= len(self.v) and 0 < c <= len(self.v[r - 1]) else None


def find_rows(g: Grid, cfg: dict) -> tuple[dict[str, int | None], list[str]]:
    """Feste Zeilen (station/grid) + Label-Lookup (erster Treffer ab min_row in Spalten A–G)."""
    rows, notes = {}, []
    for key, spec in cfg["fields"].items():
        if "row" in spec:
            rows[key] = spec["row"]
            continue
        pats = [re.compile(p) for p in spec["labels"]]
        hit = next((r for r in range(spec.get("min_row", 1), len(g.v) + 1)
                    for c in range(1, cfg["label_cols"] + 1)
                    if isinstance(g.get(r, c), str) and any(p.search(g.get(r, c).strip()) for p in pats)), None)
        rows[key] = hit
        if hit is None and not spec.get("optional"):
            notes.append(f"Label für '{key}' nicht gefunden")
    return rows, notes


def load_bt_catalog(wb, cfg: dict) -> list[dict]:
    """BT-Querschnittskatalog aus MRd (b, h, h1, bi [cm], c, d_bü [mm])."""
    bc = cfg["bt_catalog"]
    g = Grid(wb[bc["sheet"]], 20)
    out = []
    for c in range(bc["first_col"], g.ncol + 1):
        name = g.get(bc["name_row"], c)
        if not (isinstance(name, str) and name.startswith("BT")):
            continue
        rec = {"bt": name, "col": L(c)}
        rec.update({k: _num(g.get(r, c)) for k, r in bc["rows"].items()})
        out.append(rec)
    return out


def match_section(b: float, h: float, h1: float, cat: list[dict]) -> dict:
    """Querschnitt über (b, h, h1) im Katalog suchen; mehrdeutige bi werden als Befund markiert."""
    hits = [t for t in cat if t["b"] == b and t["h"] == h and t["h1"] is not None and abs(t["h1"] - h1) < 0.02]
    bis = sorted({t["bi"] for t in hits})
    return {"b": b, "h": h, "h1": h1, "bts": [t["bt"] for t in hits],
            "bi": bis[0] if len(bis) == 1 else None, "c_mm": hits[0]["c_mm"] if hits else None,
            "issue": "" if len(bis) == 1 else ("kein BT-Typ" if not hits else f"bi mehrdeutig {bis}")}


def _col_values(g: Grid, c: int, rows: dict) -> tuple[dict, dict, list[str]]:
    vals, cells, issues = {}, {}, []
    for k, r in rows.items():
        v = g.get(r, c) if r else None
        cells[k] = f"{L(c)}{r}" if r else "-"
        if _is_err(v):
            issues.append(f"{k}={v} @{cells[k]}")
            v = None
        vals[k] = v
    return vals, cells, issues


def _eta(g: Grid, c: int, rows: dict, v: dict) -> tuple[float | None, str]:
    """GESAMTAUSLASTUNG, sonst max(Pos-Nachweiszeilen = Pos-Zeile + 1) als Teil-η."""
    if rows.get("eta"):
        return _num(v["eta"]), "GESAMT"
    part = [_num(g.get(rows[f"pos{i}"] + 1, c)) for i in range(1, 6) if rows.get(f"pos{i}")]
    part = [x for x in part if x is not None]
    return (max(part) if part else None), "POS"


def _opening(g: Grid, c: int, rows: dict) -> Opening | None:
    v, cells, issues = _col_values(g, c, rows)
    geo = [_num(v[k]) for k in ("station", "b", "h", "db_b", "db_h", "hu")]
    if None in geo or geo[3] <= 0 or geo[4] <= 0:
        return None
    pos = [parse_rebar(v[f"pos{i}"]) for i in range(1, 6)]
    issues += [f"Pos.{i}: {p.raw!r} {p.issue}" for i, p in enumerate(pos, 1) if not p.valid]
    eta, src = _eta(g, c, rows, v)
    o = Opening(L(c), *geo, pos, eta, cells, issues, _num(v["h1"]) or 0.0, src)
    if o.ho_cm <= 0:
        o.issues.append(f"Geometrie: h_o={o.ho_cm:g} cm ≤ 0")
    return o


def read_sheet(g: Grid, title: str, rows: dict, cat: list[dict], src: Path, digest: str) -> BeamSheet:
    storey, axis, grp = classify_sheet(title)
    ops, axes, corb, cont, last, keys = [], [], [], [], None, set()
    for c in range(FIRST_COL, g.ncol + 1):
        x = _num(g.get(rows["station"], c))
        if x is None:
            continue
        raw = g.get(rows["grid"], c)
        letter = (f"{raw:g}" if isinstance(raw, (int, float)) and not isinstance(raw, bool) else str(raw or "")).strip()
        if letter and letter != last:   # Achse: Buchstabe (765-Blätter) oder Zahl 7…1 (ABC-Blätter), Z12
            axes.append((letter, x))
            last = letter
        k = _num(g.get(rows["kons"], c)) if rows.get("kons") else None
        if k in (1.0, 2.0):
            corb.append((x, int(k)))
        h, h1 = _num(g.get(rows["h"], c)), _num(g.get(rows["h1"], c))
        if h and h > 0:
            cont.append((x, h, h1 or 0.0))
            keys.add((_num(g.get(rows["b"], c)) or 0.0, h, h1 or 0.0))
        o = _opening(g, c, rows)
        if o:
            ops.append(o)
    secs = [match_section(b, h, h1, cat) for b, h, h1 in sorted(keys)]  # alle Querschnitte entlang Träger
    xs = [p[0] for p in cont] or [0.0, 1.0]
    return BeamSheet(title, storey, axis, grp, ops, src.name, digest, min(xs), max(xs),
                     axes=axes, corbels=corb, contour=cont, sections=secs)


def load_workbook_sheets(xlsx: Path, sheets: list[str] | None = None,
                         cfg_path: Path = CFG_DEFAULT) -> list[BeamSheet]:
    """Liest Ergebnisblätter EG…4OG (oder Auswahl). Quelle bleibt unverändert."""
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    digest = sha256(xlsx)
    wb = load_workbook(xlsx, data_only=True, read_only=True)
    cat = load_bt_catalog(wb, cfg)
    out = []
    for n in sheets or [n for n in wb.sheetnames if classify_sheet(n)]:
        g = Grid(wb[n], cfg["max_row"])
        rows, notes = find_rows(g, cfg)
        bs = read_sheet(g, n, rows, cat, xlsx, digest)
        bs.issues += notes + [f"Querschnitt {s['b']:g}/{s['h']:g}/h1 {s['h1']:g}: {s['issue']}"
                              for s in bs.sections if s["issue"]]
        if not rows.get("eta"):
            bs.issues.append("keine Zeile GESAMTAUSLASTUNG → η = max(Pos.1–5-Nachweis) (Teil-η)")
        if bs.openings and all(o.eta is None for o in bs.openings):
            bs.issues.append("η ohne gespeicherte Werte → Excel CalculateFullRebuild")
        out.append(bs)
    return out
