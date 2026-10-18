# NEXUS Monitor — scoped repository checks

The monitor runs on pushes to main, manually, and hourly at minute 17 UTC.
GitHub schedules can be delayed; this is not a hard real-time watchdog.
It reads PR metadata only, never checks out or executes PR-head code, never
merges, and uses read-only contents and pull-request permissions.
The normal CI remains a separate pull_request/push workflow.

## Evidence and states

`tools/monitor_repo.py` executes both validators even if one fails, retrieves
all open-PR pages, retries unknown mergeability up to three times, and writes
`reports/monitor/report.json` and `report.md`. Reports include commit, run ID,
attempt and UTC observation time. The artifact upload runs even if monitoring
fails, with a unique run/attempt name and 30-day retention.

| State | Meaning |
|---|---|
| PASS | The particular check passed; this is not engineering approval. |
| NO_DATA | No knowledge JSON items exist; no knowledge was evaluated. |
| INCOMPLETE | Coverage is unmeasured or knowledge data is absent. |
| CONFLICT | GitHub reports a non-mergeable PR. |
| UNKNOWN | GitHub has not supplied mergeability after bounded retries. |
| ERROR / FAIL | Retrieval or validation failed. |
| ATTENTION | Overall state when a conflict, unknown, error or failure occurs. |

ATTENTION exits 1 after reports are written. INCOMPLETE exits 0 but is explicitly
reported as incomplete in both JSON and the Actions summary. Green execution
does not certify complete data. CI uses `validate_knowledge.py --allow-empty`
explicitly while the inventory is not populated; it prints NO_DATA. Without
that option, an empty or absent knowledge directory exits 2. Remove the
exception when actual knowledge records are required by the project gate.

## Boundaries

No Drive transport, notifications, issue creation, installation on Julian's
Windows workstation, authenticated human sign-off, or production release is
implemented by this repair. Reports remain Actions artifacts unless a separately
tested adapter transfers them. Existing Drive WORK is still the document source
of truth. Automatic scheduling activates only after the workflow reaches main.
No branch protection or sharing setting is changed.

Actions use Node-24-compatible v6 releases; Ubuntu is explicitly 24.04 and
Python remains 3.12. Major action tags and runner images still receive updates;
this is not a fully immutable dependency lock.
