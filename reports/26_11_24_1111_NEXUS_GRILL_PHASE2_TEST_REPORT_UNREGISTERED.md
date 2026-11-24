---
name: NEXUS_GRILL_PHASE2_TEST_REPORT
version: "0.1.0"
created_at: "2026-11-24T11:11:16+01:00"
agent_id: null
owner: ID06
ticket_id: WO-20261124-GRILL-IMPLEMENT
status: REVIEW_REQUIRED
development_status: TESTED
registration_status: REGISTRATION_PENDING
---
# Phase 2 – local isolated candidate
Run ID: 6a14d24a-47f9-4f1b-84d7-caadf9f681c9
Actual executor: ChatGPT container Python, not Claude; external role ACK not established.
Sources: guide 1iv-PYO68krnFTXihSU16NzKt5fHqZBiK; current AGENTS.md; mcp_bridge/ctx_router.py blob 4a29e029fa355e206703bf5d8f0e89c51d5; existing skills agent-team-plan and agent-team-orchestrator.
Finding: ctx_router uses cl100k_base or len(text)//4 approximation. Full request provider count cannot be proven by this estimate. Added isolated read-only arithmetic guard and skill, no runtime wiring.
Design: reversible prototype; D4/D7/D9 approval and independent review remain pending.
Test evidence: first 11 tests PASS; targeted negative tests for empty request, zero input count and duplicate JSON keys reproduced 3 failures in 14 tests; fix; 14/14 PASS, py_compile PASS. No native provider adapter/production E2E, no full repository CI, no measured LLM token counts, no independent review.

## SHA256
- `skills/nexus-grill-run/SKILL.md`: `ac5f059eed17fb780e9f8b76310556baa73743618e6c80cbb9b165693cbf1ca4`
- `tools/run_budget_guard.py`: `d60825ea0e41f6ac7f520e29640950286fa2eef09eb88a9a6a8ec226c46412bf`
- `tests/test_run_budget_guard.py`: `c46465bda129f75121aff9cf164b95876f9dd3245d69792b685e513f16aa8f80`

## Red test log
```text
test_bool_not_int (test_run_budget_guard.BudgetGuardTests.test_bool_not_int) ... ok
test_cli (test_run_budget_guard.BudgetGuardTests.test_cli) ... ok
test_duplicate_receipt_keys (test_run_budget_guard.BudgetGuardTests.test_duplicate_receipt_keys) ... FAIL
test_empty_request (test_run_budget_guard.BudgetGuardTests.test_empty_request) ... FAIL
test_estimate (test_run_budget_guard.BudgetGuardTests.test_estimate) ... ok
test_exact_boundary (test_run_budget_guard.BudgetGuardTests.test_exact_boundary) ... ok
test_hash_mismatch (test_run_budget_guard.BudgetGuardTests.test_hash_mismatch) ... ok
test_missing_limit (test_run_budget_guard.BudgetGuardTests.test_missing_limit) ... ok
test_missing_model (test_run_budget_guard.BudgetGuardTests.test_missing_model) ... ok
test_negative_count (test_run_budget_guard.BudgetGuardTests.test_negative_count) ... ok
test_no_output_reserve (test_run_budget_guard.BudgetGuardTests.test_no_output_reserve) ... ok
test_one_token_over (test_run_budget_guard.BudgetGuardTests.test_one_token_over) ... ok
test_reserve_exceeds_cap (test_run_budget_guard.BudgetGuardTests.test_reserve_exceeds_cap) ... ok
test_zero_input_count (test_run_budget_guard.BudgetGuardTests.test_zero_input_count) ... FAIL

======================================================================
FAIL: test_duplicate_receipt_keys (test_run_budget_guard.BudgetGuardTests.test_duplicate_receipt_keys)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/mnt/data/nexus_grill_runs/candidate/tests/test_run_budget_guard.py", line 78, in test_duplicate_receipt_keys
    self.assertEqual(result.returncode,2)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 2

======================================================================
FAIL: test_empty_request (test_run_budget_guard.BudgetGuardTests.test_empty_request)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/mnt/data/nexus_grill_runs/candidate/tests/test_run_budget_guard.py", line 65, in test_empty_request
    self.assertEqual(MODULE.assess(b'', receipt)['status'], 'BLOCKED')
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'PASS_BUDGET_ARITHMETIC' != 'BLOCKED'
- PASS_BUDGET_ARITHMETIC
+ BLOCKED


======================================================================
FAIL: test_zero_input_count (test_run_budget_guard.BudgetGuardTests.test_zero_input_count)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/mnt/data/nexus_grill_runs/candidate/tests/test_run_budget_guard.py", line 68, in test_zero_input_count
    self.assertEqual(self.check(input_tokens=0)['status'], 'BLOCKED')
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'PASS_BUDGET_ARITHMETIC' != 'BLOCKED'
- PASS_BUDGET_ARITHMETIC
+ BLOCKED


----------------------------------------------------------------------
Ran 14 tests in 2.449s

FAILED (failures=3)
```

## Green test log
```text
test_bool_not_int (test_run_budget_guard.BudgetGuardTests.test_bool_not_int) ... ok
test_cli (test_run_budget_guard.BudgetGuardTests.test_cli) ... ok
test_duplicate_receipt_keys (test_run_budget_guard.BudgetGuardTests.test_duplicate_receipt_keys) ... ok
test_empty_request (test_run_budget_guard.BudgetGuardTests.test_empty_request) ... ok
test_estimate (test_run_budget_guard.BudgetGuardTests.test_estimate) ... ok
test_exact_boundary (test_run_budget_guard.BudgetGuardTests.test_exact_boundary) ... ok
test_hash_mismatch (test_run_budget_guard.BudgetGuardTests.test_hash_mismatch) ... ok
test_missing_limit (test_run_budget_guard.BudgetGuardTests.test_missing_limit) ... ok
test_missing_model (test_run_budget_guard.BudgetGuardTests.test_missing_model) ... ok
test_negative_count (test_run_budget_guard.BudgetGuardTests.test_negative_count) ... ok
test_no_output_reserve (test_run_budget_guard.BudgetGuardTests.test_no_output_reserve) ... ok
test_one_token_over (test_run_budget_guard.BudgetGuardTests.test_one_token_over) ... ok
test_reserve_exceeds_cap (test_run_budget_guard.BudgetGuardTests.test_reserve_exceeds_cap) ... ok
test_zero_input_count (test_run_budget_guard.BudgetGuardTests.test_zero_input_count) ... ok

----------------------------------------------------------------------
Ran 14 tests in 2.460s

OK
```

NEXT_ACTION: draft PR, independent review on pinned commit, native provider adapter and CI; ID01 gate before merge/release.
