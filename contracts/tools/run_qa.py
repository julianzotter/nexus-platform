"""Execute QA and save exact commands, versions, return codes and logs."""
from __future__ import annotations
from datetime import datetime
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from zoneinfo import ZoneInfo


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    folder = root / "qa"
    folder.mkdir(exist_ok=True)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root / "src") + os.pathsep + env.get("PYTHONPATH", "")
    commands = {
        "pytest": [sys.executable, "-m", "pytest", "-q", "--junitxml=qa/pytest.xml"],
        "mypy": [sys.executable, "-m", "mypy", "src"],
        "import_linter": [sys.executable, "-c", "from importlinter.cli import lint_imports_command; lint_imports_command()", "--no-cache"],
        "demo": [sys.executable, "-m", "nexus.bootstrap.demo"],
        "compile": [sys.executable, "-m", "compileall", "-q", "src"],
    }
    runs = []
    for name, command in commands.items():
        start = time.monotonic()
        result = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True, timeout=120)
        (folder / f"{name}.log").write_text(result.stdout + result.stderr, encoding="utf-8")
        runs.append({"name": name, "command": command, "returncode": result.returncode,
                     "status": "PASS" if result.returncode == 0 else "FAIL",
                     "elapsed_seconds": round(time.monotonic()-start, 3), "log": f"qa/{name}.log"})
        print(name, runs[-1]["status"], flush=True)
    report = {
        "observed_at": datetime.now(ZoneInfo("Europe/Vienna")).isoformat(),
        "python": platform.python_version(), "platform": platform.platform(),
        "versions": {name: importlib.metadata.version(name)
                     for name in ("pytest", "mypy", "import-linter", "jsonschema")},
        "scope": "software contracts only; no structural calculation or vendor API invocation",
        "overall": "PASS" if all(run["status"] == "PASS" for run in runs) else "FAIL",
        "runs": runs,
    }
    (folder / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if report["overall"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
