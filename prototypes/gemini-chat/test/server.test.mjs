import {test} from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';
import {mkdtemp, rm, readFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import path from 'node:path';
import {createServer, toParts, buildRequest} from '../server.mjs';

const PNG = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';
const listen = srv => new Promise(r => srv.listen(0, '127.0.0.1', () => r(`http://127.0.0.1:${srv.address().port}`)));

// Fake Gemini endpoint emitting the documented SSE shape (GenerateContentResponse per `data:` line).
function fakeGemini({status = 200} = {}) {
  const calls = [];
  const srv = http.createServer(async (req, res) => {
    let body = ''; for await (const c of req) body += c;
    calls.push({url: req.url, key: req.headers['x-goog-api-key'], body: JSON.parse(body)});
    if (status !== 200) { res.writeHead(status, {'content-type': 'application/json'}); return res.end(JSON.stringify({error: {message: 'Resource exhausted'}})); }
    res.writeHead(200, {'content-type': 'text/event-stream'});
    const chunks = [
      {candidates: [{content: {role: 'model', parts: [{text: 'interne Überlegung', thought: true}]}}]},
      {candidates: [{content: {role: 'model', parts: [{text: 'Ein rotes '}]}}]},
      {candidates: [{content: {role: 'model', parts: [{text: 'Pixel.'}]}, finishReason: 'STOP'}],
       usageMetadata: {promptTokenCount: 12, candidatesTokenCount: 3, totalTokenCount: 15}, modelVersion: 'gemini-3.8-flash-001'},
    ];
    for (const c of chunks) { res.write(`data: ${JSON.stringify(c)}\r\n\r\n`); await new Promise(r => setTimeout(r, 5)); }
    res.end();
  });
  return {srv, calls};
}

async function chat(base, id, message, config = {}) {
  const res = await fetch(`${base}/api/sessions/${id}/chat`, {method: 'POST', headers: {'content-type': 'application/json'}, body: JSON.stringify({message, config})});
  const text = await res.text();
  const events = res.headers.get('content-type').includes('event-stream')
    ? text.split('\n\n').filter(Boolean).map(b => ({event: /^event: (.*)$/m.exec(b)[1], data: JSON.parse(/^data: (.*)$/m.exec(b)[1])}))
    : null;
  return {status: res.status, events, json: events ? null : JSON.parse(text)};
}

test('toParts validates images and text', () => {
  assert.deepEqual(toParts({text: 'hi', images: [{mime: 'image/png', data: PNG}]}),
    [{inline_data: {mime_type: 'image/png', data: PNG}}, {text: 'hi'}]);
  assert.throws(() => toParts({text: ''}), /Leere Nachricht/);
  assert.throws(() => toParts({images: [{mime: 'image/gif', data: PNG}]}), /nicht unterstützt/);
  assert.throws(() => toParts({images: [{mime: 'image/png', data: 'not base64!'}]}), /Base64/);
  assert.throws(() => toParts({images: Array(5).fill({mime: 'image/png', data: PNG})}), /Höchstens 4/);
});

test('buildRequest sends optional parameters only when set', () => {
  const h = [{role: 'user', parts: [{text: 'x'}]}];
  assert.deepEqual(buildRequest(h), {contents: h});
  const r = buildRequest(h, {system: 'Sei knapp.', maxOutputTokens: 256, temperature: 0.3});
  assert.deepEqual(r.system_instruction, {parts: [{text: 'Sei knapp.'}]});
  assert.deepEqual(r.generationConfig, {maxOutputTokens: 256, temperature: 0.3});
});

test('streams text, skips thoughts, keeps multimodal history and persists it', async t => {
  const dir = await mkdtemp(path.join(tmpdir(), 'gchat-')); t.after(() => rm(dir, {recursive: true, force: true}));
  const up = fakeGemini(); const upBase = await listen(up.srv); t.after(() => up.srv.close());
  const app = createServer({apiKey: 'test-key', baseUrl: upBase, dataDir: dir}); const base = await listen(app); t.after(() => app.close());

  const first = await chat(base, 'session-0001', {text: 'Was ist das?', images: [{mime: 'image/png', data: PNG}]}, {model: 'gemini-3.8-flash', system: 'Deutsch'});
  assert.equal(first.status, 200);
  assert.deepEqual(first.events.map(e => e.event), ['start', 'delta', 'delta', 'done']);
  assert.equal(first.events.filter(e => e.event === 'delta').map(e => e.data.text).join(''), 'Ein rotes Pixel.');
  assert.equal(first.events.at(-1).data.usage.totalTokenCount, 15);
  assert.equal(up.calls[0].url, '/v1beta/models/gemini-3.8-flash:streamGenerateContent?alt=sse');
  assert.equal(up.calls[0].key, 'test-key');
  assert.deepEqual(up.calls[0].body.contents[0].parts[0], {inline_data: {mime_type: 'image/png', data: PNG}});
  assert.deepEqual(up.calls[0].body.system_instruction, {parts: [{text: 'Deutsch'}]});

  await chat(base, 'session-0001', {text: 'Welche Farbe genau?'});
  assert.deepEqual(up.calls[1].body.contents.map(c => c.role), ['user', 'model', 'user']);
  assert.equal(up.calls[1].body.contents[1].parts[0].text, 'Ein rotes Pixel.');
  assert.ok(up.calls[1].body.contents[0].parts[0].inline_data, 'image stays in history');

  const fresh = createServer({apiKey: 'test-key', baseUrl: upBase, dataDir: dir}); const b2 = await listen(fresh); t.after(() => fresh.close());
  const stored = await (await fetch(`${b2}/api/sessions/session-0001`)).json();
  assert.equal(stored.turns.length, 4);
  assert.equal(stored.turns[1].finishReason, 'STOP');
  assert.ok((await readFile(path.join(dir, 'session-0001.json'), 'utf8')).includes('Welche Farbe genau?'));
});

test('upstream errors are reported and not stored', async t => {
  const dir = await mkdtemp(path.join(tmpdir(), 'gchat-')); t.after(() => rm(dir, {recursive: true, force: true}));
  const up = fakeGemini({status: 429}); const upBase = await listen(up.srv); t.after(() => up.srv.close());
  const app = createServer({apiKey: 'k', baseUrl: upBase, dataDir: dir}); const base = await listen(app); t.after(() => app.close());
  const r = await chat(base, 'session-0002', {text: 'hallo'});
  assert.equal(r.status, 429);
  assert.match(r.json.error, /Resource exhausted/);
  assert.equal((await (await fetch(`${base}/api/sessions/session-0002`)).json()).turns.length, 0);
});

test('missing key, bad ids and key secrecy', async t => {
  const dir = await mkdtemp(path.join(tmpdir(), 'gchat-')); t.after(() => rm(dir, {recursive: true, force: true}));
  const noKey = createServer({apiKey: '', dataDir: dir}); const base = await listen(noKey); t.after(() => noKey.close());
  assert.equal((await chat(base, 'session-0003', {text: 'x'})).status, 503);
  assert.equal((await fetch(`${base}/api/sessions/..%2Fetc`)).status, 400);
  const withKey = createServer({apiKey: 'secret-value', dataDir: dir}); const b2 = await listen(withKey); t.after(() => withKey.close());
  const cfg = await (await fetch(`${b2}/api/config`)).text();
  assert.ok(!cfg.includes('secret-value'));
  const page = await fetch(`${b2}/`);
  assert.match(page.headers.get('content-security-policy'), /connect-src 'self'/);
  assert.ok(!(await page.text()).includes('secret-value'));
});
