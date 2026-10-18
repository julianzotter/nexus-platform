# NEXUS CPLM — bounded local execution kernel

This package is an executable local gate prototype. It is not an installed
Drive/Gemini/GitHub writer and does not enforce policy on tools that bypass it.
The existing repository orchestrator remains the model-routing component;
this kernel governs local result, validation, handoff, review and release states.

## Run the actual regression suite

```bash
python -m pip install PyYAML==6.0.3
PYTHONPATH=cplm-implementation python -m unittest discover -s cplm-implementation/tests -v
```

Python 3.12 and a local Linux filesystem are the tested target. Atomic hard-link
publication and directory fsync are deliberate; Windows, network filesystems and
multi-host deployment are not tested targets. Do not deploy this package as the
claimed Windows PowerShell solution without an appropriate adapter and tests.

## Contract

An authenticated adapter must supply the principal, never accept an arbitrary
client `actor` as authentication. A policy defines grants, source paths and hashes,
the human principal and allowlisted notification channel/recipient pairs. No
credentials or real user identities are included in test fixtures.

1. `submit` requires a current policy-read receipt and deduplicates the logical
   `task_key`. SQLite serializes writers to this single local database.
2. `result` requires YAML, matching task/source references and `status: RESULT`;
   it publishes complete bytes without overwriting conflicting evidence.
3. `validate_result` performs concrete local checks and seals their receipt plus
   artifact/source/policy/loaded-code bindings. It does not assert that a full
   test suite, a semantic review or an external integration ran.
4. Handoff advances through PUBLISHED, DELIVERED, ACKNOWLEDGED and VERIFIED.
   Evidence strings require verification by the external authenticated adapter.
5. Three different reviewer principals cover software, governance and systems
   on the same freshly checked manifest. A separate human principal may release
   only after verified handoff and three current PASS reviews.
6. Notifications have a server-derived unique key. An uncertain outcome blocks
   blind retry; an adapter must reconcile provider evidence. No email is sent
   by this library itself.

Frontmatter currently accepts exactly `task_id`, `status`, and `source_refs`;
duplicate keys and ambiguous types are rejected. Internal artifacts use the
run ID; published WORK reports use the separate timestamp/title convention.
Notification policy accepts canonical email/sms/push/webhook channels only,
not vendor aliases. Defining a channel is not an installed transport adapter.

Optional `release_inputs` must define all five roles: requirements, schema,
tests, test_receipt, dependencies. Each role is a relative file path and SHA256;
all are checked and bound into the manifest. This binds bytes, not receipt
authenticity or proof that a declared command ran. An authenticated evaluator
must produce actual test evidence for a production release.

Reviews are immutable within one run. A revised review requires a new logical
run referencing its predecessor; this API does not overwrite a prior FAIL.

An artifact conflict becomes RECOVERY_REQUIRED. Explicit recovery isolates and
preserves conflicting bytes before a retry. Orphaned staging files are retained
as crash evidence; a production retention/cleanup policy is still required.

## Remaining deployment boundaries

No external identity, signed human approval, remote ACK, Drive compare-and-swap,
exclusive service credentials, global index, provider reconciliation, watchdog,
runtime quota discovery or GitHub/OneDrive sync is implemented here. Source and
policy files require a controlled host: the SQLite lock does not lock arbitrary
external filesystem writers. Policy inheritance currently resolves one bounded
parent/child pair; recursive resolution is not claimed.

Drive WORK remains the document source of truth. This branch holds explicit
review snapshots and code. Production is blocked until these boundaries are
implemented and tested, reviews are bound to the final release package, and the
human owner approves. Passing tests are scoped evidence, never a 100% reliability
or production certification claim.
