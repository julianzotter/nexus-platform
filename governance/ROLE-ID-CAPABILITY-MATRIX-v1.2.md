# NEXUS ROLE-ID-CAPABILITY-MATRIX v1.2
date: 2026-11-24
authority: ID01; Manifest §4 NEXUS-ROLES-v1.2
status: IMPLEMENTED_POLICY / CONNECTOR_ACCESS_PARTIALLY_VERIFIED
canonical_manifest: governance/current/00_NEXUS_MANIFEST__CURRENT__2026-09-28.md
principle: ROLE != RUNTIME != TOOL_ACCESS != PROOF_OF_EXECUTION

| Role | Actor | Governance / duty | Google Drive | GitHub | Mail / Calendar | Approval | Verification |
|---|---|---|---|---|---|---|---|
| ID01 | Julian Zotter (human) | Strategy, ultimate decision and sign-off | Human-controlled | Human-controlled | Human-controlled | FINAL | ID01 explicit chat decision 2026-11-24 |
| ID02 | ChatGPT Business | Equal AI Knowledge System Engineer + Administrator, assists ID01 | PER-SESSION / TEST REQUIRED | PER-SESSION / TEST REQUIRED | PER-SESSION / TEST REQUIRED | No final ID01 sign-off | Role policy confirmed; separate Business runtime untested in this run |
| ID03 | ChatGPT Private | Equal AI Knowledge System Engineer + Administrator, Chief Orchestrator, assists ID01 | READ verified this session; native Docs WRITE verified in prior run; raw MD WRITE NOT VERIFIED | READ/WRITE verified via GitHub connector this session | Not tested in this run | No final ID01 sign-off | Connector tests in this chat; not transferable to all runtimes |
| ID04 | Gemini | Evidence/protocol per historical register | NOT TESTED | NOT TESTED | NOT TESTED | None | Historical description only |
| ID05 | Other registered LLM | See Manifest §4 | NOT TESTED | NOT TESTED | NOT TESTED | None | No current capability assertion |
| ID06 | Claude / delegated peer review and ledger in historical docs | Delegated tasks subject to manifest | NOT TESTED | NOT TESTED | NOT TESTED | None | No current capability assertion |
| ID07-ID08 | Other registered agents | See Manifest §4 | NOT TESTED | NOT TESTED | NOT TESTED | None | No current capability assertion |
| ID93 | INVALID TYPO | Alias error for ID03, not a role | N/A | N/A | N/A | None | ID01 correction |

## Access points and evidence (this run)
- Google Drive connector: search and fetch successful; WORK folder ID 1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP, LLM-LOCAL-SSOT folder ID 1j3FLJkWpQv6xGA_KO0D9sMyA11f0vxBV.
- GitHub connector: fetch/search/update_file successful; repository julianzotter/nexus-platform.
- ChatGPT Automations: 15 task definitions inspected; 6 enabled and 9 disabled as of inspection. Scheduled execution != verified delivery.
- GitHub PRs: #125 and #126 open at inspection; #123 merged (commit a0d739e698265b9c1a334bf1e675c7fa62d65a92).
- GitHub Actions: CI YAML exists at .github/workflows/ci.yml. Live workflow conclusion not verified in this run.
- MCP tool access is connection-, permission-, account- and session-specific; never extrapolate from ID03 to ID02.
- External assistants' START_ACK, actual model identity, receipt/delivery, and independent review are NOT TESTED unless directly evidenced.

## Priority / conflict resolution
1. Manifest §4 v1.2 is the sole CURRENT role register. Old v1.0/v1.1 mapping is historical.
2. ID02 and ID03 equal administrative rank; ID03 additionally coordinates as Chief Orchestrator.
3. ID01 authorizes low-risk governance consistency edits; critical release/engineering sign-off remains ID01-only.
4. Google Drive raw Markdown is declared canonical SSOT; GitHub is a versioned mirror. Do not claim byte-identical sync without readback + hashes.
5. Frontmatter v008 in Drive is ENTWURF; GitHub roles-v1.1/_FRONTMATTER.md is historical. Never treat the old path as CURRENT.
6. Each agent START_ACK must declare role_id, actual runtime, provider model ID (null if unknown), verified connector access, timestamp, and workorder.
7. Scheduled tasks, GitHub Actions, PR status and user notification delivery are separate evidence domains.

## Verification checklist
- [x] ID01 role decision recorded in canonical GitHub Manifest §4.
- [x] Baseline MUST-90 updated in GitHub; prior mapping labeled historical.
- [ ] Google Drive canonical raw MD and GitHub byte-identical / SHA-256 readback.
- [ ] Native Drive and GitHub frontmatter alignment and release state.
- [ ] CI workflow run conclusion and PR checks independently fetched.
- [ ] Delivery receipts / START_ACK for external agents.
- [ ] Independent peer review (optional for this ID01-directed governance correction, not falsely claimed).

## Three-expert synthesis (three evidence passes, not three independent model executions)
- Governance architect: one role register, explicit precedence, historical mappings quarantined.
- Platform integration engineer: capabilities evidenced per runtime/tool, no blanket access assumption.
- Operations reviewer: CI, schedules, PRs, WORK and delivery require distinct status proofs.
Consensus: approve role policy; classify operational rollout as PARTIAL until source synchronization and runtime evidence.
