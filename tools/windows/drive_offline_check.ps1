<#
name: drive-offline-check
description: Checks whether NEXUS bridge folders on Google Drive for desktop (G:) are locally readable without cloud wait; measures cold-read latency of governance files. Read-only.
version: 0.1.0
status: REVIEW_CANDIDATE (untested on target PC)
timestamp: 2026-11-16T22:35+01:00
usage:  powershell -ExecutionPolicy Bypass -File .\26_11_16_2235_IDxx_DRIVE-OFFLINE-CHECK_UNNUMBERED.ps1 [-Root "G:\Meine Ablage\_developement"]
note:   "Available offline" itself is set manually in Explorer (right-click > Offline access > Available offline).
        No documented CLI/API exists for this setting; this script only verifies the effect.
#>
param([string]$Root = "G:\Meine Ablage\_developement")

$targets = @(
  "LLM-LOCAL-SSOT\WORK\Folder.md",
  "LLM-LOCAL-SSOT\WORK\_AGBS.md",
  "LLM-LOCAL-SSOT\00_NEXUS_MANIFEST__CURRENT__2026-09-28.md",
  "LLM-LOCAL-SSOT\00_NEXUS_BASELINE_INSTRUCTIONS__CURRENT__2026-09-28.md",
  "MCP-ACCESS-TOOLS\nexus_ssot_mcp.py"
)
$rows = foreach ($t in $targets) {
  $p = Join-Path $Root $t
  if (-not (Test-Path -LiteralPath $p)) { [pscustomobject]@{File=$t; Exists=$false; ReadMs=$null; Bytes=$null; Verdict="MISSING"}; continue }
  $sw = [Diagnostics.Stopwatch]::StartNew()
  $bytes = [IO.File]::ReadAllBytes($p)
  $sw.Stop()
  $ms = [math]::Round($sw.Elapsed.TotalMilliseconds,1)
  [pscustomobject]@{File=$t; Exists=$true; ReadMs=$ms; Bytes=$bytes.Length; Verdict= $(if ($ms -lt 200) {"LOCAL_OK"} else {"SLOW_CLOUD_FETCH?"})}
}
$rows | Format-Table -AutoSize
$bad = @($rows | Where-Object { $_.Verdict -ne "LOCAL_OK" }).Count
Write-Host ("RESULT: {0}" -f $(if ($bad -eq 0) {"PASS - all governance files read locally (<200 ms)"} else {"FAIL - $bad file(s) missing or slow; set folder 'Available offline' and rerun"}))
Write-Host "Test offline: disconnect network, rerun -> PASS required."
exit $bad
