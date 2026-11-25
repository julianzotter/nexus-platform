"""NEXUS CONTROL TOWER - local task manager for the NEXUS ecosystem (127.0.0.1:8770).

Static shell is public and contains no data or token. Every data/mutation route needs the
bearer token, which the browser receives once via the URL fragment (#t=...) from
Start-NexusLocal.cmd and keeps in sessionStorage only.
"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .httpguard import GuardedHandler, LoopbackServer

STATIC = Path(__file__).with_name("static")
STATIC_FILES = {"/": ("index.html", "text/html; charset=utf-8"),
                "/app.js": ("app.js", "text/javascript; charset=utf-8"),
                "/app.css": ("app.css", "text/css; charset=utf-8")}
TOKEN_RE = re.compile(r"[0-9a-f]{32,}")
SECRET_LINE = re.compile(r"(?i)(authorization|bearer|token|password|secret)\S*\s*[:=]\s*\S+")


def tail_log(log_dir: Path, name: str, max_lines: int = 120, max_bytes: int = 32_000) -> list[str]:
    day = datetime.now().strftime("%Y%m%d")
    path = log_dir / f"{name}_{day}.log"
    if not path.is_file():
        return []
    with open(path, "rb") as f:
        f.seek(0, 2)
        size = f.tell()
        f.seek(max(0, size - max_bytes))
        text = f.read().decode("utf-8", "replace")
    lines = text.splitlines()[-max_lines:]
    return [TOKEN_RE.sub("<redacted>", SECRET_LINE.sub(r"\1=<redacted>", ln))[:400] for ln in lines]


def make_handler(sup):
    class Handler(GuardedHandler):
        def do_HEAD(self):
            self.do_GET()

        def do_GET(self):
            url = urlparse(self.path)
            if url.path in STATIC_FILES:
                if not self.guard(require_token=False):
                    return
                fn, ctype = STATIC_FILES[url.path]
                self.send_body(200, (STATIC / fn).read_bytes(), ctype)
                return
            if url.path == "/healthz":
                if not self.guard(require_token=False):
                    return
                self.send_json(200, {"service": "nexus-control-tower", "instance": self.server.instance_id,
                                     "boot_id": sup.boot_id})
                return
            if not self.guard():
                return
            if url.path == "/api/status":
                st = sup.status()
                st["bridges"] = sup.bridge_engine.status() if getattr(sup, "bridge_engine", None) else None
                st["events"] = sup.bridge_engine.ledger.recent_events(40) if getattr(sup, "bridge_engine", None) else []
                st["links"] = sup.cfg.get("links", {})
                self.send_json(200, st)
            elif url.path == "/api/logs":
                name = (parse_qs(url.query).get("task") or ["supervisor"])[0]
                allowed = {"supervisor", *sup.tasks.keys()}
                if name not in allowed:
                    self.send_json(400, {"error": "UNKNOWN_LOG"}); return
                self.send_json(200, {"task": name, "lines": tail_log(sup.log_dir, name)})
            else:
                self.send_json(404, {"error": "NOT_FOUND"})

        def do_POST(self):
            url = urlparse(self.path)
            if not self.guard(browser_mutation=True):
                return
            body = self.read_json_body()
            if body is None:
                return
            if not isinstance(body, dict):
                self.send_json(400, {"error": "OBJECT_REQUIRED"}); return
            if url.path == "/api/task":
                name, action = body.get("name"), body.get("action")
                if not isinstance(name, str) or action not in ("start", "stop", "restart", "run_now"):
                    self.send_json(400, {"error": "INVALID_ARGS"}); return
                res = sup.action(name, action)
                self.send_json(200 if "ok" in res else 400, res)
            elif url.path == "/api/supervisor/stop":
                self.send_json(200, {"ok": True, "stopping": True})
                sup.shutdown()
            else:
                self.send_json(404, {"error": "NOT_FOUND"})

        def do_PUT(self):
            self.send_json(405, {"error": "METHOD_NOT_ALLOWED"})
        do_DELETE = do_PATCH = do_PUT

    return Handler


def build_server(sup, port: int) -> LoopbackServer:
    return LoopbackServer(port, make_handler(sup), sup.token, "nexus-control-tower")
