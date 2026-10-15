---
schema: IOD.01/1.0
run_id: 2026-10-13__NEXUS-MULTI-LLM-ORCHESTRATOR__R001
type: artifact
artifact: 03_ARTIFACTS/evaluation/NEXUS_EVAL_KONTEXTPAKET_v1.0_3caf813.md
archived_ts: 2026-10-15T06:00:48+02:00
sha256_original: 9701567516c55ecff0ba8f15d124d64ee545be13874782bac134520c52c27ef2
---

# NEXUS-AI – Kontextpaket zur Evaluierung v1.0
Repo: github.com/julianzotter/nexus-platform (privat) · Commit: 3caf813 · Erstellt: 2026-10-13
Gehört zu: NEXUS_EVAL_BOGEN_v1.0.md. Enthält die prüfrelevanten Dateien im Wortlaut (ohne große HTML-/JSON-Datenbestände).

## A Dateibaum (vollständig, mit Größe in Byte)
```
     4664  ./.gitignore
     1069  ./LICENSE
      924  ./NEXUS-TEAM-WORK-01.ipynb
      280  ./README.md
     6430  ./TASK-00004-INVENTORY-AGENT-D.md
     5407  ./docs/concepts/2026-10-13/INTEGRATION.md
     1828  ./docs/concepts/2026-10-13/README.md
     5784  ./docs/concepts/2026-10-13/REVIEW.md
     4740  ./docs/concepts/2026-10-13/catalog.json
     9309  ./docs/concepts/2026-10-13/sources/pdf-normen-parser-skill.extracted.txt
        0  ./orchestrator/COMMUNICATION/lessons/.gitkeep
     2711  ./orchestrator/README.md
     2335  ./orchestrator/config/routing.json
      105  ./orchestrator/nexus_orch/__init__.py
     2007  ./orchestrator/nexus_orch/cli.py
     4690  ./orchestrator/nexus_orch/core.py
     4554  ./orchestrator/nexus_orch/providers.py
      353  ./orchestrator/pyproject.toml
     2984  ./orchestrator/registry/workflow-registry.json
      635  ./orchestrator/setup.ps1
     2079  ./orchestrator/sync_nexus.ps1
     3887  ./orchestrator/tests/test_orch.py
     1550  ./prototypes/vibe-coder-v2.3/README.md
    36304  ./prototypes/vibe-coder-v2.3/index.html
      644  ./registry/catalog-draft.yaml
     1493  ./registry/coverage-per-source.json
      502  ./registry/duplicates-report.md
        0  ./registry/file-registry.jsonl
     1183  ./registry/inventory-summary.txt
   162152  ./reports/2026-10-13_parsing-pipeline/NEXUS_PARSE_DASHBOARD_v1.0.html
   165592  ./reports/2026-10-13_parsing-pipeline/NEXUS_PARSE_DASHBOARD_v1.1.html
   153961  ./reports/2026-10-13_parsing-pipeline/NEXUS_PARSE_INVENTORY_v1.0.json
     2167  ./reports/2026-10-13_parsing-pipeline/NEXUS_PARSE_REPORT_v1.0.md
     3167  ./reports/2026-10-13_parsing-pipeline/NEXUS_PARSE_REPORT_v1.1.md
  8089502  ./reports/2026-10-13_parsing-pipeline/NEXUS_VECTOR_INDEX_v1.0.json
     2444  ./reports/2026-10-13_parsing-pipeline/ocr.py
     1743  ./reports/2026-10-13_parsing-pipeline/parse.py
     4005  ./tests/test_inventory_completeness.py
     6711  ./tools/coverage_stats.py
     3553  ./tools/detect_duplicates.py
     8176  ./tools/validate_registry.py
```

## FILE: README.md
~~~~markdown
     1	# nexus-platform
     2	NEXUS Platform Hub: Unified registry, coordinated execution, evidence-based learning. Single source of truth for engineering knowledge, deterministic solvers, validated workflows, and multiagent orchestration with dual-mode operations (production + improvement).
~~~~

## FILE: orchestrator/README.md
~~~~markdown
     1	# NEXUS-AI Multi-LLM Orchestrator v1.2.0
     2	
     3	Integrationsschicht des NEXUS AI-OS: ein Einstiegspunkt, der Aufgaben deterministisch (T=0.0) an Perplexity, Claude, GPT, Gemini oder ein lokales Modell (Ollama) routet.
     4	
     5	## Funktionen
     6	| Funktion | Umsetzung |
     7	|---|---|
     8	| Routing nach Aufgabentyp | `config/routing.json` → `routes` (research, norm_check, code, review, draft, long_context, private, engineering_decision) |
     9	| Fallback-Kette | primary → fallback[], Fehler protokolliert |
    10	| Privacy Hard Gate | Marker `VERTRAULICH`/`CONFIDENTIAL`/`[P3]` → nur `local`, kein Cloud-Fallback |
    11	| Model Council | `council`: alle Mitglieder, Konsensprüfung, sonst Synthese (Konsens / Abweichungen / Empfehlung) |
    12	| Perplexity-Integration | Sonar API (`sonar-pro`), Zitate werden mit ausgegeben |
    13	| Shared Lessons Layer | `COMMUNICATION/lessons/lessons.jsonl` (agent, context, condition, pattern, evidence; Status PROPOSED) |
    14	| OCR (Google Cloud Vision) | Route `ocr`: Vision `DOCUMENT_TEXT_DETECTION` (Bild-URL, gs:// oder lokaler Pfad), Fallback Gemini; vertraulich → lokal |
    15	| Audit | `COMMUNICATION/audit/YY_MM_DD_audit.jsonl` (nur Prompt-Hash, kein Klartext) |
    16	| Workflow-Registry | `registry/workflow-registry.json` – 17 Workflows (nexus-mvp, nexus-skill-family, nexus-platform, Control Tower, Mail-Triage) mit Route |
    17	
    18	## Installation als Befehl `nexus`
    19	```powershell
    20	cd "$env:USERPROFILE\nexus-platform\orchestrator"; python -m pip install -e .
    21	nexus status   # funktioniert danach in jedem Ordner
    22	```
    23	
    24	## Start
    25	```powershell
    26	.\setup.ps1                                   # Keys als User-Env, Tests, Status
    27	python -m nexus_orch.cli run research "EN 1995-1-1 kmod NKL2 Quellen"
    28	python -m nexus_orch.cli council engineering_decision "BSP vs. HBV Decke 7,5 m Spannweite"
    29	python -m nexus_orch.cli lesson --agent claude --context EC5 --condition "wenn NKL fehlt" --pattern "NKL vor kmod abfragen" --evidence "Session 2026-10-13"
    30	python -m nexus_orch.cli run ocr "C:/Scans/Positionsplan_EG.jpg"
    31	python -m nexus_orch.cli lessons kmod
    32	python -m nexus_orch.cli registry
    33	```
    34	Nur Python-Standardbibliothek; `pytest` für Tests. Modellnamen in `routing.json` anpassen.
    35	
    36	## Drive-Sync (Windows)
    37	```powershell
    38	.\sync_nexus.ps1              # main pullen, Tests, dann: orchestrator -> LLM-LOCAL-SSOT + BENCHMARK, komplettes Repo -> LLM-LOCAL-SSOT\nexus-platform
    39	.\sync_nexus.ps1 -NoFullRepo  # nur orchestrator
    40	# ausgeschlossen: .git, Caches, venv, node_modules, .env/*.key/*.pem; kein Loeschen in Drive
    41	```
    42	
    43	## SSOT
    44	Google Drive `/LLM-LOCAL-SSOT` = Wahrheit · GitHub `julianzotter/nexus-platform` = Versionierung · OneDrive/Dropbox = Spiegel · Perplexity-Projekt „NEXUS-AI Multi-LLM System“ = Orchestrator-Kontext.
~~~~

## FILE: orchestrator/config/routing.json
~~~~json
     1	{
     2	  "version": "1.2.0",
     3	  "default_temperature": 0.0,
     4	  "providers": {
     5	    "perplexity": {
     6	      "kind": "openai_compat",
     7	      "base_url": "https://api.perplexity.ai",
     8	      "model": "sonar-pro",
     9	      "env_key": "PERPLEXITY_API_KEY"
    10	    },
    11	    "claude": {
    12	      "kind": "anthropic",
    13	      "base_url": "https://api.anthropic.com",
    14	      "model": "claude-sonnet-4-5",
    15	      "env_key": "ANTHROPIC_API_KEY"
    16	    },
    17	    "gpt": {
    18	      "kind": "openai_compat",
    19	      "base_url": "https://api.openai.com/v1",
    20	      "model": "gpt-5",
    21	      "env_key": "OPENAI_API_KEY"
    22	    },
    23	    "gemini": {
    24	      "kind": "gemini",
    25	      "base_url": "https://generativelanguage.googleapis.com/v1beta",
    26	      "model": "gemini-2.5-pro",
    27	      "env_key": "GEMINI_API_KEY"
    28	    },
    29	    "local": {
    30	      "kind": "ollama",
    31	      "base_url": "http://localhost:11434",
    32	      "model": "qwen2.5:7b",
    33	      "env_key": null,
    34	      "num_ctx": 16384
    35	    },
    36	    "vision": {
    37	      "kind": "gcv_ocr",
    38	      "base_url": "https://vision.googleapis.com/v1",
    39	      "model": "DOCUMENT_TEXT_DETECTION",
    40	      "env_key": "GOOGLE_VISION_API_KEY"
    41	    }
    42	  },
    43	  "routes": {
    44	    "research": {
    45	      "primary": "perplexity",
    46	      "fallback": [
    47	        "gemini",
    48	        "gpt"
    49	      ]
    50	    },
    51	    "norm_check": {
    52	      "primary": "perplexity",
    53	      "fallback": [
    54	        "claude"
    55	      ],
    56	      "council": true
    57	    },
    58	    "code": {
    59	      "primary": "claude",
    60	      "fallback": [
    61	        "gpt",
    62	        "local"
    63	      ]
    64	    },
    65	    "review": {
    66	      "primary": "claude",
    67	      "fallback": [
    68	        "gpt"
    69	      ]
    70	    },
    71	    "draft": {
    72	      "primary": "gpt",
    73	      "fallback": [
    74	        "claude"
    75	      ]
    76	    },
    77	    "long_context": {
    78	      "primary": "gemini",
    79	      "fallback": [
    80	        "claude"
    81	      ]
    82	    },
    83	    "private": {
    84	      "primary": "local",
    85	      "fallback": []
    86	    },
    87	    "engineering_decision": {
    88	      "primary": "claude",
    89	      "fallback": [
    90	        "gpt"
    91	      ],
    92	      "council": true,
    93	      "council_members": [
    94	        "perplexity",
    95	        "claude",
    96	        "gpt",
    97	        "gemini"
    98	      ]
    99	    },
   100	    "ocr": {
   101	      "primary": "vision",
   102	      "fallback": [
   103	        "gemini"
   104	      ]
   105	    }
   106	  },
   107	  "privacy": {
   108	    "confidential_route": "private",
   109	    "markers": [
   110	      "VERTRAULICH",
   111	      "CONFIDENTIAL",
   112	      "[P3]"
   113	    ]
   114	  },
   115	  "lessons_dir": "COMMUNICATION/lessons"
   116	}~~~~

## FILE: orchestrator/registry/workflow-registry.json
~~~~json
     1	{
     2	  "version": "1.1.0",
     3	  "ssot": {
     4	    "primary": "Google Drive /LLM-LOCAL-SSOT",
     5	    "versioning": "github.com/julianzotter/nexus-platform",
     6	    "mirror": [
     7	      "OneDrive",
     8	      "Dropbox"
     9	    ],
    10	    "perplexity_project": "https://www.perplexity.ai/projects/nexus-ai-multi-llm-system-JCDYwmIfSliQifFlkLD9NA"
    11	  },
    12	  "pipeline": [
    13	    "inventory",
    14	    "parse",
    15	    "validate",
    16	    "register",
    17	    "report"
    18	  ],
    19	  "workflows": [
    20	    {
    21	      "id": "WF-01",
    22	      "name": "knowledge-ingestion",
    23	      "route": "long_context",
    24	      "source": "Drive:nexus-mvp.zip/skills/knowledge-ingestion"
    25	    },
    26	    {
    27	      "id": "WF-02",
    28	      "name": "knowledge-quality-gate",
    29	      "route": "review",
    30	      "source": "Drive:nexus-mvp.zip/skills/knowledge-quality-gate"
    31	    },
    32	    {
    33	      "id": "WF-03",
    34	      "name": "source-governance",
    35	      "route": "review",
    36	      "source": "Drive:nexus-mvp.zip/skills/source-governance"
    37	    },
    38	    {
    39	      "id": "WF-04",
    40	      "name": "norm-chunk-validator",
    41	      "route": "norm_check",
    42	      "source": "Drive:nexus-skill-family.zip"
    43	    },
    44	    {
    45	      "id": "WF-05",
    46	      "name": "ssot-github-sync",
    47	      "route": "code",
    48	      "source": "Drive:nexus-skill-family.zip"
    49	    },
    50	    {
    51	      "id": "WF-06",
    52	      "name": "audit-reporter",
    53	      "route": "draft",
    54	      "source": "Drive:nexus-skill-family.zip"
    55	    },
    56	    {
    57	      "id": "WF-07",
    58	      "name": "transcript-ingest",
    59	      "route": "long_context",
    60	      "source": "Drive:nexus-skill-family.zip"
    61	    },
    62	    {
    63	      "id": "WF-08",
    64	      "name": "license-router",
    65	      "route": "review",
    66	      "source": "Drive:nexus-skill-family.zip"
    67	    },
    68	    {
    69	      "id": "WF-09",
    70	      "name": "ko-extractor",
    71	      "route": "long_context",
    72	      "source": "Drive:nexus-skill-family.zip"
    73	    },
    74	    {
    75	      "id": "WF-10",
    76	      "name": "rag-eval-harness",
    77	      "route": "code",
    78	      "source": "Drive:nexus-skill-family.zip"
    79	    },
    80	    {
    81	      "id": "WF-11",
    82	      "name": "pdf-ground-truth-freeze",
    83	      "route": "review",
    84	      "source": "Drive:nexus-skill-family.zip"
    85	    },
    86	    {
    87	      "id": "WF-12",
    88	      "name": "human-ocr-public",
    89	      "route": "private",
    90	      "source": "Drive:nexus-skill-family.zip"
    91	    },
    92	    {
    93	      "id": "WF-13",
    94	      "name": "registry-inventory (TASK-00004)",
    95	      "route": "code",
    96	      "source": "GitHub:nexus-platform/tools"
    97	    },
    98	    {
    99	      "id": "WF-14",
   100	      "name": "control-tower-daily-0700",
   101	      "route": "draft",
   102	      "source": "Perplexity automation"
   103	    },
   104	    {
   105	      "id": "WF-15",
   106	      "name": "mail-executive-triage",
   107	      "route": "draft",
   108	      "source": "GitHub:EMAIL-MANAGER-DASHBAORD"
   109	    },
   110	    {
   111	      "id": "WF-16",
   112	      "name": "engineering-decision-council",
   113	      "route": "engineering_decision",
   114	      "source": "nexus_orch.council"
   115	    },
   116	    {
   117	      "id": "WF-17",
   118	      "name": "vision-ocr (Plaene, Scans, Fotos, Normtabellen)",
   119	      "route": "ocr",
   120	      "source": "Google Cloud Vision (Perplexity-Connector / REST)"
   121	    }
   122	  ]
   123	}~~~~

## FILE: orchestrator/nexus_orch/core.py
~~~~python
     1	"""Router + fallback + council + shared-lessons log."""
     2	import datetime as dt, hashlib, json, pathlib
     3	from .providers import Provider, ProviderError
     4	
     5	ROOT = pathlib.Path(__file__).resolve().parent.parent
     6	
     7	def load_config(path=None):
     8	    return json.loads(pathlib.Path(path or ROOT / "config/routing.json").read_text(encoding="utf-8"))
     9	
    10	class Orchestrator:
    11	    def __init__(self, cfg=None, providers=None, root=ROOT):
    12	        self.cfg = cfg or load_config()
    13	        self.root = pathlib.Path(root)
    14	        self.providers = providers or {n: Provider(n, c) for n, c in self.cfg["providers"].items()}
    15	
    16	    def classify(self, task, prompt):
    17	        p = self.cfg["privacy"]
    18	        if any(m in prompt for m in p["markers"]):
    19	            return p["confidential_route"]  # hard gate: confidential never leaves local
    20	        if task not in self.cfg["routes"]:
    21	            raise KeyError(f"unknown task '{task}', known: {sorted(self.cfg['routes'])}")
    22	        return task
    23	
    24	    def chain(self, route):
    25	        r = self.cfg["routes"][route]
    26	        return [r["primary"], *r.get("fallback", [])]
    27	
    28	    def run(self, task, prompt, system=""):
    29	        route = self.classify(task, prompt)
    30	        errors = []
    31	        for name in self.chain(route):
    32	            try:
    33	                res = self.providers[name].complete(prompt, system, self.cfg["default_temperature"])
    34	                out = {"route": route, "provider": name, **res, "errors": errors}
    35	                self._audit(out, prompt)
    36	                return out
    37	            except ProviderError as e:
    38	                errors.append(str(e))
    39	        raise ProviderError(f"all providers failed for route {route}: {errors}")
    40	
    41	    def council(self, task, prompt, system=""):
    42	        route = self.classify(task, prompt)
    43	        r = self.cfg["routes"][route]
    44	        members = r.get("council_members") or self.chain(route)
    45	        answers = {}
    46	        for n in members:
    47	            try:
    48	                answers[n] = self.providers[n].complete(prompt, system, 0.0)["text"]
    49	            except ProviderError as e:
    50	                answers[n] = None
    51	        valid = {k: v for k, v in answers.items() if v}
    52	        if not valid:
    53	            raise ProviderError("council: no valid answers")
    54	        norm = lambda s: " ".join(s.lower().split())
    55	        groups = {}
    56	        for k, v in valid.items():
    57	            groups.setdefault(norm(v), []).append(k)
    58	        consensus = len(groups) == 1
    59	        synth = None
    60	        if not consensus:
    61	            judge = r["primary"] if r["primary"] in valid else next(iter(valid))
    62	            body = "\n\n".join(f"### {k}\n{v}" for k, v in valid.items())
    63	            synth = self.providers[judge].complete(
    64	                f"Frage:\n{prompt}\n\nAntworten:\n{body}\n\nSynthetisiere: 1) Konsens, 2) Abweichungen je Modell, 3) begruendete Empfehlung.",
    65	                system, 0.0)["text"]
    66	        out = {"route": route, "members": members, "answers": answers, "consensus": consensus,
    67	               "synthesis": synth or next(iter(valid.values()))}
    68	        self._audit(out, prompt)
    69	        return out
    70	
    71	    def _audit(self, out, prompt):
    72	        d = self.root / "COMMUNICATION/audit"; d.mkdir(parents=True, exist_ok=True)
    73	        rec = {"ts": dt.datetime.now(dt.timezone.utc).isoformat(), "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
    74	               **{k: out[k] for k in ("route", "provider", "consensus") if k in out}}
    75	        with open(d / f"{dt.date.today():%y_%m_%d}_audit.jsonl", "a", encoding="utf-8") as f:
    76	            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    77	
    78	REQUIRED_LESSON = ("agent", "context", "condition", "pattern", "evidence")
    79	
    80	def write_lesson(lesson, root=ROOT):
    81	    """Shared-Lessons-Layer: conditional reusable pattern, published to COMMUNICATION/lessons."""
    82	    miss = [k for k in REQUIRED_LESSON if not lesson.get(k)]
    83	    if miss:
    84	        raise ValueError(f"lesson missing fields: {miss}")
    85	    lesson = {"id": hashlib.sha1(json.dumps(lesson, sort_keys=True).encode()).hexdigest()[:12],
    86	              "ts": dt.datetime.now(dt.timezone.utc).isoformat(), "status": "PROPOSED", **lesson}
    87	    p = pathlib.Path(root) / "COMMUNICATION/lessons/lessons.jsonl"; p.parent.mkdir(parents=True, exist_ok=True)
    88	    with open(p, "a", encoding="utf-8") as f:
    89	        f.write(json.dumps(lesson, ensure_ascii=False) + "\n")
    90	    return lesson
    91	
    92	def search_lessons(query, root=ROOT):
    93	    p = pathlib.Path(root) / "COMMUNICATION/lessons/lessons.jsonl"
    94	    if not p.exists():
    95	        return []
    96	    q = query.lower().split()
    97	    rows = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    98	    return [r for r in rows if all(t in json.dumps(r, ensure_ascii=False).lower() for t in q)]
~~~~

## FILE: orchestrator/nexus_orch/providers.py
~~~~python
     1	"""Provider adapters (stdlib only). temperature=0.0 default, deterministic."""
     2	import base64, json, os, urllib.error, urllib.request
     3	
     4	class ProviderError(RuntimeError):
     5	    pass
     6	
     7	def _post(url, headers, body, timeout=120):
     8	    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", **headers})
     9	    try:
    10	        with urllib.request.urlopen(req, timeout=timeout) as r:
    11	            return json.loads(r.read())
    12	    except urllib.error.HTTPError as e:
    13	        detail = e.read().decode("utf-8", "replace")[:300]
    14	        hint = " -> Modell fehlt: 'ollama pull <model>' bzw. 'ollama list' pruefen" if e.code == 404 and "11434" in url else ""
    15	        raise ProviderError(f"{url.split('?')[0]}: HTTP {e.code} {detail}{hint}") from e
    16	    except Exception as e:  # network, JSON
    17	        raise ProviderError(f"{url.split('?')[0]}: {e}") from e
    18	
    19	class Provider:
    20	    def __init__(self, name, cfg):
    21	        self.name, self.cfg = name, cfg
    22	    def key(self):
    23	        env = self.cfg.get("env_key")
    24	        if env is None:
    25	            return ""
    26	        k = os.environ.get(env)
    27	        if not k:
    28	            raise ProviderError(f"{self.name}: env {env} missing")
    29	        return k
    30	    def available(self):
    31	        try:
    32	            self.key(); return True
    33	        except ProviderError:
    34	            return False
    35	    def complete(self, prompt, system="", temperature=0.0):
    36	        kind, base, model, key = self.cfg["kind"], self.cfg["base_url"], self.cfg["model"], self.key()
    37	        if kind == "openai_compat":
    38	            msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
    39	            h = {"Authorization": f"Bearer {key}"} if key else {}
    40	            d = _post(f"{base}/chat/completions", h, {"model": model, "messages": msgs, "temperature": temperature})
    41	            return {"text": d["choices"][0]["message"]["content"], "citations": d.get("citations", []), "model": model}
    42	        if kind == "anthropic":
    43	            d = _post(f"{base}/v1/messages", {"x-api-key": key, "anthropic-version": "2023-06-01"},
    44	                      {"model": model, "max_tokens": 4096, "system": system, "temperature": temperature,
    45	                       "messages": [{"role": "user", "content": prompt}]})
    46	            return {"text": "".join(b.get("text", "") for b in d["content"]), "citations": [], "model": model}
    47	        if kind == "gemini":
    48	            body = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": temperature}}
    49	            if system:
    50	                body["systemInstruction"] = {"parts": [{"text": system}]}
    51	            d = _post(f"{base}/models/{model}:generateContent?key={key}", {}, body)
    52	            return {"text": d["candidates"][0]["content"]["parts"][0]["text"], "citations": [], "model": model}
    53	        if kind == "ollama":
    54	            # native API: num_ctx per request, unabhaengig vom App-Regler
    55	            msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
    56	            d = _post(f"{base}/api/chat", {}, {"model": model, "messages": msgs, "stream": False,
    57	                      "options": {"temperature": temperature, "num_ctx": self.cfg.get("num_ctx", 16384)}})
    58	            return {"text": d["message"]["content"], "citations": [], "model": model}
    59	        if kind == "gcv_ocr":
    60	            # prompt = image URL (http/https/gs) or local file path
    61	            img = {"source": {"imageUri": prompt}} if prompt.startswith(("http://", "https://", "gs://")) \
    62	                else {"content": base64.b64encode(open(prompt, "rb").read()).decode()}
    63	            d = _post(f"{base}/images:annotate?key={key}", {},
    64	                      {"requests": [{"image": img, "features": [{"type": model}]}]})
    65	            r0 = d["responses"][0]
    66	            if "error" in r0:
    67	                raise ProviderError(f"vision: {r0['error'].get('message')}")
    68	            return {"text": r0.get("fullTextAnnotation", {}).get("text", ""), "citations": [prompt], "model": model}
    69	        raise ProviderError(f"unknown kind {kind}")
    70	
    71	class MockProvider(Provider):
    72	    """For tests / dry-run."""
    73	    def __init__(self, name, answer="OK", fail=False):
    74	        super().__init__(name, {"kind": "mock", "model": "mock", "env_key": None})
    75	        self.answer, self.fail = answer, fail
    76	    def complete(self, prompt, system="", temperature=0.0):
    77	        if self.fail:
    78	            raise ProviderError(f"{self.name}: forced failure")
    79	        return {"text": self.answer, "citations": [], "model": "mock"}
~~~~

## FILE: orchestrator/nexus_orch/cli.py
~~~~python
     1	"""python -m nexus_orch.cli {status|run|council|lesson|lessons|registry}"""
     2	import argparse, json, pathlib, sys
     3	from .core import Orchestrator, write_lesson, search_lessons, ROOT
     4	from .providers import ProviderError
     5	
     6	def main(argv=None):
     7	    ap = argparse.ArgumentParser(prog="nexus")
     8	    sp = ap.add_subparsers(dest="cmd", required=True)
     9	    sp.add_parser("status")
    10	    for c in ("run", "council"):
    11	        p = sp.add_parser(c); p.add_argument("task"); p.add_argument("prompt"); p.add_argument("--system", default="")
    12	    p = sp.add_parser("lesson"); [p.add_argument(f"--{k}", required=True) for k in ("agent", "context", "condition", "pattern", "evidence")]
    13	    p = sp.add_parser("lessons"); p.add_argument("query", nargs="?", default="")
    14	    sp.add_parser("registry")
    15	    a = ap.parse_args(argv)
    16	    o = Orchestrator()
    17	    if a.cmd == "status":
    18	        r = {"providers": {n: p.available() for n, p in o.providers.items()},
    19	             "routes": {k: o.chain(k) for k in o.cfg["routes"]}}
    20	    elif a.cmd in ("run", "council"):
    21	        try:
    22	            r = (o.run if a.cmd == "run" else o.council)(a.task, a.prompt, a.system)
    23	        except (ProviderError, KeyError) as e:
    24	            missing = [p.cfg["env_key"] for p in o.providers.values() if p.cfg.get("env_key") and not p.available()]
    25	            print(json.dumps({"ok": False, "error": str(e).strip("'\""), "missing_keys": missing,
    26	                              "hint": "Keys setzen: .\\setup.ps1, danach neues PowerShell-Fenster; lokal: Ollama starten"},
    27	                             ensure_ascii=False, indent=2))
    28	            return 2
    29	    elif a.cmd == "lesson":
    30	        r = write_lesson({k: getattr(a, k) for k in ("agent", "context", "condition", "pattern", "evidence")})
    31	    elif a.cmd == "lessons":
    32	        r = search_lessons(a.query)
    33	    else:
    34	        r = json.loads((ROOT / "registry/workflow-registry.json").read_text(encoding="utf-8"))
    35	    print(json.dumps(r, ensure_ascii=False, indent=2))
    36	
    37	if __name__ == "__main__":
    38	    sys.exit(main())
~~~~

## FILE: orchestrator/tests/test_orch.py
~~~~python
     1	import json, pytest
     2	from nexus_orch.core import Orchestrator, load_config, write_lesson, search_lessons, ROOT
     3	from nexus_orch.providers import MockProvider, ProviderError
     4	
     5	def mk(tmp_path, **over):
     6	    cfg = load_config()
     7	    prov = {n: MockProvider(n, answer=f"A-{n}") for n in cfg["providers"]}
     8	    prov.update(over)
     9	    return Orchestrator(cfg, prov, root=tmp_path)
    10	
    11	def test_primary(tmp_path):
    12	    r = mk(tmp_path).run("research", "Q")
    13	    assert r["provider"] == "perplexity"
    14	
    15	def test_fallback(tmp_path):
    16	    r = mk(tmp_path, perplexity=MockProvider("perplexity", fail=True)).run("research", "Q")
    17	    assert r["provider"] == "gemini" and r["errors"]
    18	
    19	def test_privacy_gate(tmp_path):
    20	    assert mk(tmp_path).run("research", "VERTRAULICH Statik")["provider"] == "local"
    21	
    22	def test_privacy_no_cloud_fallback(tmp_path):
    23	    with pytest.raises(ProviderError):
    24	        mk(tmp_path, local=MockProvider("local", fail=True)).run("research", "VERTRAULICH x")
    25	
    26	def test_unknown_task(tmp_path):
    27	    with pytest.raises(KeyError):
    28	        mk(tmp_path).run("xyz", "Q")
    29	
    30	def test_council_dissent(tmp_path):
    31	    r = mk(tmp_path).council("engineering_decision", "Q")
    32	    assert r["consensus"] is False and r["synthesis"]
    33	
    34	def test_council_consensus(tmp_path):
    35	    cfg = load_config()
    36	    o = Orchestrator(cfg, {n: MockProvider(n, answer="Same") for n in cfg["providers"]}, root=tmp_path)
    37	    assert o.council("engineering_decision", "Q")["consensus"] is True
    38	
    39	def test_lessons(tmp_path):
    40	    with pytest.raises(ValueError):
    41	        write_lesson({"agent": "x"}, root=tmp_path)
    42	    write_lesson({"agent": "claude", "context": "EC5", "condition": "wenn kmod fehlt", "pattern": "NKL pruefen", "evidence": "s1"}, root=tmp_path)
    43	    assert len(search_lessons("kmod", root=tmp_path)) == 1
    44	
    45	def test_registry_routes_valid():
    46	    cfg = load_config(); reg = json.loads((ROOT / "registry/workflow-registry.json").read_text())
    47	    assert all(w["route"] in cfg["routes"] for w in reg["workflows"])
    48	    assert all(set(r["fallback"] + [r["primary"]]) <= set(cfg["providers"]) for r in cfg["routes"].values())
    49	
    50	def test_ocr_route(tmp_path):
    51	    assert mk(tmp_path).run("ocr", "https://x/plan.jpg")["provider"] == "vision"
    52	
    53	def test_ocr_fallback(tmp_path):
    54	    assert mk(tmp_path, vision=MockProvider("vision", fail=True)).run("ocr", "https://x/p.jpg")["provider"] == "gemini"
    55	
    56	def test_ocr_confidential_local(tmp_path):
    57	    assert mk(tmp_path).run("ocr", "VERTRAULICH C:/scan.png")["provider"] == "local"
    58	
    59	def test_cli_clean_error(monkeypatch, capsys):
    60	    from nexus_orch import cli
    61	    for k in ("PERPLEXITY_API_KEY", "GEMINI_API_KEY", "OPENAI_API_KEY"):
    62	        monkeypatch.delenv(k, raising=False)
    63	    assert cli.main(["run", "research", "Q"]) == 2
    64	    out = json.loads(capsys.readouterr().out)
    65	    assert out["ok"] is False and "PERPLEXITY_API_KEY" in out["missing_keys"]
    66	
    67	def test_http_error_detail(monkeypatch):
    68	    import io, urllib.error, urllib.request
    69	    from nexus_orch import providers
    70	    def boom(*a, **k):
    71	        raise urllib.error.HTTPError("http://localhost:11434/v1/chat/completions", 404, "Not Found", {}, io.BytesIO(b'{"error":"model \'qwen2.5:7b\' not found"}'))
    72	    monkeypatch.setattr(urllib.request, "urlopen", boom)
    73	    with pytest.raises(ProviderError) as e:
    74	        providers._post("http://localhost:11434/v1/chat/completions", {}, {})
    75	    assert "not found" in str(e.value) and "ollama pull" in str(e.value)
    76	
    77	def test_ollama_num_ctx(monkeypatch):
    78	    from nexus_orch import providers
    79	    seen = {}
    80	    def fake(url, h, body, timeout=120):
    81	        seen.update(url=url, body=body); return {"message": {"content": "OK"}}
    82	    monkeypatch.setattr(providers, "_post", fake)
    83	    cfg = load_config()["providers"]["local"]
    84	    r = providers.Provider("local", cfg).complete("Q")
    85	    assert r["text"] == "OK" and seen["url"].endswith("/api/chat") and seen["body"]["options"]["num_ctx"] == 16384
~~~~

## FILE: orchestrator/setup.ps1
~~~~powershell
     1	# NEXUS-AI Multi-LLM Orchestrator - Windows Setup (Keys nur als User-Env, nie im Repo)
     2	python -m pip install -q pytest
     3	foreach ($k in "PERPLEXITY_API_KEY","ANTHROPIC_API_KEY","OPENAI_API_KEY","GEMINI_API_KEY","GOOGLE_VISION_API_KEY") {
     4	  if (-not [Environment]::GetEnvironmentVariable($k,"User")) {
     5	    $v = Read-Host "$k (leer = ueberspringen)" -AsSecureString
     6	    $p = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($v))
     7	    if ($p) { [Environment]::SetEnvironmentVariable($k,$p,"User"); Set-Item "env:$k" $p }
     8	  }
     9	}
    10	python -m pytest -q tests
    11	python -m nexus_orch.cli status
~~~~

## FILE: orchestrator/sync_nexus.ps1
~~~~powershell
     1	# NEXUS Sync: GitHub (nexus-platform, main) -> Google Drive for desktop (G:)
     2	# Richtung: GitHub = Versionierung -> Drive = SSOT-Ablage + Benchmark-Kopie. Kein Push, kein Loeschen (robocopy ohne /MIR).
     3	#   .\sync_nexus.ps1              Orchestrator (SSOT + Benchmark) + komplettes Repo (SSOT\nexus-platform)
     4	#   .\sync_nexus.ps1 -NoFullRepo  nur Orchestrator
     5	param(
     6	  [string]$Repo      = "$env:USERPROFILE\nexus-platform",
     7	  [string]$Drive     = "G:\Meine Ablage",
     8	  [string]$Ssot      = "_developement\LLM-LOCAL-SSOT\nexus-llm-orchestrator",
     9	  [string]$Benchmark = "_INDEX_LNK\BENCHMARK Multi-LLM-Orchestrierung\nexus-llm-orchestrator",
    10	  [string]$FullRepo  = "_developement\LLM-LOCAL-SSOT\nexus-platform",
    11	  [switch]$NoFullRepo
    12	)
    13	$ErrorActionPreference = "Stop"
    14	if (-not (Test-Path $Drive)) { throw "Drive-Pfad fehlt: $Drive (Google Drive for desktop gestartet?)" }
    15	if (-not (Test-Path $Repo)) { git clone https://github.com/julianzotter/nexus-platform.git $Repo }
    16	git -C $Repo checkout main; git -C $Repo pull --ff-only
    17	if ($LASTEXITCODE -ne 0) { throw "git pull fehlgeschlagen (lokale Aenderungen? -> git -C `"$Repo`" status)" }
    18	$src = Join-Path $Repo "orchestrator"
    19	python -m pytest -q (Join-Path $src "tests"); if ($LASTEXITCODE -ne 0) { throw "Tests fehlgeschlagen - kein Sync" }
    20	$sha = (git -C $Repo rev-parse --short HEAD)
    21	$XD  = @(".git", "__pycache__", ".pytest_cache", ".ipynb_checkpoints", "node_modules", ".venv", "venv", "audit")
    22	$XF  = @("*.pyc", ".env", "*.key", "*.pem", "*.secret")
    23	
    24	function Sync-Dir($from, $to) {
    25	  robocopy $from $to /E /XD $XD /XF $XF /R:2 /W:2 /NFL /NDL /NJH /NP | Out-Null
    26	  if ($LASTEXITCODE -ge 8) { throw "robocopy Fehler $LASTEXITCODE -> $to" }
    27	  "commit=$sha`nsynced=$(Get-Date -Format s)`nsource=github.com/julianzotter/nexus-platform/$(Split-Path $from -Leaf)" |
    28	    Set-Content (Join-Path $to "SYNC_STAMP.txt") -Encoding UTF8
    29	  Write-Host "[OK] $to  @ $sha"
    30	}
    31	
    32	$jobs = @(@($src, $Ssot), @($src, $Benchmark))
    33	if (-not $NoFullRepo) { $jobs += ,@($Repo, $FullRepo) }
    34	foreach ($j in $jobs) { Sync-Dir $j[0] (Join-Path $Drive $j[1]) }
~~~~

## FILE: orchestrator/pyproject.toml
~~~~toml
     1	[build-system]
     2	requires = ["setuptools>=61"]
     3	build-backend = "setuptools.build_meta"
     4	
     5	[project]
     6	name = "nexus-orch"
     7	version = "1.2.0"
     8	description = "NEXUS-AI Multi-LLM Orchestrator (Perplexity, Claude, GPT, Gemini, Vision, Ollama)"
     9	requires-python = ">=3.10"
    10	
    11	[project.scripts]
    12	nexus = "nexus_orch.cli:main"
    13	
    14	[tool.setuptools]
    15	packages = ["nexus_orch"]
~~~~

## FILE: registry/inventory-summary.txt
~~~~text
     1	Inventory coverage (formula: indexed / accessible)
     2	NEXUS-AI-AEC-ENGINEERIN-KNOWLEDGE-GRAPH: INCOMPLETE — No local read-only source mount is available; required per-file metadata could not be measured.
     3	julianzotter: INCOMPLETE — No local read-only source mount is available; required per-file metadata could not be measured.
     4	Obsidian-Vault: INCOMPLETE — No accessible local vault mount was present.
     5	Google Drive: INCOMPLETE — No authenticated Drive mount was present.
     6	Total: INCOMPLETE (one or more sources are incomplete)
     7	
     8	Reproducibility
     9	Tool: coverage_stats.py v1; Python 3.12.3
    10	Command: /usr/bin/python3 tools/coverage_stats.py --registry registry/file-registry.jsonl --output registry/coverage-per-source.json --summary registry/inventory-summary.txt --incomplete 'NEXUS-AI-AEC-ENGINEERIN-KNOWLEDGE-GRAPH=No local read-only source mount is available; required per-file metadata could not be measured.' --incomplete 'julianzotter=No local read-only source mount is available; required per-file metadata could not be measured.' --incomplete 'Obsidian-Vault=No accessible local vault mount was present.' --incomplete 'Google Drive=No authenticated Drive mount was present.'
~~~~

## FILE: registry/duplicates-report.md
~~~~markdown
     1	# Duplicate candidates
     2	
     3	Groups are ordered by SHA-256; canonical records are ordered by root, path, and id.
     4	Candidates cover only indexed records; an empty result does not establish that unavailable sources contain no duplicates.
     5	
     6	No duplicate candidates were found in the available registry records.
     7	
     8	## Reproducibility
     9	
    10	Tool: detect_duplicates.py v1; Python 3.12.3
    11	
    12	Command: `/usr/bin/python3 tools/detect_duplicates.py --registry registry/file-registry.jsonl --report registry/duplicates-report.md`
~~~~

## FILE: tools/validate_registry.py
~~~~python
     1	#!/usr/bin/env python3
     2	"""Validate inventory registry structure and measured coverage calculations."""
     3	from __future__ import annotations
     4	
     5	import argparse
     6	import hashlib
     7	import json
     8	import re
     9	from datetime import datetime
    10	from pathlib import Path
    11	from typing import Any
    12	
    13	from coverage_stats import COUNT_FIELDS, SOURCE_NAMES
    14	
    15	REQUIRED_FIELDS = {"id", "root", "path", "name", "ext", "size", "mtime", "sha256", "status"}
    16	VALID_STATUSES = {"FOUND", "SKIPPED", "ERROR", "INCOMPLETE"}
    17	
    18	
    19	def validate_registry(registry_path: Path, coverage_path: Path) -> list[str]:
    20	    errors: list[str] = []
    21	    records: list[dict[str, Any]] = []
    22	    try:
    23	        with registry_path.open(encoding="utf-8") as stream:
    24	            for line_number, line in enumerate(stream, 1):
    25	                if not line.strip():
    26	                    errors.append(f"line {line_number}: blank JSONL lines are not allowed")
    27	                    continue
    28	                try:
    29	                    record = json.loads(line)
    30	                except json.JSONDecodeError as exc:
    31	                    errors.append(f"line {line_number}: invalid JSON: {exc.msg}")
    32	                    continue
    33	                if not isinstance(record, dict):
    34	                    errors.append(f"line {line_number}: record must be a JSON object")
    35	                    continue
    36	                records.append(record)
    37	                missing = REQUIRED_FIELDS - record.keys()
    38	                if missing:
    39	                    errors.append(f"line {line_number}: missing fields: {', '.join(sorted(missing))}")
    40	                    continue
    41	                if not isinstance(record["id"], str) or not re.fullmatch(r"[0-9a-f]{16}", record["id"]):
    42	                    errors.append(f"line {line_number}: id must be 16 lowercase hexadecimal characters")
    43	                elif isinstance(record["root"], str) and isinstance(record["path"], str):
    44	                    expected_id = hashlib.sha256(f"{record['root']}/{record['path']}".encode("utf-8")).hexdigest()[:16]
    45	                    if record["id"] != expected_id:
    46	                        errors.append(f"line {line_number}: id does not match SHA-256(root/path)[:16]")
    47	                if not isinstance(record["size"], int) or isinstance(record["size"], bool) or record["size"] < 0:
    48	                    errors.append(f"line {line_number}: size must be a non-negative integer")
    49	                if not isinstance(record["status"], str) or record["status"] not in VALID_STATUSES:
    50	                    errors.append(f"line {line_number}: invalid status {record['status']!r}")
    51	                if record["root"] not in SOURCE_NAMES:
    52	                    errors.append(f"line {line_number}: unknown source root {record['root']!r}")
    53	                digest = record["sha256"]
    54	                if digest is not None and (not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest)):
    55	                    errors.append(f"line {line_number}: sha256 must be null or 64 lowercase hexadecimal characters")
    56	                try:
    57	                    datetime.fromisoformat(record["mtime"].replace("Z", "+00:00"))
    58	                except (AttributeError, TypeError, ValueError):
    59	                    errors.append(f"line {line_number}: mtime must be an ISO 8601 timestamp")
    60	                if not all(isinstance(record[field], str) for field in ("root", "path", "name", "ext", "mtime")):
    61	                    errors.append(f"line {line_number}: root, path, name, ext, and mtime must be strings")
    62	        ids = [record.get("id") for record in records if isinstance(record.get("id"), str)]
    63	        if len(ids) != len(set(ids)):
    64	            errors.append("registry contains duplicate ids")
    65	    except OSError as exc:
    66	        return [f"cannot read registry: {exc}"]
    67	
    68	    try:
    69	        coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
    70	    except (OSError, json.JSONDecodeError) as exc:
    71	        return errors + [f"cannot read coverage report: {exc}"]
    72	    if not isinstance(coverage, dict):
    73	        return errors + ["coverage report must be an object"]
    74	    if coverage.get("formula") != "indexed / accessible":
    75	        errors.append("coverage formula must be 'indexed / accessible'")
    76	    sources = coverage.get("sources")
    77	    if not isinstance(sources, dict):
    78	        return errors + ["coverage sources must be an object"]
    79	    for name in SOURCE_NAMES:
    80	        source = sources.get(name)
    81	        if not isinstance(source, dict):
    82	            errors.append(f"{name}: missing coverage entry")
    83	            continue
    84	        if source.get("status") == "INCOMPLETE":
    85	            if not source.get("reason"):
    86	                errors.append(f"{name}: INCOMPLETE source must include a reason")
    87	            if any(source.get(field) is not None for field in (*COUNT_FIELDS, "coverage_percent")):
    88	                errors.append(f"{name}: INCOMPLETE metrics must be null, not guessed")
    89	        elif source.get("status") == "COMPLETE":
    90	            values = [source.get(field) for field in COUNT_FIELDS]
    91	            if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in values):
    92	                errors.append(f"{name}: COMPLETE source counts must be non-negative integers")
    93	                continue
    94	            if not (
    95	                source["indexed"] <= source["accessible"] <= source["discovered"]
    96	                and source["skipped"] <= source["accessible"]
    97	                and source["error"] <= source["discovered"]
    98	            ):
    99	                errors.append(f"{name}: source counts are inconsistent")
   100	            expected = source["indexed"] / source["accessible"] * 100 if source["accessible"] else None
   101	            actual = source.get("coverage_percent")
   102	            if (expected is not None and (not isinstance(actual, (int, float)) or isinstance(actual, bool))) or actual != expected:
   103	                errors.append(f"{name}: coverage_percent does not match indexed / accessible")
   104	        else:
   105	            errors.append(f"{name}: status must be COMPLETE or INCOMPLETE")
   106	
   107	    total = coverage.get("total")
   108	    if not isinstance(total, dict):
   109	        errors.append("coverage total must be an object")
   110	    elif any(source.get("status") == "INCOMPLETE" for source in sources.values()):
   111	        if total.get("status") != "INCOMPLETE":
   112	            errors.append("total must be INCOMPLETE when any source is INCOMPLETE")
   113	        elif any(total.get(field) is not None for field in (*COUNT_FIELDS, "coverage_percent")):
   114	            errors.append("INCOMPLETE total metrics must be null, not guessed")
   115	    elif total.get("status") == "COMPLETE":
   116	        values = [total.get(field) for field in COUNT_FIELDS]
   117	        if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in values):
   118	            errors.append("COMPLETE total counts must be non-negative integers")
   119	        else:
   120	            if not (
   121	                total["indexed"] <= total["accessible"] <= total["discovered"]
   122	                and total["skipped"] <= total["accessible"]
   123	                and total["error"] <= total["discovered"]
   124	            ):
   125	                errors.append("total counts are inconsistent")
   126	            expected = total["indexed"] / total["accessible"] * 100 if total["accessible"] else None
   127	            actual = total.get("coverage_percent")
   128	            if (expected is not None and (not isinstance(actual, (int, float)) or isinstance(actual, bool))) or actual != expected:
   129	                errors.append("total coverage_percent does not match indexed / accessible")
   130	    else:
   131	        errors.append("total status must be COMPLETE or INCOMPLETE")
   132	    return errors
   133	
   134	
   135	def main() -> int:
   136	    parser = argparse.ArgumentParser(description=__doc__)
   137	    parser.add_argument("--registry", type=Path, default=Path("registry/file-registry.jsonl"))
   138	    parser.add_argument("--coverage", type=Path, default=Path("registry/coverage-per-source.json"))
   139	    args = parser.parse_args()
   140	    errors = validate_registry(args.registry, args.coverage)
   141	    if errors:
   142	        print("Inventory validation: FAIL")
   143	        for error in errors:
   144	            print(f"- {error}")
   145	        return 1
   146	    print("Inventory validation: PASS")
   147	    return 0
   148	
   149	
   150	if __name__ == "__main__":
   151	    raise SystemExit(main())
~~~~

## FILE: TASK-00004-INVENTORY-AGENT-D.md
~~~~markdown
     1	# TASK-00004: INVENTAR — Agent D / Curator
     2	
     3	**Status:** READY_FOR_EXECUTION
     4	**Owner:** ID-02 (Agent D / Curator)
     5	**Implementation Support:** Coding Agent (nur Tooling, kein Rollenträger)
     6	**Reviewer:** ID-01 (Human Gate)
     7	**Start:** 2026-10-08
     8	
     9	> **Regel: Evidenzmetriken werden nie vorab befüllt.** Alle Zahlen (Coverage, Duplikate, Dateianzahlen) stehen in dieser Spezifikation als Platzhalter `[MEASURED_AFTER_SCAN]` und werden ausschließlich aus dem tatsächlichen Scan erzeugt.
    10	
    11	---
    12	
    13	## Rollen
    14	
    15	| Rolle | Verantwortung | Status |
    16	|---|---|---|
    17	| ID-02 / Agent D (Curator) | Task-Ownership, Datenqualität, Evidence-Kette, Signatur | OWNER |
    18	| Coding Agent | Implementierung der deterministischen Skripte (Scan, Duplikate, Coverage, Katalog) | SUPPORT |
    19	| ID-01 | Review, Approval, Merge-Entscheidung | HUMAN GATE |
    20	
    21	*D owns the task; coding support implements tooling.*
    22	
    23	## Governance
    24	
    25	1. Spezifikation liegt auf `main`.
    26	2. Die gesamte Inventar-Arbeit erfolgt ausschließlich auf `feature/TASK-00004-inventory`.
    27	3. PR nach `main`, Review durch ID-01, Status `AWAITING_REVIEW`.
    28	4. **Kein automatischer Merge.**
    29	
    30	## Aufgabe
    31	
    32	Quellen inventarisieren: Repos, Obsidian-Vault, Google Drive (soweit zugänglich).
    33	
    34	**Wichtig:** Quellrepos bleiben read-only. Keine Änderungen an Quellen. Nur Metadaten erfassen.
    35	
    36	## Input
    37	
    38	- `julianzotter/julianzotter/tools/01_scan_registry.py` (atomarer Scanner)
    39	- Quellen (Zugänglichkeit je Quelle im Report ausweisen):
    40	  - `julianzotter/NEXUS-AI-AEC-ENGINEERIN-KNOWLEDGE-GRAPH`
    41	  - `julianzotter/julianzotter`
    42	  - Obsidian-Vault (lokal oder Drive)
    43	  - Google Drive (falls Zugang vorhanden)
    44	
    45	## Output
    46	
    47	```
    48	registry/
    49	├─ file-registry.jsonl        # 1 Zeile = 1 Datei
    50	├─ duplicates-report.md       # alle Duplikat-Kandidaten, deterministisch
    51	├─ catalog-draft.yaml         # Status = DRAFT
    52	├─ inventory-summary.txt      # Coverage je Quelle
    53	└─ coverage-per-source.json   # maschinenlesbar
    54	```
    55	
    56	## Datensatz je Datei (file-registry.jsonl)
    57	
    58	| Feld | Beschreibung |
    59	|---|---|
    60	| `id` | SHA-256(root + relpath)[:16], stabil |
    61	| `root`, `path`, `name`, `ext` | Herkunft |
    62	| `size`, `mtime` | Metadaten (mtime ISO 8601) |
    63	| `sha256` | Hash über Bytes, `null` bei Datei > 500 MB |
    64	| `status` | `FOUND` / `SKIPPED` / `ERROR` / `INCOMPLETE` (bei Zugriff verweigert) |
    65	| `duplicate_of` | id der Referenzdatei bei gleichem SHA-256 |
    66	| `duplicate_group` | Gruppen-ID bei mehreren Duplikaten |
    67	
    68	`supersedes` wird **nicht** für Duplikate verwendet, nur für echte Versionsnachfolge.
    69	
    70	## Coverage-Definition
    71	
    72	**Explizite Formel (verbindlich):**
    73	
    74	```
    75	Coverage % = ( indexed / accessible ) × 100
    76	```
    77	
    78	**Definitionen:**
    79	- `discovered`: Dateien auf Quelle laut Dateisystem sichtbar
    80	- `accessible`: Dateien, die lesbar sind (keine Permission-Fehler, keine Locks)
    81	- `indexed`: Dateien, die erfolgreich in `file-registry.jsonl` aufgenommen wurden
    82	- `skipped`: Dateien, die per Ausschlussregel bewusst übersprungen (z.B. `__pycache__`)
    83	- `error`: Dateien, die Fehler beim Lesen erzeugt haben
    84	- `INCOMPLETE`: Quelle war nicht zugänglich (z.B. Google Drive offline, Obsidian-Pfad nicht gefunden)
    85	
    86	**Beispiel:**
    87	```
    88	Quelle A: discovered=100, accessible=98, indexed=95, skipped=2, error=1
    89	Coverage = 95 / 98 = 96.9 %
    90	
    91	Quelle B: INCOMPLETE (kein Zugriff)
    92	Coverage = INCOMPLETE
    93	```
    94	
    95	## Abnahmekriterien
    96	
    97	- [ ] Coverage je Quelle ausgewiesen nach Formel: `indexed / accessible`
    98	- [ ] Inaccessible Quellen als `INCOMPLETE` gekennzeichnet (nicht geraten)
    99	- [ ] Gesamtquote indexed/accessible wird berichtet (Zielwert ≥ 90 %, Abweichungen begründet)
   100	- [ ] Alle Duplikat-Kandidaten deterministisch gelistet (kein Mindestwert)
   101	- [ ] Gleicher SHA-256 → `duplicate_of` bzw. `duplicate_group`
   102	- [ ] Ausschlüsse: `__pycache__`, `.git`, `node_modules`, `$RECYCLE.BIN`, `System Volume Information`
   103	- [ ] Credentials ausgeschlossen: `token.json`, `credentials.json`, `.env*`
   104	- [ ] Atomares Schreiben (`.tmp` → `replace`)
   105	- [ ] Rohdateien unverändert, read-only
   106	- [ ] Alle Metriken stammen aus dem realen Lauf, nichts vorbefüllt
   107	- [ ] Keine Metriken geraten (report `INCOMPLETE` bei Zugriff verweigert)
   108	- [ ] Skript-Versionen und Aufrufparameter im Report dokumentiert (Reproduzierbarkeit)
   109	- [ ] PR gegen `main`, Reviewer ID-01, Status `AWAITING_REVIEW`
   110	- [ ] Nur Task-erforderliche Dateien in PR (keine unrelated changes)
   111	
   112	## Coverage-Tabelle (Vorlage, wird vom Scan befüllt)
   113	
   114	| Quelle | discovered | accessible | indexed | skipped | error | coverage |
   115	|---|---|---|---|---|---|---|
   116	| NEXUS-AI-AEC-ENGINEERIN-KNOWLEDGE-GRAPH | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] |
   117	| julianzotter | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] |
   118	| Obsidian-Vault | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] |
   119	| Google Drive | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] | [MEASURED_AFTER_SCAN] |
   120	
   121	Duplikat-Kandidaten gesamt: `[MEASURED_AFTER_SCAN]`
   122	
   123	## Tooling (durch Coding Agent zu implementieren, deterministisch)
   124	
   125	- `tools/01_scan_registry.py` (vorhanden, ggf. um Coverage-Zähler erweitern)
   126	- `tools/detect_duplicates.py` (neu): Gruppierung nach SHA-256, Report und Felder
   127	- `tools/coverage_stats.py` (neu): Zähler je Quelle nach Formel, JSON und TXT
   128	- Katalog-Generator für `catalog-draft.yaml` (Status = DRAFT)
   129	- Unit-Tests für alle neuen Skripte (Muster: `tests/test_scan_registry.py`)
   130	
   131	## PR-Vorlage (Platzhalter bleiben, bis gemessen)
   132	
   133	```markdown
   134	## Task
   135	- Agent: D (Curator, ID-02)
   136	- Task: TASK-00004
   137	- Support: Coding Agent (Tooling)
   138	
   139	## Coverage (Formula: indexed / accessible)
   140	Siehe registry/inventory-summary.txt: [MEASURED_AFTER_SCAN]
   141	
   142	## Duplikate
   143	Siehe registry/duplicates-report.md: [MEASURED_AFTER_SCAN]
   144	
   145	## Reproduzierbarkeit
   146	Skript-Versionen, Aufrufe, Datum: [FILLED_FROM_RUN]
   147	
   148	## Status
   149	AWAITING_REVIEW, Reviewer ID-01, kein automatischer Merge
   150	```
   151	
   152	## Dependencies
   153	
   154	- Keine vorgelagerten Tasks
   155	- Blockiert: TASK-00001 (Agent A / Reference), startet erst nach Merge durch ID-01
   156	
   157	## Signatur (erst nach realem Lauf)
   158	
   159	```
   160	Agent: D (ID-02)
   161	Datum: [FILLED_AT_SUBMISSION]
   162	Evidence: [PR-LINK]
   163	Status: AWAITING_REVIEW
   164	```
~~~~

## FILE: reports/2026-10-13_parsing-pipeline/NEXUS_PARSE_REPORT_v1.1.md
~~~~markdown
     1	# NEXUS-AI – Technischer Bericht Parsing-Pipeline v1.1
     2	Stand: 2026-10-13 (v1.1: OCR + Vektorindex) · Projekt: NEXUS-AI Multi-LLM System · Autor: Perplexity Computer (Orchestrator)
     3	
     4	## 1 Zweck
     5	Vollständige Inventarisierung der SSOT-Bestände (Google Drive LLM-LOCAL-SSOT) und der NEXUS-relevanten GitHub-Repos (julianzotter) als Basis für Routing, Deduplizierung und Index.
     6	
     7	## 2 Pipeline
     8	1. Quelle A/B/C: drei Drive-Ordner gleichen Namens, rekursiv über Drive API v3 (`files.list`, Paging, max. 4000 Objekte/Root).
     9	2. Metadaten: id, Name, MIME, Größe, Änderungsdatum, MD5.
    10	3. GitHub: `gh repo list` gefiltert auf nexus|ai|llm|agent|ssot.
    11	4. Duplikatprüfung: MD5-Gleichheit über alle Roots.
    12	5. Ausgabe: JSON-Inventar, Bericht (MD), Dashboard (HTML).
    13	
    14	## 3 Ergebnisse
    15	| Kennwert | Wert |
    16	|---|---|
    17	| Objekte gesamt | 858 |
    18	| Datenvolumen | 1.28 GB |
    19	| Root A (1MDir…) | 2 Objekte |
    20	| Root B (1uBR…) | 3 Objekte |
    21	| Root C (1j3F…) = kanonische SSOT | 853 Objekte |
    22	| MD5-Duplikatgruppen | 27 (55 Dateien) |
    23	| Repos | 17 |
    24	
    25	### Dateitypen
    26	- md: 251
    27	- txt: 111
    28	- pdf: 97
    29	- jpg: 93
    30	- ORDNER: 60
    31	- json: 41
    32	- py: 31
    33	- css: 24
    34	- gdoc: 23
    35	- docx: 22
    36	- png: 18
    37	- html: 14
    38	- yaml: 14
    39	- zip: 12
    40	
    41	### Top-Ordner (Root C)
    42	- WORK: 200
    43	- BILDER-RAW: 93
    44	- PDF-RAW: 74
    45	- 26_09_19_BOOKKEEPER_v1.1.0: 69
    46	- scratch_gdoc-meta.ai: 64
    47	- NORMEN: 23
    48	- ALT: 14
    49	- scripts: 8
    50	- nexus_os: 4
    51	- HISTORICAL: 3
    52	- 00_ID_LEDGER.csv: 2
    53	- tests: 2
    54	
    55	## 4 Bewertung / Maßnahmen
    56	- Root C ist die SSOT (https://drive.google.com/drive/folders/1j3FLJkWpQv6xGA_KO0D9sMyA11f0vxBV). A und B sind Reste (≤3 Objekte) → nach Freigabe in C zusammenführen und archivieren.
    57	- Duplikate meist Root ↔ WORK/ → Original in WORK/ belassen, Root-Kopie durch Verweis ersetzen.
    58	- Rohbestände (PDF-RAW, BILDER-RAW) → nächster Schritt: Text-/OCR-Parsing, Chunking, Vektorindex (Chroma/Qdrant laut Work Order 26_10_06).
    59	
    60	## 5 Artefakte
    61	| Datei | Inhalt |
    62	|---|---|
    63	| NEXUS_PARSE_REPORT_v1.1.md | dieser Bericht |
    64	| NEXUS_PARSE_INVENTORY_v1.1.json | Vollinventar (Drive + Repos + Duplikate) |
    65	| NEXUS_PARSE_DASHBOARD_v1.1.html | interaktives Dashboard (Suche, Filter, Charts) |
    66	| parse.py | reproduzierbares Pipeline-Skript |
    67	
    68	## 6 Erweiterung v1.1 – OCR-Parsing und Vektorindex
    69	Umfang: Root C, Textdateien < 2 MB, PDF/Bilder < 5 MB, Google Docs (Export text/plain) = 671 Dateien.
    70	
    71	| Methode | Dateien |
    72	|---|---|
    73	| Text direkt (md, txt, json, yaml, py, csv, html, gdoc) | 418 |
    74	| PDF-Textlayer (pdftotext, max. 30 Seiten) | 23 |
    75	| OCR PDF (Scan, pdftoppm 150 dpi, Seiten 1–3, Tesseract deu+eng) | 44 |
    76	| OCR Bild (jpg/png, Tesseract deu+eng) | 108 |
    77	| Fehler (Netzdrosselung nach 2 Leseversuchen) | 78 |
    78	
    79	Vektorindex: 4 534 Chunks (220 Wörter, Überlappung 40), Vokabular 36 914 Terme (df ≥ 2, < 50 % der Chunks), TF-IDF mit log-TF, L2-normiert, Top-60 Terme je Chunk, Kosinus-Ähnlichkeit im Browser. Datei: NEXUS_VECTOR_INDEX_v1.0.json.
    80	
    81	Grenzen: lexikalischer Index (keine semantischen Embeddings); OCR-Qualität bei Fotos/Plänen begrenzt; PDFs > 5 MB (30 Stk.) nicht verarbeitet. Nächster Schritt: Embeddings (z. B. lokal via Ollama nomic-embed-text) in Chroma/Qdrant über nexus_orch.
~~~~

## FILE: reports/2026-10-13_parsing-pipeline/parse.py
~~~~python
     1	import json,subprocess,collections
     2	def gws(q,tok=None):
     3	    p={"q":q,"pageSize":1000,"fields":"nextPageToken,files(id,name,mimeType,size,modifiedTime,md5Checksum)"}
     4	    if tok:p["pageToken"]=tok
     5	    return json.loads(subprocess.run(["gws","drive","files","list","--params",json.dumps(p)],capture_output=True,text=True).stdout)
     6	roots={"1MDir6QolBWV8S8mNcd1S9Wn7JT_W9Yqx":"LLM_LOCAL_SSOT (A)","1uBRBCYUQTu-4tsu0MZEAN17HfqUlbIgW":"LLM_LOCAL_SSOT (B)","1j3FLJkWpQv6xGA_KO0D9sMyA11f0vxBV":"LLM-LOCAL-SSOT (C)"}
     7	files=[]
     8	for rid,rn in roots.items():
     9	    stack=[(rid,"")];n=0
    10	    while stack and n<4000:
    11	        fid,path=stack.pop();tok=None
    12	        while True:
    13	            r=gws(f"'{fid}' in parents and trashed=false",tok)
    14	            for f in r.get("files",[]):
    15	                n+=1;f["path"]=path+"/"+f["name"];f["root"]=rn
    16	                if f["mimeType"].endswith("folder"):stack.append((f["id"],f["path"]))
    17	                files.append(f)
    18	            tok=r.get("nextPageToken")
    19	            if not tok:break
    20	repos=json.loads(subprocess.run(["gh","repo","list","julianzotter","--limit","200","--json","name,visibility,updatedAt,description,url,diskUsage,primaryLanguage"],capture_output=True,text=True).stdout)
    21	repos=[r for r in repos if any(k in r["name"].lower() for k in["nexus","ai","llm","agent","ssot"])]
    22	md5=collections.defaultdict(list)
    23	for f in files:
    24	    if f.get("md5Checksum"):md5[f["md5Checksum"]].append(f["root"]+f["path"])
    25	dups=[v for v in md5.values() if len(v)>1]
    26	json.dump({"files":files,"repos":repos,"dups":dups},open("inventory.json","w"),ensure_ascii=False)
    27	print(len(files),len(repos),len(dups))
    28	for rn in roots.values():
    29	    fs=[f for f in files if f["root"]==rn];print(rn,len(fs),sum(int(f.get("size",0)) for f in fs))
~~~~

## FILE: reports/2026-10-13_parsing-pipeline/ocr.py
~~~~python
     1	import json,subprocess,os,concurrent.futures as cf,re,time
     2	os.environ["TESSDATA_PREFIX"]=os.path.abspath("tessdata")
     3	d=json.load(open("out/NEXUS_PARSE_INVENTORY_v1.0.json"))
     4	TXT={"md","txt","json","yaml","yml","py","csv","jsonl","html","ps1","js"}
     5	IMG={"jpg","jpeg","png"}
     6	R=[r for r in d["rows"] if r["r"]=="C" and ((r["e"] in TXT and r["s"]<2e6) or (r["e"] in IMG|{"pdf"} and r["s"]<5e6) or r["e"]=="gdoc")]
     7	out={}; 
     8	if os.path.exists("ocr_cache.json"): out=json.load(open("ocr_cache.json"))
     9	def run(r):
    10	    time.sleep(0.4)
    11	    if r["id"] in out: return r["id"],out[r["id"]]
    12	    fn=f"dl/{r['id']}.{r['e']}"; meth=""
    13	    try:
    14	        if r["e"]=="gdoc":
    15	            subprocess.run(["gws","drive","files","export","--params",json.dumps({"fileId":r["id"],"mimeType":"text/plain"}),"--output",fn],capture_output=True,timeout=60)
    16	        else:
    17	            subprocess.run(["gws","drive","files","get","--params",json.dumps({"fileId":r["id"],"alt":"media"}),"--output",fn],capture_output=True,timeout=90)
    18	        if not os.path.exists(fn): return r["id"],{"m":"fehler","t":""}
    19	        if r["e"] in IMG:
    20	            t=subprocess.run(["tesseract",fn,"-","-l","deu+eng"],capture_output=True,text=True,timeout=120).stdout;meth="ocr-bild"
    21	        elif r["e"]=="pdf":
    22	            t=subprocess.run(["pdftotext","-l","30",fn,"-"],capture_output=True,text=True,timeout=60).stdout;meth="pdftext"
    23	            if len(t.strip())<200:
    24	                subprocess.run(["pdftoppm","-r","150","-l","3","-png",fn,f"dl/{r['id']}_p"],timeout=120)
    25	                t="";meth="ocr-pdf"
    26	                for p in sorted(x for x in os.listdir("dl") if x.startswith(r["id"]+"_p")):
    27	                    t+=subprocess.run(["tesseract","dl/"+p,"-","-l","deu+eng"],capture_output=True,text=True,timeout=120).stdout
    28	        else:
    29	            t=open(fn,encoding="utf-8",errors="ignore").read();meth="text"
    30	        return r["id"],{"m":meth,"t":re.sub(r"\s+"," ",t)[:60000]}
    31	    except Exception as e: return r["id"],{"m":"fehler","t":""}
    32	    finally:
    33	        for x in os.listdir("dl"):
    34	            if x.startswith(r["id"]): os.remove("dl/"+x)
    35	t0=time.time()
    36	with cf.ThreadPoolExecutor(3) as ex:
    37	    for i,(k,v) in enumerate(ex.map(run,R)):
    38	        out[k]=v
    39	        if i%50==0: print(i,len(R),int(time.time()-t0),flush=True); json.dump(out,open("ocr_cache.json","w"))
    40	json.dump(out,open("ocr_cache.json","w"))
    41	import collections;print(collections.Counter(v["m"] for v in out.values()))
~~~~

## FILE: docs/concepts/2026-10-13/README.md
~~~~markdown
     1	# Nexus: Voice und Normen-Parser
     2	
     3	Stand: 2026-10-13. Dokumentierter Integrationsentwurf, keine aktive Pipeline.
     4	
     5	- [Quellenkatalog](catalog.json): Drive-IDs, Formate, Änderungsstände und Prüfgrenzen.
     6	- [Inhaltsprüfung](REVIEW.md): Befunde, Gegenprüfung und Freigabekriterien.
     7	- [Integration und Sync](INTEGRATION.md): Komponenten, Beziehungen und Umsetzungsschritte.
     8	- [SKILL-Textsnapshot](sources/pdf-normen-parser-skill.extracted.txt): lesbarer Connector-Text; kein verifizierter Originaldatei-Export und kein installierter Skill.
     9	
    10	Die Originale bleiben in [Google Drive](https://drive.google.com/drive/folders/1WQkvQDTlWfcHvKDrXtIYU8P4HZyYv0lA). Die gesamte Transkriptions-API-Dokumentation wird über ihre Quelle referenziert. Es wurden keine Audiodateien an Anbieter gesendet, keine Cloud-Dienste aktiviert und keine kostenpflichtigen Aufträge erstellt.
    11	
    12	Der vorhandene [VIBE-CODER-Prototyp, PR #3](https://github.com/julianzotter/nexus-platform/pull/3), bleibt ein separater UI-Prototyp. Gemeinsame Oberfläche ist ein Ziel; daraus folgt noch keine sichere Schlüsselverwaltung, Mehragentensteuerung oder Echtzeitfunktion.
    13	
    14	## Prüfgrenze
    15	
    16	Textinhalte aus Markdown, DOCX, PDF und konvertiertem Google Doc wurden gelesen. Der lokale Prozessstart scheitert an der Ausführungsumgebung; daher keine visuelle DOCX/PDF-Prüfung, keine Originalbyte-Hashes und keine Ausführung der vorgeschlagenen Parser. Die nachträglich erwähnte neue Word-Konvertierung konnte keiner zusätzlichen Datei eindeutig zugeordnet werden. Keine Behauptung verlustfreier Gleichheit dieser Fassungen.
    17	
    18	Der Konzeptkatalog ist absichtlich unter docs abgelegt. Er ersetzt nicht registry/file-registry.jsonl: dessen Validator verlangt reale Inventardaten und berechnete IDs; unbekannte Größen, Hashes und Abdeckungswerte werden nicht erfunden.
~~~~

## FILE: docs/concepts/2026-10-13/REVIEW.md
~~~~markdown
     1	# Inhaltsprüfung und unabhängige Gegenprüfung
     2	
     3	Stand 2026-10-13. Ergebnis: Konzepte dokumentarisch integrierbar; produktive Freigabe ausstehend.
     4	
     5	## Quellen und Verfahren
     6	
     7	[S1: SKILL.md](https://drive.google.com/file/d/1vo_0gccV1Vg-lUrGlCzmazYPqVlyeH7p/view), [S2: Human-Transcription-Markdown](https://drive.google.com/file/d/1tMW2Km2Kj_2JUfK-r54EN99PUGc3RoVI/view). Weitere Fassungen und Metadaten: [Katalog](catalog.json).
     8	
     9	Primärprüfung: lesbarer Text aller katalogisierten Dateien. Unabhängiger Agent independent_concept_review prüfte S1 und S2 lesend und lieferte eigenständige Gegenbefunde. Das ist eine zweite Agentenprüfung, kein Nachweis eines anderen Modellherstellers und keine fachliche Freigabe durch einen Prüfingenieur. Alle sechs Gegenbefunde wurden übernommen. Keine Runtime- oder visuelle Layoutprüfung.
    10	
    11	## Priorisierte Befunde
    12	
    13	| ID | Priorität / Quelle | Befund und Konsequenz | Abnahmekriterium |
    14	|---|---|---|---|
    15	| F01 | P1, S2: How it works, mode, turnaround_time | Datei-URL und späterer Callback; live bedeutet bezahlter Auftragsmodus. Kein belegter Echtzeit-/WebRTC-/MCP-Stream. | Async-Adapter außerhalb der Live-Gesprächsschleife; eigene Streaming-Schnittstelle separat evaluieren. |
    16	| F02 | P1, S1: Kernprinzip, Parser-Auswahl | Parser/OCR-Extrakt als alleinige Ground Truth kann Fehler konservieren. Dokumentmedian >50 Zeichen übersieht einzelne Scan-/Fehlerseiten. | Originalbytes, separate Extrakthashes, Werkzeug-/Modellversionen und Konfiguration erhalten; seitenweise Prüfergebnisse; Formeln, Tabellen und Symbole gegen Originalansicht prüfen. |
    17	| F03 | P1, S1: Pydantic-Schema | Ein source_hash und eine page pro Chunk genügen für mehrere Blöcke/Seiten nicht. Version optional, Kapitelbeispiel ohne Normausgabe. | source_refs[] mit doc_id, Ausgabe, block_id, Hash, Seite/BBox; getrennte Quell-/Chunk-Hashes; strikte Hash-, Seiten- und BBox-Prüfung. |
    18	| F04 | P1, S1: P3 | abort_if prüft nur new_violations. Alte ungelöste Fehler können bestehen bleiben. | Jede Revision erneut vollständig prüfen; nur valid=true UND leere Gesamtfehlerliste UND bestandene maschinelle Prüfungen zulassen. Fehler, Timeout, Schemaabweichung, Limit → Quarantäne. |
    19	| F05 | P1, S1: P2, Datasets | Hash allein enthält keinen fachlichen Beleg; Valid-Rate auf Gold misst keine Falschfreigaben auf Negativfällen. | Verifizierte Quellblöcke an Reviewer; Negativ-/Delta-Sätze versionieren; falsche Normausgabe, Seiten, Symbole und Einheiten als Pflichtfälle prüfen. |
    20	| F06 | P2, S2: Callbacks, Updates to downloaded files | Wiederholte Callbacks und später korrigierte Ergebnisse können gleich aussehen. Nur order_id zu deduplizieren verliert Korrekturen. | Persistente Jobzustände, authentifizierte Statusabfrage, idempotente Verarbeitung plus neue Ergebnisrevision bei verändertem Inhalt. |
    21	
    22	Weitere Primärbefunde:
    23	
    24	- S1/P1 erzwingt numerische Kapitelnummern. Anhänge wie A.1, Vorworte und unnummerierte Abschnitte brauchen eigene Strukturtypen. Eine Blockzuordnung muss maschinell auf Vollständigkeit geprüft werden.
    25	- S1/Modultabelle enthält Abbildungen und Normprofilfilter; im YAML fehlen explizite entsprechende Stufen. Tabellenzellen, verbundene Zellen, Fußnoten, Formelausschnitte und Einheitenzuordnung benötigen eigene Artefakte und Tests.
    26	- S1/Schutzregeln sind ein vorgeschlagener Umgang mit Lizenzen, kein belegter Rechtsnachweis. Öffentlich lesbar ist kein maschinenprüfbarer Nachweis eines Nutzungsrechts. Die Ein-Satz-Regel wird nicht als rechtliche Freigabe übernommen. Pro Quelle Rechtebeleg, erlaubte Zwecke und Zielgruppen erfassen; ungeklärte Exporte sperren.
    27	- S2 enthält Anbietertext und kopierte Beispiele mit Markdown-Escapes/HTML-Entities, nicht bereits ausführbaren Adaptercode. Beispiele unverändert als Evidenz behandeln und gesonderte validierte Request-Fixtures erstellen.
    28	- S2/auto_retranscribe kann einen zusätzlichen bezahlten Human-Auftrag auslösen. Im ersten Adapter standardmäßig deaktivieren; separate Preisprüfung und explizite Beauftragung.
    29	- Drei API-Schlüssel allein gewährleisten keine unabhängige Prüfung. Planer und Reviewer benötigen getrennte Kontexte, einen gemeinsamen unveränderten Belegsatz und dokumentierte Konfliktauflösung.
    30	
    31	## Fassungsabgleich
    32	
    33	SKILL.md, DOCX, PDF und das konvertierte Google Doc enthalten dieselben zentralen Konzeptabschnitte. Eine vollständige Gleichheit ist nicht nachgewiesen.
    34	
    35	Der PDF-Textabruf verbindet beispielsweise pdf_sha256: Hash mit class TextBlock und endet im Dataset-Satz auf retrieva. Der DOCX-Abruf enthält den vollständigen retrieval-Satz, hängt aber die Modultabelle ans Textende. Das können Export- oder Extraktionseffekte sein; ohne Seitenrendering ist die Ursache offen. Code aus diesen Extrakten nicht als ausführbar freigeben.
    36	
    37	Die vom Nutzer anschließend erwähnte neue DOCX-Konvertierung ist noch nicht eindeutig durch eine zusätzliche Drive-ID identifiziert. Konvertierungsrichtung und führende Fassung nicht aus Dateinamen ableiten.
    38	
    39	## Externe Plausibilisierung
    40	
    41	- [GoTranscript API](https://gotranscript.com/api): Auftrags-/Callback-Modell; vor Adapterbau aktuellen Vertrag und produktbezogene Parameter erneut abgleichen.
    42	- [PyMuPDF Text](https://pymupdf.readthedocs.io/en/latest/recipes-text.html): Extraktionsreihenfolge kann von der Lesereihenfolge abweichen. Ein Extrakt allein belegt keine Layouttreue.
    43	
    44	## Noch offen
    45	
    46	Originaldateien herunterladen und hashen, PDF-/Word-Seiten rendern, Symbole/Tabellen visuell abgleichen; kanonische Bearbeitungsfassung festlegen; Parser- und Adapterimplementierungen erstellen und gegen unabhängige Fixtures testen. Der lokale Prozessstart scheitert aktuell an einem Infrastrukturfehler, nicht an einer abgeschlossenen negativen Inhaltsprüfung.
~~~~

## FILE: docs/concepts/2026-10-13/INTEGRATION.md
~~~~markdown
     1	# Integrations- und Sync-Entwurf
     2	
     3	Status: Vorschlag mit verknüpften Quellen; keine laufende Synchronisation, kein Deployment.
     4	
     5	## Zielstruktur und Beziehungen
     6	
     7	1. Drive bewahrt bearbeitbare Originale und Formatvarianten. Eine führende Fassung wird je Konzept explizit gewählt. Für den Parser ist SKILL.md der Vorschlag, solange keine neuere fachliche Word-Fassung bestätigt ist.
     8	2. GitHub nexus-platform versioniert geprüfte Spezifikationen, Code, Testfälle und Reviewentscheidungen. Der Katalog verbindet Drive-Datei-ID, Revision/Änderungszeit, Originalhash, Format und Konzept-ID.
     9	3. Nexus verwendet nur freigegebene Artefakte. Dokumente und Transkripte sind Quellenmaterial, niemals automatisch Agentenanweisungen.
    10	4. Die vorhandene Dateiinventur bleibt getrennt: Ihr Schema und die gemessene Abdeckung werden nicht mit Konzept-IDs oder geschätzten Quellhashes überschrieben.
    11	
    12	Beziehungsmodell: Konzept → Quellrevision → Formatvariante/abgeleitetes Artefakt → Prüfbericht → Freigabe → konsumierendes Modul.
    13	Beziehungen erhalten Typen wie derived_from, reviewed_by, supersedes und used_by. Gleicher Titel bedeutet weder gleiche Bytes noch gleichen Inhalt.
    14	
    15	## Drei Komponenten
    16	
    17	| Komponente | Eingang / Ausgang | Rolle und Grenze |
    18	|---|---|---|
    19	| Live-Gespräch | Mikrofonereignisse → Audioantworten und vorläufiges Transkript | Gemeinsame Oberfläche; Mensch hat Vorrang, Antworten abbrechbar, nur ein KI-Sprecher gleichzeitig. Anbieteradapter separat verifizieren. |
    20	| Transkriptionsnachbearbeitung | Freigegebene Aufnahme → Async-Auftrag → versioniertes Ergebnis | GoTranscript-Kandidat für spätere Korrektur/Benchmark. Keine Voraussetzung für flüssiges Sprechen. |
    21	| Normen-Wissenspipeline | Originaldokument → Extrakt → geprüfte Quellenstellen/Chunks | Original und Ableitungen getrennt; Normausgabe und nationale Anhänge eindeutig; Export nur mit bestandenen Prüfungen. |
    22	
    23	Gemeinsamer Nenner ist ein Evidence-Register. Ein Sprachturn referenziert transcript_revision und gegebenenfalls freigegebene norm_chunk_ids. Eine spätere Transkriptkorrektur überschreibt keinen alten Prüfbericht: Sie erzeugt eine neue Revision und markiert abhängige Entscheidungen als erneut prüfbedürftig.
    24	
    25	## Sync-Vertrag, zunächst manuell
    26	
    27	- Explizite Allowlist der Drive-IDs aus catalog.json; keine pauschale Verteilung des gesamten Drives.
    28	- Quellmetadaten und Revision lesen, Originalbytes abrufen, SHA-256 berechnen, Metadaten erneut lesen. Bei Änderung während des Abrufs abbrechen und neu beginnen.
    29	- Native Google Docs als explizit benannte Exportartefakte mit Exportformat/-zeit behandeln; ein Exporthash ist kein Hash einer nativen Originaldatei.
    30	- Abgleich mit zuletzt übernommenem Quellstand und aktuellem Git-Head. Bei Änderungen auf beiden Seiten Konfliktbericht statt Überschreiben.
    31	- Importbranch und PR enthalten Katalogdelta, geprüfte Artefakte, Transformationsprotokoll und Review. Keine direkte main-Aktualisierung.
    32	- Fehlende Dateien als missing/unresolved markieren; keine automatische Löschung. Formatumwandlung erzeugt eine Beziehung, keinen stillen Ersatz.
    33	- Geheimnisse, Rohaufnahmen und lizenzbeschränkte Inhalte nicht automatisch in Git übernehmen. Exportziel und Zugriffsrecht gehören zur Artefaktfreigabe.
    34	- Unveränderter Quellstand erzeugt kein Duplikat. Verschobene/umbenannte Dateien werden über ihre ID zugeordnet.
    35	- Automatisierung erst nach nachgewiesenem manuellen Durchlauf; Zeitplan und Ausführungsidentität sind noch nicht festgelegt.
    36	
    37	## Umsetzung in prüfbaren Schritten
    38	
    39	1. **Quellenbasis abschließen:** neue Word-Fassung identifizieren; Originalhashes, Formatvergleich und kanonische Fassung festhalten. Abnahme: keine ungeklärte Variantenzuordnung.
    40	2. **Belegschema und Validator:** source_refs[], Normausgaben, Blockzuordnung, Hashprüfung, Seiten/BBox und fail-closed Freigabe. Abnahme: manipulierte Belege, alte Restfehler und falsche Ausgaben werden verworfen.
    41	3. **Parser-Prototyp:** kleine selbst erstellte/geeignet lizenzierte Fixtures: Text, Scan, Mischdokument, Tabelle, Anhang A.1, mehrseitige Formel. Abnahme anhand unabhängiger Referenzannotation, nicht nur Zustimmung eines LLM.
    42	4. **Voice-Prototyp:** zuerst Mensch plus eine KI, danach optional zweite KI mit getrennter Reviewrolle. Abnahme: Unterbrechen, Stummschalten, Ende, Verbindungsabbruch und keine Selbstgesprächsschleife.
    43	5. **Async-Adapter:** zunächst lokale Callback-Fixtures und Testmodus. Abnahme: Wiederholung, Korrekturrevision, Refund/Cancel, Fehler und Wiederanlauf. Bezahlte Echtaufträge gesondert beauftragen.
    44	6. **CI/Sync:** Prüfungen an PRs binden; fehlgeschlagene Prüfer blockieren die Freigabe. Cloud Build ist optional für spätere Google-Cloud-Builds/Deployments, kein benötigter Drive-Sync-Baustein.
    45	
    46	GitHub Actions hat tarifabhängige Kontingente; tatsächlichen Accountstatus vor Ausführung prüfen. Cloud-Build-Abrechnung und Guthaben werden durch diesen Entwurf nicht verändert.
    47	
    48	## Freigabeentscheidung
    49	
    50	Planer liefert überprüfbare Anforderungen und Artefakte. Reviewer prüft unabhängig gegen denselben unveränderten Belegsatz; bei fachlichem Streit zweite Gegenposition bzw. menschliche Entscheidung. Gespeichert werden Befunde, Quellen, Tests und Entscheidungen, keine freien internen Gedankengänge. Fachliche Berechnungen erfolgen durch versionierte Python-Skripte mit Einheiten- und Testnachweisen.
~~~~

## FILE: prototypes/vibe-coder-v2.3/README.md
~~~~markdown
     1	# VIBE CODER v2.3 — imported prototype
     2	
     3	Source: [Google Drive HTML](https://drive.google.com/file/d/1KurGBe1SVcub-ZdkMPIjRUZSrRsCEmHG/view)
     4	
     5	Original title: VIBE CODER v2.3 – Multi‑Provider · Free‑Tier · 3D‑Visual.html
     6	
     7	Drive modification time: 2026-03-16T04:06:05.035Z. Imported: 2026-10-13.
     8	
     9	The HTML source was imported without intentional code changes. It has not been run or deployed. Repository import does not establish production readiness.
    10	
    11	## Observed behavior from source inspection
    12	
    13	- Provider selection with one active provider/key at a time; no three-agent peer-review orchestration.
    14	- Direct browser API requests. Entered keys are stored in localStorage.
    15	- Generated HTML is rendered in an iframe without a sandbox attribute; generated scripts may access the parent origin and stored keys. Do not enter live credentials or render untrusted output until this is addressed.
    16	- The validation stage only checks for non-empty output of a minimum length; its failure does not stop assembly. It is not engineering or code correctness validation.
    17	- No WebRTC voice implementation in this file. Provider endpoints and model availability have not been tested.
    18	
    19	## Nexus integration work
    20	
    21	Move provider credentials to a backend; isolate generated previews; implement explicit planner and independent reviewer roles with separate conversation contexts; enforce validation failures as workflow gates; add the voice layer and interruption handling.
    22	
    23	Retain the original source as a reference while implementing these changes separately.
~~~~

## B Laufzeitnachweise (vom Betreiber berichtet, 2026-10-13, Windows-PC, RTX 4080)
- `pytest orchestrator/tests`: 15 passed (Commit 40dfdd4); vorher 14 passed (1363166).
- `sync_nexus.ps1` @1363166: 3x [OK] – LLM-LOCAL-SSOT\nexus-llm-orchestrator, _INDEX_LNK\BENCHMARK Multi-LLM-Orchestrierung\nexus-llm-orchestrator, LLM-LOCAL-SSOT\nexus-platform; SYNC_STAMP.txt in Drive verifiziert.
- `nexus_orch.cli run private "Kurztest"`: provider=local, model=qwen2.5:7b, text="OK", errors=[]; `ollama ps`: 100% GPU, CONTEXT 4096 (vor v1.2.0 / num_ctx 16384).
- `nexus_orch.cli status`: perplexity/claude/gpt/gemini/vision = false (keine API-Keys gesetzt), local = true.
- Google Cloud Vision über Perplexity-Connector: Testbild korrekt gelesen ("WAITING? PLEASE TURN OFF YOUR ENGINE").
- Direkter Drive-Upload aus der Perplexity-Sandbox blockiert (Policy), Drive-Ablage nur über lokalen Sync.
