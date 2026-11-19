"""Read-only host capability inventory; no license, network or solver calls."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
from importlib import metadata
from pathlib import Path
from typing import Any


def _package(name: str, module: str) -> dict[str, str | bool]:
    try:
        version = metadata.version(name)
    except metadata.PackageNotFoundError:
        version = "NOT_INSTALLED"
    try:
        found = importlib.util.find_spec(module) is not None
    except (ModuleNotFoundError, ValueError):
        found = False
    return {"distribution": name, "version": version, "module_found": found}


def inspect_host() -> dict[str, Any]:
    """Collect nonsecret environment and installation evidence only."""
    return {
        "mode": "READ_ONLY_OFFLINE_PREFLIGHT",
        "system": platform.system(), "python": platform.python_version(),
        "rfem5": {"bridge": _package("comtypes", "comtypes"),
                  "com_application": "NOT_PROBED", "license": "NOT_PROBED"},
        "rfem6": {"sdk": _package("dlubal.api", "dlubal"),
                  "grpc_server": "NOT_PROBED", "api_key": "NOT_PROBED"},
        "deepseek": {"process_key_present": bool(os.environ.get("DEEPSEEK_API_KEY")),
                     "models_auth": "NOT_PROBED", "dsh_store": "NOT_OPENED"},
        "model_creation": "BLOCKED", "solver": "NOT_RUN",
        "source_models_modified": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="create new JSON report (never overwrite)")
    args = parser.parse_args()
    result = inspect_host()
    body = json.dumps(result, sort_keys=True, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        with args.out.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(body)
    print(body, end="")


if __name__ == "__main__":
    main()
