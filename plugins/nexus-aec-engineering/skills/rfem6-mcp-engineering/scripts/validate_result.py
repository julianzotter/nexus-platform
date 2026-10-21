"""Offline envelope consistency check; does not authenticate RFEM or certify design."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


def values_hash(values: dict[str, Any]) -> str:
    data = json.dumps(values, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def validate(envelope: dict[str, Any], expected_model: str,
             expected_calculation: str) -> list[str]:
    """Return findings; expected identities must come from independent runtime evidence."""
    findings: list[str] = []
    expected = {"schema_version": "0.1.0", "mode": "LIVE", "source": "RFEM",
                "model_fingerprint": expected_model, "calculation_id": expected_calculation}
    if not expected_model.strip() or not expected_calculation.strip():
        findings.append("EXPECTED_IDENTITY_MISSING")
    for key, value in expected.items():
        if envelope.get(key) != value:
            findings.append(f"MISMATCH:{key}")
    for key in ("run_id", "combination_id"):
        if not isinstance(envelope.get(key), str) or not envelope[key].strip():
            findings.append(f"MISSING:{key}")
    if envelope.get("converged") is not True:
        findings.append("NOT_CONVERGED")
    if envelope.get("units") != {"force": "N", "length": "m", "moment": "N*m"}:
        findings.append("UNITS_NOT_SI_CONTRACT")
    try:
        observed = datetime.fromisoformat(envelope.get("observed_at", "").replace("Z", "+00:00"))
        if observed.utcoffset() is None:
            findings.append("TIMESTAMP_WITHOUT_ZONE")
    except (ValueError, TypeError, AttributeError):
        findings.append("INVALID_TIMESTAMP")
    values = envelope.get("values")
    if not isinstance(values, dict) or not values:
        findings.append("VALUES_MISSING")
    else:
        for key, value in values.items():
            if not isinstance(key, str) or not key.strip():
                findings.append("INVALID_QUANTITY_NAME")
            if type(value) not in (int, float):
                findings.append(f"INVALID_VALUE:{key}")
            elif not isinstance(value, int) and not math.isfinite(value):
                findings.append(f"NONFINITE:{key}")
        try:
            if envelope.get("result_sha256") != values_hash(values):
                findings.append("RESULT_HASH_MISMATCH")
        except (ValueError, TypeError):
            findings.append("UNHASHABLE_VALUES")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("envelope", type=Path)
    parser.add_argument("--expected-model", required=True)
    parser.add_argument("--expected-calculation", required=True)
    args = parser.parse_args()
    try:
        data = json.loads(args.envelope.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("envelope must be an object")
        findings = validate(data, args.expected_model, args.expected_calculation)
    except (ValueError, OSError):
        findings = ["INVALID_ENVELOPE_FILE"]
    print(json.dumps({"status": "FAIL" if findings else "ENVELOPE_PASS",
                      "scope": "offline_consistency_only", "findings": findings}))
    return 2 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
