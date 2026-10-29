#!/usr/bin/env python3
"""Fail-closed assertion of operational evidence, separate from Actions job status."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def assess(kind: str, report: dict[str, Any]) -> tuple[bool, str]:
    if kind == "monitor":
        if report.get("status") != "PASS":
            return False, "MONITOR_NOT_COMPLETE"
        checks = report.get("checks")
        if not isinstance(checks, dict) or not checks:
            return False, "MONITOR_CHECKS_MISSING"
        if any(not isinstance(v, dict) or v.get("status") != "PASS" for v in checks.values()):
            return False, "MONITOR_CHECK_NOT_PASS"
        if not report.get("commit") or report.get("commit") == "UNKNOWN":
            return False, "COMMIT_UNBOUND"
        if not report.get("run_id") or report.get("run_id") == "LOCAL":
            return False, "RUN_UNBOUND"
        return True, "MONITOR_EVIDENCE_PASS"
    if kind == "drive-poll":
        if report.get("status") != "OK":
            return False, "DRIVE_POLL_NOT_OPERATIONAL"
        if not isinstance(report.get("change_count"), int) or report["change_count"] < 0:
            return False, "CHANGE_COUNT_INVALID"
        # Token must be checked in the separate durable state file.
        return True, "POLL_REPORT_PASS_REQUIRES_CHECKPOINT"
    return False, "UNKNOWN_KIND"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=["monitor", "drive-poll"])
    parser.add_argument("report", type=Path)
    parser.add_argument("--checkpoint", type=Path)
    args = parser.parse_args()
    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
        valid, reason = assess(args.kind, report)
        if args.kind == "drive-poll" and valid:
            if args.checkpoint is None:
                valid, reason = False, "CHECKPOINT_MISSING"
            else:
                checkpoint = json.loads(args.checkpoint.read_text(encoding="utf-8"))
                if not isinstance(checkpoint.get("page_token"), str) or not checkpoint["page_token"]:
                    valid, reason = False, "CHECKPOINT_INVALID"
                elif checkpoint.get("initialized") is not False:
                    valid, reason = False, "CHECKPOINT_INITIALIZATION_ONLY"
    except (OSError, ValueError, TypeError, AttributeError):
        valid, reason = False, "EVIDENCE_UNREADABLE"
    print(json.dumps({"evidence_gate": "PASS" if valid else "BLOCKED", "reason": reason}))
    return 0 if valid else 2


if __name__ == "__main__":
    raise SystemExit(main())
