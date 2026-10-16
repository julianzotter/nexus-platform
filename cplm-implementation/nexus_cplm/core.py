"""Local CPLM state/commit kernel. Caller authentication is an external boundary."""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import uuid
import yaml
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


class GateError(ValueError):
    """A required invariant or authorization is absent."""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# Detect replacement of the source on disk while this imported runtime is alive.
_LOADED_CODE_HASH = digest(Path(__file__).read_bytes())

def resolve_policy(parent: dict[str, Any], child: dict[str, Any]) -> dict[str, Any]:
    """Child may narrow permissions; it cannot introduce principals/actions."""
    if child.get("parent_id") != parent["folder_id"]:
        raise GateError("MISSING_OR_WRONG_PARENT")
    if child.get("parent_hash") != digest(json.dumps(parent, sort_keys=True).encode()):
        raise GateError("STALE_PARENT")
    if child.get("folder_id") == parent["folder_id"]:
        raise GateError("POLICY_SELF_CYCLE")
    for field in ("human_principal", "source_of_truth", "sources"):
        if field in child and child[field] != parent.get(field):
            raise GateError("PROTECTED_PARENT_FIELD")
    grants = child.get("grants", parent["grants"])
    for actor, actions in grants.items():
        if actor not in parent["grants"] or not set(actions) <= set(parent["grants"][actor]):
            raise GateError("CHILD_RELAXATION")
    return {**parent, **child, "grants": grants}


class Kernel:
    """One SQLite transaction serializes this kernel's writers on one host."""
    def __init__(self, root: Path, policy_path: Path) -> None:
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.policy_path = policy_path.resolve(strict=True)
        self.policy = json.loads(self.policy_path.read_text())
        self.policy_hash = digest(self.policy_path.read_bytes())
        self.db = self.root / "state.sqlite"
        with self._tx() as c:
            c.executescript("""
                CREATE TABLE IF NOT EXISTS runs(
                  id TEXT PRIMARY KEY, task_key TEXT UNIQUE NOT NULL, actor TEXT NOT NULL,
                  policy_hash TEXT NOT NULL, bundle_hash TEXT NOT NULL,
                  revision INTEGER NOT NULL, execution TEXT NOT NULL, handoff TEXT NOT NULL,
                  recipient TEXT NOT NULL, artifact_hash TEXT, approved INTEGER DEFAULT 0);
                CREATE TABLE IF NOT EXISTS events(
                  seq INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT, kind TEXT, body TEXT);
                CREATE TABLE IF NOT EXISTS reviews(
                  run_id TEXT, perspective TEXT, reviewer TEXT, bundle_hash TEXT, verdict TEXT,
                  PRIMARY KEY(run_id,perspective), UNIQUE(run_id,reviewer));
                CREATE TABLE IF NOT EXISTS validations(
                  run_id TEXT PRIMARY KEY, manifest TEXT NOT NULL, manifest_hash TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS outbox(
                  key TEXT PRIMARY KEY, run_id TEXT, state TEXT, receipt TEXT);
            """)

    @contextmanager
    def _tx(self) -> Iterator[sqlite3.Connection]:
        c = sqlite3.connect(self.db, timeout=10, isolation_level=None)
        c.row_factory = sqlite3.Row
        try:
            c.execute("BEGIN IMMEDIATE")
            yield c
            if c.in_transaction:
                c.commit()
        except BaseException:
            if c.in_transaction:
                c.rollback()
            raise
        finally:
            c.close()

    def _event(self, c: sqlite3.Connection, run_id: str, kind: str, body: Any) -> None:
        c.execute("INSERT INTO events(run_id,kind,body) VALUES(?,?,?)",
                  (run_id, kind, json.dumps(body, sort_keys=True)))

    def _guard(self, actor: str, action: str) -> None:
        if digest(self.policy_path.read_bytes()) != self.policy_hash:
            raise GateError("POLICY_CHANGED")
        if action not in self.policy["grants"].get(actor, []):
            raise GateError("NOT_AUTHORIZED")

    def _run(self, c: sqlite3.Connection, run_id: str, revision: int) -> sqlite3.Row:
        row = c.execute("SELECT * FROM runs WHERE id=?", (run_id,)).fetchone()
        if row is None or row["revision"] != revision:
            raise GateError("STALE_REVISION_OR_UNKNOWN_RUN")
        if row["policy_hash"] != self.policy_hash:
            raise GateError("STALE_POLICY_BINDING")
        return row

    def get(self, run_id: str) -> dict[str, Any]:
        with self._tx() as c:
            row = c.execute("SELECT * FROM runs WHERE id=?", (run_id,)).fetchone()
            if row is None:
                raise GateError("UNKNOWN_RUN")
            return dict(row)

    def submit(self, actor: str, task_key: str, bundle_hash: str,
               recipient: str, observed_policy_hash: str) -> str:
        self._guard(actor, "execute")
        if observed_policy_hash != self.policy_hash or not all((task_key, bundle_hash, recipient)):
            raise GateError("MISSING_READ_RECEIPT_OR_INPUT")
        with self._tx() as c:
            old = c.execute("SELECT * FROM runs WHERE task_key=?", (task_key,)).fetchone()
            if old:
                if (old["actor"], old["bundle_hash"], old["recipient"], old["policy_hash"]) != (
                        actor, bundle_hash, recipient, self.policy_hash):
                    raise GateError("IDEMPOTENCY_CONFLICT")
                return old["id"]
            run_id = "CPLM-" + uuid.uuid4().hex
            c.execute("INSERT INTO runs VALUES(?,?,?,?,?,0,'RUNNING','CREATED',?,NULL,0)",
                      (run_id, task_key, actor, self.policy_hash, bundle_hash, recipient))
            self._event(c, run_id, "STARTED", {"actor": actor, "policy": self.policy_hash})
            return run_id

    def _write_stage(self, stage: Path, data: bytes) -> None:
        with stage.open("xb") as output:
            output.write(data)
            output.flush()
            os.fsync(output.fileno())

    def _sync_directory(self) -> None:
        fd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)

    def _persist(self, target: Path, data: bytes) -> None:
        # A crash leaves only an unpublished stage; never publish partial bytes.
        stage = self.root / (target.name + ".stage-" + uuid.uuid4().hex)
        self._write_stage(stage, data)
        try:
            os.link(stage, target)  # atomic create-if-absent, no overwrite
            self._sync_directory()
        except FileExistsError:
            if target.is_symlink() or target.read_bytes() != data:
                raise GateError("ARTIFACT_CONFLICT")
        else:
            if target.read_bytes() != data:
                raise GateError("READBACK_FAILED")
        stage.unlink()
        self._sync_directory()

    def recover_artifact_conflict(self, actor: str, run_id: str, revision: int) -> str:
        """Explicitly isolate conflicting evidence; a later result call may retry."""
        with self._tx() as c:
            self._guard(actor, "execute")
            row = self._run(c, run_id, revision)
            if row["actor"] != actor or row["execution"] != "RECOVERY_REQUIRED":
                raise GateError("RECOVERY_NOT_ALLOWED")
            target = self.root / (run_id + ".md")
            evidence = self.root / (run_id + ".conflict-" + uuid.uuid4().hex)
            if target.exists() or target.is_symlink():
                os.replace(target, evidence)
                self._sync_directory()
            c.execute("UPDATE runs SET execution='RUNNING',revision=revision+1 WHERE id=?", (run_id,))
            self._event(c, run_id, "CONFLICT_ISOLATED", {"evidence": evidence.name})
            return str(evidence)

    def _validate_sources(self, references: Any) -> None:
        if not isinstance(references, list) or not references:
            raise GateError("SOURCES_REQUIRED")
        for ref in references:
            item = self.policy.get("sources", {}).get(ref)
            if not item:
                raise GateError("UNRESOLVED_SOURCE")
            path = (self.policy_path.parent / item["path"]).resolve()
            if not path.is_relative_to(self.policy_path.parent) or not path.is_file():
                raise GateError("SOURCE_PATH_INVALID")
            if digest(path.read_bytes()) != item["sha256"]:
                raise GateError("SOURCE_CHANGED")

    def result(self, actor: str, run_id: str, revision: int, markdown: str) -> str:
        self._guard(actor, "execute")
        if not markdown.startswith("---\n") or "\n---\n" not in markdown[4:]:
            raise GateError("MISSING_FRONTMATTER")
        try:
            metadata = yaml.safe_load(markdown.split("---", 2)[1])
        except yaml.YAMLError as exc:
            raise GateError("INVALID_FRONTMATTER") from exc
        if not isinstance(metadata, dict) or not {"task_id", "status", "source_refs"} <= metadata.keys():
            raise GateError("MISSING_METADATA")
        if metadata["task_id"] != self.get(run_id)["task_key"] or not metadata["source_refs"]:
            raise GateError("INVALID_TASK_OR_SOURCE_LINK")
        self._validate_sources(metadata["source_refs"])
        if metadata["status"] != "RESULT":
            raise GateError("RESULT_STATUS_NOT_ACCEPTED")
        data = markdown.encode("utf-8")
        conflict = False
        with self._tx() as c:
            row = self._run(c, run_id, revision)
            if row["actor"] != actor or row["execution"] != "RUNNING":
                raise GateError("WRONG_OWNER_OR_STATE")
            target = self.root / (run_id + ".md")
            if target.is_symlink():
                raise GateError("SYMLINK_TARGET")
            try:
                self._persist(target, data)
            except GateError as exc:
                if str(exc) != "ARTIFACT_CONFLICT":
                    raise
                c.execute("UPDATE runs SET execution='RECOVERY_REQUIRED',revision=revision+1 WHERE id=?", (run_id,))
                self._event(c, run_id, "ARTIFACT_CONFLICT", {"target": target.name})
                conflict = True
            if not conflict:
                actual = digest(target.read_bytes())
                if actual != digest(data):
                    raise GateError("READBACK_FAILED")
                c.execute("UPDATE runs SET execution='RESULT_VERIFIED',artifact_hash=?,revision=revision+1 WHERE id=?",
                          (actual, run_id))
                self._event(c, run_id, "RESULT_VERIFIED", {"sha256": actual})
        if conflict:
            raise GateError("ARTIFACT_CONFLICT_RECOVERY_REQUIRED")
        return actual

    def _current_inputs(self, row: sqlite3.Row) -> dict[str, Any]:
        if digest(Path(__file__).read_bytes()) != _LOADED_CODE_HASH:
            raise GateError("CODE_CHANGED_RESTART_REQUIRED")
        artifact = self.root / (row["id"] + ".md")
        if artifact.is_symlink() or not artifact.is_file() or digest(artifact.read_bytes()) != row["artifact_hash"]:
            raise GateError("ARTIFACT_CHANGED_OR_MISSING")
        metadata = yaml.safe_load(artifact.read_text().split("---", 2)[1])
        if metadata["status"] != "RESULT" or metadata["task_id"] != row["task_key"]:
            raise GateError("INVALID_RESULT")
        self._validate_sources(metadata["source_refs"])
        sources = {ref: self.policy["sources"][ref]["sha256"] for ref in sorted(metadata["source_refs"])}
        return {"run_id": row["id"], "task_key": row["task_key"],
                "declared_input_bundle": row["bundle_hash"], "artifact_sha256": row["artifact_hash"],
                "policy_sha256": digest(self.policy_path.read_bytes()), "sources": sources,
                "code_sha256": _LOADED_CODE_HASH}

    def validate_result(self, actor: str, run_id: str, revision: int) -> str:
        """Execute local post-result checks and seal their actual receipt.

        This is not a claim that the external integration or test suite ran.
        """
        with self._tx() as c:
            self._guard(actor, "execute")
            row = self._run(c, run_id, revision)
            if row["actor"] != actor or row["execution"] != "RESULT_VERIFIED":
                raise GateError("POST_RESULT_VALIDATION_REQUIRED")
            inputs = self._current_inputs(row)
            receipt = {"kind": "local-post-result-validation-v1", "inputs": inputs,
                       "checks": {"artifact_readback": "PASS", "source_freshness": "PASS",
                                  "result_status": "PASS", "policy_freshness": "PASS"}}
            receipt_json = json.dumps(receipt, sort_keys=True)
            manifest = json.dumps({"inputs": inputs, "validation_receipt": receipt,
                                   "validation_receipt_sha256": digest(receipt_json.encode())}, sort_keys=True)
            manifest_hash = digest(manifest.encode())
            old = c.execute("SELECT manifest_hash FROM validations WHERE run_id=?", (run_id,)).fetchone()
            if old and old["manifest_hash"] != manifest_hash:
                c.execute("DELETE FROM reviews WHERE run_id=?", (run_id,))
            c.execute("INSERT OR REPLACE INTO validations VALUES(?,?,?)", (run_id, manifest, manifest_hash))
            self._event(c, run_id, "POST_RESULT_VALIDATED", {"manifest": manifest_hash, "receipt": receipt})
            return manifest_hash

    def _fresh_manifest(self, c: sqlite3.Connection, row: sqlite3.Row, manifest_hash: str) -> None:
        saved = c.execute("SELECT * FROM validations WHERE run_id=?", (row["id"],)).fetchone()
        if saved is None:
            raise GateError("POST_RESULT_VALIDATION_REQUIRED")
        if saved["manifest_hash"] != manifest_hash or digest(saved["manifest"].encode()) != manifest_hash:
            raise GateError("STALE_REVIEW_MANIFEST")
        if json.loads(saved["manifest"])["inputs"] != self._current_inputs(row):
            raise GateError("STALE_VALIDATION_INPUTS")

    def handoff(self, actor: str, run_id: str, revision: int, state: str, evidence: str) -> None:
        transitions = {"CREATED": "PUBLISHED", "PUBLISHED": "DELIVERED",
                       "DELIVERED": "ACKNOWLEDGED", "ACKNOWLEDGED": "VERIFIED"}
        with self._tx() as c:
            row = self._run(c, run_id, revision)
            action = "ack" if state in {"ACKNOWLEDGED", "VERIFIED"} else "execute"
            self._guard(actor, action)
            required_actor = row["recipient"] if action == "ack" else row["actor"]
            if actor != required_actor or not evidence or transitions.get(row["handoff"]) != state:
                raise GateError("INVALID_HANDOFF_OR_ACK")
            if row["execution"] != "RESULT_VERIFIED":
                raise GateError("RESULT_REQUIRED")
            c.execute("UPDATE runs SET handoff=?,revision=revision+1 WHERE id=?", (state, run_id))
            self._event(c, run_id, state, {"actor": actor, "evidence": evidence})

    def review(self, actor: str, run_id: str, perspective: str, bundle_hash: str, verdict: str) -> None:
        self._guard(actor, "review")
        if perspective not in {"software", "governance", "systems"} or verdict not in {"PASS", "FAIL"}:
            raise GateError("INVALID_REVIEW")
        with self._tx() as c:
            self._guard(actor, "review")
            row = c.execute("SELECT * FROM runs WHERE id=?", (run_id,)).fetchone()
            if row is None or actor == row["actor"]:
                raise GateError("SELF_OR_UNKNOWN_REVIEW")
            if row["execution"] != "RESULT_VERIFIED":
                raise GateError("RESULT_REQUIRED")
            self._fresh_manifest(c, row, bundle_hash)
            try:
                c.execute("INSERT INTO reviews VALUES(?,?,?,?,?)",
                          (run_id, perspective, actor, bundle_hash, verdict))
            except sqlite3.IntegrityError as exc:
                raise GateError("REVIEWER_OR_PERSPECTIVE_ALREADY_USED") from exc
            self._event(c, run_id, "REVIEW", {"reviewer": actor, "perspective": perspective})

    def release(self, actor: str, run_id: str, revision: int, bundle_hash: str) -> None:
        self._guard(actor, "approve")
        if actor != self.policy["human_principal"]:
            raise GateError("HUMAN_GATE_REQUIRED")
        with self._tx() as c:
            self._guard(actor, "approve")
            row = self._run(c, run_id, revision)
            self._fresh_manifest(c, row, bundle_hash)
            reviews = c.execute("SELECT * FROM reviews WHERE run_id=?", (run_id,)).fetchall()
            if row["handoff"] != "VERIFIED" or row["execution"] != "RESULT_VERIFIED":
                raise GateError("HANDOFF_AND_RESULT_REQUIRED")
            if len(reviews) != 3 or any(
                    r["verdict"] != "PASS" or r["bundle_hash"] != bundle_hash for r in reviews):
                raise GateError("THREE_CURRENT_PASS_REVIEWS_REQUIRED")
            artifact = self.root / (run_id + ".md")
            if not artifact.exists() or artifact.is_symlink() or digest(artifact.read_bytes()) != row["artifact_hash"]:
                raise GateError("ARTIFACT_CHANGED_OR_MISSING")
            c.execute("UPDATE runs SET approved=1,execution='COMPLETED',revision=revision+1 WHERE id=?", (run_id,))
            self._event(c, run_id, "HUMAN_GATE", {"actor": actor, "bundle": bundle_hash})

    def notification_key(self, run_id: str, channel: str) -> str:
        config = self.policy.get("notifications", {}).get(channel)
        if not config or not config.get("recipient"):
            raise GateError("NOTIFICATION_CHANNEL_NOT_CONFIGURED")
        return digest(json.dumps({"run": run_id, "channel": channel,
                                  "recipient": config["recipient"], "kind": "result"}, sort_keys=True).encode())

    def reserve_notification(self, actor: str, run_id: str, channel: str) -> bool:
        # Caller selects only an allowlisted channel, never the idempotency key/recipient.
        with self._tx() as c:
            self._guard(actor, "notify")
            key = self.notification_key(run_id, channel)
            row = c.execute("SELECT * FROM runs WHERE id=?", (run_id,)).fetchone()
            if row is None or row["policy_hash"] != self.policy_hash:
                raise GateError("UNKNOWN_RUN_OR_STALE_POLICY")
            old = c.execute("SELECT run_id FROM outbox WHERE key=?", (key,)).fetchone()
            if old:
                return False
            c.execute("INSERT INTO outbox VALUES(?,?,'OUTCOME_UNKNOWN',NULL)", (key, run_id))
            self._event(c, run_id, "NOTIFICATION_RESERVED", {"key": key, "channel": channel,
                        "recipient": self.policy["notifications"][channel]["recipient"]})
            return True

    def notification_receipt(self, actor: str, run_id: str, channel: str, receipt: str) -> None:
        """Receipt is adapter evidence, not authenticated delivery or recipient ACK."""
        with self._tx() as c:
            self._guard(actor, "notify")
            key = self.notification_key(run_id, channel)
            if not receipt:
                raise GateError("RECEIPT_REQUIRED")
            row = c.execute("SELECT * FROM outbox WHERE key=? AND run_id=?", (key, run_id)).fetchone()
            if row is None or row["state"] != "OUTCOME_UNKNOWN":
                raise GateError("INVALID_OUTBOX_STATE")
            c.execute("UPDATE outbox SET state='SENT',receipt=? WHERE key=?", (receipt, key))
            self._event(c, row["run_id"], "NOTIFICATION_SENT", {"receipt": receipt})
