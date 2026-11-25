"""Read-only NEXUS P2 source evidence (Sites v8 private feed, v14 panel).
Caller authenticates the baseline's exact bytes against ID01's out-of-band digest.
"""
import base64
import csv
import hashlib
import io
import json
import os
import re
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlencode

REPO = "julianzotter/nexus-platform"
WORK = "1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP"
REGISTRY = "15m8T5cWbogIup9snzFwiB1g9HqNCoGow"
LEDGER = "1Qso4VQE-cySJdxo6j-MNjxxOc5-GJlrK"
PLAN = "config/control-register-repair-2026-11-16.json"
FEED = "https://nexus-work-sync.julianzotter.chatgpt.site"
FEED_PATH = "/api/v1/feed"
PANEL = "https://nexus-sync-diagnose.julianzotter.chatgpt.site"
MAX_BYTES = 20 * 1024 * 1024
FOLDER = "application/vnd.google-apps.folder"
ORDER = re.compile(r"(?:^|[^a-z0-9])(?:work[-_ ]?orders?|arbeitsauftr[aäÄ]g[e]?|wo[-_][a-z0-9]+)(?:[^a-z0-9]|$)", re.I | re.ASCII)
REPORT = re.compile("report|bericht|audit|protokoll|befund", re.I)
GIT_PATH = re.compile(r"^(?:work|reports?|work[-_]?orders?|usecases|docs|governance|registry)/", re.I)


class Blocked(ValueError):
    """Safe diagnostic, without credentials or remote response bodies."""


def need(ok, reason):
    if not ok:
        raise Blocked(reason)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def is_sha(s, n=64):
    return isinstance(s, str) and re.fullmatch("[a-f0-9]{%d}" % n, s) is not None


def ident(s):
    need(isinstance(s, str) and re.fullmatch(r"[A-Za-z0-9_-]+", s), "Invalid provider ID.")
    return s


def stamp(s):
    t = datetime.fromisoformat(s.replace("Z", "+00:00"))
    need(t.utcoffset() is not None, "Timestamp needs a timezone.")
    return t


def decode(raw):
    def unique(pairs):
        obj = dict(pairs)
        need(len(pairs) == len(obj), "Duplicate JSON field.")
        return obj
    return json.loads(raw.decode("utf-8"), object_pairs_hook=unique,
                      parse_constant=lambda _: need(False, "Non-finite JSON number."))


def encode(value):
    # The verified snapshot contract only contains strings, safe integers and null.
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")


def kind(path):
    parts = path.split("/")
    name = parts[-1]
    if "." in name and not re.search(r"\.(md|txt|docx?|pdf|ya?ml|json|xlsx?|csv|html)$", name, re.I):
        return None
    for candidates in ([name], parts[:-1]):
        if any(ORDER.search(p) for p in candidates):
            return "orders"
        if any(REPORT.search(p) for p in candidates):
            return "reports"
    return None


def sorted_items(items):
    return sorted(items, key=lambda row: (row["path"].encode("utf-16-be"), row["id"].encode("utf-16-be")))


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None


def request(url, headers=None, body=None, local=False):
    handlers = [NoRedirect()]
    if local:
        handlers.append(urllib.request.ProxyHandler({}))
    req = urllib.request.Request(url, headers=headers or {}, data=body)
    try:
        with urllib.request.build_opener(*handlers).open(req, timeout=20) as response:
            raw = response.read(MAX_BYTES + 1)
            need(len(raw) <= MAX_BYTES, "Response exceeded the read limit.")
            return response.status, response.headers.get_content_type(), raw
    except urllib.error.HTTPError as exc:
        return exc.code, "", b""


class Live:
    def __init__(self):
        self._drive = None

    def drive(self):
        if self._drive is None:
            from deliver_work import DriveClient, get_access_token
            self._drive = DriveClient(get_access_token())
        return self._drive

    def drive_meta(self, fid):
        return self.drive().metadata(ident(fid))

    def drive_raw(self, fid):
        return self.drive().read(ident(fid))

    def drive_inventory(self):
        d = self.drive()
        root = decode(d.call("/files/" + WORK + "?" + urlencode({
            "supportsAllDrives": "true", "fields": "id,name,mimeType,trashed,driveId"})))
        need(root["id"] == WORK and root["name"] == "WORK" and root["mimeType"] == FOLDER
             and root["trashed"] is False, "Canonical WORK identity changed.")
        queue, folders, seen, items = [WORK], {WORK: "WORK"}, set(), []
        pages = 0
        while queue:
            group, queue = queue[:15], queue[15:]
            params = {"q": "trashed = false and (" + " or ".join(f"'{i}' in parents" for i in group) + ")",
                      "spaces": "drive", "pageSize": 1000, "supportsAllDrives": "true",
                      "includeItemsFromAllDrives": "true", "corpora": "drive" if root.get("driveId") else "user",
                      "fields": "nextPageToken,incompleteSearch,files(id,name,mimeType,parents,modifiedTime,version,sha256Checksum)"}
            if root.get("driveId"):
                params["driveId"] = root["driveId"]
            while True:
                pages += 1
                need(pages <= 25, "Drive listing exceeds feed scan limit.")
                page = decode(d.call("/files?" + urlencode(params)))
                need(page.get("incompleteSearch") is False and isinstance(page["files"], list), "Incomplete Drive listing.")
                for f in page["files"]:
                    fid = ident(f["id"])
                    need(fid not in seen, "Duplicate Drive ID or moving source.")
                    seen.add(fid)
                    need(len(seen) <= 6000 and len(set(f["parents"]).intersection(group)) == 1, "Ambiguous Drive tree.")
                    parent = next(i for i in f["parents"] if i in group)
                    path = folders[parent] + "/" + f["name"].replace("/", "∕")
                    if f["mimeType"] == FOLDER:
                        folders[fid] = path
                        queue.append(fid)
                    elif f["mimeType"] != "application/vnd.google-apps.shortcut" and kind(path):
                        need(str(f["version"]).isdigit(), "Missing Drive item revision.")
                        stamp(f["modifiedTime"])
                        items.append(dict(kind=kind(path), path=path, id=fid, revision=str(f["version"]),
                                          modifiedAt=f["modifiedTime"], sha256=f.get("sha256Checksum")))
                if not page.get("nextPageToken"):
                    break
                params["pageToken"] = page["nextPageToken"]
        return dict(root=WORK, directoryIds=sorted(folders), items=sorted_items(items))

    def git(self, path):
        from nexus_p2_actions import gh_read
        return decode(gh_read(["api", "--hostname", "github.com", "repos/" + REPO + "/" + path]))

    def git_inventory(self):
        ref = self.git("git/ref/heads/main")["object"]
        need(ref["type"] == "commit" and is_sha(ref["sha"], 40), "GitHub main reference missing.")
        commit = self.git("git/commits/" + ref["sha"])
        tree_id = commit["tree"]["sha"]
        need(commit["sha"] == ref["sha"] and is_sha(tree_id, 40), "GitHub commit/tree mismatch.")
        tree = self.git("git/trees/" + tree_id + "?recursive=1")
        need(tree["sha"] == tree_id and tree["truncated"] is False, "Incomplete Git tree.")
        items = []
        for entry in tree["tree"]:
            path = entry["path"]
            if entry["type"] == "blob" and entry["mode"] in {"100644","100755"} and GIT_PATH.match(path) and kind(path):
                need(is_sha(entry["sha"], 40) and type(entry["size"]) is int and 0 <= entry["size"] < 2**53,
                     "Invalid Git blob metadata.")
                items.append(dict(kind=kind(path), path=path, id=entry["sha"], size=entry["size"]))
        return dict(repo=REPO, branch="main", commit=ref["sha"], items=sorted_items(items))

    def git_blob(self, identity):
        need(is_sha(identity, 40), "Invalid Git blob ID.")
        value = self.git("git/blobs/" + identity)
        need(value["sha"] == identity and value["encoding"] == "base64", "Invalid Git blob response.")
        data = base64.b64decode("".join(value["content"].split()), validate=True)
        blob_id = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        need(blob_id == identity and value["size"] == len(data), "Git blob hash mismatch.")
        return data

    def repair_plan(self, commit):
        need(is_sha(commit, 40), "Invalid approved commit.")
        value = self.git("contents/" + PLAN + "?ref=" + commit)
        need(value["path"] == PLAN and value["type"] == "file", "Repair plan missing from commit.")
        return decode(self.git_blob(value["sha"]))

    def feed(self, path=FEED_PATH, auth=True):
        headers = {"Accept":"application/json", "Cache-Control":"no-cache"}
        if auth:
            key = os.getenv("NEXUS_FEED_MACHINE_KEY")
            need(key, "NEXUS_FEED_MACHINE_KEY unavailable.")
            headers["X-Nexus-Feed-Key"] = key
        return request(FEED + path, headers)

    def panel(self):
        port = int(os.getenv("NEXUS_P2_WEBDRIVER_PORT", "0"))
        session = ident(os.getenv("NEXUS_P2_WEBDRIVER_SESSION", ""))
        need(0 < port <= 65535, "Local WebDriver port unavailable.")
        base = f"http://127.0.0.1:{port}/session/{session}"
        def wd(path, body=None):
            code, _, raw = request(base + path, {"Content-Type":"application/json"}, body, local=True)
            need(code == 200, "Live WebDriver session required.")
            return decode(raw)["value"]
        before = wd("/url")
        need(before.split("#")[0] == PANEL + "/", "WebDriver is not on the production panel.")
        # WebDriver's execute/sync uses POST only on loopback. Expression reads existing tab state.
        script = """
            const f = typeof feedRecord === 'undefined' ? null : feedRecord;
            const root = document.querySelector('#sourceFeed');
            const hashes = [...(root?.querySelectorAll('.feed-info p code[title]') || [])].map(e=>e.title);
            return {origin: location.origin, hashes, status:root?.querySelector('.panel-head [aria-live]')?.textContent,
              attempt:f?.attempt?.id, checkedAt:f?.snapshot?.checkedAt, root:f?.snapshot?.drive?.root,
              commit:f?.snapshot?.github?.commit, revision:f?.snapshot?.revision,
              payload: f?.snapshot && {drive:f.snapshot.drive,github:f.snapshot.github,comparison:f.snapshot.comparison}};
        """
        value = wd("/execute/sync", encode({"script":script, "args":[]}))
        need(wd("/url") == before and value["origin"] == PANEL, "Panel URL changed during readback.")
        return value


def current_file(src, identity):
    before = src.drive_meta(identity)
    data = src.drive_raw(identity)
    after = src.drive_meta(identity)
    need(before == after and before["id"] == identity and before["trashed"] is False
         and str(before["version"]).isdigit() and int(before["size"]) == len(data),
         "Drive source identity, size or revision changed during readback.")
    return before, data


def verify_registry(src, baseline, deliveries):
    plan = src.repair_plan(baseline["github_commit"])
    frozen = plan["artifacts"]
    need(plan["schema_version"] == "1.0" and plan["ticket_id"] == "nexus-platform#73"
         and plan["registry_file_id"] == REGISTRY and plan["ledger_file_id"] == LEDGER,
         "Unexpected canonical repair plan.")
    need(len(frozen) == len(set(r["file_id"] for r in frozen)) == 13, "Expected 13 distinct frozen artifacts.")
    meta, raw = current_file(src, REGISTRY)
    ledger_meta, ledger = current_file(src, LEDGER)
    for key, m, data in (("registry",meta,raw), ("ledger",ledger_meta,ledger)):
        expected = baseline[key]
        need(str(m["version"]) == str(expected["version"]) and sha(data) == expected["sha256"],
             f"{key} revision or digest differs from ID01 baseline.")
    rows = [decode(line) for line in raw.splitlines()]
    need(rows and all(isinstance(r, dict) for r in rows), "Invalid registry JSONL records.")
    by_id = defaultdict(list)
    for row in rows:
        if row.get("provider_file_id"):
            by_id[row["provider_file_id"]].append(row)

    def registered(meta, digest, operation=None):
        # Earlier revisions may remain in the append-only registry.
        current = [r for r in by_id[meta["id"]] if str(r.get("provider_version")) == str(meta["version"])]
        need(current, "Missing provider revision in registry.")
        for r in current:
            need(r["registration_status"] == "REGISTERED" and r["content_sha256"] == digest
                 and r["artifact_id"] == "gdrive:" + meta["id"] and r["name"] == meta["name"]
                 and r["sha256_scope"] == "complete_raw_file_bytes" and r["version"] == meta["modifiedTime"]
                 and r["verification_status"] == "BYTE_READBACK_VERIFIED_REVIEW_PENDING",
                 "Missing or conflicting registration for a current revision.")
            stamp(r["registered_at"])
        if operation:
            need(any(r.get("operation_id") == operation and r.get("ticket_id") == "nexus-platform#73"
                     for r in current), "Delivery registration operation or ticket mismatch.")

    for artifact in frozen:
        m, data = current_file(src, ident(artifact["file_id"]))
        need(m["name"] == artifact["name"] and artifact["parent_id"] in m["parents"]
             and sha(data) == artifact["sha256"], "Frozen artifact is missing or changed.")
        registered(m, artifact["sha256"])
    registered(ledger_meta, sha(ledger))
    reader = csv.DictReader(io.StringIO(ledger.decode("utf-8-sig"), newline=""))
    entries = list(reader)
    ids = [r["ID"] for r in entries]
    need(len(ids) == len(set(ids)) and all(None not in row for row in entries), "Malformed or duplicate ledger row.")
    ledger_rows = {r["ID"]:r for r in entries}
    report = next(d for d in frozen if d["file_id"] == plan["ledger_report_id"])
    need((ledger_rows["0210"]["DRIVE_ID"], ledger_rows["0210"]["SHA256"]) == (report["file_id"], report["sha256"]),
         "Ledger 0210 differs from frozen report.")
    note = "SHA256_SCOPE=merged_2026-11-16T21:50:08.974Z_pre_repair_bytes; current_revision_hash_in_JSONL"
    need((ledger_rows["0211"]["DRIVE_ID"], ledger_rows["0211"]["SHA256"]) == (LEDGER,plan["source_ledger_sha256"])
         and note in ledger_rows["0211"]["NOTE"], "Ledger 0211 hash scope or identity mismatch.")
    need(len(deliveries) == len(set(r["file_id"] for r in deliveries)) == 2, "Two distinct verified delivery receipts required.")
    for receipt in deliveries:
        m, data = current_file(src, ident(receipt["file_id"]))
        need(WORK in m["parents"] and receipt["registry_file_id"] == REGISTRY and is_sha(receipt["key"])
             and str(m["version"]) == str(receipt["provider_version"])
             and len(data) == receipt["bytes"] and sha(data) == receipt["sha256"], "Delivered target readback mismatch.")
        registered(m, sha(data), receipt["key"])
    need(meta == src.drive_meta(REGISTRY) and ledger_meta == src.drive_meta(LEDGER),
         "Registers changed while evidence was checked.")
    return {"registry_id":REGISTRY, "registry_version":str(meta["version"]), "sha256":sha(raw), "rows":len(rows),
            "ledger_id":LEDGER, "ledger_version":str(ledger_meta["version"]), "ledger_sha256":sha(ledger),
            "frozen_artifacts":len(frozen), "delivery_targets":len(deliveries)}


def feed_json(src):
    status, mime, raw = src.feed()
    need(status == 200 and mime == "application/json", "Authenticated feed must return HTTP 200 JSON.")
    data = decode(raw)
    need(isinstance(data, dict) and type(data["version"]) is int and data["version"] == 1, "Unrecognized feed envelope.")
    return data


def cloud_state(data, baseline, now):
    a, s = data["attempt"], data["snapshot"]
    need(data.get("cloudDriveConfigured") is True and isinstance(a, dict) and isinstance(s, dict)
         and a["state"] == "VERIFIED" and a["drive"] == a["github"] == "READ_OK" and not a.get("error")
         and isinstance(a["id"], str) and a["id"], "No successful cloud-provider attempt.")
    start, checked, finish = (stamp(t) for t in (a["startedAt"], s["checkedAt"], a["finishedAt"]))
    need(start <= checked <= finish <= now and (now - checked).total_seconds() <= min(900,baseline["max_age_seconds"]),
         "Stale, future or inconsistent feed timestamp.")
    expected = baseline["snapshot_sha256"]
    payload = {k:s[k] for k in ("drive","github","comparison")}
    need(is_sha(expected) and s["revision"] == expected == sha(encode(payload)), "Snapshot payload digest differs from approved revision.")
    return {"revision":expected, "checked_at":s["checkedAt"], "attempt":a["id"],
            "valid_until":(checked + timedelta(seconds=min(900,baseline["max_age_seconds"]))).isoformat()}


def compare_sources(src, snap, drive, git, approved):
    left, right = defaultdict(list), defaultdict(list)
    for entries, names in ((drive["items"],left), (git["items"],right)):
        for item in entries:
            names[item["path"].rsplit("/", 1)[-1]].append(item)
    by_id = {d["id"]: d for d in drive["items"]}
    by_path = {g["path"]: g for g in git["items"]}
    need(len(by_id) == len(drive["items"]) and len(by_path) == len(git["items"]), "Ambiguous provider IDs/paths.")
    verified = {}
    def check(d, g):
        key = (d["id"], g["path"])
        if key not in verified:
            m, raw = current_file(src, d["id"])
            need(str(m["version"]) == d["revision"] and sha(raw) == d["sha256"] and
                 len(raw) == g["size"] and raw == src.git_blob(g["id"]), "Independent Drive/Git blob comparison differs.")
            verified[key] = dict(drive_id=d["id"], drive_version=d["revision"], git_path=g["path"],
                                 git_blob=g["id"], sha256=d["sha256"])
        return verified[key]

    need(isinstance(approved, list) and len(approved) > 0, "ID01-pinned Drive/Git mirror mapping required.")
    need(len({r["drive_id"] for r in approved}) == len({r["git_path"] for r in approved}) == len(approved),
         "Duplicate approved Drive or GitHub mirror target.")
    bindings = []
    for row in approved:
        d, g = by_id.get(row["drive_id"]), by_path.get(row["git_path"])
        need(d is not None and g is not None and d["revision"] == str(row["drive_version"]) and
             is_sha(row["sha256"]) and d["sha256"] == row["sha256"], "Approved mirror identity, version or SHA missing.")
        bindings.append(check(d, g))

    # v8 compares overlaps by basename. Validate all assertions and permit an empty
    # overlap when ID01 deliberately maps differently named sources.
    names = left.keys() & right.keys()
    rows = snap["comparison"]
    need(isinstance(rows, list) and len(rows) == len(names)
         and {r["name"] for r in rows} == names, "Missing or duplicate feed comparisons.")
    for r in rows:
        name = r["name"]
        need(r["status"] == "BYTES_MATCH" and len(left[name]) == len(right[name]) == 1,
             "Unverified, conflicting or ambiguous feed comparison.")
        check(left[name][0], right[name][0])
    return {"byte_matches":len(verified), "mirrors":bindings}


def verify_p0(src, baseline, directory, data):
    spec = baseline["p0"]
    name, path = spec["filename"], spec["readback_path"]
    need(isinstance(name, str) and re.fullmatch(r"[\w.-]+\.json",name) and name not in {".",".."}, "Unsafe P0 filename.")
    directory = Path(directory).resolve()
    local = (directory / name).resolve(strict=True)
    need(local.parent == directory and local.is_file() and 0 < local.stat().st_size <= 2*1024*1024, "Invalid P0 manifest.")
    raw = local.read_bytes()
    need(len(raw) == spec["bytes"] and sha(raw) == spec["sha256"], "Local P0 file differs from ID01 baseline.")
    # v8 has no raw readback endpoint. Only an approved same-origin provider route can satisfy this gate.
    need(isinstance(path,str) and re.fullmatch(r"/api/v1/feed/local/(?:[A-Za-z0-9_-]+/)*[A-Za-z0-9_-]+",path),
         "Approved raw P0 import route unavailable.")
    doc, mirror = decode(raw), data["localMirror"]
    # Acceptance interface only. Sites v8 does NOT implement this producer evidence;
    # BLOCK until an actual accepted import binds its output to a raw readback.
    binding = mirror.get("rawManifest")
    need(isinstance(binding,dict) and binding.get("path") == path and binding.get("sha256") == spec["sha256"]
         and type(binding.get("bytes")) is int and binding["bytes"] == spec["bytes"],
         "Accepted import lacks bound raw-file readback evidence.")
    need(src.feed(path, auth=False)[0] in (401,403), "P0 raw endpoint lacks expected anonymous denial.")
    code, mime, got = src.feed(path)
    need(code == 200 and mime in {"application/json","application/octet-stream"} and got == raw,
         "Authenticated raw P0 bytes unavailable or different; a wrapper hash is insufficient.")
    need(doc["version"] == 1 and doc["root"] == "WORK" and "scope" not in doc and mirror["source"] == "LOCAL_WORK_MIRROR",
         "Wrong P0 manifest or partial import.")
    need(sha(encode({k:mirror[k] for k in ("source","items","github")})) == mirror["revision"],
         "P0 accepted mirror payload digest does not match.")
    projected = [{k:r[k] for k in ("path","modifiedMs","size")} for r in mirror["items"]]
    need(len(doc["items"]) == len(projected) and sorted(doc["items"],key=lambda i:i["path"]) == sorted(projected,key=lambda i:i["path"])
         and int(stamp(doc["observedAt"]).timestamp()*1000) == int(stamp(mirror["observedAt"]).timestamp()*1000),
         "Stored mirror metadata does not correspond to the original P0 file.")
    return {"sha256":sha(got), "bytes":len(raw), "items":len(projected), "path":path}


def evaluate_evidence(baseline, evidence_dir, now, *, io=None, deliveries=()):
    """Verify actual independent reads. Report safe reasons for unavailable evidence."""
    src = io if io is not None else Live()
    results, values = {}, {}
    def gate(key, func):
        try:
            values[key], summary = func()
            results[key] = dict(status="PASS", detail="Verified by readback.", **summary)
        except Exception as exc:
            # Some provider/network exceptions contain URL queries or bearer material.
            reason = str(exc) if isinstance(exc, Blocked) else type(exc).__name__
            results[key] = {"status":"BLOCKED", "detail":reason}

    def acl():
        status = src.feed(auth=False)[0]
        need(status in (401,403), f"Anonymous API returned HTTP {status}; expected 401/403.")
        return status, {"http_status":status}

    def drive():
        live = src.drive_inventory()
        need(encode(live) == encode(values["FEED"]["snapshot"]["drive"]) and live["root"] == WORK and live["items"],
             "Complete current WORK tree differs from snapshot.")
        return live, {"root":WORK, "items":len(live["items"]), "inventory_sha256":sha(encode(live))}

    def github():
        live = src.git_inventory()
        need(encode(live) == encode(values["FEED"]["snapshot"]["github"]) and live["repo"] == REPO and live["branch"] == "main"
             and live["commit"] == baseline["github_commit"] and live["items"], "GitHub main/tree differs from baseline or feed.")
        return live, {"commit":live["commit"], "items":len(live["items"]), "inventory_sha256":sha(encode(live))}

    def snapshot():
        data = values["FEED"]
        state = cloud_state(data, baseline, now)
        matches = compare_sources(src, data["snapshot"], values["DRIVE"], values["GITHUB"], baseline["mirrors"])
        return state, dict(state, **matches)

    def panel():
        state = values["SNAPSHOT"]
        view = src.panel()
        need(view["origin"] == PANEL and view["hashes"] == [state["revision"]] and view["status"] == "Quellen gelesen"
             and view["revision"] == state["revision"] and view["root"] == WORK and view["commit"] == baseline["github_commit"]
             and view["checkedAt"] == state["checked_at"] and view["attempt"] == state["attempt"],
             "Live panel DOM or panel source record differs from the cloud snapshot.")
        payload = view["payload"]
        # WebDriver may reorder object keys. Restore the original producer ordering
        # from the authenticated snapshot only after a strict structural comparison.
        expected = {k:values["FEED"]["snapshot"][k] for k in ("drive","github","comparison")}
        strict = lambda obj: json.dumps(obj, sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False)
        need(strict(payload) == strict(expected) and sha(encode(expected)) == state["revision"],
             "Panel dataset differs despite its displayed revision.")
        need(src.git_inventory() == values["GITHUB"] and src.drive_inventory() == values["DRIVE"],
             "Source inventory changed during audit.")
        need(cloud_state(feed_json(src), baseline, now) == state, "Cloud source changed during panel readback.")
        return view, {"panel_origin":PANEL, "revision":view["revision"], "checked_at":view["checkedAt"], "attempt":view["attempt"],
                      "drive_items":len(payload["drive"]["items"]), "github_items":len(payload["github"]["items"]),
                      "comparison_count":len(payload["comparison"]), "dataset_sha256":sha(encode(expected))}

    gate("ACL", acl)
    gate("FEED", lambda:(feed_json(src), {"api":FEED+FEED_PATH}))
    gate("P0", lambda:(None,verify_p0(src,baseline,evidence_dir,values["FEED"])))
    gate("REGISTRY", lambda:(None,verify_registry(src,baseline,deliveries)))
    gate("DRIVE", drive)
    gate("GITHUB", github)
    gate("SNAPSHOT", snapshot)
    gate("PANEL", panel)
    return results

