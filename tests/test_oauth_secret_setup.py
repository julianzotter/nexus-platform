import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from configure_drive_oauth import publish_secrets


class SecretSetupTests(unittest.TestCase):
    def test_secret_is_stdin_not_command_argument(self):
        with patch('configure_drive_oauth.subprocess.run', return_value=Mock(returncode=0)) as run, patch('builtins.print'):
            publish_secrets({'OPENAI_API_KEY': 'TEST_FIXTURE_SECRET'})
            args, kwargs = run.call_args
            self.assertNotIn('TEST_FIXTURE_SECRET', ' '.join(args[0]))
            self.assertEqual(kwargs['input'], b'TEST_FIXTURE_SECRET')

    def test_bad_auth_prevents_secret_write(self):
        with patch('configure_drive_oauth.subprocess.run', return_value=Mock(returncode=1)) as run:
            with self.assertRaisesRegex(RuntimeError, 'authentication required'):
                publish_secrets({'OPENAI_API_KEY': 'TEST_FIXTURE_SECRET'})
            self.assertEqual(run.call_count, 1)

    def test_unknown_secret_and_multiline_rejected(self):
        for data in [{'UNKNOWN': 'x'}, {'OPENAI_API_KEY': 'a\nb'}]:
            with self.assertRaises(ValueError): publish_secrets(data)


class ExistingCredentialTests(unittest.TestCase):
    def test_rejects_public_readable_or_wrong_credential_set(self):
        import json, os, tempfile
        from configure_drive_oauth import read_existing
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as td:
            path = Path(td) / 'private.json'
            path.write_text(json.dumps({'UNKNOWN': 'fixture'}))
            path.chmod(0o600)
            with self.assertRaises(ValueError):
                read_existing(path)
            if os.name != 'nt':
                path.chmod(0o644)
                with self.assertRaisesRegex(ValueError, 'owner-only'):
                    read_existing(path)

    def test_check_does_not_publish_or_request_consent(self):
        from configure_drive_oauth import main
        with patch('sys.argv', ['configure_drive_oauth.py', '--check']), \
             patch('drive_auth_check.check_access', return_value={'status': 'BLOCKED'}) as check, \
             patch('configure_drive_oauth.publish_secrets') as publish, \
             patch('configure_drive_oauth.authorize') as authorize, patch('builtins.print'):
            self.assertEqual(main(), 2)
        publish.assert_not_called()
        authorize.assert_not_called()
        check.assert_called_once()
