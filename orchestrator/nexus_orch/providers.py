"""Provider adapters (stdlib only). Sampling control depends on provider."""
import base64, json, os, urllib.error, urllib.request

class ProviderError(RuntimeError):
    pass

def _post(url, headers, body, timeout=120):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", **headers})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:300]
        hint = " -> Modell fehlt: 'ollama pull <model>' bzw. 'ollama list' pruefen" if e.code == 404 and "11434" in url else ""
        raise ProviderError(f"{url.split('?')[0]}: HTTP {e.code} {detail}{hint}") from e
    except Exception as e:  # network, JSON
        raise ProviderError(f"{url.split('?')[0]}: {e}") from e

class Provider:
    def __init__(self, name, cfg):
        self.name, self.cfg = name, cfg
    def key(self):
        env = self.cfg.get("env_key")
        if env is None:
            return ""
        k = os.environ.get(env)
        if not k:
            raise ProviderError(f"{self.name}: env {env} missing")
        return k
    def available(self):
        try:
            self.key(); return True
        except ProviderError:
            return False
    def complete(self, prompt, system="", temperature=0.0):
        try:
            return self._complete(prompt, system, temperature)
        except ProviderError:
            raise
        except (KeyError, IndexError, TypeError, AttributeError, ValueError) as e:
            # O-01: unerwartete Antwortstruktur -> ProviderError -> Fallback-Kette greift
            raise ProviderError(f"{self.name}: parse error {type(e).__name__}: {e}") from e

    def _complete(self, prompt, system="", temperature=0.0):
        post = lambda u, h, body: _post(u, h, body, self.cfg.get("timeout", 120))
        kind, base, model, key = self.cfg["kind"], self.cfg["base_url"], self.cfg["model"], self.key()
        if kind == "openai_compat":
            msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
            h = {"Authorization": f"Bearer {key}"} if key else {}
            body = {"model": model, "messages": msgs}
            if self.cfg.get("supports_temperature", True):  # O-01: gpt-5 akzeptiert keine Temperatur
                body["temperature"] = temperature
            if self.name == "deepseek":
                mode = self.cfg.get("thinking", "disabled")
                if mode not in ("enabled", "disabled"):
                    raise ProviderError("deepseek: invalid thinking setting")
                body["thinking"] = {"type": mode}
                body.pop("temperature", None)
                if mode == "enabled":
                    body["reasoning_effort"] = self.cfg.get("reasoning_effort", "high")
                body["max_tokens"] = self.cfg.get("max_tokens", 512)
            d = post(f"{base}/chat/completions", h, body)
            return {"text": d["choices"][0]["message"]["content"], "citations": d.get("citations", []), "model": model}
        if kind == "anthropic":
            d = post(f"{base}/v1/messages", {"x-api-key": key, "anthropic-version": "2023-06-01"},
                      {"model": model, "max_tokens": self.cfg.get("max_tokens", 4096), "system": system, "temperature": temperature,
                       "messages": [{"role": "user", "content": prompt}]})
            return {"text": "".join(b.get("text", "") for b in d["content"]), "citations": [], "model": model}
        if kind == "gemini":
            body = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": temperature}}
            if system:
                body["systemInstruction"] = {"parts": [{"text": system}]}
            d = post(f"{base}/models/{model}:generateContent?key={key}", {}, body)
            return {"text": d["candidates"][0]["content"]["parts"][0]["text"], "citations": [], "model": model}
        if kind == "ollama":
            # native API: num_ctx per request, unabhaengig vom App-Regler
            msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
            d = post(f"{base}/api/chat", {}, {"model": model, "messages": msgs, "stream": False,
                      "options": {"temperature": temperature, "num_ctx": self.cfg.get("num_ctx", 16384)}})
            return {"text": d["message"]["content"], "citations": [], "model": model}
        if kind == "gcv_ocr":
            # prompt = image URL (http/https/gs) or local file path
            img = {"source": {"imageUri": prompt}} if prompt.startswith(("http://", "https://", "gs://")) \
                else {"content": base64.b64encode(open(prompt, "rb").read()).decode()}
            d = post(f"{base}/images:annotate?key={key}", {},
                      {"requests": [{"image": img, "features": [{"type": model}]}]})
            r0 = d["responses"][0]
            if "error" in r0:
                raise ProviderError(f"vision: {r0['error'].get('message')}")
            return {"text": r0.get("fullTextAnnotation", {}).get("text", ""), "citations": [prompt], "model": model}
        raise ProviderError(f"unknown kind {kind}")

class MockProvider(Provider):
    """For tests / dry-run."""
    def __init__(self, name, answer="OK", fail=False):
        super().__init__(name, {"kind": "mock", "model": "mock", "env_key": None})
        self.answer, self.fail = answer, fail
    def complete(self, prompt, system="", temperature=0.0):
        if self.fail:
            raise ProviderError(f"{self.name}: forced failure")
        return {"text": self.answer, "citations": [], "model": "mock"}
