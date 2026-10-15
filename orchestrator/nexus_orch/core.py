"""Router + fallback + council + shared-lessons log."""
import datetime as dt, hashlib, json, pathlib, unicodedata
from .providers import Provider, ProviderError

ROOT = pathlib.Path(__file__).resolve().parent.parent

def load_config(path=None):
    return json.loads(pathlib.Path(path or ROOT / "config/routing.json").read_text(encoding="utf-8"))

MIN_COUNCIL = 2

def _norm(s):
    return " ".join(unicodedata.normalize("NFKC", s).casefold().split())

class Orchestrator:
    def __init__(self, cfg=None, providers=None, root=ROOT):
        self.cfg = cfg or load_config()
        self.root = pathlib.Path(root)
        self.providers = providers or {n: Provider(n, c) for n, c in self.cfg["providers"].items()}

    def is_confidential(self, *texts):
        """O-01: Gate unabhaengig von Schreibweise (casefold+NFKC+Whitespace), prueft Prompt UND Systemtext."""
        hay = _norm(" ".join(t or "" for t in texts))
        return any(_norm(m) in hay for m in self.cfg["privacy"]["markers"])

    def classify(self, task, prompt, system=""):
        p = self.cfg["privacy"]
        if self.is_confidential(prompt, system):
            return p["confidential_route"]  # hard gate: confidential never leaves local
        if task not in self.cfg["routes"]:
            raise KeyError(f"unknown task '{task}', known: {sorted(self.cfg['routes'])}")
        return task

    def chain(self, route):
        r = self.cfg["routes"][route]
        return [r["primary"], *r.get("fallback", [])]

    def run(self, task, prompt, system=""):
        route = self.classify(task, prompt, system)
        errors = []
        for name in self.chain(route):
            try:
                res = self.providers[name].complete(prompt, system, self.cfg["default_temperature"])
                out = {"route": route, "provider": name, **res, "errors": errors}
                self._audit(out, prompt)
                return out
            except ProviderError as e:
                errors.append(str(e))
        raise ProviderError(f"all providers failed for route {route}: {errors}")

    def council(self, task, prompt, system=""):
        route = self.classify(task, prompt, system)
        r = self.cfg["routes"][route]
        members = r.get("council_members") or self.chain(route)
        answers = {}
        for n in members:
            try:
                answers[n] = self.providers[n].complete(prompt, system, 0.0)["text"]
            except ProviderError as e:
                answers[n] = None
        valid = {k: v for k, v in answers.items() if v}
        if not valid:
            raise ProviderError("council: no valid answers")
        norm = lambda s: " ".join(s.lower().split())
        groups = {}
        for k, v in valid.items():
            groups.setdefault(norm(v), []).append(k)
        quorum = len(valid) >= MIN_COUNCIL  # O-01: Konsens erst ab 2 gueltigen Antworten
        consensus = quorum and len(groups) == 1
        synth = None
        if quorum and not consensus:
            judge = r["primary"] if r["primary"] in valid else next(iter(valid))
            body = "\n\n".join(f"### {k}\n{v}" for k, v in valid.items())
            synth = self.providers[judge].complete(
                f"Frage:\n{prompt}\n\nAntworten:\n{body}\n\nSynthetisiere: 1) Konsens, 2) Abweichungen je Modell, 3) begruendete Empfehlung.",
                system, 0.0)["text"]
        out = {"route": route, "members": members, "answers": answers, "consensus": consensus, "quorum": quorum,
               "valid_answers": len(valid),
               "synthesis": synth or next(iter(valid.values()))}
        self._audit(out, prompt)
        return out

    def _audit(self, out, prompt):
        d = self.root / "COMMUNICATION/audit"; d.mkdir(parents=True, exist_ok=True)
        rec = {"ts": dt.datetime.now(dt.timezone.utc).isoformat(), "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
               **{k: out[k] for k in ("route", "provider", "consensus") if k in out}}
        with open(d / f"{dt.date.today():%y_%m_%d}_audit.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

REQUIRED_LESSON = ("agent", "context", "condition", "pattern", "evidence")

def write_lesson(lesson, root=ROOT):
    """Shared-Lessons-Layer: conditional reusable pattern, published to COMMUNICATION/lessons."""
    miss = [k for k in REQUIRED_LESSON if not lesson.get(k)]
    if miss:
        raise ValueError(f"lesson missing fields: {miss}")
    lesson = {"id": hashlib.sha1(json.dumps(lesson, sort_keys=True).encode()).hexdigest()[:12],
              "ts": dt.datetime.now(dt.timezone.utc).isoformat(), **lesson,
              "status": "PROPOSED"}  # O-01: Status nie vom Aufrufer ueberschreibbar
    p = pathlib.Path(root) / "COMMUNICATION/lessons/lessons.jsonl"; p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(lesson, ensure_ascii=False) + "\n")
    return lesson

def search_lessons(query, root=ROOT):
    p = pathlib.Path(root) / "COMMUNICATION/lessons/lessons.jsonl"
    if not p.exists():
        return []
    q = query.lower().split()
    rows = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    return [r for r in rows if all(t in json.dumps(r, ensure_ascii=False).lower() for t in q)]
