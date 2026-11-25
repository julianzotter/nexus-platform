"use strict";
// NEXUS CONTROL TOWER client. No external scripts, textContent only, token in sessionStorage.
(function () {
  const KEY = "nexus_tower_token";
  const m = location.hash.match(/[#&]t=([0-9a-f]{32,})/);
  if (m) { sessionStorage.setItem(KEY, m[1]); history.replaceState(null, "", location.pathname); }
  let token = sessionStorage.getItem(KEY) || "";
  const $ = (id) => document.getElementById(id);
  const el = (tag, text, cls) => { const e = document.createElement(tag); if (text !== undefined && text !== null) e.textContent = String(text); if (cls) e.className = cls; return e; };
  const fmtUp = (s) => { if (!s) return "-"; const h = Math.floor(s / 3600), mi = Math.floor((s % 3600) / 60); return h ? `${h}h ${mi}m` : `${mi}m ${s % 60}s`; };
  const short = (t) => (t ? String(t).replace("T", " ").slice(0, 19) : "-");

  async function api(path, body) {
    const opt = { headers: { Authorization: "Bearer " + token }, cache: "no-store" };
    if (body) { opt.method = "POST"; opt.headers["Content-Type"] = "application/json"; opt.body = JSON.stringify(body); }
    const r = await fetch(path, opt);
    if (r.status === 401) { showLogin(true); throw new Error("401"); }
    return r.json();
  }
  function showLogin(on) { $("login").classList.toggle("hidden", !on); }
  $("tokbtn").addEventListener("click", () => { token = $("tok").value.trim(); sessionStorage.setItem(KEY, token); showLogin(false); refresh(); });

  function statusCls(s) { return ({ RUNNING: "ok", EXTERNAL: "ok", STOPPED: "off", BACKOFF: "warn", BLOCKED: "warn", FAILED: "bad", CIRCUIT_OPEN: "bad" })[s] || "off"; }

  function renderTasks(tasks) {
    const tb = $("tasks"); tb.replaceChildren();
    for (const t of tasks) {
      const tr = el("tr");
      const name = el("td"); name.append(el("strong", t.name), el("div", t.desc, "muted")); tr.append(name);
      tr.append(el("td", t.kind));
      const st = el("td"); st.append(el("span", t.status, "pill " + statusCls(t.status))); tr.append(st);
      tr.append(el("td", fmtUp(t.uptime_s)), el("td", t.restarts), el("td", short(t.last_ok)), el("td", t.last_error || "", "err"));
      const act = el("td");
      const acts = t.kind === "external" ? [] : t.kind === "periodic" ? ["run_now", "restart", "stop", "start"] : ["restart", "stop", "start"];
      for (const a of acts) {
        const b = el("button", ({ run_now: "Jetzt", restart: "Neu", stop: "Stop", start: "Start" })[a]);
        b.type = "button";
        b.addEventListener("click", async () => { b.disabled = true; try { await api("/api/task", { name: t.name, action: a }); } finally { b.disabled = false; refresh(); } });
        act.append(b);
      }
      tr.append(act); tb.append(tr);
    }
    const sel = $("logsel");
    if (!sel.options.length) {
      for (const n of ["supervisor", ...tasks.map((t) => t.name)]) { const o = el("option", n); o.value = n; sel.append(o); }
      sel.addEventListener("change", loadLog);
    }
  }

  function renderKpis(s) {
    const k = $("kpis"); k.replaceChildren();
    const tasks = s.tasks || [];
    const ok = tasks.filter((t) => ["RUNNING", "EXTERNAL"].includes(t.status)).length;
    const bad = tasks.filter((t) => ["FAILED", "CIRCUIT_OPEN", "BLOCKED", "BACKOFF"].includes(t.status)).length;
    const conflicts = (s.bridges && s.bridges.event_counts) ? Object.values(s.bridges.event_counts).reduce((a, c) => a + (c.conflict || 0), 0) : 0;
    for (const [label, val, cls] of [["Tasks aktiv", `${ok}/${tasks.length}`, "ok"], ["Probleme", bad, bad ? "bad" : "ok"], ["Konflikte gesamt", conflicts, conflicts ? "warn" : "ok"], ["Job Object", s.job_object ? "aktiv" : "aus", s.job_object ? "ok" : "warn"]]) {
      const c = el("div", null, "kpi " + cls); c.append(el("div", label, "kl"), el("div", val, "kv")); k.append(c);
    }
  }

  function renderBridges(b) {
    const tb = $("bridges"); tb.replaceChildren();
    if (!b) { tb.append(el("tr")).append(el("td", "Brücken nicht konfiguriert")); return; }
    for (const r of b.rules) {
      const l = r.last || {};
      const tr = el("tr");
      tr.append(el("td", r.name), el("td", r.mode + (b.dry_run ? " (Probelauf)" : "")));
      const st = el("td"); st.append(el("span", r.enabled ? (l.blocked || "OK") : "AUS", "pill " + (!r.enabled ? "off" : l.blocked ? "warn" : "ok"))); tr.append(st);
      tr.append(el("td", l.copied ?? "-"), el("td", l.waiting ?? "-"), el("td", l.conflicts ?? "-"), el("td", l.skipped_placeholder ?? "-"));
      tb.append(tr);
    }
  }

  function renderOllama(tasks) {
    const box = $("ollama"); box.replaceChildren();
    const t = tasks.find((x) => x.name === "ollama");
    if (!t) { box.append(el("div", "nicht konfiguriert")); return; }
    const i = t.info || {};
    const rows = [["Status", t.status], ["Version", i.version], ["Standardmodell", i.default_model]];
    for (const mdl of i.loaded || []) rows.push([mdl.name, `${mdl.size_vram_gb} / ${mdl.size_gb} GB VRAM · ctx ${mdl.context_length ?? "?"} · ${mdl.gpu_share}`]);
    if (!(i.loaded || []).length) rows.push(["Geladen", "kein Modell im Speicher"]);
    for (const [a, v] of rows) { const r = el("div", null, "row"); r.append(el("span", a, "k"), el("span", v ?? "-", "v")); box.append(r); }
  }

  function renderEvents(ev) {
    const tb = $("events"); tb.replaceChildren();
    for (const e of ev || []) { const tr = el("tr"); tr.append(el("td", short(e.at)), el("td", e.rule), el("td", e.kind, "ev-" + e.kind), el("td", e.rel), el("td", e.detail)); tb.append(tr); }
  }
  function renderLinks(links) {
    const ul = $("links"); ul.replaceChildren();
    for (const [name, href] of Object.entries(links || {})) {
      if (!/^https:\/\//.test(href) && !/^http:\/\/127\.0\.0\.1:\d+\/?$/.test(href)) continue;
      const li = el("li"); const a = el("a", name); a.href = href; a.rel = "noopener noreferrer"; a.target = "_blank"; li.append(a); ul.append(li);
    }
  }
  async function loadLog() {
    try { const r = await api("/api/logs?task=" + encodeURIComponent($("logsel").value || "supervisor")); $("log").textContent = (r.lines || []).join("\n"); } catch (e) { /* login shown */ }
  }
  async function refresh() {
    if (!token) { showLogin(true); return; }
    try {
      const s = await api("/api/status");
      $("meta").textContent = `v${s.version} · boot ${s.boot_id} · ${short(s.now)} UTC`;
      renderKpis(s); renderTasks(s.tasks || []); renderBridges(s.bridges); renderOllama(s.tasks || []); renderEvents(s.events); renderLinks(s.links);
    } catch (e) { $("meta").textContent = "Verbindung fehlgeschlagen"; }
  }
  refresh(); loadLog();
  setInterval(refresh, 3000); setInterval(loadLog, 10000);
})();
