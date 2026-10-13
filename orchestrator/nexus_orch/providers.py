"""Provider adapters (stdlib only). temperature=0.0 default, deterministic."""
import json, os, urllib.request

class ProviderError(RuntimeError):
    pass

def _post(url, headers, body, timeout=120):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", **headers})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:  # network, HTTP, JSON
        raise ProviderError(f"{url}: {e}") from e

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
        kind, base, model, key = self.cfg["kind"], self.cfg["base_url"], self.cfg["model"], self.key()
        if kind == "openai_compat":
            msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
            h = {"Authorization": f"Bearer {key}"} if key else {}
            d = _post(f"{base}/chat/completions", h, {"model": model, "messages": msgs, "temperature": temperature})
            return {"text": d["choices"][0]["message"]["content"], "citations": d.get("citations", []), "model": model}
        if kind == "anthropic":
            d = _post(f"{base}/v1/messages", {"x-api-key": key, "anthropic-version": "2023-06-01"},
                      {"model": model, "max_tokens": 4096, "system": system, "temperature": temperature,
                       "messages": [{"role": "user", "content": prompt}]})
            return {"text": "".join(b.get("text", "") for b in d["content"]), "citations": [], "model": model}
        if kind == "gemini":
            body = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": temperature}}
            if system:
                body["systemInstruction"] = {"parts": [{"text": system}]}
            d = _post(f"{base}/models/{model}:generateContent?key={key}", {}, body)
            return {"text": d["candidates"][0]["content"]["parts"][0]["text"], "citations": [], "model": model}
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
