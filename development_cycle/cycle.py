"""Small append-only DELTA history; no model calls, email or delete operations."""
from __future__ import annotations
import hashlib
import json
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def encode(value: Any) -> str:
    """Canonical JSON rejects non-finite numeric values."""
    return json.dumps(value,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(',',':'))


def digest(value: Any) -> str:
    """Hash canonical JSON, not a model assertion."""
    return hashlib.sha256(encode(value).encode()).hexdigest()


def difference(before: dict, after: dict) -> dict:
    """Sparse top-level replacement patch; nested values are atomic."""
    return {'set':{key:value for key,value in after.items() if key not in before or before[key]!=value},
            'remove':sorted(set(before)-set(after))}


def _history(connection: sqlite3.Connection, task: str, number: int) -> dict:
    """Verify hashes while reconstructing an output from its checkpoint."""
    output={};expected=1
    rows=connection.execute('SELECT run_number,delta_json,checkpoint_json,record_json,record_hash FROM cycle_runs WHERE task_id=? AND run_number<=? ORDER BY run_number',(task,number))
    for run_number,patch_text,checkpoint_text,record_text,record_hash in rows:
        if run_number!=expected or digest([patch_text,checkpoint_text,record_text])!=record_hash:
            raise ValueError('Run history integrity failure')
        patch=json.loads(patch_text);record=json.loads(record_text)
        if checkpoint_text is not None:output=json.loads(checkpoint_text)
        else:
            for key in patch['remove']:output.pop(key,None)
            output.update(patch['set'])
        if digest(output)!=record['output_sha256']:raise ValueError('Output integrity failure')
        expected+=1
    if expected!=number+1:raise ValueError('Requested run not found')
    return output


def replay(database: Path, task: str, number: int) -> dict:
    """Read-only reconstruction of one recorded result."""
    if number<1:raise ValueError('Run number must be positive')
    with closing(sqlite3.connect(database.resolve().as_uri()+'?mode=ro',uri=True)) as connection:
        return _history(connection,task,number)


def _record(connection: sqlite3.Connection, task: str, output: dict, checks: dict, baseline: str, assumptions: list[str]) -> dict:
    """Create evaluation metadata and N-1/N-2 comparisons."""
    previous=connection.execute('SELECT run_number,record_json FROM cycle_runs WHERE task_id=? ORDER BY run_number DESC LIMIT 1',(task,)).fetchone()
    number=previous[0]+1 if previous else 1
    compared=list(range(number-1,max(0,number-3),-1))
    comparisons={str(index):difference(_history(connection,task,index),output) for index in compared}
    return {'task_id':task,'run_number':number,'created_at_utc':datetime.now(timezone.utc).isoformat(),
        'baseline_sha256':hashlib.sha256(baseline.encode()).hexdigest(),
        'baseline_changed':bool(previous and json.loads(previous[1])['baseline_sha256']!=hashlib.sha256(baseline.encode()).hexdigest()),
        'output_sha256':digest(output),'checks':checks,'acceptance_met':bool(checks) and all(checks.values()),
        'acceptance_pass_rate':sum(checks.values())/len(checks) if checks else None,
        'accuracy':None,'confidence':None,'assumptions':assumptions,
        'compared_to':compared,'comparison_deltas':comparisons,
        'baseline_check_status':'PASS' if checks.get('baseline') is True else 'UNVERIFIED',
        'review_status':'NOT_RUN','release_status':'DEVELOPMENT_ONLY'}


def append_run(database: Path, task: str, output: dict, checks: dict, baseline: str, assumptions: list[str]) -> dict:
    """Append one immutable-by-application record; keep a base plus deltas."""
    if not task or not baseline or not isinstance(output,dict):raise ValueError('Task, baseline and object output required')
    if any(type(value) is not bool for value in checks.values()):raise ValueError('Checks require explicit boolean observations')
    encode(output)
    with closing(sqlite3.connect(database)) as connection, connection:
        connection.execute('CREATE TABLE IF NOT EXISTS cycle_runs (task_id TEXT, run_number INTEGER, delta_json TEXT NOT NULL, checkpoint_json TEXT, record_json TEXT NOT NULL, record_hash TEXT NOT NULL, PRIMARY KEY(task_id,run_number))')
        connection.execute('BEGIN IMMEDIATE')
        record=_record(connection,task,output,checks,baseline,assumptions)
        number=record['run_number']
        previous=_history(connection,task,number-1) if number>1 else {}
        patch_text=encode(difference(previous,output));checkpoint_text=encode(output) if number==1 else None
        record_text=encode(record)
        connection.execute('INSERT INTO cycle_runs VALUES (?,?,?,?,?,?)',(task,number,patch_text,checkpoint_text,record_text,digest([patch_text,checkpoint_text,record_text])))
    return record


def execute_cycle(database: Path, task: str, candidates: list[tuple[dict,dict]], baseline: str, max_runs: int=3) -> dict:
    """Evaluate supplied trials within an explicit budget; always return progress."""
    if type(max_runs) is not int or max_runs<1 or not candidates:raise ValueError('Candidates and positive budget required')
    signatures=[]
    for output,checks in candidates[:max_runs]:
        record=append_run(database,task,output,checks,baseline,[])
        signatures.append(record['output_sha256'])
        if record['acceptance_met']:return dict(record,termination='ACCEPTANCE_MET')
        if len(signatures)>=3 and len(set(signatures[-3:]))==1:
            return dict(record,termination='PLATEAU_PARTIAL_DELIVERY')
    return dict(record,termination='BUDGET_PARTIAL_DELIVERY')


def freeze_review(root: Path, files: list[str]) -> dict:
    """Bind independent review requests to identical file bytes."""
    entries={}
    for relative in sorted(files):
        target=(root/relative).resolve()
        if not target.is_relative_to(root.resolve()):raise ValueError('Review path escapes root')
        entries[relative]=hashlib.sha256(target.read_bytes()).hexdigest()
    return {'schema':'NEXUS_REVIEW_BUNDLE_V1','files':entries,'bundle_sha256':digest(entries),
        'reviews':{'claude':{'status':'NOT_RUN','focus':'architecture_interfaces_simplification'},
                   'gemini':{'status':'NOT_RUN','focus':'evidence_algorithm_tests_counterexamples'}}}


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    options=parser.parse_args()
    options.out.mkdir(parents=True,exist_ok=True)
    trials=[({'answer':answer},{'reference':answer==6*7,'baseline':True})
            for answer in (40,41,42)]
    result=execute_cycle(options.out/'runs.sqlite','demo-arithmetic',trials,'DEMO: 6 * 7 = 42; no email; no deletion')
    (options.out/'result.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
