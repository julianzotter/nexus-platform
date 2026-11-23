"""Run the actual import-linter against clean and intentionally broken copies."""
import os
import ast
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]


def lint(folder: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(folder / "src") + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run([sys.executable, "-c", "from importlinter.cli import lint_imports_command; lint_imports_command()",
                           "--config", str(folder / ".importlinter"), "--no-cache"],
                          cwd=folder, env=env, text=True, capture_output=True, timeout=45)


def test_actual_import_linter_accepts_package():
    result = lint(ROOT)
    assert result.returncode == 0, result.stdout + result.stderr


def test_static_source_module_import_graph_is_acyclic():
    modules = {}
    for path in (ROOT / "src/nexus").rglob("*.py"):
        parts = path.relative_to(ROOT / "src").with_suffix("").parts
        name = ".".join(parts[:-1] if parts[-1] == "__init__" else parts)
        modules[name] = path
    edges = {name: set() for name in modules}
    for name, path in modules.items():
        package = name if path.name == "__init__.py" else name.rpartition(".")[0]
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Import):
                edges[name].update(alias.name for alias in node.names if alias.name in modules)
            elif isinstance(node, ast.ImportFrom):
                target = importlib.util.resolve_name("."*node.level + (node.module or ""), package) if node.level else node.module
                if target in modules:
                    edges[name].add(target)
    done, active = set(), set()
    def visit(name):
        assert name not in active, f"cyclic source imports: {name}"
        if name in done:
            return
        active.add(name)
        for target in edges[name]:
            visit(target)
        active.remove(name)
        done.add(name)
    for name in modules:
        visit(name)


@pytest.mark.parametrize("target,statement", [
    ("application", "import nexus.adapters"),
    ("adapters", "import nexus.application"),
    ("domain", "import pydantic"),
    ("domain", "import openpyxl"),
    ("domain", "import nexus.adapters"),
    ("domain", "import PyNite"),
])
def test_actual_import_linter_rejects_injected_violation(tmp_path, target, statement):
    shutil.copytree(ROOT / "src", tmp_path / "src", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copyfile(ROOT / ".importlinter", tmp_path / ".importlinter")
    (tmp_path / "src/nexus" / target / "injected_violation.py").write_text(statement + "\n")
    result = lint(tmp_path)
    assert result.returncode != 0, result.stdout + result.stderr
    assert "BROKEN" in result.stdout, result.stdout + result.stderr
