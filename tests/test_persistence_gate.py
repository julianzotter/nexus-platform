import hashlib
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from deliver_work import DeliveryError, WORK, deliver, execute
from persistence_gate import REGISTRY_ID, register_delivery


class Drive:
    def __init__(self):
        self.files = {}; self.registry = b''; self.creates = 0; self.updates = 0
        self.meta_change = False; self.reads = 0; self.registry_conflict = False
        self.timeout_after_update = False; self.corrupt = False

    def generate_id(self):
        return 'id-' + str(self.creates + 1)

    def find(self, folder, key):
        return [dict(id=k) for k, v in self.files.items()
                if v['meta']['appProperties']['nexus_delivery_key'] == key]

    def create(self, file_id, folder, key, name, data):
        self.creates += 1
        self.files[file_id] = {'data': data, 'meta': dict(id=file_id, name=name,
            mimeType='application/octet-stream', size=str(len(data)), version='1',
            modifiedTime='2026-11-02T18:00:00Z', parents=[folder], trashed=False,
            appProperties={'nexus_delivery_key': key})}

    def metadata(self, file_id):
        meta = dict(self.files[file_id]['meta'])
        if self.meta_change:
            self.files[file_id]['meta']['version'] = str(int(meta['version']) + 1)
        return meta

    def read(self, file_id):
        if file_id == REGISTRY_ID:
            self.reads += 1
            if self.registry_conflict and self.reads == 2:
                self.registry += b'{"artifact_id":"another"}\n'
            return self.registry
        return b'corrupt' if self.corrupt else self.files[file_id]['data']

    def replace(self, file_id, data, mime):
        assert file_id == REGISTRY_ID
        self.updates += 1; self.registry = data
        if self.timeout_after_update:
            raise DeliveryError('NETWORK_RETRY_EXHAUSTED')


class PersistenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.journal = Path(self.tmp.name) / 'journal.json'
        self.drive = Drive(); self.body = 'ä\r\nß\n'.encode()
        self.receipt = deliver(self.drive, self.body, WORK, 'operation', 'file.zip', self.journal)

    def register(self, mode='exclusive-writer'):
        return register_delivery(self.drive, self.receipt, self.body, 'file.zip',
                                 'application/octet-stream', 'WO-TEST', 'ID01', mode)

    def test_success_requires_file_and_registry_readbacks(self):
        result = self.register()
        self.assertEqual(result['state'], 'PERSISTED_VERIFIED')
        self.assertEqual(result['human_acceptance'], 'PENDING')
        event = json.loads(self.drive.registry)
        self.assertEqual(event['content_sha256'], hashlib.sha256(self.body).hexdigest())
        self.assertEqual(event['provider_version'], '1')

    def test_repeat_is_idempotent(self):
        self.register(); before = self.drive.registry
        self.register()
        self.assertEqual(self.drive.registry, before)
        self.assertEqual(self.drive.updates, 1)

    def test_missing_registration_timestamp_is_not_accepted(self):
        self.register()
        event = json.loads(self.drive.registry); event.pop('registered_at')
        self.drive.registry = json.dumps(event).encode() + b'\n'
        self.assertEqual(self.register('read-only')['state'], 'FILE_VERIFIED')

    def test_permission_failure_remains_explicit(self):
        with patch.object(self.drive, 'replace', side_effect=DeliveryError('HTTP_403')):
            result = self.register()
        self.assertEqual(result['registration_error'], 'HTTP_403')

    def test_registry_timeout_without_write_is_not_success(self):
        with patch.object(self.drive, 'replace', side_effect=DeliveryError('NETWORK_RETRY_EXHAUSTED')):
            result = self.register()
        self.assertEqual(result['state'], 'FILE_VERIFIED')
        self.assertEqual(result['registration_error'], 'REGISTRY_WRITE_OUTCOME_UNKNOWN')

    def test_read_only_keeps_communication_partial(self):
        result = self.register('read-only')
        self.assertEqual(result['state'], 'FILE_VERIFIED')
        self.assertEqual(result['registration_status'], 'REGISTRATION_PENDING')
        self.assertEqual(self.drive.updates, 0)

    def test_metadata_identity_failures(self):
        for key, wrong in [('id', 'old'), ('name', 'other'), ('mimeType', 'text/plain'),
                           ('size', '999'), ('parents', ['wrong']), ('trashed', True),
                           ('version', None), ('modifiedTime', None)]:
            with self.subTest(key=key):
                meta = self.drive.files['id-1']['meta']; before = dict(meta); meta[key] = wrong
                with self.assertRaisesRegex(DeliveryError, 'TARGET_IDENTITY_CONFLICT'):
                    self.register()
                self.drive.files['id-1']['meta'] = before

    def test_changing_version_blocks(self):
        self.drive.meta_change = True
        with self.assertRaisesRegex(DeliveryError, 'TARGET_VERSION_CONFLICT'): self.register()

    def test_corrupt_bytes_block(self):
        self.drive.corrupt = True
        with self.assertRaisesRegex(DeliveryError, 'READBACK_HASH_MISMATCH'): self.register()

    def test_operation_binding_blocks_forged_receipt(self):
        self.receipt['key'] = 'fabricated'
        with self.assertRaisesRegex(DeliveryError, 'DELIVERY_OPERATION_CONFLICT'): self.register()

    def test_no_delivery_status_blocks(self):
        self.receipt['state'] = 'LOCAL_ONLY'
        with self.assertRaisesRegex(DeliveryError, 'UNVERIFIED_DELIVERY'): self.register()

    def test_registry_conflict_preserves_partial_status(self):
        self.drive.registry_conflict = True
        result = self.register()
        self.assertEqual(result['registration_error'], 'REGISTRY_SOURCE_CONFLICT')
        self.assertEqual(self.drive.updates, 0)

    def test_timeout_after_registry_write_is_reconciled(self):
        self.drive.timeout_after_update = True
        self.assertEqual(self.register()['state'], 'PERSISTED_VERIFIED')
        self.assertEqual(self.drive.updates, 1)

    def test_old_registry_bytes_are_preserved(self):
        old = b'{"historical":true}'
        self.drive.registry = old
        self.register()
        self.assertTrue(self.drive.registry.startswith(old + b'\n'))

    def test_malformed_registry_does_not_block_file_evidence(self):
        self.drive.registry = b'not-json'
        result = self.register()
        self.assertEqual(result['state'], 'FILE_VERIFIED')
        self.assertEqual(result['registration_error'], 'REGISTRY_INVALID_JSONL')

    def test_changed_name_cannot_reuse_journal(self):
        with self.assertRaisesRegex(DeliveryError, 'JOURNAL_SOURCE_CONFLICT'):
            deliver(self.drive, self.body, WORK, 'operation', 'other.zip', self.journal)

    def test_cli_execute_calls_real_registration_path(self):
        from argparse import Namespace
        args = Namespace(repo='julianzotter/nexus-platform', run_id=1, folder=WORK,
                         register=True, ticket_id='WO-TEST', owner='ID01',
                         registry_write_mode='exclusive-writer')
        run = dict(id=1, run_attempt=1, head_sha='a'*40, html_url='https://github.com/run')
        artifact = dict(id=7, digest='sha256:' + hashlib.sha256(self.body).hexdigest())
        with patch('deliver_work.collect_artifacts', return_value=(run, [artifact])), \
             patch('deliver_work.download_artifact', return_value=self.body), \
             patch('deliver_work.get_access_token', return_value='TEST'), \
             patch('deliver_work.DriveClient', return_value=self.drive):
            result = execute(args, Path(self.tmp.name))
            self.drive.registry += b'{"artifact_id":"unrelated","operation_id":"different"}\n'
            repeated = execute(args, Path(self.tmp.name))
        self.assertEqual(result['status'], 'PERSISTED_VERIFIED')
        self.assertEqual(repeated['status'], 'PERSISTED_VERIFIED')
        self.assertEqual(len(result['deliveries']), 2)
        self.assertEqual(len(self.drive.registry.splitlines()), 3)
        self.assertEqual(self.drive.creates, 3)  # setUp file + payload + receipt


if __name__ == '__main__':
    unittest.main()
