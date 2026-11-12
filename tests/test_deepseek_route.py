"""Expose DeepSeek contract checks to the main NEXUS unittest suite."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "deepseek_route_tests"))
from test_deepseek_route import DeepSeekRouteTests  # noqa: F401
