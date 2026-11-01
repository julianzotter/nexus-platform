"""Fail-closed validation for NEXUS artifact registry (stdlib only)."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

REQUIRED = ("artifact_id", "provider_file_id", "name", "canonical_uri",
            "version", "provenance", "verification_status",
            "registration_status", "registered_at", "owner", "ticket_id")

def validate_record(record: dict) -> list[str]:
    errors = [f"missing: {k}" for k in REQUIRED if k not in record]
    for k in ("artifact_id", "provider_file_id", "name", "canonical_uri",
              "version", "verification_status", "registration_status", "registered_at"):
        if not isinstance(record.get(k), str) or not record[k].strip():
            errors.append(f"invalid: {k}")
    uri = record.get("canonical_uri")
    if isinstance(uri, str):
        p = urlparse(uri)
        if p.scheme != "https" or not p.netloc:
            errors.append("canonical_uri must be HTTPS")
    if not isinstance(record.get("provenance"), dict):
        errors.append("provenance must be object")
    if record.get("artifact_id", "").startswith("gdrive:") and (
        record.get("artifact_id") != f"gdrive:{record.get('provider_file_id')}"):
        errors.append("gdrive artifact_id mismatch")
    return errors

def validate_registry(path: Path, artifact_id: str) -> list[str]:
    if not path.is_file():
        return ["registry missing"]
    errors: list[str] = []
    records: list[dict] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            errors.append(f"line {line_number}: empty line")
            continue
        try:
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError("not an object")
            records.append(record)
            errors.extend(f"line {line_number}: {e}" for e in validate_record(record))
        except ValueError as exc:
            errors.append(f"line {line_number}: {exc}")
    matches = [r for r in records if r.get("artifact_id") == artifact_id]
    if not matches:
        errors.append(f"artifact not registered: {artifact_id}")
    elif matches[-1].get("registration_status") != "REGISTERED":
        errors.append("latest registration not REGISTERED")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--artifact-id", required=True)
    args = parser.parse_args()
    errors = validate_registry(args.registry, args.artifact_id)
    print(json.dumps({"status": "BLOCKED" if errors else "PASS", "errors": errors}))
    return int(bool(errors))

if __name__ == "__main__":
    raise SystemExit(main())
