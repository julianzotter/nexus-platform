"""Offline contracts; no real credentials, API calls or store mutations."""
import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'orchestrator'))
from nexus_orch.credentials import CredentialError,resolve_key
from nexus_orch.deepseek import DeepSeekError,complete,models_probe,request_json
from nexus_orch.providers import Provider,ProviderError
CFG=json.loads((ROOT/'orchestrator/config/routing.json').read_text())

class DeepSeekContracts(unittest.TestCase):
    def test_routing_references_and_private_route(self):
        for route in CFG['routes'].values():
            self.assertTrue(set([route['primary'],*route.get('fallback',[])])<=set(CFG['providers']))
        self.assertEqual(CFG['routes']['private'],{'primary':'local','fallback':[]})
        self.assertEqual(CFG['routes']['deepseek_chat']['fallback'],[])
    def test_explicit_thinking_modes_no_temperature(self):
        response={'choices':[{'finish_reason':'stop','message':{'content':'OK'}}]}
        for name,mode,effort in [('deepseek','disabled','none'),('deepseek_review','enabled','high')]:
            with patch('nexus_orch.deepseek.request_json',return_value=response) as call:
                self.assertEqual(complete(CFG['providers'][name],'Q','','fixture')['text'],'OK')
                body=call.call_args.args[2]
                self.assertEqual(body['thinking']['type'],mode)
                self.assertEqual(body['reasoning_effort'],effort)
                self.assertNotIn('temperature',body)
    def test_missing_mode_or_incomplete_response(self):
        cfg={**CFG['providers']['deepseek'],'thinking':{}}
        with self.assertRaises(DeepSeekError):complete(cfg,'Q','','fixture')
        with patch('nexus_orch.deepseek.request_json',return_value={'choices':[{'finish_reason':'length','message':{'content':'partial'}}]}):
            with self.assertRaises(DeepSeekError):complete(CFG['providers']['deepseek'],'Q','','fixture')
    def test_models_200_and_401(self):
        with patch('nexus_orch.deepseek.resolve_key',return_value='fixture'),patch('nexus_orch.deepseek.request_json',return_value={'data':[{'id':'deepseek-flash'}]}):
            self.assertEqual(models_probe()['http_status'],200)
        with patch('nexus_orch.deepseek.resolve_key',return_value='fixture'),patch('nexus_orch.deepseek.request_json',side_effect=DeepSeekError('DEEPSEEK_HTTP_401')):
            self.assertEqual(models_probe()['http_status'],401)
    def test_provider_uses_adapter(self):
        with patch.dict(os.environ,{'DEEPSEEK_API_KEY':'fixture'}),patch('nexus_orch.deepseek.complete',return_value={'text':'OK'}) as call:
            self.assertEqual(Provider('deepseek',CFG['providers']['deepseek']).complete('Q')['text'],'OK')
            self.assertEqual(call.call_args.args[-1],'fixture')
    def test_dsh_safe_scalar_and_mode(self):
        with tempfile.TemporaryDirectory() as d,patch.dict(os.environ,{},clear=True):
            p=Path(d)/'.credentials.yaml';p.write_text('DEEPSEEK_API_KEY: fixture-not-a-real-key\n');p.chmod(0o600)
            self.assertEqual(resolve_key('DEEPSEEK_API_KEY','dsh',p),'fixture-not-a-real-key')
            p.chmod(0o644)
            if os.name!='nt':
                with self.assertRaises(CredentialError):resolve_key('DEEPSEEK_API_KEY','dsh',p)
    def test_dsh_schema_not_guessed(self):
        with tempfile.TemporaryDirectory() as d,patch.dict(os.environ,{},clear=True):
            p=Path(d)/'.credentials.yaml';p.write_text('providers:\n  deepseek: fixture\n');p.chmod(0o600)
            with self.assertRaises(CredentialError):resolve_key('DEEPSEEK_API_KEY','dsh',p)
    def test_http_error_body_redacted(self):
        fake=urllib.error.HTTPError('https://api.deepseek.com/models',401,'fail',{},io.BytesIO(b'fixture-secret-must-not-leak'))
        with patch('urllib.request.OpenerDirector.open',side_effect=fake):
            with self.assertRaises(DeepSeekError) as e:request_json('/models','fixture')
            self.assertEqual(str(e.exception),'DEEPSEEK_HTTP_401')
    def test_no_credential_storage_and_sandbox(self):
        s=(ROOT/'prototypes/vibe-coder-v2.3/index.html').read_text()
        self.assertNotIn("localStorage.setItem('vc_apikey_",s)
        self.assertNotIn("localStorage.getItem('vc_apikey_",s)
        self.assertIn('sandbox="allow-scripts"',s)
        self.assertIn("localStorage.removeItem(k)",s)

if __name__=='__main__':unittest.main()
