import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from drive_changes_poll import in_scope, poll

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
