#!/usr/bin/env python3
"""Read-only repository monitoring with durable local JSON/Markdown evidence."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def command(args: list[str], cwd: Path = ROOT) -> dict[str, Any]:
    """Capture failures without preventing the remaining checks or report writing."""
    try:
        result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=60)
        return {"exit_code": result.returncode, "stdout": result.stdout,
                "stderr": result.stderr}
    except (OSError, subprocess.TimeoutExpired) as exc:
        # Do not include environment variables or credentials in diagnostics.
        return {"exit_code": 1, "stdout": "", "stderr": type(exc).__name__}


def github_json(endpoint: str) -> Any:
    result = command(["gh", "api", "--paginate", "--slurp", endpoint])
    if result["exit_code"]:
        raise RuntimeError("GitHub metadata request failed; inspect authentication/API access")
    return json.loads(result["stdout"])


def inspect_prs(repository: str) -> dict[str, Any]:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        return {"status": "ERROR", "error": "Missing or invalid owner/repository", "items": []}
    items: list[dict[str, Any]] = []
    try:
        pages = github_json(f"repos/{repository}/pulls?state=open&per_page=100")
        for page in pages:
            for pr in page:
                number = int(pr["number"])
                for attempt in range(3):
                    detail = github_json(f"repos/{repository}/pulls/{number}")[0]
                    if detail.get("mergeable") is not None:
                        break
                    if attempt < 2:
                        time.sleep(1)
                state = {True: "MERGEABLE", False: "CONFLICT"}.get(detail.get("mergeable"), "UNKNOWN")
                items.append({"number": number, "state": state, "head_sha": detail["head"]["sha"],
                              "base_sha": detail["base"]["sha"], "draft": detail.get("draft", False)})
        states = {item["state"] for item in items}
        status = "CONFLICT" if "CONFLICT" in states else "UNKNOWN" if "UNKNOWN" in states else "PASS"
        return {"status": status, "items": items}
    except (RuntimeError, ValueError, KeyError, TypeError, IndexError):
        return {"status": "ERROR", "error": "Incomplete GitHub metadata retrieval", "items": items}


def validation_checks() -> dict[str, Any]:
    checks: dict[str, Any] = {}
    for name, tool in (("registry", "validate_registry.py"), ("knowledge", "validate_knowledge.py")):
        result = command([sys.executable, str(ROOT / "tools" / tool)])
        status = "NO_DATA" if name == "knowledge" and result["exit_code"] == 2 else (
            "PASS" if result["exit_code"] == 0 else "FAIL")
        checks[name] = {"status": status, **result}
    try:
        coverage = json.loads((ROOT / "registry/coverage-per-source.json").read_text())
        total = coverage["total"]["status"]
        checks["coverage"] = {"status": "PASS" if total == "COMPLETE" else "INCOMPLETE"}
    except (OSError, ValueError, KeyError, TypeError):
        checks["coverage"] = {"status": "ERROR"}
    return checks


def inspect_workflow_configuration(directory: Path = ROOT / ".github/workflows") -> dict[str, Any]:
    """Inventory declared workflow triggers; this does not prove a workflow ran."""
    workflows = []
    paths = sorted((*directory.glob("*.yml"), *directory.glob("*.yaml"))) if directory.is_dir() else []
    for path in paths:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        name = next((match.group(1).strip() for line in lines
                     if (match := re.match(r"^name:\s*(.+?)\s*$", line))), path.stem)
        triggers: list[str] = []
        schedules: list[str] = []
        in_triggers = False
        current_trigger = None
        for line in lines:
            if not in_triggers:
                if re.fullmatch(r"on:\s*(?:#.*)?", line):
                    in_triggers = True
                else:
                    inline = re.match(r"^on:\s*\[([^\]]*)\]", line)
                    if inline:
                        triggers.extend(part.strip().strip("'\"") for part in inline.group(1).split(",")
                                        if part.strip())
                continue
            if line.strip() and not line.startswith((" ", "\t", "#")):
                break
            event = re.match(r"^  ([A-Za-z0-9_-]+):\s*(?:#.*)?$", line)
            if event:
                current_trigger = event.group(1)
                triggers.append(current_trigger)
            elif current_trigger == "schedule":
                cron = re.match(r"^    - cron:\s*(.+?)\s*(?:#.*)?$", line)
                if cron:
                    schedules.append(cron.group(1).strip().strip("'\""))
        workflows.append({"file": path.name, "name": name, "events": triggers, "schedules": schedules})
    return {
        "state": "OBSERVED" if workflows else "NO_DATA",
        "runtime_verified": False,
        "scope": "workflow declarations only; configured schedules are not execution receipts",
        "workflows": workflows,
    }


def overall_status(checks: dict[str, Any]) -> str:
    states = {check["status"] for check in checks.values()}
    if states & {"FAIL", "ERROR", "CONFLICT", "UNKNOWN"}:
        return "ATTENTION"
    return "INCOMPLETE" if states & {"NO_DATA", "INCOMPLETE"} else "PASS"


def write_report(report: dict[str, Any], directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = ["# NEXUS repository monitor", "", f"Overall: **{report['status']}**", "",
             "| Check | State |", "|---|---|"]
    lines += [f"| {name} | {check['status']} |" for name, check in report["checks"].items()]
    automation = report.get("automation_configuration", {})
    lines += ["", "## Workflow trigger configuration", "",
              "Declared triggers only; this inventory does not prove that a workflow ran.", "",
              "| Workflow | Events | Schedules (UTC) |", "|---|---|---|"]
    lines += [
        f"| {item['name']} (`{item['file']}`) | {', '.join(item['events']) or 'none detected'} "
        f"| {', '.join(f'`{cron}`' for cron in item['schedules']) or 'none'} |"
        for item in automation.get("workflows", [])
    ]
    if not automation.get("workflows"):
        lines.append("| — | No workflow files observed | — |")
    lines += ["", f"Commit: `{report['commit']}`", f"Observed UTC: {report['observed_at']}", "",
              "A successful workflow is not proof of complete knowledge coverage or engineering approval.",
              "Reports are GitHub artifacts. A separate WORK delivery workflow exists; only its verified receipts prove delivery. No automated merge is authorized."]
    text = "\n".join(lines) + "\n"
    (directory / "report.md").write_text(text, encoding="utf-8")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with Path(summary).open("a", encoding="utf-8") as output:
            output.write(text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY", ""))
    parser.add_argument("--report-dir", type=Path, default=ROOT / "reports/monitor")
    args = parser.parse_args()
    checks = validation_checks()
    checks["pull_requests"] = inspect_prs(args.repository)
    report = {"schema_version": "1.0.0", "observed_at": datetime.now(timezone.utc).isoformat(),
              "commit": os.environ.get("GITHUB_SHA", "UNKNOWN"),
              "run_id": os.environ.get("GITHUB_RUN_ID", "LOCAL"),
              "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT", "1"),
              "automation_configuration": inspect_workflow_configuration(),
              "status": overall_status(checks), "checks": checks}
    write_report(report, args.report_dir)
    print(f"NEXUS monitor: {report['status']}")
    return 1 if report["status"] == "ATTENTION" else 0


if __name__ == "__main__":
    raise SystemExit(main())
