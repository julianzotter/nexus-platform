[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$InputXlsx,

    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$OutputDirectory,

    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[A-Fa-f0-9]{64}$')]
    [string]$ExpectedSha256,

    [ValidateRange(30, 7200)]
    [int]$TimeoutSeconds = 900
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Release-ComObject {
    param([object]$ComObject)
    if ($null -ne $ComObject -and [Runtime.InteropServices.Marshal]::IsComObject($ComObject)) {
        [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($ComObject)
    }
}

function Wait-ForExcelCalculation {
    param(
        [Parameter(Mandatory = $true)][object]$Excel,
        [Parameter(Mandatory = $true)][int]$Timeout
    )
    $deadline = [DateTime]::UtcNow.AddSeconds($Timeout)
    while ($Excel.CalculationState -ne 0) {
        if ([DateTime]::UtcNow -ge $deadline) {
            throw 'E_EXCEL_CALCULATION_TIMEOUT'
        }
        Start-Sleep -Milliseconds 250
    }
}

function Get-LinkSources {
    param([Parameter(Mandatory = $true)][object]$Workbook)
    $links = $Workbook.LinkSources(1)
    if ($null -eq $links) { return @() }
    return @($links | ForEach-Object { [string]$_ })
}

$sourcePath = [IO.Path]::GetFullPath($InputXlsx)
$outputRoot = [IO.Path]::GetFullPath($OutputDirectory)

if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
    throw "E_INPUT_NOT_FOUND: $sourcePath"
}
if ([IO.Path]::GetExtension($sourcePath) -notin @('.xlsx', '.xlsm', '.xlsb')) {
    throw 'E_INPUT_TYPE_NOT_SUPPORTED'
}

$sourceHashBefore = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($sourceHashBefore -ne $ExpectedSha256.ToLowerInvariant()) {
    throw "E_SOURCE_HASH_MISMATCH: expected=$($ExpectedSha256.ToLowerInvariant()) actual=$sourceHashBefore"
}

New-Item -ItemType Directory -Path $outputRoot -Force | Out-Null
$runId = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')
$copyName = "{0}__NATIVE-RECALC__{1}{2}" -f @(
    [IO.Path]::GetFileNameWithoutExtension($sourcePath),
    $runId,
    [IO.Path]::GetExtension($sourcePath)
)
$copyPath = Join-Path $outputRoot $copyName
$reportPath = Join-Path $outputRoot ("P205_FT_EXCEL_E2E__{0}.json" -f $runId)

$excel = $null
$sourceWorkbook = $null
$copyWorkbook = $null
$report = [ordered]@{
    schema_version = '1.0'
    run_id = $runId
    status = 'RUNNING'
    source_sha256_before = $sourceHashBefore
    output_sha256 = $null
    source_unchanged = $false
    excel_version = $null
    excel_build = $null
    calculation = 'NOT_STARTED'
    external_links = @()
    connection_count = $null
    query_count = $null
    started_at_utc = [DateTime]::UtcNow.ToString('o')
    completed_at_utc = $null
    error_code = $null
}

try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    $excel.AskToUpdateLinks = $false
    $excel.AutomationSecurity = 3
    $report.excel_version = [string]$excel.Version
    $report.excel_build = [string]$excel.Build

    # Source is always read-only. Link updates and macros are disabled.
    $sourceWorkbook = $excel.Workbooks.Open($sourcePath, 0, $true)
    $report.external_links = @(Get-LinkSources -Workbook $sourceWorkbook)
    $report.connection_count = [int]$sourceWorkbook.Connections.Count
    try { $report.query_count = [int]$sourceWorkbook.Queries.Count } catch { $report.query_count = $null }

    $excel.CalculateFullRebuild()
    Wait-ForExcelCalculation -Excel $excel -Timeout $TimeoutSeconds
    $report.calculation = 'SOURCE_FULL_REBUILD_COMPLETE'
    $sourceWorkbook.SaveCopyAs($copyPath)
    $sourceWorkbook.Close($false)
    Release-ComObject $sourceWorkbook
    $sourceWorkbook = $null

    # Reopen only the generated copy, recalculate, save and close to persist caches.
    $copyWorkbook = $excel.Workbooks.Open($copyPath, 0, $false)
    $excel.CalculateFullRebuild()
    Wait-ForExcelCalculation -Excel $excel -Timeout $TimeoutSeconds
    $copyWorkbook.Save()
    $copyWorkbook.Close($true)
    Release-ComObject $copyWorkbook
    $copyWorkbook = $null

    $sourceHashAfter = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($sourceHashAfter -ne $sourceHashBefore) {
        throw 'E_SOURCE_MUTATED'
    }
    $report.source_unchanged = $true
    $report.output_sha256 = (Get-FileHash -LiteralPath $copyPath -Algorithm SHA256).Hash.ToLowerInvariant()
    $report.calculation = 'FULL_REBUILD_SAVE_CLOSE_COMPLETE'
    $report.status = 'COMPLETE'
}
catch {
    $report.status = 'FAILED'
    $report.error_code = $_.Exception.Message
    throw
}
finally {
    if ($null -ne $copyWorkbook) {
        try { $copyWorkbook.Close($false) } catch {}
        Release-ComObject $copyWorkbook
    }
    if ($null -ne $sourceWorkbook) {
        try { $sourceWorkbook.Close($false) } catch {}
        Release-ComObject $sourceWorkbook
    }
    if ($null -ne $excel) {
        try { $excel.Quit() } catch {}
        Release-ComObject $excel
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
    $report.completed_at_utc = [DateTime]::UtcNow.ToString('o')
    $report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $reportPath -Encoding UTF8
}

Write-Output ($report | ConvertTo-Json -Depth 8)
