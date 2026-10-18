#!/usr/bin/env python3
"""Knowledge health report: freshness, sign-off validity, source-link integrity, coverage.

Unmeasurable metrics are reported as INCOMPLETE, never guessed.
Exit code 1 if any item is STALE/BROKEN (CI gate); INCOMPLETE alone does not fail.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAX_AGE_DAYS = 180


def _parse(ts: Any) -> datetime | None:
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    except ValueError:
        return None


def assess_item(item: dict, registry_ids: set[str], now: datetime, max_age_days: int) -> dict:
    """Return {id, state, reasons}; state is OK, STALE, BROKEN or INCOMPLETE."""
    reasons: list[str] = []
    state = "OK"
    if item.get("source_file_id") not in registry_ids:
        state, reasons = "BROKEN", ["source_file_id not found in file registry"]
    signoff = item.get("signoff")
    if item.get("engineering_result") and not isinstance(signoff, dict):
        state = "BROKEN"
        reasons.append("engineering result without sign-off")
    elif isinstance(signoff, dict):
        if signoff.get("result_version") != item.get("version"):
            state = "STALE"
            reasons.append("sign-off bound to a different version")
        decided = _parse(signoff.get("decided_at"))
        if decided is None:
            state = state if state != "OK" else "INCOMPLETE"
            reasons.append("sign-off date unreadable")
        else:
            if decided.tzinfo is None:
                decided = decided.replace(tzinfo=timezone.utc)
            if (now - decided).days > max_age_days and state == "OK":
                state = "STALE"
                reasons.append(f"sign-off older than {max_age_days} days")
    return {"id": item.get("id"), "state": state, "reasons": reasons}


def load_registry_ids(path: Path) -> set[str]:
    ids: set[str] = set()
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                ids.add(json.loads(line)["id"])
    return ids


def build_report(knowledge_dir: Path, registry: Path, coverage: Path, now: datetime, max_age_days: int) -> dict:
    ids = load_registry_ids(registry)
    results = []
    for p in sorted(knowledge_dir.glob("*.json")) if knowledge_dir.is_dir() else []:
        try:
            item = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            results.append({"id": p.name, "state": "BROKEN", "reasons": ["unreadable"]})
            continue
        results.append(assess_item(item, ids, now, max_age_days))
    counts: dict[str, int] = {}
    for r in results:
        counts[r["state"]] = counts.get(r["state"], 0) + 1
    sources: dict[str, Any] = {}
    if coverage.is_file():
        for name, s in json.loads(coverage.read_text(encoding="utf-8")).get("sources", {}).items():
            sources[name] = s.get("coverage_percent") if s.get("coverage_percent") is not None else "INCOMPLETE"
    total = len(results)
    return {
        "items": total,
        "counts": counts,
        "healthy_percent": round(100 * counts.get("OK", 0) / total, 1) if total else "INCOMPLETE",
        "coverage": sources,
        "details": [r for r in results if r["state"] != "OK"],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--knowledge-dir", type=Path, default=ROOT / "registry" / "knowledge")
    ap.add_argument("--registry", type=Path, default=ROOT / "registry" / "file-registry.jsonl")
    ap.add_argument("--coverage", type=Path, default=ROOT / "registry" / "coverage-per-source.json")
    ap.add_argument("--max-age-days", type=int, default=DEFAULT_MAX_AGE_DAYS)
    args = ap.parse_args()
    report = build_report(args.knowledge_dir, args.registry, args.coverage, datetime.now(timezone.utc), args.max_age_days)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    bad = report["counts"].get("STALE", 0) + report["counts"].get("BROKEN", 0)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
