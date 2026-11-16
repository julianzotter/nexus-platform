"""Fail-closed RFEM 6 gRPC Python SDK preflight; no model mutation.

`--live --ack-api-cost` is deliberately a separate, manual action for the
licensed Windows workstation. Never store credentials in the output.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
from datetime import datetime, timezone
from importlib import metadata


def inspect_sdk() -> dict[str, object]:
    """Inspect the local Python installation without importing Dlubal or RFEM."""
    result: dict[str, object] = {
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "os": platform.system(),
        "python": platform.python_version(),
        "mode": "OFFLINE_SDK_ONLY",
        "rfem_connection": "NOT_RUN",
        "model_changed": False,
        "calculations": "NOT_RUN",
    }
    try:
        result["dlubal_api_version"] = metadata.version("dlubal.api")
        result["sdk"] = "INSTALLED_NOT_SIGNATURE_TESTED"
    except metadata.PackageNotFoundError:
        result["dlubal_api_version"] = None
        result["sdk"] = "NOT_INSTALLED"
    return result


def read_application_info(report: dict[str, object], acknowledged: bool) -> None:
    """Read application info only, using Dlubal's documented context manager."""
    if not acknowledged:
        raise PermissionError("Live RFEM requests may be metered; --ack-api-cost required")
    if report["os"] != "Windows" or report["sdk"] == "NOT_INSTALLED":
        raise RuntimeError("Requires Windows RFEM host and installed matching SDK")
    from dlubal.api import rfem  # type: ignore[import-not-found]  # noqa: PLC0415

    # No open_model, set_active_model, create, update, calculate or save calls.
    with rfem.Application() as app:
        info = app.get_application_info()
    report["mode"] = "LIVE_APPLICATION_READONLY"
    report["rfem_connection"] = "READ_ONLY_OK"
    report["application_info_type"] = type(info).__name__


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--ack-api-cost", action="store_true")
    args = parser.parse_args()
    report = inspect_sdk()
    code = 0
    if args.live:
        try:
            read_application_info(report, args.ack_api_cost)
        except Exception as error:
            report["rfem_connection"] = "BLOCKED"
            report["failure_type"] = type(error).__name__
            code = 2
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
