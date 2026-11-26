"""Read-only GitHub Actions and delivery evidence for the ID01-pinned P2 check."""
from __future__ import annotations

import hashlib
import io
import json
import os
import re
import subprocess
from threading import Timer
import zipfile
from datetime import datetime, timedelta, timezone

REPO = "julianzotter/nexus-platform"
WORK = "1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP"
REGISTRY = "15m8T5cWbogIup9snzFwiB1g9HqNCoGow"
MONITOR, POLL, DELIVERY = "nexus-monitor.yml", "nexus-drive-poll.yml", "nexus-delivery.yml"
WORKFLOWS = (MONITOR, POLL, DELIVERY)
FIELDS = "databaseId,status,conclusion,headSha,createdAt,updatedAt,headBranch,attempt,workflowDatabaseId,url"
LIMIT = 20 * 1024 * 1024  # deliver_work.MAX_BYTES
SHA256 = re.compile(r"[0-9a-f]{64}")


def require(condition, code):
    if not condition:
        raise ValueError(code)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def gh_read(args):
    """Do not propagate CLI error bodies or credentials to the report."""
    try:
        with subprocess.Popen(["gh", *args], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                              env={**os.environ, "GH_HOST": "github.com", "GH_PROMPT_DISABLED": "1"}) as proc:
            timer = Timer(90, proc.kill)
            timer.daemon = True
            timer.start()
            try:
                data = proc.stdout.read(LIMIT + 1)
                if len(data) > LIMIT:
                    proc.kill()
                    raise ValueError("GH_RESPONSE_TOO_LARGE")
                require(proc.wait() == 0, "GH_COMMAND_FAILED: " + " ".join(args[:2]))
                return data
            finally:
                timer.cancel()
    except OSError:
        raise ValueError("GH_UNAVAILABLE") from None


def strict_json(data):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            require(key not in out, "DUPLICATE_JSON_KEY")
            out[key] = value
        return out
    def reject(_):
        raise ValueError("INVALID_JSON_NUMBER")
    return json.loads(data.decode("utf-8"), object_pairs_hook=unique, parse_constant=reject)


def instant(value):
    require(isinstance(value, str), "TIMESTAMP_MISSING")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "TIMESTAMP_NO_TIMEZONE")
    return parsed.astimezone(timezone.utc)


def workflows(gh):
    catalog = strict_json(gh(["workflow", "list", "--repo", REPO, "--all", "--limit", "1000",
                              "--json", "path,id,state"]))
    result = {}
    for name in WORKFLOWS:
        matches = [w for w in catalog if w["path"] == ".github/workflows/" + name]
        require(len(matches) == 1 and matches[0]["state"] == "active", "WORKFLOW_INACTIVE: " + name)
        result[name] = matches[0]["id"]
    return result


def latest(gh, name):
    rows = strict_json(gh(["run", "list", "--repo", REPO, "--workflow", name, "--branch", "main",
                           "--limit", "1", "--json", FIELDS]))
    require(type(rows) is list and len(rows) == 1, "LATEST_RUN_MISSING: " + name)
    return rows[0]


def check_run(row, expected, workflow_id, commit, now, age, name):
    for key in ("run_id", "run_attempt"):
        require(type(expected[key]) is int and expected[key] > 0, "INVALID_BASELINE_RUN: " + name)
    require(row["status"] == "completed" and row["conclusion"] == "success", "RUN_NOT_SUCCESSFUL: " + name)
    require(row["workflowDatabaseId"] == workflow_id and row["headBranch"] == "main" and
            row["headSha"] == commit and row["databaseId"] == expected["run_id"] and
            row["attempt"] == expected["run_attempt"], "RUN_BASELINE_MISMATCH: " + name)
    require(row["url"] == f"https://github.com/{REPO}/actions/runs/{row['databaseId']}", "RUN_URL: " + name)
    require(now - age <= instant(row["createdAt"]) <= instant(row["updatedAt"]) <= now, "RUN_TIME: " + name)


def artifact(gh, row, name):
    run_id = row["databaseId"]
    base = f"repos/{REPO}/actions"
    found = []
    page = 1
    while True:
        batch = strict_json(gh(["api", f"{base}/runs/{run_id}/artifacts?per_page=100&page={page}"]))["artifacts"]
        require(isinstance(batch, list), "INCOMPLETE_ARTIFACT_LIST")
        found.extend(a for a in batch if a.get("name") == name)
        if len(batch) < 100:
            break
        page += 1
    require(len(found) == 1, "MISSING_OR_AMBIGUOUS_ARCHIVE: " + name)
    a = found[0]
    require(type(a["id"]) is int and a["id"] > 0 and a["expired"] is False and
            0 < a["size_in_bytes"] <= LIMIT, "INVALID_ARTIFACT_METADATA")
    # GitHub's per-run endpoint binds the archive even if workflow_run is omitted.
    if a.get("workflow_run") is not None:
        source = a["workflow_run"]
        require(source["id"] == run_id and source["head_sha"] == row["headSha"] and
                source["head_branch"] == "main" and source["repository_id"] == source["head_repository_id"],
                "ARTIFACT_RUN_MISMATCH")
    blob = gh(["api", f"{base}/artifacts/{a['id']}/zip"])
    require(len(blob) == a["size_in_bytes"] and a["digest"] == "sha256:" + sha(blob), "ARCHIVE_DIGEST_MISMATCH")
    return a, blob

def check_delivery(archive, source_artifact, monitor_bytes, monitor, delivery):
    """Check the exact files emitted by the pinned nexus-delivery workflow."""
    start = instant(delivery["createdAt"])
    # GitHub run timestamps use second precision; producer clocks provide fractions.
    end = instant(delivery["updatedAt"]) + timedelta(seconds=1)
    monitor_id = monitor["databaseId"]
    attempt = monitor["attempt"]
    aid = source_artifact["id"]
    src_key = f"{REPO}:{monitor_id}:{attempt}:{aid}"
    source = dict(repository=REPO, run_id=monitor_id, run_attempt=attempt, head_sha=monitor["headSha"],
                  artifact_id=aid, run_url=monitor["url"], artifact_digest=source_artifact["digest"],
                  run_conclusion="success")
    targets = []
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        require(len(z.namelist()) == len(set(z.namelist())) and sum(f.file_size for f in z.infolist()) <= LIMIT,
                "INVALID_DELIVERY_ZIP")

        def read(name):
            return strict_json(z.read(name))

        preflight = read("preflight.json")
        require(preflight["status"] == "READ_ACCESS_VERIFIED" and preflight["source"] == "refresh_token" and
                preflight["operation"] == "drive.files.get_work_metadata" and preflight["folder_id"] == WORK and
                preflight["configured"] is True and preflight["missing_names"] == [] and
                preflight["can_add_children"] is True and preflight["write_test"] == "NOT_RUN",
                "OAUTH_REFRESH_NOT_PROVEN")
        status = read("delivery-status.json")
        require(start <= instant(preflight["observed_at"]) <= instant(status["recorded_at"]) < end,
                "RECEIPT_OUTSIDE_RUN")
        require(status["status"] == "PERSISTED_VERIFIED" and status["registration_status"] == "REGISTERED",
                "DELIVERY_INCOMPLETE")
        primary = read(f"receipt-{aid}.json")
        secondary = read(f"receipt-evidence-{aid}.json")
        require(status["deliveries"] == [primary, secondary], "RECEIPT_STATUS_MISMATCH")
        expected_bytes = monitor_bytes
        name = f"NEXUS_{monitor_id}_{attempt}_{aid}.zip"
        for number, item in enumerate((primary, secondary)):
            key = sha(src_key.encode())
            require(item["source"] == source and item["source_key"] == src_key and item["key"] == key and
                    item["folder"] == WORK and item["name"] == name, "RECEIPT_SOURCE_MISMATCH")
            require(item["state"] == "PERSISTED_VERIFIED" and item["delivery_status"] == "FILE_VERIFIED" and
                    item["registration_status"] == "REGISTERED" and item["registry_file_id"] == REGISTRY and
                    SHA256.fullmatch(item["registry_sha256"]), "RECEIPT_NOT_REGISTERED")
            require(item["bytes"] == len(expected_bytes) and item["sha256"] == sha(expected_bytes),
                    "DELIVERY_BYTES_MISMATCH")
            require(re.fullmatch(r"[a-zA-Z0-9_-]+", item["file_id"]) and
                    re.fullmatch(r"[1-9][0-9]*", str(item["provider_version"])), "DRIVE_RECEIPT_IDENTITY")
            targets.append({k: item[k] for k in ("file_id", "provider_version", "sha256", "bytes", "key",
                                                  "registry_file_id")})
            if number == 0:
                # deliver_work freezes this receipt before register_delivery changes the state.
                frozen = {k: item[k] for k in ("key", "sha256", "folder", "file_id", "name", "source_key",
                                                "source", "bytes", "consumer_ack", "human_acceptance", "review_status")}
                frozen.update(state="DELIVERY_VERIFIED", delivery_status="BYTE_READBACK_VERIFIED",
                              registration_status="NOT_CHECKED")
                expected_bytes = json.dumps(frozen, sort_keys=True).encode()
                src_key += ":receipt"
                name += ".receipt.json"
    require(targets[0]["file_id"] != targets[1]["file_id"], "DUPLICATE_DELIVERY_ID")
    return targets


def verify_actions(baseline, *, now=None, gh=None):
    """GET-only production adapter. Incomplete evidence never yields a partial PASS."""
    gh = gh or gh_read
    now = now or datetime.now(timezone.utc)
    try:
        commit = baseline["github_commit"]
        age = baseline["max_age_seconds"]
        require(re.fullmatch(r"[0-9a-f]{40}", commit) and type(age) is int and age > 0, "INVALID_ACTIONS_BASELINE")
        head = strict_json(gh(["api", f"repos/{REPO}/git/ref/heads/main"]))["object"]
        require(head["sha"] == commit and head["type"] == "commit", "MAIN_HEAD_MISMATCH")
        ids = workflows(gh)
        rows = {}
        for name in WORKFLOWS:
            rows[name] = latest(gh, name)
            check_run(rows[name], baseline["actions"][name], ids[name], commit, now, timedelta(seconds=age), name)
        m, d = rows[MONITOR], rows[DELIVERY]
        sm, monitor_bytes = artifact(gh, m, f"nexus-monitor-{m['databaseId']}-{m['attempt']}")
        expected = baseline["monitor_artifact"]
        require(sm["id"] == expected["id"] and sm["digest"] == expected["digest"], "MONITOR_ARTIFACT_BASELINE")
        sd, delivery_bytes = artifact(gh, d, f"nexus-delivery-state-{d['databaseId']}-{d['attempt']}")
        approved_delivery = baseline["delivery_artifact"]
        require(sd["id"] == approved_delivery["id"] and sd["digest"] == approved_delivery["digest"],
                "DELIVERY_ARTIFACT_BASELINE")
        targets = check_delivery(delivery_bytes, sm, monitor_bytes, m, d)
        valid_until = min(instant(row["createdAt"]) for row in rows.values()) + timedelta(seconds=age)
        return {"valid_until": valid_until.isoformat(), "runs": rows, "monitor_artifact_id": sm["id"], "monitor_digest": sm["digest"],
                "delivery_artifact_id": sd["id"], "delivery_digest": sd["digest"], "deliveries": targets}
    except (KeyError, TypeError, AttributeError, OSError, OverflowError, RuntimeError, zipfile.BadZipFile) as exc:
        raise ValueError("INCOMPLETE_ACTIONS_EVIDENCE: " + type(exc).__name__) from None


def confirm_latest(baseline, evidence, *, gh=None):
    """Re-read the three latest runs after source checks, then close on the pinned main HEAD."""
    gh = gh or gh_read
    try:
        commit = baseline["github_commit"]
        for name in WORKFLOWS:
            pinned = baseline["actions"][name]
            original = evidence["runs"][name]
            row = latest(gh, name)
            require(row == original and row["databaseId"] == pinned["run_id"] and row["attempt"] == pinned["run_attempt"]
                    and row["headSha"] == commit and row["headBranch"] == "main"
                    and row["status"] == "completed" and row["conclusion"] == "success",
                    "RUN_CHANGED_DURING_ACCEPTANCE: " + name)
        head = strict_json(gh(["api", f"repos/{REPO}/git/ref/heads/main"]))["object"]
        require(head["type"] == "commit" and head["sha"] == commit, "MAIN_CHANGED_DURING_ACCEPTANCE")
        return True
    except (KeyError, TypeError, AttributeError, OSError) as exc:
        raise ValueError("FINAL_ACTIONS_READ_UNAVAILABLE: " + type(exc).__name__) from None
