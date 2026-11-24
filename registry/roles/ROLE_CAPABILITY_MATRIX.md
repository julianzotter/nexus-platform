# NEXUS Role-ID Capability Matrix (NEXUS-ROLES-v1.2)

Generated from `registry/roles/role_capability_matrix.json` - do not edit by hand.
Status ENTWURF - as of 2026-11-24T23:55:00+01:00 - author ID06.
Role authority: Manifest §4 (Drive `1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn`, sha256 `09c8786b9064c1e5`).

Derived projection of Manifest §4. Not a second register: role names/functions follow the manifest; this file only adds observed capabilities with evidence. Role label grants no platform rights.

| ID | Actor | Function | Status | drive_read | drive_write | github_read | github_write | merge | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| ID01 | Julian Zotter (human) | strategic authority, priorities, final decisions and approvals | ACTIVE | VERIFIED | VERIFIED | VERIFIED | VERIFIED | VERIFIED | all PR merges on main, e.g. PR #123 merged 2026-11-24T21:51Z |
| ID02 | ChatGPT Business | NEXUS AI Knowledge System Engineer and Administrator; equal rank with ID03; assists ID01 | ACTIVE | OBSERVED | OBSERVED | OBSERVED | OBSERVED | NONE | raw MD in WORK gdrive:1z78MpMDV__ett23O1BlOpCY3HmHi1lrW (2026-11-24 20:55); PR #119 merged; commits under account julianzotter |
| ID03 | ChatGPT Private | NEXUS AI Knowledge System Engineer and Administrator; equal rank with ID02; Chief Orchestrator; assists ID01 | ACTIVE | OBSERVED | OBSERVED | OBSERVED | OBSERVED | NONE | _FRONTMATTER v008 agent_id ID03 gdrive:1rKnQMZbhO6ii0ThnJLhUCRYrXFcDvRbi; branches id03/* (PR #125, #126) |
| ID04 | Gemini | protocol, evidence, source traceability, decision log, status logging | ACTIVE | NOT_TESTED | NOT_TESTED | NOT_TESTED | NOT_TESTED | NONE | historical only: LLM-CAPABILITY-MATRIX v0.1 (2026-10-14) Colab direct write |
| ID05 | Perplexity | targeted external research, primary sources, cross-check | ACTIVE | HUMAN_RELAY | HUMAN_RELAY | NOT_TESTED | NONE | NONE | historical only: v0.1 matrix |
| ID06 | Claude | responsible coding and implementation; parser/registry, deterministic tools, tests, regression loops | ACTIVE | VERIFIED | VERIFIED | VERIFIED | VERIFIED | BLOCKED | 2026-11-24: Drive write gdrive:1pix0uyGPu_DzhpwuYf6xfPh_0O0JzhCh; branch push id06/role-capability-matrix; PR merge via API denied by session permission policy |
| ID07 | DeepSeek | independent architecture/engineering auditor; never sole author and sole reviewer | ACTIVE | OBSERVED | BLOCKED | OBSERVED | NONE | NONE | DSH log pasted by ID01 2026-11-24: pwsh SetNamedSecurityInfoW Win32 87 and write tool EISDIR on G:\Meine Ablage |
| ID08 | Ollama (local) | delegated local/private model execution | OPTIONAL | NOT_TESTED | NOT_TESTED | NONE | NONE | NONE | historical only |
| ID09 | legacy DeepSeek alias | inactive | INACTIVE | NONE | NONE | NONE | NONE | NONE | Manifest §4 |
| ID10 | Meta AI | inactive historical record | INACTIVE | NONE | NONE | NONE | NONE | NONE | Manifest §4 |

Invalid IDs: ID93 (typo for ID03)

## Runtimes without role ID

- OpenAI Codex: declare executor per run; role = the ordering ID
- GitHub Copilot cloud agent / Copilot CLI: runs under the ordering ID (currently ID03); record task URL, PR, full SHA
- Microsoft 365 Copilot: no role id; ID01 decision open
- Kimi: no role id; ID01 decision open

## Legend

- VERIFIED: operation succeeded in a run with evidence
- OBSERVED: artifacts of this actor exist; the executing run was not checked by the author
- NOT_TESTED: no current evidence
- BLOCKED: attempt failed or denied
- NONE: not available by design
- HUMAN_RELAY: only via ID01 copy/upload
