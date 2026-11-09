# Systems delta re-review — final bounded verdict
Reviewer: OpenAI Codex, separate instance /root/systems_review. Not OPUS.
Verdict: PASS_WITH_DEPLOYMENT_GATES for the frozen local review candidate. Not production approval; live registration workflow remains incomplete.

## Delta closure
- SYS-C01 CLOSED by inspection: `tzdata>=2024.1` is now required; Windows dependency and host QA are documented. Actual Windows execution remains NOT_RUN.
- SYS-C02 CLOSED for the stated bounded transport scope: ADC refresh now receives timeout=10; provider I/O also has timeout=10. These are per-operation network timeouts, not a hard wall-clock deadline for every possible credential implementation or whole save. Proxy/browser timeout still means uncertain outcome and same-ID reconciliation.
- Cross-tab browser saves now use Web Locks. Missing Web Locks fails closed. Exact same snapshot retains persisted request ID. This is browser-origin/local-storage scoped, not account-wide exactly-once.
- Frontmatter now contains ticket/run/runtime traceability without inventing a model or actor ID. Unix runtime umask is private; Windows ACL protection remains an explicit host check.
- SYS-C03 RETAINED_LIMITATION, documented in DRIVE-HARDLOCK.md: a continuously changing transcript produces a new snapshot/key; the UI does not automatically freeze an uncertain snapshot for retry. User must retry the exact snapshot. No assertion that this usability limitation is implemented away.
- SYS-C04/C05 EXPLICIT_GATES: remote content readback is distinct from registration, physical-media durability, access-control exclusivity, independent OPUS review and human release. Single host, single writer, durable local journal only.

## Independent validation on final bytes
- SHA-256: all 15 entries of `evidence/code-hashes.json` match current studio files. Manifest SHA-256: fe126e2309a51653095379fda696409ce7965f384f73f518e59451e5b1d5d65a.
- `python -m unittest backend.test_drive_writer -v`: PASS 13/13, independently rerun after delta.
- `node --test protocolPersistence.test.mjs`: PASS 6/6, independently rerun after delta.
- Full app lint/build, real browser visual QA, real Google ADC/Drive multipart E2E, Windows execution, authenticated canonical-number reservation and registry integration: NOT_RUN / deployment gates.

## Deployment assessment
Minimal two-process loopback architecture is coherent for the explicit Python vertical slice; no graph framework, distributed queue or multi-agent runtime is needed to enforce this I/O gate. Do not merge/deploy as complete before the documented host, registry, external-review and ID01 gates. The number pool is explicitly operator-asserted, not independently authenticated by this service. Available fake-provider tests do not establish real Google API compatibility.

## Frozen manifest
```json
{
  ".github/workflows/drive-hardlock.yml": "aeab427717a4d08192cc9b618e77fe38572e65391be5f70c5b5f8bf6e0bfcce7",
  ".gitignore": "f45e17afb1160d44219379ecb3cd95dd71a513d21f08955397fec72220ee3e2b",
  "backend/__init__.py": "380f10bdd89208e61f0c82af5668b498e4d358a488d8b656a4bef135b0fe8483",
  "backend/drive_writer.py": "c102466c4b0eda05e072a5cb5e457195a3a85ec658852bd593b9238a46b0b40a",
  "backend/google_drive.py": "b9c2f657290f95a10c2f86b161e60c96ad3cf44be4e8987a2a39de65924407f1",
  "backend/nexus_server.py": "a50f52337ea01fdab9483dc3c75e50e3175ccd40a13596f4fc2269f650e9fccf",
  "backend/requirements.txt": "d098339d35103660d6a7833a469984f2ef6a335a4fa0d9305a0d68199e0bcf1f",
  "backend/test_drive_writer.py": "04e9d653ba798bf60f5cb264b8a9d15ed690ef5103b33e0b8ee8d3ecbe5a62ba",
  "docs/DRIVE-HARDLOCK.md": "86bcbce21040d5ba9f4305e8d42d4908e97980f71e52cbfe1925a48f6b0d20cd",
  "package.json": "b046d74d51662b70883e77c45c79b1d575c9816ca0c489eda9f3cb165e9f06e5",
  "protocolPersistence.test.mjs": "ce187ba5dc5d66709507c452382d92a309504e0c47aca8386efd951e70496c39",
  "protocolProxy.ts": "e60e7d45604c0872baff81a512f8166e985fbeb856bf01db1829e624bb4ed918",
  "server.ts": "794617fd3c4d0bdc45341d4a1b99da4549fef0ca56ee251c1dac69f67c8b932b",
  "src/components/TranscriptTimeline.tsx": "1f8da1c8af27604e7775f2811e382cc114655d69e68c66c3ab490da49fb172d8",
  "src/utils/protocolPersistence.ts": "8cc3a1c11fd2a29a0d342d674d373e788207942feae0d51186acb38c6af05151"
}
```

## Historical first implementation review
The following prior CHANGES_REQUIRED verdict is retained for traceability; C01/C02 are superseded only by the scoped delta verdict above.

# Independent systems implementation review
Reviewer: separate OpenAI Codex instance /root/systems_review. Not OPUS; no external model execution.
Scope: exact files in SHA-256 manifest below. No production or engineering approval.
Verdict: CHANGES_REQUIRED for deployment; bounded local implementation otherwise coherent.

## Findings
- SYS-C01 / P1 / deployment blocker: `drive_writer.py` calls `ZoneInfo("Europe/Vienna")` but `backend/requirements.txt` only installs google-auth. Windows commonly has no system IANA timezone database. Add `tzdata` to dependencies and validate timezone availability at startup. This is particularly relevant to the explicitly described Windows 11 deployment. Linux unit success does not prove Windows readiness.
- SYS-C02 / P1 / availability: `GoogleDrive.call()` bounds `urlopen` to 10 seconds but credential refresh calls `self.credentials.refresh(self.auth_request)` without an explicitly bounded transport timeout. Bound authentication refresh too; clarify per-operation vs whole-request deadlines. Proxy/browser timeouts can currently return uncertainty while the single Python worker remains busy.
- SYS-C03 / P2 / retry usability: browser idempotency persists fingerprint + request ID, but `TranscriptTimeline` invokes `persistProtocol(items)` against current live items each time. If the first response is lost and live events are appended, clicking again creates a new snapshot/key, not a retry of the uncertain snapshot. Freeze an uncertain snapshot in memory for explicit retry or clearly document that saving a changed transcript creates a distinct artifact. This is not server-side duplicate creation for the same request ID.
- SYS-C04 / documented system boundary: `DRIVE_VERIFIED_REGISTRATION_PENDING` correctly remains HTTP 202 and amber UI. Registration is deliberately absent; therefore the complete AGB-governed save workflow remains BLOCKED. Local bytes/metadata readback is provider persistence evidence at that moment, not physical disk verification, exclusive ownership, or future immutability.
- SYS-C05 / deployment constraint: one HTTPServer and one journal on a local persistent disk are the supported topology. Do not run independent replicas sharing a reservation pool. `threading.Lock` is process-local. SQLite protects intent allocation but does not establish exclusive external cloud-writer governance.

## Verified improvements
- Express is bound to 127.0.0.1; save proxy checks loopback peer, exact Host/Origin, JSON MIME and a custom header. Python endpoint is separately loopback-bound and bearer protected.
- Request fields are bounded, target/name cannot be supplied by caller, transcript text is serialized as quoted data, role/model unknowns are null.
- Exact serialized bytes/name/target/preallocated Drive ID are committed before upload; same request ID + changed payload conflicts. Restart retries reconcile the same provider ID.
- Metadata and exact bytes must match before a receipt. No Blob fallback exists in the reviewed timeline/persistence path.
- Externally reserved canonical numbers are required rather than generated from filenames.

## Validation actually run
`python -m unittest backend.test_drive_writer -v` from studio: PASS, 13 tests, 2026-11-02 session run.
Fake-provider scope only. Google ADC, Drive multipart API, Windows startup, browser rendering and deployed proxy-to-Python-to-Drive E2E: NOT_RUN in this review.

## Minimal deployment path
Correct C01/C02; run local regression; start Python with durable journal + host secret + actual Drive credentials + fixed folder + canonical reservation receipt; start Express on loopback with the same host secret; verify denied requests and one real upload/readback; obtain canonical registry receipt before workflow completion. No graph framework or distributed queue is necessary for this vertical slice.

## SHA-256 reviewed bytes
- `studio/backend/drive_writer.py`: `9e76490d1a57c6da6eba250660e3672adb3ed34adb8e9c658e69a520ac59db30`
- `studio/backend/google_drive.py`: `a93696e25ccaf76f34f61928b80a7a38b3fe4294996140d3573c92a24339c41f`
- `studio/backend/nexus_server.py`: `31bb93af520abb6c94e5842bb95bafba65bc930e9935b651df44a61c5d874f7f`
- `studio/backend/requirements.txt`: `9495f5a2b88718b34a1e3971324601a98e0bf0473f887198b3c215ceabb1b086`
- `studio/backend/test_drive_writer.py`: `04e9d653ba798bf60f5cb264b8a9d15ed690ef5103b33e0b8ee8d3ecbe5a62ba`
- `studio/protocolProxy.ts`: `e60e7d45604c0872baff81a512f8166e985fbeb856bf01db1829e624bb4ed918`
- `studio/src/utils/protocolPersistence.ts`: `cc7926e8d66559b46eef85abe018df56047f51cbc4fd95184d2b676b97ad2c3b`
- `studio/src/components/TranscriptTimeline.tsx`: `1f8da1c8af27604e7775f2811e382cc114655d69e68c66c3ab490da49fb172d8`
- `studio/server.ts`: `794617fd3c4d0bdc45341d4a1b99da4549fef0ca56ee251c1dac69f67c8b932b`
