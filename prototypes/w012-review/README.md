# W012 review tools — 2026-11-09

Review snapshot for evidence retrieval and 2D drawing validation. Not an RFEM model, EC5 solver or engineering release.

Canonical report: https://drive.google.com/file/d/1Ocn8wcWfKQmsjjz_Hz5CYAL3WSKukN7p/view

## Reproduce
Use Python 3 with SQLite FTS5 and Node for HTML search parity. Install CAD QA dependencies from `requirements-cad-qa.txt`. The code has no cloud credentials and performs no cloud writes.

Knowledge build: `python build_knowledge.py --baseline /path/to/W012_Hoftrakt.sqlite --extras /path/to/extras --output /new/output/directory`.

The private baseline is in the existing Drive W012 workpackage v0.2: https://drive.google.com/file/d/1UxPsgMMeumw1QaF6zRIEFSQeXCVar1z3/view . Extract its W012_Work directory next to this tools directory for default paths and knowledge tests. Do not commit project inputs, emails, photos or norms. Tests require authorized local access to this fixture; this snapshot does not claim an unattended CI run.

Run `python -m unittest discover -s . -p 'test_*.py' -v`. The drawing tests are synthetic and do not use project dimensions. The included unfilled model contract deliberately fails drawing validation. Complete explicit drawing geometry and verified source references before using `python w012_dxf.py INPUT.json OUTPUT.dxf`.

Knowledge projection retains baseline tables, adds source-backed searchable documents and produces SQLite, JSON and self-contained HTML with one snapshot ID. Extra JSON records preserve evidence status, never engineering approval. Local measurements are not cloud latency guarantees.

Drawing output is a 2D REVIEW-only DXF with checked units, nodes, members, column rectangles, axes and dimensions. No CLT surface generation, load generation, solver invocation or structural checks. Source declarations still require independent primary-source review. Paired DXF/receipt output is rollback-protected for normal errors, not a crash-atomic transaction.

Validated locally: 8 knowledge tests and 13 CAD tests (52 subcases). Human engineering release and recipient ACK remain outstanding. Drive is SSOT; this branch is a code review snapshot only.
