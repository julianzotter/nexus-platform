"""Architecture gate: one canonical display, one local backend, no undeclared HTML surface."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build_control_data as bcd  # noqa: E402
import check_ui_surfaces as cus  # noqa: E402


def copy_repo_subset(tmp: Path) -> Path:
    """Minimal tree: registry + declared surface dirs (empty) -> isolated mutations."""
    (tmp / "registry").mkdir()
    shutil.copy(ROOT / cus.REGISTRY, tmp / cus.REGISTRY)
    for s in cus.load(ROOT):
        (tmp / s["path"]).mkdir(parents=True, exist_ok=True)
    return tmp


def test_repository_passes_gate() -> None:
    assert cus.check(ROOT) == []


def test_undeclared_dashboard_fails(tmp_path: Path) -> None:
    root = copy_repo_subset(tmp_path)
    (root / "prototypes/new-panel").mkdir(parents=True)
    (root / "prototypes/new-panel/index.html").write_text("<!doctype html>", encoding="utf-8")
    assert any("R4 undeclared surface: prototypes/new-panel" in e for e in cus.check(root))
    (root / "apps/control-panel/dist").mkdir(parents=True)  # build output is ignored
    (root / "apps/control-panel/dist/index.html").write_text("x", encoding="utf-8")
    assert not any("dist" in e for e in cus.check(root))


def test_second_canonical_and_prototype_without_target_fail(tmp_path: Path) -> None:
    root = copy_repo_subset(tmp_path)
    reg = json.loads((root / cus.REGISTRY).read_text(encoding="utf-8"))
    for s in reg["surfaces"]:
        if s["id"] == "UI-05":
            s["role"] = "CANONICAL_DISPLAY"
        if s["id"] == "UI-03":
            s["consolidation_target"] = None
    (root / cus.REGISTRY).write_text(json.dumps(reg), encoding="utf-8")
    errors = cus.check(root)
    assert any(e.startswith("R2 CANONICAL_DISPLAY") for e in errors)
    assert any(e.startswith("R3") and "UI-03" in e for e in errors)


def test_panel_data_contains_surfaces(tmp_path: Path) -> None:
    commit = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], check=True,
                            capture_output=True, text=True).stdout.strip()
    assert bcd.main(["--source-commit", commit, "--out", str(tmp_path), "--snapshot", "missing.json"]) == 0
    surfaces = json.loads((tmp_path / "control-data.json").read_text(encoding="utf-8"))["nexus"]["surfaces"]
    assert [i[0] for i in surfaces["items"]] == [s["id"] for s in cus.load(ROOT)]
    assert surfaces["byRole"]["CANONICAL_DISPLAY"] == 1
