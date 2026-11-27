#!/usr/bin/env python3
"""Read-only NEXUS Control Panel snapshot API. Bind loopback; use external auth proxy."""
from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
GITHUB_REPO = "julianzotter/nexus-platform"
WORK_FOLDER = "1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP"
MAX_PAGES = 10
MAX_ITEMS = 1000
LOCK = threading.Lock()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def request_json(url: str, token: str | None, *, drive: bool = False) -> dict | list:
    headers = {"Accept": "application/json", "User-Agent": "NEXUS-ControlPanel/1.2"}
    if token:
        headers["Authorization"] = "Bearer " + token
    if drive and not token:
        raise RuntimeError("GOOGLE_DRIVE_ACCESS_TOKEN_MISSING")
    try:
        with urlopen(Request(url, headers=headers), timeout=12) as response:
            raw = response.read(2_000_001)
            if len(raw) > 2_000_000:
                raise RuntimeError("UPSTREAM_RESPONSE_TOO_LARGE")
            return json.loads(raw)
    except HTTPError as exc:
        raise RuntimeError(f"UPSTREAM_HTTP_{exc.code}") from None
    except (URLError, TimeoutError) as exc:
        raise RuntimeError("UPSTREAM_UNAVAILABLE") from exc


def drive_inventory(token: str) -> list[dict]:
    records: list[dict] = []
    page_token = ""
    for _ in range(MAX_PAGES):
        query = {
            "q": f"'{WORK_FOLDER}' in parents and trashed = false",
            "fields": "nextPageToken,files(id,name,mimeType,modifiedTime,webViewLink,description)",
            "pageSize": "100",
            "orderBy": "modifiedTime desc",
        }
        if page_token:
            query["pageToken"] = page_token
        endpoint = "https://www.googleapis.com/drive/v3/files?" + urlencode(query)
        data = request_json(endpoint, token, drive=True)
        if not isinstance(data, dict):
            raise RuntimeError("DRIVE_SCHEMA_ERROR")
        for item in data.get("files", []):
            if not isinstance(item, dict) or not item.get("id") or not item.get("name"):
                raise RuntimeError("DRIVE_RECORD_INVALID")
            records.append(item)
        page_token = str(data.get("nextPageToken") or "")
        if len(records) > MAX_ITEMS:
            raise RuntimeError("DRIVE_INVENTORY_EXCEEDS_LIMIT")
        if not page_token:
            return records
    raise RuntimeError("DRIVE_PAGINATION_INCOMPLETE")


def github_open_prs(token: str | None) -> list[dict]:
    url = f"https://api.github.com/repos/{GITHUB_REPO}/pulls?state=open&per_page=100"
    rows = request_json(url, token)
    if not isinstance(rows, list) or len(rows) >= 100:
        raise RuntimeError("GITHUB_PR_PAGINATION_REQUIRED")
    return [{"number": row["number"], "title": row["title"],
             "updatedAt": row["updated_at"], "status": "OPEN",
             "url": row["html_url"]} for row in rows]


def project_records(items: list[dict]) -> tuple[list[dict], list[dict]]:
    work: list[dict] = []
    reports: list[dict] = []
    for item in items:
        name = str(item["name"])
        record = {"id": str(item["id"]), "title": name,
                  "status": "UNVERIFIED", "ack": "NOT_OBSERVED",
                  "revision": "NOT_AVAILABLE", "updatedAt": item.get("modifiedTime"),
                  "sourceId": item["id"]}
        if re.search(r"(WORK.?ORDER|(^|[_-])WO[-_]|WORK-ID)", name, re.I):
            work.append(record)
        elif re.search(r"(REPORT|STATUS|PROTOKOLL|AUDIT)", name, re.I):
            reports.append(record)
    return work, reports


def source_time(records: list[dict], prs: list[dict]) -> str:
    stamps = [str(item["modifiedTime"]) for item in records if item.get("modifiedTime")]
    stamps += [str(item["updatedAt"]) for item in prs if item.get("updatedAt")]
    if not stamps:
        raise RuntimeError("SOURCE_TIMESTAMP_MISSING")
    # Compare real instants, never lexicographic strings with mixed timezone offsets.
    parsed = [(datetime.fromisoformat(s.replace("Z", "+00:00")), s) for s in stamps]
    if any(dt.tzinfo is None for dt, _ in parsed):
        raise RuntimeError("SOURCE_TIMEZONE_MISSING")
    return max(parsed, key=lambda pair: pair[0])[1]


def build_snapshot(drive: list[dict], prs: list[dict]) -> dict:
    work, reports = project_records(drive)
    canonical = json.dumps({"drive": sorted(drive, key=lambda x: str(x["id"])),
                            "prs": sorted(prs, key=lambda x: x["number"])},
                           sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    revision = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return {"schemaVersion": "nexus-controlpanel/2",
            "observedAt": source_time(drive, prs), "checkedAt": now(),
            "sourceRevision": revision, "syncStatus": "SOURCE_READ_OK",
            "workOrders": work, "reports": reports, "githubPullRequests": prs,
            "inventory": {"source": "HISTORICAL_2026_11_25",
                          "gptIds": 219, "kbFolders": 44, "knowledgeReferences": 1967,
                          "verifiedAt": None},
            "limitations": ["NO_ACK_INFERENCE", "METADATA_ONLY",
                            "NO_LEDGER_VERIFICATION", "NO_SITE_DEPLOYMENT"]}


def load_previous(path: Path) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and data.get("sourceRevision"):
            return data
    except (FileNotFoundError, OSError, ValueError):
        pass
    return None


def save_atomic(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(data, ensure_ascii=False, sort_keys=True) + "\n").encode()
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        os.chmod(temporary, 0o600)
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def refresh(state_path: Path) -> tuple[int, dict]:
    with LOCK:
        previous = load_previous(state_path)
        try:
            drive = drive_inventory(os.environ.get("GOOGLE_DRIVE_ACCESS_TOKEN", ""))
            prs = github_open_prs(os.environ.get("GITHUB_TOKEN"))
            fresh = build_snapshot(drive, prs)
            save_atomic(state_path, fresh)
            return 200, fresh
        except (RuntimeError, ValueError, KeyError) as exc:
            error = str(exc)
            if previous is None:
                return 503, {"syncStatus": "ERROR", "checkedAt": now(),
                             "error": error, "workOrders": [], "reports": []}
            return 200, {**previous, "syncStatus": "STALE", "checkedAt": now(),
                         "error": error}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]
        if path == "/api/v1/control-panel/snapshot":
            status, body = refresh(Path(os.environ.get("NEXUS_STATE_FILE", "./.state/nexus.json")))
            self.send_bytes(status, json.dumps(body, ensure_ascii=False).encode(), "application/json")
        elif path == "/":
            self.send_bytes(200, (ROOT / "index.html").read_bytes(), "text/html; charset=utf-8")
        elif path == "/healthz":
            self.send_bytes(200, b'{"service":"up","sourceFreshness":"NOT_CHECKED"}', "application/json")
        else:
            self.send_bytes(404, b'{"error":"NOT_FOUND"}', "application/json")

    def send_bytes(self, code: int, body: bytes, media: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", media)
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy",
                         "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    port = int(os.environ.get("NEXUS_PORT", "8766"))
    if not 1 <= port <= 65535:
        raise ValueError("Invalid port")
    print(f"NEXUS read-only panel at http://127.0.0.1:{port}")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
