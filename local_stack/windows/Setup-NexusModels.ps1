# NEXUS Local Stack - Ollama-Modelle einrichten + messen (RTX 3080 10 GB). v0.1.0
#   powershell -ExecutionPolicy Bypass -File .\Setup-NexusModels.ps1
#   ... -NoPull     keine Downloads, nur Varianten/Benchmark fuer vorhandene Modelle
param([string]$ConfigPath = (Join-Path $env:LOCALAPPDATA "NEXUS\local\nexus-local.json"), [switch]$NoPull, [switch]$SkipNestedFix)
$ErrorActionPreference = "Stop"
$api = "http://127.0.0.1:11434"
$models = Join-Path $env:USERPROFILE ".ollama\models"
$mfDir = Join-Path $env:USERPROFILE ".ollama\modelfiles"
$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$out = Join-Path $env:LOCALAPPDATA "NEXUS\local\tests"
New-Item -ItemType Directory -Force -Path $mfDir, $out | Out-Null
function Wait-Ollama { for ($i = 0; $i -lt 60; $i++) { try { Invoke-RestMethod "$api/api/version" -TimeoutSec 2 | Out-Null; return $true } catch { Start-Sleep 1 } }; $false }

# ---------------------------------------------------------------- 1 Umgebungsvariablen (Benutzer)
$envs = [ordered]@{ OLLAMA_FLASH_ATTENTION = "1"; OLLAMA_KV_CACHE_TYPE = "q8_0"; OLLAMA_NUM_PARALLEL = "1";
                    OLLAMA_MAX_LOADED_MODELS = "1"; OLLAMA_KEEP_ALIVE = "30m"; OLLAMA_HOST = "127.0.0.1:11434" }
$changed = $false
foreach ($k in $envs.Keys) {
  if ([Environment]::GetEnvironmentVariable($k, "User") -ne $envs[$k]) { [Environment]::SetEnvironmentVariable($k, $envs[$k], "User"); $changed = $true }
  Write-Host ("{0,-26} = {1}" -f $k, $envs[$k])
}

# ---------------------------------------------------------------- 2 Verschachtelte Kopie unter llama3.2 sichern (verschieben, nicht loeschen)
$nested = Join-Path $models "manifests\registry.ollama.ai\library\llama3.2"
$nestedDirs = @("blobs", "manifests", "manifests-v2", "metadata") | Where-Object { Test-Path (Join-Path $nested $_) }
if (-not $SkipNestedFix -and $nestedDirs) {
  Write-Host "`nVerschachtelte Ollama-Kopie gefunden: $($nestedDirs -join ', ')"
  $latest = Join-Path $nested "latest"
  $man = Get-Content $latest -Raw | ConvertFrom-Json
  foreach ($d in @($man.config.digest) + @($man.layers | ForEach-Object { $_.digest })) {
    $top = Join-Path $models ("blobs\" + ($d -replace ":", "-"))
    if (-not (Test-Path $top)) {
      $alt = Join-Path $nested ("blobs\" + ($d -replace ":", "-"))
      if (Test-Path $alt) { Copy-Item $alt $top } else { throw "Blob $d fehlt ueberall - Abbruch, nichts verschoben" }
    }
  }
  $root = "C:\NEXUS\ollama_backup"
  try { New-Item -ItemType Directory -Force -Path $root | Out-Null } catch { $root = Join-Path $env:USERPROFILE "ollama_backup"; New-Item -ItemType Directory -Force -Path $root | Out-Null }
  $bk = Join-Path $root "llama3.2_nested_$ts"
  Write-Host "Bitte Ollama ueber das Tray-Symbol BEENDEN, dann Enter." -ForegroundColor Yellow; Read-Host | Out-Null
  New-Item -ItemType Directory -Force -Path $bk | Out-Null
  foreach ($n in $nestedDirs) { Move-Item (Join-Path $nested $n) (Join-Path $bk $n); Write-Host "VERSCHOBEN: $n -> $bk" }
  $changed = $true
}
if ($changed) {
  Write-Host "`nOllama jetzt (neu) starten: Startmenue -> Ollama. Danach Enter." -ForegroundColor Yellow; Read-Host | Out-Null
}
if (-not (Wait-Ollama)) { throw "Ollama antwortet nicht auf $api" }

# ---------------------------------------------------------------- 3 Modelle + Varianten
if (-not $NoPull) { ollama pull qwen3.5:9b; ollama pull qwen3.5:4b }
$variants = @(
  @{ name = "nexus-q35-9b-16k"; from = "qwen3.5:9b"; ctx = 16384 },
  @{ name = "nexus-q35-9b-32k"; from = "qwen3.5:9b"; ctx = 32768 },
  @{ name = "nexus-q35-4b-32k"; from = "qwen3.5:4b"; ctx = 32768 }
)
$have = (ollama list) -join "`n"
foreach ($v in $variants) {
  if ($have -notmatch [regex]::Escape($v.from)) { Write-Host "UEBERSPRUNGEN $($v.name): $($v.from) nicht installiert"; $v.skip = $true; continue }
  $mf = Join-Path $mfDir "Modelfile-$($v.name)"
  "FROM $($v.from)`nPARAMETER num_ctx $($v.ctx)`n" | Set-Content -Encoding ascii $mf
  ollama create $v.name -f $mf | Out-Null
  Write-Host "[OK] $($v.name) (num_ctx $($v.ctx))"
}

# ---------------------------------------------------------------- 4 Messung (kalt + warm)
$prompt = "Erklaere in 5 Saetzen den Unterschied zwischen Biegung und Querkraft bei einem Einfeldtraeger. Antworte auf Deutsch."
$rows = @()
foreach ($v in $variants | Where-Object { -not $_.skip }) {
  foreach ($phase in "kalt", "warm") {
    $body = @{ model = $v.name; stream = $false; messages = @(@{ role = "user"; content = $prompt }); options = @{ num_predict = 200; temperature = 0 } } | ConvertTo-Json -Depth 5
    $sw = [Diagnostics.Stopwatch]::StartNew()
    try { $r = Invoke-RestMethod "$api/api/chat" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 600 } catch { $rows += [pscustomobject]@{ model = $v.name; phase = $phase; status = "FAIL $($_.Exception.Message)" }; continue }
    $sw.Stop()
    $ps = (Invoke-RestMethod "$api/api/ps").models | Where-Object { $_.name -like "$($v.name)*" } | Select-Object -First 1
    $tps = if ($r.eval_duration) { [math]::Round($r.eval_count / ($r.eval_duration / 1e9), 1) } else { $null }
    $gpu = if ($ps.size) { [math]::Round(100 * $ps.size_vram / $ps.size) } else { $null }
    $smi = $null; try { $smi = (& nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits) -join " " } catch {}
    $rows += [pscustomobject]@{ model = $v.name; phase = $phase; status = "OK"; seconds = [math]::Round($sw.Elapsed.TotalSeconds, 1)
      tokens_per_s = $tps; context = $ps.context_length; size_gb = [math]::Round($ps.size / 1e9, 2); vram_gb = [math]::Round($ps.size_vram / 1e9, 2)
      gpu_pct = $gpu; nvidia_smi_used_total_mib = $smi }
  }
  try { ollama stop $v.name | Out-Null } catch {}
}
$rows | Format-Table -AutoSize | Out-String | Write-Host
$rows | ConvertTo-Json -Depth 4 | Set-Content -Encoding utf8 (Join-Path $out "model_bench_$ts.json")

# ---------------------------------------------------------------- 5 Standardmodell waehlen (gemessen, nicht angenommen)
$best = $rows | Where-Object { $_.phase -eq "warm" -and $_.status -eq "OK" -and $_.gpu_pct -ge 100 -and $_.tokens_per_s -ge 15 } |
        Sort-Object @{ e = { if ($_.model -like "*9b*") { 1 } else { 0 } } }, context -Descending | Select-Object -First 1
if ($best -and (Test-Path $ConfigPath)) {
  Copy-Item $ConfigPath "$ConfigPath.bak_$ts"
  $c = Get-Content $ConfigPath -Raw | ConvertFrom-Json
  $c.ollama.default_model = $best.model
  $c | ConvertTo-Json -Depth 10 | Set-Content -Encoding utf8 $ConfigPath
  Write-Host "Standardmodell (gemessen): $($best.model)  ctx=$($best.context)  $($best.tokens_per_s) tok/s  100% GPU" -ForegroundColor Green
} else { Write-Host "Kein Modell erfuellt 100% GPU + >=15 tok/s -> Standard bleibt unveraendert. Bericht: $out\model_bench_$ts.json" -ForegroundColor Yellow }
Write-Host "DeepSeek Harness: Base URL http://127.0.0.1:11434/v1  Model-ID = obiges Standardmodell, neue Session."
