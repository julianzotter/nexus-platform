---
name: aec-connectivity-audit
description: Inspect RFEM MCP/gRPC, Colab/local runtime, Drive, GitHub, CI and artifact-delivery connections for AEC workflows. Use for diagnostics, status dashboards, synchronization claims, delivery receipts and missing acknowledgments. Distinguish configured, reachable, authenticated, executed and acknowledged states.
---
# AEC Connectivity Audit

## Contract
Input: named directed edges, runtime locations, exact source/destination IDs,
operation scope and connector schemas.
Output: edge evidence with timestamp, limitations, blockers and next action;
separate status report and chronological log.

## Execute
1. Read current governance and relevant original work orders. Discover actual
   tools before claiming connection. Do not infer account identity from labels.
2. Distinguish Windows RFEM host, Colab VM, ChatGPT environment and Actions
   runner. Their 127.0.0.1 addresses do not identify the same machine.
3. Record actual evidence independently: configuration, transport response,
   authenticated identity, successful intended operation, full byte readback,
   consumer ACK and explicit human acceptance. Missing evidence is UNKNOWN or
   NOT_RUN. Tool presence proves availability, not successful execution.
4. Run authorized reads first. Do not create test files/change access merely to
   measure capability unless that write is in scope. Use exact known source IDs.
5. For authorized delivery preserve source/destination revision, raw-byte hash,
   run/attempt and connector/runner path. Verify complete readback. Normalized
   text hashes are not raw-byte equality. Apply [connectivity-contract.md](references/connectivity-contract.md).
6. Do not infer ACK from delivery, bidirectional sync from one transfer, schedule
   success from enabled state, or runner OAuth from a connector read.
7. Use [create_audit_bundle.py](scripts/create_audit_bundle.py) to package reviewed
   non-secret evidence in a new run directory. It creates status/log/hashes.
   Hashes detect changes; they do not prove authenticity or enforce immutability.
   Preserve the run in the approved versioned destination.
8. Re-read saved artifacts and verify hashes. Report actual status, dependencies
   and next action. Reconcile uncertain creates before retrying. Never overwrite
   shared state or fabricate CAS/lease guarantees.

## Boundaries
Do not configure OAuth, open ports, install bridges, change permissions,
schedule jobs or send messages without task authorization. Missing RFEM runtime
blocks that edge, not independent offline work.
