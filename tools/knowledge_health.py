#!/usr/bin/env python3
"""Assess knowledge readiness; NO_DATA is never PASS and defaults to exit 2."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAX_AGE_DAYS = 180
SCHEMA = json.loads((ROOT / 'schemas/knowledge-item.schema.json').read_text())
VALIDATOR = jsonschema.Draft202012Validator(SCHEMA, format_checker=jsonschema.FormatChecker())
SEVERITY = {'OK': 0, 'INCOMPLETE': 1, 'STALE': 2, 'BROKEN': 3}


def _parse(ts: Any) -> datetime | None:
    try:
        result = datetime.fromisoformat(str(ts).replace('Z', '+00:00'))
        return result if result.tzinfo is not None else None
    except (ValueError, TypeError):
        return None


def assess_item(item: Any, registry_ids: set[str], now: datetime, max_age_days: int) -> dict:
    """Use the repository schema; a DRAFT is not a released engineering result."""
    findings: list[tuple[str, str]] = []
    for error in VALIDATOR.iter_errors(item):
        findings.append(('BROKEN', error.message))
    if not isinstance(item, dict):
        return {'id': None, 'state': 'BROKEN', 'reasons': ['item must be an object']}
    if item.get('source_file_id') not in registry_ids:
        findings.append(('BROKEN', 'source_file_id not found in file registry'))
    if item.get('status') != 'VALID':
        findings.append(('INCOMPLETE', 'item is not published as VALID'))
    signoff = item.get('signoff')
    if isinstance(signoff, dict):
        if signoff.get('result_version') != item.get('version'):
            findings.append(('STALE', 'sign-off bound to a different version'))
        decided = _parse(signoff.get('decided_at'))
        if decided is None:
            findings.append(('BROKEN', 'sign-off date requires a valid timezone'))
        elif decided > now:
            findings.append(('BROKEN', 'sign-off date is in the future'))
        elif (now - decided).total_seconds() > max_age_days * 86400:
            findings.append(('STALE', f'sign-off older than {max_age_days} days'))
        if signoff.get('decision') != 'APPROVED':
            findings.append(('INCOMPLETE', 'sign-off is not APPROVED'))
    state = max((s for s, _ in findings), key=SEVERITY.get, default='OK')
    return {'id': item.get('id'), 'state': state, 'reasons': [r for _, r in findings]}


def load_registry_ids(path: Path) -> set[str]:
    ids: set[str] = set()
    if not path.is_file():
        raise ValueError('file registry is missing or not a file')
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.strip():
            record = json.loads(line)
            if not isinstance(record, dict) or not isinstance(record.get('id'), str):
                raise ValueError('file registry record requires a string id')
            if record['id'] in ids:
                raise ValueError('duplicate file registry id')
            ids.add(record['id'])
    return ids


def _read_inputs(registry: Path, coverage: Path) -> tuple[set[str], dict, list[str]]:
    errors: list[str] = []
    try:
        ids = load_registry_ids(registry)
    except (OSError, ValueError, TypeError) as exc:
        ids = set()
        errors.append(f'registry: {exc}')
    sources: dict[str, Any] = {}
    try:
        if coverage.is_file():
            raw = json.loads(coverage.read_text(encoding='utf-8'))
            if not isinstance(raw, dict) or not isinstance(raw.get('sources', {}), dict):
                raise ValueError('coverage must contain an object of sources')
            for name, entry in raw.get('sources', {}).items():
                if not isinstance(entry, dict):
                    raise ValueError('coverage source must be an object')
                value = entry.get('coverage_percent')
                if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 100):
                    raise ValueError('coverage percentage must be in [0,100]')
                sources[name] = value if value is not None else 'INCOMPLETE'
    except (OSError, ValueError, TypeError) as exc:
        errors.append(f'coverage: {exc}')
    return ids, sources, errors


def build_report(knowledge_dir: Path, registry: Path, coverage: Path, now: datetime, max_age_days: int) -> dict:
    ids, sources, errors = _read_inputs(registry, coverage)
    results = []
    if knowledge_dir.exists() and not knowledge_dir.is_dir():
        errors.append('knowledge path is not a directory')
    for path in sorted(knowledge_dir.rglob('*.json')) if knowledge_dir.is_dir() else []:
        try:
            item = json.loads(path.read_text(encoding='utf-8'))
            results.append(assess_item(item, ids, now, max_age_days))
        except (OSError, ValueError, TypeError) as exc:
            results.append({'id': path.name, 'state': 'BROKEN', 'reasons': [str(exc)]})
    counts: dict[str, int] = {}
    for result in results:
        counts[result['state']] = counts.get(result['state'], 0) + 1
    bad = bool(errors or counts.get('BROKEN') or counts.get('STALE'))
    status = 'FAIL' if bad else 'NO_DATA' if not results else 'INCOMPLETE' if counts.get('INCOMPLETE') else 'PASS'
    return {'status': status, 'items': len(results), 'registry_items': len(ids), 'counts': counts,
            'healthy_percent': round(100 * counts.get('OK', 0) / len(results), 1) if results else 'INCOMPLETE',
            'coverage': sources, 'input_errors': errors,
            'details': [r for r in results if r['state'] != 'OK'],
            'scope': 'schema, registry references and sign-off metadata; no human identity or live-source authentication'}


def exit_code(report: dict, allow_empty: bool = False, strict: bool = False) -> int:
    if report['status'] == 'FAIL':
        return 1
    if report['status'] == 'NO_DATA':
        return 0 if allow_empty and not strict else 2
    return 2 if strict and report['status'] != 'PASS' else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--knowledge-dir', type=Path, default=ROOT / 'registry/knowledge')
    parser.add_argument('--registry', type=Path, default=ROOT / 'registry/file-registry.jsonl')
    parser.add_argument('--coverage', type=Path, default=ROOT / 'registry/coverage-per-source.json')
    parser.add_argument('--max-age-days', type=int, default=DEFAULT_MAX_AGE_DAYS)
    parser.add_argument('--allow-empty', action='store_true', help='Development only: report NO_DATA but exit 0')
    parser.add_argument('--strict', '--require-data', dest='strict', action='store_true', help='Release gate: only PASS exits 0; --require-data retained as alias')
    args = parser.parse_args()
    if args.max_age_days < 0:
        parser.error('--max-age-days cannot be negative')
    report = build_report(args.knowledge_dir, args.registry, args.coverage, datetime.now(timezone.utc), args.max_age_days)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return exit_code(report, args.allow_empty, args.strict)


if __name__ == '__main__':
    raise SystemExit(main())
