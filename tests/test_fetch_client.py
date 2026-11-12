import importlib.util
import os
import unittest
from pathlib import Path
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('bounded_fetch',Path(__file__).resolve().parents[1]/'integrations/deepseek-clients/fetch.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class FetchContracts(unittest.TestCase):
    def test_url_and_receipt(self):
        url='https://api-docs.deepseek.com/api/fetch/'
        self.assertEqual(m.checked_url(url,[]),url)
        self.assertEqual(len(m.normalize({'title':'Test','content':'# Test'},url)['sha256']),64)
    def test_boundaries(self):
        for url in ['https://127.0.0.1/','https://localhost/','https://unknown.example/','https://api-docs.deepseek.com/?token=x']:
            with self.assertRaises((m.Blocked,ValueError)):m.checked_url(url,[])
        for response in [{'title':'Test','content':''},{'title':'Test','content':'x','truncated':True}]:
            with self.assertRaises(m.Blocked):m.normalize(response,'https://api-docs.deepseek.com/')
    def test_no_key_no_request(self):
        with patch.dict(os.environ,{},clear=True),patch('urllib.request.build_opener') as network:
            with self.assertRaises(m.Blocked):m.fetch('https://api-docs.deepseek.com/',30)
            network.assert_not_called()
if __name__=='__main__':unittest.main()
