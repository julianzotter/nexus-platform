"""Include read-only RFEM model identity and topology tests in CI."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "rfem_parametric"))
from test_host_readback import HostReadbackTests  # noqa: F401
