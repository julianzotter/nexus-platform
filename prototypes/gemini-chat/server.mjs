// NEXUS multimodal chat: local proxy to the Gemini API (streamGenerateContent, SSE).
// The API key stays in this process; the browser never sees it. Zero dependencies (Node >= 20).
import http from 'node:http';
import {readFile, writeFile, mkdir, rm} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';

const HERE = path.dirname(fileURLToPath(import.meta.url));
export const MODELS = ['gemini-3.8-flash', 'gemini-3.5-flash-lite', 'gemini-4-argon'];
const IMAGE_TYPES = new Set(['image/png', 'image/jpeg', 'image/webp', 'image/heic', 'image/heif']);
const LIMITS = {bodyBytes: 18 * 1024 * 1024, images: 4, imageBytes: 6 * 1024 * 1024, textChars: 32000, turns: 200};
const SESSION_ID = /^[a-z0-9-]{8,64}$/;
const MODEL_ID = /^[a-z0-9][a-z0-9.\-]{2,63}$/;

function json(res, status, body) {
  res.writeHead(status, {'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store'});
  res.end(JSON.stringify(body));
}
async function readBody(req, limit) {
  const chunks = []; let size = 0;
  for await (const c of req) { size += c.length; if (size > limit) throw Object.assign(new Error('Anfrage zu groß'), {status: 413}); chunks.push(c); }
  return JSON.parse(Buffer.concat(chunks).toString('utf8') || '{}');
}

// Validates one user turn from the browser; returns Gemini `parts`.
export function toParts(message) {
  const text = typeof message?.text === 'string' ? message.text.slice(0, LIMITS.textChars) : '';
  const images = Array.isArray(message?.images) ? message.images : [];
  if (images.length > LIMITS.images) throw Object.assign(new Error(`Höchstens ${LIMITS.images} Bilder pro Nachricht`), {status: 400});
  const parts = images.map(img => {
    if (!IMAGE_TYPES.has(img?.mime)) throw Object.assign(new Error(`Bildformat nicht unterstützt: ${img?.mime}`), {status: 400});
    if (typeof img.data !== 'string' || !/^[A-Za-z0-9+/]+={0,2}$/.test(img.data)) throw Object.assign(new Error('Bilddaten sind kein Base64'), {status: 400});
    if (img.data.length * 3 / 4 > LIMITS.imageBytes) throw Object.assign(new Error('Bild größer als 6 MB'), {status: 413});
    return {inline_data: {mime_type: img.mime, data: img.data}};
  });
  if (text.trim()) parts.push({text});
  if (!parts.length) throw Object.assign(new Error('Leere Nachricht'), {status: 400});
  return parts;
}

export function buildRequest(history, config = {}) {
  const body = {contents: history.map(t => ({role: t.role, parts: t.parts}))};
  if (config.system?.trim()) body.system_instruction = {parts: [{text: config.system.slice(0, 8000)}]};
  const gen = {};
  if (Number.isFinite(config.maxOutputTokens)) gen.maxOutputTokens = Math.max(1, Math.min(65536, Math.round(config.maxOutputTokens)));
  // Gemini 3.6+ and 4 ignore temperature; only sent when the user sets it explicitly.
  if (Number.isFinite(config.temperature)) gen.temperature = Math.max(0, Math.min(2, config.temperature));
  if (Object.keys(gen).length) body.generationConfig = gen;
  return body;
}

// Parses an SSE byte stream from Gemini; yields GenerateContentResponse objects.
export async function* sseEvents(stream) {
  const decoder = new TextDecoder(); let buf = '';
  for await (const chunk of stream) {
    buf += decoder.decode(chunk, {stream: true});
    let idx;
    while ((idx = buf.search(/\r?\n\r?\n/)) >= 0) {
      const block = buf.slice(0, idx); buf = buf.slice(idx).replace(/^\r?\n\r?\n/, '');
      const data = block.split(/\r?\n/).filter(l => l.startsWith('data:')).map(l => l.slice(5).trimStart()).join('\n');
      if (data && data !== '[DONE]') yield JSON.parse(data);
    }
  }
}

class Sessions {
  constructor(dir) { this.dir = dir; this.cache = new Map(); }
  file(id) { return path.join(this.dir, id + '.json'); }
  async get(id) {
    if (this.cache.has(id)) return this.cache.get(id);
    let s; try { s = JSON.parse(await readFile(this.file(id), 'utf8')); } catch { s = {id, created: new Date().toISOString(), turns: []}; }
    this.cache.set(id, s); return s;
  }
  async save(s) { await mkdir(this.dir, {recursive: true}); s.updated = new Date().toISOString(); await writeFile(this.file(s.id), JSON.stringify(s), 'utf8'); }
  async drop(id) { this.cache.delete(id); await rm(this.file(id), {force: true}); }
}

export function createServer({apiKey = process.env.GEMINI_API_KEY, baseUrl = process.env.GEMINI_BASE_URL || 'https://generativelanguage.googleapis.com',
                              dataDir = path.join(HERE, '.sessions'), defaultModel = process.env.GEMINI_MODEL || MODELS[0]} = {}) {
  const sessions = new Sessions(dataDir);
  const busy = new Set();

  async function chat(req, res, id) {
    if (!apiKey) return json(res, 503, {error: 'GEMINI_API_KEY ist auf dem Server nicht gesetzt.'});
    if (busy.has(id)) return json(res, 409, {error: 'In dieser Sitzung läuft bereits eine Antwort.'});
    const body = await readBody(req, LIMITS.bodyBytes);
    const parts = toParts(body.message);
    const config = body.config || {};
    const model = MODEL_ID.test(config.model || '') ? config.model : defaultModel;
    const session = await sessions.get(id);
    if (session.turns.length >= LIMITS.turns) return json(res, 400, {error: 'Sitzung ist voll. Bitte neuen Chat beginnen.'});
    const userTurn = {role: 'user', parts, at: new Date().toISOString()};
    const history = [...session.turns, userTurn];

    busy.add(id);
    const upstreamAbort = new AbortController();
    res.on('close', () => { if (!res.writableFinished) upstreamAbort.abort(); });
    const send = (event, data) => res.write(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`);
    let text = '', usage = null, finishReason = null, modelVersion = null;
    try {
      const upstream = await fetch(`${baseUrl}/v1beta/models/${encodeURIComponent(model)}:streamGenerateContent?alt=sse`, {
        method: 'POST', signal: upstreamAbort.signal,
        headers: {'content-type': 'application/json', 'x-goog-api-key': apiKey},
        body: JSON.stringify(buildRequest(history, config)),
      });
      if (!upstream.ok) {
        const err = await upstream.json().catch(() => ({}));
        return json(res, upstream.status === 429 ? 429 : 502, {error: `Gemini ${upstream.status}: ${err.error?.message || upstream.statusText}`});
      }
      res.writeHead(200, {'content-type': 'text/event-stream; charset=utf-8', 'cache-control': 'no-store', connection: 'keep-alive'});
      send('start', {model});
      for await (const ev of sseEvents(upstream.body)) {
        const cand = ev.candidates?.[0];
        for (const p of cand?.content?.parts || []) if (typeof p.text === 'string' && !p.thought) { text += p.text; send('delta', {text: p.text}); }
        if (cand?.finishReason) finishReason = cand.finishReason;
        if (ev.promptFeedback?.blockReason) finishReason = 'BLOCKED: ' + ev.promptFeedback.blockReason;
        if (ev.usageMetadata) usage = ev.usageMetadata;
        if (ev.modelVersion) modelVersion = ev.modelVersion;
      }
      // the turn pair is stored only after a complete answer, so history never holds a dangling user turn
      session.turns.push(userTurn, {role: 'model', parts: [{text}], at: new Date().toISOString(), model: modelVersion || model, finishReason, usage});
      await sessions.save(session);
      send('done', {finishReason, usage, model: modelVersion || model});
      res.end();
    } catch (e) {
      if (upstreamAbort.signal.aborted) return;
      if (!res.headersSent) return json(res, 502, {error: 'Verbindung zu Gemini fehlgeschlagen: ' + e.message});
      send('error', {error: e.message}); res.end();
    } finally { busy.delete(id); }
  }

  return http.createServer(async (req, res) => {
    try {
      const url = new URL(req.url, 'http://local');
      const m = url.pathname.match(/^\/api\/sessions\/([^/]+)(\/chat)?$/);
      if (req.method === 'GET' && (url.pathname === '/' || url.pathname === '/index.html')) {
        res.writeHead(200, {'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store',
          'content-security-policy': "default-src 'self'; img-src 'self' data: blob:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; connect-src 'self'"});
        return res.end(await readFile(path.join(HERE, 'index.html')));
      }
      if (req.method === 'GET' && url.pathname === '/api/config') return json(res, 200, {hasKey: Boolean(apiKey), models: MODELS, defaultModel, limits: LIMITS});
      if (m) {
        if (!SESSION_ID.test(m[1])) return json(res, 400, {error: 'Ungültige Sitzungs-ID'});
        if (m[2] && req.method === 'POST') return await chat(req, res, m[1]);
        if (!m[2] && req.method === 'GET') return json(res, 200, await sessions.get(m[1]));
        if (!m[2] && req.method === 'DELETE') { await sessions.drop(m[1]); return json(res, 200, {ok: true}); }
      }
      json(res, 404, {error: 'Nicht gefunden'});
    } catch (e) {
      if (!res.headersSent) json(res, e.status || (e instanceof SyntaxError ? 400 : 500), {error: e.message}); else res.end();
    }
  });
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const port = Number(process.env.PORT) || 8787;
  createServer().listen(port, '127.0.0.1', () => {
    console.log(`NEXUS Gemini-Chat: http://127.0.0.1:${port}  (Key ${process.env.GEMINI_API_KEY ? 'gesetzt' : 'FEHLT: GEMINI_API_KEY setzen'})`);
  });
}
