# Run evidence contract
Create a unique timestamp/random run ID. Preserve runtime_capability_manifest.json,
model_state_before.json, model_state_after.json for writes, object_inventory.csv,
bounded result exports, tool_calls.jsonl, observations.jsonl, status.json and
SHA256SUMS.txt. Log schemas/versions, model identity, units, combinations,
source hashes, outcome and redacted evidence pointers. Never store secrets.
Create a NEW run folder; verify saved bytes and hashes. Checksums exclude the
checksum manifest itself. Source file hash, model fingerprint and result hash
are distinct. A payload hash does not prove RFEM produced it: bind the payload
to authenticated tool response and exact calculation state. Hashes do not
make storage immutable. Preserve evidence in versioned approved storage.
Maintain chronological log separately from current status. Final release stays
HUMAN_SIGNOFF_REQUIRED.
