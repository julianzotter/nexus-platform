#!/usr/bin/env python3
"""One-time local Google consent and secret installation; never prints token values."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Any

REPO = 'julianzotter/nexus-platform'
ROOT = Path(__file__).resolve().parents[1]


def write_private(path: Path, values: dict[str, str]) -> None:
    if path.is_symlink() or path.exists():
        raise ValueError('Refusing existing or symlink credential target')
    if ROOT not in path.resolve().parents:
        raise ValueError('Credential target must be inside this checkout')
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as stream:
        json.dump(values, stream)


def publish_secrets(values: dict[str, str]) -> None:
    allowed = {'OPENAI_API_KEY', 'NEXUS_GOOGLE_CLIENT_ID', 'NEXUS_GOOGLE_CLIENT_SECRET', 'NEXUS_GOOGLE_REFRESH_TOKEN'}
    if set(values) - allowed or not all(isinstance(v, str) and v and '\n' not in v and '\r' not in v for v in values.values()):
        raise ValueError('Invalid secret name or empty/multiline value')
    status = subprocess.run(['gh', 'auth', 'status', '--hostname', 'github.com'], capture_output=True)
    if status.returncode:
        raise RuntimeError('GitHub CLI authentication required; no secrets were written')
    for name, value in values.items():
        result = subprocess.run(['gh', 'secret', 'set', name, '--repo', REPO], input=value.encode(), capture_output=True)
        if result.returncode:
            raise RuntimeError(f'Secret write failed: {name}; inspect repository Secrets permission')
    print(json.dumps({'repository': REPO, 'secret_names_installed': list(values), 'values_printed': False}))


def authorize(client_path: Path) -> dict[str, str]:
    # Optional setup-only dependency; normal CI/runtime does not need a browser or this library.
    from google_auth_oauthlib.flow import InstalledAppFlow
    client = json.loads(client_path.read_text())
    config = client.get('installed', {})
    if config.get('token_uri') != 'https://oauth2.googleapis.com/token' or config.get('auth_uri') not in {
        'https://accounts.google.com/o/oauth2/auth', 'https://accounts.google.com/o/oauth2/v2/auth'}:
        raise ValueError('Use the original Google Desktop OAuth client JSON')
    flow = InstalledAppFlow.from_client_config(client, scopes=['https://www.googleapis.com/auth/drive'],
                                               autogenerate_code_verifier=True)
    credentials = flow.run_local_server(host='127.0.0.1', port=0, access_type='offline', prompt='consent',
                                        authorization_prompt_message='Authorize the NEXUS Drive writer in the browser.')
    if not credentials.refresh_token:
        raise RuntimeError('No refresh token returned; no secrets installed')
    return {'NEXUS_GOOGLE_CLIENT_ID': credentials.client_id,
            'NEXUS_GOOGLE_CLIENT_SECRET': credentials.client_secret,
            'NEXUS_GOOGLE_REFRESH_TOKEN': credentials.refresh_token}


def read_existing(path: Path) -> dict[str, str]:
    if path.is_symlink() or ROOT not in path.resolve().parents or not path.is_file():
        raise ValueError('Credential target must be a regular private file in this checkout')
    if os.name != 'nt' and path.stat().st_mode & 0o077:
        raise ValueError('Credential file permissions must be owner-only')
    values = json.loads(path.read_text())
    expected = {'NEXUS_GOOGLE_CLIENT_ID', 'NEXUS_GOOGLE_CLIENT_SECRET', 'NEXUS_GOOGLE_REFRESH_TOKEN'}
    if not isinstance(values, dict) or set(values) != expected or not all(isinstance(x, str) and x.strip() and '\n' not in x and '\r' not in x for x in values.values()):
        raise ValueError('Existing file is not the exact NEXUS OAuth credential set')
    return values


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--client-json', type=Path)
    parser.add_argument('--output', type=Path, default=ROOT / '.nexus-credentials/drive-oauth.json')
    parser.add_argument('--publish', action='store_true')
    parser.add_argument('--publish-existing', action='store_true', help='Publish an existing private OAuth file; no new browser consent')
    parser.add_argument('--check', action='store_true', help='Read-only token refresh and exact WORK-folder access check')
    parser.add_argument('--require-write', action='store_true', help='Also require provider canAddChildren metadata; performs no write')
    parser.add_argument('--check-output', type=Path)
    parser.add_argument('--openai-env', type=Path, help='Install existing OPENAI_API_KEY from a local env file')
    args = parser.parse_args()
    if sum(bool(x) for x in (args.check, args.publish_existing, args.openai_env, args.client_json)) != 1:
        parser.error('Choose exactly one: --check, --publish-existing, --client-json, --openai-env')
    if args.check:
        from drive_auth_check import check_access
        from deliver_work import save_json
        environment = dict(os.environ)
        if args.output.exists():
            environment.update(read_existing(args.output))
        report = check_access(args.require_write, environment)
        if args.check_output:
            save_json(args.check_output, report)
        print(json.dumps(report))
        return 0 if report['status'] == 'READ_ACCESS_VERIFIED' else 2
    if args.publish_existing:
        values = read_existing(args.output)
        publish_secrets(values)
        return 0
    if args.openai_env:
        values = dict(line.split('=', 1) for line in args.openai_env.read_text().splitlines() if '=' in line and not line.startswith('#'))
        publish_secrets({'OPENAI_API_KEY': values.get('OPENAI_API_KEY', '').strip()})
        return 0
    values = authorize(args.client_json)
    write_private(args.output, values)
    if args.publish:
        publish_secrets(values)
    print(json.dumps({'credential_file': str(args.output), 'oauth_complete': True, 'published': args.publish, 'values_printed': False}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
