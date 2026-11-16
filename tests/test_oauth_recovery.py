"""OAuth renewal, redaction and failure-preservation regressions; no live credentials."""
import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from configure_drive_oauth import ROOT, cli, main, read_existing, renew_private, write_private
from deliver_work import DeliveryError, get_access_token, retry
from oauth_errors import oauth_request

OLD = {'NEXUS_GOOGLE_CLIENT_ID': 'fixture-client', 'NEXUS_GOOGLE_CLIENT_SECRET': 'fixture-secret',
       'NEXUS_GOOGLE_REFRESH_TOKEN': 'fixture-old-refresh'}
NEW = dict(OLD, NEXUS_GOOGLE_REFRESH_TOKEN='fixture-new-refresh')


def http_error(body: bytes, code: int = 400) -> urllib.error.HTTPError:
    return urllib.error.HTTPError('https://oauth2.googleapis.com/token', code,
                                  'untrusted-service-message', {}, io.BytesIO(body))


class OAuthDiagnosticTests(unittest.TestCase):
    def test_cli_does_not_print_exception_service_text(self):
        with patch('configure_drive_oauth.main', side_effect=RuntimeError('SECRET_SERVICE_TEXT')), \
             patch('builtins.print') as output:
            self.assertEqual(cli(), 2)
        self.assertNotIn('SECRET_SERVICE_TEXT', str(output.call_args))

    def test_allowlisted_error_only_and_no_service_description(self):
        error = http_error(json.dumps({'error': 'invalid_grant',
                                      'error_description': 'SECRET fixture-old-refresh'}).encode())
        with self.assertRaisesRegex(DeliveryError, '^OAUTH_HTTP_400_INVALID_GRANT$'):
            oauth_request(Mock(side_effect=error))

    def test_unknown_error_malformed_and_oversize_bodies_are_not_echoed(self):
        for body in (b'{"error":"SECRET"}', b'not-json SECRET', b'x' * 4097):
            with self.assertRaisesRegex(DeliveryError, '^OAUTH_HTTP_400$'):
                oauth_request(Mock(side_effect=http_error(body)))

    def test_session_control_subtype_is_allowlisted(self):
        body = b'{"error":"invalid_grant","error_subtype":"invalid_rapt"}'
        with self.assertRaisesRegex(DeliveryError, '^OAUTH_HTTP_400_INVALID_GRANT_INVALID_RAPT$'):
            oauth_request(Mock(side_effect=http_error(body)))

    def test_transient_error_is_retried_without_changing_policy(self):
        operation = Mock(side_effect=[http_error(b'SECRET', 503), b'ok'])
        sleep = Mock()
        self.assertEqual(retry(lambda: oauth_request(operation), sleep), b'ok')
        sleep.assert_called_once_with(1)

    def test_token_refresh_reports_sanitized_specific_error(self):
        with patch('deliver_work.request_bytes', side_effect=http_error(b'{"error":"invalid_client"}')):
            with self.assertRaisesRegex(DeliveryError, '^OAUTH_HTTP_400_INVALID_CLIENT$'):
                get_access_token(OLD)


class OAuthRenewalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT)
        self.path = Path(self.tmp.name) / 'drive-oauth.json'
        write_private(self.path, OLD)
        self.before = self.path.read_bytes()

    def tearDown(self):
        self.tmp.cleanup()

    def test_atomic_renewal_preserves_prior_bytes_and_private_permissions(self):
        snapshot = renew_private(self.path, NEW, self.before)
        self.assertEqual(snapshot.read_bytes(), self.before)
        self.assertEqual(read_existing(self.path), NEW)
        self.assertFalse(self.path.with_name(self.path.name + '.renew.lock').exists())
        if os.name != 'nt':
            self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(snapshot.stat().st_mode & 0o777, 0o600)

    def test_changed_file_and_occupied_lock_fail_without_overwrite(self):
        with self.assertRaisesRegex(RuntimeError, 'changed during consent'):
            renew_private(self.path, NEW, b'stale')
        self.assertEqual(self.path.read_bytes(), self.before)
        lock = self.path.with_name(self.path.name + '.renew.lock')
        lock.write_text('another writer')
        with self.assertRaises(FileExistsError):
            renew_private(self.path, NEW, self.before)
        self.assertEqual(self.path.read_bytes(), self.before)
        self.assertEqual(lock.read_text(), 'another writer')

    def test_failed_candidate_does_not_replace_or_publish_and_ignores_access_token(self):
        argv = ['configure_drive_oauth.py', '--renew', '--publish', '--output', str(self.path)]
        with patch('sys.argv', argv), patch.dict(os.environ, {'GOOGLE_ACCESS_TOKEN': 'stale-fixture'}), \
             patch('configure_drive_oauth.authorize_config', return_value=NEW), \
             patch('drive_auth_check.check_access', return_value={'status': 'BLOCKED'}) as check, \
             patch('configure_drive_oauth.publish_secrets') as publish, patch('builtins.print'):
            self.assertEqual(main(), 2)
        check.assert_called_once_with(True, NEW)
        publish.assert_not_called()
        self.assertEqual(self.path.read_bytes(), self.before)

    def test_renew_uses_existing_client_then_validates_and_publishes(self):
        argv = ['configure_drive_oauth.py', '--renew', '--publish', '--output', str(self.path)]
        with patch('sys.argv', argv), patch('configure_drive_oauth.authorize_config', return_value=NEW) as consent, \
             patch('drive_auth_check.check_access', return_value={'status': 'READ_ACCESS_VERIFIED'}), \
             patch('configure_drive_oauth.publish_secrets') as publish, patch('builtins.print'):
            self.assertEqual(main(), 0)
        self.assertEqual(consent.call_args.args[0]['installed']['client_id'], OLD['NEXUS_GOOGLE_CLIENT_ID'])
        publish.assert_called_once_with(NEW)
        self.assertEqual(read_existing(self.path), NEW)

    def test_existing_target_requires_explicit_renew_before_consent(self):
        argv = ['configure_drive_oauth.py', '--client-json', 'unused-client.json', '--output', str(self.path)]
        with patch('sys.argv', argv), patch('configure_drive_oauth.authorize') as consent:
            with self.assertRaisesRegex(ValueError, 'use --renew'):
                main()
        consent.assert_not_called()


if __name__ == '__main__':
    unittest.main()
