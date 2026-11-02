import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from nexus_folder_index import render, summarize  # noqa: E402

INV = {'observed_at': '2026-11-02', 'scope': 'depth 1',
       'folders': [{'id': 'B', 'name': 'NEXUS.REPORTS'}, {'id': 'A', 'name': 'NEXUS.PDF-RAW'},
                   {'id': 'C', 'name': 'NEXUS.NEW'}],
       'children': [{'parent': 'B', 'title': 'x.md', 'mime': 'text/markdown', 'modified': '2026-10-01'},
                    {'parent': 'B', 'title': 'sub', 'mime': 'application/vnd.google-apps.folder', 'modified': '2026-10-02'},
                    {'parent': 'A', 'title': 'README.md', 'mime': 'text/markdown', 'modified': '2026-09-01'}]}


class FolderIndexTests(unittest.TestCase):
    def test_counts_anchor_and_unclassified(self):
        rows = {r['name']: r for r in summarize(INV)}
        self.assertEqual((rows['NEXUS.REPORTS']['files'], rows['NEXUS.REPORTS']['subfolders']), (1, 1))
        self.assertEqual(rows['NEXUS.REPORTS']['status'], 'NO_ANCHOR')
        self.assertEqual(rows['NEXUS.PDF-RAW']['status'], 'ANCHORED')
        self.assertEqual(rows['NEXUS.NEW']['layer'], 'UNCLASSIFIED')

    def test_render_is_deterministic_with_frontmatter(self):
        a = render(summarize(INV), INV, 'abc', {'name': 'X'})
        b = render(summarize(dict(INV, folders=list(reversed(INV['folders'])))), INV, 'abc', {'name': 'X'})
        self.assertEqual(a, b)
        self.assertTrue(a.startswith('---\nname: X\nsource_inventory_sha256: abc'))
        self.assertIn('folders_without_anchor: 2', a)


if __name__ == '__main__':
    unittest.main()
