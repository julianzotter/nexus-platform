"""Pure-function EN 1995-1-1 ULS checks for rectangular timber sections.

PROTOTYPE - not a certified calculation. Human review required.
Units: lengths mm, forces kN, moments kNm, stresses N/mm2.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from .materials import TimberMaterial, design_strength, get_material, get_national_annex, kmod

TOLERANCE = 1.0e-9
KM_RECTANGULAR = 0.7  # EN 1995-1-1 6.1.6(2)
DEFAULT_NA = "AT"  # OENORM B 1995-1-1:2019; use "EN" for the EN 1995-1-1 recommended values


@dataclass(frozen=True)
class CheckResult:
    check: str
    clause: str
    utilization: float
    details: dict = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return self.utilization <= 1.0 + TOLERANCE

    def to_dict(self) -> dict:
        return {
            "check": self.check,
            "clause": self.clause,
            "utilization": self.utilization,
            "pass": self.passed,
            "gate": "PASS" if self.passed else "FAIL",
            "status": "KANDIDAT - PASS (no release)" if self.passed else "KANDIDAT - FAIL",
            "details": self.details,
        }


def _positive(**values: float) -> None:
    for name, value in values.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise ValueError(f"Invalid input {name}: {value!r}")


def _non_negative(**values: float) -> None:
    for name, value in values.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
            raise ValueError(f"Invalid input {name}: {value!r}")


def size_factor(mat: TimberMaterial, dim: float) -> float:
    """kh, EN 1995-1-1 eq. (3.1) solid (h<150) and (3.2) glulam (h<600)."""
    if mat.glulam:
        return 1.0 if dim >= 600.0 else min(1.1, (600.0 / dim) ** 0.1)
    return 1.0 if dim >= 150.0 else min(1.3, (150.0 / dim) ** 0.2)


def _kmod(material: str, service_class: int, load_duration: str) -> tuple[TimberMaterial, float]:
    return get_material(material), kmod(service_class, load_duration)


def lateral_torsional_kcrit(mat: TimberMaterial, b: float, h: float, lef: float) -> tuple[float, float]:
    """kcrit and relative slenderness, EN 1995-1-1 6.3.3 (eq. 6.32, 6.34, 6.35)."""
    _positive(lef=lef)
    sigma_m_crit = 0.78 * b**2 / (h * lef) * mat.E005
    lam_rel_m = math.sqrt(mat.fmk / sigma_m_crit)
    if lam_rel_m <= 0.75:
        return 1.0, lam_rel_m
    if lam_rel_m <= 1.4:
        return 1.56 - 0.75 * lam_rel_m, lam_rel_m
    return 1.0 / lam_rel_m**2, lam_rel_m


def check_bending(*, material: str, b: float, h: float, My: float, Mz: float = 0.0,
                  service_class: int = 1, load_duration: str = "medium",
                  lef: float | None = None) -> CheckResult:
    """Bending about y (strong, depth h) and optionally z, EN 1995-1-1 6.1.6 eq. (6.11)/(6.12).

    lef (effective length for lateral torsional buckling, 6.3.3) is optional;
    without it the compression edge is assumed laterally restrained (kcrit = 1).
    """
    _positive(b=b, h=h)
    _non_negative(My=My, Mz=Mz)
    mat, k = _kmod(material, service_class, load_duration)
    fmd_y = design_strength(mat.fmk, k, mat.gammaM, size_factor(mat, h))
    fmd_z = design_strength(mat.fmk, k, mat.gammaM, size_factor(mat, b))
    sigma_y = My * 1e6 / (b * h**2 / 6.0)
    sigma_z = Mz * 1e6 / (h * b**2 / 6.0)
    kcrit, lam_rel_m = (1.0, None) if lef is None else lateral_torsional_kcrit(mat, b, h, lef)
    ratio_y = sigma_y / (kcrit * fmd_y) + KM_RECTANGULAR * sigma_z / fmd_z
    ratio_z = KM_RECTANGULAR * sigma_y / (kcrit * fmd_y) + sigma_z / fmd_z
    return CheckResult("bending", "EN 1995-1-1 6.1.6", max(ratio_y, ratio_z), {
        "material": material, "kmod": k, "fmd_y": fmd_y, "fmd_z": fmd_z,
        "sigma_m_y": sigma_y, "sigma_m_z": sigma_z, "kcrit": kcrit, "lambda_rel_m": lam_rel_m,
    })


def check_shear(*, material: str, b: float, h: float, V: float,
                service_class: int = 1, load_duration: str = "medium",
                national_annex: str = DEFAULT_NA) -> CheckResult:
    """Shear with cracking factor kcr, EN 1995-1-1 6.1.7 eq. (6.13), (6.13a)."""
    _positive(b=b, h=h)
    _non_negative(V=V)
    mat, k = _kmod(material, service_class, load_duration)
    kcr = get_national_annex(national_annex).kcr
    fvd = design_strength(mat.fvk, k, mat.gammaM)
    tau = 1.5 * V * 1e3 / (kcr * b * h)
    return CheckResult("shear", "EN 1995-1-1 6.1.7", tau / fvd,
                       {"material": material, "kmod": k, "fvd": fvd, "tau_d": tau, "kcr": kcr,
                        "national_annex": national_annex})


def check_compression_perpendicular(*, material: str, b: float, contact_length: float, F: float,
                                    service_class: int = 1, load_duration: str = "medium",
                                    kc90: float | None = None, support: str | None = None,
                                    national_annex: str = DEFAULT_NA) -> CheckResult:
    """Bearing, EN 1995-1-1 6.1.5 eq. (6.3), (6.4). Effective contact length is the caller's input
    (add 30 mm per side where 6.1.5(1) allows).

    kc,90 precedence: explicit kc90, else support ("continuous" / "discrete", 6.1.5(3)/(4)),
    else the national-annex base value (1.0). The caller must ensure the support conditions apply.
    """
    _positive(b=b, contact_length=contact_length)
    _non_negative(F=F)
    mat, k = _kmod(material, service_class, load_duration)
    if kc90 is not None:
        factor = kc90
    elif support is not None:
        factor = mat.kc90_factor(support)
    else:
        factor = get_national_annex(national_annex).kc90_base
    if factor > 1.75:
        raise ValueError(f"Invalid input kc90: {factor!r} (maximum 1.75)")
    _positive(kc90=factor)
    fc90d = design_strength(mat.fc90k, k, mat.gammaM)
    sigma = F * 1e3 / (b * contact_length)
    return CheckResult("compression_perpendicular", "EN 1995-1-1 6.1.5", sigma / (factor * fc90d),
                       {"material": material, "kmod": k, "fc90d": fc90d, "sigma_c90d": sigma, "kc90": factor,
                        "national_annex": national_annex})


def check_column_buckling(*, material: str, b: float, h: float, L: float, N: float,
                          beta_y: float = 1.0, beta_z: float = 1.0,
                          service_class: int = 1, load_duration: str = "medium") -> CheckResult:
    """Pure compression with buckling about both axes, EN 1995-1-1 6.3.2 eq. (6.21)-(6.26).

    Axial force only; combined bending and compression (6.23/6.24) is not covered.
    """
    _positive(b=b, h=h, L=L, N=N, beta_y=beta_y, beta_z=beta_z)
    mat, k = _kmod(material, service_class, load_duration)
    area = b * h
    kc_axis = {}
    for axis, dim, beta in (("y", h, beta_y), ("z", b, beta_z)):
        lam = beta * L / (dim / math.sqrt(12.0))
        lam_rel = lam / math.pi * math.sqrt(mat.fc0k / mat.E005)
        kk = 0.5 * (1.0 + mat.betaC * (lam_rel - 0.3) + lam_rel**2)
        kc = 1.0 if lam_rel <= 0.3 else 1.0 / (kk + math.sqrt(kk * kk - lam_rel**2))
        kc_axis[axis] = {"lambda": lam, "lambda_rel": lam_rel, "kc": kc}
    kc_min = min(v["kc"] for v in kc_axis.values())
    fc0d = design_strength(mat.fc0k, k, mat.gammaM)
    sigma = N * 1e3 / area
    return CheckResult("column_buckling", "EN 1995-1-1 6.3.2", sigma / (kc_min * fc0d), {
        "material": material, "kmod": k, "fc0d": fc0d, "sigma_c0d": sigma, "kc": kc_min, "axes": kc_axis,
    })
