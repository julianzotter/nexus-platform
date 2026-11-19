"""Untrusted model text becomes a validated JSON proposal, never Python code."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .core import Orchestrator
from .geometry_run import load_spec, run
from .geometry import canonical_bytes, validate_spec


def plan(prompt_file: Path, output: Path, orchestrator: Any = None) -> dict[str, Any]:
    prompt = prompt_file.read_text(encoding="utf-8")
    if not prompt.strip(): raise ValueError("Empty prompt")
    schema = (Path(__file__).parents[1] / "schemas/geometry-input.schema.json").read_text(encoding="utf-8")
    system = ("Return only one JSON object matching this schema. Never generate or execute Python. "
              "Do not invent project dimensions, catalogs or sources; abstain if missing. "
              "This is a proposal with no engineering approval. Schema: " + schema)
    response = (orchestrator or Orchestrator()).run("rfem_plan", prompt, system)
    # Reuse the duplicate-key-rejecting loader without storing raw model output.
    from .geometry_run import parse_spec
    spec = parse_spec(response["text"])
    validate_spec(spec)
    result = run(spec, output)  # This entrypoint cannot select a live adapter.
    origin = {"prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
              "provider": response.get("provider"), "model": response.get("model"),
              "runtime": response.get("runtime"), "session_id": response.get("session_id"),
              "proposal_status": "SCHEMA_VALID_NOT_ENGINEERING_APPROVED"}
    from .geometry_run import _write
    directory = Path(result["run_dir"])
    _write(directory, "proposal-origin.json", origin)
    # Separate manifest because hashes.json is immutable once created.
    _write(directory, "proposal-hashes.json", {
        "proposal-origin.json": hashlib.sha256((directory / "proposal-origin.json").read_bytes()).hexdigest(),
        "hashes.json": hashlib.sha256((directory / "hashes.json").read_bytes()).hexdigest()})
    return {**result, "proposal": origin}
