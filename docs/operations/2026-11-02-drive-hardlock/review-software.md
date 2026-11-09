---
name: "review-software"
version: "0.2.0"
status: "REVIEW_CANDIDATE"
timestamp: "2026-11-02T19:12:30.706211+01:00"
agent_id: null
executor: "OpenAI Codex"
executor_instance: "/root/software_review"
model_id: null
requested_external_model: "OPUS 5.5"
external_model_execution: "NOT_RUN"
hash_scope: "body_utf8_after_closing_frontmatter_lf"
hash: "d5cbe95f23f9275cf57dc74577c40aa6890829a2abf8f05d17fdc8040eb0ac0d"
review_bundle_sha256: "5b349b8c66a8fc86ca5da89fd2db7190fc48e06f863ce7be81e50878b9e6beed"
---
# Independent software architecture review — final delta
Verdict: PASS_SCOPED_REVIEW_CANDIDATE; production/E2E release remains BLOCKED.
Reviewer: separate OpenAI Codex instance `/root/software_review`; model_id unknown; OPUS 5.5 NOT_RUN.
Review basis: actual frozen code/test/docs bytes matching every entry in `evidence/code-hashes.json`; initial review preserved as `review-software-v0.1.md`.

## Independently executed verification
- `python -m unittest backend.test_drive_writer -v`: 13 PASS, 0 FAIL after final delta.
- `node --experimental-strip-types --test protocolPersistence.test.mjs`: 6 PASS, 0 FAIL after final delta; Node v24.22.1.
- Independent fake-credential delta probe: refresh callback forced timeout=10 even when caller passed timeout=999; PASS. No live credential/provider calls.
- Every one of 15 frozen manifest entries independently rehashed and matched; PASS.
- App lint/build, real browser UI, real browser cross-tab race, Windows ACL validation and live Drive E2E: NOT_RUN by this reviewer.

## Plan gates and final corrections
- Persisted reservation/exact bytes precede upload; exact Drive object ID survives uncertain upload and restart. Provider calls occur outside the SQLite transaction.
- Metadata (including exact file ID, name, sole parent, MIME, untrashed state, size) and complete raw-byte equality gate the 202 receipt.
- Loopback binding, exact browser Host/Origin/custom-header policy, fixed proxy destination and independent host bearer secret are present.
- No Blob/download fallback in Timeline Markdown route. UI explicitly retains registration-pending status.
- Runtime actor ID remains null. Artifact IDs derive from actual preallocated Drive IDs. Canonical number reservation is operator asserted; it is not falsely described as remotely authenticated.
- SW-01 prior P1: CODE_CORRECTED. Web Locks now wrap reservation and save. Missing Web Locks fails closed. Locking is same-origin/browser-profile scope; true browser race test remains NOT_RUN. `localhost` and `127.0.0.1` are separate origin profiles and do not share the mapping/lock.
- SW-02 prior P1: CODE_CORRECTED + INDEPENDENT_DELTA_PROBE_PASS. Credential transport calls now receive timeout=10. This bounds each transport call, not total credential retries or the entire writer operation; proxy timeout does not cancel Python.
- SW-03 prior contract check: PARTIALLY_ADDRESSED. Added artifact_id, input_hash, run_id, ticket_id and explicit operator-reservation verification status. Executor-instance and reply fields are not invented; governance reviewer retains authority to assess contract applicability. No universal frontmatter compliance is certified here.
- tzdata added for Windows timezone data; restrictive umask added for new POSIX runtime files. POSIX umask does not prove protected Windows ACLs; intended-host verification remains required.

## Remaining gates and limits
1. Real ADC/Drive write/readback/revocation, real canonical ledger reservation and actual protected host journal: NOT_RUN/UNVERIFIED. Registration deliberately remains BLOCKED_NO_ATOMIC_REGISTRY_WRITER. No parallel canonical registry is created.
2. External OPUS review, authenticated runtime-role mapping, ID01 decision, app lint/build, CI execution, merge and deployment remain separate gates. This review does not certify any of them.
3. Single-host/single-writer custom HTTP service only; no multi-host lease/fencing claim. Loss of browser mappings, use of different origins/profiles or reconstruction of an uncertain changed snapshot can introduce a new identity. Transcript content restoration across browser restart is outside this slice. Remote files are mutable after verification; receipt proves observed contents/metadata at verification time, not Google's physical media or future immutability.

## Decision
No P0 blocker found for this bounded frozen implementation/test candidate. Initial technical corrections are present and targeted tests pass. PASS is an independent software review verdict on this hash set, not live deployment acceptance, external-model peer review, registration completion or engineering approval. Any later code change invalidates affected review evidence until re-reviewed.

## SHA-256 binding
Bundle hash = SHA256(canonical JSON mapping, sorted keys, compact separators): `5b349b8c66a8fc86ca5da89fd2db7190fc48e06f863ce7be81e50878b9e6beed`
Previous review SHA-256: `ea1eccd548a110cb7442c45845876c66d87b241e713e65f3ef0bf0c49b444ac3`

- `.github/workflows/drive-hardlock.yml`: `aeab427717a4d08192cc9b618e77fe38572e65391be5f70c5b5f8bf6e0bfcce7`
- `.gitignore`: `f45e17afb1160d44219379ecb3cd95dd71a513d21f08955397fec72220ee3e2b`
- `backend/__init__.py`: `380f10bdd89208e61f0c82af5668b498e4d358a488d8b656a4bef135b0fe8483`
- `backend/drive_writer.py`: `c102466c4b0eda05e072a5cb5e457195a3a85ec658852bd593b9238a46b0b40a`
- `backend/google_drive.py`: `b9c2f657290f95a10c2f86b161e60c96ad3cf44be4e8987a2a39de65924407f1`
- `backend/nexus_server.py`: `a50f52337ea01fdab9483dc3c75e50e3175ccd40a13596f4fc2269f650e9fccf`
- `backend/requirements.txt`: `d098339d35103660d6a7833a469984f2ef6a335a4fa0d9305a0d68199e0bcf1f`
- `backend/test_drive_writer.py`: `04e9d653ba798bf60f5cb264b8a9d15ed690ef5103b33e0b8ee8d3ecbe5a62ba`
- `docs/DRIVE-HARDLOCK.md`: `86bcbce21040d5ba9f4305e8d42d4908e97980f71e52cbfe1925a48f6b0d20cd`
- `package.json`: `b046d74d51662b70883e77c45c79b1d575c9816ca0c489eda9f3cb165e9f06e5`
- `protocolPersistence.test.mjs`: `ce187ba5dc5d66709507c452382d92a309504e0c47aca8386efd951e70496c39`
- `protocolProxy.ts`: `e60e7d45604c0872baff81a512f8166e985fbeb856bf01db1829e624bb4ed918`
- `server.ts`: `794617fd3c4d0bdc45341d4a1b99da4549fef0ca56ee251c1dac69f67c8b932b`
- `src/components/TranscriptTimeline.tsx`: `1f8da1c8af27604e7775f2811e382cc114655d69e68c66c3ab490da49fb172d8`
- `src/utils/protocolPersistence.ts`: `8cc3a1c11fd2a29a0d342d674d373e788207942feae0d51186acb38c6af05151`
