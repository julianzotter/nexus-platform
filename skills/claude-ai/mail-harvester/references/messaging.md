# SMS & WhatsApp — scope and ingestion paths

E-mail is the reliable, fully automatable core (IMAP). SMS and WhatsApp have
**no official personal bulk-pull API**, so they are handled as periodic
*exports* that feed the same SQLite store, keeping search unified.

## WhatsApp

There is no API to retroactively download your personal chats. Two routes:

1. **Per-chat export (supported, works today).** On the phone: open a chat ->
   ⋮ / contact name -> Export chat -> "Without media". You get `_chat.txt`.
   Ingest it so it becomes searchable next to mail:
   ```
   python ingest_chat.py path/to/_chat.txt --name "Daniel Civegna"
   ```
   `ingest_chat.py` parses the common AT/DE iOS and Android timestamp formats.
   Repeat per chat; re-exporting later and re-ingesting picks up new lines.

2. **WhatsApp Business Cloud API** (Meta). Only for a *business* phone number,
   webhook-based, and only captures messages from the moment it is connected —
   it cannot fetch history. Not suitable for archiving an existing personal
   account.

## SMS

Device-dependent; export, then ingest:

- **Android:** the app "SMS Backup & Restore" exports an XML file. Or, with USB
  debugging, `adb` can pull the SMS database. Either can be transformed into the
  same row shape as `ingest_chat.py` (account = `sms:<number>`, ts, sender, body).
- **iPhone:** SMS/iMessage live in `sms.db` inside an *encrypted* local
  Finder/iTunes backup; tools exist to read it. Export to CSV/text, then ingest.

## Why keep them separate from the IMAP core

The IMAP path is deterministic and idempotent — schedule it and forget it.
Chat exports require a manual step on the device, so they are intentionally a
separate, occasional ingestion rather than something the scheduler runs. Both
land in the same `messages` table, so `search_mail.py` queries everything at
once (filter chat-only with `--account whatsapp:<name>` or `sms:<number>`).
