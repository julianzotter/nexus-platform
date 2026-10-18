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
