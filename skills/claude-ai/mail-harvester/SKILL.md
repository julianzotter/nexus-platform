---
name: mail-harvester
description: >-
  Collect and full-text search e-mail from multiple IMAP accounts (World4You,
  Gmail, and any other IMAP provider) in one local SQLite archive. Use this
  whenever the user wants to fetch, sync, back up, aggregate, archive, or search
  their e-mail across several mailboxes — including phrases like "get all my
  mails", "search my correspondence about X", "pull mails from office@…",
  "find the thread about the Kienberg project", or any request to consolidate
  messages from World4You / Gmail. Also covers ingesting exported WhatsApp / SMS
  chats into the same searchable store. Prefer this over ad-hoc IMAP snippets:
  it does incremental UID-based sync, keeps .eml originals, and exposes an FTS5
  search CLI.
---

# mail-harvester

A small, dependency-light toolkit that pulls every message from one or more
IMAP mailboxes into a local SQLite database with a full-text index, plus the
original `.eml` files. One query path then searches all accounts at once.

## Architecture (why it is reliable)

```
IMAP accounts ──fetch_imap.py──► mail.db (SQLite + FTS5)  +  eml/<account>/<folder>/*.eml
(World4You, Gmail, …)               ▲
WhatsApp/SMS export ─ingest_chat.py─┘            search_mail.py ──► ranked results + .eml paths
```

- **IMAP** is the common protocol for World4You *and* Gmail → one code path.
- **Incremental** sync tracks the highest IMAP `UID` per folder together with
  `UIDVALIDITY`, so re-runs fetch only new mail and are safe to schedule.
- **Standard library only** on Python ≥ 3.11 (no pip install for the core).
- **Secrets** are read from environment variables; the config file holds only
  the *names* of those variables, never passwords.

## Setup (once)

1. Copy the templates and fill them in:
   ```
   cp accounts.example.toml accounts.toml
   cp secrets.env.example secrets.env        # macOS/Linux
   cp secrets.cmd.example secrets.cmd        # Windows
   ```
2. Put real passwords in `secrets.env` / `secrets.cmd`. For World4You use the
   mailbox password; for Gmail use an **App Password** (2FA required). Exact
   server values and the App-Password walkthrough are in
   `references/providers.md`.
3. Python ≥ 3.11 needs nothing else. On 3.10 or older: `pip install tomli`.

`accounts.example.toml` already contains the user's four mailboxes with the
verified World4You / Gmail IMAP hosts.

## Fetch / sync

```bash
# everything (all accounts, all folders) — first run downloads, later runs top up
./run_fetch.sh                 # macOS/Linux   (run_fetch.bat on Windows)

# or call the script directly:
python fetch_imap.py                       # all accounts
python fetch_imap.py --account gmail       # one account
python fetch_imap.py --folders INBOX INBOX.Sent
python fetch_imap.py --list-folders        # discover folder names, fetch nothing
```

Schedule it for hands-off collection:
- **cron** (every 30 min): `*/30 * * * * /path/to/mail-harvester/run_fetch.sh >> sync.log 2>&1`
- **Windows Task Scheduler**: action → start `run_fetch.bat`, "Start in" = this folder.

## Search

```bash
python search_mail.py "Kienberg AND Aufbauten"
python search_mail.py "from_addr:bwm.at" --after 2026-04-01
python search_mail.py "Lodges" --account zotterconsult --limit 10
```

FTS5 query syntax: terms AND-combine by default; `OR` / `NOT`, `"exact phrase"`,
and column filters `subject:`, `from_addr:`, `to_addr:`, `body:`. Results print
date, account, sender, subject and the path to the original `.eml`.

When the user asks a context question ("what did we agree with BWM about the
floor build-up?"), translate it into an FTS query, run `search_mail.py`, then
read the matched `.eml` files (e.g. with the standard `email` module) to answer
from their content.

## Including WhatsApp / SMS

Chat platforms have no personal bulk-pull API, so they are ingested from
exports into the same database. See `references/messaging.md`. Quick path:
```bash
python ingest_chat.py path/to/_chat.txt --name "Daniel Civegna"
```

## Files

| File | Purpose |
|------|---------|
| `fetch_imap.py` | incremental IMAP → SQLite + `.eml` |
| `search_mail.py` | FTS5 search CLI over the archive |
| `ingest_chat.py` | optional WhatsApp `_chat.txt` → same DB |
| `common.py` | config, schema, message parsing |
| `accounts.example.toml` | account list template (pre-filled) |
| `secrets.env.example` / `secrets.cmd.example` | password env templates |
| `run_fetch.sh` / `run_fetch.bat` | scheduler/manual wrappers |
| `references/providers.md` | verified server settings + Gmail App Password |
| `references/messaging.md` | SMS/WhatsApp ingestion paths |

## Notes & limits

- Sent mail is captured too, as long as the Sent folder is synced (default =
  all folders). Restrict scope with `--folders` if a mailbox is huge.
- The archive is append-only; deleting a message on the server does not remove
  it locally (this is desirable for an archive).
- If a folder's `UIDVALIDITY` changes server-side, that folder is re-synced in
  full automatically on the next run.
- Credentials only exist where you configure them. In a sandbox without your
  mailbox access, run `fetch_imap.py` on your own machine (or Claude Code);
  `search_mail.py` then works against the produced `mail.db`.
