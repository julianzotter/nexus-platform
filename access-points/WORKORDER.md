# WO-20261021-ACCESS-POINTS
Status: IN_PROGRESS | Human Gate: required before merge

## Goal
One canonical searchable registry of NEXUS API/MCP/library access points, linked from an invocable skill.

## Acceptance criteria
- [x] Registry with canonical documentation URLs and classification
- [x] Skill entrypoint and navigation rules
- [ ] Validate URLs and availability against authoritative sources
- [ ] Discover real AEC MCP implementations and classify maturity/security
- [ ] Check connector installation, authorization, and read-only smoke tests
- [ ] Add JSON schema, automated link checks, CI, evidence IDs, SHA-256
- [ ] Link from root manifest/registry and dashboard repo
- [ ] Human review and merge

## Governance
No secrets, no assumed permissions, no irreversible API calls. Differentiate catalogued / reachable / authenticated / tested. Log verification timestamp and source. Sync to dashboard only after review.
