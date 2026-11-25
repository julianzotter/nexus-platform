# P2 acceptance for NEXUS WORK and the AEC panel

Run from a reviewed checkout with Windows PowerShell 5.1 or PowerShell 7, Python 3.12 (the repository CI runtime), and an authenticated GitHub CLI with read access to repository contents and Actions. Running the check does not start a workflow, refresh the feed, write to Drive, or approve a release. The existing delivery workflow's recorded OAuth preflight is evidence of its own prior refresh.

## Run

From the repository root, the following command creates a timestamped local report even when no baseline is available. The optional P1 inventory shows the most recent run of each of the three workflows on main, including queued or unsuccessful runs.

```powershell
.\tools\windows\verify_nexus_sync_p2.ps1 -RunP1PreflightCheck
```

For an evidence-backed run, use the ID01-approved baseline JSON, its SHA-256 received over an independent authenticated channel, and the directory containing the original Windows manifest. The variables below refer to those inputs. Calculating the expected digest from the candidate file in the same command defeats the approval check.

```powershell
.\tools\windows\verify_nexus_sync_p2.ps1 -BaselinePath $approvedFile -BaselineSha256 $approvedHash -EvidenceDirectory $manifestDirectory
```

The process prints its report directory. Inspect `status.json`, `status.md`, and `SHA256SUMS` there. Exit 0 is a point-in-time technical result. Exit 2 means at least one check failed or lacks evidence. Local report files are the only writes. The operator retains responsibility for the authenticity of the independently supplied baseline digest. This program does not authenticate a human reviewer.

## Evidence contract

| Approved JSON input | Contents |
|---|---|
| `repository`, `branch`, `github_commit` | `julianzotter/nexus-platform`, `main`, and the full approved commit SHA |
| `max_age_seconds`, `actions` | Positive evidence-age limit and each of `nexus-monitor.yml`, `nexus-drive-poll.yml`, `nexus-delivery.yml` mapped to integer `run_id` and `run_attempt` |
| `monitor_artifact`, `delivery_artifact` | Each includes the artifact `id` and the full GitHub `digest` with its `sha256:` prefix |
| `registry`, `ledger` | Independent approved Drive `version` and raw `sha256` for each canonical file. The 13 frozen file identities come from the repair plan at the approved Git commit. |
| `snapshot_sha256` | Digest of the exact ordered JSON payload containing `drive`, `github`, and `comparison`, as stored by the cloud feed |
| `mirrors` | Approved list of cross-source pairs. Each contains `drive_id`, `drive_version`, `git_path`, and the raw `sha256` of the shared content. |
| `p0` | Local `filename` (basename), `bytes`, `sha256`, and the approved same-origin raw `readback_path`. The authenticated feed must bind the stored object to this import through `localMirror.rawManifest.{path,sha256,bytes}`. The deployed v8 feed currently has no such original-byte readback. |

The source adapter uses the repository Drive reader and its existing OAuth configuration. The feed receives its service key (`NEXUS_FEED_MACHINE_KEY`) only on the fixed private Sites origin. Supply credentials through the existing runtime environment. For the panel check, open the source feed section in a signed-in panel tab under an existing local WebDriver session and provide its loopback port and session ID via `NEXUS_P2_WEBDRIVER_PORT` and `NEXUS_P2_WEBDRIVER_SESSION`. The observer reads this tab; it never clicks refresh or transfers feed credentials to the panel. An unavailable observer blocks the panel gate.

The v8 GET contract has `attempt.state`, separate `attempt.drive` and `attempt.github` statuses, and `snapshot.checkedAt`, `snapshot.drive`, `snapshot.github`, `snapshot.comparison`, and `snapshot.revision`. A verified recent cloud attempt must cover the snapshot. Local mirrors have separate scope. Panel v14 displays the cloud revision in its own source section. A raw manifest digest, a registry file digest, a Git blob ID, an archive digest and the snapshot revision identify different byte sequences. The verifier checks the relationships explicitly.

## Existing repair workflow (outside P2)

Only the operator with the required approval and writer coordination runs the existing repair. In the canonical checkout on main:

```powershell
$branch = git branch --show-current
if ($LASTEXITCODE -ne 0 -or $branch -ne 'main') { throw 'Expected main.' }
$changes = @(git status --porcelain)
if ($LASTEXITCODE -ne 0 -or $changes.Count -gt 0) { throw 'Clean working tree required.' }
git pull --ff-only origin main
if ($LASTEXITCODE -ne 0) { throw 'Fast-forward pull failed.' }
powershell -NoProfile -File .\tools\windows\repair_nexus_sync.ps1
if ($LASTEXITCODE -ne 0) { throw 'Repair or dispatch failed.' }
```

The repair already dispatches delivery. Use the exact run ID supplied by the dispatch or independently correlated by ID01. If the CLI returns no run ID, the newest run alone is insufficient evidence of this dispatch.

```powershell
gh run watch $deliveryRunId --repo julianzotter/nexus-platform --exit-status
if ($LASTEXITCODE -ne 0) { throw 'Delivery failed or could not be read.' }
gh run view $deliveryRunId --repo julianzotter/nexus-platform --json databaseId,attempt,headBranch,headSha,status,conclusion,url
if ($LASTEXITCODE -ne 0) { throw 'Final delivery readback failed.' }
```

P2 checks the run-bound delivery ZIP digest before parsing the contained status and two receipts, then checks the actual Drive targets. A digest calculated over an extracted JSON member does not establish the integrity of the original ZIP.

## Tests and operator boundaries

Run `python -m pytest -q tests -k nexus_p2` and `.\tests\windows\test_verify_nexus_sync_p2.ps1`. Positive cases use in-process fixtures. The production entrypoint has no switches for mock responses, arbitrary credential destinations or manual schema confirmation. Feed v8 currently lacks a raw original-manifest readback. With that deployment a verified production P0-P2 chain remains blocked. Production changes and human release are separate decisions.
