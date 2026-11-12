# nexus-counter (review snapshot, status ENTWURF)

Single-writer counter for NEXUS artifact numbers (ID01 decision 2026-11-10: counter system).

`nexus_counter.py` finds files in WORK whose names end in `_LEDGER-PENDING` or
`_UNREGISTERED`, assigns the next free number (highest of ledger and already numbered
file names, plus one; oldest file first), appends one row to the ledger CSV and one line
to the history log, and renames the file. Dry run by default; `--apply` acts.
It deletes and moves nothing. A lock file rejects a second concurrent run.

Agents do not allocate numbers themselves.

Tested: `tests/test_nexus_counter.py` on synthetic files.
Not tested: Windows, the Google Drive mount, the real ledger. No `file-registry.jsonl` entry yet.
