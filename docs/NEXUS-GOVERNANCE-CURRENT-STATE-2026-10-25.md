# NEXUS Governance and Lifecycle Status — correction candidate (2026-10-25)

Status: REVIEW / NOT_APPROVED / NO_PRODUCTION_RELEASE
GitHub baseline: 05f5194ac8013b49f681fa00bb9f0e5abdae75e5
Document SSOT: https://drive.google.com/drive/folders/1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP
Source: WORK/Folder.md; AGENTS.md; docs/adr/0001-evidence-and-gates.md; current Drive CPLM v0.109.0 and rollout v1.70.0.

## Evidence vocabulary (proposal; not a production policy update)

- REPORTED: statement or document claim, not independently proven.
- HASH_MATCH: deterministic byte-integrity result; NOT human or engineering verification.
- E2E_VERIFIED: named end-to-end path, successful live execution, target readback and matching digest; cannot be inferred from a separate connector delivery.
- REVIEW_PASSED: independent scoped review tied to immutable commit/file version and test evidence; not human release.
- HUMAN_ACCEPTED: authenticated receiving/human acceptance with explicit subject and scope.
- RELEASED: explicit authorized ID01 decision after the required separate review perspectives, with recorded evidence. No LLM self-approval.
- UNKNOWN/INCOMPLETE/BLOCKED: fail closed. Green CI or an enabled schedule alone is insufficient.
- Unqualified VERIFIED is ambiguous; use an explicit scoped status until ID01 approves a canonical schema.

## Current-state boundaries

- GitHub main observed at 05f5194ac8013b49f681fa00bb9f0e5abdae75e5; branch protection reported disabled.
- Native GitHub-to-WORK delivery remains BLOCKED_DRIVE_CREDENTIALS; a connector ZIP byte-match is only DELIVERY_VERIFIED_CONNECTOR_ONLY.
- Monitor coverage/skill inventory remains INCOMPLETE; Drive-to-GitHub poll is functionally blocked despite green workflow runs.
- WORK and at least one directly checked ZIP retain anyone:writer; remediation needs a distinct authorized permissions decision.
- No authenticated consumer ACK or ID01 production release was demonstrated.

## Required acceptance / next actions

1. ID01/security owner: authorize and independently verify ACL remediation and credential scope; do not publish secrets.
2. CI/workflow owner: commit-bound negative tests for BLOCKED/INCOMPLETE and genuine native E2E delivery with journal, target ID, SHA-256 readback and poll page token.
3. Three independent reviewer perspectives, re-review after fixes, authenticated consumer ACK and explicit ID01 release. Prior history is not the current receipt.

This is a review snapshot only; it does not supersede WORK Folder.md or amend any ACL, credentials, workflows, merges or production permissions.
