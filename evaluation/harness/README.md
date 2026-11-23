# EVAL HARNESS — LLM-EVAL-OBSERVATION-SELFREFINE (WO0 + WO3)
Source: Drive LLM-LOCAL-SSOT/WORK — 26_11_23_0858_WO0_OUT, 26_11_23_0905_WO3_OUT · SSOT v1.0 Drive 10iwFkM2RV7wOL97uQ4la3TqFe4eE8UZC (sha 62ab70ed…)
Bounded loop OBSERVE→EVALUATE→REFINE(≤3)→STOP. Gates G1–G4 deterministic; G5 human. Solver = stub (mechanics only).
Run: `python -m pytest -q tests` · `python src/evaluate.py evals/cases.jsonl reports/runs.jsonl <run_id>`
Status: PASS 4/4 · freeze PENDING Human Gate (see schemas/status_vocabulary.md Q1–Q3)
