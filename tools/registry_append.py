#!/usr/bin/env python3
"""Single-writer, compare-and-swap append to the canonical NEXUS registry files on Drive.

Writes in place (same Drive file ID) so references never break:
  1. ledger CSV  : fill-only patch of empty DRIVE_ID/SHA256 cells (never overwrites)
  2. file-registry.jsonl : append-only events, idempotent by (artifact_id, content_sha256)
Each step: read raw bytes -> verify expected SHA256 (CAS) -> write -> raw readback check.
Placeholder "@SHA_OF:<drive_id>" in an event resolves to the live SHA256 of that file.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

sys.path.insert(0, str(Path(__file__).resolve().parent))
from delivery_errors import DeliveryError  # noqa: E402

REGISTRY_ID = '15m8T5cWbogIup9snzFwiB1g9HqNCoGow'
LEDGER_ID = '1Qso4VQE-cySJdxo6j-MNjxxOc5-GJlrK'
FILL_COLUMNS = ('DRIVE_ID', 'SHA256')


class Drive(Protocol):
    def read(self, file_id: str) -> bytes: ...
    def replace(self, file_id: str, data: bytes, mime_type: str) -> None: ...


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def cas_write(drive: Drive, file_id: str, expected: str | None, new: bytes, mime: str) -> dict[str, Any]:
    """Write only if live bytes still match `expected`; verify raw readback."""
    current = drive.read(file_id)
    if expected and sha(current) != expected:
        raise DeliveryError('CAS_CONFLICT')
    if new == current:
        return {'file_id': file_id, 'changed': False, 'sha256': sha(current)}
    drive.replace(file_id, new, mime)
    if sha(drive.read(file_id)) != sha(new):
        raise DeliveryError('READBACK_HASH_MISMATCH')
    return {'file_id': file_id, 'changed': True, 'before': sha(current), 'sha256': sha(new), 'bytes': len(new)}


def patch_ledger(data: bytes, fills: dict[str, dict[str, str]]) -> bytes:
    """Fill empty or placeholder cells only; refuse to overwrite real values."""
    text = data.decode('utf-8-sig')
    newline = '\r\n' if '\r\n' in text else '\n'
    rows = list(csv.reader(io.StringIO(text)))
    header = rows[0]
    index = {name: header.index(name) for name in FILL_COLUMNS}
    seen = set()
    for row in rows[1:]:
        for col, value in fills.get(row[0], {}).items():
            cell = row[index[col]]
            if cell and cell != value and cell != 'SEE_REPORT_LOG':
                raise DeliveryError(f'LEDGER_FILL_CONFLICT_{row[0]}_{col}')
            row[index[col]] = value
            seen.add(row[0])
    if set(fills) - seen:
        raise DeliveryError('LEDGER_ID_NOT_FOUND')
    out = io.StringIO()
    csv.writer(out, lineterminator=newline).writerows(rows)
    return out.getvalue().encode('utf-8')


def resolve(event: dict[str, Any], drive: Drive) -> dict[str, Any]:
    value = str(event.get('content_sha256', ''))
    if value.startswith('@SHA_OF:'):
        event = dict(event, content_sha256=sha(drive.read(value.split(':', 1)[1])))
    return event


def append_events(data: bytes, events: list[dict[str, Any]], now: str) -> tuple[bytes, list[str]]:
    existing = {(e.get('artifact_id'), e.get('content_sha256'))
                for e in (json.loads(line) for line in data.decode('utf-8').splitlines() if line.strip())}
    lines, added = [], []
    for event in events:
        if (event['artifact_id'], event['content_sha256']) in existing:
            continue
        lines.append(json.dumps(dict(event, registered_at=now), ensure_ascii=False))
        added.append(event['artifact_id'])
    if not lines:
        return data, []
    prefix = data if data.endswith(b'\n') or not data else data + b'\n'
    return prefix + ('\n'.join(lines) + '\n').encode('utf-8'), added


def run(drive: Drive, plan: dict[str, Any], now: str) -> dict[str, Any]:
    result: dict[str, Any] = {'started_at': now}
    ledger = plan.get('ledger')
    if ledger:
        live = drive.read(ledger['file_id'])
        result['ledger'] = cas_write(drive, ledger['file_id'], ledger.get('expected_sha256'),
                                     patch_ledger(live, ledger['fills']), 'text/csv')
    reg = plan['registry']
    events = [resolve(e, drive) for e in reg['events']]
    live = drive.read(reg['file_id'])
    new, added = append_events(live, events, now)
    result['registry'] = cas_write(drive, reg['file_id'], reg.get('expected_sha256'), new, 'application/x-ndjson')
    result['registry']['appended'] = added
    result['status'] = 'REGISTERED_VERIFIED'
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', required=True, type=Path)
    parser.add_argument('--out', type=Path, default=Path('reports/registry/append-result.json'))
    args = parser.parse_args()
    from deliver_work import DriveClient, get_access_token
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    now = datetime.now(timezone.utc).isoformat()
    try:
        result = run(DriveClient(get_access_token()), plan, now)
    except DeliveryError as exc:
        result = {'status': 'BLOCKED', 'reason': str(exc), 'observed_at': now}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))
    return 0 if result['status'] == 'REGISTERED_VERIFIED' else 2


if __name__ == '__main__':
    raise SystemExit(main())
