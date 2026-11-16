"""ID-preserving Drive v2 conditional writes, gated by an observed probe.

No claim of provider support before stale and concurrent writes reject with 412.
No arbitrary lockfile, unconditional fallback, or blind write retry is used.
"""
from __future__ import annotations

import hashlib
import json
import re
import urllib.error
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from delivery_errors import DeliveryError

API = "https://www.googleapis.com/drive/v2/files/"
UPLOAD = "https://www.googleapis.com/upload/drive/v2/files/"
LIMIT = 20 * 1024 * 1024


@dataclass(frozen=True)
class Snapshot:
    data: bytes
    etag: str


def strong_etag(value: Any) -> str:
    if not isinstance(value, str) or not re.fullmatch(r'"[^"\r\n]+"', value):
        raise DeliveryError("BLOCKED_STRONG_ETAG_REQUIRED")
    return value


class ConditionalDrive:
    def __init__(self, client: Any, probe_journal: Path | None = None):
        self.client = client
        self.probe_receipt: dict | None = None
        self.probe_journal = probe_journal

    def record_probe(self, receipt: dict) -> None:
        from deliver_work import save_json
        self.probe_receipt = receipt
        if self.probe_journal is not None:
            save_json(self.probe_journal, receipt)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.client, name)

    def request(self, url: str, method: str = "GET", data: bytes | None = None,
                etag: str | None = None, mime: str = "application/json") -> bytes:
        headers = {"Authorization": "Bearer " + self.client.token, "Content-Type": mime}
        if etag is not None:
            headers["If-Match"] = strong_etag(etag)
        request = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                body = response.read(LIMIT + 1)
            if len(body) > LIMIT:
                raise DeliveryError("PAYLOAD_TOO_LARGE")
            return body
        except urllib.error.HTTPError as exc:
            raise DeliveryError(f"HTTP_{exc.code}") from None
        except (urllib.error.URLError, TimeoutError):
            raise DeliveryError("CONDITIONAL_REQUEST_OUTCOME_UNKNOWN") from None

    def etag(self, file_id: str) -> str:
        raw = self.request(API + file_id + "?supportsAllDrives=true&fields=id,etag")
        meta = json.loads(raw)
        if meta.get("id") != file_id:
            raise DeliveryError("TARGET_IDENTITY_CONFLICT")
        return strong_etag(meta.get("etag"))

    def snapshot(self, file_id: str) -> Snapshot:
        before = self.etag(file_id)
        data = self.read(file_id)
        if self.etag(file_id) != before:
            raise DeliveryError("REGISTRY_SOURCE_CONFLICT")
        return Snapshot(data, before)

    def put(self, file_id: str, data: bytes, mime: str, etag: str) -> None:
        self.request(UPLOAD + file_id + "?uploadType=media&supportsAllDrives=true&newRevision=true",
                     "PUT", data, etag, mime)

    def replace_conditional(self, file_id: str, before: Snapshot,
                            data: bytes, mime: str) -> str:
        if not self.probe_receipt or self.probe_receipt.get("status") != "CAS_PROBE_PASS":
            raise DeliveryError("BLOCKED_CAS_PROBE_REQUIRED")
        try:
            self.put(file_id, data, mime, before.etag)
        except DeliveryError as exc:
            if str(exc) == "HTTP_412":
                raise DeliveryError("REGISTRY_SOURCE_CONFLICT") from None
            if str(exc) != "CONDITIONAL_REQUEST_OUTCOME_UNKNOWN":
                raise
            # A lost response is reconciled; never replay an ambiguous write.
            if self.read(file_id) != data:
                raise DeliveryError("REGISTRY_WRITE_OUTCOME_UNKNOWN") from None
        raw = self.read(file_id)
        if raw != data:
            raise DeliveryError("REGISTRY_READBACK_CONFLICT")
        return hashlib.sha256(raw).hexdigest()

    def reject_stale(self, file_id: str, etag: str) -> None:
        try:
            self.put(file_id, b"STALE_WRITE_MUST_NOT_COMMIT", "application/octet-stream", etag)
        except DeliveryError as exc:
            if str(exc) == "HTTP_412":
                return
            raise
        raise DeliveryError("BLOCKED_IF_MATCH_NOT_ENFORCED")

    def probe(self, folder: str) -> dict:
        """Retain preallocated identity before create, including failed probes."""
        try:
            return self.probe_run(folder)
        except DeliveryError as exc:
            if self.probe_receipt:
                self.record_probe(dict(self.probe_receipt, status="CAS_PROBE_FAILED", reason=str(exc)))
            raise

    def probe_run(self, folder: str) -> dict:
        file_id = self.generate_id()
        key = "nexus-cas-probe-" + uuid.uuid4().hex
        self.record_probe({"file_id": file_id, "key": key, "status": "CAS_PROBE_PENDING"})
        self.create(file_id, folder, key, "NEXUS_CAS_PROBE_" + file_id + ".bin", b"initial")
        initial = self.snapshot(file_id)
        self.reject_stale(file_id, '"deliberately-stale-' + uuid.uuid4().hex + '"')
        if self.read(file_id) != initial.data:
            raise DeliveryError("BLOCKED_STALE_WRITE_CHANGED_CONTENT")
        payloads = (b"conditional-probe-A", b"conditional-probe-B")

        def attempt(data: bytes) -> str:
            try:
                self.put(file_id, data, "application/octet-stream", initial.etag)
                return "COMMITTED"
            except DeliveryError as exc:
                return str(exc)

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(attempt, payloads))
        if sorted(outcomes) != ["COMMITTED", "HTTP_412"]:
            raise DeliveryError("BLOCKED_CONCURRENT_CAS_PROBE_FAILED")
        winner = payloads[outcomes.index("COMMITTED")]
        self.reject_stale(file_id, initial.etag)
        if self.read(file_id) != winner:
            raise DeliveryError("BLOCKED_CAS_PROBE_READBACK_FAILED")
        self.record_probe({"file_id": file_id, "status": "CAS_PROBE_PASS",
                              "route": "drive-v2-media-put", "outcomes": outcomes,
                              "sha256": hashlib.sha256(winner).hexdigest(),
                              "observed_at": datetime.now(timezone.utc).isoformat()})
        return dict(self.probe_receipt)


def registered_revision(record: dict, event: dict) -> bool:
    """Same verified representation regardless of writer/operation provenance."""
    required = ("artifact_id", "provider_file_id", "name", "canonical_uri", "version", "provenance",
                "verification_status", "registration_status", "registered_at", "owner", "ticket_id")
    if not all(key in record for key in required):
        return False
    try:
        moment = datetime.fromisoformat(record["registered_at"].replace("Z", "+00:00"))
    except (ValueError, TypeError, AttributeError):
        return False
    keys = ("artifact_id", "provider_file_id", "name", "canonical_uri", "version", "content_sha256",
            "sha256_scope", "verification_status")
    return (moment.tzinfo is not None and record.get("registration_status") == "REGISTERED"
            and record.get("provider_version") is not None
            and str(record["provider_version"]) == str(event.get("provider_version"))
            and all(record.get(key) == event.get(key) for key in keys))


def append_events(client: ConditionalDrive, registry_id: str, events: list[dict]) -> dict:
    """One conditional append. Conflicts require a new read/plan, not overwrite."""
    from persistence_gate import records
    if not client.probe_receipt or client.probe_receipt.get("status") != "CAS_PROBE_PASS":
        raise DeliveryError("BLOCKED_CAS_PROBE_REQUIRED")
    before = client.snapshot(registry_id)
    current = records(before.data)
    pending: list[dict] = []
    for event in events:
        revisions = [r for r in current + pending if r.get("artifact_id") == event.get("artifact_id")
                     and r.get("provider_version") is not None
                     and str(r["provider_version"]) == str(event.get("provider_version"))]
        if any(r.get("content_sha256") and r["content_sha256"] != event.get("content_sha256") for r in revisions):
            raise DeliveryError("REGISTRY_REVISION_HASH_CONFLICT")
        if any(registered_revision(r, event) for r in revisions):
            continue
        matches = [r for r in current + pending if r.get("operation_id") == event["operation_id"]]
        if matches:
            comparable = lambda r: {k: v for k, v in r.items() if k != "registered_at"}
            if comparable(matches[-1]) != comparable(event):
                raise DeliveryError("REGISTRY_OPERATION_CONFLICT")
            if event.get("registration_status") == "REGISTERED" and not registered_revision(matches[-1], event):
                raise DeliveryError("REGISTRY_OPERATION_CONFLICT")
        else:
            pending.append(event)
    updated = before.data
    for event in pending:
        updated += (b"" if not updated or updated.endswith(b"\n") else b"\n")
        updated += json.dumps(event, ensure_ascii=False, sort_keys=True).encode() + b"\n"
    digest = client.replace_conditional(registry_id, before, updated, "application/x-ndjson") if pending else hashlib.sha256(before.data).hexdigest()
    return {"inserted": len(pending), "skipped": len(events) - len(pending),
            "registry_sha256": digest, "preserved_prefix_sha256": hashlib.sha256(before.data).hexdigest()}
