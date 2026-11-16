"""Bounded OAuth error classification without service text or credential values."""
from __future__ import annotations

import json
import urllib.error
from typing import Any, Callable

from delivery_errors import DeliveryError

ERRORS = frozenset({
    'invalid_grant', 'invalid_client', 'unauthorized_client', 'invalid_scope',
    'invalid_request', 'access_denied', 'temporarily_unavailable', 'server_error',
    'unsupported_grant_type',
})
TRANSIENT = frozenset({408, 429, 500, 502, 503, 504})


def oauth_request(operation: Callable[[], bytes]) -> bytes:
    """Preserve transient retries; expose only fixed allowlisted permanent errors."""
    try:
        return operation()
    except urllib.error.HTTPError as exc:
        if exc.code in TRANSIENT:
            raise
        body: Any = None
        try:
            raw = exc.read(4097)
            if len(raw) <= 4096:
                body = json.loads(raw)
        except (OSError, ValueError):
            pass
        code = body.get('error') if isinstance(body, dict) else None
        suffix = '_' + code.upper() if isinstance(code, str) and code in ERRORS else ''
        if suffix and body.get('error_subtype') == 'invalid_rapt':
            suffix += '_INVALID_RAPT'
        raise DeliveryError(f'OAUTH_HTTP_{exc.code}{suffix}') from None


def recovery_action(reason: str) -> str:
    if reason.endswith('_INVALID_GRANT') or reason.endswith('_INVALID_RAPT'):
        return 'REAUTHORIZE_GOOGLE_CONSENT'
    if reason.endswith('_INVALID_CLIENT'):
        return 'CHECK_DESKTOP_CLIENT_CONFIGURATION'
    if reason.endswith(('_INVALID_SCOPE', '_UNAUTHORIZED_CLIENT', '_ACCESS_DENIED')):
        return 'CHECK_SCOPE_OR_ADMIN_POLICY'
    return 'INSPECT_SANITIZED_FAILURE_AND_RETRY_IF_APPROPRIATE'
