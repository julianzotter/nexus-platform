#!/usr/bin/env python3
"""Single-writer GitHub artifact -> Drive transfer with readback and resumable IDs.

No LLM decides delivery or human acceptance. Requires authenticated Drive access.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

DRIVE = 'https://www.googleapis.com/drive/v3'
WORK = '1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP'
REPO = 'julianzotter/nexus-platform'
MAX_BYTES = 20 * 1024 * 1024


class DeliveryError(Exception):
    """Sanitized, evidence-preserving transfer failure."""


def retry(operation: Callable[[], Any], sleep: Callable[[float], None] = time.sleep) -> Any:
    for attempt in range(3):
        try:
            return operation()
        except urllib.error.HTTPError as exc:
            if exc.code not in (408, 429, 500, 502, 503, 504) or attempt == 2:
                raise DeliveryError(f'HTTP_{exc.code}') from None
        except (urllib.error.URLError, TimeoutError):
            if attempt == 2:
                raise DeliveryError('NETWORK_RETRY_EXHAUSTED') from None
        sleep(2 ** attempt)
    raise DeliveryError('RETRY_EXHAUSTED')


def request_bytes(request: urllib.request.Request, limit: int = MAX_BYTES) -> bytes:
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read(limit + 1)
    if len(body) > limit:
        raise DeliveryError('PAYLOAD_TOO_LARGE')
    return body


def get_access_token() -> str:
    token = os.environ.get('GOOGLE_ACCESS_TOKEN')
    if token:
        return token
    names = ('NEXUS_GOOGLE_CLIENT_ID', 'NEXUS_GOOGLE_CLIENT_SECRET', 'NEXUS_GOOGLE_REFRESH_TOKEN')
    values = [os.environ.get(name) for name in names]
    if not all(values):
        raise DeliveryError('BLOCKED_DRIVE_CREDENTIALS')
    payload = urllib.parse.urlencode(dict(zip(('client_id', 'client_secret', 'refresh_token'), values)) | {'grant_type': 'refresh_token'}).encode()
    req = urllib.request.Request('https://oauth2.googleapis.com/token', data=payload)
    result = json.loads(retry(lambda: request_bytes(req)))
    if not result.get('access_token'):
        raise DeliveryError('OAUTH_TOKEN_MISSING')
    return result['access_token']


class DriveClient:
    def __init__(self, token: str, sleep: Callable[[float], None] = time.sleep):
        self.token, self.sleep = token, sleep

    def call(self, path: str, method: str = 'GET', data: bytes | None = None,
             content_type: str = 'application/json', upload: bool = False) -> bytes:
        prefix = 'https://www.googleapis.com/upload/drive/v3' if upload else DRIVE
        req = urllib.request.Request(prefix + path, data=data, method=method,
                                     headers={'Authorization': 'Bearer ' + self.token, 'Content-Type': content_type})
        return retry(lambda: request_bytes(req), self.sleep)

    def find(self, folder: str, key: str) -> list[dict]:
        query = f"'{folder}' in parents and trashed=false and appProperties has {{ key='nexus_delivery_key' and value='{key}' }}"
        files: list[dict] = []
        token = ''
        while True:
            params = {'q': query, 'fields': 'nextPageToken,files(id,parents,appProperties)', 'pageSize': 100, 'supportsAllDrives': 'true', 'includeItemsFromAllDrives': 'true'}
            if token:
                params['pageToken'] = token
            result = json.loads(self.call('/files?' + urllib.parse.urlencode(params)))
            files.extend(result.get('files', []))
            token = result.get('nextPageToken', '')
            if not token:
                return files

    def generate_id(self) -> str:
        return json.loads(self.call('/files/generateIds?count=1&space=drive'))['ids'][0]

    def create(self, file_id: str, folder: str, key: str, name: str, data: bytes) -> None:
        boundary = 'nexus_' + uuid.uuid4().hex
        metadata = {'id': file_id, 'name': name, 'parents': [folder], 'appProperties': {'nexus_delivery_key': key, 'sha256': hashlib.sha256(data).hexdigest()}}
        body = (f'--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n'.encode()
                + json.dumps(metadata).encode()
                + f'\r\n--{boundary}\r\nContent-Type: application/octet-stream\r\n\r\n'.encode()
                + data + f'\r\n--{boundary}--\r\n'.encode())
        try:
            self.call('/files?uploadType=multipart&supportsAllDrives=true&fields=id', 'POST', body,
                      f'multipart/related; boundary={boundary}', upload=True)
        except DeliveryError as exc:
            if str(exc) != 'HTTP_409':
                raise
            # Same pre-generated ID may already exist after an ambiguous response.
            # Always verify its identity, parent and content below; never trust 409 alone.

    def metadata(self, file_id: str) -> dict:
        return json.loads(self.call(f'/files/{file_id}?supportsAllDrives=true&fields=id,parents,trashed,appProperties'))

    def read(self, file_id: str) -> bytes:
        return self.call(f'/files/{file_id}?alt=media&supportsAllDrives=true')


def save_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    temporary.replace(path)


def deliver(client: Any, data: bytes, folder: str, source_key: str, name: str,
            journal: Path, source: dict | None = None) -> dict:
    if not re.fullmatch(r'[A-Za-z0-9_-]+', folder):
        raise DeliveryError('INVALID_FOLDER_ID')
    if len(data) > MAX_BYTES:
        raise DeliveryError('PAYLOAD_TOO_LARGE')
    key, digest = hashlib.sha256(source_key.encode()).hexdigest(), hashlib.sha256(data).hexdigest()
    saved = json.loads(journal.read_text()) if journal.is_file() else {}
    if saved and (saved.get('key'), saved.get('sha256'), saved.get('folder')) != (key, digest, folder):
        raise DeliveryError('JOURNAL_SOURCE_CONFLICT')
    matches = client.find(folder, key)
    if len(matches) > 1:
        raise DeliveryError('DUPLICATE_DELIVERY_RECORDS')
    file_id = matches[0]['id'] if matches else saved.get('file_id')
    reused = bool(matches)
    if not file_id:
        file_id = client.generate_id()
    # Persist ID before any create; restore this journal after process/runner loss.
    state = {'key': key, 'sha256': digest, 'folder': folder, 'file_id': file_id}
    save_json(journal, state)
    if not matches:
        client.create(file_id, folder, key, name, data)
    meta = client.metadata(file_id)
    if meta.get('trashed') or folder not in meta.get('parents', []) or meta.get('appProperties', {}).get('nexus_delivery_key') != key:
        raise DeliveryError('TARGET_IDENTITY_CONFLICT')
    if hashlib.sha256(client.read(file_id)).hexdigest() != digest:
        raise DeliveryError('READBACK_HASH_MISMATCH')
    receipt = dict(state, source_key=source_key, state='DELIVERY_VERIFIED', reused=reused,
                   source=source or {}, bytes=len(data), consumer_ack='NOT_OBSERVED', human_acceptance='PENDING')
    return receipt


def gh_bytes(path: str) -> bytes:
    for attempt in range(3):
        result = subprocess.run(['gh', 'api', path], capture_output=True, timeout=60)
        if result.returncode == 0:
            return result.stdout
        if attempt < 2:
            time.sleep(2 ** attempt)
    raise DeliveryError('GITHUB_API_RETRY_EXHAUSTED')


def gh_json(path: str) -> dict:
    return json.loads(gh_bytes(path))


def collect_artifacts(repo: str, run_id: int) -> tuple[dict, list[dict]]:
    if repo != REPO or run_id <= 0:
        raise DeliveryError('UNTRUSTED_SOURCE_REPOSITORY')
    run = gh_json(f'repos/{repo}/actions/runs/{run_id}')
    if run.get('name') != 'NEXUS Monitor' or run.get('head_branch') != 'main' or run.get('status') != 'completed' or run.get('path') != '.github/workflows/nexus-monitor.yml':
        raise DeliveryError('UNTRUSTED_SOURCE_RUN')
    if run.get('head_repository', {}).get('full_name') != repo or not re.fullmatch('[0-9a-f]{40}', run.get('head_sha', '')):
        raise DeliveryError('UNTRUSTED_SOURCE_IDENTITY')
    artifacts: list[dict] = []
    page = 1
    while True:
        batch = gh_json(f'repos/{repo}/actions/runs/{run_id}/artifacts?per_page=100&page={page}').get('artifacts', [])
        artifacts.extend(a for a in batch if a.get('name') == f"nexus-monitor-{run_id}-{run['run_attempt']}" and not a.get('expired'))
        if len(batch) < 100:
            break
        page += 1
    if not artifacts:
        raise DeliveryError('NO_SOURCE_ARTIFACT')
    return run, artifacts


def download_artifact(repo: str, artifact: dict) -> bytes:
    if artifact.get('size_in_bytes', MAX_BYTES + 1) > MAX_BYTES:
        raise DeliveryError('PAYLOAD_TOO_LARGE')
    body = gh_bytes(f"repos/{repo}/actions/artifacts/{int(artifact['id'])}/zip")
    if len(body) > MAX_BYTES:
        raise DeliveryError('PAYLOAD_TOO_LARGE')
    expected = artifact.get('digest', '')
    if not expected.startswith('sha256:') or expected[7:] != hashlib.sha256(body).hexdigest():
        raise DeliveryError('SOURCE_DIGEST_MISMATCH_OR_MISSING')
    with zipfile.ZipFile(io.BytesIO(body)) as archive:
        if sum(f.file_size for f in archive.infolist()) > MAX_BYTES or archive.testzip() is not None:
            raise DeliveryError('INVALID_OR_OVERSIZED_ARCHIVE')
    return body


def execute(args: argparse.Namespace, output: Path) -> dict:
    run, artifacts = collect_artifacts(args.repo, args.run_id)
    client = DriveClient(get_access_token())
    receipts: list[dict] = []
    for artifact in artifacts:
        source_key = f"{args.repo}:{run['id']}:{run['run_attempt']}:{artifact['id']}"
        source = {'repository': args.repo, 'run_id': run['id'], 'run_attempt': run['run_attempt'],
                  'head_sha': run['head_sha'], 'artifact_id': artifact['id'], 'run_url': run['html_url'],
                  'artifact_digest': artifact['digest'], 'run_conclusion': run.get('conclusion')}
        body = download_artifact(args.repo, artifact)
        name = f"NEXUS_{run['id']}_{run['run_attempt']}_{artifact['id']}.zip"
        receipt = deliver(client, body, args.folder, source_key, name,
                          output / 'state' / f"{artifact['id']}.json", source)
        receipts.append(receipt)
        save_json(output / f"receipt-{artifact['id']}.json", receipt)
        # Stable receipt content is itself delivered and byte-verified, independently.
        encoded = json.dumps({k: v for k, v in receipt.items() if k != 'reused'}, sort_keys=True).encode()
        deliver(client, encoded, args.folder, source_key + ':receipt', name + '.receipt.json',
                output / 'state' / f"receipt-{artifact['id']}.json", source)
    return {'status': 'DELIVERY_VERIFIED', 'deliveries': receipts, 'human_acceptance': 'PENDING'}


def failure_status(reason: str) -> str:
    if reason.startswith('BLOCKED') or reason in {'HTTP_400', 'HTTP_401', 'HTTP_403', 'HTTP_404'}:
        return 'BLOCKED'
    if 'CONFLICT' in reason or 'DUPLICATE' in reason:
        return 'CONFLICT'
    if 'DIGEST' in reason or 'HASH_MISMATCH' in reason or 'ARCHIVE' in reason:
        return 'INTEGRITY_FAILED'
    return 'RETRY_REQUIRED'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', default=REPO)
    parser.add_argument('--run-id', required=True, type=int)
    parser.add_argument('--folder', default=WORK)
    parser.add_argument('--output', type=Path, default=Path('reports/delivery'))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    try:
        report = execute(args, args.output)
        code = 0
    except (DeliveryError, OSError, ValueError, KeyError, zipfile.BadZipFile, subprocess.TimeoutExpired) as exc:
        # Only our sanitized errors are surfaced; raw service responses may contain credentials.
        reason = str(exc) if isinstance(exc, DeliveryError) else type(exc).__name__
        report = {'status': failure_status(reason),
                  'reason': reason, 'run_id': args.run_id, 'human_acceptance': 'PENDING'}
        code = 2
    report['recorded_at'] = datetime.now(timezone.utc).isoformat()
    save_json(args.output / 'delivery-status.json', report)
    print(json.dumps(report, ensure_ascii=False))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
