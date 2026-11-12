"""Bounded, read-only Actions telemetry; run metadata is not delivery evidence."""
from __future__ import annotations

import re
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

# Explicit observation tolerances, not a guaranteed GitHub scheduling SLA.
WORKFLOWS = (
    ("nexus-monitor.yml", "schedule", 60, 30),
    ("nexus-drive-poll.yml", "schedule", 30, 30),
    ("nexus-delivery.yml", "workflow_run", 60, 30),
)


def timestamp(value: str) -> datetime:
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("Timezone required")
    return result.astimezone(timezone.utc)


def evidence_run(raw: dict[str, Any], now: datetime) -> dict[str, Any]:
    """Whitelist public run evidence; never copy arbitrary API diagnostics."""
    if type(raw.get("id")) is not int or raw["id"] <= 0:
        raise ValueError("Invalid run ID")
    if type(raw.get("run_attempt")) is not int or raw["run_attempt"] < 1:
        raise ValueError("Invalid run attempt")
    if not re.fullmatch(r"[0-9a-f]{40}", raw.get("head_sha", "")):
        raise ValueError("Invalid commit")
    created = timestamp(raw["created_at"])
    if created > now:
        raise ValueError("Future run")
    if raw.get("status") not in {"queued", "in_progress", "completed", "waiting", "pending", "requested"}:
        raise ValueError("Invalid run status")
    return {key: raw.get(key) for key in (
        "id", "run_attempt", "event", "head_branch", "head_sha", "created_at",
        "status", "conclusion", "html_url",
    )}


def assess_runs(runs: list[dict[str, Any]], now: datetime,
                interval: int, grace: int) -> tuple[str, str]:
    """Three distinct latest completed runs; current run may still be executing."""
    if not runs:
        return "NO_DATA", "NO_MATCHING_TRIGGER_RUNS"
    limit = (interval + grace) * 60
    age = lambda run: (now - timestamp(run["created_at"])).total_seconds()
    if age(runs[0]) > limit:
        return "FAIL", "STALE"
    if any(run["status"] != "completed" and age(run) > limit for run in runs[:4]):
        return "FAIL", "OVERDUE_RUN"
    completed = [run for run in runs if run["status"] == "completed"][:3]
    if any(run["conclusion"] != "success" for run in completed):
        return "FAIL", "RECENT_RUN_NOT_SUCCESSFUL"
    if any(run["run_attempt"] != 1 for run in completed):
        return "INCOMPLETE", "RETRY_NOT_INITIAL_TRIGGER_SUCCESS"
    if len(completed) < 3:
        return "INCOMPLETE", "THREE_COMPLETED_RUNS_REQUIRED"
    if age(completed[0]) > limit:
        return "FAIL", "LAST_COMPLETED_RUN_STALE"
    gaps = [(timestamp(a["created_at"]) - timestamp(b["created_at"])).total_seconds()
            for a, b in zip(completed, completed[1:])]
    if any(gap > limit for gap in gaps):
        return "FAIL", "OBSERVED_RUN_GAP"
    return "PASS", "THREE_RECENT_SUCCESSFUL_TRIGGER_RUNS"


def inspect_workflow(repository: str, spec: tuple[str, str, int, int],
                     fetch: Callable[[str], Any], now: datetime) -> dict[str, Any]:
    filename, event, interval, grace = spec
    result: dict[str, Any] = {"file": filename, "expected_event": event,
        "interval_minutes": interval, "grace_minutes": grace,
        "status": "ERROR", "reason": "METADATA_UNAVAILABLE", "runs": []}
    try:
        endpoint = f"repos/{repository}/actions/workflows/{filename}"
        meta = fetch(endpoint)
        result["workflow_state"] = meta["state"]
        if meta["state"] != "active":
            return {**result, "status": "FAIL", "reason": "WORKFLOW_NOT_ACTIVE"}
        if meta["path"] != f".github/workflows/{filename}":
            raise ValueError("Wrong workflow")
        payload = fetch(f"{endpoint}/runs?event={event}&branch=main&per_page=100&page=1")
        raw_runs = payload["workflow_runs"]
        if not isinstance(raw_runs, list) or len(raw_runs) > 100:
            raise ValueError("Invalid bounded response")
        # A filtered API response containing foreign evidence fails closed.
        if any(r["event"] != event or r["head_branch"] != "main"
               or r["workflow_id"] != meta["id"] for r in raw_runs):
            raise ValueError("Wrong event, branch or workflow")
        runs = [evidence_run(run, now) for run in raw_runs]
        if len({run["id"] for run in runs}) != len(runs):
            raise ValueError("Duplicate runs")
        runs.sort(key=lambda run: timestamp(run["created_at"]), reverse=True)
        result["status"], result["reason"] = assess_runs(runs, now, interval, grace)
        result["runs"] = runs[:4]
    except (RuntimeError, ValueError, KeyError, TypeError, AttributeError, OSError):
        # Do not emit provider exception text: it may contain credentials.
        result.update(status="ERROR", reason="INVALID_OR_UNAVAILABLE_METADATA")
    return result


def inspect_runtime(repository: str, fetch: Callable[[str], Any],
                    now: datetime | None = None) -> dict[str, Any]:
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("Timezone required")
    result: dict[str, Any] = {"schema_version": "1.0.0", "observed_at": now.isoformat(),
        "status": "ERROR", "end_to_end": "UNVERIFIED", "workflows": [],
        "scope": "Actions run metadata only; no receipt or consumer ACK verification"}
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        return result
    result["workflows"] = [inspect_workflow(repository, spec, fetch, now) for spec in WORKFLOWS]
    states = {item["status"] for item in result["workflows"]}
    result["status"] = ("ERROR" if "ERROR" in states else "FAIL" if "FAIL" in states
                        else "INCOMPLETE" if states & {"NO_DATA", "INCOMPLETE"} else "PASS")
    return result
