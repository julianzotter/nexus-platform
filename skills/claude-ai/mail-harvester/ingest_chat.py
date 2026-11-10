#!/usr/bin/env python3
"""Ingest an exported WhatsApp chat (_chat.txt) into the mail archive DB so it
is searchable alongside e-mail.

Export on the phone: open chat -> Export chat -> Without media. Then:

    python ingest_chat.py path/to/_chat.txt --name "Daniel Civegna"

Date/time parsing is locale-dependent; the common AT/DE iOS and Android
formats are handled. Re-importing the same file is idempotent for unchanged
lines (rows are keyed by line index).
"""
from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

from common import open_db

# iOS:     [28.04.26, 16:53:01] Sender: text
# Android: 28.04.26, 16:53 - Sender: text
_LINE = re.compile(
    r"^\[?\s*(\d{1,2}[./]\d{1,2}[./]\d{2,4}),?\s+"
    r"(\d{1,2}:\d{2}(?::\d{2})?)\s*\]?\s*-?\s*"
    r"([^:]{1,60}?):\s(.*)$"
)
_FORMATS = (
    "%d.%m.%y %H:%M:%S", "%d.%m.%y %H:%M",
    "%d.%m.%Y %H:%M:%S", "%d.%m.%Y %H:%M",
    "%d/%m/%y %H:%M:%S", "%d/%m/%y %H:%M",
    "%m/%d/%y %H:%M:%S", "%m/%d/%y %H:%M",
)


def _parse_ts(date: str, time: str) -> int | None:
    norm = date.replace("/", ".") + " " + time
    for fmt in _FORMATS:
        try:
            return int(datetime.strptime(norm, fmt.replace("/", ".")).timestamp())
        except ValueError:
            continue
    return None


def iter_messages(text: str):
    """Yield (sender, ts, body), joining wrapped continuation lines."""
    sender: str | None = None
    ts: int | None = None
    buf: list[str] = []
    for line in text.splitlines():
        m = _LINE.match(line)
        if m:
            if sender is not None:
                yield sender, ts, "\n".join(buf)
            date, time, sender, msg = m.groups()
            ts = _parse_ts(date, time)
            buf = [msg]
        else:
            buf.append(line)
    if sender is not None:
        yield sender, ts, "\n".join(buf)


def ingest(db: Path, chat_file: Path, chat_name: str) -> int:
    conn = open_db(db)
    text = chat_file.read_text(encoding="utf-8", errors="replace")
    added = 0
    for idx, (sender, ts, body) in enumerate(iter_messages(text)):
        iso = datetime.fromtimestamp(ts).isoformat() if ts else None
        cur = conn.execute(
            """INSERT OR IGNORE INTO messages
               (account, folder, uid, uidvalidity, message_id, date, ts,
                from_addr, to_addr, cc_addr, subject, body, eml_path)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (f"whatsapp:{chat_name}", "chat", idx, 0, None, iso, ts,
             sender, chat_name, None, body[:80], body, str(chat_file)),
        )
        added += cur.rowcount
    conn.commit()
    conn.close()
    return added


def main() -> None:
    ap = argparse.ArgumentParser(description="Ingest a WhatsApp _chat.txt export")
    ap.add_argument("chat_file")
    ap.add_argument("--db", default="mail.db")
    ap.add_argument("--name", required=True, help="label for this chat/contact")
    args = ap.parse_args()
    n = ingest(Path(args.db), Path(args.chat_file), args.name)
    print(f"ingested {n} message(s) from {args.chat_file}")


if __name__ == "__main__":
    main()
