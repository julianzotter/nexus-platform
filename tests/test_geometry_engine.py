"""Include geometry/DSH contracts in the existing root CI discovery."""
import importlib.util
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "orchestrator"))
specification = importlib.util.spec_from_file_location(
    "nexus_geometry_contract", root / "orchestrator/tests/test_geometry.py")
module = importlib.util.module_from_spec(specification)
specification.loader.exec_module(module)
for name, value in vars(module).items():
    if name.startswith("test_") or name == "spec":
        globals()[name] = value
