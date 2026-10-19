#!/usr/bin/env python3
"""NEXUS event ledger: Inbox/Outbox state machine without shared mutable files.

One immutable JSON file per event under WORK/LEDGER/<work_order_id>/<seq>.json (exclusive create =
optimistic concurrency: two writers racing for the same seq -> one gets SEQUENCE_CONFLICT_RETRY).
Safe on Google Drive for desktop: concurrent agents never write the same file, so no
conflict copies. State = replay of events (sorted by time-ordered event id).

States:  REQUESTED -> ACK -> DONE -> VERIFIED   (+ BLOCKED, TIMEOUT)
- ACK/DONE/BLOCKED only by the addressed receiver (BLOCKED also by SYS-VERIFY on hash mismatch); REQUESTED by anyone (sender = configured agent).
- VERIFIED only by the deterministic verifier (agent SYS-VERIFY) after sha256 readback.
- APPROVED is NOT a ledger state: human release (ID01) stays outside agents (PR merge / signed decision).
0 LLM tokens. Stdlib only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

SAFE = re.compile(r'^[A-Za-z0-9_-]{1,64}$')
VERIFIER = 'SYS-VERIFY'
TRANSITIONS = {
    None: {'REQUESTED'},
    'REQUESTED': {'ACK', 'BLOCKED', 'TIMEOUT'},
    'ACK': {'DONE', 'BLOCKED', 'TIMEOUT'},
    'DONE': {'VERIFIED', 'BLOCKED'},
    'TIMEOUT': {'ACK', 'BLOCKED'},
    'BLOCKED': {'REQUESTED'},
    'VERIFIED': set(),
}
RECEIVER_ONLY = {'ACK', 'DONE', 'BLOCKED'}


class LedgerError(Exception):
    pass


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


class Ledger:
    def __init__(self, work_root: str | Path, agent_id: str, now=lambda: datetime.now(timezone.utc)):
        if not SAFE.fullmatch(agent_id):
            raise LedgerError('INVALID_AGENT_ID')
        self.work = Path(work_root).resolve()
        self.root = self.work / 'LEDGER'
        self.agent = agent_id
        self.now = now

    # ---- storage ------------------------------------------------------
    def _artifact(self, rel: str) -> Path:
        if not rel or Path(rel).is_absolute() or '..' in Path(rel).parts:
            raise LedgerError('ARTIFACT_PATH_NOT_ALLOWED')
        p = (self.work / rel).resolve()
        if self.work not in p.parents:
            raise LedgerError('ARTIFACT_OUTSIDE_WORK')
        return p

    def events(self, wo: str) -> list[dict]:
        d = self.root / wo
        if not d.is_dir():
            return []
        out = []
        for f in sorted(d.glob('[0-9]*.json')):
            try:
                out.append(json.loads(f.read_text(encoding='utf-8')))
            except (ValueError, OSError):
                out.append({'event_id': f.stem, 'state': 'CORRUPT', 'file': f.name})
        return out  # filename order == seq order (zero-padded)

    def state(self, wo: str) -> dict | None:
        allev = self.events(wo)
        evs = [e for e in allev if e.get('state') != 'CORRUPT']
        if not evs:
            return None
        req = next(e for e in reversed(evs) if e['state'] == 'REQUESTED')
        last = evs[-1]
        return {'work_order_id': wo, 'state': last['state'], 'from': req['from'], 'to': req['to'],
                'title': req.get('title'), 'last_event': last['event_id'], 'last_by': last['by'],
                'artifact': next((e.get('artifact') for e in reversed(evs) if e.get('artifact')), None),
                'ack_deadline': req.get('ack_deadline'), 'events': len(evs), 'corrupt': len(allev) - len(evs)}

    def _append(self, wo: str, state: str, **fields) -> dict:
        if not SAFE.fullmatch(wo):
            raise LedgerError('INVALID_WORK_ORDER_ID')
        cur = self.state(wo)
        prev_state = cur['state'] if cur else None
        if state not in TRANSITIONS.get(prev_state, set()):
            raise LedgerError(f'INVALID_TRANSITION_{prev_state}_TO_{state}')
        if state in RECEIVER_ONLY and self.agent not in (cur['to'], VERIFIER):
            raise LedgerError('ONLY_RECEIVER_MAY_SET_' + state)
        if state == 'VERIFIED' and self.agent != VERIFIER:
            raise LedgerError('ONLY_SYS_VERIFY_MAY_VERIFY')
        seq = (cur['events'] + cur.get('corrupt', 0)) + 1 if cur else 1
        ev = {'event_id': f'{wo}-{seq:06d}', 'seq': seq, 'work_order_id': wo, 'state': state, 'by': self.agent,
              'prev_event': cur['last_event'] if cur else None,
              'ts': self.now().isoformat(timespec='seconds'), **fields}
        d = self.root / wo
        d.mkdir(parents=True, exist_ok=True)
        try:
            with open(d / f'{seq:06d}.json', 'x', encoding='utf-8') as fh:
                json.dump(ev, fh, indent=2, ensure_ascii=False)
        except FileExistsError:
            raise LedgerError('SEQUENCE_CONFLICT_RETRY') from None
        return ev

    # ---- agent API ----------------------------------------------------
    def send(self, wo: str, to: str, title: str, input_path: str | None = None, ack_minutes: int = 120) -> dict:
        if not SAFE.fullmatch(to):
            raise LedgerError('INVALID_RECEIVER')
        art = None
        if input_path:
            p = self._artifact(input_path)
            art = {'path': input_path, 'sha256': sha256_file(p)}
        deadline = (self.now() + timedelta(minutes=ack_minutes)).isoformat(timespec='seconds')
        return self._append(wo, 'REQUESTED', **{'from': self.agent, 'to': to}, title=title[:200],
                            input=art, ack_deadline=deadline)

    def ack(self, wo: str) -> dict:
        return self._append(wo, 'ACK')

    def done(self, wo: str, artifact_path: str, drive_id: str | None = None) -> dict:
        p = self._artifact(artifact_path)
        if not p.is_file():
            raise LedgerError('ARTIFACT_MISSING')
        return self._append(wo, 'DONE', artifact={'path': artifact_path, 'sha256': sha256_file(p),
                                                  'drive_id': drive_id})

    def block(self, wo: str, reason: str) -> dict:
        return self._append(wo, 'BLOCKED', reason=reason[:500])

    def inbox(self) -> list[dict]:
        """Open items that need action by this agent (receiver: REQUESTED/TIMEOUT, sender: BLOCKED)."""
        out = []
        for wo in self.work_orders():
            s = self.state(wo)
            if (s['to'] == self.agent and s['state'] in ('REQUESTED', 'TIMEOUT', 'ACK')) or \
               (s['from'] == self.agent and s['state'] == 'BLOCKED'):
                out.append(s)
        return out

    def work_orders(self) -> list[str]:
        return sorted(p.name for p in self.root.iterdir() if p.is_dir()) if self.root.is_dir() else []

    # ---- deterministic verifier (SYS-VERIFY only) ---------------------
    def verify_all(self) -> list[dict]:
        if self.agent != VERIFIER:
            raise LedgerError('ONLY_SYS_VERIFY_MAY_VERIFY')
        results = []
        for wo in self.work_orders():
            s = self.state(wo)
            if s['state'] in ('REQUESTED',) and s['ack_deadline'] and \
                    self.now() > datetime.fromisoformat(s['ack_deadline']):
                results.append(self._append(wo, 'TIMEOUT', reason='ACK_DEADLINE_PASSED'))
            elif s['state'] == 'DONE':
                art = s['artifact']
                p = self._artifact(art['path'])
                if p.is_file() and sha256_file(p) == art['sha256']:
                    results.append(self._append(wo, 'VERIFIED', check='SHA256_READBACK_MATCH',
                                                human_acceptance='PENDING'))
                else:
                    results.append(self._append(wo, 'BLOCKED', reason='ARTIFACT_MISSING_OR_SHA_MISMATCH'))
        self.render_status()
        return results

    def render_status(self) -> Path:
        """Regenerate STATUS.md and _FRONT_LOG.md from events (single writer, derived, never hand-edited)."""
        rows, log = [], []
        for wo in self.work_orders():
            s = self.state(wo)
            rows.append(f"| {wo} | {s['state']} | {s['from']} -> {s['to']} | {s['last_by']} | "
                        f"{(s['artifact'] or {}).get('sha256', '')[:12]} |")
            for e in self.events(wo):
                log.append((e.get('ts', ''), f"| {e.get('ts')} | {wo} | {e.get('state')} | {e.get('by')} |"))
        stamp = self.now().isoformat(timespec='seconds')
        status = ['# NEXUS STATUS (generiert, nicht editieren)', f'Stand: {stamp}', '',
                  '| Work order | State | Route | Last by | Artifact sha256 |', '|---|---|---|---|---|', *rows]
        front = ['# _FRONT_LOG (generiert aus LEDGER, chronologisch)', '', '| ts | WO | State | By |',
                 '|---|---|---|---|', *[l for _, l in sorted(log)]]
        out = self.root / 'STATUS.md'
        for path, lines in ((out, status), (self.root / '_FRONT_LOG.md', front)):
            tmp = path.with_name(path.name + '.tmp')
            tmp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
            os.replace(tmp, path)
        return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--work', default=os.environ.get('NEXUS_WORK_ROOT', r'G:\Meine Ablage\_developement\LLM-LOCAL-SSOT\WORK'))
    ap.add_argument('--agent', default=os.environ.get('NEXUS_AGENT_ID'), required=not os.environ.get('NEXUS_AGENT_ID'))
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('send'); s.add_argument('wo'); s.add_argument('to'); s.add_argument('title')
    s.add_argument('--input'); s.add_argument('--ack-minutes', type=int, default=120)
    sub.add_parser('ack').add_argument('wo')
    d = sub.add_parser('done'); d.add_argument('wo'); d.add_argument('artifact'); d.add_argument('--drive-id')
    b = sub.add_parser('block'); b.add_argument('wo'); b.add_argument('reason')
    sub.add_parser('inbox'); sub.add_parser('verify'); sub.add_parser('status')
    a = ap.parse_args()
    L = Ledger(a.work, a.agent)
    try:
        r = {'send': lambda: L.send(a.wo, a.to, a.title, a.input, a.ack_minutes), 'ack': lambda: L.ack(a.wo),
             'done': lambda: L.done(a.wo, a.artifact, a.drive_id), 'block': lambda: L.block(a.wo, a.reason),
             'inbox': L.inbox, 'verify': L.verify_all, 'status': lambda: str(L.render_status())}[a.cmd]()
    except LedgerError as exc:
        print(json.dumps({'error': str(exc)})); return 2
    print(json.dumps(r, indent=2, ensure_ascii=False)); return 0


if __name__ == '__main__':
    raise SystemExit(main())
