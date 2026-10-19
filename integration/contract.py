"""Portable, read-only registry/dashboard contract. No release authority."""
import json
from datetime import datetime
from pathlib import Path
import jsonschema

SCHEMA = json.loads((Path(__file__).with_name('snapshot.schema.json')).read_text(encoding='utf-8'))
VALIDATOR = jsonschema.Draft202012Validator(SCHEMA, format_checker=jsonschema.FormatChecker())

def validate(snapshot):
    VALIDATOR.validate(snapshot)
    for value in [snapshot['generated_at']] + ([snapshot['monitor']['observed_at']] if snapshot['monitor'] else []):
        if datetime.fromisoformat(value.replace('Z', '+00:00')).utcoffset() is None:
            raise ValueError('Timezone required')
    ids = [entry['record']['id'] for entry in snapshot['knowledge']]
    if len(ids) != len(set(ids)) or any(not value.strip() for value in ids):
        raise ValueError('Duplicate or empty knowledge ID')
    paths = [entry['path'] for entry in snapshot['source']['files']]
    if len(paths) != len(set(paths)):
        raise ValueError('Duplicate source path')
    if snapshot['monitor'] is not None and snapshot['monitor']['commit'] != snapshot['source']['revision']:
        raise ValueError('Monitor revision differs from registry revision')
    return snapshot

def graph(snapshot):
    validate(snapshot)
    return {
        'schema_version': snapshot['schema_version'],
        'generated_at': snapshot['generated_at'], 'source': snapshot['source'],
        'monitor': snapshot['monitor'], 'limitations': snapshot['limitations'],
        'nodes': [{'id': e['record']['id'], 'title': e['record']['title'],
                   'domain': e['record']['kind'], 'status': e['record']['status'],
                   'health': e['health'], 'source_file_id': e['record']['source_file_id'],
                   'record': e['record']} for e in snapshot['knowledge']],
        'edges': [],
        'release_authority': False,
    }
