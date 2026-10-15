# NEXUS DELTA Development Cycle v0.1

Contract + runnable standard-library vertical slice. Central code location: nexus-platform/development_cycle. This extends the development process; it does not replace PR #13 or modify the canonical Drive Manifest/Baseline.

```bash
python -m unittest development_cycle.test_cycle -v
python -m development_cycle.cycle --out YOUR_LOCAL_RUN_DIRECTORY
```

Choose a new, non-synced local output directory for each demonstration. Output is runs.sqlite plus result.json. The demonstration contains supplied candidate answers to 6*7; Python computes their reference checks. It tests the history/evaluation mechanism, not an LLM's intelligence or autonomous improvement. No dependencies or credentials required.

## Shared understanding

Ubiquitous Language precedes GRILL-ME and Shared Understanding. Architecture/algorithms precede skills/agents. Simple requests take the short route. Development allows direct scripts and experiments; no skills-only rule. No emails and no deletion of existing user/project files. Traceable assumptions permit partial delivery while important verification gaps remain visible.

The SQLite application only inserts rows. It stores one initial checkpoint and subsequent sparse top-level patches; N-1/N-2 comparisons are retained without repeated complete outputs. Replay is O(number of runs); checkpoint compaction and large-history acceleration are future measured improvements. No claim of optimized large-scale storage or tamperproof audit. Hashes detect accidental changes, not an adversary capable of rewriting all hashes.

Checks are supplied evaluator observations. The recorder does not independently establish their truth, interpret all Baseline instructions or automatically calculate domain accuracy. Acceptance rate is distinct from accuracy; confidence remains null without a method. Costs/latency/reusability require a future measured evaluator. No hidden score or arbitrary convergence percent.

The cycle accepts a bounded list of trial outputs. It is a recording/refinement kernel, not a generative multi-LLM runtime. Three unchanged failed outputs produce partial delivery. Budget exhaustion also preserves the last result. Call append_run with explicit assumptions for normal integration. Database writer transactions serialize run numbering.

Review bundle hashes freeze identical inputs for Claude and Gemini; review status remains NOT_RUN until real responses arrive. No external provider calls are made by these files. Review requests are ready in REVIEW_REQUESTS.md.

## Source and scope

Basis: ID01's 2026-10-15 development discussion and go-ahead in this session; canonical source references from the preceding reconciliation. CONTRACT.md is a review candidate, not an assertion of production adoption. Actual executor: OpenAI Codex; exact model identifier unavailable to the implementation.

All development artifacts are versioned here so both accounts can reference the same commit and manifest. Existing canonical Drive IDs remain the shared knowledge entry points. No account memory is copied. No user secrets or project data are in the demonstration.
