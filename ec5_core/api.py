"""Stable JSON contract: run_check(request) -> result dict."""
from __future__ import annotations

import json
from pathlib import Path

from . import checks

SCHEMA_PATH = Path(__file__).parent / "schemas" / "ec5_check_request.schema.json"

_DISPATCH = {
    "bending": checks.check_bending,
    "shear": checks.check_shear,
    "compression_perpendicular": checks.check_compression_perpendicular,
    "column_buckling": checks.check_column_buckling,
}


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def run_check(request: dict) -> dict:
    """Validate request against the JSON schema, run the check, return a JSON-serialisable result."""
    import jsonschema

    jsonschema.validate(request, load_schema())
    params = {k: v for k, v in request.items() if k != "check"}
    return _DISPATCH[request["check"]](**params).to_dict()
