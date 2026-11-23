# Requires Windows with Microsoft Excel Desktop installed.
# Recalculates a read-only source and saves a distinct, never-overwritten copy.
# Does not certify the structural design or EC2 parameter choices.
# v1.2 COM hotfix: move Calculation=-4105 after Workbooks.Open (v1.1 QA retained).
# UNTESTED on Excel Desktop: requires an actual Windows E2E run.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)] [string] $InputXlsx,
    [Parameter(Mandatory = $true)] [string] $OutputDirectory,
    [string] $ExpectedSha256 = "a921f515c3d56b281a47343ff5ee39c65e8cc2093fe371ef048006c4a55810f9"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-ExcelFormulaAudit {
    param([Parameter(Mandatory = $true)] [object] $Workbook)
    $details = [System.Collections.Generic.List[object]]::new()
    $warnings = [System.Collections.Generic.List[string]]::new()
    $noMatches = [System.Collections.Generic.List[string]]::new()
    [long] $formulaCount = 0
    foreach ($sheet in $Workbook.Worksheets) {
        $allFormulaCells = $null
        $errorCells = $null
        try { $allFormulaCells = $sheet.UsedRange.SpecialCells(-4123) }
        catch {
            if ($_.Exception.Message -match "(?i)no cells were found|keine zellen gefunden") {
                $noMatches.Add("$($sheet.Name) / formula cells: none")
            } else { $warnings.Add("$($sheet.Name) / formula SpecialCells: $($_.Exception.Message)") }
        }
        if ($null -ne $allFormulaCells) {
            $formulaCount += [long] $allFormulaCells.Cells.CountLarge
        }
        try { $errorCells = $sheet.UsedRange.SpecialCells(-4123, 16) }
        catch {
            if ($_.Exception.Message -match "(?i)no cells were found|keine zellen gefunden") {
                $noMatches.Add("$($sheet.Name) / formula errors: none")
            } else { $warnings.Add("$($sheet.Name) / error SpecialCells: $($_.Exception.Message)") }
        }
        if ($null -ne $errorCells) {
            foreach ($cell in $errorCells.Cells) {
                $details.Add([pscustomobject]@{
                    Sheet = [string] $sheet.Name
                    Cell = [string] $cell.Address($false, $false)
                    Error = [string] $cell.Text
                    Formula = [string] $cell.Formula
                })
            }
        }
    }
    return [pscustomobject]@{
        SheetCount = [int] $Workbook.Worksheets.Count
        FormulaCells = $formulaCount
        FormulaErrors = $details.Count
        Details = @($details.ToArray())
        QueryWarnings = @($warnings.ToArray())
        NoMatchDiagnostics = @($noMatches.ToArray())
    }
}

function Release-ComObject {
    param([object] $Instance)
    if ($null -ne $Instance) {
        [void] [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($Instance)
    }
}

$source = (Resolve-Path -LiteralPath $InputXlsx).Path
$actualHash = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actualHash -ne $ExpectedSha256.ToLowerInvariant()) {
    throw "STOP: Vers-D input SHA256 mismatch: $actualHash"
}

[void] (New-Item -ItemType Directory -Path $OutputDirectory -Force)
$outputFolder = (Resolve-Path -LiteralPath $OutputDirectory).Path
$stamp = (Get-Date).ToString("yyyyMMdd_HHmmss")
$destination = Join-Path $outputFolder "P205_FT_Vers_D_EXCEL_NATIVE_$stamp.xlsx"
$reportFile = Join-Path $outputFolder "P205_FT_Vers_D_EXCEL_NATIVE_$stamp.json"
$errorsFile = Join-Path $outputFolder "P205_FT_Vers_D_EXCEL_NATIVE_$stamp-errors.csv"
if (Test-Path -LiteralPath $destination) { throw "Output already exists: $destination" }

$excel = $null
$book = $null
$verify = $null
try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    $excel.AskToUpdateLinks = $false
    $excel.EnableEvents = $false
    $excel.AutomationSecurity = 3  # msoAutomationSecurityForceDisable
    # Excel.Application.Calculation requires an open workbook (avoids COM 0x800A03EC).
    $book = $excel.Workbooks.Open($source, 0, $true)
    if ($null -eq $book) { throw "STOP: Excel failed to open input workbook" }
    $excel.Calculation = -4105     # xlCalculationAutomatic
    $book.ForceFullCalculation = $true
    $book.FullCalculationOnLoad = $true
    if ([int] $book.Worksheets.Count -ne 106) {
        throw "STOP: unexpected source sheet count: $($book.Worksheets.Count)"
    }

    $excel.CalculateFullRebuild()
    $deadline = (Get-Date).AddMinutes(15)
    while ([int] $excel.CalculationState -ne 0) {
        if ((Get-Date) -ge $deadline) { throw "STOP: Excel calculation timeout" }
        Start-Sleep -Milliseconds 500
    }

    $sourceAudit = Get-ExcelFormulaAudit -Workbook $book
    if ($sourceAudit.FormulaCells -ne 239689) {
        throw "STOP: unexpected formula count after rebuild: $($sourceAudit.FormulaCells)"
    }

    $book.SaveCopyAs($destination)
    # Reopen under manual calculation: avoid silent recalculation of the saved copy.
    $excel.Calculation = -4135  # xlCalculationManual
    $verify = $excel.Workbooks.Open($destination, 0, $true)
    $copyAudit = Get-ExcelFormulaAudit -Workbook $verify
    if ($copyAudit.SheetCount -ne 106 -or $copyAudit.FormulaCells -ne 239689) {
        throw "STOP: reopened copy changed sheet/formula count"
    }

    $copyAudit.Details | Export-Csv -Path $errorsFile -NoTypeInformation -Encoding UTF8
    $auditWarnings = @($sourceAudit.QueryWarnings) + @($copyAudit.QueryWarnings)
    $result = [ordered]@{
        Project = "P205_Campus_Eisteiche_BIG / FT-Traeger-Matrix Vers-D"
        TimestampUtc = (Get-Date).ToUniversalTime().ToString("o")
        Engine = "Microsoft Excel Desktop"
        EngineVersion = [string] $excel.Version
        Method = "Workbooks.Open ReadOnly + CalculateFullRebuild + SaveCopyAs + reopen audit"
        SourcePath = $source
        SourceSha256 = $actualHash
        OutputPath = $destination
        OutputSha256 = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant()
        SheetCount = $copyAudit.SheetCount
        FormulaCells = $copyAudit.FormulaCells
        FormulaErrors = $copyAudit.FormulaErrors
        QueryWarnings = $auditWarnings
        NoMatchDiagnostics = @($sourceAudit.NoMatchDiagnostics) + @($copyAudit.NoMatchDiagnostics)
        ErrorListCsv = $errorsFile
        Status = if ($auditWarnings.Count -gt 0) { "AUDIT_INDETERMINATE" } elseif ($copyAudit.FormulaErrors -eq 0) { "REVIEW_REQUIRED_PERSISTED_CACHE_CHECK_PENDING" } else { "BLOCKED_FORMULA_ERRORS" }
        Note = "COM readback only. Persisted OOXML cache/formula check mandatory. SpecialCells no-match warnings may be benign; verify independently. Not EC2 design approval."
    }
    $result | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $reportFile -Encoding UTF8
    $finalSourceHash = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($finalSourceHash -ne $actualHash) { throw "STOP: original source hash changed" }
    $result | ConvertTo-Json -Depth 5
}
finally {
    if ($null -ne $verify) { $verify.Close($false) }
    if ($null -ne $book) { $book.Close($false) }
    if ($null -ne $excel) { $excel.Quit() }
    Release-ComObject $verify
    Release-ComObject $book
    Release-ComObject $excel
}
