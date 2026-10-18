# NEXUS dashboard v3 / OSR-9 prototype modules

Prototype only; not certified. Source HTML was not in the repository, so the corrected logic lives in standalone modules:

- `ec5_solver.js` - EC5 6.3.2 buckling; material dropdown value selects constants; gate returns `PASS`/`FAIL`.
- `osr9_mmr.js` - MMR selection (`lambda*relevance - (1-lambda)*max similarity`).

Tests: `python -m unittest tests.test_dashboard_prototype` (needs `node`).
See `docs/audit/_AGBS.md`.
