#!/usr/bin/env python3
"""Restore bounded JSON delivery journals from an earlier attempt of a trusted run."""
from __future__ import annotations

import io
import json
import os
import re
import subprocess
import zipfile
from pathlib import Path

from deliver_work import DeliveryError, MAX_BYTES, REPO, gh_json, save_json, download_artifact


def restore_archive(body: bytes, output: Path) -> int:
    if len(body) > MAX_BYTES:
        raise DeliveryError('STATE_ARCHIVE_TOO_LARGE')
    count = 0
    with zipfile.ZipFile(io.BytesIO(body)) as archive:
        if sum(entry.file_size for entry in archive.infolist()) > MAX_BYTES:
            raise DeliveryError('STATE_ARCHIVE_TOO_LARGE')
        for entry in archive.infolist():
            if not re.fullmatch(r'state/(receipt-)?[0-9]+\.json', entry.filename):
                continue
            state = json.loads(archive.read(entry))
            if not isinstance(state, dict) or not re.fullmatch(r'[0-9a-f]{64}', state.get('key', '')):
                raise DeliveryError('INVALID_RESTORE_STATE')
            target = output / entry.filename
            if target.is_file() and json.loads(target.read_text()) != state:
                raise DeliveryError('RESTORE_STATE_CONFLICT')
            save_json(target, state)
            count += 1
    return count


def main() -> int:
    repo = os.environ.get('GITHUB_REPOSITORY', '')
    run_id = os.environ.get('RESUME_DELIVERY_RUN_ID') or os.environ.get('GITHUB_RUN_ID', '')
    output = Path('reports/delivery'); output.mkdir(parents=True, exist_ok=True)
    if repo != REPO or not run_id.isdigit():
        raise DeliveryError('INVALID_RESTORE_RUN')
    run = gh_json(f'repos/{repo}/actions/runs/{run_id}')
    if run.get('name') != 'NEXUS GitHub to WORK' or run.get('head_branch') != 'main':
        raise DeliveryError('UNTRUSTED_RESTORE_RUN')
    artifacts = []
    page = 1
    while True:
        batch = gh_json(f'repos/{repo}/actions/runs/{run_id}/artifacts?per_page=100&page={page}').get('artifacts', [])
        artifacts.extend(a for a in batch if not a.get('expired') and a.get('name', '').startswith(f'nexus-delivery-state-{run_id}-'))
        if len(batch) < 100:
            break
        page += 1
    if not artifacts:
        save_json(output / 'restore-status.json', {'status': 'NO_PREVIOUS_JOURNAL', 'run_id': run_id})
        return 0
    latest = max(artifacts, key=lambda a: a['created_at'])
    if latest.get('size_in_bytes', MAX_BYTES + 1) > MAX_BYTES:
        raise DeliveryError('STATE_ARCHIVE_TOO_LARGE')
    count = restore_archive(download_artifact(repo, latest), output)
    save_json(output / 'restore-status.json', {'status': 'RESTORED', 'files': count, 'run_id': run_id})
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
