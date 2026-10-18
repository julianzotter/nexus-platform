import hashlib
import json
import os
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from deliver_work import (DeliveryError, DriveClient, collect_artifacts, deliver,
                          get_access_token, retry, WORK)


class FakeDrive:
    def __init__(self):
        self.files = {}; self.creates = 0; self.ambiguous = False; self.corrupt = False

    def find(self, folder, key):
        return [dict(id=k, **v['meta']) for k, v in self.files.items()
                if key == v['meta']['appProperties']['nexus_delivery_key']]

    def generate_id(self):
        return 'generated-id'

    def create(self, file_id, folder, key, name, data):
        self.creates += 1
        self.files[file_id] = {'body': data, 'meta': {'parents': [folder], 'appProperties': {'nexus_delivery_key': key}}}
        if self.ambiguous:
            raise DeliveryError('NETWORK_RETRY_EXHAUSTED')

    def metadata(self, file_id):
        return self.files[file_id]['meta']

    def read(self, file_id):
        return b'tampered' if self.corrupt else self.files[file_id]['body']


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.journal = Path(self.temp.name) / 'state.json'; self.drive = FakeDrive()

    def send(self, data=b'artifact'):
        return deliver(self.drive, data, WORK, 'repo:1:1:2', 'source.zip', self.journal)

    def test_success_is_byte_verified_not_human_accepted(self):
        receipt = self.send()
        self.assertEqual(receipt['state'], 'DELIVERY_VERIFIED')
        self.assertEqual(receipt['human_acceptance'], 'PENDING')
        self.assertEqual(receipt['consumer_ack'], 'NOT_OBSERVED')

    def test_repeat_reuses_file_and_rechecks_bytes(self):
        self.send(); receipt = self.send()
        self.assertTrue(receipt['reused']); self.assertEqual(self.drive.creates, 1)

    def test_timeout_after_create_recovers_without_second_create(self):
        self.drive.ambiguous = True
        with self.assertRaises(DeliveryError): self.send()
        self.assertTrue(self.journal.is_file())
        self.drive.ambiguous = False; self.send()
        self.assertEqual(self.drive.creates, 1)

    def test_resumed_journal_reuses_preallocated_id(self):
        self.drive.ambiguous = True
        with self.assertRaises(DeliveryError): self.send()
        self.drive.files.clear(); self.drive.ambiguous = False; self.send()
        self.assertEqual(set(self.drive.files), {'generated-id'})

    def test_different_input_cannot_reuse_journal(self):
        self.send()
        with self.assertRaisesRegex(DeliveryError, 'JOURNAL_SOURCE_CONFLICT'): self.send(b'changed')

    def test_corrupt_readback_is_failure(self):
        self.drive.corrupt = True
        with self.assertRaisesRegex(DeliveryError, 'READBACK_HASH_MISMATCH'): self.send()

    def test_duplicates_stop_transfer(self):
        self.send(); self.drive.files['second'] = self.drive.files['generated-id']
        with self.assertRaisesRegex(DeliveryError, 'DUPLICATE_DELIVERY_RECORDS'): self.send()

    def test_wrong_parent_is_not_accepted(self):
        self.send(); self.drive.files['generated-id']['meta']['parents'] = ['other']
        with self.assertRaisesRegex(DeliveryError, 'TARGET_IDENTITY_CONFLICT'): self.send()

    def test_permanent_auth_failure_not_retried(self):
        operation = unittest.mock.Mock(side_effect=urllib.error.HTTPError('url', 403, 'Forbidden', {}, None))
        with self.assertRaisesRegex(DeliveryError, 'HTTP_403'): retry(operation, lambda _: None)
        self.assertEqual(operation.call_count, 1)

    def test_transient_failure_retried_and_recovers(self):
        error = urllib.error.HTTPError('url', 503, 'Unavailable', {}, None)
        operation = unittest.mock.Mock(side_effect=[error, b'ok'])
        self.assertEqual(retry(operation, lambda _: None), b'ok')
        self.assertEqual(operation.call_count, 2)

    def test_network_exhaustion_is_bounded(self):
        operation = unittest.mock.Mock(side_effect=urllib.error.URLError('secret must not leak'))
        with self.assertRaisesRegex(DeliveryError, '^NETWORK_RETRY_EXHAUSTED$'): retry(operation, lambda _: None)
        self.assertEqual(operation.call_count, 3)

    def test_missing_credentials_explicit(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(DeliveryError, 'BLOCKED_DRIVE_CREDENTIALS'): get_access_token()

    def test_untrusted_run_is_rejected(self):
        with patch('deliver_work.gh_json', return_value={'name': 'NEXUS Monitor', 'head_branch': 'attacker', 'status': 'completed'}):
            with self.assertRaisesRegex(DeliveryError, 'UNTRUSTED_SOURCE_RUN'):
                collect_artifacts('julianzotter/nexus-platform', 1)

    def test_drive_search_is_paginated(self):
        client = DriveClient('NEVER_LOG_TEST_TOKEN')
        with patch.object(client, 'call', side_effect=[b'{"files":[{"id":"a"}],"nextPageToken":"p2"}', b'{"files":[{"id":"b"}]}']) as call:
            self.assertEqual(len(client.find(WORK, 'abc')), 2)
            self.assertIn('pageToken=p2', call.call_args.args[0])

    def test_409_alone_does_not_confirm_delivery(self):
        client = DriveClient('TEST_TOKEN')
        with patch.object(client, 'call', side_effect=DeliveryError('HTTP_409')):
            client.create('id', WORK, 'key', 'name', b'data')
        # create can return after 409, but deliver still checks parent/key/media separately.


class RestoreTests(unittest.TestCase):
    def test_restore_only_bounded_state_json_paths(self):
        import io
        import zipfile
        from restore_delivery_state import restore_archive
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, 'w') as archive:
            archive.writestr('state/123.json', json.dumps({'key': 'a' * 64}))
            archive.writestr('../../evil.py', 'bad')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(restore_archive(stream.getvalue(), root), 1)
            self.assertTrue((root / 'state/123.json').exists())
            self.assertFalse((root / 'evil.py').exists())


class TransportBoundaryTests(unittest.TestCase):
    def test_real_http_503_then_success(self):
        from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
        from threading import Thread
        from urllib.request import Request
        from deliver_work import request_bytes
        class Handler(BaseHTTPRequestHandler):
            calls = 0
            def do_GET(self):
                Handler.calls += 1
                self.send_response(503 if Handler.calls == 1 else 200)
                self.end_headers(); self.wfile.write(b'ok')
            def log_message(self, *args):
                pass
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = Thread(target=server.serve_forever, daemon=True); thread.start()
        try:
            request = Request(f'http://127.0.0.1:{server.server_port}/')
            self.assertEqual(retry(lambda: request_bytes(request), lambda _: None), b'ok')
            self.assertEqual(Handler.calls, 2)
        finally:
            server.shutdown(); server.server_close(); thread.join()
