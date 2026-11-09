import pytest

from ec5_core import (
    check_bending,
    check_column_buckling,
    check_compression_perpendicular,
    check_shear,
    run_check,
)
from ec5_core.materials import kmod


def test_kmod_table():
    assert kmod(1, "medium") == 0.8
    assert kmod(3, "permanent") == 0.5
    with pytest.raises(ValueError):
        kmod(4, "medium")
    with pytest.raises(ValueError):
        kmod(1, "forever")


def test_bending_golden():
    # C24 100x200, My = 5 kNm, SC1 medium: sigma = 5e6/(100*200^2/6) = 7.5, fmd = 0.8*24/1.3
    r = check_bending(material="C24", b=100, h=200, My=5.0)
    assert r.utilization == pytest.approx(7.5 / (0.8 * 24 / 1.3), rel=1e-12)
    assert r.passed


def test_bending_size_factor_small_section():
    # h = 100 < 150: kh = (150/100)^0.2
    r = check_bending(material="C24", b=60, h=100, My=1.0)
    kh = (150 / 100) ** 0.2
    assert r.details["fmd_y"] == pytest.approx(kh * 0.8 * 24 / 1.3)


def test_bending_biaxial_includes_km():
    uni = check_bending(material="C24", b=100, h=200, My=5.0)
    bi = check_bending(material="C24", b=100, h=200, My=5.0, Mz=1.0)
    assert bi.utilization > uni.utilization


def test_bending_lateral_torsional_buckling_reduces_capacity():
    restrained = check_bending(material="GL24h", b=100, h=400, My=20.0)
    free = check_bending(material="GL24h", b=100, h=400, My=20.0, lef=6000)
    assert free.details["kcrit"] < 1.0
    assert free.utilization > restrained.utilization


def test_shear_golden_austrian_annex_default():
    r = check_shear(material="C24", b=100, h=200, V=10.0)
    assert r.details["kcr"] == 1.0
    assert r.utilization == pytest.approx((1.5 * 10000 / (1.0 * 100 * 200)) / (0.8 * 4.0 / 1.3), rel=1e-12)


def test_shear_en_recommended_kcr():
    at = check_shear(material="C24", b=100, h=200, V=10.0, national_annex="AT")
    en = check_shear(material="C24", b=100, h=200, V=10.0, national_annex="EN")
    assert en.details["kcr"] == 0.67
    assert en.utilization == pytest.approx(at.utilization / 0.67, rel=1e-12)
    with pytest.raises(ValueError):
        check_shear(material="C24", b=100, h=200, V=10.0, national_annex="DE")


def test_compression_perpendicular_golden():
    # OENORM base value kc,90 = 1.0 unless a support condition is claimed
    r = check_compression_perpendicular(material="C24", b=100, contact_length=100, F=10.0)
    assert r.details["kc90"] == 1.0
    assert r.utilization == pytest.approx(1.0 / (0.8 * 2.5 / 1.3), rel=1e-12)


@pytest.mark.parametrize("material,support,expected", [
    ("C24", "continuous", 1.25), ("GL24h", "continuous", 1.5),
    ("C24", "discrete", 1.5), ("GL24h", "discrete", 1.75),
])
def test_kc90_support_conditions(material, support, expected):
    r = check_compression_perpendicular(material=material, b=100, contact_length=100, F=10.0, support=support)
    assert r.details["kc90"] == expected


def test_kc90_override_and_cap():
    r = check_compression_perpendicular(material="GL24h", b=100, contact_length=100, F=10.0, kc90=1.2)
    assert r.details["kc90"] == 1.2
    with pytest.raises(ValueError):
        check_compression_perpendicular(material="GL24h", b=100, contact_length=100, F=10.0, kc90=2.2)
    with pytest.raises(ValueError):
        check_compression_perpendicular(material="C24", b=100, contact_length=100, F=10.0, support="x")


def test_column_buckling_golden_weak_axis():
    # Hand calculation: lambda = 103.92, lambda_rel = 1.762, kc = 0.2846, fc0d = 12.923
    r = check_column_buckling(material="C24", b=100, h=100, L=3000, N=50.0)
    assert r.details["axes"]["y"]["lambda"] == pytest.approx(103.923, rel=1e-5)
    assert r.details["kc"] == pytest.approx(0.2846, abs=5e-4)
    assert r.utilization == pytest.approx(5.0 / (0.2846 * 12.923), rel=2e-3)
    assert not r.passed


def test_column_buckling_governed_by_weak_axis():
    r = check_column_buckling(material="GL24h", b=120, h=240, L=3000, N=100.0)
    assert r.details["axes"]["z"]["kc"] < r.details["axes"]["y"]["kc"]
    assert r.details["kc"] == r.details["axes"]["z"]["kc"]


def test_column_short_has_kc_one():
    r = check_column_buckling(material="C24", b=200, h=200, L=300, N=10.0)
    assert r.details["kc"] == 1.0


def test_monotonicity():
    loads = [1, 2, 4, 8]
    for fn, key, kw in (
        (check_bending, "My", dict(material="C24", b=100, h=200)),
        (check_shear, "V", dict(material="C24", b=100, h=200)),
        (check_compression_perpendicular, "F", dict(material="C24", b=100, contact_length=100)),
        (check_column_buckling, "N", dict(material="C24", b=100, h=100, L=2000)),
    ):
        utils = [fn(**kw, **{key: v}).utilization for v in loads]
        assert utils == sorted(utils) and utils[0] < utils[-1]
    deeper = [check_bending(material="C24", b=100, h=h, My=5.0).utilization for h in (160, 200, 240, 300)]
    assert deeper == sorted(deeper, reverse=True)


def test_longer_load_duration_is_less_favourable():
    medium = check_bending(material="C24", b=100, h=200, My=5.0, load_duration="medium")
    permanent = check_bending(material="C24", b=100, h=200, My=5.0, load_duration="permanent")
    assert permanent.utilization > medium.utilization


@pytest.mark.parametrize("kwargs", [
    dict(material="C24", b=0, h=200, My=5.0),
    dict(material="C24", b=100, h=-1, My=5.0),
    dict(material="C24", b=100, h=200, My=float("nan")),
    dict(material="X99", b=100, h=200, My=5.0),
    dict(material="C24", b=100, h=200, My=5.0, service_class=5),
])
def test_invalid_inputs_rejected(kwargs):
    with pytest.raises(ValueError):
        check_bending(**kwargs)


def test_run_check_contract():
    out = run_check({"check": "shear", "material": "GL24h", "b": 160, "h": 400, "V": 40.0})
    assert out["check"] == "shear" and out["gate"] == "PASS" and out["pass"] is True
    assert out["status"].startswith("KANDIDAT")


def test_run_check_schema_rejects_bad_requests():
    import jsonschema

    for bad in (
        {"check": "unknown"},
        {"check": "shear", "material": "C24", "b": 100, "h": 200},
        {"check": "shear", "material": "C24", "b": 100, "h": 200, "V": 1, "extra": 1},
        {"check": "shear", "material": "C24", "b": -1, "h": 200, "V": 1},
    ):
        with pytest.raises(jsonschema.ValidationError):
            run_check(bad)
