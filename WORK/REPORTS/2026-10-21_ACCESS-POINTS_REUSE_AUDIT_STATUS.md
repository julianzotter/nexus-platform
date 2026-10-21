# NEXUS Statusreport — Access Points / Reuse Audit
Date: 2026-10-21 | Status: REVIEW_REQUIRED | Human approval: PENDING
Workorder: [WO-20261021-ACCESS-POINTS](../../access-points/WORKORDER.md)
Branch: feat/access-points-registry-20261021
Author identity: ChatGPT connector session (agent ID unverified)
Delivery: GitHub branch only. Drive WORK writeback NOT VERIFIED.

## Summary
Initial registry of 20 API/MCP/library documentation access points and new navigator skill created. Existing assets identified; **reuse before implementing parallel functionality**. No live RFEM connection or secrets audit performed.

## Existing reusable GitHub assets
- [RFEM6 MCP engineering skill](https://github.com/julianzotter/nexus-platform/blob/main/plugins/nexus-aec-engineering/skills/rfem6-mcp-engineering/SKILL.md): reuse setup, G0 gate, model identity, tool discovery.
- [RFEM6 runtime setup](https://github.com/julianzotter/nexus-platform/blob/main/plugins/nexus-aec-engineering/skills/rfem6-mcp-engineering/references/runtime-setup.md): reuse runtime preflight.
- [MCP bridge](https://github.com/julianzotter/nexus-platform/blob/main/mcp_bridge/nexus_mcp_server.py): reuse existing Drive WORK transport, never assume connected.
- [MCP bridge installation](https://github.com/julianzotter/nexus-platform/blob/main/mcp_bridge/install_mcp_bridge.ps1): Windows setup reference.
- [Drive-GitHub-MCP contract](https://github.com/julianzotter/nexus-platform/blob/main/docs/NEXUS-DRIVE-GITHUB-MCP.md): review/NOT_MERGED as documented.
- [Skill inventory](https://github.com/julianzotter/nexus-platform/blob/main/tools/skill_inventory.py): reuse structural inventory and SHA-256 logic.
- [Hybrid integration](https://github.com/julianzotter/nexus-platform/blob/main/hybrid_integration/README.md): local derived index, connector candidates.
- [RFEM API log specification](https://github.com/julianzotter/julianzotter/blob/main/docs/00_Quellenlog/API_Auszuege/README.md): units, audit log and hash rules.
- [Dashboard integration](https://github.com/julianzotter/NEXUS-AI-ECOSYSTEM-LOOP_3D-STUDIO-VISUALS-DASHBOARD-/blob/main/integration/README.md): coordinate downstream UI.

## Drive sources identified by metadata, content not audited
- [2026-10-21 RFEM PowerShell/Dlubal API COM gRPC dump — WORK copy](https://drive.google.com/file/d/1mg1P5AKeNjKOb5NHOy6H5G4aOsvBYfS7/view) — 57,962 bytes.
- [Same-named RFEM dump — other copy](https://drive.google.com/file/d/1Sm_ELlci5gO8hJzjb1F2q2WxssMpZyi9/view) — 57,962 bytes; same size is not hash equivalence.
- [RFEM API Port9000 PowerShell notes](https://drive.google.com/file/d/1YcK3xOH2saPMoP_xtDZnmIAQZLBKHSJv/view) — potential credentials: SECURITY_REVIEW_REQUIRED before copying any content.
- [MCP-ACCESS-TOOLS](https://drive.google.com/drive/folders/1fRa7rQvKi-BkhVIzjXPcY_u8iIJ4Vn5J)
- [Authoritative NEXUS WORK](https://drive.google.com/drive/folders/1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP)
- [WORK Folder.md governance entrypoint](https://drive.google.com/file/d/11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH/view)

## Decisions
1. Preserve existing RFEM MCP engineering skill; navigator is only discovery/routing, not a competing engineering solver.
2. Do not publish raw RFEM dumps until secrets, host paths, credentials and sensitive config are redacted.
3. Treat GitHub as review snapshot and Drive WORK as authoritative where current governance requires it.
4. No automatic merge/release: review, CI, human approval required.

## Review checklist
- [ ] Read current WORK Folder.md and confirm naming, delivery, owner and evidence conventions.
- [ ] Inspect both RFEM dump copies securely; classify COM/gRPC/port, SDK versions and ini settings; redact secrets; compare SHA-256.
- [ ] Inventory all existing ChatGPT skills and relevant GitHub repos; consolidate duplicates.
- [ ] Extend registry with references to reused implementations, transport, capabilities, verification and evidence IDs.
- [ ] Validate JSON schema, links, skill metadata, CI and tests.
- [ ] Deliver status to Drive WORK via authorized bridge, obtain readback receipt.
- [ ] Obtain reviewer ACK and human signoff; only then merge PR to main.

## Evidence / limitations
GitHub code search and Drive metadata search completed; no full repository-wide inventory, no source-byte hashing, no live MCP smoke test, no authenticated RFEM host access, no Drive writeback receipt. This status file is a review candidate, not an engineering release.
