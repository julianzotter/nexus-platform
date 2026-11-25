"""Shared helpers: config, atomic writes, hashing, daily logs, Windows flags."""
from __future__ import annotations

import hashlib
import json
import logging
import os
import secrets
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from zoneinfo import ZoneInfo
    VIENNA = ZoneInfo("Europe/Vienna")
except Exception:  # tzdata missing on Windows without the package
    VIENNA = None

IS_WINDOWS = os.name == "nt"
CREATE_NO_WINDOW = 0x08000000
CREATE_NEW_PROCESS_GROUP = 0x00000200

SECRET_PATTERNS = (".env", ".env.*", "*.key", "*.pem", "*.p12", "*.pfx", "*.secret", "token.json",
                   "*.token", "client_secret*.json", "credentials*.json", "drive-oauth.json",
                   "service_account*.json", "id_rsa*", "id_ed25519*", "*.kdbx")


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _vienna_fallback(utc: datetime) -> datetime:
    """EU rule without tzdata: CEST from last Sunday March 01:00 UTC to last Sunday October 01:00 UTC."""
    from datetime import timedelta, timezone as tz

    def last_sunday(year: int, month: int) -> datetime:
        d = datetime(year, month + 1, 1, 1, tzinfo=tz.utc) - timedelta(days=1)
        return d - timedelta(days=(d.weekday() + 1) % 7)
    y = utc.year
    summer = last_sunday(y, 3) <= utc < last_sunday(y, 10)
    return utc.astimezone(tz(timedelta(hours=2 if summer else 1), "CEST" if summer else "CET"))


def now_vienna() -> datetime:
    return datetime.now(VIENNA) if VIENNA else _vienna_fallback(now_utc())


def iso(dt: datetime | None = None) -> str:
    return (dt or now_utc()).isoformat(timespec="seconds")


def expand(p: str | None) -> Path | None:
    if not p:
        return None
    return Path(os.path.expandvars(os.path.expanduser(p)))


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def long_path(p: Path) -> str:
    """Return a Windows extended-length path for >240 chars; unchanged elsewhere."""
    s = str(p)
    if IS_WINDOWS and len(s) > 240 and not s.startswith("\\\\?\\"):
        s = os.path.abspath(s)
        return "\\\\?\\UNC\\" + s[2:] if s.startswith("\\\\") else "\\\\?\\" + s
    return s


class DestinationExists(FileExistsError):
    pass


def atomic_write_bytes(path: Path, data: bytes, create_only: bool = False) -> str:
    """Write via temp file in the same directory, then publish.

    create_only=True never replaces an existing destination (Windows os.rename and POSIX
    os.link both fail if the target exists) -> DestinationExists. Returns sha256 of re-read bytes.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".~nexus-", suffix=".tmp", dir=long_path(path.parent))
    published = False
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        target = long_path(path)
        if create_only:
            try:
                if IS_WINDOWS:
                    os.rename(tmp, target)
                else:
                    os.link(tmp, target)
            except FileExistsError as exc:
                raise DestinationExists(str(path)) from exc
        else:
            os.replace(tmp, target)
        published = True
    finally:
        if os.path.exists(tmp) and (not published or not IS_WINDOWS):
            try:
                os.unlink(tmp)  # only our own temp file
            except OSError:
                pass
    back = Path(long_path(path)).read_bytes()
    digest = sha256_bytes(back)
    if digest != sha256_bytes(data):
        raise OSError(f"READBACK_HASH_MISMATCH {path}")
    return digest


def atomic_write_text(path: Path, text: str) -> str:
    return atomic_write_bytes(path, text.encode("utf-8"))


def atomic_write_json(path: Path, obj: Any) -> str:
    return atomic_write_text(path, json.dumps(obj, ensure_ascii=False, indent=2, default=str))


def load_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return default


def ensure_token(path: Path) -> str:
    """Create a random local API token once (user-only ACL is set by the installer)."""
    if path.is_file():
        tok = path.read_text(encoding="utf-8").strip()
        if len(tok) >= 32:
            return tok
    tok = secrets.token_hex(32)
    atomic_write_text(path, tok)
    return tok


class DailyFileHandler(logging.Handler):
    """Append to <name>_YYYYMMDD.log. Never deletes old logs (R1: nichts loeschen)."""

    def __init__(self, directory: Path, name: str):
        super().__init__()
        self.directory, self.name_ = directory, name
        directory.mkdir(parents=True, exist_ok=True)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            day = datetime.now().strftime("%Y%m%d")
            with open(self.directory / f"{self.name_}_{day}.log", "a", encoding="utf-8") as f:
                f.write(self.format(record) + "\n")
        except Exception:
            self.handleError(record)


def setup_logging(log_dir: Path, name: str = "supervisor", console: bool = False) -> logging.Logger:
    log = logging.getLogger("nexus_local")
    log.setLevel(logging.INFO)
    if not any(isinstance(h, DailyFileHandler) for h in log.handlers):
        h = DailyFileHandler(log_dir, name)
        h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(threadName)s %(message)s"))
        log.addHandler(h)
    if console and sys.stderr and not any(type(h) is logging.StreamHandler for h in log.handlers):
        log.addHandler(logging.StreamHandler())
    return log


DEFAULT_CONFIG: dict[str, Any] = {
    "agent_id": "ID08",
    "executor": "nexus-local-supervisor (ID01 Windows workstation)",
    "runtime_dir": "%LOCALAPPDATA%\\NEXUS\\local",
    "paths": {},
    "ports": {"control_tower": 8770, "mcp_gateway": 8766, "nexus_tower": 8765, "ollama": 11434},
    "services": {},
    "bridges": [],
    "git_mirror": {"enabled": False},
    "gpt_to_skill": {"enabled": False},
    "reporter": {"enabled": True},
    "search": {"searxng_url": None},
    "ollama": {"base_url": "http://127.0.0.1:11434", "default_model": "nexus-q35-9b-32k"},
}


def load_config(path: Path) -> dict[str, Any]:
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    user = load_json(path, None)
    if user is None:
        raise ValueError(f"CONFIG_UNREADABLE {path}")
    for k, v in user.items():
        if isinstance(v, dict) and isinstance(cfg.get(k), dict):
            cfg[k].update(v)
        else:
            cfg[k] = v
    cfg["_config_path"] = str(path)
    cfg["_runtime"] = str(expand(cfg["runtime_dir"]))
    return cfg
