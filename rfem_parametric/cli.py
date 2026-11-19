"""W012 RFEM parametric dry-run CLI; no default API connection."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from geometry import build_geometry, load_spec
from targets import rfem5_manifest


def make_receipt(spec: Path, target: str) -> dict[str, Any]:
    """Create a deterministic offline transfer manifest, with no RFEM calls."""
    geom = build_geometry(load_spec(spec))
    payload = rfem5_manifest(geom) if target == "rfem5" else {
        "adapter": "RFEM6_API_II", "mode": "TRANSFER_PREVIEW_ONLY",
        "model": geom, "solver": "NOT_RUN", "readback": "NOT_RUN",
    }
    body = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return {"sha256": hashlib.sha256(body.encode()).hexdigest(), "payload": payload}


def write_receipt_exclusive(path: Path, receipt: dict[str, Any]) -> None:
    """Write one new JSON report; never overwrite a previous receipt."""
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(receipt, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    parser.add_argument("--target", choices=["rfem5", "rfem6"], required=True)
    parser.add_argument("--out", type=Path, help="new JSON receipt path; existing files rejected")
    args = parser.parse_args()
    receipt = make_receipt(args.spec, args.target)
    if args.out:
        write_receipt_exclusive(args.out, receipt)
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
