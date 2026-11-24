# NEXUS Role-ID Capability Matrix (NEXUS-ROLES-v1.2)

Generated from `registry/roles/role_capability_matrix.json` - do not edit by hand.
Status ENTWURF - as of 2026-11-25T00:10:00+01:00 - author ID06.
Role authority: Manifest §4 (`governance/current/00_NEXUS_MANIFEST__CURRENT__2026-09-28.md`, Drive `1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn`).

Derived view of Manifest §4 (sole role authority). Roles/functions follow the manifest and are checked by tests; this file adds observed capabilities only. A role label grants no platform rights; a capability is per runtime, session and operation.

| ID | Actor | Function | Status | drive_read | drive_write | github_read | github_write | merge | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| ID01 | Julian Zotter (human) | strategic authority, priorities, final decisions and approvals | ACTIVE | OBSERVED | OBSERVED | OBSERVED | OBSERVED | OBSERVED | owner of WORK files; PR #123 merged as a0d739e (2026-11-24 21:51Z) |
| ID02 | ChatGPT Business | NEXUS AI Knowledge System Engineer and Administrator; equal rank with ID03; assists ID01 | ACTIVE | NOT_TESTED | OBSERVED | NOT_TESTED | NOT_TESTED | NOT_TESTED | WORK raw MD gdrive:1z78MpMDV__ett23O1BlOpCY3HmHi1lrW named ID02 (2026-11-24 20:55); executor not checked; Business runtime untested per ID03 pass |
| ID03 | ChatGPT Private | NEXUS AI Knowledge System Engineer and Administrator; equal rank with ID02; additionally Chief Orchestrator; assists ID01 | ACTIVE | OBSERVED | OBSERVED | OBSERVED | OBSERVED | NOT_TESTED | ID03 pass 2026-11-24 22:38Z: Drive read, GitHub read/write via connector (commits 1b5071b..3372255); WORK raw MD gdrive:1AqhLUApBtkwwuaLBQvfjq2shpe5iyggC; _FRONTMATTER v008 executor OpenAI Codex /root |
| ID04 | Gemini | protocol, evidence, source traceability, decision log, status logging | ACTIVE | NOT_TESTED | NOT_TESTED | NOT_TESTED | NOT_TESTED | NOT_TESTED | historical only (capability matrix v0.1, 2026-10-14) |
| ID05 | Perplexity | targeted external research, primary sources, cross-check, contradiction search | ACTIVE | HUMAN_RELAY | HUMAN_RELAY | NOT_TESTED | NOT_TESTED | NOT_TESTED | historical only (v0.1) |
| ID06 | Claude | responsible coding and implementation; parser/registry, deterministic tools, evaluation, tests, regression loops | ACTIVE | VERIFIED | VERIFIED | VERIFIED | VERIFIED | BLOCKED | 2026-11-24 22:3xZ Opus 5.5: Drive download Manifest 1POfiQ… (sha 09c8786b); Drive write 1d8ikFWZOPEBQUjKYIdvmAbFN_nOGWcmu readback sha 38a1ad5c match; clone a0d739e; push 8326ea0; merge via API denied by session permission policy |
| ID07 | DeepSeek | independent architecture/engineering auditor; never sole author and sole reviewer | ACTIVE | NOT_TESTED | BLOCKED | NOT_TESTED | NOT_TESTED | NOT_TESTED | DSH log pasted by ID01 2026-11-24: pwsh Win32 87 (ACL grant) and write tool EISDIR on G:\Meine Ablage |
| ID08 | Ollama (local) | delegated local/private model execution; optional | OPTIONAL | NOT_TESTED | NOT_TESTED | NOT_TESTED | NOT_TESTED | NOT_TESTED | historical only |
| ID09 | legacy DeepSeek alias | inactive; no new assignment | INACTIVE | NONE | NONE | NONE | NONE | NONE | Manifest §4 |
| ID10 | Meta AI | inactive historical record | INACTIVE | NONE | NONE | NONE | NONE | NONE | Manifest §4 |

Invalid IDs: ID93 (typo for ID03)

## Runtimes without role ID

- OpenAI Codex: coding tickets under ID06 responsibility (Manifest §4) unless the work order names another role; declare executor/provider/model per run
- GitHub Copilot cloud agent / Copilot CLI: role = ordering ID recorded in the task (task URL, PR, full SHA); else UNRESOLVED
- Microsoft 365 Copilot: no role ID; ID01 decision open
- Kimi: no role ID; ID01 decision open

Superseded: governance/ROLE-ID-CAPABILITY-MATRIX-v1.2 hand-written ID03 version (commit 25bb3a3): ID05/ID06/ID07 descriptions contradicted Manifest §4; replaced by this generated view

## Legend

- VERIFIED: operation succeeded in a run whose evidence the author checked
- OBSERVED: artifacts attributed to this role exist; executing run not checked by the author
- NOT_TESTED: no current evidence
- BLOCKED: attempt failed or was denied
- NONE: inactive role (Manifest §4)
- HUMAN_RELAY: only via ID01 copy/upload
