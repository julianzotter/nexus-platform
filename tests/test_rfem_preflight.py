"""Include RFEM host preflight tests in NEXUS CI discovery."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "rfem_parametric"))
from test_preflight import PreflightTests  # noqa: F401
