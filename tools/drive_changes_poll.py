#!/usr/bin/env python3
"""Read-only Drive -> GitHub change feed (iterative, scheduled polling).

Uses Drive changes.list with a persisted page token. Reports only changes whose
ancestor chain reaches a watched folder (default: WORK and WORK/REPORTS).
Never writes to Drive, never commits. Missing credentials -> explicit BLOCKED report.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deliver_work import DRIVE, WORK, DeliveryError, get_access_token, request_bytes, retry  # noqa: E402

REPORTS = '1MVSe1zq-alkb3hIcclimvZvLbCIYI2NV'
DEFAULT_WATCH = (WORK, REPORTS)
MAX_DEPTH = 8
FIELDS = ('nextPageToken,newStartPageToken,changes(fileId,removed,time,'
          'file(id,name,mimeType,parents,modifiedTime,md5Checksum,size,trashed))')


class DriveReader:
    def __init__(self, token: str):
        self.token = token

    def get(self, path: str, params: dict[str, str]) -> dict[str, Any]:
        import urllib.request
        url = f'{DRIVE}{path}?{urllib.parse.urlencode(params)}'
        req = urllib.request.Request(url, headers={'Authorization': f'Bearer {self.token}'})
        return json.loads(retry(lambda: request_bytes(req)))

    def start_token(self) -> str:
        return self.get('/changes/startPageToken', {'supportsAllDrives': 'true'})['startPageToken']

    def changes(self, token: str) -> dict[str, Any]:
        return self.get('/changes', {'pageToken': token, 'fields': FIELDS, 'pageSize': '500',
                                     'supportsAllDrives': 'true', 'includeItemsFromAllDrives': 'true'})

    def parents(self, file_id: str) -> list[str]:
        return self.get(f'/files/{file_id}', {'fields': 'parents', 'supportsAllDrives': 'true'}).get('parents', [])


def in_scope(file: dict[str, Any], watch: set[str], parents_of: Callable[[str], list[str]],
             cache: dict[str, bool]) -> bool:
    frontier, seen = list(file.get('parents') or []), set()
    for _ in range(MAX_DEPTH):
        if not frontier:
            return False
        nxt = []
        for pid in frontier:
            if pid in watch or cache.get(pid):
                return True
            if pid in seen or cache.get(pid) is False:
                continue
            seen.add(pid)
            nxt.extend(parents_of(pid))
        frontier = nxt
    return False


def poll(reader: Any, state: dict[str, Any], watch: set[str]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    token = state.get('page_token')
    if not token:
        return [], {'page_token': reader.start_token(), 'initialized': True}
    events, cache = [], {}
    while True:
        page = reader.changes(token)
        for ch in page.get('changes', []):
            f = ch.get('file') or {}
            if ch.get('removed') or not f:
                continue  # removal without parents cannot be scoped; not reported
            if in_scope(f, watch, reader.parents, cache):
                events.append({'file_id': f.get('id'), 'name': f.get('name'), 'mime_type': f.get('mimeType'),
                               'modified_time': f.get('modifiedTime'), 'md5': f.get('md5Checksum'),
                               'size': f.get('size'), 'trashed': bool(f.get('trashed')),
                               'change_time': ch.get('time')})
        if page.get('nextPageToken'):
            token = page['nextPageToken']
            continue
        return events, {'page_token': page['newStartPageToken'], 'initialized': False}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--state', type=Path, default=Path('.nexus-state/drive-changes-token.json'))
    ap.add_argument('--out', type=Path, default=Path('reports/drive-changes'))
    ap.add_argument('--watch', nargs='*', default=list(DEFAULT_WATCH))
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    state = json.loads(args.state.read_text()) if args.state.exists() else {}
    try:
        reader = DriveReader(get_access_token())
        events, new_state = poll(reader, state, set(args.watch))
    except DeliveryError as exc:
        report = {'status': 'BLOCKED', 'reason': str(exc), 'recorded_at': now}
        (args.out / 'status.json').write_text(json.dumps(report, indent=2))
        print(json.dumps(report))
        return 2
    args.state.parent.mkdir(parents=True, exist_ok=True)
    args.state.write_text(json.dumps(new_state))
    report = {'status': 'INITIALIZED' if new_state['initialized'] else 'OK', 'recorded_at': now,
              'watched_folders': sorted(args.watch), 'change_count': len(events),
              'human_acceptance': 'PENDING'}
    (args.out / 'status.json').write_text(json.dumps(report, indent=2))
    (args.out / 'changes.json').write_text(json.dumps(events, indent=2, ensure_ascii=False))
    print(json.dumps(report))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
