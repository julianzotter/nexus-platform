"""Hardened loopback HTTP base for the control tower and the MCP gateway.

- Binds literal 127.0.0.1 only; Windows SO_EXCLUSIVEADDRUSE, no SO_REUSEADDR (no port sharing).
- Exact Host allowlist (127.0.0.1:PORT, localhost:PORT) against DNS rebinding.
- Origin: if present it must be in the exact allowlist, else 403.
- Bearer token compared with secrets.compare_digest; 401 on missing/invalid.
- Content-Length must be a plain non-negative integer <= MAX_BODY; no Transfer-Encoding.
- Socket timeout per connection; strict security headers (CSP, nosniff, no-store, DENY frames).
"""
from __future__ import annotations

import json
import secrets
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from .util import IS_WINDOWS

MAX_BODY = 1_000_000
SO_EXCLUSIVEADDRUSE = getattr(socket, "SO_EXCLUSIVEADDRUSE", -5)  # Windows-only constant (~SO_REUSEADDR)

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Cache-Control": "no-store",
    "Content-Security-Policy": "default-src 'none'; script-src 'self'; style-src 'self'; "
                               "connect-src 'self'; img-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'",
    "Cross-Origin-Resource-Policy": "same-origin",
}


class LoopbackServer(ThreadingHTTPServer):
    allow_reuse_address = False
    daemon_threads = True

    def __init__(self, port: int, handler, token: str, name: str, extra: dict | None = None):
        self.token, self.service_name, self.extra = token, name, extra or {}
        self.instance_id = secrets.token_hex(8)
        self.allowed_hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}
        self.allowed_origins = {f"http://127.0.0.1:{port}", f"http://localhost:{port}"}
        super().__init__(("127.0.0.1", port), handler, bind_and_activate=False)
        try:
            if IS_WINDOWS:
                self.socket.setsockopt(socket.SOL_SOCKET, SO_EXCLUSIVEADDRUSE, 1)
            self.server_bind()
            self.server_activate()
        except OSError:
            self.server_close()
            raise


    def handle_error(self, request, client_address) -> None:  # client aborts etc.: no stderr noise
        import logging
        logging.getLogger("nexus_local.http").debug("connection error from %s", client_address)


class GuardedHandler(BaseHTTPRequestHandler):
    server: LoopbackServer
    timeout = 15
    protocol_version = "HTTP/1.1"
    server_version = "NEXUS-local"
    sys_version = ""

    # ------------------------------------------------------------------ checks
    def guard(self, require_token: bool = True, browser_mutation: bool = False) -> bool:
        if self.client_address[0] != "127.0.0.1":
            self.send_json(403, {"error": "LOOPBACK_ONLY"}); return False
        hosts = self.headers.get_all("Host") or []
        if len(hosts) != 1 or hosts[0] not in self.server.allowed_hosts:
            self.send_json(421, {"error": "HOST_NOT_ALLOWED"}); return False
        if self.headers.get("X-Forwarded-For") or self.headers.get("Forwarded"):
            self.send_json(400, {"error": "FORWARDING_NOT_ALLOWED"}); return False
        origin = self.headers.get("Origin")
        if origin is not None and origin not in self.server.allowed_origins:
            self.send_json(403, {"error": "ORIGIN_NOT_ALLOWED"}); return False
        if browser_mutation:
            site = self.headers.get("Sec-Fetch-Site")
            if site is not None and site not in ("same-origin", "none"):
                self.send_json(403, {"error": "CROSS_SITE_BLOCKED"}); return False
        if require_token:
            auth = self.headers.get("Authorization", "")
            given = auth[7:].strip() if auth.startswith("Bearer ") else ""
            if not given or not secrets.compare_digest(given.encode(), self.server.token.encode()):
                self.send_json(401, {"error": "UNAUTHORIZED"}, extra={"WWW-Authenticate": "Bearer"}); return False
        return True

    def read_json_body(self) -> Any:
        """Return parsed JSON or None after having sent an error."""
        if self.headers.get("Transfer-Encoding"):
            self.send_json(400, {"error": "TRANSFER_ENCODING_NOT_ALLOWED"}); return None
        raw = self.headers.get("Content-Length", "")
        if not raw.isdigit():
            self.send_json(411, {"error": "CONTENT_LENGTH_REQUIRED"}); return None
        length = int(raw)
        if length > MAX_BODY:
            self.send_json(413, {"error": "BODY_TOO_LARGE"}); return None
        ctype = (self.headers.get("Content-Type") or "").split(";")[0].strip().lower()
        if ctype != "application/json":
            self.send_json(415, {"error": "JSON_REQUIRED"}); return None
        try:
            data = self.rfile.read(length)
            return json.loads(data.decode("utf-8")) if data else {}
        except (UnicodeDecodeError, ValueError):
            self.send_json(400, {"error": "INVALID_JSON"}); return None
        except (socket.timeout, OSError):
            self.close_connection = True
            return None

    # ------------------------------------------------------------------ output
    def send_body(self, code: int, body: bytes, ctype: str, extra: dict | None = None) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        for k, v in {**SECURITY_HEADERS, **(extra or {})}.items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD" and body:
            self.wfile.write(body)

    def send_json(self, code: int, obj: Any, extra: dict | None = None) -> None:
        self.send_body(code, json.dumps(obj, ensure_ascii=False, default=str).encode("utf-8"),
                       "application/json; charset=utf-8", extra)

    def send_empty(self, code: int, extra: dict | None = None) -> None:
        self.send_body(code, b"", "text/plain", extra)

    def log_message(self, fmt: str, *args) -> None:  # no request logging (may contain names)
        pass
