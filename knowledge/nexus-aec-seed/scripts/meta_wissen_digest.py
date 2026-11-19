"""Make a deterministic weekly META_WISSEN digest from verified observations.

Input: JSON array of observed records. Acquisition and source verification are
separate authorized connector steps. This script makes no HTTP requests.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


ALLOWED_TOPICS = {
    "OIB", "MATERIAL", "LCA", "ZIRKULARITAET", "ETA_EAD",
    "RFEM_API", "HOLZBAU", "NORMEN", "FORSCHUNG",
}


def canonical_url(url: str) -> str:
    """Normalize host/case/fragment only; preserve meaningful query params."""
    p = urlsplit(url)
    if p.scheme != "https" or not p.hostname:
        raise ValueError(f"Not an HTTPS URL: {url}")
    host = p.hostname.lower()
    return urlunsplit(("https", host, p.path.rstrip("/") or "/", p.query, ""))


def select_records(items: list[dict], since: datetime) -> list[dict]:
    """Reject unverified/undated entries and deduplicate by canonical identity."""
    selected: dict[tuple[str, str], dict] = {}
    for item in items:
        if item.get("evidence_status") != "VERIFIED":
            continue
        if item.get("topic") not in ALLOWED_TOPICS:
            continue
        published = datetime.fromisoformat(item["published_at"])
        if published.tzinfo is None or published.astimezone(timezone.utc) < since:
            continue
        for field in ("publisher_id", "title", "finding", "locator", "version_id"):
            if not item.get(field):
                raise ValueError(f"Missing {field} in VERIFIED item")
        url = canonical_url(item["source_uri"])
        key = (item["publisher_id"], url)
        normalized = {**item, "source_uri": url}
        if key not in selected or normalized["published_at"] > selected[key]["published_at"]:
            selected[key] = normalized
    return sorted(selected.values(), key=lambda i: (i["topic"], i["publisher_id"], i["source_uri"]))


def render_digest(items: list[dict], observed_at: datetime, lookback_days: int) -> str:
    """Return source-linked Markdown with no LLM-generated technical claims."""
    start = observed_at - timedelta(days=lookback_days)
    records = select_records(items, start)
    lines = [
        "# NEXUS META_WISSEN — Weekly Evidence Digest",
        f"- generated_utc: {observed_at.isoformat()}",
        f"- window_start_utc: {start.isoformat()}",
        f"- observations_verified: {len(records)}",
        "- status: SOURCE_DIGEST_NOT_ENGINEERING_RELEASE",
        "",
        "## TL;DR",
        f"{len(records)} verified, deduplicated source changes. No source change means no technical change claim.",
        "",
        "## Quick topic matrix",
        "| Topic | Source | Version | Finding | Evidence |",
        "|---|---|---|---|---|",
    ]
    for item in records:
        clean = lambda s: str(s).replace("|", "\\|").replace("\n", " ")
        source = clean(item["publisher_id"])
        version = clean(item["version_id"])
        finding = clean(item["finding"])
        locator = clean(item["locator"])
        lines.append(
            f"| {item['topic']} | [{source}]({item['source_uri']}) | "
            f"{version} | {finding} | {locator} |"
        )
    if not records:
        lines.append("| — | — | — | No VERIFIED new observations | — |")
    lines.append("")
    lines.append("## Trace")
    for item in records:
        encoded = json.dumps(item, sort_keys=True, ensure_ascii=False)
        digest = hashlib.sha256(encoded.encode("utf-8")).hexdigest()
        lines.append(f"- {item['publisher_id']} {item['source_uri']} | record_sha256={digest}")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--observations", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--as-of", required=True, help="UTC ISO-8601 timestamp")
    parser.add_argument("--lookback-days", type=int, default=9)
    args = parser.parse_args()
    observed = datetime.fromisoformat(args.as_of)
    if observed.tzinfo is None or args.lookback_days < 1:
        raise ValueError("--as-of must carry a timezone; lookback must be >= 1")
    if args.output.exists():
        raise FileExistsError(f"Will not replace an existing digest: {args.output}")
    items = json.loads(args.observations.read_text(encoding="utf-8"))
    args.output.write_text(render_digest(items, observed, args.lookback_days), encoding="utf-8")


if __name__ == "__main__":
    main()
