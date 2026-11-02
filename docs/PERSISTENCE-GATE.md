# Bounded persistence gate — reviewed development slice

Ticket: WO-20261102-NEXUS-PERSISTENCE-GATE. Drive remains document SSOT.
The current AGB v005 additionally requires continuous safe development and honest
partial reporting. A blocked save/registration does not halt independent tests,
analysis or authorized WORK Markdown communication. No delete/email/deploy path
is introduced here.

## Actual integration
`tools/deliver_work.py` retains its existing artifact delivery path. Its new
`--register` option invokes `tools/persistence_gate.py` for both the payload
and its immutable delivery receipt. Registration uses the existing Drive file
`15m8T5cWbogIup9snzFwiB1g9HqNCoGow`; no competing registry is created.

Without `--register`, delivery still returns `DELIVERY_VERIFIED`, now explicitly
with `registration_status: NOT_CHECKED`. This is not a full-persistence claim.
With it, a matching raw-byte/version/metadata readback and registry event are
required for `PERSISTED_VERIFIED`. Registry errors preserve `FILE_VERIFIED` and
`REGISTRATION_PENDING`; review/human acceptance remain pending.

The default registry mode is `read-only`. Missing registration then produces
an explicit partial result; it does not mutate the register. Mutating mode
`--registry-write-mode exclusive-writer` requires real external exclusivity.
The flag is an operator contract, not proof or an implemented lock. The bounded
compare/replace/readback algorithm is not atomic CAS and must not be deployed
as a multi-writer service. No workflow caller is silently migrated by this change.

## Recovery and evidence
- Persist preallocated Drive IDs before upload; reconcile ambiguous responses.
- Verify file ID, parent, name, MIME, byte count, version, timestamp and exact bytes.
- Bind event to operation, file, hash, provider version, ticket and provenance.
- Validate an existing matching registration timestamp, preserving historical bytes.
- Freeze delivery-only receipt bytes before adding mutable registry status.
- Preserve permission failures and reconcile uncertain registry writes by readback.

The receipt proves the observed point in time, not Google's physical media,
future immutability, a trusted arbitrary client, or an external reviewer ACK.
Free model prose outside this controlled output path can still contain errors.

## Verification
```sh
python3 -m unittest discover -s tests -p 'test_deliver_work.py' -v
python3 -m unittest discover -s tests -p 'test_persistence_gate.py' -v
python3 tools/deliver_work.py --help
```
18 existing and 17 new tests passed; two separate Codex reviewer instances each
reran them and reviewed the final code/test hashes. The review found and fixed
an idempotency defect that the first tests missed. Fake-provider tests are not
live Drive E2E. No production release is implied.

## Convergence
The existing Studio PR1 at `julianzotter/GEMINI-LIVE-DESKTOP-STUDIO-` supplies
the UI/Express/Python export path. It honestly returns registration pending.
Another candidate `tools/nexus_export_lock.py` exists on
`id06/nexus-wayfinder-export-lock`. This slice strengthens the shared monitor
delivery path; it does not start a third gateway or declare either exporter
canonically deployed. Converge request/receipt/registry contracts before release.
