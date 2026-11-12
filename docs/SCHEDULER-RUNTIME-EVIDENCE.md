# Scheduler runtime evidence — Issue 73

Status: DRAFT; ID02 / ChatGPT Private; no production acceptance.

The monitor previously inventoried YAML triggers without checking execution. It now
adds `scheduler_runtime` to the existing JSON and Markdown report. The collector uses
six bounded read requests: workflow identity/state and the first 100 matching main
branch runs for Monitor, Drive poller and WORK delivery. API failures fail closed in
this evidence section. No credentials or arbitrary API errors are copied to reports.

Metadata PASS requires an active workflow, three distinct recent successful initial
trigger runs, valid run/commit identities, no overdue active run and no observed gap
above the declared interval plus 30 minutes. The intervals are 60, 30 and 60 minutes
respectively; delivery is event-driven and its 60-minute observation target follows
the monitor. The tolerance is an explicit observation policy, not an exact-time SLA.
Manual dispatches and successful reruns do not establish initial schedule success.

## Avoid a self-blocking health check

Historical runtime health does not alter the repository validation exit code.
Otherwise three prior successful monitor jobs could become impossible after the
monitor itself failed on this historical condition. `status` continues to describe
repository checks; `scheduler_runtime.status` separately describes run metadata.
No consumer may treat either field as full scheduler acceptance.
`scheduler_runtime.end_to_end` always remains `UNVERIFIED`: this collector does not
download inner operational evidence, match delivery receipts to upstream run IDs,
verify raw-byte hashes, verify consumer ACKs or authorize engineering acceptance.
The existing dashboard schema/projection is unchanged; detailed runtime evidence
is in the existing monitor artifacts. No competing dashboard is introduced.

## Deterministic verification

Run `python -m unittest discover -s tests -v` in a complete checkout, or explicitly
the scheduler-runtime, monitor and operational-evidence test modules. The local
development environment held only those three test modules: its result is scoped
and is not the complete repository test result. Tests mock all GitHub access.
The existing CI remains responsible for the full checkout and pytest suite.

## Remaining acceptance gates

1. Review the draft and obtain ID01 merge/release approval; run CI at the exact head.
2. Restore runner Google OAuth using the existing recovery procedure; connector
   access in ChatGPT is not evidence that GitHub runner credentials work.
3. Observe three actual schedule runs after activation. Read each inner report;
   green wrapper status alone is insufficient. Preserve run IDs and timestamps.
4. Confirm durable change-feed checkpoint, controlled change, exact WORK destination,
   matching source run, raw-byte readback/hash and idempotent retry.
5. Prove conflict-safe registry append and real consumer ACK; independent review
   and human acceptance remain separate. Do not allocate a ledger number as ID02.

The Drive poller observes change-feed metadata. It is not a WORK-file backup into Git.
The source DOCX includes alternative proposals (including daily polling and cleanup);
they do not authorize silently deleting jobs or overriding Issue 73's hourly/daily scope.

Sources: [Issue 73](https://github.com/julianzotter/nexus-platform/issues/73),
[source DOCX](https://drive.google.com/file/d/1XARPAlYDwtGIUjx1n6VgLzV8FaBDZ7tH/view),
`docs/NEXUS-SCHEDULER-RECOVERY.md`, and current AGB v006 / role Manifest v1.1.
