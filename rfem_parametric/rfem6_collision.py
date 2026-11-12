"""Read-only collision preflight for a proposed isolated RFEM6 model name."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def check_candidate(model_list: object, candidate: str) -> dict[str, object]:
    if not candidate.startswith("NEXUS_W012_TEST_") or len(candidate) <= len("NEXUS_W012_TEST_"):
        return {"status": "REJECTED_PREFIX"}
    duplicates = [m for m in model_list.model_info if m.name.casefold() == candidate.casefold()]
    return {"status": "COLLISION" if duplicates else "NAME_AVAILABLE_NOT_RESERVED",
            "candidate": candidate, "collision_count": len(duplicates)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        from dlubal.api import rfem
        with rfem.Application() as app:
            result = check_candidate(app.get_model_list(), args.candidate)
    except Exception as exc:
        result = {"status": "BLOCKED", "error_class": type(exc).__name__}
    result["mode"] = "READ_ONLY_NO_RESERVATION_OR_CREATION"
    with args.out.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
