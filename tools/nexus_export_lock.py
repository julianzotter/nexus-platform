#!/usr/bin/env python3
"""Server-side hard-lock for NEXUS protocol exports to Google Drive (Run 1 / Step 1).

Replaces the client-side Blob download of TranscriptTimeline.tsx:
- the client (and any LLM) only submits theme, ticket and Markdown; role/session come
  from the authenticated principal; it never names the file or chooses the folder;
- the server builds the AGBS v004 name (YY_MM_DD_HHMM_ID##_THEMA_###.md, Europe/Vienna)
  with a number from a key-idempotent ledger allocator, and writes through
  tools/deliver_work.deliver() (pre-generated ID, journal, SHA-256 readback);
- success only for DELIVERY_VERIFIED and Drive name == reserved name; otherwise
  ExportLockError (fail closed). One export per key at a time (flock). No delete path.

NOTE: no `from __future__ import annotations` here - FastAPI must resolve the body model.
"""
import fcntl
import hashlib
import os
import re
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Iterator, Protocol, Tuple
from zoneinfo import ZoneInfo

from deliver_work import WORK, DeliveryError, deliver
from artifact_registry_gate import validate_record

VIENNA = ZoneInfo('Europe/Vienna')
MAX_MD_BYTES = 2 * 1024 * 1024
ROLE_RE = re.compile(r'ID(0[1-9]|10)')                 # NEXUS-ROLES v1.0: ID01..ID10
THEME_RE = re.compile(r'[A-Z0-9][A-Z0-9+-]{1,59}')      # POSIX-safe, no '_' inside theme
ALLOWED_FOLDERS: dict = {'WORK': WORK}                 # alias -> Drive folder ID (registry-only)
VALIDATION_CODES = ('INVALID_', 'TICKET_ID_REQUIRED', 'TARGET_NOT_IN_REGISTRY', 'EMPTY_PAYLOAD',
                    'PAYLOAD_TOO_LARGE', 'FRONTMATTER_MISSING', 'ARTIFACT_NUMBER_OUT_OF_RANGE')
TRANSIENT_CODES = ('NETWORK_RETRY_EXHAUSTED', 'RETRY_EXHAUSTED', 'HTTP_408', 'HTTP_429', 'HTTP_5')
CONFLICT_CODES = ('READBACK_HASH_MISMATCH', 'TARGET_IDENTITY_CONFLICT', 'DUPLICATE_DELIVERY_RECORDS',
                  'JOURNAL_SOURCE_CONFLICT', 'NAME_MISMATCH', 'NOT_VERIFIED')


class ExportLockError(Exception):
    """Fail-closed export refusal; message is a stable machine code."""


class ArtifactNumberAllocator(Protocol):
    """Ledger allocator. MUST be idempotent per reservation_key and globally monotonic."""

    def allocate(self, reservation_key: str) -> int: ...


@dataclass(frozen=True)
class ExportRequest:
    """role_id/session_id are set server-side from the authenticated principal."""

    role_id: str
    theme: str
    ticket_id: str
    markdown: str
    target: str = 'WORK'
    session_id: str = ''


@dataclass
class ExportReceipt:
    state: str
    file_id: str
    name: str
    sha256: str
    bytes: int
    registry_record: dict = field(default_factory=dict)
    line_endings_normalized: bool = False      # CRLF -> LF before hashing
    consumer_ack: str = 'NOT_OBSERVED'
    human_acceptance: str = 'PENDING'


def validate_request(req: ExportRequest) -> bytes:
    """Reject anything the server cannot deterministically name and place."""
    if not ROLE_RE.fullmatch(req.role_id):
        raise ExportLockError('INVALID_ROLE_ID')
    if not THEME_RE.fullmatch(req.theme):
        raise ExportLockError('INVALID_THEME')
    if not req.ticket_id.strip():
        raise ExportLockError('TICKET_ID_REQUIRED')
    if req.target not in ALLOWED_FOLDERS:
        raise ExportLockError('TARGET_NOT_IN_REGISTRY')
    text = req.markdown.replace('\r\n', '\n')
    data = text.encode('utf-8')
    if not data.strip():
        raise ExportLockError('EMPTY_PAYLOAD')
    if len(data) > MAX_MD_BYTES:
        raise ExportLockError('PAYLOAD_TOO_LARGE')
    if not text.startswith('---\n') or '\n---\n' not in text[4:]:
        raise ExportLockError('FRONTMATTER_MISSING')
    return data


def build_name(role_id: str, theme: str, number: int, now: datetime) -> str:
    """AGBS v004: YY_MM_DD_HHMM_ID##_THEMA_###.md, HHMM = Europe/Vienna."""
    if not 1 <= number <= 999:
        raise ExportLockError('ARTIFACT_NUMBER_OUT_OF_RANGE')
    return f"{now.astimezone(VIENNA):%y_%m_%d_%H%M}_{role_id}_{theme}_{number:03d}.md"


def registry_record(receipt: dict, name: str, req: ExportRequest, now: datetime) -> dict:
    """Pending file-registry.jsonl entry (AGBS v004 §2-§5); not a release."""
    file_id = receipt['file_id']
    record = {
        'artifact_id': f'gdrive:{file_id}', 'provider_file_id': file_id, 'name': name,
        'canonical_uri': f'https://drive.google.com/file/d/{file_id}/view',
        'version': '1', 'provenance': {'writer': 'nexus_export_lock', 'role_id': req.role_id,
                                       'session_id': req.session_id, 'sha256': receipt['sha256']},
        'verification_status': 'REVIEW_PENDING', 'registration_status': 'REGISTRATION_PENDING',
        'registered_at': now.astimezone(VIENNA).isoformat(timespec='seconds'),
        'owner': 'ID01', 'ticket_id': req.ticket_id,
    }
    errors = validate_record(record)
    if errors:
        raise ExportLockError('REGISTRY_RECORD_INVALID:' + ';'.join(errors))
    return record


@contextmanager
def key_lock(path: Path) -> Iterator[None]:
    """Exclusive per-key lock on ONE host. Deployment contract: single replica, local disk
    (not NFS); scale-out requires a shared lock (e.g. DB advisory lock)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'a+') as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def _write_atomic(path: Path, text: str) -> None:
    tmp = path.with_name(f'{path.name}.{os.getpid()}.{os.urandom(4).hex()}.tmp')
    tmp.write_text(text, encoding='utf-8')
    tmp.replace(path)


def _reserve_name(sidecar: Path, existing: list, req: ExportRequest, source_key: str,
                  allocator: ArtifactNumberAllocator, now: Callable[[], datetime]) -> str:
    """Name precedence: Drive (already delivered) > local sidecar > new allocation."""
    if len(existing) == 1 and existing[0].get('name'):
        name = existing[0]['name']
        expected = re.compile(rf'\d{{2}}_\d{{2}}_\d{{2}}_\d{{4}}_{req.role_id}_{re.escape(req.theme)}_\d{{3}}\.md')
        local = sidecar.read_text(encoding='utf-8').strip() if sidecar.is_file() else name
        if not expected.fullmatch(name) or name != local:   # renamed in Drive: never adopt
            raise ExportLockError('NAME_MISMATCH')
    elif sidecar.is_file():
        name = sidecar.read_text(encoding='utf-8').strip()
    else:
        name = build_name(req.role_id, req.theme, allocator.allocate(source_key), now())
    _write_atomic(sidecar, name + '\n')
    return name


def export_protocol(req: ExportRequest, client: Any, allocator: ArtifactNumberAllocator,
                    journal_dir: Path, now: Callable[[], datetime] = lambda: datetime.now(VIENNA)
                    ) -> ExportReceipt:
    """Single server-side write path. Returns only a byte- and name-verified receipt."""
    data = validate_request(req)
    folder, digest = ALLOWED_FOLDERS[req.target], hashlib.sha256(data).hexdigest()
    source_key = f'export:{req.ticket_id}:{req.role_id}:{req.theme}:{digest}'
    key_hash = hashlib.sha256(source_key.encode()).hexdigest()
    with key_lock(journal_dir / f'{key_hash}.lock'):
        try:
            existing = client.find(folder, key_hash)
            name = _reserve_name(journal_dir / f'{key_hash}.name', existing, req, source_key,
                                 allocator, now)
            receipt = deliver(client, data, folder, source_key, name, journal_dir / f'{key_hash}.json')
            drive_name = client.metadata(receipt['file_id']).get('name')
        except DeliveryError as exc:
            raise ExportLockError(f'DELIVERY_FAILED:{exc}') from None
    if receipt.get('state') != 'DELIVERY_VERIFIED' or receipt.get('sha256') != digest:
        raise ExportLockError('NOT_VERIFIED')
    if drive_name != name:
        raise ExportLockError('NAME_MISMATCH')
    return ExportReceipt('DELIVERY_VERIFIED', receipt['file_id'], name, digest, len(data),
                         registry_record(receipt, name, req, now()), '\r\n' in req.markdown)


def http_status(code: str) -> int:
    """422 bad input, 503 retryable, 409 identity/integrity conflict, 502 other provider error."""
    inner = code.split(':', 1)[-1]
    if code.startswith('REGISTRY_RECORD_INVALID'):
        return 500
    if inner == 'BLOCKED_DRIVE_CREDENTIALS':
        return 503
    if code.startswith(VALIDATION_CODES):
        return 422
    if inner.startswith(TRANSIENT_CODES):
        return 503
    if inner in CONFLICT_CODES:
        return 409
    return 502


def build_router(client_factory: Callable[[], Any], allocator: ArtifactNumberAllocator,
                 journal_dir: Path, principal: Callable[[Any], Tuple[str, str]]) -> Any:
    """FastAPI router for nexus_server.py. `principal(request)` -> (role_id, session_id)
    from server-side auth; it must raise HTTPException(401) for unauthenticated callers."""
    from fastapi import APIRouter, HTTPException, Request
    from pydantic import BaseModel, Field

    class ExportBody(BaseModel):
        theme: str = Field(max_length=60)
        ticket_id: str = Field(max_length=120)
        markdown: str = Field(max_length=MAX_MD_BYTES)
        target: str = Field(default='WORK', max_length=32)

    router = APIRouter()

    @router.post('/api/export/protocol')
    def export(body: ExportBody, request: Request) -> dict:
        role_id, session_id = principal(request)
        req = ExportRequest(role_id, body.theme, body.ticket_id, body.markdown, body.target, session_id)
        try:
            try:
                client = client_factory()
            except DeliveryError as exc:
                raise ExportLockError(f'DELIVERY_FAILED:{exc}') from None
            receipt = export_protocol(req, client, allocator, journal_dir)
        except ExportLockError as exc:
            raise HTTPException(status_code=http_status(str(exc)), detail=str(exc)) from None
        except HTTPException:
            raise
        except Exception:                      # never leak internals; fail closed
            raise HTTPException(status_code=500, detail='INTERNAL_ERROR') from None
        return receipt.__dict__

    return router
