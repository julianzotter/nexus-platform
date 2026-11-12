"""Shared config, SQLite schema and message parsing for mail-harvester.

Standard library only (Python >= 3.11 for tomllib; on 3.10 install `tomli`).
The local store is a single SQLite database with an FTS5 full-text index so
that mail from every account — and optionally chat exports — is searchable
through one query path.
"""
from __future__ import annotations

import email
import os
import re
import sqlite3
from dataclasses import dataclass, field
from email.header import decode_header, make_header
from email.message import Message
from email.utils import parsedate_to_datetime
from pathlib import Path

try:  # Python >= 3.11
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - fallback for 3.10
    import tomli as tomllib  # type: ignore


# --------------------------------------------------------------------------- #
# Account configuration
# --------------------------------------------------------------------------- #
@dataclass
class Account:
    """One IMAP mailbox. The password is never stored in the config file —
    only the *name* of the environment variable that holds it."""

    name: str
    host: str
    user: str
    password_env: str
    port: int = 993
    folders: list[str] = field(default_factory=list)  # empty == all folders

    @property
    def password(self) -> str:
        pw = os.environ.get(self.password_env)
        if not pw:
            raise SystemExit(
                f"[{self.name}] environment variable {self.password_env} "
                f"is not set — see secrets.env.example"
            )
        return pw


def load_accounts(path: Path) -> list[Account]:
    """Parse accounts.toml into a list of Account objects."""
    data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    return [Account(**entry) for entry in data.get("account", [])]


# --------------------------------------------------------------------------- #
# Database
# --------------------------------------------------------------------------- #
SCHEMA = """
CREATE TABLE IF NOT EXISTS messages (
  id           INTEGER PRIMARY KEY,
  account      TEXT NOT NULL,
  folder       TEXT NOT NULL,
  uid          INTEGER NOT NULL,
  uidvalidity  INTEGER NOT NULL,
  message_id   TEXT,
  date         TEXT,
  ts           INTEGER,
  from_addr    TEXT,
  to_addr      TEXT,
  cc_addr      TEXT,
  subject      TEXT,
  body         TEXT,
  eml_path     TEXT,
  UNIQUE(account, folder, uidvalidity, uid)
);

CREATE TABLE IF NOT EXISTS sync_state (
  account     TEXT,
  folder      TEXT,
  uidvalidity INTEGER,
  last_uid    INTEGER,
  PRIMARY KEY(account, folder)
);

CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(
  subject, from_addr, to_addr, body,
  content='messages', content_rowid='id'
);

CREATE TRIGGER IF NOT EXISTS messages_ai AFTER INSERT ON messages BEGIN
  INSERT INTO messages_fts(rowid, subject, from_addr, to_addr, body)
  VALUES (new.id, new.subject, new.from_addr, new.to_addr, new.body);
END;
"""


def assert_fts5(conn: sqlite3.Connection) -> None:
    """Fail early with a clear message if this SQLite build lacks FTS5."""
    try:
        conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS _fts_probe USING fts5(x)")
        conn.execute("DROP TABLE IF EXISTS _fts_probe")
    except sqlite3.OperationalError as exc:  # pragma: no cover
        raise SystemExit(
            "This Python's SQLite has no FTS5 module. Install a build with "
            "FTS5 enabled, or `pip install pysqlite3-binary`."
        ) from exc


def open_db(path: Path) -> sqlite3.Connection:
    """Open (creating if needed) the archive DB with schema + FTS index."""
    conn = sqlite3.connect(str(path))
    assert_fts5(conn)
    conn.executescript(SCHEMA)
    return conn


# --------------------------------------------------------------------------- #
# Message parsing
# --------------------------------------------------------------------------- #
def _hdr(msg: Message, name: str) -> str:
    """Decode a possibly RFC2047-encoded header into plain text."""
    raw = msg.get(name, "")
    try:
        return str(make_header(decode_header(raw)))
    except Exception:
        return raw or ""


def _decode_part(part: Message) -> str:
    payload = part.get_payload(decode=True) or b""
    charset = part.get_content_charset() or "utf-8"
    try:
        return payload.decode(charset, errors="replace")
    except (LookupError, ValueError):
        return payload.decode("utf-8", errors="replace")


def body_text(msg: Message) -> str:
    """Return a plain-text body, preferring text/plain over stripped HTML."""
    plains: list[str] = []
    htmls: list[str] = []
    for part in msg.walk():
        if part.get_content_disposition() == "attachment":
            continue
        ctype = part.get_content_type()
        if ctype == "text/plain":
            plains.append(_decode_part(part))
        elif ctype == "text/html":
            htmls.append(_decode_part(part))
    if any(plains):
        return "\n".join(p for p in plains if p).strip()
    stripped = re.sub(r"<[^>]+>", " ", "\n".join(htmls))
    return re.sub(r"[ \t]+", " ", stripped).strip()


def _timestamp(msg: Message) -> int | None:
    try:
        dt = parsedate_to_datetime(msg.get("Date"))
        return int(dt.timestamp()) if dt else None
    except (TypeError, ValueError):
        return None


def store_message(
    conn: sqlite3.Connection,
    account: str,
    folder: str,
    uidvalidity: int,
    uid: int,
    raw: bytes,
    eml_path: str,
) -> bool:
    """Parse one RFC822 message and insert it. True if a new row was added."""
    msg = email.message_from_bytes(raw)
    cur = conn.execute(
        """INSERT OR IGNORE INTO messages
           (account, folder, uid, uidvalidity, message_id, date, ts,
            from_addr, to_addr, cc_addr, subject, body, eml_path)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            account, folder, uid, uidvalidity, _hdr(msg, "Message-ID"),
            _hdr(msg, "Date"), _timestamp(msg), _hdr(msg, "From"),
            _hdr(msg, "To"), _hdr(msg, "Cc"), _hdr(msg, "Subject"),
            body_text(msg), eml_path,
        ),
    )
    conn.commit()
    return cur.rowcount > 0
