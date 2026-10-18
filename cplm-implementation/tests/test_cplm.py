"""Behaviour tests for a bounded local kernel, not external identity/Drive tests."""
import concurrent.futures
import hashlib
import json
import multiprocessing
import os
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
from nexus_cplm.core import GateError, Kernel, resolve_policy


class CPLMTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "source.md").write_text("approved test fixture")
        self.policy = {"folder_id": "test-root", "human_principal": "human-test",
                       "notifications": {"email": {"recipient": "fixture@example.invalid"}},
                       "sources": {"test-fixture:source-1": {"path": "source.md",
                                   "sha256": hashlib.sha256(b"approved test fixture").hexdigest()}},
                       "grants": {"writer": ["execute", "notify"], "receiver": ["ack"],
                                  "review-a": ["review"], "review-b": ["review"],
                                  "review-c": ["review"], "human-test": ["approve"]}}
        self.policy_path = self.root / "policy.json"
        self.policy_path.write_text(json.dumps(self.policy))
        self.kernel = Kernel(self.root / "runtime", self.policy_path)

    def start(self):
        return self.kernel.submit("writer", "WO-TEST:1", "bundle-v1", "receiver", self.kernel.policy_hash)

    def body(self):
        return "---\ntask_id: 'WO-TEST:1'\nstatus: RESULT\nsource_refs: ['test-fixture:source-1']\n---\nResult\n"

    def prepare(self):
        run = self.start()
        self.kernel.result("writer", run, 0, self.body())
        for version, state, actor in [(1, "PUBLISHED", "writer"), (2, "DELIVERED", "writer"),
                                      (3, "ACKNOWLEDGED", "receiver"), (4, "VERIFIED", "receiver")]:
            self.kernel.handoff(actor, run, version, state, "test-fixture:receipt")
        return run

    def manifest(self, run):
        return self.kernel.validate_result("writer", run, self.kernel.get(run)["revision"])

    def reviews(self, run):
        manifest = self.manifest(run)
        for actor, perspective in [("review-a", "software"), ("review-b", "governance"),
                                   ("review-c", "systems")]:
            self.kernel.review(actor, run, perspective, manifest, "PASS")

    def test_human_cannot_supply_peer_review_even_with_review_grant(self):
        self.policy["grants"]["human-test"].append("review")
        self.policy_path.write_text(json.dumps(self.policy))
        self.kernel = Kernel(self.root / "runtime", self.policy_path)
        run = self.prepare()
        manifest = self.manifest(run)
        with self.assertRaisesRegex(GateError, "HUMAN_REVIEW_SEPARATION_REQUIRED"):
            self.kernel.review("human-test", run, "software", manifest, "PASS")
        self.reviews(run)
        self.kernel.release("human-test", run, self.kernel.get(run)["revision"], manifest)
        self.assertEqual(self.kernel.get(run)["execution"], "COMPLETED")

    def test_read_receipt_and_unknown_actor_denied(self):
        with self.assertRaises(GateError):
            self.kernel.submit("writer", "wo", "h", "receiver", "wrong-policy")
        with self.assertRaises(GateError):
            self.kernel.submit("unknown", "wo", "h", "receiver", self.kernel.policy_hash)

    def test_duplicate_delivery_returns_same_logical_run(self):
        run = self.start()
        self.assertEqual(self.start(), run)
        with self.assertRaises(GateError):
            self.kernel.submit("writer", "WO-TEST:1", "different", "receiver", self.kernel.policy_hash)

    def test_parallel_duplicate_submit_creates_one_run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            ids = list(pool.map(lambda _: self.start(), range(8)))
        self.assertEqual(len(set(ids)), 1)

    def test_missing_frontmatter_and_source_denied(self):
        run = self.start()
        for body in ["plain text", "---\nstatus: RESULT\n---\nx", self.body().replace("source_refs: ['test-fixture:source-1']", "source_refs: []")]:
            with self.assertRaises(GateError):
                self.kernel.result("writer", run, 0, body)
        self.assertEqual(self.kernel.get(run)["execution"], "RUNNING")

    def test_result_readback_and_stale_revision(self):
        run = self.start()
        actual = self.kernel.result("writer", run, 0, self.body())
        self.assertEqual(actual, hashlib.sha256(self.body().encode()).hexdigest())
        with self.assertRaises(GateError):
            self.kernel.handoff("writer", run, 0, "PUBLISHED", "receipt")

    def test_concurrent_result_commits_only_one_revision(self):
        run = self.start()
        def attempt(_):
            try:
                self.kernel.result("writer", run, 0, self.body())
                return "COMMITTED"
            except GateError:
                return "REJECTED"
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(attempt, range(2)))
        self.assertCountEqual(results, ["COMMITTED", "REJECTED"])

    def test_crash_after_artifact_then_restart_recovers_without_duplicate(self):
        run = self.start()
        original = self.kernel._persist
        def fail_after_write(target, data):
            original(target, data)
            raise RuntimeError("injected crash after artifact before DB commit")
        self.kernel._persist = fail_after_write
        with self.assertRaises(RuntimeError):
            self.kernel.result("writer", run, 0, self.body())
        restarted = Kernel(self.root / "runtime", self.policy_path)
        self.assertEqual(restarted.get(run)["execution"], "RUNNING")
        self.assertEqual(restarted.submit("writer", "WO-TEST:1", "bundle-v1", "receiver", restarted.policy_hash), run)
        restarted.result("writer", run, 0, self.body())
        self.assertEqual(len(list((self.root / "runtime").glob("*.md"))), 1)

    def test_ack_not_implied_by_sent_and_wrong_recipient_denied(self):
        run = self.start()
        self.kernel.result("writer", run, 0, self.body())
        self.reviews(run)
        with self.assertRaises(GateError):
            self.kernel.release("human-test", run, 1, self.manifest(run))
        with self.assertRaises(GateError):
            self.kernel.handoff("writer", run, 1, "ACKNOWLEDGED", "self-claim")

    def test_three_distinct_reviewers_and_current_bundle(self):
        run = self.prepare()
        self.kernel.review("review-a", run, "software", self.manifest(run), "PASS")
        with self.assertRaises(GateError):
            self.kernel.review("review-a", run, "governance", self.manifest(run), "PASS")
        with self.assertRaises(GateError):
            self.kernel.review("review-b", run, "governance", "old-bundle", "PASS")
        with self.assertRaises(GateError):
            self.kernel.release("human-test", run, 5, self.manifest(run))

    def test_happy_path_requires_actual_test_human_principal(self):
        run = self.prepare()
        self.reviews(run)
        with self.assertRaises(GateError):
            self.kernel.release("writer", run, 5, self.manifest(run))
        self.kernel.release("human-test", run, 5, self.manifest(run))
        self.assertEqual(self.kernel.get(run)["execution"], "COMPLETED")

    def test_changed_artifact_and_policy_invalidate_release(self):
        run = self.prepare()
        self.reviews(run)
        manifest = self.manifest(run)
        (self.root / "runtime" / (run + ".md")).write_text("tampered")
        with self.assertRaisesRegex(GateError, "ARTIFACT_CHANGED_OR_MISSING"):
            self.kernel.release("human-test", run, 5, manifest)
        self.policy_path.write_text(json.dumps({**self.policy, "changed": True}))
        with self.assertRaises(GateError):
            self.kernel.reserve_notification("writer", run, "email")

    def test_notification_unknown_outcome_is_not_blindly_retried(self):
        run = self.start()
        self.assertTrue(self.kernel.reserve_notification("writer", run, "email"))
        restarted = Kernel(self.root / "runtime", self.policy_path)
        self.assertFalse(restarted.reserve_notification("writer", run, "email"))
        restarted.notification_receipt("writer", run, "email", "test-fixture:sent-id")
        self.assertFalse(restarted.reserve_notification("writer", run, "email"))

    def test_child_policy_can_narrow_but_not_relax(self):
        parent_hash = hashlib.sha256(json.dumps(self.policy, sort_keys=True).encode()).hexdigest()
        child = {"folder_id": "child", "parent_id": "test-root", "parent_hash": parent_hash,
                 "grants": {"writer": ["execute"]}}
        self.assertEqual(resolve_policy(self.policy, child)["grants"], {"writer": ["execute"]})
        for change in [{"parent_id": "wrong"}, {"parent_hash": "old"},
                       {"grants": {"writer": ["approve"]}},
                       {"human_principal": "writer"}, {"folder_id": "test-root"}]:
            with self.assertRaises(GateError):
                resolve_policy(self.policy, {**child, **change})

    def test_unresolved_and_changed_sources_block_result(self):
        run = self.start()
        with self.assertRaises(GateError):
            self.kernel.result("writer", run, 0, self.body().replace("test-fixture:source-1", "missing-link"))
        (self.root / "source.md").write_text("changed source")
        with self.assertRaises(GateError):
            self.kernel.result("writer", run, 0, self.body())

    def test_missing_archive_blocks_release(self):
        run = self.prepare()
        self.reviews(run)
        manifest = self.manifest(run)
        (self.root / "runtime" / (run + ".md")).unlink()
        with self.assertRaisesRegex(GateError, "ARTIFACT_CHANGED_OR_MISSING"):
            self.kernel.release("human-test", run, 5, manifest)

    def test_c01_reviews_require_post_result_validation(self):
        run = self.start()
        with self.assertRaisesRegex(GateError, "RESULT_REQUIRED"):
            self.kernel.review("review-a", run, "software", "bundle-v1", "PASS")
        self.kernel.result("writer", run, 0, self.body())
        with self.assertRaisesRegex(GateError, "POST_RESULT_VALIDATION_REQUIRED"):
            self.kernel.review("review-a", run, "software", "bundle-v1", "PASS")
        manifest = self.manifest(run)
        with self.assertRaisesRegex(GateError, "STALE_REVIEW_MANIFEST"):
            self.kernel.review("review-a", run, "software", "bundle-v1", "PASS")
        self.kernel.review("review-a", run, "software", manifest, "PASS")
        with self.kernel._tx() as c:
            saved = json.loads(c.execute("SELECT manifest FROM validations WHERE run_id=?", (run,)).fetchone()[0])
        self.assertEqual(saved["inputs"]["artifact_sha256"], self.kernel.get(run)["artifact_hash"])
        self.assertEqual(saved["inputs"]["policy_sha256"], self.kernel.policy_hash)
        self.assertEqual(saved["validation_receipt"]["checks"]["source_freshness"], "PASS")
        self.assertEqual(saved["validation_receipt_sha256"], hashlib.sha256(
            json.dumps(saved["validation_receipt"], sort_keys=True).encode()).hexdigest())

    def test_c02_source_change_after_reviews_blocks_release(self):
        run = self.prepare()
        self.reviews(run)
        manifest = self.manifest(run)
        (self.root / "source.md").write_text("changed after reviews")
        with self.assertRaisesRegex(GateError, "SOURCE_CHANGED"):
            self.kernel.release("human-test", run, 5, manifest)
        self.assertEqual(self.kernel.get(run)["approved"], 0)
        with self.assertRaisesRegex(GateError, "SOURCE_CHANGED"):
            self.kernel.review("review-a", run, "software", manifest, "PASS")

    def test_code_change_invalidates_validation_and_prior_reviews(self):
        run = self.prepare()
        self.reviews(run)
        manifest = self.manifest(run)
        code = self.root / "different-core.py"
        code.write_text("changed executable revision fixture")
        with patch("nexus_cplm.core.__file__", str(code)):
            with self.assertRaisesRegex(GateError, "CODE_CHANGED_RESTART_REQUIRED"):
                self.kernel.release("human-test", run, 5, manifest)
            with self.assertRaisesRegex(GateError, "CODE_CHANGED_RESTART_REQUIRED"):
                self.manifest(run)

    def test_c03_caller_keys_and_unconfigured_channels_rejected(self):
        run = self.start()
        for key in ["one", "two"]:
            with self.assertRaisesRegex(GateError, "NOTIFICATION_CHANNEL_NOT_CONFIGURED"):
                self.kernel.reserve_notification("writer", run, key)
        with self.assertRaises(TypeError):
            self.kernel.reserve_notification("writer", run, "email", recipient="attacker@example.invalid")
        self.assertTrue(self.kernel.reserve_notification("writer", run, "email"))
        self.assertFalse(self.kernel.reserve_notification("writer", run, "email"))
        with self.kernel._tx() as c:
            self.assertEqual(c.execute("SELECT count(*) FROM outbox").fetchone()[0], 1)

    def test_parallel_notification_reservations_have_one_winner(self):
        run = self.start()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(lambda _: self.kernel.reserve_notification("writer", run, "email"), range(8)))
        self.assertEqual(results.count(True), 1)
        self.assertEqual(results.count(False), 7)

    def test_c04_partial_final_preserved_and_explicitly_recovered(self):
        run = self.start()
        target = self.root / "runtime" / (run + ".md")
        fragment = self.body().encode()[:20]
        target.write_bytes(fragment)
        with self.assertRaisesRegex(GateError, "RECOVERY_REQUIRED"):
            self.kernel.result("writer", run, 0, self.body())
        self.assertEqual(target.read_bytes(), fragment)
        self.assertEqual(self.kernel.get(run)["execution"], "RECOVERY_REQUIRED")
        restarted = Kernel(self.root / "runtime", self.policy_path)
        evidence = Path(restarted.recover_artifact_conflict("writer", run, 1))
        self.assertEqual(evidence.read_bytes(), fragment)
        self.assertFalse(target.exists())
        restarted.result("writer", run, 2, self.body())
        self.assertEqual(target.read_text(), self.body())
        self.assertEqual(evidence.read_bytes(), fragment)

    def test_atomic_stage_crash_never_publishes_partial_final(self):
        run = self.start()
        target = self.root / "runtime" / (run + ".md")
        def partial(stage, data):
            stage.write_bytes(data[:1])
            raise RuntimeError("injected midwrite crash")
        with patch.object(self.kernel, "_write_stage", partial):
            with self.assertRaises(RuntimeError):
                self.kernel.result("writer", run, 0, self.body())
        self.assertFalse(target.exists())
        fragments = list(target.parent.glob("*.stage-*"))
        self.assertEqual(len(fragments), 1)
        restarted = Kernel(target.parent, self.policy_path)
        restarted.result("writer", run, 0, self.body())
        self.assertEqual(target.read_text(), self.body())
        self.assertEqual(fragments[0].read_bytes(), self.body().encode()[:1])

    def test_crash_after_stage_fsync_before_publish_can_retry(self):
        run = self.start()
        target = self.root / "runtime" / (run + ".md")
        with patch("nexus_cplm.core.os.link", side_effect=RuntimeError("crash before publication")):
            with self.assertRaises(RuntimeError):
                self.kernel.result("writer", run, 0, self.body())
        self.assertFalse(target.exists())
        stages = list(target.parent.glob("*.stage-*"))
        self.assertEqual(len(stages), 1)
        self.assertEqual(stages[0].read_text(), self.body())
        Kernel(target.parent, self.policy_path).result("writer", run, 0, self.body())
        self.assertEqual(target.read_text(), self.body())

    def test_source_change_after_result_prevents_validation_receipt(self):
        run = self.start()
        self.kernel.result("writer", run, 0, self.body())
        (self.root / "source.md").write_text("changed before validation")
        with self.assertRaisesRegex(GateError, "SOURCE_CHANGED"):
            self.manifest(run)
        with self.kernel._tx() as c:
            self.assertEqual(c.execute("SELECT count(*) FROM validations").fetchone()[0], 0)

    def test_c05_failed_unknown_and_nonstring_result_statuses_denied(self):
        run = self.start()
        for status in ["FAILED", "FAIL", "UNKNOWN", "COMPLETED", "null", "[]"]:
            with self.subTest(status=status), self.assertRaisesRegex(GateError, "RESULT_STATUS_NOT_ACCEPTED"):
                self.kernel.result("writer", run, 0, self.body().replace("status: RESULT", "status: " + status))
        self.assertEqual(self.kernel.get(run)["execution"], "RUNNING")
        self.assertFalse((self.root / "runtime" / (run + ".md")).exists())

    def test_tampered_validation_receipt_cannot_be_reviewed(self):
        run = self.prepare()
        manifest = self.manifest(run)
        with self.kernel._tx() as c:
            c.execute("UPDATE validations SET manifest=? WHERE run_id=?", ('{}', run))
        with self.assertRaisesRegex(GateError, "STALE_REVIEW_MANIFEST"):
            self.kernel.review("review-a", run, "software", manifest, "PASS")

    def test_dg02_existing_and_dangling_symlinks_enter_safe_recovery(self):
        for dangling in [False, True]:
            with self.subTest(dangling=dangling):
                # Distinct logical runs, one existing and one dangling link target.
                task = "WO-LINK:" + str(dangling)
                run = self.kernel.submit("writer", task, "bundle-v1", "receiver", self.kernel.policy_hash)
                target = self.root / "runtime" / (run + ".md")
                linked = self.root / ("missing.md" if dangling else "source.md")
                before = linked.read_bytes() if linked.exists() else None
                target.symlink_to(linked)
                body = self.body().replace("WO-TEST:1", task)
                with self.assertRaisesRegex(GateError, "RECOVERY_REQUIRED"):
                    self.kernel.result("writer", run, 0, body)
                self.assertEqual(self.kernel.get(run)["execution"], "RECOVERY_REQUIRED")
                evidence = Path(self.kernel.recover_artifact_conflict("writer", run, 1))
                self.assertTrue(evidence.is_symlink())
                self.assertEqual(evidence.readlink(), linked)
                self.assertFalse(target.is_symlink())
                self.kernel.result("writer", run, 2, body)
                self.assertEqual(target.read_text(), body)
                self.assertEqual(linked.read_bytes() if linked.exists() else None, before)

    def test_dg04_duplicate_keys_and_invalid_field_types_rejected(self):
        run = self.start()
        bad = [self.body().replace("status: RESULT", "status: FAILED\nstatus: RESULT"),
               self.body().replace("source_refs: ['test-fixture:source-1']", "source_refs: [[nested]]"),
               self.body().replace("source_refs: ['test-fixture:source-1']", "source_refs: [1]"),
               self.body().replace("source_refs: ['test-fixture:source-1']", "source_refs: [null]"),
               self.body().replace("source_refs: ['test-fixture:source-1']", "source_refs: [test-fixture:source-1, test-fixture:source-1]"),
               self.body().replace("task_id: 'WO-TEST:1'", "task_id: []"),
               self.body().replace("status: RESULT", "status: RESULT\nunknown: value")]
        for body in bad:
            with self.subTest(body=body), self.assertRaises(GateError):
                self.kernel.result("writer", run, 0, body)
        self.assertEqual(self.kernel.get(run)["revision"], 0)
        self.assertFalse((self.root / "runtime" / (run + ".md")).exists())

    def test_dg03_notification_vendor_alias_policy_rejected(self):
        self.policy["notifications"]["gmail"] = dict(self.policy["notifications"]["email"])
        self.policy_path.write_text(json.dumps(self.policy))
        with self.assertRaisesRegex(GateError, "NONCANONICAL_NOTIFICATION_CHANNEL"):
            Kernel(self.root / "runtime", self.policy_path)

    def test_child_cannot_redirect_notifications_or_release_evidence(self):
        parent_hash = hashlib.sha256(json.dumps(self.policy, sort_keys=True).encode()).hexdigest()
        child = {"folder_id": "child", "parent_id": "test-root", "parent_hash": parent_hash}
        for field, changed in [("notifications", {"email": {"recipient": "other@example.invalid"}}),
                               ("release_inputs", {"requirements": {"path": "changed"}})]:
            with self.subTest(field=field), self.assertRaisesRegex(GateError, "PROTECTED_PARENT_FIELD"):
                resolve_policy(self.policy, {**child, field: changed})

    def configure_release_inputs(self):
        self.policy["release_inputs"] = {}
        for role in ["requirements", "schema", "tests", "test_receipt", "dependencies"]:
            path = self.root / (role + ".fixture")
            # Hash binding only: this fixture is never presented as a genuine executed suite receipt.
            path.write_text("explicit test fixture for " + role)
            self.policy["release_inputs"][role] = {"path": path.name,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        self.policy_path.write_text(json.dumps(self.policy))
        self.kernel = Kernel(self.root / "runtime", self.policy_path)

    def test_dg05_release_inputs_bound_and_mutation_blocks_review_and_release(self):
        self.configure_release_inputs()
        run = self.prepare()
        self.reviews(run)
        manifest = self.manifest(run)
        with self.kernel._tx() as c:
            saved = json.loads(c.execute("SELECT manifest FROM validations WHERE run_id=?", (run,)).fetchone()[0])
        self.assertEqual(set(saved["inputs"]["release_inputs"]), set(self.policy["release_inputs"]))
        for role, item in self.policy["release_inputs"].items():
            path = self.root / item["path"]
            original = path.read_bytes()
            path.write_text("mutated evidence")
            with self.subTest(role=role):
                with self.assertRaisesRegex(GateError, "RELEASE_INPUT_CHANGED"):
                    self.manifest(run)
                with self.assertRaisesRegex(GateError, "RELEASE_INPUT_CHANGED"):
                    self.kernel.review("review-a", run, "software", manifest, "PASS")
                with self.assertRaisesRegex(GateError, "RELEASE_INPUT_CHANGED"):
                    self.kernel.release("human-test", run, 5, manifest)
            path.write_bytes(original)
        self.kernel.release("human-test", run, 5, manifest)
        self.assertEqual(self.kernel.get(run)["execution"], "COMPLETED")

    def test_dg05_partial_or_escaping_release_input_map_denied(self):
        self.configure_release_inputs()
        run = self.prepare()
        del self.kernel.policy["release_inputs"]["schema"]
        with self.assertRaisesRegex(GateError, "INCOMPLETE_RELEASE_INPUTS"):
            self.manifest(run)
        self.kernel.policy["release_inputs"] = json.loads(self.policy_path.read_text())["release_inputs"]
        self.kernel.policy["release_inputs"]["schema"]["path"] = "../outside.fixture"
        with self.assertRaisesRegex(GateError, "RELEASE_INPUT_PATH_INVALID"):
            self.manifest(run)

    def test_ds01_actual_process_death_after_rename_reconciles_real_evidence(self):
        run = self.start()
        target = self.root / "runtime" / (run + ".md")
        fragment = b"preserve actual conflicting bytes"
        target.write_bytes(fragment)
        with self.assertRaisesRegex(GateError, "RECOVERY_REQUIRED"):
            self.kernel.result("writer", run, 0, self.body())
        def die_after_rename():
            child = Kernel(target.parent, self.policy_path)
            replace = os.replace
            def rename_and_die(source, destination):
                replace(source, destination)
                os._exit(72)  # No Python exception/finally/transaction rollback handler.
            with patch("nexus_cplm.core.os.replace", rename_and_die):
                child.recover_artifact_conflict("writer", run, 1)
        child = multiprocessing.get_context("fork").Process(target=die_after_rename)
        child.start()
        child.join(5)
        if child.is_alive():
            child.terminate()
            child.join()
            self.fail("recovery child did not exit")
        self.assertEqual(child.exitcode, 72)
        restarted = Kernel(target.parent, self.policy_path)
        self.assertEqual(restarted.get(run)["execution"], "RECOVERY_REQUIRED")
        self.assertFalse(target.exists())
        evidence = Path(restarted.recover_artifact_conflict("writer", run, 1))
        self.assertTrue(evidence.is_file())
        self.assertEqual(evidence.read_bytes(), fragment)
        with restarted._tx() as c:
            event = c.execute("SELECT body FROM events WHERE run_id=? AND kind='CONFLICT_ISOLATED'", (run,)).fetchone()
        self.assertEqual(json.loads(event[0])["evidence"], evidence.name)
        restarted.result("writer", run, 2, self.body())
        self.assertEqual(evidence.read_bytes(), fragment)
        self.assertEqual(target.read_text(), self.body())

    def test_ds01_missing_or_ambiguous_recovery_evidence_fails_closed(self):
        run = self.start()
        target = self.root / "runtime" / (run + ".md")
        target.write_bytes(b"conflict")
        with self.assertRaisesRegex(GateError, "RECOVERY_REQUIRED"):
            self.kernel.result("writer", run, 0, self.body())
        target.unlink()
        with self.assertRaisesRegex(GateError, "RECOVERY_EVIDENCE_MISSING_OR_AMBIGUOUS"):
            self.kernel.recover_artifact_conflict("writer", run, 1)
        for suffix in ["one", "two"]:
            (target.parent / (run + ".conflict-" + suffix)).write_bytes(b"conflict")
        with self.assertRaisesRegex(GateError, "RECOVERY_EVIDENCE_MISSING_OR_AMBIGUOUS"):
            self.kernel.recover_artifact_conflict("writer", run, 1)
        self.assertEqual(self.kernel.get(run)["execution"], "RECOVERY_REQUIRED")
        self.assertEqual(self.kernel.get(run)["revision"], 1)

    def test_ds02_policy_rotation_denies_receipt_and_preserves_unknown_outcome(self):
        run = self.start()
        self.kernel.reserve_notification("writer", run, "email")
        self.policy["revision"] = 2
        self.policy_path.write_text(json.dumps(self.policy))
        restarted = Kernel(self.root / "runtime", self.policy_path)
        with self.assertRaisesRegex(GateError, "UNKNOWN_RUN_OR_STALE_POLICY"):
            restarted.notification_receipt("writer", run, "email", "fixture:sent")
        with restarted._tx() as c:
            row = c.execute("SELECT state,receipt FROM outbox WHERE run_id=?", (run,)).fetchone()
        self.assertEqual(tuple(row), ("OUTCOME_UNKNOWN", None))


if __name__ == "__main__":
    unittest.main()
