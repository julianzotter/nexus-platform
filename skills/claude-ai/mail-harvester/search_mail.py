#!/usr/bin/env python3
"""Full-text search over the local mail archive (SQLite FTS5).

    python search_mail.py "Kienberg AND Aufbauten"
    python search_mail.py "Lodges" --account zotterconsult --limit 10
    python search_mail.py --from bwm.at --after 2026-04-01
    python search_mail.py "Aufbauten" --from bwm.at --subject Kienberg

The positional query is an FTS5 expression (terms AND-combine by default; use
OR / NOT, "exact phrase", and column filters subject: from_addr: to_addr: body:).
Domains contain a dot, which is special in FTS5 — match senders with the robust
`--from` substring filter instead of `from_addr:bwm.at`. The query is optional:
with only --from / --subject / date filters it lists matching mail directly.
"""
from __future__ import annotations

import argparse
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def _to_ts(date_str: str | None) -> int | None:
    if not date_str:
        return None
    dt = datetime.fromisoformat(date_str).replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


def search(db: Path, query: str | None = None, account: str | None = None,
           after: int | None = None, before: int | None = None,
           from_like: str | None = None, subject_like: str | None = None,
           limit: int = 30) -> list[tuple]:
    conn = sqlite3.connect(str(db))
    cols = "m.date, m.account, m.from_addr, m.subject, m.eml_path"
    where: list[str] = []
    params: list = []
    if query:
        base = (f"SELECT {cols} FROM messages_fts f "
                "JOIN messages m ON m.id = f.rowid")
        where.append("messages_fts MATCH ?")
        params.append(query)
    else:
        base = f"SELECT {cols} FROM messages m"
    if account:
        where.append("m.account = ?"); params.append(account)
    if after is not None:
        where.append("m.ts >= ?"); params.append(after)
    if before is not None:
        where.append("m.ts <= ?"); params.append(before)
    if from_like:
        where.append("m.from_addr LIKE ?"); params.append(f"%{from_like}%")
    if subject_like:
        where.append("m.subject LIKE ?"); params.append(f"%{subject_like}%")
    sql = base + ((" WHERE " + " AND ".join(where)) if where else "")
    sql += " ORDER BY m.ts DESC LIMIT ?"
    params.append(limit)
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def main() -> None:
    ap = argparse.ArgumentParser(description="Search the local mail archive")
    ap.add_argument("query", nargs="?", help="FTS5 query (optional)")
    ap.add_argument("--db", default="mail.db")
    ap.add_argument("--account", help="filter by account name")
    ap.add_argument("--from", dest="from_like", help="sender substring, e.g. bwm.at")
    ap.add_argument("--subject", dest="subject_like", help="subject substring")
    ap.add_argument("--after", help="ISO date lower bound, e.g. 2026-04-01")
    ap.add_argument("--before", help="ISO date upper bound")
    ap.add_argument("--limit", type=int, default=30)
    args = ap.parse_args()

    if not any([args.query, args.from_like, args.subject_like,
                args.after, args.before]):
        ap.error("give a query and/or at least one filter")

    rows = search(
        Path(args.db), args.query, args.account,
        _to_ts(args.after), _to_ts(args.before),
        args.from_like, args.subject_like, args.limit,
    )
    if not rows:
        print("no matches")
        return
    for date, account, frm, subject, path in rows:
        print(f"{(date or '')[:31]:<31} [{account}] "
              f"{(frm or '')[:38]:<38} {subject or ''}")
        print(f"    {path}")
    print(f"\n{len(rows)} hit(s)")


if __name__ == "__main__":
    main()
