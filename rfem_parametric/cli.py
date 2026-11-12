"""W012 RFEM parametric dry-run CLI; no default API connection."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from geometry import build_geometry, load_spec
from targets import rfem5_manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    parser.add_argument("--target", choices=["rfem5", "rfem6"], required=True)
    args = parser.parse_args()
    geom = build_geometry(load_spec(args.spec))
    payload = rfem5_manifest(geom) if args.target == "rfem5" else {
        "adapter": "RFEM6_API_II", "mode": "TRANSFER_PREVIEW_ONLY",
        "model": geom, "solver": "NOT_RUN", "readback": "NOT_RUN",
    }
    body = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    print(json.dumps({"sha256": hashlib.sha256(body.encode()).hexdigest(), "payload": payload},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
