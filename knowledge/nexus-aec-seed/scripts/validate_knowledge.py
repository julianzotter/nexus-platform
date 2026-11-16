"""Validate safety-critical semantic constraints beyond the JSON Schema draft.

Source-specific values stay unverified unless source byte identity and a locator
are supplied. This is a data QA tool, not an engineering calculation engine.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


UNITS = {
    "lambda": {"W/(m K)"}, "rho": {"kg/m3"}, "mu": {"1"},
    "Rw": {"dB"}, "E_modulus": {"N/mm2", "Pa"},
    "f_strength": {"N/mm2", "Pa"}, "service_life": {"a"},
    "fire_resistance": {"min"}, "fire_class": {"1"},
    "gwp": {"kg CO2e"}, "reusable_share": {"1"},
    "recycled_content": {"1"}, "zifa_score": {"1"},
    "reversible_connection": {"1"}, "layer_group": {"1"},
    "eta_number": {"1"}, "ead_number": {"1"},
}
LCA_METRICS = {"gwp", "ap", "odp", "pocp", "ep", "adp"}


def validate(record: dict) -> list[str]:
    """Check binding-status evidence and non-mixing of LCA declared units."""
    issues: list[str] = []
    src = record.get("source", {})
    scope = record.get("scope", {})
    props = record.get("properties", [])
    if not record.get("record_id") or not src.get("source_uri") or not src.get("locator"):
        issues.append("missing record/source identity or locator")
    if record.get("evidence_status") == "VERIFIED" and not src.get("content_sha256"):
        issues.append("VERIFIED requires real content_sha256")
    if scope.get("binding_status") == "BINDING_VERIFIED":
        for key in ("edition", "effective_date"):
            if not scope.get(key):
                issues.append(f"BINDING_VERIFIED requires {key}")
        if scope.get("country") == "AT" and not scope.get("federal_state"):
            issues.append("Austrian binding requires federal_state")
    if scope.get("binding_status") == "DRAFT" and record.get("engineering_release") == "ID01_APPROVED":
        issues.append("DRAFT regulatory record cannot be released as binding")
    for index, field in enumerate(props):
        name, unit, stage = field.get("name"), field.get("unit"), field.get("stage")
        if name in UNITS and unit not in UNITS[name]:
            issues.append(f"property[{index}] wrong SI canonical unit for {name}: {unit}")
        if name in LCA_METRICS:
            if stage in (None, "NONE") or not field.get("declared_unit"):
                issues.append(f"property[{index}] missing LCA module/declared unit")
            if not field.get("dataset_version"):
                issues.append(f"property[{index}] missing LCA dataset version")
        elif stage not in (None, "NONE"):
            issues.append(f"property[{index}] non-LCA field with lifecycle module")
        if not field.get("locator"):
            issues.append(f"property[{index}] missing source locator")
        if field.get("verification") == "VERIFIED" and not src.get("content_sha256"):
            issues.append(f"property[{index}] VERIFIED without source byte identity")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    record = json.loads(args.record.read_text(encoding="utf-8"))
    issues = validate(record)
    for item in issues:
        print(f"FAIL: {item}")
    if not issues:
        print("PASS: semantic evidence/unit checks")
    return bool(issues)


if __name__ == "__main__":
    raise SystemExit(main())
