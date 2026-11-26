"""Production-shaped positive and negative fixtures. No external services or writes."""
import copy
from datetime import datetime, timezone
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import nexus_p2_evidence as p

T = "2026-11-25T16:20:00.000Z"
NOW = datetime(2026, 11, 25, 16, 21, tzinfo=timezone.utc)
GIT = "f" * 40


class Providers:
    def __init__(self, directory):
        self.objects, self.meta, self.deliveries = {}, {}, []
        records, frozen = [], []
        for i in range(13):
            fid = "f" + str(i)
            name = "Bericht.md" if i == 0 else "Artifact-%d.md" % i
            raw = self.put(fid, name, ("Grüße #%s" % i).encode())
            records.append(self.registration(fid))
            frozen.append(dict(file_id=fid, name=name, parent_id=p.WORK, sha256=p.sha(raw)))
        for i in range(2):
            fid = "d" + str(i)
            raw = self.put(fid, fid + ".json", p.encode({"test":i}))
            op = ("%x" % i) * 64
            records.append(dict(self.registration(fid), operation_id=op, ticket_id="nexus-platform#73"))
            self.deliveries.append(dict(file_id=fid, registry_file_id=p.REGISTRY, bytes=len(raw),
                                        sha256=p.sha(raw), key=op, provider_version="17"))
        old = "a" * 64
        note = "SHA256_SCOPE=merged_2026-11-16T21:50:08.974Z_pre_repair_bytes; current_revision_hash_in_JSONL"
        ledger = f"ID,DRIVE_ID,SHA256,NOTE\n0210,f0,{frozen[0]['sha256']},\n0211,{p.LEDGER},{old},{note}\n".encode()
        self.put(p.LEDGER, "ledger.csv", ledger)
        records.append(self.registration(p.LEDGER))
        self.registry_rows = records
        reg = self.put(p.REGISTRY, "file-registry.jsonl", b"\n".join(map(p.encode,records))+b"\n")
        self.plan = dict(schema_version="1.0",ticket_id="nexus-platform#73",artifacts=frozen,
                         ledger_file_id=p.LEDGER,registry_file_id=p.REGISTRY,ledger_report_id="f0",source_ledger_sha256=old)
        drive_item = dict(kind="reports",path="WORK/Bericht.md",id="f0",revision="17",modifiedAt=T,sha256=frozen[0]["sha256"])
        git_item = dict(kind="reports",path="reports/Bericht.md",id="a"*40,size=len(self.objects["f0"]))
        self.drive = dict(root=p.WORK,directoryIds=[p.WORK],items=[drive_item])
        self.git = dict(repo=p.REPO,branch="main",commit=GIT,items=[git_item])
        shot = dict(drive=copy.deepcopy(self.drive),github=copy.deepcopy(self.git),comparison=[dict(name="Bericht.md",status="BYTES_MATCH")])
        revision = p.sha(p.encode(shot))
        shot.update(revision=revision,checkedAt=T)
        manifest = dict(version=1,root="WORK",observedAt=T,items=[dict(path="WORK/Bericht.md",modifiedMs=1000,size=9)])
        self.raw = p.encode(manifest)
        (directory/"work.json").write_bytes(self.raw)
        self.data = dict(version=1,cloudDriveConfigured=True,snapshot=shot,
            attempt=dict(id="run",drive="READ_OK",github="READ_OK",state="VERIFIED",startedAt=T,finishedAt=T),
            localMirror=dict(source="LOCAL_WORK_MIRROR",items=[dict(manifest["items"][0], kind="reports")],observedAt=T))
        self.baseline = dict(github_commit=GIT,max_age_seconds=120,snapshot_sha256=revision,
            ledger=dict(version="17",sha256=p.sha(ledger)),registry=dict(version="17",sha256=p.sha(reg)),
            p0=dict(filename="work.json",sha256=p.sha(self.raw),bytes=len(self.raw),readback_path=p.FEED_PATH+"/local/original"))
        self.baseline["mirrors"] = [dict(drive_id="f0", drive_version="17", git_path=git_item["path"], sha256=frozen[0]["sha256"])]
        mirror=self.data["localMirror"]
        mirror["github"]=None
        mirror["revision"]=p.sha(p.encode({k:mirror[k] for k in ("source","items","github")}))
        spec=self.baseline["p0"]
        mirror["rawManifest"]={"path":spec["readback_path"],"sha256":spec["sha256"],"bytes":spec["bytes"]}
        self.view = dict(origin=p.PANEL, hashes=[revision],status="Quellen gelesen", revision=revision,root=p.WORK,
                         commit=GIT, checkedAt=T,attempt="run")
        self.view["payload"] = copy.deepcopy({k:shot[k] for k in ("drive","github","comparison")})
        self.deny = 401
        self.blob = self.objects["f0"]

    def put(self,fid,name,raw):
        self.objects[fid] = raw
        self.meta[fid] = dict(id=fid,name=name,size=str(len(raw)),parents=[p.WORK],modifiedTime=T,version="17",trashed=False)
        return raw

    def registration(self,fid):
        m = self.meta[fid]
        return dict(artifact_id="gdrive:"+fid,provider_file_id=fid,name=m["name"], provider_version=m["version"],
                    version=T,sha256_scope="complete_raw_file_bytes",content_sha256=p.sha(self.objects[fid]),
                    registration_status="REGISTERED",verification_status="BYTE_READBACK_VERIFIED_REVIEW_PENDING",registered_at=T)

    def feed(self,path=p.FEED_PATH,auth=True):
        if not auth:
            return self.deny,"",b""
        return 200,"application/json",p.encode(self.data) if path==p.FEED_PATH else self.raw

    def panel(self): return self.view
    def repair_plan(self,commit): return self.plan
    def drive_meta(self,id): return self.meta[id]
    def drive_raw(self,id): return self.objects[id]
    def drive_inventory(self): return self.drive
    def git_inventory(self): return self.git
    def git_blob(self,id): return self.blob


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path=pathlib.Path(self.tmp.name)
        self.src=Providers(self.path)

    def evaluate(self):
        return p.evaluate_evidence(self.src.baseline,self.path,NOW,io=self.src,deliveries=self.src.deliveries)

    def assert_blocked(self, key):
        self.assertEqual(self.evaluate()[key]["status"],"BLOCKED")

    def test_independent_provider_evidence_chain(self):
        result=self.evaluate()
        self.assertTrue(all(x["status"]=="PASS" for x in result.values()),result)
        self.assertEqual(result["REGISTRY"]["frozen_artifacts"],13)
        self.assertEqual(result["SNAPSHOT"]["byte_matches"],1)
        self.assertEqual(p.stamp(result["SNAPSHOT"]["valid_until"]).minute,22)

    def test_worker_german_uppercase_filename(self):
        self.assertEqual(p.kind("WORK/ARBEITSAUFTRÄGE.md"),"orders")

    def test_missing_required_fields_block(self):
        for part, field, gate in (("snapshot","comparison","SNAPSHOT"),("attempt","drive","SNAPSHOT"),
                                  ("localMirror","observedAt","P0"),("snapshot","drive","DRIVE")):
            with self.subTest(part=part,field=field):
                saved=self.src.data[part].pop(field)
                self.assert_blocked(gate)
                self.src.data[part][field]=saved

    def test_registry_check_rejects_repacked_but_valid_jsonl(self):
        self.src.objects[p.REGISTRY] += b"\n"
        self.assert_blocked("REGISTRY")

    def test_wrong_provider_revision_even_though_bytes_same(self):
        self.src.meta["f3"]["version"]="18"
        self.assert_blocked("REGISTRY")

    def test_frozen13_distinct(self):
        self.src.plan["artifacts"][-1]=self.src.plan["artifacts"][0]
        self.assert_blocked("REGISTRY")

    def test_ledger_cannot_point_to_another_drive_id_even_if_rehashed(self):
        ledger=self.src.objects[p.LEDGER].replace(b"0210,f0,",b"0210,f1,")
        self.src.put(p.LEDGER,"ledger.csv",ledger)
        self.src.baseline["ledger"]["sha256"]=p.sha(ledger)
        self.src.registry_rows[-1]=self.src.registration(p.LEDGER)
        raw=b"\n".join(map(p.encode,self.src.registry_rows))+b"\n"
        self.src.put(p.REGISTRY,"file-registry.jsonl",raw)
        self.src.baseline["registry"]["sha256"]=p.sha(raw)
        self.assert_blocked("REGISTRY")

    def test_delivery_content_mismatch(self):
        self.src.objects["d0"]=b'{"test":9}'
        self.assert_blocked("REGISTRY")

    def test_approved_pair_can_be_renamed(self):
        s=self.src
        s.baseline["mirrors"][0]["git_path"]="reports/Renamed.md"
        s.git["items"][0]["path"]="reports/Renamed.md"
        shot=s.data["snapshot"]
        shot.update(github=s.git,comparison=[])
        revision=p.sha(p.encode({k:shot[k] for k in ("drive","github","comparison")}))
        shot["revision"]=s.baseline["snapshot_sha256"]=revision
        s.view.update(revision=revision,hashes=[revision],payload=copy.deepcopy({k:shot[k] for k in ("drive","github","comparison")}))
        results=self.evaluate()
        self.assertEqual(results["PANEL"]["status"],"PASS")
        binding=results["SNAPSHOT"]["mirrors"][0]
        self.assertEqual(binding,dict(s.baseline["mirrors"][0],git_blob="a"*40))

    def test_unrelated_filename_match_cannot_replace_missing_pair(self):
        self.src.baseline["mirrors"][0]["git_path"]="reports/Missing.md"
        self.assert_blocked("SNAPSHOT")

    def test_duplicate_mapping_never_passes(self):
        self.src.baseline["mirrors"]*=2
        self.assert_blocked("SNAPSHOT")

    def test_raw_p0_requires_an_accepted_producer_binding(self):
        self.src.data["localMirror"].pop("rawManifest")
        self.assert_blocked("P0")

    def test_cached_snapshot_and_local_fallback_do_not_pass(self):
        self.src.data["attempt"].update(state="BLOCKED",drive="DRIVE_CREDENTIAL_MISSING")
        self.assert_blocked("SNAPSHOT")

    def test_full_registry_with_wrong_blob_blocks_sync(self):
        self.src.blob=b"different"
        self.assert_blocked("SNAPSHOT")

    def test_correct_panel_label_cannot_hide_incomplete_panel_dataset(self):
        self.src.view["payload"]["drive"]["items"]=[]
        self.assert_blocked("PANEL")

    def test_new_and_missing_source_rows_are_detected(self):
        self.src.drive["items"].append(dict(self.src.drive["items"][0],id="new"))
        self.assert_blocked("DRIVE")
        self.src.git["items"]=[]
        self.assert_blocked("GITHUB")

    def test_unauth_redirect_is_not_an_acl_pass(self):
        self.src.deny=302
        self.assert_blocked("ACL")

    def test_wrapper_claim_is_not_p0_evidence(self):
        self.src.raw=p.encode({"sha256":p.sha(self.src.raw)})
        self.assert_blocked("P0")

    def test_panel_must_render_full_hash_from_current_attempt(self):
        self.src.view["hashes"]=[self.src.baseline["snapshot_sha256"][:12]]
        self.assert_blocked("PANEL")
        self.src.view["hashes"]=[self.src.baseline["snapshot_sha256"]]
        self.src.view["attempt"]="prior"
        self.assert_blocked("PANEL")

    def test_stale_snapshot_even_if_its_hash_and_run_match(self):
        self.src.baseline["max_age_seconds"]=15
        self.assert_blocked("SNAPSHOT")

    def test_source_drift_during_panel_readback(self):
        changed=dict(self.src.git,commit="e"*40)
        with patch.object(self.src,"git_inventory",side_effect=[self.src.git,changed]):
            self.assert_blocked("PANEL")

    def test_unset_or_unknown_proof_never_redirects_credentials(self):
        for path in ("https://other.example/q",p.FEED_PATH+"/../raw",p.FEED_PATH+"/raw?next=x"):
            self.src.baseline["p0"]["readback_path"]=path
            self.assert_blocked("P0")


if __name__ == "__main__":
    unittest.main()

