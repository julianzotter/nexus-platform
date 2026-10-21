"""Package reviewed, non-secret evidence. No network calls or model mutations."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def write_json(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write("\n")


def create_bundle(root: Path, run_id: str, evidence: dict[str, Any]) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,119}", run_id):
        raise ValueError("INVALID_RUN_ID")
    status = evidence.get("status")
    if status not in {"PRECHECK_PASS", "PRECHECK_BLOCKED", "BLOCKED", "REVIEW_CANDIDATE"}:
        raise ValueError("INVALID_STATUS")
    if not isinstance(evidence.get("observations"), list):
        raise ValueError("OBSERVATIONS_REQUIRED")
    # Serialize before touching storage, rejecting NaN and invalid JSON objects.
    json.dumps(evidence, allow_nan=False)
    target = root / run_id
    target.mkdir(parents=True, exist_ok=False)
    now = datetime.now(timezone.utc).isoformat()
    write_json(target / "evidence.json", evidence)
    write_json(target / "status.json", {
        "run_id": run_id, "recorded_at": now, "status": status,
        "evidence": "evidence.json", "final_release": "HUMAN_SIGNOFF_REQUIRED"})
    with (target / "observations.jsonl").open("x", encoding="utf-8") as stream:
        for item in evidence["observations"]:
            stream.write(json.dumps(item, ensure_ascii=False, allow_nan=False) + "\n")
    hashes = []
    for path in sorted(target.iterdir()):
        hashes.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n")
    (target / "SHA256SUMS.txt").write_text("".join(hashes), encoding="utf-8")
    verify_bundle(target)
    return target


def verify_bundle(target: Path) -> None:
    for line in (target / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        expected, name = line.split("  ", 1)
        if Path(name).name != name or name in {".", ".."}:
            raise ValueError("INVALID_CHECKSUM_PATH")
        actual = hashlib.sha256((target / name).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"READBACK_MISMATCH:{name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    value = json.loads(args.evidence.read_text(encoding="utf-8"))
    target = create_bundle(args.out, args.run_id, value)
    print(json.dumps({"path": str(target), "raw_byte_readback": "PASS"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
