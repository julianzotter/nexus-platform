# Glossary (ubiquitous language)

| Term | Meaning |
|---|---|
| Task | A scoped unit of work with an owner, acceptance criteria, dependencies and a human gate (`schemas/task.schema.json`). |
| Agent | A role with a list of allowed skills and tools. |
| Skill | A folder with manifest, input/output schemas, tests and an owner. |
| Evidence | A measured, reproducible fact backing a claim (command, tool version, timestamp). Never pre-filled. |
| Gate | A human approval step (ID-01). No automatic merge. |
| Knowledge item | A registered unit of knowledge with a stable ID shared with the NEXUS-AI-AEC knowledge graph. |
| Norm | A standard clause (Eurocode, ÖNORM, DIN, ...) with edition, national annex and validity status. |
| Solver | A deterministic, unit-tested calculation. LLMs call solvers; they do not do the arithmetic. |
| Run | One execution of a task/workflow, recorded with inputs, outputs and scores. |
| Delta | Difference between a run and its baseline; drives the smallest fix. |
| Score | Measured accuracy, confidence and cost of a run. |
| INCOMPLETE | A source or metric that could not be measured; reported as such, never guessed. |
