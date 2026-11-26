"""Construct synthetic workflow output using the delivery producer's receipt formats."""
import io
import json
import sys
import unittest
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import nexus_p2_actions as p2


def encode(value):
    return json.dumps(value).encode()


def zip_members(members):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for name, data in members.items():
            archive.writestr(name, encode(data))
    return buffer.getvalue()


class ActionsFixture:
    now = datetime(2026, 1, 1, 3, tzinfo=timezone.utc)
    start = "2026-01-01T02:50:10Z"
    finish = "2026-01-01T02:58:00Z"
    commit = "b" * 40

    def __init__(self):
        self.workflows = {}
        self.runs = {}
        ids = {}
        self.argv = []
        for i, name in enumerate(p2.WORKFLOWS):
            run_id = 101 + i
            self.workflows[name] = {"id": 11+i, "path": ".github/workflows/" + name, "state": "active"}
            self.runs[name] = dict(databaseId=run_id, status="completed", conclusion="success", headSha=self.commit,
                                   createdAt=self.start, updatedAt=self.finish, headBranch="main", attempt=1,
                                   workflowDatabaseId=11+i, url=f"https://github.com/{p2.REPO}/actions/runs/{run_id}")
            ids[name] = {"run_id": run_id, "run_attempt": 1}
        self.monitor = zip_members({"monitor/report.json": {"test": "monitor"}})
        monitor_digest = "sha256:" + p2.sha(self.monitor)
        self.baseline = {"github_commit": self.commit, "max_age_seconds": 3600, "actions": ids,
                         "monitor_artifact": {"id": 111, "digest": monitor_digest}}
        src = dict(repository=p2.REPO, run_id=101, run_attempt=1, head_sha=self.commit,
                   artifact_id=111, run_url=self.runs[p2.MONITOR]["url"],
                   artifact_digest=monitor_digest, run_conclusion="success")
        key = f"{p2.REPO}:101:1:111"
        name = "NEXUS_101_1_111.zip"
        payload = self.monitor
        records = []
        for i in (0, 1):
            receipt = dict(folder=p2.WORK, key=p2.sha(key.encode()), name=name, file_id=f"drive{i}",
                           sha256=p2.sha(payload), source_key=key, state="DELIVERY_VERIFIED",
                           source=src, bytes=len(payload), consumer_ack="NOT_OBSERVED", human_acceptance="PENDING",
                           delivery_status="BYTE_READBACK_VERIFIED", registration_status="NOT_CHECKED",
                           review_status="REVIEW_PENDING")
            records.append(dict(receipt, reused=False, registration_status="REGISTERED", state="PERSISTED_VERIFIED",
                                delivery_status="FILE_VERIFIED", registry_file_id=p2.REGISTRY,
                                registry_sha256="f"*64, provider_version="5"))
            payload = json.dumps(receipt, sort_keys=True).encode()
            key += ":receipt"
            name += ".receipt.json"
        self.docs = {"receipt-111.json": records[0], "receipt-evidence-111.json": records[1],
                     "delivery-status.json": dict(deliveries=records, status="PERSISTED_VERIFIED",
                                                  registration_status="REGISTERED", recorded_at=self.finish),
                     "preflight.json": dict(status="READ_ACCESS_VERIFIED", source="refresh_token",
                                            operation="drive.files.get_work_metadata", folder_id=p2.WORK,
                                            write_test="NOT_RUN", configured=True, missing_names=[],
                                            can_add_children=True, observed_at=self.start)}
        self.archive = zip_members(self.docs)
        self.baseline["delivery_artifact"] = {"id": 222, "digest": "sha256:" + p2.sha(self.archive)}
        self.corrupt = False
        self.missing = False

    def gh(self, args):
        self.argv.append(args)
        if args[:2] == ["workflow", "list"]:
            return encode(list(self.workflows.values()))
        if args[:2] == ["run", "list"]:
            name = args[args.index("--workflow") + 1]
            return encode([self.runs[name]])
        path = args[1]
        if path.endswith("/git/ref/heads/main"):
            return encode({"object": {"sha": self.commit, "type": "commit"}})
        for rid, aid, body, name in ((101, 111, self.monitor, "nexus-monitor-101-1"),
                                     (103, 222, self.archive, "nexus-delivery-state-103-1")):
            if f"runs/{rid}/artifacts?" in path:
                return encode({"artifacts": [] if self.missing else [dict(id=aid, name=name, expired=False,
                                           size_in_bytes=len(body), digest="sha256:"+p2.sha(body))]})
            if path.endswith(f"/artifacts/{aid}/zip"):
                return body + (b"different" if self.corrupt else b"")
        raise AssertionError(f"unexpected gh call {args}")

    def run(self):
        return p2.verify_actions(self.baseline, gh=self.gh, now=self.now)


class P2ActionsTests(unittest.TestCase):
    def test_hash_checked_archive_and_both_actual_receipts(self):
        f = ActionsFixture()
        result = f.run()
        self.assertEqual(["drive0", "drive1"], [d["file_id"] for d in result["deliveries"]])
        self.assertEqual("2026-01-01T03:50:10+00:00", result["valid_until"])
        cmds = [a for a in f.argv if a[:2] == ["run", "list"]]
        self.assertEqual(len(cmds), 3)
        self.assertTrue(all("--status" not in a for a in cmds))

    def test_final_actions_read_blocks_new_run_attempt_or_head(self):
        for case in ("stable", "new_id", "rerun", "failed", "main_advanced"):
            with self.subTest(case=case):
                fixture = ActionsFixture()
                evidence = fixture.run()
                if case == "stable":
                    self.assertTrue(p2.confirm_latest(fixture.baseline, evidence, gh=fixture.gh))
                    self.assertEqual(fixture.argv[-1][-1], f"repos/{p2.REPO}/git/ref/heads/main")
                    continue
                if case == "main_advanced":
                    fixture.commit = "a" * 40
                else:
                    changes = {"new_id": {"databaseId": 444}, "rerun": {"attempt": 2},
                               "failed": {"conclusion": "failure"}}
                    fixture.runs[p2.POLL].update(changes[case])
                with self.assertRaises(ValueError):
                    p2.confirm_latest(fixture.baseline, evidence, gh=fixture.gh)

    def test_pinned_inputs_and_fail_closed_actions(self):
        cases = [
            ("stale", lambda f: f.baseline.update(max_age_seconds=1)),
            ("old approval", lambda f: f.baseline.update(github_commit="a"*40)),
            ("prior attempt", lambda f: f.baseline["actions"][p2.POLL].update(run_attempt=2)),
            ("new pending run", lambda f: f.runs[p2.POLL].update(status="in_progress", conclusion="")),
            ("disabled workflow", lambda f: f.workflows[p2.DELIVERY].update(state="disabled_manually")),
            ("wrong run id", lambda f: f.runs[p2.MONITOR].update(databaseId=40)),
            ("wrong workflow identity", lambda f: f.runs[p2.DELIVERY].update(workflowDatabaseId=11)),
            ("missing delivery pin", lambda f: f.baseline.pop("delivery_artifact")),
            ("wrong delivery id", lambda f: f.baseline["delivery_artifact"].update(id=223)),
            ("wrong delivery digest", lambda f: f.baseline["delivery_artifact"].update(digest="sha256:" + "e"*64)),
            ("wrong source artifact", lambda f: f.baseline["monitor_artifact"].update(id=881)),
            ("zip digest", lambda f: setattr(f, "corrupt", True)),
            ("missing artifact", lambda f: setattr(f, "missing", True)),
        ]
        for case, change in cases:
            with self.subTest(case):
                f = ActionsFixture()
                change(f)
                with self.assertRaises(ValueError):
                    f.run()

    def test_successful_workflow_with_bad_or_missing_receipts_blocks(self):
        cases = [
            lambda docs: docs.pop("preflight.json"),
            lambda docs: docs["preflight.json"].update(source="access_token"),
            lambda docs: docs["preflight.json"].update(observed_at="2026-01-01T01:00:00Z"),
            lambda docs: docs["receipt-111.json"]["source"].update(run_id=123),
            lambda docs: docs["receipt-111.json"].update(registration_status="NOT_CHECKED"),
            lambda docs: docs["receipt-111.json"].update(sha256="0"*64),
            lambda docs: docs["receipt-evidence-111.json"].update(sha256="0"*64),
            lambda docs: docs["delivery-status.json"].update(deliveries=[]),
            lambda docs: docs["receipt-111.json"].update(folder="different"),
        ]
        for i, change in enumerate(cases):
            with self.subTest(i=i):
                f = ActionsFixture()
                change(f.docs)
                f.archive = zip_members(f.docs)
                f.baseline["delivery_artifact"]["digest"] = "sha256:" + p2.sha(f.archive)
                with self.assertRaises(ValueError):
                    f.run()

    def test_gh_failure_and_invalid_output_are_not_empty_success(self):
        child = MagicMock()
        child.stdout = io.BytesIO(b"private debug")
        child.wait.return_value = 1
        child.__enter__.return_value = child
        with patch.object(p2.subprocess, "Popen", return_value=child):
            with self.assertRaisesRegex(ValueError, "GH_COMMAND_FAILED"):
                p2.gh_read(["run", "list"])
            child.stdout.seek(0)
            with patch.object(p2, "LIMIT", 4), self.assertRaisesRegex(ValueError, "GH_RESPONSE_TOO_LARGE"):
                p2.gh_read(["api", "archive"])
            child.kill.assert_called_once()
        with self.assertRaises(ValueError):
            p2.latest(lambda _: b"[]", p2.MONITOR)
        with self.assertRaises(ValueError):
            p2.latest(lambda _: b"<html>", p2.MONITOR)
        with self.assertRaisesRegex(ValueError, "DUPLICATE_JSON_KEY"):
            p2.strict_json(b'{"a":0,"a":2}')


if __name__ == "__main__":
    unittest.main()
