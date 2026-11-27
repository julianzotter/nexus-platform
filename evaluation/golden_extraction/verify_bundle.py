"""Check frozen package hashes and score a prediction JSONL. Run from the package."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

from score import load_rows, score


def main():
    options = argparse.ArgumentParser(description=__doc__)
    options.add_argument("predictions", nargs="?")
    options.add_argument("--routing", action="store_true")
    args = options.parse_args()
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest["files_sha256"].items():
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"digest mismatch: {name}")
    truth = "routing-gold.jsonl" if args.routing else "gold.jsonl"
    predictions = Path(args.predictions) if args.predictions else root / (
        "routing-predictions.jsonl" if args.routing else "baseline-predictions.jsonl")
    result = score(load_rows(root / truth), load_rows(predictions))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyError, TypeError, ValueError, OSError) as exc:
        print(json.dumps({"status": "BLOCKED", "error": str(exc)}))
        sys.exit(2)
