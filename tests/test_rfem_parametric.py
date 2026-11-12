"""Run the RFEM5/6 dry-run regression suite in the repository's main CI tests."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "rfem_parametric"))
from test_parametric import ParametricTests  # noqa: E402,F401
