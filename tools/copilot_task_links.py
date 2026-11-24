"""Report GitHub Copilot task/PR/head links as JSON, using an authenticated gh CLI."""
import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from collections.abc import Iterator
from typing import Any

Record = dict[str, Any]
API_VERSION = "2026-03-10"


def github(path: str) -> Any:
    response = subprocess.run(
        ["gh", "api", "--hostname", "github.com", "-H", f"X-GitHub-Api-Version: {API_VERSION}", path],
        check=True, capture_output=True, text=True, timeout=90,
    )
    return json.loads(response.stdout)


def pages(path: str, key: str | None = None) -> Iterator[Record]:
    separator = "&" if "?" in path else "?"
    page = 1
    while True:
        result = github(f"{path}{separator}per_page=100&page={page}")
        records = result[key] if key else result
        if not isinstance(records, list):
            raise ValueError(f"Unexpected response for {path}")
        yield from records
        if len(records) < 100:
            return
        page += 1


def make_rows(task: Record, repo: str, pulls: list[Record]) -> list[Record]:
    task_id = task["id"]
    base = {"task_id": task_id, "task_url": f"https://github.com/copilot/tasks/{task_id}",
            "repo": repo, "pr_url": None, "commit_sha": None}
    artifacts = task.get("artifacts")
    if not isinstance(artifacts, list):
        return [dict(base, status="UNRESOLVED")]
    matched = []
    for artifact in artifacts:
        if artifact.get("provider") != "github" or artifact.get("type") != "pull":
            continue
        data = artifact.get("data") or {}
        # GitHub IDs and repository-local PR numbers are distinct identifiers.
        by_id = [p for p in pulls if p["id"] == data.get("id")]
        if data.get("number") is not None:
            by_id = [p for p in (by_id or pulls) if p["number"] == data["number"]
                     and (data.get("id") is None or p["id"] == data["id"])]
        if not by_id and data.get("number") is None:
            # Some producers use a local number. Only accept it with an independent session branch match.
            sessions = {(s.get("head_ref"), s.get("base_ref")) for s in task.get("sessions", [])}
            by_id = [p for p in pulls if p["number"] == data.get("id")
                     and p["head"].get("repo") and p["head"]["repo"].get("full_name") == repo
                     and p["head"].get("ref") and p["base"].get("ref")
                     and (p["head"]["ref"], p["base"]["ref"]) in sessions]
        if len(by_id) != 1:
            matched.append(dict(base, status="UNRESOLVED", pull_artifact=data))
            continue
        pr = by_id[0]
        sha = pr["head"]["sha"]
        if pr["base"]["repo"]["full_name"].casefold() != repo.casefold() or not re.fullmatch("[0-9a-f]{40}", sha):
            raise ValueError(f"Invalid PR identity or SHA for task {task_id}")
        matched.append(dict(base, status="VERIFIED", pr_url=pr["html_url"], commit_sha=sha))
    return matched or [dict(base, status="NO_PR_RECORDED")]


def collect(repos: list[str]) -> Record:
    result = []
    # Query the authenticated user's active AND archived tasks. A failed page aborts the run.
    tasks: dict[str, Record] = {}
    for archived in ("false", "true"):
        for task in pages(f"/agents/tasks?is_archived={archived}", "tasks"):
            tasks[task["id"]] = task
    for repo in dict.fromkeys(repos):
        metadata = github(f"/repos/{repo}")
        relevant = [t for t in tasks.values() if t["repository"]["id"] == metadata["id"]]
        if not relevant:
            continue
        pulls = list(pages(f"/repos/{repo}/pulls?state=all"))
        for listed in relevant:
            task_id = listed["id"]
            task = github(f"/agents/repos/{repo}/tasks/{task_id}")
            if task["id"] != task_id or task["repository"]["id"] != metadata["id"]:
                raise ValueError(f"Task identity mismatch for {repo}")
            result.extend(make_rows(task, metadata["full_name"], pulls))
    result.sort(key=lambda r: (r["repo"], r["task_id"], r["pr_url"] or ""))
    return {"observed_at": datetime.now(timezone.utc).isoformat(), "repositories": repos, "rows": result}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repositories", nargs="+", metavar="OWNER/REPO")
    args = parser.parse_args()
    if any(not re.fullmatch(r"[\w.-]+/[\w.-]+", r) for r in args.repositories):
        parser.error("Pass repositories as OWNER/REPO")
    print(json.dumps(collect(args.repositories), ensure_ascii=False, indent=2))
