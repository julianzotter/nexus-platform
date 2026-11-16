#!/usr/bin/env python3
"""Incremental IMAP sync into the local SQLite archive and .eml files.

For every account in accounts.toml this fetches only messages newer than the
last run (tracked per folder via IMAP UID + UIDVALIDITY), so re-runs are cheap
and idempotent — safe to schedule via cron / Task Scheduler.

    python fetch_imap.py                       # sync all accounts, all folders
    python fetch_imap.py --account gmail       # one account
    python fetch_imap.py --list-folders        # show folder names, fetch nothing
    python fetch_imap.py --folders INBOX INBOX.Sent
"""
from __future__ import annotations

import argparse
import imaplib
import re
from pathlib import Path

from common import Account, load_accounts, open_db, store_message

imaplib._MAXLINE = 10_000_000  # tolerate very large headers / bodies


def connect(acc: Account) -> imaplib.IMAP4_SSL:
    mbox = imaplib.IMAP4_SSL(acc.host, acc.port)
    mbox.login(acc.user, acc.password)
    return mbox


def list_folders(mbox: imaplib.IMAP4_SSL) -> list[str]:
    """Best-effort parse of LIST output into folder names."""
    typ, data = mbox.list()
    names: list[str] = []
    for line in data or []:
        text = line.decode(errors="replace") if isinstance(line, bytes) else str(line)
        match = re.search(r'"([^"]*)"\s*$', text) or re.search(r"(\S+)\s*$", text)
        if match:
            names.append(match.group(1))
    return names


def _quote(folder: str) -> str:
    return '"%s"' % folder.replace('"', '\\"')


def folder_uidvalidity(mbox: imaplib.IMAP4_SSL, folder: str) -> int:
    typ, resp = mbox.status(_quote(folder), "(UIDVALIDITY)")
    match = re.search(rb"UIDVALIDITY (\d+)", resp[0]) if resp and resp[0] else None
    return int(match.group(1)) if match else 0


def new_uids(mbox: imaplib.IMAP4_SSL, last_uid: int) -> list[int]:
    """UIDs strictly greater than last_uid (the `n:*` form always returns the
    highest UID, so the explicit filter is required)."""
    typ, data = mbox.uid("search", None, f"UID {last_uid + 1}:*")
    if typ != "OK" or not data or not data[0]:
        return []
    return sorted(u for u in (int(x) for x in data[0].split()) if u > last_uid)


def fetch_rfc822(mbox: imaplib.IMAP4_SSL, uid: int) -> bytes | None:
    typ, data = mbox.uid("fetch", str(uid), "(RFC822)")
    if typ != "OK" or not data or not isinstance(data[0], tuple):
        return None
    return data[0][1]


def write_eml(archive: Path, account: str, folder: str,
              uidvalidity: int, uid: int, raw: bytes) -> Path:
    safe = re.sub(r"[^A-Za-z0-9._-]", "_", folder) or "ROOT"
    out_dir = archive / account / safe
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{uidvalidity}_{uid}.eml"
    path.write_bytes(raw)
    return path


def sync_folder(conn, mbox, acc: Account, folder: str, archive: Path) -> int:
    typ, _ = mbox.select(_quote(folder), readonly=True)
    if typ != "OK":
        print(f"  ! skip {folder} (not selectable)")
        return 0
    uidvalidity = folder_uidvalidity(mbox, folder)
    row = conn.execute(
        "SELECT uidvalidity, last_uid FROM sync_state WHERE account=? AND folder=?",
        (acc.name, folder),
    ).fetchone()
    last_uid = row[1] if row and row[0] == uidvalidity else 0
    uids = new_uids(mbox, last_uid)
    added = 0
    for uid in uids:
        raw = fetch_rfc822(mbox, uid)
        if raw is None:
            continue
        path = write_eml(archive, acc.name, folder, uidvalidity, uid, raw)
        if store_message(conn, acc.name, folder, uidvalidity, uid, raw, str(path)):
            added += 1
    high = max(uids) if uids else last_uid
    conn.execute(
        """INSERT INTO sync_state(account, folder, uidvalidity, last_uid)
           VALUES (?,?,?,?)
           ON CONFLICT(account, folder) DO UPDATE SET
             uidvalidity = excluded.uidvalidity, last_uid = excluded.last_uid""",
        (acc.name, folder, uidvalidity, high),
    )
    conn.commit()
    print(f"  {folder}: +{added} new (uid<= {high})")
    return added


def sync_account(conn, acc: Account, archive: Path,
                 folders: list[str] | None) -> int:
    mbox = connect(acc)
    try:
        targets = folders or acc.folders or list_folders(mbox)
        return sum(sync_folder(conn, mbox, acc, f, archive) for f in targets)
    finally:
        try:
            mbox.logout()
        except Exception:
            pass


def main() -> None:
    ap = argparse.ArgumentParser(description="Incremental IMAP -> SQLite archive")
    ap.add_argument("--config", default="accounts.toml")
    ap.add_argument("--db", default="mail.db")
    ap.add_argument("--archive", default="eml")
    ap.add_argument("--account", help="restrict to this account name")
    ap.add_argument("--folders", nargs="*", help="restrict to these folders")
    ap.add_argument("--list-folders", action="store_true",
                    help="print folder names for each account and exit")
    args = ap.parse_args()

    conn = open_db(Path(args.db))
    accounts = load_accounts(Path(args.config))
    if args.account:
        accounts = [a for a in accounts if a.name == args.account]
    if not accounts:
        raise SystemExit("no matching accounts in config")

    for acc in accounts:
        print(f"[{acc.name}] {acc.user}")
        if args.list_folders:
            mbox = connect(acc)
            for name in list_folders(mbox):
                print("    ", name)
            mbox.logout()
            continue
        total = sync_account(conn, acc, Path(args.archive), args.folders)
        print(f"  -> total +{total}")
    conn.close()


if __name__ == "__main__":
    main()
