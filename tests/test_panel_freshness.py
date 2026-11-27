"""Control Panel freshness guard (apps/control-panel/site/freshness.js): stale data never shows FRESH."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "apps/control-panel/site/freshness.js"
NOW = "2026-11-27T12:00:00Z"


def run(data: dict) -> dict:
    script = (f"const {{freshness}} = require({json.dumps(str(MODULE))});"
              f"console.log(JSON.stringify(freshness({json.dumps(data)}, Date.parse({json.dumps(NOW)}))));")
    out = subprocess.run(["node", "-e", script], check=True, capture_output=True, text=True).stdout
    return json.loads(out)


pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="node required")


def monitor(observed: str | None, hours: float | None = None) -> dict:
    data: dict = {"nexus": {"monitor": {"status": "PASS"}}}
    if observed:
        data["nexus"]["monitor"]["observedAt"] = observed
    if hours is not None:
        data["policy"] = {"staleAfterHours": hours}
    return data


def test_fresh_within_default_limit() -> None:
    assert run(monitor("2026-11-27T10:30:00Z"))["state"] == "FRESH"  # 1.5 h <= 2 h


def test_stale_after_limit() -> None:
    result = run(monitor("2026-11-27T09:00:00Z"))
    assert (result["state"], result["ageHours"], result["limitHours"]) == ("STALE", 3, 2)


def test_policy_threshold_and_missing_and_future() -> None:
    assert run(monitor("2026-11-27T09:00:00Z", hours=4))["state"] == "FRESH"
    assert run(monitor(None))["state"] == "NO_DATA"
    assert run({})["state"] == "NO_DATA"
    assert run(monitor("2026-11-27T13:00:00Z"))["state"] == "CONFLICT"


def test_panel_loads_guard_before_app() -> None:
    html = (ROOT / "apps/control-panel/site/index.html").read_text(encoding="utf-8")
    assert html.index("freshness.js") < html.index("app.js")
