<#
Read-only NEXUS diagnostic. Windows PowerShell 5.1+.
Latency cannot prove offline pinning or network isolation.
Disconnect network manually, then use -OfflineConfirmed to record that user
attestation. No adapter, Drive setting, policy or file is changed.
Exit: 0 readable + attested offline; 1 file failure; 2 offline unverified.
#>
param(
    [string]$Root = "G:\Meine Ablage\_developement",
    [switch]$OfflineConfirmed,
    [switch]$AsJson
)
$targets = @(
    "LLM-LOCAL-SSOT\WORK\Folder.md",
    "LLM-LOCAL-SSOT\WORK\_AGBS.md",
    "LLM-LOCAL-SSOT\00_NEXUS_MANIFEST__CURRENT__2026-09-28.md",
    "LLM-LOCAL-SSOT\00_NEXUS_BASELINE_INSTRUCTIONS__CURRENT__2026-09-28.md",
    "MCP-ACCESS-TOOLS\nexus_ssot_mcp.py"
)
$utf8 = New-Object System.Text.UTF8Encoding($false, $true)
$rows = @(foreach ($target in $targets) {
    $path = Join-Path $Root $target
    $row = [ordered]@{ File=$target; Bytes=$null; ReadMs=$null; SHA256=$null; Status="UNREADABLE" }
    $watch = [Diagnostics.Stopwatch]::StartNew()
    try {
        if (-not (Test-Path -LiteralPath $path -PathType Leaf -ErrorAction Stop)) {
            $row.Status = "MISSING_OR_NOT_FILE"
        } else {
            $bytes = [IO.File]::ReadAllBytes($path)
            $row.Bytes = $bytes.Length
            $text = $utf8.GetString($bytes)
            if ([string]::IsNullOrWhiteSpace($text.TrimStart([char]0xFEFF))) {
                $row.Status = "EMPTY"
            } else {
                $hasher = [Security.Cryptography.SHA256]::Create()
                try { $row.SHA256 = ([BitConverter]::ToString($hasher.ComputeHash($bytes))).Replace("-", "").ToLowerInvariant() }
                finally { $hasher.Dispose() }
                $row.Status = "READABLE"
            }
        }
    } catch [System.Text.DecoderFallbackException] {
        $row.Status = "INVALID_UTF8"
    } catch {
        $row.Status = "READ_ERROR"
    } finally {
        $watch.Stop()
        $row.ReadMs = [math]::Round($watch.Elapsed.TotalMilliseconds, 1)
    }
    [pscustomobject]$row
})
$failed = @($rows | Where-Object { $_.Status -ne "READABLE" }).Count
$offline = if ($OfflineConfirmed) { "USER_ATTESTED_NETWORK_DISCONNECTED" } else { "NOT_VERIFIED" }
$code = if ($failed -gt 0) { 1 } elseif ($OfflineConfirmed) { 0 } else { 2 }
$status = if ($failed -gt 0) { "FILE_CHECK_FAILED" } elseif ($OfflineConfirmed) { "OFFLINE_READ_PASS_USER_ATTESTED" } else { "READABLE_OFFLINE_UNVERIFIED" }
$result = [ordered]@{
    SchemaVersion="0.2.0"; Status=$status; OfflineEvidence=$offline
    PinningEvidence="NOT_VERIFIED"; PolicyAuthorization="NOT_EVALUATED"
    ObservedAt=[DateTimeOffset]::Now.ToString("o"); Files=$rows; ExitCode=$code
}
if ($AsJson) { $result | ConvertTo-Json -Depth 5 }
else {
    $rows | Format-Table -AutoSize
    Write-Host ("RESULT: {0}; offline={1}; pinning=NOT_VERIFIED" -f $status, $offline)
    Write-Host "Latency does not prove offline access. Disconnect network manually and rerun with -OfflineConfirmed."
}
exit $code

