#!/usr/bin/env python3
"""Deterministic wayfinder generator for the NEXUS.* folders in LLM-LOCAL-SSOT.

Input : inventory JSON (folders + direct children, from Drive search or Drive API).
Output: one Markdown wayfinder, YAML frontmatter + one table row per folder.
Same input -> same bytes (sorted, no wall-clock). A wayfinder is NOT a registry:
it points to folder IDs; artifacts are registered only in file-registry.jsonl (AGBS v004 §2).
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

FOLDER_MIME = 'application/vnd.google-apps.folder'
ANCHOR_PREFIXES = ('folder.md', '_folder', 'readme', '_index', '_nexus_wayfinder')  # ledgers/snapshots are not anchors
# Role of each folder in the NEXUS layer model (name-derived, reviewed by ID01).
LAYER = {
    'NEXUS.REPORTS': ('L4-REPORTING', 'durable reports; WORK keeps operative originals'),
    'NEXUS.EVAL': ('L4-REPORTING', 'evaluation forms, scoring scripts'),
    'NEXUS.HISTORICAL': ('L0-GOVERNANCE', 'snapshots: ledger, AGBS, manifest (read-only history)'),
    'NEXUS.PROMPTS': ('L2-KNOWLEDGE', 'prompt registry / PromptSmith'),
    'NEXUS.NORM.SEARCH': ('L2-KNOWLEDGE', 'norm search results EC2/EC5/HBV/TCC'),
    'NEXUS.INDEX.PARSER': ('L3-TOOLS', 'parser, OCR, vector index, parse dashboards'),
    'NEXUS.MCP.SERVER': ('L3-TOOLS', 'MCP server code + desktop config'),
    'NEXUS.CAD.SKILLS': ('L3-TOOLS', 'RFEM6/dlubal API, DXF/IFC, CAD Python'),
    'NEXUS.DASHBOARDS': ('L5-INTERFACE', 'dashboards / speech-to-3D prototypes'),
    'NEXUS.CHAT.HISTORY': ('L1-RAW', 'chat exports, takeouts'),
    'NEXUS.PDF-RAW': ('L1-RAW', 'raw PDFs (literature, scans)'),
    'NEXUS.DOCX-RAW': ('L1-RAW', 'raw DOCX'),
    'NEXUS.TXT-RAW': ('L1-RAW', 'raw TXT notes'),
    'NEXUS.BILDER-RAW': ('L1-RAW', 'raw images, sketches'),
    'NEXUS.SCREENSHOTS': ('L1-RAW', 'device screenshots'),
    'NEXUS.MP3': ('L1-RAW', 'audio / transcripts'),
}


def summarize(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    """One deterministic summary row per folder."""
    children: dict[str, list[dict]] = defaultdict(list)
    for child in inventory['children']:
        children[child['parent']].append(child)
    rows = []
    for folder in sorted(inventory['folders'], key=lambda f: (LAYER.get(f['name'], ('L9',))[0], f['name'])):
        items = children.get(folder['id'], [])
        files = [c for c in items if c['mime'] != FOLDER_MIME]
        anchors = sorted(c['title'] for c in files if c['title'].lower().startswith(ANCHOR_PREFIXES))
        layer, role = LAYER.get(folder['name'], ('UNCLASSIFIED', 'unknown'))
        rows.append({
            'name': folder['name'], 'id': folder['id'], 'layer': layer, 'role': role,
            'files': len(files), 'subfolders': len(items) - len(files),
            'last_modified': max((c['modified'] for c in items), default='-'),
            'anchor': anchors[0] if anchors else 'NONE',
            'status': 'ANCHORED' if anchors else 'NO_ANCHOR',
        })
    return rows


def render(rows: list[dict[str, Any]], inventory: dict[str, Any], digest: str, header: dict[str, str]) -> str:
    """YAML frontmatter + table; values only from inventory/header (no wall clock)."""
    missing = sum(r['status'] == 'NO_ANCHOR' for r in rows)
    fm = [f'{k}: {v}' for k, v in header.items()] + [
        f'source_inventory_sha256: {digest}', f'observed_at: {inventory["observed_at"]}',
        f'folders_total: {len(rows)}', f'folders_without_anchor: {missing}',
        f'files_total: {sum(r["files"] for r in rows)}', f'scope: "{inventory["scope"]}"']
    lines = ['---', *fm, '---', '', '# NEXUS.* Wayfinder (LLM-LOCAL-SSOT)', '',
             'Lookup: keyword -> layer/role -> folder link. Not a registry; register artifacts in file-registry.jsonl.', '',
             '| Layer | Folder | Role | Files | Sub | Last mod. | Anchor | Link |',
             '|---|---|---|---:|---:|---|---|---|']
    for r in rows:
        link = f'https://drive.google.com/drive/folders/{r["id"]}'
        lines.append(f'| {r["layer"]} | {r["name"]} | {r["role"]} | {r["files"]} | {r["subfolders"]} '
                     f'| {r["last_modified"]} | {r["anchor"]} | [open]({link}) |')
    return '\n'.join(lines) + '\n'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--inventory', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--header', type=Path, required=True, help='JSON object with frontmatter keys')
    args = ap.parse_args()
    raw = args.inventory.read_bytes()
    inventory = json.loads(raw)
    text = render(summarize(inventory), inventory, hashlib.sha256(raw).hexdigest(),
                  json.loads(args.header.read_text(encoding='utf-8')))
    args.out.write_text(text, encoding='utf-8')
    print(json.dumps({'out': str(args.out), 'sha256': hashlib.sha256(text.encode()).hexdigest()}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
