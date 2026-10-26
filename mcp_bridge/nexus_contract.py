"""Local policy loading and the adopted WORK Markdown filename contract."""
from __future__ import annotations
import hashlib
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

SOURCE_IDS = {
    'agbs': '10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg',
    'manifest': '1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg',
    'baseline': '1Ig0YFqbWji6B5-oOFcxuVpHb5GEBk0HlbJVz51rf9ho',
    'folder': '11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH',
}

def policy_paths(work: Path, overrides: dict[str, str] | None = None) -> dict[str, str]:
    paths = {'agbs': 'WORK/_AGBS.md', 'folder': 'WORK/Folder.md',
             'manifest': '00_NEXUS_MANIFEST__CURRENT__2026-09-28.md',
             'baseline': '00_NEXUS_BASELINE_INSTRUCTIONS__CURRENT__2026-09-28.md'}
    paths['agbs'] = str(work.relative_to(work.parent) / '_AGBS.md')
    paths['folder'] = str(work.relative_to(work.parent) / 'Folder.md')
    if overrides:
        if set(overrides) - set(paths):
            raise ValueError('UNKNOWN_POLICY_KEY')
        if not all(isinstance(value, str) and value for value in overrides.values()):
            raise ValueError('INVALID_POLICY_PATH_TYPE')
        paths.update(overrides)
    return paths

def read_policy(root: Path, relative: str, max_bytes: int = 200_000) -> dict:
    path = (root / relative).resolve()
    if Path(relative).is_absolute() or root not in path.parents:
        return {'status': 'POLICY_PATH_NOT_ALLOWED'}
    if path.suffix.lower() in {'.gdoc', '.gsheet', '.gslides'}:
        return {'status': 'NATIVE_EXPORT_REQUIRED'}
    if path.suffix.lower() not in {'.md', '.txt'}:
        return {'status': 'POLICY_FORMAT_NOT_ALLOWED'}
    if not path.is_file():
        return {'status': 'MISSING_POLICY', 'relative_path': relative}
    with path.open('rb') as stream:
        data = stream.read(max_bytes + 1)
    if not data or len(data) > max_bytes:
        return {'status': 'EMPTY_OR_OVERSIZED_POLICY', 'relative_path': relative}
    try:
        text = data.decode('utf-8-sig')
    except UnicodeDecodeError:
        return {'status': 'INVALID_POLICY_ENCODING', 'relative_path': relative}
    return {'status': 'LOADED', 'relative_path': relative, 'text': text,
            'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'truncated': False}

def load_governance(work: Path, overrides: dict[str, str] | None = None) -> dict:
    root = work.parent.resolve()
    policies = {}
    for key, relative in policy_paths(work, overrides).items():
        record = read_policy(root, relative)
        policies[key] = dict(record, configured_source_id=SOURCE_IDS[key])
    missing = [key for key, record in policies.items() if record['status'] != 'LOADED']
    return {'state': 'BLOCKED' if missing else 'LOCAL_POLICIES_LOADED',
            'ready': not missing, 'policies': policies, 'missing_or_invalid': missing,
            'authority_verified': False,
            'limitation': 'Local byte receipts do not authenticate Drive identity, adoption or human release.'}

def report_filename(topic: str, artifact_id: str, agent_id: str,
                    observed_at: datetime | None = None) -> str:
    if not re.fullmatch(r'[0-9]{3,}', artifact_id or ''):
        raise ValueError('LEDGER_ARTIFACT_ID_REQUIRED')
    actor = agent_id.replace('ID-', 'ID')
    if not re.fullmatch(r'ID0[1-8]', actor):
        raise ValueError('INVALID_AGENT_ID')
    if not topic.endswith('.md') or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,100}', topic[:-3]):
        raise ValueError('INVALID_MARKDOWN_REPORT_TOPIC')
    moment = observed_at or datetime.now(ZoneInfo('Europe/Vienna'))
    if moment.tzinfo is None:
        raise ValueError('TIMEZONE_AWARE_TIMESTAMP_REQUIRED')
    stamp = moment.astimezone(ZoneInfo('Europe/Vienna')).strftime('%y_%m_%d_%H%M')
    return f'{stamp}_{topic[:-3]}_{artifact_id}_{actor}.md'
