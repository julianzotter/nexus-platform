# nexus-platform
NEXUS Platform Hub: Unified registry, coordinated execution, evidence-based learning. Versioned code, contracts, tests and review snapshots for engineering knowledge, deterministic solvers and multiagent workflows. Google Drive is the canonical source for operational documents and WORK records.

## Dokumentation
- [NEXUS-AI Kurz-Manual](docs/NEXUS-AI-Kurz-Manual.md) – die zwei Perplexity-Aufgaben (Recherche-Anbindung, Multi-LLM-System), PDF-exportierbar.

## Authority and storage

| Location | What to look up there |
|---|---|
| [Drive SSOT](https://drive.google.com/drive/folders/1j3FLJkWpQv6xGA_KO0D9sMyA11f0vxBV) and [WORK](https://drive.google.com/drive/folders/1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP) | Current governance, work orders, operational reports, and their [ticket references](https://docs.google.com/spreadsheets/d/1o1ZCZUgsCGTDOwdbJ7EbUCKOKJng1LcJLFnrRiPjYTE/edit) |
| [`governance/current/`](governance/current) and [`WORK/`](WORK) | GitHub review mirrors. Verify current document authority against Drive. |
| [`registry/`](registry), [`reports/`](reports), [`runs/`](runs), and [`backups/`](backups) | Repository registry data, report snapshots, run evidence, and preserved copies. Use the work order, commit/run ID, or artifact hash to identify a specific version. |
| [GitHub Actions](https://github.com/julianzotter/nexus-platform/actions) | Commit-bound CI results and workflow run artifacts |

## Reproduce CI locally

Use Python 3.12, Git, and a clone with complete history. CI checks the ancestry of
the dashboard's embedded data revision, so a shallow checkout or source ZIP is
insufficient for those tests.

```console
git rev-parse --is-shallow-repository
git --version
python -m venv .venv
```

If Git reports a shallow checkout, run `git fetch --unshallow origin`. Activate
the virtual environment, check out the commit under investigation, then run:

```console
python -m pip install pytest jsonschema
python -m pytest -q tests/test_data_dashboard.py tests/test_mcp_bridge.py
python -m pytest -q tests
python tools/validate_registry.py
```

If a Git subprocess fails, capture the failing Git command, its exit status and
stderr alongside the Python version and the commit SHA. The bridge tests create
temporary Git repositories and require a Git executable and a writable temp
directory.

See [Drive OAuth recovery](docs/NEXUS-OAUTH-RECOVERY.md) for independent checks of
delivery, polling and monitor coverage.
