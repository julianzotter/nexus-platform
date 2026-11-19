"""Append-only run directories and byte-verified JSON receipts."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
from typing import Any
from uuid import uuid4

from .geometry import canonical_bytes, generate


def _write(directory: Path, name: str, value: Any) -> str:
    raw = canonical_bytes(value)
    path = directory / name
    with path.open("xb") as stream: stream.write(raw)
    if path.read_bytes() != raw: raise OSError("JSON byte readback failed")
    return hashlib.sha256(raw).hexdigest()


def run(spec: dict[str, Any], output: Path, *, target: str = "dry-run",
        type_library: Path | None = None, expected_model: Path | None = None,
        port: int = 9000) -> dict[str, Any]:
    if target not in ("dry-run", "sdk-check", "rfem6-new", "rfem5-empty"):
        raise ValueError("Unknown target")
    model = generate(spec)  # Validate before creating any output or connecting.
    folder = output / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_") + uuid4().hex)
    folder.mkdir(parents=True, exist_ok=False)
    hashes = {"input.json": _write(folder, "input.json", spec),
              "geometry.json": _write(folder, "geometry.json", model)}
    receipt: dict[str, Any] = {"status": "DRY_RUN_PASS", "target": target,
        "calculation": "NOT_RUN", "engineering_release": "NOT_GRANTED",
        "scope": model["scope"], "created_at": datetime.now(timezone.utc).isoformat(),
        "normalized_spec_sha256": model["normalized_spec_sha256"], "input_file_sha256": hashes["input.json"], "counts": {k: len(model[k]) for k in ("nodes", "lines", "members")}}
    def checkpoint() -> None:
        with (folder / "progress.jsonl").open("ab") as stream:
            stream.write(canonical_bytes(receipt))
            stream.flush()
            os.fsync(stream.fileno())
    checkpoint()
    try:
        if target == "sdk-check":
            from .rfem6 import sdk_check
            receipt.update(status="SDK_OFFLINE_PASS", **sdk_check(model))
        elif target == "rfem6-new":
            from .rfem6 import write_new
            write_new(model, receipt, port=port, checkpoint=checkpoint)
        elif target == "rfem5-empty":
            from .rfem5 import write_empty
            if type_library is None or expected_model is None:
                raise ValueError("RFEM5 requires type library and exact working-model path")
            write_empty(type_library, expected_model, model, receipt, checkpoint=checkpoint)
    except Exception as error:
        receipt.update(previous_status=receipt["status"], status="FAILED_OR_BLOCKED",
                       error_type=type(error).__name__)
    checkpoint()
    hashes["progress.jsonl"] = hashlib.sha256((folder / "progress.jsonl").read_bytes()).hexdigest()
    hashes["receipt.json"] = _write(folder, "receipt.json", receipt)
    _write(folder, "hashes.json", hashes)
    return {"run_dir": str(folder.resolve()), **receipt}


def parse_spec(text: str) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result: raise ValueError("Duplicate JSON key")
            result[key] = value
        return result
    return json.loads(text, object_pairs_hook=unique)


def load_spec(path: Path) -> dict[str, Any]:
    return parse_spec(path.read_text(encoding="utf-8"))
