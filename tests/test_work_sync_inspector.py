"""Regression checks for the isolated Control Panel inspector."""
import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

SITE = Path(__file__).resolve().parents[1] / "apps/control-panel/site"


class WorkSyncInspectorTests(unittest.TestCase):
    def test_navigation_and_privacy_boundary(self):
        index = (SITE / "index.html").read_text(encoding="utf-8")
        html = (SITE / "work-sync-inspector.html").read_text(encoding="utf-8")
        self.assertEqual(index.count('href="./work-sync-inspector.html"'), 1)
        self.assertIn('target="_blank" rel="noopener noreferrer">◇ WORK Sync Inspector', index)
        self.assertIn("connect-src 'none'", html)
        self.assertIn("default-src 'none'", html)
        self.assertNotRegex(html, r"\b(?:fetch|XMLHttpRequest|WebSocket|sendBeacon)\s*\(")

    @unittest.skipUnless(shutil.which("node"), "Node.js unavailable")
    def test_byte_gate_and_browser_event_handlers(self):
        html = (SITE / "work-sync-inspector.html").read_text(encoding="utf-8")
        script = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
        harness = r"""
const vm = require('node:vm');
const assert = require('node:assert/strict');
const {webcrypto} = require('node:crypto');
const elements = new Map();
const document = {getElementById(id) {
  if (!elements.has(id)) elements.set(id, {
    files: [], disabled: false, textContent: '', className: '',
    handlers: {}, addEventListener(name, fn) {this.handlers[name] = fn;}
  });
  return elements.get(id);
}};
const ctx = vm.createContext({document, crypto:webcrypto, Uint8Array, Date});
vm.runInContext(JSON.parse(process.argv[1]), ctx);
const e = id => document.getElementById(id);
const file = (name, data) => {
  const bytes = Uint8Array.from(data);
  return {name, size:bytes.byteLength, arrayBuffer:async()=>bytes.buffer};
};
(async()=>{
  e('original').files = [file('original.json',[97,98,99])];
  e('readback').files = [file('readback.json',[97,98,99])];
  await e('compare').handlers.click();
  let result = JSON.parse(e('result').textContent);
  assert.equal(result.original.sha256,'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad');
  assert.equal(result.byte_gate,'PASS');
  assert.equal(result.p0_gate,'BLOCKED');
  assert.equal(result.acl_gate,'NOT_VERIFIED');
  assert.equal(result.p2_gate,'BLOCKED');
  assert.equal(result.release,'NOT_RELEASED');
  assert.equal(e('export').disabled,false);
  e('readback').handlers.change();
  assert.equal(e('export').disabled,true);
  e('readback').files=[file('readback.json',[97,98,100])];
  await e('compare').handlers.click();
  result=JSON.parse(e('result').textContent);
  assert.equal(result.byte_gate,'FAIL');
  assert.equal(result.p0_gate,'FAIL');
  e('readback').files=[file('empty.json',[])];
  await e('compare').handlers.click();
  assert.match(e('result').textContent,/BLOCKED/);
  assert.equal(e('export').disabled,true);
  e('readback').files=[{size:16*1024*1024+1}];
  await e('compare').handlers.click();
  assert.match(e('result').textContent,/BLOCKED/);
  assert.equal(e('export').disabled,true);
  e('folder').files=[{name:'b',webkitRelativePath:'WORK/b',size:2,lastModified:0},{name:'a',webkitRelativePath:'WORK/a',size:1,lastModified:0}];
  e('folder').handlers.change();
  assert.match(e('preview').textContent,/WORK\/a \| 1 B\nWORK\/b \| 2 B/);
  assert.equal(e('snapshot').disabled,false);
})().catch(error=>{console.error(error);process.exitCode=1;});
"""
        subprocess.run(["node", "-e", harness, json.dumps(script)], check=True, timeout=15)


if __name__ == "__main__":
    unittest.main()
