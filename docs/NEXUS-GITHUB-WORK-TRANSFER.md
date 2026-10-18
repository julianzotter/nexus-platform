# GitHub -> WORK delivery contract

State: REVIEW / NOT_MERGED. A validated transport receipt is not human acceptance.

## Implemented

- Existing PR26 preserves an hourly `:17 UTC` monitor during stabilization. No monitor PR trigger is invented; it retains push/main and manual entry.
- `nexus-delivery.yml` listens only to completed NEXUS Monitor runs on main (including failed runs with artifacts). It checks out trusted main, never an untrusted PR head. GitHub credentials are contents:read/actions:read, not write.
- `deliver_work.py` verifies the source repository, workflow name, completed state, branch and 40-character commit. It paginates artifact metadata and verifies the actual ZIP against the GitHub SHA-256 digest. ZIP content is never executed.
- Immutable delivery key: repository + source run ID + run attempt + artifact ID. Drive uses an appProperties lookup, not only a filename. Multiple records are a conflict.
- Generate and journal a Drive ID before upload. Retried creates use the same ID; HTTP409 is not success until parent/key/raw media verification passes.
- Bounded retries (three attempts, backoff) for transient Drive transport and GitHub CLI failures. No raw OAuth/service error response is logged.
- Every success verifies SHA-256 of downloaded Drive bytes. Stable receipt metadata is also uploaded and byte-verified. Delivery never changes consumer_ack=NOT_OBSERVED or human_acceptance=PENDING to a fabricated approval.
- Always preserve status, receipts and ID journals as a GitHub artifact. Resume a failed workflow attempt with **Re-run jobs**; an explicit dispatch for an earlier source run can additionally specify `resume_delivery_run_id` to restore the earlier delivery journal. This avoids generating replacement IDs after an ambiguous upload.

## Authentication and activation

The connected ChatGPT Drive account does not export its OAuth credentials into GitHub Actions. There is no credential-free cloud writer.

Runner auth supports an already supplied short-lived `GOOGLE_ACCESS_TOKEN`, or user OAuth refresh with repository secrets `NEXUS_GOOGLE_CLIENT_ID`, `NEXUS_GOOGLE_CLIENT_SECRET`, `NEXUS_GOOGLE_REFRESH_TOKEN`. Do not paste secret values in WORK, issues or chat. Use a dedicated authorized account/app and only the required Drive scope and destination access. The runner needs OAuth authorization that actually grants access to the existing WORK folder; a generic drive.file token does not automatically grant access to arbitrary preexisting files. The code does not create a key, change sharing or authenticate a human approver.

Secrets inventory could not be read through this connector (endpoint not allowed). The current local process has no Google access token. Therefore an authenticated runner transfer remains **BLOCKED / NOT_EXECUTED** until credentials are configured and a real delivery workflow succeeds after a separate merge. A missing credential generates an explicit BLOCKED report and nonzero exit.

For a local authorized adapter, run `python tools/deliver_work.py --run-id <completed-main-monitor-run>` with a supported credential in the environment. Its default output is `reports/delivery/`. Keep its state directory across retries. OAuth access is needed only by this delivery adapter; root unit tests use isolated fake clients and do not access Drive.

## Retry and concurrency limits

The workflow serializes its writer with one concurrency group. Other runtimes must not concurrently write the same delivery key; Drive filenames/appProperties are not a transactional unique constraint. Journal recovery is necessary after an ambiguous create and loss of local state. GitHub pending concurrency jobs can be superseded, so periodic reconciliation/backfill is also necessary: the existing hourly NEXUS status task is instructed to find missed monitor packages and repeat unresolved deliveries. A schedule alone does not prove this reconciliation ran successfully. For long outages, backfill explicit source run IDs before their 30-day artifacts expire.

A connector-mediated live delivery is a distinct execution path from Actions OAuth. Its receipt must identify that path; successful connector access does not prove runner access. Reports must not claim global bidirectional synchronization.

## LLM analysis

The existing hourly NEXUS status agent performs LLM-based interpretation of deterministic findings. It cannot override hashes, schema checks, transport verification or human gates. A Python API-backed LLM call is not silently installed: provider/credential selection is still unresolved. No OpenAI key was found locally; no new key, model API charge or plaintext credential was created. Provider configuration and a real inference receipt are required before claiming Python LLM invocation.

## Branch protection

Observed main: protected=false; required checks off. Rulesets API returned403: "Upgrade to GitHub Pro or make this repository public to enable this feature." The repository was not made public and no subscription was changed. The adjacent JSON is a review proposal, not applied protection. Confirm an eligible plan and independent reviewer identity before activation: all agents using the same human GitHub account cannot provide independent authenticated approval.

## Acceptance checklist

- [ ] PR26 reviewed and separately merged.
- [ ] OAuth account and WORK scope configured through secure settings.
- [ ] Actual Actions run -> source ZIP digest -> Drive raw-byte match -> receipt raw-byte match.
- [ ] Rerun reuses the same package ID; no duplicate.
- [ ] Simulated transport error and recovered persisted journal tested; an actual cloud failure drill remains separate.
- [ ] Consumer actually acknowledges the package; receipt alone is not this ACK.
- [ ] ID01 explicitly accepts the final version; no LLM self-approval.

Official references: https://developers.google.com/workspace/drive/api/guides/manage-uploads ; https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_run
