import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from drive_changes_poll import in_scope, poll
import drive_changes_poll as polling

TREE = {'sub': ['WORKID'], 'deep': ['sub'], 'other': ['root'], 'root': []}


class FakeReader:
    def __init__(self, pages):
        self.pages = pages; self.lookups = 0

    def start_token(self):
        return 't0'

    def changes(self, token):
        return self.pages[token]

    def parents(self, fid):
        self.lookups += 1
        return TREE.get(fid, [])


class PollTest(unittest.TestCase):
    def run_main(self, root: Path) -> int:
        args = ['poll', '--state', str(root / 'state.json'), '--out', str(root / 'reports')]
        with patch.object(sys, 'argv', args), contextlib.redirect_stdout(io.StringIO()):
            return polling.main()

    def test_missing_credentials_fail_and_preserve_checkpoint(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkpoint = '{"page_token": "unchanged"}'
            (root / 'state.json').write_text(checkpoint)
            with patch.object(polling, 'get_access_token', side_effect=polling.DeliveryError(
                    'BLOCKED_DRIVE_CREDENTIALS')):
                self.assertEqual(self.run_main(root), 2)
            report = json.loads((root / 'reports/status.json').read_text())
            self.assertEqual(report['status'], 'BLOCKED')
            self.assertEqual(report['reason'], 'BLOCKED_DRIVE_CREDENTIALS')
            self.assertEqual((root / 'state.json').read_text(), checkpoint)
            self.assertFalse((root / 'reports/changes.json').exists())

    def test_success_writes_events_and_advances_checkpoint(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(polling, 'get_access_token', return_value='test-only'), patch.object(
                    polling, 'poll', return_value=([{'file_id': 'f'}], {
                        'page_token': 'next', 'initialized': False})):
                self.assertEqual(self.run_main(root), 0)
            self.assertEqual(json.loads((root / 'reports/status.json').read_text())['status'], 'OK')
            self.assertEqual(json.loads((root / 'state.json').read_text())['page_token'], 'next')
            self.assertEqual(json.loads((root / 'reports/changes.json').read_text()), [{'file_id': 'f'}])

    def test_first_run_only_initializes(self):
        events, state = poll(FakeReader({}), {}, {'WORKID'})
        self.assertEqual((events, state['page_token'], state['initialized']), ([], 't0', True))

    def test_scoped_changes_and_pagination(self):
        pages = {
            't1': {'nextPageToken': 't2', 'changes': [
                {'file': {'id': 'a', 'name': 'in.md', 'parents': ['deep']}, 'time': 'T'},
                {'file': {'id': 'b', 'name': 'out.md', 'parents': ['other']}}]},
            't2': {'newStartPageToken': 't3', 'changes': [
                {'fileId': 'c', 'removed': True},
                {'file': {'id': 'd', 'name': 'direct.md', 'parents': ['WORKID']}}]}}
        events, state = poll(FakeReader(pages), {'page_token': 't1'}, {'WORKID'})
        self.assertEqual([e['name'] for e in events], ['in.md', 'direct.md'])
        self.assertEqual(state['page_token'], 't3')

    def test_cycle_safe(self):
        TREE['loop'] = ['loop']
        self.assertFalse(in_scope({'parents': ['loop']}, {'WORKID'}, FakeReader({}).parents, {}))


if __name__ == '__main__':
    unittest.main()
