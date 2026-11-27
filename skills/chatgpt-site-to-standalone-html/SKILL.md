---
name: chatgpt-site-to-standalone-html
description: Export or reconstruct an authorized ChatGPT Site or HTML-based Control Panel as a versioned, portable single-file HTML deliverable for Windows, Android and web browsers. Use for HTML snapshots, read-only decision dashboards, and NEXUS use-case delivery; never claim server-side feature equivalence without verified sources.
---

# ChatGPT Site → Standalone HTML
Version: 0.1.0-draft · Ticket: [nexus-platform#158](https://github.com/julianzotter/nexus-platform/issues/158) · Scope: NEXUS Control Panel & authorized user projects. Status: PROPOSED / REVIEW_REQUIRED.

## Start gate and authority
Read **current** Drive `_AGBS.md`, Manifest/role register, Baseline, WORK/Folder.md and target USECASE folder before any repository or cloud mutation. Record observed source IDs, versions, timestamps, runtime identity, permissions, task_id and GitHub HEAD; unknowns remain UNKNOWN. ID01 authorizes/reviews; ID03 coordinates; ID06 performs engineering implementation; an independent reviewer checks output. Never modify the canonical Site or merge a PR without the actual ID01 human gate.

## Sources and modes (mandatory distinction)
**SOURCE_EXPORT** — user-provided authorized source files or source bundle, including index.html, CSS, JS, images and licenses. Use reproducible bundling and explicit provenance.

**RECONSTRUCTION** — authored equivalent built from content and screenshots the user may lawfully supply; mark functionality not actually recovered. A published `*.chatgpt.site` URL alone does not demonstrate access to the original project files or its server-side app logic. Never promise automatic extraction, reverse-engineering of access controls, or a byte-identical original.

**CONNECTED_VIEW** — HTML frontend consuming separately authorized documented read-only APIs; this is not fully offline and must show LIVE / STALE / UNKNOWN, as_of and exact source. Do not embed secrets or access tokens. Network failure must not silently become READY.

All three modes are separate deliverables; a single HTML file does not replicate an API, server persistence, ChatGPT conversation state, sign-in, or native ChatGPT Apps/Sites navigation.

## Executable workflow
1. **Resolve input** — site URL (context only), repository path or upload, canonical version/commit, ownership, requested behaviors, output target and necessary external endpoints. Check reuse: `apps/control-panel/site`, `skills/` and Drive `USECASES/CONTROL-PANEL`; do not create a duplicate master UI.
2. **Inventory** — create manifest of relative asset paths, hashes, MIME types, dependencies, data flows, dynamic operations and pages. Identify external CSS/JS/images, API routes, cookies and backend requirements. Fail closed on untrusted or inaccessible assets.
3. **Render/bundle** — create versioned `index.html` with `<!doctype html>`, UTF-8, viewport, accessible semantic layout, local/embed assets and CSP appropriate to the selected mode. Prefer offline-safe inline CSS/JS without third-party CDNs. Escape untrusted source text and avoid `innerHTML` for API content. Never insert credentials.
4. **Integrate decision layer** — render ID01 decisions by verified `ticket_id`, owner, status, as_of, evidence URL and destination URL. Link GitHub PRs/reviews, settings and Work Order; use native browser links for action. GitHub actions requiring user authentication remain on GitHub; no counterfeit Merge/Approve button.
5. **Validate** — parse HTML, check local links and embedded assets, JS syntax and CSP/XSS surfaces; open at 390/900/1440 px and keyboard only; test offline (no network) and connected-mode timeout/rate-limit/private-repo errors. Include test matrix with actual environments; unexecuted tests = NOT_RUN.
6. **Publish** — preserve existing files. Write new versioned raw HTML to Drive `USECASES/CONTROL-PANEL` (verified folder ID `1t7T-KWn2s9HUctXGg-HY04z3xLamRJ5g`) and, if authorized, the review branch of `julianzotter/nexus-platform`. GitHub is review mirror, Drive the artifact destination. Verify Drive ID/path, original bytes or limits of readback, size and SHA-256 where possible.
7. **Review, return, monitor** — register the new artifact through the designated single writer (until then `REGISTRATION_PENDING`). Link GitHub issue #158 ↔ PR ↔ full HEAD SHA ↔ Drive file URL in a UTF-8 Markdown WORK return record. Require separate actual ACK, CI/test receipt, ID02/ID07 review and ID01 release. Track outstanding changes in issue #158; do not confuse GitHub comment with ACK.

## Acceptance / result contract
Return exactly **FINDINGS | EVIDENCE/SOURCES | ARTIFACTS | RISKS | NEXT_ACTION** plus:
- `workorder=WO-20261127-ID01-SITE2HTML-CONTROLPANEL`
- `mode=SOURCE_EXPORT|RECONSTRUCTION|CONNECTED_VIEW`
- `source_commit`, `output_sha256` (only calculated from actual bytes), `drive_file_id`, `pr_url`, `head_sha`
- `tests` including exact executed command/device/browser and PASS/FAIL/NOT_RUN
- `registration_status`, `review_status`, `human_gate`, `return_receipt`, and `as_of` in Europe/Vienna.

Never claim a ChatGPT native-app tab or launch popup was installed. Treat popups/on-login requests as a separate platform-support requirement; offer a scheduled notification or web dashboard entry only as a different, explicitly labeled mechanism.

## Required references
- [NEXUS issue #158](https://github.com/julianzotter/nexus-platform/issues/158)
- [Canonical NEXUS Site](https://nexus-sync-diagnose.julianzotter.chatgpt.site)
- [NEXUS WORK](https://drive.google.com/drive/folders/1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP)
- [Drive USECASES/CONTROL-PANEL](https://drive.google.com/drive/folders/1t7T-KWn2s9HUctXGg-HY04z3xLamRJ5g)
