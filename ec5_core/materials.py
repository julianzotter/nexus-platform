"""Material data and modification factors for EN 1995-1-1 (EC5).

PROTOTYPE - not a certified calculation. Characteristic values per EN 338 (solid
timber) and EN 14080 (glulam); partial factors are the EN 1995-1-1 recommended
values and must be replaced by the National Annex values of the project.
"""
from __future__ import annotations

from dataclasses import dataclass

# EN 1995-1-1 Table 3.1, solid timber and glulam (service classes 1, 2, 3).
_KMOD = {
    1: {"permanent": 0.60, "long": 0.70, "medium": 0.80, "short": 0.90, "instantaneous": 1.10},
    2: {"permanent": 0.60, "long": 0.70, "medium": 0.80, "short": 0.90, "instantaneous": 1.10},
    3: {"permanent": 0.50, "long": 0.55, "medium": 0.65, "short": 0.70, "instantaneous": 0.90},
}


@dataclass(frozen=True)
class TimberMaterial:
    name: str
    glulam: bool
    fmk: float  # bending, N/mm2
    fvk: float  # shear
    fc0k: float  # compression parallel to grain
    fc90k: float  # compression perpendicular to grain
    E005: float  # 5% modulus of elasticity parallel to grain
    gammaM: float  # partial factor (recommended value, no National Annex)

    @property
    def betaC(self) -> float:
        # EN 1995-1-1 eq. (6.29)
        return 0.1 if self.glulam else 0.2

    def kc90_factor(self, support: str) -> float:
        """EN 1995-1-1 6.1.5(3)/(4) (identical in OENORM B 1995-1-1:2019).

        continuous: l1 >= 2h, solid 1.25, glulam 1.5
        discrete:   solid 1.5, glulam 1.75 (only valid for contact length <= 400 mm)
        """
        if support == "continuous":
            return 1.5 if self.glulam else 1.25
        if support == "discrete":
            return 1.75 if self.glulam else 1.5
        raise ValueError(f"Invalid support: {support!r}")


@dataclass(frozen=True)
class NationalAnnex:
    name: str
    kcr: float  # shear cracking factor, EN 1995-1-1 6.1.7(2)
    kc90_base: float  # kc,90 when no 6.1.5(3)/(4) condition is claimed


NATIONAL_ANNEXES = {
    # EN 1995-1-1 recommended values
    "EN": NationalAnnex("EN", kcr=0.67, kc90_base=1.0),
    # OENORM B 1995-1-1:2019-06: kcr = 1.0 (6.1.7(2)), kc,90 = 1.0 base, max 1.75 (6.1.5(2)).
    # gammaM (Table 2.3), kmod (Table 3.1), kdef (Table 3.2), km = 0.7 are the recommended values.
    "AT": NationalAnnex("AT", kcr=1.0, kc90_base=1.0),
}

# EN 1995-1-1 / OENORM B 1995-1-1 Table 3.2, solid timber and glulam, by service class.
KDEF = {1: 0.60, 2: 0.80, 3: 2.00}


def get_national_annex(name: str) -> NationalAnnex:
    try:
        return NATIONAL_ANNEXES[name]
    except KeyError:
        raise ValueError(f"Unknown national annex: {name!r}") from None


MATERIALS = {
    m.name: m
    for m in (
        TimberMaterial("C24", False, 24.0, 4.0, 21.0, 2.5, 7400.0, 1.3),
        TimberMaterial("C30", False, 30.0, 4.0, 23.0, 2.7, 8000.0, 1.3),
        TimberMaterial("GL24h", True, 24.0, 3.5, 24.0, 2.5, 9400.0, 1.25),
        TimberMaterial("GL28h", True, 28.0, 3.5, 26.5, 3.0, 10200.0, 1.25),
    )
}


def get_material(name: str) -> TimberMaterial:
    try:
        return MATERIALS[name]
    except KeyError:
        raise ValueError(f"Unknown material: {name!r}") from None


def kmod(service_class: int, load_duration: str) -> float:
    if service_class not in _KMOD:
        raise ValueError(f"Invalid service class: {service_class!r}")
    if load_duration not in _KMOD[service_class]:
        raise ValueError(f"Invalid load duration: {load_duration!r}")
    return _KMOD[service_class][load_duration]


def design_strength(fk: float, kmod_value: float, gamma_m: float, kh: float = 1.0) -> float:
    """EN 1995-1-1 eq. (2.14): Xd = kh * kmod * Xk / gammaM."""
    return kh * kmod_value * fk / gamma_m
