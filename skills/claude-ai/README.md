# skills/claude-ai — review snapshot of Julian's claude.ai account skills

- Source: claude.ai account skills (synced copy), snapshot 2026-11-10, taken by ID06 Claude.
- Content: nine custom skills, copied byte-identical. Not edited here; the account is the source, this is a snapshot.
- Integrity: `MANIFEST.sha256` (sha256sum format, 24 files). CI runs `sha256sum -c` on every pull request.
- Inventory (`tools/skill_inventory.py`, structure and bytes only): 5 INCOMPLETE (optional fields unknown), 4 INVALID
  (`knowledge-ingestion`, `knowledge-quality-gate`, `mail-harvester`, `source-governance`: multi-line YAML description,
  which the flat-frontmatter parser rejects). Function and release are not checked.
- Status: REVIEW SNAPSHOT. No ledger ID allocated, no human release (ID01).
- `README.md` and `MANIFEST.sha256` are not listed in the manifest.
- `_proposed/`: three skills drafted by ID06 on 2026-11-10 from the Fable 5.2 / Mythos 5.2 release page (`model-effort-router`, `orchestrator-reviewer-split`, `model-release-watch`). Status PROPOSED: shown as proposal card in chat, not confirmed saved in the account, untested.
