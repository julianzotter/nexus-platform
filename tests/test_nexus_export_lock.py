"""Behaviour tests: server-side Drive export hard-lock (Run 1 / Step 1)."""
import hashlib
import sys
import tempfile
import threading
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from deliver_work import DeliveryError, WORK  # noqa: E402
from nexus_export_lock import (ExportLockError, ExportRequest, build_name,  # noqa: E402
                               build_router, export_protocol, http_status)

MD = '---\nname: test\nstatus: ENTWURF\n---\n# Protokoll\n- Punkt\n'
FIXED = datetime(2026, 11, 2, 18, 5, tzinfo=timezone.utc)   # 19:05 Europe/Vienna


class FakeDrive:
    def __init__(self):
        self.files, self.creates, self.corrupt, self.fail_create = {}, 0, False, False

    def find(self, folder, key):
        return [dict(id=k, **v['meta']) for k, v in self.files.items()
                if v['meta']['appProperties']['nexus_delivery_key'] == key
                and folder in v['meta']['parents'] and not v['meta']['trashed']]

    def generate_id(self):
        return f'gen-{len(self.files) + 1}'

    def create(self, file_id, folder, key, name, data):
        if self.fail_create:
            raise DeliveryError('HTTP_403')
        if file_id in self.files:   # Drive answers 409 for a used pre-generated ID; deliver() swallows it
            return
        self.creates += 1
        self.files[file_id] = {'body': data, 'meta': {'name': name, 'trashed': False,
            'parents': [folder], 'appProperties': {'nexus_delivery_key': key}}}

    def metadata(self, file_id):
        return self.files[file_id]['meta']

    def read(self, file_id):
        return b'tampered' if self.corrupt else self.files[file_id]['body']


class Ledger:
    """Key-idempotent, globally monotonic (contract of ArtifactNumberAllocator)."""
    def __init__(self, start=7):
        self.next, self.calls, self.by_key = start, 0, {}

    def allocate(self, key):
        self.calls += 1
        if key not in self.by_key:
            self.by_key[key], self.next = self.next, self.next + 1
        return self.by_key[key]


class ExportLockTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        self.dir, self.drive, self.ledger = Path(tmp.name), FakeDrive(), Ledger()

    def run_export(self, **overrides):
        fields = dict(role_id='ID06', theme='TRANSCRIPT-PROTOKOLL', ticket_id='WO-TEST-1', markdown=MD)
        fields.update(overrides)
        return export_protocol(ExportRequest(**fields), self.drive, self.ledger, self.dir, lambda: FIXED)

    def test_verified_receipt_with_server_built_name(self):
        r = self.run_export()
        self.assertEqual(r.state, 'DELIVERY_VERIFIED')
        self.assertEqual(r.name, '26_11_02_1905_ID06_TRANSCRIPT-PROTOKOLL_007.md')
        self.assertEqual(r.sha256, hashlib.sha256(MD.encode()).hexdigest())
        self.assertEqual(self.drive.files[r.file_id]['meta']['parents'], [WORK])
        self.assertEqual(r.registry_record['artifact_id'], f'gdrive:{r.file_id}')
        self.assertEqual(r.registry_record['registration_status'], 'REGISTRATION_PENDING')
        self.assertEqual(r.human_acceptance, 'PENDING')

    def test_replay_is_idempotent_and_does_not_reallocate(self):
        a, b = self.run_export(), self.run_export()
        self.assertEqual((a.file_id, a.name), (b.file_id, b.name))
        self.assertEqual((self.drive.creates, self.ledger.calls), (1, 1))

    def test_lost_local_state_returns_drive_name_not_new_number(self):
        a = self.run_export()
        for f in self.dir.iterdir():
            f.unlink()
        self.ledger.by_key.clear()
        b = self.run_export()
        self.assertEqual((b.file_id, b.name), (a.file_id, a.name))
        self.assertEqual(self.drive.creates, 1)

    def test_trashed_target_is_not_reused_and_identity_check_fails(self):
        a = self.run_export()
        self.drive.files[a.file_id]['meta']['trashed'] = True
        with self.assertRaisesRegex(ExportLockError, 'TARGET_IDENTITY_CONFLICT'):
            self.run_export()

    def test_renamed_drive_file_is_never_adopted(self):
        a = self.run_export()
        self.drive.files[a.file_id]['meta']['name'] = '../evil name.exe'
        for f in self.dir.iterdir():
            f.unlink()
        with self.assertRaisesRegex(ExportLockError, 'NAME_MISMATCH'):
            self.run_export()

    def test_valid_looking_rename_conflicts_with_sidecar(self):
        a = self.run_export()
        self.drive.files[a.file_id]['meta']['name'] = a.name.replace('_007.md', '_999.md')
        with self.assertRaisesRegex(ExportLockError, 'NAME_MISMATCH'):
            self.run_export()

    def test_crlf_is_normalized_and_flagged(self):
        r = self.run_export(markdown=MD.replace('\n', '\r\n'))
        self.assertTrue(r.line_endings_normalized)
        self.assertEqual(r.sha256, hashlib.sha256(MD.encode()).hexdigest())

    def test_concurrent_identical_requests_create_once(self):
        results, errors = [], []
        def go():
            try:
                results.append(self.run_export())
            except Exception as exc:  # pragma: no cover - surfaced below
                errors.append(exc)
        threads = [threading.Thread(target=go) for _ in range(8)]
        [t.start() for t in threads]; [t.join() for t in threads]
        self.assertEqual(errors, [])
        self.assertEqual({r.file_id for r in results}, {'gen-1'})
        self.assertEqual(self.drive.creates, 1)

    def test_http_status_mapping(self):
        self.assertEqual(http_status('INVALID_THEME'), 422)
        self.assertEqual(http_status('DELIVERY_FAILED:NETWORK_RETRY_EXHAUSTED'), 503)
        self.assertEqual(http_status('DELIVERY_FAILED:HTTP_503'), 503)
        self.assertEqual(http_status('DELIVERY_FAILED:READBACK_HASH_MISMATCH'), 409)
        self.assertEqual(http_status('DELIVERY_FAILED:HTTP_403'), 502)
        self.assertEqual(http_status('DELIVERY_FAILED:BLOCKED_DRIVE_CREDENTIALS'), 503)
        self.assertEqual(http_status('REGISTRY_RECORD_INVALID:x'), 500)

    def test_readback_mismatch_fails_closed(self):
        self.drive.corrupt = True
        with self.assertRaisesRegex(ExportLockError, 'READBACK_HASH_MISMATCH'):
            self.run_export()

    def test_provider_error_fails_closed(self):
        self.drive.fail_create = True
        with self.assertRaisesRegex(ExportLockError, 'DELIVERY_FAILED:HTTP_403'):
            self.run_export()

    def test_client_cannot_choose_folder(self):
        with self.assertRaisesRegex(ExportLockError, 'TARGET_NOT_IN_REGISTRY'):
            self.run_export(target='1j3FLJkWpQv6xGA_KO0D9sMyA11f0vxBV')

    def test_rejects_invalid_role_theme_ticket_and_frontmatter(self):
        cases = [(dict(role_id='ID-CLA'), 'INVALID_ROLE_ID'),
                 (dict(theme='../evil'), 'INVALID_THEME'),
                 (dict(theme='A_B'), 'INVALID_THEME'),
                 (dict(ticket_id=' '), 'TICKET_ID_REQUIRED'),
                 (dict(markdown='# no frontmatter'), 'FRONTMATTER_MISSING'),
                 (dict(markdown=''), 'EMPTY_PAYLOAD')]
        for overrides, code in cases:
            with self.subTest(code=code), self.assertRaisesRegex(ExportLockError, code):
                self.run_export(**overrides)
        self.assertEqual(self.drive.creates, 0)

    def test_name_uses_vienna_time_across_dst(self):
        summer = datetime(2026, 7, 1, 10, 0, tzinfo=timezone.utc)   # UTC+2
        self.assertEqual(build_name('ID03', 'X1', 1, summer), '26_07_01_1200_ID03_X1_001.md')
        with self.assertRaises(ExportLockError):
            build_name('ID03', 'X1', 1000, summer)


try:
    from fastapi import FastAPI, HTTPException
    from fastapi.testclient import TestClient
except ImportError:  # pragma: no cover
    FastAPI = None


@unittest.skipIf(FastAPI is None, 'fastapi not installed')
class RouterTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        self.drive = FakeDrive()

        def principal(request):
            if request.headers.get('x-test-principal') != 'ID06':
                raise HTTPException(status_code=401, detail='UNAUTHENTICATED')
            return 'ID06', 'sess-1'
        app = FastAPI()
        app.include_router(build_router(lambda: self.drive, Ledger(), Path(tmp.name), principal))
        self.client = TestClient(app)

    def post(self, headers=None, **body):
        payload = dict(theme='TRANSCRIPT-PROTOKOLL', ticket_id='WO-TEST-1', markdown=MD); payload.update(body)
        return self.client.post('/api/export/protocol', json=payload, headers={'x-test-principal': 'ID06'} if headers is None else headers)

    def test_valid_post_returns_verified_receipt(self):
        r = self.post()
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(r.json()['state'], 'DELIVERY_VERIFIED')
        self.assertEqual(r.json()['registry_record']['provenance']['role_id'], 'ID06')

    def test_client_role_field_is_ignored_and_auth_required(self):
        self.assertEqual(self.post(headers={}).status_code, 401)
        r = self.post(role_id='ID01')
        self.assertEqual(r.json()['registry_record']['provenance']['role_id'], 'ID06')

    def test_errors_are_mapped(self):
        self.assertEqual(self.post(theme='bad_theme').status_code, 422)
        self.drive.corrupt = True
        self.assertEqual(self.post().status_code, 409)


if __name__ == '__main__':
    unittest.main()
