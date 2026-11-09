"""Bind delivery evidence to the existing registry; bounded single-writer mode.

This is a point-in-time receipt, not a distributed lock or human acceptance.
The caller supplies an authenticated Drive client, never a client-side receipt.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from delivery_errors import DeliveryError

REGISTRY_ID = '15m8T5cWbogIup9snzFwiB1g9HqNCoGow'


def records(raw: bytes) -> list[dict]:
    """Preserve old bytes; reject malformed JSONL rather than repairing history."""
    try:
        result = [json.loads(line) for line in raw.decode('utf-8').splitlines()]
        if not all(isinstance(item, dict) for item in result):
            raise ValueError
        return result
    except (UnicodeError, ValueError):
        raise DeliveryError('REGISTRY_INVALID_JSONL') from None


def verified_file(client: Any, file_id: str, folder: str, name: str,
                  mime_type: str, data: bytes) -> dict:
    before = client.metadata(file_id)
    if (before.get('id') != file_id or before.get('trashed') is not False
            or before.get('name') != name or before.get('mimeType') != mime_type
            or folder not in before.get('parents', [])
            or str(before.get('size')) != str(len(data))
            or not before.get('version') or not before.get('modifiedTime')):
        raise DeliveryError('TARGET_IDENTITY_CONFLICT')
    raw = client.read(file_id)
    after = client.metadata(file_id)
    if before != after:
        raise DeliveryError('TARGET_VERSION_CONFLICT')
    if not isinstance(raw, bytes) or raw != data:
        raise DeliveryError('READBACK_HASH_MISMATCH')
    return after


def event_for(meta: dict, receipt: dict, ticket_id: str, owner: str) -> dict:
    return {
        'artifact_id': 'gdrive:' + meta['id'], 'provider_file_id': meta['id'],
        'name': meta['name'], 'canonical_uri': 'https://drive.google.com/file/d/' + meta['id'] + '/view',
        'version': meta['modifiedTime'], 'provider_modified_at': meta['modifiedTime'],
        'provider_version': meta['version'], 'content_sha256': receipt['sha256'],
        'sha256_scope': 'complete_raw_file_bytes', 'operation_id': receipt['key'],
        'provenance': {'type': 'DELIVERY_GATE', 'source': receipt.get('source', {}),
                       'source_key': receipt['source_key']},
        'verification_status': 'BYTE_READBACK_VERIFIED_REVIEW_PENDING',
        'registration_status': 'REGISTERED',
        'registered_at': datetime.now(timezone.utc).isoformat(),
        'owner': owner, 'ticket_id': ticket_id,
    }


def same_event(record: dict, event: dict) -> bool:
    try:
        timestamp = datetime.fromisoformat(record['registered_at'].replace('Z', '+00:00'))
        if timestamp.tzinfo is None:
            return False
    except (KeyError, ValueError, TypeError, AttributeError):
        return False
    keys = ('artifact_id', 'provider_file_id', 'name', 'canonical_uri', 'version',
            'provider_version', 'content_sha256', 'sha256_scope', 'operation_id',
            'registration_status', 'verification_status', 'ticket_id', 'owner', 'provenance')
    return all(record.get(key) == event.get(key) for key in keys)


def append_event(client: Any, event: dict, write_mode: str) -> str:
    """No atomic CAS: caller must provide an exclusive writer for mutation.

    Compare-before-write detects observed conflicts only. Never claim this
    implements an exclusive writer, fencing, a lock, or distributed atomicity.
    """
    before = client.read(REGISTRY_ID)
    parsed = records(before)
    operations = [r for r in parsed if r.get('operation_id') == event['operation_id']]
    if operations and not same_event(operations[-1], event):
        raise DeliveryError('REGISTRY_OPERATION_CONFLICT')
    current = [r for r in parsed if r.get('artifact_id') == event['artifact_id']]
    if current and same_event(current[-1], event):
        return hashlib.sha256(before).hexdigest()
    if write_mode != 'exclusive-writer':
        raise DeliveryError('BLOCKED_REGISTRY_EXCLUSIVE_WRITER_REQUIRED')
    tail = b'' if not before or before.endswith(b'\n') else b'\n'
    updated = before + tail + json.dumps(event, ensure_ascii=False, sort_keys=True).encode('utf-8') + b'\n'
    if client.read(REGISTRY_ID) != before:
        raise DeliveryError('REGISTRY_SOURCE_CONFLICT')
    try:
        client.replace(REGISTRY_ID, updated, 'application/x-ndjson')
    except DeliveryError as exc:
        if str(exc) in {'HTTP_400', 'HTTP_401', 'HTTP_403', 'HTTP_404'}:
            raise
        # A timeout can follow a successful write; reconcile before any retry.
        if client.read(REGISTRY_ID) != updated:
            raise DeliveryError('REGISTRY_WRITE_OUTCOME_UNKNOWN') from None
    readback = client.read(REGISTRY_ID)
    if readback != updated:
        raise DeliveryError('REGISTRY_READBACK_CONFLICT')
    return hashlib.sha256(readback).hexdigest()


def register_delivery(client: Any, receipt: dict, data: bytes, name: str,
                      mime_type: str, ticket_id: str, owner: str,
                      write_mode: str = 'read-only') -> dict:
    """File errors raise; registry errors preserve the verified partial result."""
    if receipt.get('state') != 'DELIVERY_VERIFIED':
        raise DeliveryError('UNVERIFIED_DELIVERY')
    if not ticket_id or not owner:
        raise DeliveryError('BLOCKED_REGISTRY_IDENTITY_REQUIRED')
    if hashlib.sha256(data).hexdigest() != receipt.get('sha256'):
        raise DeliveryError('DELIVERY_INPUT_CONFLICT')
    meta = verified_file(client, receipt['file_id'], receipt['folder'], name, mime_type, data)
    if meta.get('appProperties', {}).get('nexus_delivery_key') != receipt.get('key'):
        raise DeliveryError('DELIVERY_OPERATION_CONFLICT')
    result = dict(receipt, delivery_status='FILE_VERIFIED', registration_status='REGISTRATION_PENDING',
                  review_status='REVIEW_PENDING', human_acceptance='PENDING',
                  verification_scope='point-in-time; no distributed lock', provider_version=meta['version'])
    event = event_for(meta, receipt, ticket_id, owner)
    try:
        registry_sha = append_event(client, event, write_mode)
        # Do not confirm an event for a file changed while registering it.
        if client.metadata(receipt['file_id']) != meta:
            raise DeliveryError('TARGET_VERSION_CONFLICT')
        final_raw = client.read(REGISTRY_ID)
        latest = [r for r in records(final_raw)
                  if r.get('artifact_id') == event['artifact_id']]
        if not latest or not same_event(latest[-1], event):
            raise DeliveryError('REGISTRY_EVENT_CONFLICT')
        result.update(state='PERSISTED_VERIFIED', registration_status='REGISTERED',
                      registry_file_id=REGISTRY_ID, registry_sha256=hashlib.sha256(final_raw).hexdigest())
    except DeliveryError as exc:
        result.update(state='FILE_VERIFIED', registration_error=str(exc))
    return result
