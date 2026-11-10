---
name: "artifacts-capabilities"
description: "Explains what artifacts can do: types, templates, editing, export, sharing, AI-powered use, connectors, storage, plan availability, limits. Use for any question on artifact capabilities."
---

# Artifacts Capabilities Explainer

## Purpose
Answer questions such as "what can artifacts do?", "which artifact type fits X?", "can an artifact do Y on my plan?", "why can't I share/store/connect?".

## Source of truth
- Primary: https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them
- Snapshot below taken 2026-11-10. Product details change: if the question hinges on a plan, limit, date or setting name, re-fetch the article first and prefer the live text. If fetch fails, answer from the snapshot and say it is dated 2026-11-10.
- Never invent a capability, limit or menu path. Unknown = "not documented in the article".

## Procedure
1. Identify what is asked: overview | specific capability | plan/availability | limit/restriction | choosing a type | troubleshooting.
2. Re-fetch the article if the answer depends on volatile facts (see above).
3. Answer only the asked scope. Overview = the capability matrix; specific question = the one relevant row plus its restriction.
4. Always state the restriction that belongs to a capability (plan, platform, limit).
5. End with the source link.

## Output format
- TL;DR line first.
- Compact bullets or one table; no filler.
- Answer in the user's language.
- For "which type for X": one recommendation + one-line reason.

## Capability snapshot (2026-11-10)

### Basics
- Artifact = content Claude makes that opens beside the chat and can be edited, revisited, shared.
- Created in any conversation (also Claude Code) or from a template in the Artifacts tab.
- Kinds: documents, code, single-page websites, images, diagrams/flowcharts, dashboards, small interactive tools.
- All artifacts live in the Artifacts tab (claude.ai/artifacts).
- Prerequisite: file creation / code execution setting enabled (Settings > Capabilities; Team/Enterprise: Organization settings > Capabilities).

### Templates and plans
| Template | Plans | Notes |
|---|---|---|
| Docs, Slides, Design | all plans | on by default; Enterprise default-on from 2026-10-15 |
| Dashboards (beta) | Pro, Max, Ultra, Team, Enterprise | Enterprise: off until owner enables; each chart shows query + last refresh |
| Motion (beta) | Team, Enterprise | Enterprise: off until owner enables; MP4 export |

- Designs and decks can use a design system (colors, fonts, components).
- Slides can be presented inside Claude.

### Editing
- Ask Claude, or edit directly in template artifacts (type in docs, edit slides, move canvas elements).
- Docs/Markdown: highlight text > "Edit with Claude" for a targeted edit.
- Multi-file Markdown (skill, plugin): queue edits across files, apply in one message.
- Editing an earlier message = separate chat branch with its own artifacts; original untouched.
- Errors: "Try fixing with Claude" button; fix not guaranteed.

### Export
| Type | Formats |
|---|---|
| Docs | Word, PDF, Markdown, Google Docs |
| Slides | PowerPoint, PDF, Google Slides |
| Design | zip, PDF, PowerPoint, standalone HTML |
| Motion | MP4 |
| Legacy | view code, copy, download |

### Sharing
- Start private. New artifacts share without publishing; legacy artifacts must be published.
- Sharing settings not changeable in iOS/Android apps (use web or Desktop).
- Remix (legacy published artifacts; Free, Pro, Max, Ultra): copy code into a new chat, describe changes; only from trusted sources.

### Artifacts that use Claude
- Artifact can call Claude; each user runs it on their own account and plan limits.
- No API key, no cost to the creator.
- New artifacts ask permission on first use; legacy: toggle under Settings > Capabilities.

### Connectors (MCP)
- Pro and above, web and Desktop.
- Read/write to connected apps and custom connectors.
- First use: approval list of apps/tools; individual tools can be disabled (persists).
- Tools needing per-action approval are not available to artifacts.
- Each user connects their own apps, also for shared artifacts.
- Team/Enterprise owners can disable org-wide.

### Storage
- Pro and above, web and Desktop.
- Personal (private per user) or shared (visible to all users of the artifact; confirmation on first use).
- Limit: 20 MB per artifact, text only.
- Legacy: storage only after publishing; unpublishing deletes stored data permanently.
- Warn: check for shared storage before entering sensitive data.

### Claude Code
- Every plan that includes Claude Code.
- Publish session output as a live page at a private URL, updating during the session.
- Designs via /design, docs too; Desktop opens docs in the side panel, terminal returns a web link.

### Legacy notes
- Legacy = created in chat before 2026-09-16; still work, can be published/shared, cannot be newly created.
- Live artifacts made before 2026-08-19 keep working but cannot be edited in place.

## Not covered by the article
- Detailed sharing permissions (separate article).
- Version history beyond chat branching.
- Answer these with "not documented here" and point to support.claude.com.