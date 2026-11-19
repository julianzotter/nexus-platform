"""Expose DeepSeek contract tests to core NEXUS CI under a unique module name."""
import importlib.util
from pathlib import Path

source = Path(__file__).resolve().parents[1] / "deepseek_route_tests" / "test_deepseek_route.py"
spec = importlib.util.spec_from_file_location("nexus_deepseek_contract_tests", source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
DeepSeekRouteTests = module.DeepSeekRouteTests
