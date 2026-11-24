"""Kanonisches FT-Träger-Modell (SSOT für DXF/PDF/QA). Einheiten: cm, m, cm², %."""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field, asdict

D_CATALOG: tuple[int, ...] = (6, 8, 10, 12, 14, 16, 20, 25, 28, 32)  # mm, Stabkatalog
_RE_BAR = re.compile(r"^\s*(\d+)\s*[dØø]\s*(\d+)\s*(?:/\s*(\d+(?:[.,]\d+)?))?\s*$")
ETA_LIMIT_GREEN = 1.00   # η ≤ 1,00  -> OK
ETA_LIMIT_YELLOW = 1.05  # 1,00 < η ≤ 1,05 -> GELB (Projektvorgabe max. 105 %)


@dataclass(frozen=True)
class Rebar:
    """Bewehrungsangabe Pos.1–5, z. B. '4d10' (Stäbe) oder '2d10/20' (Bügel, s in cm)."""
    raw: str
    n: int | None = None
    d_mm: int | None = None
    s_cm: float | None = None
    valid: bool = False
    issue: str = ""

    @property
    def as_cm2(self) -> float | None:
        """Stäbe: As = n·π·d²/4 [cm²]; Bügel: a_sw = n·π·d²/4 · 100/s [cm²/m]."""
        if not self.valid or self.n is None or self.d_mm is None:
            return None
        a = self.n * math.pi * (self.d_mm / 10.0) ** 2 / 4.0
        return a * 100.0 / self.s_cm if self.s_cm else a

    @property
    def label(self) -> str:
        return self.raw.replace("d", "Ø") if self.valid else f"{self.raw} (!)"


def parse_rebar(raw: object) -> Rebar:
    """Parst Pos-Angaben streng; Katalogfehler (z. B. '4d23') werden markiert, nicht korrigiert."""
    txt = "" if raw is None else str(raw).strip()
    if not txt or txt in {"--", "-", "—"}:
        return Rebar(txt, issue="leer")
    m = _RE_BAR.match(txt)
    if not m:
        return Rebar(txt, issue="Format")
    n, d = int(m.group(1)), int(m.group(2))
    s = float(m.group(3).replace(",", ".")) if m.group(3) else None
    if d not in D_CATALOG:
        return Rebar(txt, n, d, s, False, f"d={d} nicht im Katalog")
    if s is not None and not (5.0 <= s <= 30.0):
        return Rebar(txt, n, d, s, False, f"s={s:g} cm unplausibel")
    return Rebar(txt, n, d, s, True)


def eta_class(eta: float | None) -> str:
    """Ampel nach Projektvorgabe (max. 105 %)."""
    if eta is None or not math.isfinite(eta):
        return "FEHLT"
    if eta < 0:
        return "NEGATIV"
    if eta <= ETA_LIMIT_GREEN:
        return "OK"
    return "GELB" if eta <= ETA_LIMIT_YELLOW else "ROT"


@dataclass
class Opening:
    """Ein Durchbruch = eine Ergebnisspalte im Geschossblatt."""
    col: str
    station_m: float
    beam_b_cm: float
    beam_h_cm: float
    db_b_cm: float
    db_h_cm: float
    hu_cm: float
    pos: list[Rebar]
    eta: float | None
    cells: dict[str, str] = field(default_factory=dict)
    issues: list[str] = field(default_factory=list)
    h1_cm: float = 0.0
    eta_src: str = "GESAMT"   # GESAMT = Z 'GESAMTAUSLASTUNG'; POS = max(Pos.1–5-Nachweis) = Teil-η

    @property
    def ho_cm(self) -> float:
        """Oberer Restgurt h_o = h − h_u − h_DB."""
        return self.beam_h_cm - self.hu_cm - self.db_h_cm

    @property
    def eta_cls(self) -> str:
        return eta_class(self.eta)


@dataclass
class BeamSheet:
    """Ein Geschoss-/Achsblatt der FT-Matrix (z. B. '4OG-2')."""
    sheet: str
    storey: str
    axis: str
    axis_group: str
    openings: list[Opening]
    source_file: str
    source_sha256: str
    x_min_m: float
    x_max_m: float
    issues: list[str] = field(default_factory=list)
    axes: list[tuple[str, float]] = field(default_factory=list)        # (Achse, x [m]) aus Z12
    corbels: list[tuple[float, int]] = field(default_factory=list)     # (x [m], 1=links/2=rechts) aus Z15
    contour: list[tuple[float, float, float]] = field(default_factory=list)  # (x [m], h [cm], h1 [cm])
    sections: list[dict] = field(default_factory=list)                 # BT-Querschnitte (MRd-Katalog)

    def to_dict(self) -> dict:
        d = asdict(self)
        for o, od in zip(self.openings, d["openings"]):
            od["ho_cm"] = round(o.ho_cm, 2)
            od["eta_cls"] = o.eta_cls
            od["pos"] = [{"raw": p.raw, "valid": p.valid, "issue": p.issue,
                          "as_cm2": None if p.as_cm2 is None else round(p.as_cm2, 3)}
                         for p in o.pos]
        return d


def beam_from_dict(d: dict) -> BeamSheet:
    """Inverse zu BeamSheet.to_dict() – Eingang für Dashboard/Pyodide (kein openpyxl nötig)."""
    ops = [Opening(o["col"], o["station_m"], o["beam_b_cm"], o["beam_h_cm"], o["db_b_cm"], o["db_h_cm"],
                   o["hu_cm"], [parse_rebar(p["raw"]) for p in o["pos"]], o["eta"], o.get("cells", {}),
                   o.get("issues", []), o.get("h1_cm", 0.0), o.get("eta_src", "GESAMT")) for o in d["openings"]]
    return BeamSheet(d["sheet"], d["storey"], d["axis"], d["axis_group"], ops, d["source_file"],
                     d["source_sha256"], d["x_min_m"], d["x_max_m"], d.get("issues", []),
                     [tuple(a) for a in d.get("axes", [])], [tuple(c) for c in d.get("corbels", [])],
                     [tuple(c) for c in d.get("contour", [])], d.get("sections", []))
