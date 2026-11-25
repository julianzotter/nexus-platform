#!/usr/bin/env python3
"""Read-only inventory of a locally mounted Google Drive folder -> registry/file-registry.jsonl.

Runs on the machine where Google Drive for Desktop is mounted (e.g. G:\\Meine Ablage).
Every record uses root "Google Drive" and path relative to the Drive root ("Meine Ablage"),
so ids are stable: id = SHA-256("Google Drive/<path>")[:16] (see tools/validate_registry.py).

Rules (TASK-00004-INVENTORY-AGENT-D.md):
- excluded directories are not entered: __pycache__, .git, node_modules, $RECYCLE.BIN,
  System Volume Information
- credential files (token.json, credentials.json, .env*) are recorded as SKIPPED, never read
- sha256 is null for files > --hash-limit-mb and, by default, for cloud-only placeholders
  (Windows recall-on-access attribute), so the scan does not download the whole Drive
- unreadable files -> status ERROR; nothing is guessed
- atomic write (.tmp -> replace); sources are opened read-only
stdlib only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

ROOT_NAME = "Google Drive"
EXCLUDED_DIRS = {"__pycache__", ".git", "node_modules", "$RECYCLE.BIN", "System Volume Information"}
CREDENTIAL_NAMES = {"token.json", "credentials.json"}
RECALL_ATTRIBUTES = 0x00400000 | 0x00040000  # RECALL_ON_DATA_ACCESS | RECALL_ON_OPEN
CHUNK = 1 << 20


def iter_files(base: Path) -> Iterator[Path]:
    """Yield files below base in deterministic order without entering excluded dirs."""
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDED_DIRS)
        for name in sorted(filenames):
            yield Path(dirpath) / name


def is_credential(name: str) -> bool:
    return name.lower() in CREDENTIAL_NAMES or name.lower().startswith(".env")


def is_cloud_only(info: os.stat_result) -> bool:
    return bool(getattr(info, "st_file_attributes", 0) & RECALL_ATTRIBUTES)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(CHUNK), b""):
            digest.update(block)
    return digest.hexdigest()


def make_record(path: Path, drive_root: Path, hash_limit: int, hash_cloud: bool) -> dict[str, Any]:
    rel = path.relative_to(drive_root).as_posix()
    record: dict[str, Any] = {
        "id": hashlib.sha256(f"{ROOT_NAME}/{rel}".encode("utf-8")).hexdigest()[:16],
        "root": ROOT_NAME, "path": rel, "name": path.name, "ext": path.suffix.lower(),
        "size": 0, "mtime": "1970-01-01T00:00:00Z", "sha256": None, "status": "FOUND",
    }
    try:
        info = path.stat()
        record["size"] = info.st_size
        record["mtime"] = datetime.fromtimestamp(info.st_mtime, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        if not stat.S_ISREG(info.st_mode):
            record.update(status="SKIPPED", skip_reason="not a regular file")
        elif is_credential(path.name):
            record.update(status="SKIPPED", skip_reason="credential file excluded")
        elif info.st_size > hash_limit:
            record["hash_skipped"] = "size limit"
        elif is_cloud_only(info) and not hash_cloud:
            record["hash_skipped"] = "cloud-only placeholder"
        else:
            record["sha256"] = sha256_file(path)
    except OSError as exc:
        record.update(status="ERROR", error=type(exc).__name__)
    return record


def write_jsonl_atomic(records: list[dict[str, Any]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    tmp = output.with_suffix(output.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as stream:
        for record in records:
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=False) + "\n")
    os.replace(tmp, output)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--drive-root", type=Path, required=True, help=r'e.g. "G:\Meine Ablage"')
    parser.add_argument("--folder", action="append", required=True, help="folder below drive root, e.g. _developement")
    parser.add_argument("--output", type=Path, default=Path("registry/file-registry.jsonl"))
    parser.add_argument("--hash-limit-mb", type=int, default=500)
    parser.add_argument("--hash-cloud-only", action="store_true", help="also hash cloud-only files (downloads them)")
    args = parser.parse_args()
    drive_root = args.drive_root.resolve()
    records = []
    for folder in args.folder:
        base = drive_root / folder
        if not base.is_dir():
            print(f"missing folder: {base}", file=sys.stderr)
            return 2
        for path in iter_files(base):
            records.append(make_record(path, drive_root, args.hash_limit_mb << 20, args.hash_cloud_only))
    write_jsonl_atomic(records, args.output)
    counts = {s: sum(r["status"] == s for r in records) for s in ("FOUND", "SKIPPED", "ERROR")}
    hashed = sum(r["sha256"] is not None for r in records)
    print(json.dumps({"files": len(records), **counts, "hashed": hashed}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
