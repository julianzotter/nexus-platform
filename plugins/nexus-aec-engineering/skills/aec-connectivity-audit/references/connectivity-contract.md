# Connectivity contract
For each directed edge record source runtime, destination/resource ID, operation,
observed_at, evidence locator/hash, status and limitations. Record independently:
CONFIGURED, REACHABLE, AUTHENTICATED, OPERATION_PASS, READBACK_PASS,
ACK_OBSERVED, HUMAN_ACCEPTED, UNKNOWN, NOT_RUN, BLOCKED, FAIL.
Do not promote one evidence dimension automatically to the next.
For Drive→GitHub distinguish curated commits from change-feed artifacts. For
GitHub→Drive verify run/attempt/artifact IDs, ZIP digest, uploaded bytes and
receipt bytes. Local mount presence is not cloud sync proof. Reuse the existing
repository delivery contract; do not create another synchronization master.
Document authorization, retries, duplicate reconciliation and CAS/lease limitations.
Normalized text hashes are not raw-byte equality. Use Vienna local time for
reports and a verified registry identity; otherwise state UNRESOLVED.
Read current AGENTS.md/WORK Folder.md each run. Historic audit status is not
current proof. Maintain separate chronological log and current status.
