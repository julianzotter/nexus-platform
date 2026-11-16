"""Repair the existing ledger and append verified missing identities, fail closed.

Default dry-run. --apply requires live credential validation and a fresh CAS probe.
No ID allocation, policy promotion, permission changes, or unconditional fallback.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from delivery_errors import DeliveryError
from deliver_work import DriveClient, WORK, get_access_token, save_json
from drive_conditional import ConditionalDrive, append_events
from persistence_gate import REGISTRY_ID, verified_file

LEDGER_ID = "1Qso4VQE-cySJdxo6j-MNjxxOc5-GJlrK"
ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_LEDGER_SHA = "8b7cafe7f00d3e0b0db9792a1fe8c81fc258cc5de81e6760bcbfd24b37a89cff"
LEDGER_NOTE = "SHA256_SCOPE=merged_2026-11-16T21:50:08.974Z_pre_repair_bytes; current_revision_hash_in_JSONL"


def patch_ledger(raw: bytes, report: dict) -> tuple[bytes, bool]:
    text = raw.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    rows, fields = list(reader), reader.fieldnames
    if not fields or not {"ID", "DRIVE_ID", "SHA256", "NOTE"}.issubset(fields):
        raise DeliveryError("LEDGER_SCHEMA_CONFLICT")
    if any(None in row for row in rows) or len({r["ID"] for r in rows}) != len(rows):
        raise DeliveryError("LEDGER_DUPLICATE_OR_MALFORMED_ROWS")
    by_id = {r["ID"]: r for r in rows}
    if not {"0210", "0211"}.issubset(by_id):
        raise DeliveryError("LEDGER_REPAIR_ROWS_MISSING")
    intended = {"0210": {"DRIVE_ID": report["file_id"], "SHA256": report["sha256"]},
                "0211": {"DRIVE_ID": LEDGER_ID, "SHA256": ORIGINAL_LEDGER_SHA}}
    changed = False
    for identity, updates in intended.items():
        row = by_id[identity]
        for key, value in updates.items():
            if row[key] not in ("", "SEE_REPORT_LOG", value):
                raise DeliveryError("LEDGER_EXISTING_VALUE_CONFLICT")
            changed |= row[key] != value
            row[key] = value
    row = by_id["0211"]
    if LEDGER_NOTE not in row["NOTE"]:
        row["NOTE"] = row["NOTE"].rstrip("; ") + "; " + LEDGER_NOTE
        changed = True
    if not changed:
        return raw, False
    if hashlib.sha256(raw).hexdigest() != ORIGINAL_LEDGER_SHA:
        raise DeliveryError("LEDGER_SOURCE_CONFLICT")
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\r\n" if "\r\n" in text else "\n")
    writer.writeheader()
    writer.writerows(rows)
    bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
    return bom + stream.getvalue().encode("utf-8"), True


def source_event(client: Any, descriptor: dict) -> dict:
    identity = descriptor["file_id"]
    data = client.read(identity)
    digest = hashlib.sha256(data).hexdigest()
    if descriptor.get("sha256") and digest != descriptor["sha256"]:
        raise DeliveryError("ARTIFACT_SOURCE_HASH_CONFLICT")
    meta = client.metadata(identity)
    expected = descriptor.get("name", meta["name"])
    folder = descriptor.get("parent_id", meta["parents"][0])
    meta = verified_file(client, identity, folder, expected, meta["mimeType"], data)
    stable = identity + ":" + str(meta["version"]) + ":" + digest
    return {"artifact_id": "gdrive:" + identity, "provider_file_id": identity,
            "name": expected, "canonical_uri": "https://drive.google.com/file/d/" + identity + "/view",
            "version": meta["modifiedTime"], "provider_modified_at": meta["modifiedTime"],
            "provider_version": meta["version"], "content_sha256": digest,
            "sha256_scope": "complete_raw_file_bytes",
            "operation_id": "nexus-control-repair-v1:" + hashlib.sha256(stable.encode()).hexdigest(),
            "provenance": {"type": "CONTROL_REGISTER_REPAIR", "ticket": "nexus-platform#73"},
            "verification_status": "BYTE_READBACK_VERIFIED_REVIEW_PENDING",
            "registration_status": "REGISTERED", "registered_at": datetime.now(timezone.utc).isoformat(),
            "owner": "ID02", "ticket_id": "nexus-platform#73", "technical_approval": False}


def repair(client: ConditionalDrive, plan: dict, output: Path, apply: bool = False) -> dict:
    if plan.get("schema_version") != "1.0" or not isinstance(plan.get("artifacts"), list):
        raise DeliveryError("REPAIR_PLAN_INVALID")
    ledger = client.snapshot(LEDGER_ID)
    output.mkdir(parents=True, exist_ok=True)
    with (output / "ledger.before.csv").open("xb") as stream:
        stream.write(ledger.data)
    report_descriptor = next(d for d in plan["artifacts"] if d["file_id"] == plan["ledger_report_id"])
    report_event = source_event(client, report_descriptor)
    updated, changed = patch_ledger(ledger.data, {"file_id": report_event["provider_file_id"],
                                                 "sha256": report_event["content_sha256"]})
    events = [source_event(client, d) for d in plan["artifacts"] if d["file_id"] != LEDGER_ID]
    result = {"status": "DRY_RUN", "ledger_would_change": changed,
              "candidate_events": len(events) + 1, "technical_approval": False}
    if not apply:
        return result
    probe = client.probe(WORK)
    result["probe"] = probe
    # Preserve exact pre-write registry bytes outside canonical state for recovery.
    with (output / "registry.before.jsonl").open("xb") as stream:
        stream.write(client.snapshot(REGISTRY_ID).data)
    if changed:
        client.replace_conditional(LEDGER_ID, ledger, updated, "text/csv")
    events += [source_event(client, {"file_id": LEDGER_ID}),
               source_event(client, {"file_id": probe["file_id"], "sha256": probe["sha256"]})]
    result["ledger_status"] = "VERIFIED_CHANGED" if changed else "VERIFIED_ALREADY_REPAIRED"
    result["registry"] = append_events(client, REGISTRY_ID, events)
    # Recheck every source revision and byte hash before reporting full success.
    for event in events:
        descriptor = {"file_id": event["provider_file_id"], "sha256": event["content_sha256"], "name": event["name"]}
        if source_event(client, descriptor)["provider_version"] != event["provider_version"]:
            raise DeliveryError("TARGET_VERSION_CONFLICT")
    result.update(status="CONTROL_REGISTERS_VERIFIED", registration_status="REGISTERED",
                  ledger_file_id=LEDGER_ID, registry_file_id=REGISTRY_ID,
                  ledger_sha256=hashlib.sha256(client.read(LEDGER_ID)).hexdigest())
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=ROOT / "config/control-register-repair-2026-11-16.json")
    parser.add_argument("--output", type=Path, default=ROOT / "reports/control-repair")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--credentials", type=Path, default=ROOT / ".nexus-credentials/drive-oauth.json")
    args = parser.parse_args()
    run_output = args.output / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_") + uuid.uuid4().hex)
    client = None
    try:
        from configure_drive_oauth import read_existing
        environment = dict(os.environ)
        if args.credentials.exists():
            environment.pop("GOOGLE_ACCESS_TOKEN", None)
            environment.update(read_existing(args.credentials))
        client = ConditionalDrive(DriveClient(get_access_token(environment)), run_output / "cas-probe.json")
        result = repair(client, json.loads(args.plan.read_text()), run_output, args.apply)
    except (DeliveryError, OSError, ValueError, KeyError, StopIteration) as exc:
        result = {"status": "BLOCKED", "reason": str(exc) if isinstance(exc, DeliveryError) else type(exc).__name__,
                  "registration_status": "UNCONFIRMED", "technical_approval": False,
                  "limitation": "A ledger write may precede a later registry conflict; inspect saved preimages and rerun safely."}
    result["run_directory"] = str(run_output)
    if client is not None and client.probe_receipt:
        result["probe"] = client.probe_receipt
    save_json(run_output / "repair-receipt.json", result)
    save_json(args.output / "repair-receipt.json", result)
    print(json.dumps(result))
    return 0 if result["status"] in ("DRY_RUN", "CONTROL_REGISTERS_VERIFIED") else 2


if __name__ == "__main__":
    raise SystemExit(main())
