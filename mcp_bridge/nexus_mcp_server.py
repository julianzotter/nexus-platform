#!/usr/bin/env python3
"""NEXUS MCP-Bridge (stdio): LLM <-> local Google Drive mount (WORK) <-> nexus-platform repo.

Read tools are always on. The single write tool `submit_result` is disabled unless
NEXUS_MCP_WRITE=1; it only creates new, timestamped files (never overwrites) with a
sidecar .meta.json (sha256, status REVIEW, approval PENDING). Drive for desktop then
syncs the file to drive.google.com. No commits, merges or deployments.
"""
from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_WORK = r'G:\Meine Ablage\_developement\LLM-LOCAL-SSOT\WORK'
DEFAULT_REPO = str(Path.home() / 'nexus-platform')
BLOCKED_NAMES = ('.env', '.env.*', '*.key', '*.pem', '*.p12', '*.secret', 'token.json', '*.token',
                 'client_secret*.json', 'credentials*.json', 'drive-oauth.json', 'service_account*.json')
MAX_READ = 200_000
MAX_WRITE = 2_000_000
SAFE_NAME = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._ +()-]{0,150}$')
SAFE_ID = re.compile(r'^[A-Za-z0-9_-]{1,64}$')


class BridgeError(Exception):
    pass


class NexusBridge:
    def __init__(self, work_root: str | Path, repo_root: str | Path, write_enabled: bool = False):
        self.work = Path(work_root).resolve()
        self.repo = Path(repo_root).resolve()
        self.write_enabled = write_enabled

    # ---- guards -------------------------------------------------------
    def _inside(self, root: Path, rel: str) -> Path:
        if not rel or Path(rel).is_absolute() or '..' in Path(rel).parts:
            raise BridgeError('PATH_NOT_ALLOWED')
        p = (root / rel).resolve()
        if p != root and root not in p.parents:
            raise BridgeError('PATH_OUTSIDE_ROOT')
        if any(fnmatch.fnmatch(p.name.lower(), pat) for pat in BLOCKED_NAMES):
            raise BridgeError('SECRET_LIKE_FILE_BLOCKED')
        return p

    # ---- read tools ---------------------------------------------------
    def status(self) -> dict:
        return {'work_root': str(self.work), 'work_mounted': self.work.is_dir(),
                'repo_root': str(self.repo), 'repo_present': (self.repo / '.git').exists(),
                'repo_head': self._git('rev-parse', 'HEAD') if (self.repo / '.git').exists() else None,
                'write_enabled': self.write_enabled}

    def list_work(self, subdir: str = '.', pattern: str = '*', limit: int = 200) -> list[dict]:
        base = self.work if subdir in ('', '.') else self._inside(self.work, subdir)
        if not base.is_dir():
            raise BridgeError('NOT_A_DIRECTORY')
        out = []
        for p in sorted(base.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if fnmatch.fnmatch(p.name, pattern):
                st = p.stat()
                out.append({'path': str(p.relative_to(self.work)), 'dir': p.is_dir(), 'size': st.st_size,
                            'modified': datetime.fromtimestamp(st.st_mtime, timezone.utc).isoformat()})
                if len(out) >= min(limit, 1000):
                    break
        return out

    def read_work_file(self, path: str, max_bytes: int = MAX_READ) -> dict:
        p = self._inside(self.work, path)
        if not p.is_file():
            raise BridgeError('NOT_A_FILE')
        if p.suffix.lower() in ('.gdoc', '.gsheet', '.gslides'):
            raise BridgeError('GOOGLE_NATIVE_SHORTCUT_EXPORT_AS_MD_FIRST')
        data = p.read_bytes()
        return {'path': path, 'sha256': hashlib.sha256(data).hexdigest(), 'size': len(data),
                'truncated': len(data) > max_bytes,
                'text': data[:min(max_bytes, MAX_READ)].decode('utf-8', errors='replace')}

    def _git(self, *args: str) -> str:
        r = subprocess.run(['git', '-C', str(self.repo), *args], capture_output=True, text=True, timeout=30)
        if r.returncode:
            raise BridgeError('GIT_ERROR')
        return r.stdout.strip()

    def read_repo_file(self, path: str, ref: str = 'HEAD') -> dict:
        self._inside(self.repo, path)
        if not re.fullmatch(r'[A-Za-z0-9._/-]{1,100}', ref) or ref.startswith('-'):
            raise BridgeError('INVALID_REF')
        sha = self._git('rev-parse', f'{ref}^{{commit}}')
        text = self._git('show', f'{sha}:{path}')
        return {'path': path, 'commit': sha, 'text': text[:MAX_READ], 'truncated': len(text) > MAX_READ}

    def get_governance(self) -> dict:
        files = {}
        for rel in ('AGENTS.md', 'docs/adr/0001-evidence-and-gates.md', 'docs/NEXUS-GITHUB-WORK-TRANSFER.md'):
            try:
                files[rel] = self.read_repo_file(rel)
            except BridgeError:
                files[rel] = None
        agbs = sorted(self.work.parent.glob('_AGBS*.md')) if self.work.is_dir() else []
        return {'repo': files, 'agbs_local_candidates': [str(p) for p in agbs],
                'rule': 'REVIEW != APPROVED; human gate ID01 required'}

    # ---- gated write tool ---------------------------------------------
    def submit_result(self, work_order_id: str, name: str, content: str, agent_id: str,
                      subdir: str = 'REPORTS') -> dict:
        if not self.write_enabled:
            raise BridgeError('WRITE_DISABLED_SET_NEXUS_MCP_WRITE_1')
        if not SAFE_ID.fullmatch(work_order_id) or not SAFE_ID.fullmatch(agent_id) or not SAFE_NAME.fullmatch(name):
            raise BridgeError('INVALID_IDENTIFIER')
        data = content.encode('utf-8')
        if len(data) > MAX_WRITE:
            raise BridgeError('PAYLOAD_TOO_LARGE')
        target_dir = self._inside(self.work, subdir)
        target_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime('%y_%m_%d_%H%M%S')
        target = self._inside(self.work, f'{subdir}/{stamp}_{agent_id}_{work_order_id}_{name}')
        digest = hashlib.sha256(data).hexdigest()
        with open(target, 'xb') as fh:  # exclusive create: never overwrite
            fh.write(data)
        meta = {'work_order_id': work_order_id, 'agent_id': agent_id, 'file': target.name, 'sha256': digest,
                'repo_head': self.status()['repo_head'], 'status': 'REVIEW', 'approval': 'PENDING',
                'created_utc': datetime.now(timezone.utc).isoformat()}
        with open(target.with_name(target.name + '.meta.json'), 'x', encoding='utf-8') as fh:
            json.dump(meta, fh, indent=2)
        return meta


def build_server(bridge: NexusBridge):
    from mcp.server.fastmcp import FastMCP  # pip install "mcp>=1.2"
    mcp = FastMCP('nexus-bridge')

    def safe(fn):
        def wrapper(*a, **k):
            try:
                return fn(*a, **k)
            except BridgeError as exc:
                return {'error': str(exc)}
        wrapper.__name__, wrapper.__doc__ = fn.__name__, fn.__doc__
        return wrapper

    @mcp.tool()
    def bridge_status() -> dict:
        """Mount, repo HEAD and write gate status."""
        return safe(bridge.status)()

    @mcp.tool()
    def get_governance() -> dict:
        """Governance files (AGENTS.md, ADR, transfer contract) at repo HEAD."""
        return safe(bridge.get_governance)()

    @mcp.tool()
    def list_work(subdir: str = '.', pattern: str = '*', limit: int = 200) -> list | dict:
        """List WORK folder entries (newest first) on the local Drive mount."""
        return safe(bridge.list_work)(subdir, pattern, limit)

    @mcp.tool()
    def read_work_file(path: str) -> dict:
        """Read a WORK file (relative path) with sha256 provenance."""
        return safe(bridge.read_work_file)(path)

    @mcp.tool()
    def read_repo_file(path: str, ref: str = 'HEAD') -> dict:
        """Read a nexus-platform file at a commit/branch."""
        return safe(bridge.read_repo_file)(path, ref)

    @mcp.tool()
    def submit_result(work_order_id: str, name: str, content: str, agent_id: str) -> dict:
        """Create a NEW result file in WORK/REPORTS (status REVIEW). Requires NEXUS_MCP_WRITE=1."""
        return safe(bridge.submit_result)(work_order_id, name, content, agent_id)

    return mcp


def main() -> None:
    bridge = NexusBridge(os.environ.get('NEXUS_WORK_ROOT', DEFAULT_WORK),
                         os.environ.get('NEXUS_REPO_ROOT', DEFAULT_REPO),
                         os.environ.get('NEXUS_MCP_WRITE') == '1')
    build_server(bridge).run()  # stdio


if __name__ == '__main__':
    main()
