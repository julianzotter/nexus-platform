"""Read-only credential and WORK access check; never prints credential values."""
from __future__ import annotations
import json
import os
from datetime import datetime, timezone
from deliver_work import DriveClient, DeliveryError, WORK, get_access_token

NAMES = ('NEXUS_GOOGLE_CLIENT_ID', 'NEXUS_GOOGLE_CLIENT_SECRET', 'NEXUS_GOOGLE_REFRESH_TOKEN')

def credential_presence(environ: dict[str, str] | None = None) -> dict:
    environ = os.environ if environ is None else environ
    present = {name: bool(environ.get(name, '').strip()) for name in NAMES}
    direct = bool(environ.get('GOOGLE_ACCESS_TOKEN', '').strip())
    return {'source': 'access_token' if direct else 'refresh_token',
            'configured': direct or all(present.values()),
            'missing_names': [] if direct else [name for name, value in present.items() if not value]}

def check_access(require_write: bool = False, environ: dict[str, str] | None = None) -> dict:
    presence = credential_presence(environ)
    report = dict(presence, observed_at=datetime.now(timezone.utc).isoformat(),
                  folder_id=WORK, write_test='NOT_RUN', values_printed=False)
    if not presence['configured']:
        return dict(report, status='BLOCKED', reason='BLOCKED_DRIVE_CREDENTIALS')
    report['operation'] = 'oauth.token_refresh'
    try:
        client = DriveClient(get_access_token(environ))
        report['operation'] = 'drive.files.get_work_metadata'
        metadata = json.loads(client.call('/files/' + WORK +
            '?supportsAllDrives=true&fields=id,mimeType,capabilities(canAddChildren)'))
        if metadata.get('id') != WORK or metadata.get('mimeType') != 'application/vnd.google-apps.folder':
            raise DeliveryError('WORK_IDENTITY_MISMATCH')
        can_add = metadata.get('capabilities', {}).get('canAddChildren')
        if require_write and can_add is not True:
            raise DeliveryError('WORK_WRITE_CAPABILITY_NOT_CONFIRMED')
        return dict(report, status='READ_ACCESS_VERIFIED', can_add_children=can_add,
                    limitation='Metadata capability is not a byte-write/readback receipt.')
    except (DeliveryError, ValueError, OSError) as exc:
        reason = str(exc) if isinstance(exc, DeliveryError) else type(exc).__name__
        return dict(report, status='BLOCKED', reason=reason)

