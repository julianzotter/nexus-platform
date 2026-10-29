# NEXUS scheduler recovery

Recovery candidate based on `805d7ddc2f2933892050b043cd8ff6765b126737`, inspected
2026-10-29. Drive remains document SSOT. This runbook is not a production release.

## Observed failures

| Layer | Evidence | Observed state |
| --- | --- | --- |
| Scheduled monitor | [run 40890442204](https://github.com/julianzotter/nexus-platform/actions/runs/40890442204), created 14:20:12Z | Outer success; log says `NEXUS monitor: INCOMPLETE` |
| Drive change feed | [run 40901998215](https://github.com/julianzotter/nexus-platform/actions/runs/40901998215), created 15:28:55Z; current `drive_changes_poll.py` | Outer success; missing-credential exception deliberately exits zero |
| WORK delivery | [job 123505634157](https://github.com/julianzotter/nexus-platform/actions/runs/40890492066/job/123505634157) | Preflight exits 2: all three NEXUS Google secret variables empty; transfer skipped |
| Schedule liveness | Latest 12 repository runs inspected on 2026-10-29 | No newer monitor/poller runs returned; why scheduled slots are missing is UNKNOWN |
| Knowledge coverage | `registry/coverage-per-source.json` at the base commit | `INCOMPLETE`, unmeasured sources; cannot be repaired by changing a status label |

Times above are UTC; Vienna is UTC+1 on this date. A successful manual run does
not establish schedule recovery. Workflow activation, actor eligibility and
Actions account limits were not readable through the available connector.
The browser has no authenticated GitHub session; no setting was changed.

## Implemented repair and validation

- Polling returns exit 2 for missing credentials, retaining the BLOCKED report
  and previous checkpoint. Other `DeliveryError` failures still return 2.
- Monitoring returns PASS=0, ATTENTION=1, INCOMPLETE=2 after saving evidence.
  Existing `always()` export/upload steps preserve reports on failure.
- Delivery accepts completed monitor runs independently of their conclusion;
  failure evidence remains deliverable. Delivery does not mean content approval.
- Regression: both new failure cases reproduced against the base code; after
  repair 22 targeted tests pass with
  `python -m unittest discover -s tests -v` in the scoped local checkout.
  Full repository CI and native recovery are NOT_RUN locally.
- Native first PR CI [40928508121](https://github.com/julianzotter/nexus-platform/actions/runs/40928508121)
  exposed a pre-existing `ModuleNotFoundError: pytest` in the ACB tests. CI now
  installs pytest and uses it to collect both unittest classes and pytest
  functions; merely installing the package while retaining unittest discovery
  would leave the ACB function tests unexecuted.
- Existing cron expressions remain monitor `17 * * * *` and poller
  `7,37 * * * *`, UTC. No source inventories or coverage results were invented.

## Restore the actual execution path

Use an authenticated owner session. These are continuation commands, not a
record of executed mutations. Review and integrate this candidate according to
the repository gate before claiming its exit-code behavior is live.

1. Inspect workflow enablement, current run/queue state and account limits:

   ```sh
   gh workflow list --all --repo julianzotter/nexus-platform
   gh run list --repo julianzotter/nexus-platform --limit 30
   ```

   Re-enable only workflows confirmed disabled and intended for restoration:

   ```sh
   gh workflow enable nexus-monitor.yml --repo julianzotter/nexus-platform
   gh workflow enable nexus-drive-poll.yml --repo julianzotter/nexus-platform
   gh workflow enable nexus-delivery.yml --repo julianzotter/nexus-platform
   ```

   If workflows are already active, enablement alone is not a diagnosis or
   recovery proof. Inspect account restrictions and the schedule actor. Do not
   buy a plan or change billing/security rules as an unreviewed workaround.

2. Restore Google runner credentials through the existing local OAuth setup in
   [NEXUS-RUNNER-ACTIVATION.md](NEXUS-RUNNER-ACTIVATION.md). Required secret names:
   `NEXUS_GOOGLE_CLIENT_ID`, `NEXUS_GOOGLE_CLIENT_SECRET`,
   `NEXUS_GOOGLE_REFRESH_TOKEN`. A ChatGPT Drive connection is separate from
   the Actions runner credentials. Never paste secret values into chat or WORK.
   Use a previously authorized private OAuth file, or complete local Google
   consent if no valid credential set exists. Verify refresh and exact WORK
   capability with the existing read-only preflight. A prior consent or a secret
   name alone does not prove current access.

3. After preflight succeeds, start one controlled probe per workflow:

   ```sh
   gh workflow run nexus-drive-poll.yml --ref main --repo julianzotter/nexus-platform
   gh workflow run nexus-monitor.yml --ref main --repo julianzotter/nexus-platform
   ```

   Monitor completion already triggers `nexus-delivery.yml`; do not dispatch a
   duplicate delivery blindly. If resuming an interrupted delivery, preserve
   its journal with `resume_delivery_run_id` or rerun that delivery attempt.
   Inspect actual run IDs and artifacts before retrying a timeout.

## Acceptance evidence

Record native evidence separately for each gate; all remain pending until read:

| Gate | Required evidence |
| --- | --- |
| Schedule restored | Three consecutive actual schedule-triggered monitor runs and three consecutive poller slots; record UTC times, event type, source SHA, gaps and actual inner status. A dispatch does not count. |
| Polling functional | Successful token refresh plus INITIALIZED then a subsequent OK change-feed cycle. INITIALIZED alone is not a transfer receipt. A controlled authorized WORK change must appear in `changes.json` to prove the feed. |
| Monitoring complete | Inner PASS on the inspected revision, supported by measured source inventories/coverage. Existing INCOMPLETE must remain visible until its causes are resolved. |
| Delivery functional | Native `DELIVERY_VERIFIED`, exact WORK destination, source-run/artifact binding, raw-byte hash readback and same-ID retry evidence. |
| Human acceptance | Actual consumer/device ACK and Julian's final release decision; neither is implied by job success or receipt creation. |

Schedules are not an exact-time SLA. GitHub documents that scheduled events may
be delayed or dropped. Missing runs alone do not identify the cause. If an
enabled workflow's actor is ineligible, follow GitHub's documented recovery
after verifying that condition; no actor problem was established in this audit.

## Sources and boundaries

- [WORK Folder.md, pilot policy 0.4.0](https://drive.google.com/file/d/11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH/view)
- [Leading AGB v003](https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view)
- Repository `AGENTS.md`, workflow files, polling/monitoring/delivery code and
  linked native run logs at the inspected base revision.
- [GitHub: scheduled-workflow troubleshooting](https://docs.github.com/en/actions/how-tos/troubleshoot-workflows)
- [GitHub: disabling/enabling workflows](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows)
- [GitHub: manual workflow dispatch](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)

No GitHub setting, secret, cron, sharing permission, engineering solver,
ChatGPT automation, email or production release was changed by this candidate.
