---
name: google-ai-stack-starter
description: Antigravity 2.0 + AI Studio + Colab MCP — verified inventory, starter configs, 30-min test plan
version: 0.1.0
status: configs built, NOT yet executed on device (Tests 1-3 open)
timestamp: 2026-11-09T07:25:10Z
agent: claude-fable-5.1 (Claude Computer session)
tasks_done: verify attachment vs live docs; build mcp_config.json, .env.example, colab_starter.ipynb
tasks_open: T1 AI Studio Get-Code; T2 Colab MCP create/execute; T3 Antigravity project + GitHub MCP; enter keys
problems: Datalayer endpoint unreachable from sandbox; colab-mcp tool names/auth not on README landing page
open_questions: GitHub PAT scope (fine-grained vs classic); which repo for Tallinn slides
checksum_sha256: see LOG
---

## TL;DR
- Attachment is largely correct; 4 claims unverified (see below).
- 3 artefacts ready: `mcp_config.json` (GitHub-hosted, colab-mcp, context7, gemini-docs), `.env.example`, Colab notebook (Gemini call, LCA table+plot, structured output).
- Nothing executed yet — needs your keys + local run.

## Verified (live docs, 2026-11-09T07:25:10Z)
- Antigravity = product family: App v2.29.1, CLI v1.5.1 (`agy`), standalone IDE v2.6.0, SDK v0.1.23, IDE extensions. Install CLI: `curl -fsSL https://antigravity.google/cli/install.sh | bash` (Win: `irm .../install.ps1 | iex`).
- Shared MCP config: `~/.gemini/config/mcp_config.json` (global) | `<ws>/.agents/mcp_config.json` (workspace) | `<plugin>/mcp_config.json`. Schema supports `command/args/env` and `serverUrl/headers`.
- Plugin marketplace: announced 2026-10-29; `agy plugin install <name|github-url|./path>`, `list/enable/disable/uninstall`; manifest schema `antigravity.google/schemas/v1/plugin.json`.
- colab-mcp: Apache-2.0, run via `uvx git+https://github.com/googlecolab/colab-mcp`; clients: Gemini CLI, Claude Code, Windsurf; needs local client + `tools/list_changed`; bridges to a Colab session open in your browser.
- AI Studio llms.txt: models incl. gemini-3.5-flash, gemini-3.8-flash, gemini-3.1-pro-preview, gemini-4-argon; SDK = `google-genai`; Gemini Docs MCP: `https://gemini-api-docs-mcp.dev`; `llms-full.txt` exists.
- js-genai: `npm i @google/genai`, env `GEMINI_API_KEY`, MCP via `mcpToTool` (experimental), Live API.

## Unverified (attachment claims, no primary source found)
- "2.0 since I/O 19 May 2026", "Jules EOL 31 Dec 2026", "key restriction since 19 Jun 2026", colab-mcp "7 tools / OAuth token path".
- Datalayer `mcp.datalayer.run/mcp`: fetch failed (client error) — check manually.

## Security rules (confirmed)
- Keys only in `.env` / Colab Secrets / Antigravity settings. Colab OAuth = broad Drive scope. Review `hooks.json`+`mcp_config.json` before installing third-party plugins (hooks can execute commands).

## Next (your device)
1. `cp .env.example .env`, fill keys. 2. Copy `mcp_config.json` → `~/.gemini/config/`. 3. Upload notebook to Colab, add Secret. 4. Run Tests 1-3 from attachment, log results here.

## References
#1, AG-MCP, https://antigravity.google/docs/mcp
#2, AG-Plugins, https://antigravity.google/docs/cli/plugins
#3, AG-Download, https://antigravity.google/download
#4, Colab-MCP, https://github.com/googlecolab/colab-mcp
#5, AIS-llms, https://aistudio.google.com/llms.txt
#6, js-genai, https://github.com/googleapis/js-genai
#7, DevKnow-Codelab, https://codelabs.developers.google.com/developer-knowledge-mcp-antigravity
