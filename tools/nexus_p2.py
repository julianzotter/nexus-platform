"""Read-only P2 acceptance. Production transport is fixed; test doubles are never CLI inputs."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

REPO = "julianzotter/nexus-platform"
EVIDENCE_GATES = ("P0", "REGISTRY", "FEED", "DRIVE", "GITHUB", "SNAPSHOT", "PANEL", "ACL")
REQUIRED = ("BASELINE", "ACTIONS_DELIVERY", *EVIDENCE_GATES)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate key in approved baseline")
        result[key] = value
    return result


def read_baseline(path, expected_hash):
    if not path or not re.fullmatch(r"[0-9a-fA-F]{64}", expected_hash or ""):
        raise ValueError("Approved baseline and independently obtained ID01 SHA-256 required")
    with Path(path).open("rb") as stream:
        raw = stream.read(1024 * 1024 + 1)
    if len(raw) > 1024 * 1024 or sha(raw) != expected_hash.lower():
        raise ValueError("Approved baseline digest or size invalid")
    doc = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_keys)
    if not isinstance(doc, dict) or doc.get("repository") != REPO or doc.get("branch") != "main":
        raise ValueError("Approved baseline must identify nexus-platform/main")
    if not re.fullmatch("[0-9a-f]{40}", str(doc.get("github_commit", ""))):
        raise ValueError("Invalid approved main revision")
    age = doc.get("max_age_seconds")
    if type(age) is not int or age <= 0:
        raise ValueError("Missing positive maximum evidence age")
    return doc, sha(raw)


def canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False).encode()


def blocked(detail):
    return {"status": "BLOCKED", "detail": detail}


def decide(baseline_path, expected_hash, evidence_dir, now, actions, evidence):
    gates = {key: blocked("Approved baseline unavailable") for key in REQUIRED}
    report = {
        "schema": "nexus.sync.p2/1", "repository": REPO, "branch": "main",
        "started_at": now.isoformat(), "gates": gates, "baseline_sha256": None,
        "approved_github_commit": None, "production_release": "NOT_GRANTED",
    }
    try:
        doc, digest = read_baseline(baseline_path, expected_hash)
    except (OSError, ValueError, RecursionError) as exc:
        gates["BASELINE"] = blocked(str(exc))
        return report
    report.update(baseline_sha256=digest, approved_github_commit=doc["github_commit"])
    gates["BASELINE"] = {"status": "PASS", "sha256": digest}
    deliveries = []
    try:
        details = actions(doc, now=now)
        deliveries = details["deliveries"]
        if not isinstance(deliveries, list) or not deliveries:
            raise ValueError("Verified delivery targets missing")
        gates["ACTIONS_DELIVERY"] = {"status": "PASS", "evidence": details}
    except Exception as exc:
        # Do not print arbitrary network exceptions, URLs with secrets, or response bodies.
        gates["ACTIONS_DELIVERY"] = blocked(str(exc) if isinstance(exc, ValueError) else type(exc).__name__)
    try:
        checks = evidence(doc, Path(evidence_dir), now, deliveries=deliveries)
        for key in EVIDENCE_GATES:
            result = checks.get(key)
            gates[key] = result if isinstance(result, dict) and result.get("status") in ("PASS", "BLOCKED") else blocked("Required check absent")
    except Exception as exc:
        for key in EVIDENCE_GATES:
            gates[key] = blocked("Evidence could not be evaluated (" + type(exc).__name__ + ")")
    return report


def finish(report, when):
    gates = report["gates"]
    for key, result in list(gates.items()):
        if result.get("status") != "PASS":
            continue
        limit = result.get("valid_until")
        if key == "ACTIONS_DELIVERY":
            limit = result.get("evidence", {}).get("valid_until")
        if limit is None and key not in ("ACTIONS_DELIVERY", "SNAPSHOT"):
            continue
        try:
            expires = datetime.fromisoformat(limit.replace("Z", "+00:00"))
            current = expires.utcoffset() is not None and when < expires
        except (AttributeError, TypeError, ValueError):
            current = False
        if not current:
            gates[key] = {**result, **blocked("Evidence expired or expiry missing at decision time")}
    passed = set(gates) == set(REQUIRED) and all(gates[key]["status"] == "PASS" for key in REQUIRED)
    report.update(checked_at=when.isoformat(), decision="SYNC_VERIFIED" if passed else "P2_BLOCKED")
    return 0 if passed else 2


def save_report(report, directory):
    # A new private directory per run; callers cannot overwrite an existing receipt.
    encoded = canonical(report)
    payload_hash = sha(encoded)
    data = json.dumps({"payload_sha256": payload_hash, "report": report}, indent=2, ensure_ascii=False, allow_nan=False)
    lines = ["# NEXUS P2", "", report["decision"], "", "UTC: " + report["checked_at"],
             "SHA-256 (report payload): " + payload_hash,
             "Baseline SHA-256: " + str(report.get("baseline_sha256")),
             "Approved GitHub main: " + str(report.get("approved_github_commit")), ""]
    for gate, result in report["gates"].items():
        lines.extend(["## " + gate + " · " + result["status"], "",
                      "```json", json.dumps(result, sort_keys=True, ensure_ascii=False, indent=2), "```", ""])
    checksums = []
    for name, text in (("status.json", data), ("status.md", "\n".join(lines))):
        content = (text + "\n").encode("utf-8")
        path = directory / name
        with path.open("xb") as stream:
            stream.write(content)
        checksum = sha(path.read_bytes())
        if checksum != sha(content):
            raise OSError("Local report readback failed")
        checksums.append(checksum + "  " + name)
    sums = ("\n".join(checksums) + "\n").encode()
    with (directory / "SHA256SUMS").open("xb") as stream:
        stream.write(sums)
    if (directory / "SHA256SUMS").read_bytes() != sums:
        raise OSError("Local digest file readback failed")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline")
    parser.add_argument("--baseline-sha256")
    parser.add_argument("--evidence-dir", default=".")
    args = parser.parse_args(argv)
    now = datetime.now(timezone.utc)
    directory = Path(tempfile.mkdtemp(prefix="nexus-p2-" + now.strftime("%y_%m_%d_%H%M%S-")))
    # Lazy imports let a missing baseline produce all blocked gates without external reads.
    def actions(doc, **kwargs):
        from nexus_p2_actions import verify_actions
        return verify_actions(doc, **kwargs)

    def evidence(doc, where, stamp, **kwargs):
        from nexus_p2_evidence import evaluate_evidence
        return evaluate_evidence(doc, where, stamp, **kwargs)

    report = decide(args.baseline, args.baseline_sha256, args.evidence_dir, now, actions, evidence)
    if all(report["gates"][name]["status"] == "PASS" for name in REQUIRED):
        try:
            from nexus_p2_actions import confirm_latest
            bound, _ = read_baseline(args.baseline, args.baseline_sha256)
            confirm_latest(bound, report["gates"]["ACTIONS_DELIVERY"]["evidence"])
        except Exception as exc:
            report["gates"]["ACTIONS_DELIVERY"] = {**report["gates"]["ACTIONS_DELIVERY"],
                **blocked("Final source-run readback failed: " + (str(exc) if isinstance(exc, ValueError) else type(exc).__name__))}
    report["execution"] = "live-read-only"
    result = finish(report, datetime.now(timezone.utc))
    save_report(report, directory)
    print("P2_REPORT_DIR=" + str(directory))
    print("P2_DECISION=" + report["decision"])
    return result


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print("P2_BLOCKED: verifier/report unavailable (" + type(error).__name__ + ")", file=sys.stderr)
        sys.exit(2)
