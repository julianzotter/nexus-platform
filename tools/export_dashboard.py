#!/usr/bin/env python3
"""Export a validated read-only snapshot; never change registry/release state."""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from integration.contract import validate
from knowledge_health import assess_item, load_registry_ids

def build_snapshot(root, revision, monitor_path=None, now=None):
    now = now or datetime.now(timezone.utc)
    sources = []
    def read(path):
        body = path.read_bytes()
        sources.append({'path': path.relative_to(root).as_posix(), 'sha256': hashlib.sha256(body).hexdigest()})
        return body.decode('utf-8')
    registry = root/'registry/file-registry.jsonl'
    # Hash and parse the same bytes, without a second read of a mutable input.
    records = [json.loads(line) for line in read(registry).splitlines() if line.strip()]
    ids = [r['id'] for r in records]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate file registry ID')
    directory = root/'registry/knowledge'
    if not directory.is_dir():
        raise ValueError('Knowledge directory unavailable')
    entries = []
    for path in sorted(directory.glob('*.json')):
        item = json.loads(read(path))
        entries.append({'record': item, 'health': assess_item(item, set(ids), now, 180)['state']})
    monitor = None
    if monitor_path is not None:
        raw = json.loads(read(monitor_path))
        monitor = {key: raw[key] for key in ('status','observed_at','commit','run_id','run_attempt')}
        monitor['checks'] = {name: value['status'] for name,value in raw['checks'].items()}
    result = {'schema_version':'nexus-registry-dashboard/1.0.0',
              'generated_at':now.isoformat(),
              'source':{'repository':'julianzotter/nexus-platform','revision':revision,'files':sources},
              'knowledge':entries,'monitor':monitor,
              'limitations':['Read-only export; no engineering or human release authority.',
                 'Hashes identify exported inputs; they do not authenticate original sources.',
                 'Health is metadata validation, not an authenticated engineering approval.',
                 'No inferred graph relations; monitoring timestamps are separate from export time.']}
    return validate(result)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revision',default=os.environ.get('GITHUB_SHA'))
    parser.add_argument('--monitor',type=Path)
    parser.add_argument('--output',type=Path,default=ROOT/'reports/monitor/dashboard-snapshot.json')
    args=parser.parse_args()
    snapshot=build_snapshot(ROOT,args.revision,args.monitor)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    temporary=args.output.with_suffix('.tmp')
    temporary.write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    temporary.replace(args.output)
    print(f"Exported {len(snapshot['knowledge'])} knowledge records; no release decision")

if __name__=='__main__':
    main()
