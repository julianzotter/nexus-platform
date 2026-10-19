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

The report also inventories declared GitHub workflow triggers and cron
expressions using a dependency-free reader for common workflow YAML forms; it
is not a complete YAML validator, so unusual syntax must be checked against the
workflow source. This is configuration evidence only: a scheduled trigger does not
prove a successful run, delivery, acknowledgment, or a closed communication
loop. Polling is relevant for observing external changes; push/workflow events
reduce detection latency; scheduled runs provide bounded reconciliation when
notifications are unavailable. The current workflow inventory must be read
alongside Actions run receipts.

The circular communications work is staged separately: PR [#31](https://github.com/julianzotter/nexus-platform/pull/31)
proposes Drive-to-GitHub polling, and PR [#32](https://github.com/julianzotter/nexus-platform/pull/32)
proposes a persistent event ledger with inbox/acknowledgment and verification.
Both remain review candidates, and #32 depends on #31; neither should be treated
as deployed until separately reviewed, merged, and exercised with readback and
recovery evidence. Keep workflow declarations and external UI/backend claims
distinct from observed runtime behavior.

## Relevance to a NEXUS control panel

| Loop | Relevance | Current evidence and boundary |
|---|---|---|
| Polling | High for detecting external Drive/WORK changes and reconciling missed notifications. | Main currently polls repository/PR metadata; PR #31 proposes Drive change polling, but is not merged. |
| Commits and pushes | High as versioned change signals and CI triggers; automatic writes should remain separately gated. | CI and monitor are push/PR-triggered; the delivery workflow reacts to completed main monitor runs. No automatic commit is implied by those triggers. |
| Messages and acknowledgments | High for assigning work and distinguishing delivery from receipt/acceptance. | PR #32 proposes durable event transitions and receiver acknowledgments; it is open and depends on #31. |
| Schedules | High for bounded reconciliation, not real-time guarantees. | The monitor declares an hourly schedule. A cron declaration is not evidence of a successful run. |
| Circular learning loop | High as a governed feedback workflow, not automatic model training. | A closed loop requires source-grounded retrieval, user-confirmed feedback, durable storage, verified readback after restart, and retrieval showing a traceable change. JSONL feedback or changed retrieval weights alone do not establish this. |

The first acceptance exercise should use one authorized real source and prove,
in order: source retrieval -> chat response with source references -> confirmed
feedback -> durable write -> process restart -> readback hash/identity check ->
retrieval showing the feedback-derived change. Preserve each receipt and keep
human acknowledgment separate from transport verification. Passing this exercise
demonstrates a feedback-data loop only; it does not demonstrate model training,
production readiness, or safe autonomous self-modification.

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
