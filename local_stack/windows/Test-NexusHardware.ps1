# Test-NexusHardware.ps1 - einmaliger Hardware- und Modell-Abnahmetest (Windows PowerShell 5.1)
# Nur lesend, ausser: legt fehlende nexus-q35-* Modellvarianten per "ollama create" an.
# Ausgabe: %LOCALAPPDATA%\NEXUS\local\reports\hwbench_<ts>.json + .md (Inhalt bitte an ID05 senden)
param(
  [string]$Api = "http://127.0.0.1:11434",
  [switch]$PullFallback,          # laedt qwen3.5:4b (ca. 3.4 GB) fuer den Fallback-Test
  [int]$NumPredict = 256
)
$ErrorActionPreference = "Stop"
$ts  = Get-Date -Format "yyyyMMdd_HHmmss"
$out = Join-Path $env:LOCALAPPDATA "NEXUS\local\reports"
New-Item -ItemType Directory -Force -Path $out | Out-Null
$REP = [ordered]@{ timestamp = (Get-Date).ToString("s"); host = $env:COMPUTERNAME; hardware = [ordered]@{}; tests = @(); state = "RUNNING" }
$jsonPath = "$out\hwbench_$ts.json"
function Save { $script:REP | ConvertTo-Json -Depth 10 | Set-Content -Encoding UTF8 $script:jsonPath }
trap { $script:REP.state = "ABORTED: $($_.Exception.Message)"; Save; Write-Host "[ABBRUCH] $($_.Exception.Message) -> $jsonPath" -ForegroundColor Red; break }
Write-Host "Zwischenstand laufend in: $jsonPath" -ForegroundColor Cyan

function Add-Test($id, $name, $status, $data) {
  $script:REP.tests += [ordered]@{ id = $id; name = $name; status = $status; data = $data }
  $c = @{ PASS = "Green"; FAIL = "Red"; WARN = "Yellow"; INFO = "Cyan"; NOT_RUN = "DarkGray" }[$status]
  Write-Host ("[{0}] {1} {2}" -f $status, $id, $name) -ForegroundColor $c
  Save
}
function Post($path, $obj, $timeout = 600) {
  $json  = $obj | ConvertTo-Json -Depth 10 -Compress
  $bytes = [Text.Encoding]::UTF8.GetBytes($json)
  Invoke-RestMethod -Uri "$Api$path" -Method Post -Body $bytes -ContentType "application/json; charset=utf-8" -TimeoutSec $timeout
}
function Smi($q) {
  $exe = Get-Command nvidia-smi -ErrorAction SilentlyContinue
  if (-not $exe) { return $null }
  (& $exe.Source "--query-gpu=$q" "--format=csv,noheader,nounits" 2>$null | Select-Object -First 1)
}
function CpuPct { [int]((Get-CimInstance Win32_PerfFormattedData_PerfOS_Processor -Filter "Name='_Total'").PercentProcessorTime) }

# ---------- H: Hardware ----------
$cs  = Get-CimInstance Win32_ComputerSystem
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
$os  = Get-CimInstance Win32_OperatingSystem
$mem = Get-CimInstance Win32_PhysicalMemory
$dsk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
$REP.hardware.system = "$($cs.Manufacturer) $($cs.Model)"
$REP.hardware.os     = "$($os.Caption) build $($os.BuildNumber)"
$REP.hardware.cpu    = [ordered]@{ name = $cpu.Name.Trim(); cores = $cpu.NumberOfCores; threads = $cpu.NumberOfLogicalProcessors; max_mhz = $cpu.MaxClockSpeed }
$REP.hardware.ram    = [ordered]@{ total_gb = [math]::Round($cs.TotalPhysicalMemory / 1GB, 1); modules = @($mem).Count; speed_mts = (@($mem | ForEach-Object { $_.ConfiguredClockSpeed }) | Measure-Object -Maximum).Maximum }
$REP.hardware.disk_c = [ordered]@{ size_gb = [math]::Round($dsk.Size / 1GB, 0); free_gb = [math]::Round($dsk.FreeSpace / 1GB, 0) }
$g = Smi "name,memory.total,driver_version,compute_cap,pcie.link.gen.max,pcie.link.width.max,power.limit"
if ($g) {
  $p = $g -split ",\s*"
  $hdr = (& nvidia-smi 2>$null | Select-String "CUDA Version:\s*([\d.]+)").Matches
  $REP.hardware.gpu = [ordered]@{ name = $p[0]; vram_mib = [int]$p[1]; driver = $p[2]; compute_cap = $p[3]; pcie = "Gen$($p[4]) x$($p[5])"; power_limit_w = $p[6]; driver_cuda_max = $(if ($hdr) { $hdr[0].Groups[1].Value } else { "?" }) }
  Add-Test "H01" "NVIDIA-Treiber + GPU erkannt" "PASS" $REP.hardware.gpu
} else {
  $vc = Get-CimInstance Win32_VideoController | Select-Object -First 1
  $REP.hardware.gpu = [ordered]@{ name = $vc.Name; driver = $vc.DriverVersion; note = "nvidia-smi fehlt" }
  Add-Test "H01" "NVIDIA-Treiber + GPU erkannt" "FAIL" $REP.hardware.gpu
}
$nvcc = Get-Command nvcc -ErrorAction SilentlyContinue
$cudaTk = if ($nvcc) { ((& nvcc --version) | Select-String "release ([\d.]+)").Matches[0].Groups[1].Value } else { $null }
Add-Test "H02" "CUDA-Toolkit (nvcc) - fuer Ollama NICHT noetig (bringt eigene CUDA-Runtime mit)" "INFO" @{ nvcc = $(if ($cudaTk) { $cudaTk } else { "nicht installiert" }) }
Add-Test "H03" "Systemdaten" "INFO" ([ordered]@{ cpu = $REP.hardware.cpu; ram = $REP.hardware.ram; disk_c = $REP.hardware.disk_c; os = $REP.hardware.os })

# ---------- E: Ollama-Umgebung ----------
try { $ver = (Invoke-RestMethod "$Api/api/version" -TimeoutSec 5).version; Add-Test "E01" "Ollama erreichbar" "PASS" @{ version = $ver; api = $Api } }
catch { Add-Test "E01" "Ollama erreichbar" "FAIL" @{ error = "$_" }; $REP.state = "ABORTED: Ollama nicht erreichbar"; Save; exit 1 }
$envs = [ordered]@{}
foreach ($k in "OLLAMA_FLASH_ATTENTION","OLLAMA_KV_CACHE_TYPE","OLLAMA_NUM_PARALLEL","OLLAMA_MAX_LOADED_MODELS","OLLAMA_KEEP_ALIVE","OLLAMA_HOST","OLLAMA_CONTEXT_LENGTH","OLLAMA_MODELS") {
  $envs[$k] = [Environment]::GetEnvironmentVariable($k, "User")
}
$envOk = ($envs.OLLAMA_FLASH_ATTENTION -eq "1" -and $envs.OLLAMA_KV_CACHE_TYPE -eq "q8_0")
Add-Test "E02" "Ollama-Umgebungsvariablen (User)" $(if ($envOk) { "PASS" } else { "WARN" }) $envs

# ---------- Modellvarianten sicherstellen ----------
$have = @((Invoke-RestMethod "$Api/api/tags").models | ForEach-Object { $_.name })
$variants = @(
  @{ name = "nexus-q35-9b-16k"; from = "qwen3.5:9b"; ctx = 16384 },
  @{ name = "nexus-q35-9b-32k"; from = "qwen3.5:9b"; ctx = 32768 },
  @{ name = "nexus-q35-9b-64k"; from = "qwen3.5:9b"; ctx = 65536 }
)
if ($PullFallback -and -not ($have -contains "qwen3.5:4b")) { & ollama pull qwen3.5:4b; $have += "qwen3.5:4b" }
if ($have -contains "qwen3.5:4b") { $variants += @{ name = "nexus-q35-4b-32k"; from = "qwen3.5:4b"; ctx = 32768 } }
Write-Host "Modellvarianten pruefen/anlegen ..." -ForegroundColor Cyan
foreach ($v in $variants) {
  if (-not ($have -contains "$($v.name):latest")) {
    $mf = Join-Path $env:TEMP "Modelfile-$($v.name)"
    "FROM $($v.from)`nPARAMETER num_ctx $($v.ctx)`n" | Set-Content -Encoding ascii $mf
    & ollama create $v.name -f $mf | Out-Null
  }
}

# ---------- B: Geschwindigkeit + GPU-Residenz je Variante ----------
$prompt = "Erklaere in 150 Woertern, wie ein lokaler LLM-Agent Dateien sicher zwischen zwei Ordnern synchronisiert."
$rows = @()
foreach ($v in $variants) {
  Write-Host "Messung $($v.name) ..." -ForegroundColor Cyan
  foreach ($m in @((Invoke-RestMethod "$Api/api/ps").models)) { Post "/api/generate" @{ model = $m.name; keep_alive = 0 } 60 | Out-Null }
  Start-Sleep -Seconds 2
  $vram0 = Smi "memory.used"
  $cpuS = @(); $job = $null
  $sw = [Diagnostics.Stopwatch]::StartNew()
  try {
    $r1 = Post "/api/generate" @{ model = $v.name; prompt = "OK"; stream = $false; think = $false; options = @{ num_predict = 1 } }    # kalt: laden
    $cold = [math]::Round($r1.load_duration / 1e9, 1)
    $job = Start-Job -ScriptBlock { 1..60 | ForEach-Object { [int]((Get-CimInstance Win32_PerfFormattedData_PerfOS_Processor -Filter "Name='_Total'").PercentProcessorTime); Start-Sleep -Milliseconds 500 } }
    $r = Post "/api/generate" @{ model = $v.name; prompt = $prompt; stream = $false; think = $false; options = @{ num_predict = $NumPredict; temperature = 0 } }
    $cpuS = @(Receive-Job $job -ErrorAction SilentlyContinue)
    $ps = (Invoke-RestMethod "$Api/api/ps").models | Where-Object { $_.name -like "$($v.name)*" } | Select-Object -First 1
    $vram1 = Smi "memory.used"
    $tps = if ($r.eval_duration -gt 0) { [math]::Round($r.eval_count / ($r.eval_duration / 1e9), 1) } else { 0 }
    $pps = if ($r.prompt_eval_duration -gt 0) { [math]::Round($r.prompt_eval_count / ($r.prompt_eval_duration / 1e9), 1) } else { 0 }
    $gpu = if ($ps.size -gt 0) { [math]::Round(100 * $ps.size_vram / $ps.size, 0) } else { 0 }
    $row = [ordered]@{ model = $v.name; ctx = $v.ctx; load_s = $cold; eval_tokens = $r.eval_count; eval_tps = $tps; prompt_tps = $pps; size_gb = [math]::Round($ps.size / 1e9, 2); vram_gb = [math]::Round($ps.size_vram / 1e9, 2); gpu_pct = $gpu; vram_used_mib = $vram1; vram_idle_mib = $vram0; cpu_avg_pct = $(if ($cpuS.Count) { [math]::Round(($cpuS | Measure-Object -Average).Average, 0) } else { $null }); cpu_max_pct = $(if ($cpuS.Count) { ($cpuS | Measure-Object -Maximum).Maximum } else { $null }) }
    $st = if ($gpu -ge 100 -and $tps -ge 15 -and $r.eval_count -ge 100) { "PASS" } elseif ($gpu -ge 100) { "WARN" } else { "FAIL" }
  } catch { $row = [ordered]@{ model = $v.name; ctx = $v.ctx; error = "$_" }; $st = "FAIL" }
  finally { if ($job) { Stop-Job $job -ErrorAction SilentlyContinue; Remove-Job $job -Force -ErrorAction SilentlyContinue } }
  $rows += $row
  Add-Test ("B" + $v.name) "Speed/GPU $($v.name)" $st $row
}

# ---------- L: Langer Kontext (Prefill ~12k Tokens im 16K-Modell, Faktentreue) ----------
try {
  $filler = (1..700 | ForEach-Object { "Zeile $_ : Der Bauteilkatalog listet Element E$_ mit Rasterachse A$_ und Laenge $($_ % 9 + 3) m." }) -join "`n"
  $needle = "GEHEIMCODE-NEXUS-4711"
  $lp = "$filler`nZeile 701 : Der Pruefcode lautet $needle.`n" + $filler.Substring(0, [math]::Min(4000, $filler.Length)) + "`nFrage: Wie lautet der Pruefcode? Antworte nur mit dem Code."
  $r = Post "/api/generate" @{ model = "nexus-q35-9b-16k"; prompt = $lp; stream = $false; think = $false; options = @{ num_predict = 20; temperature = 0 } } 900
  $ok = "$($r.response)" -match [regex]::Escape($needle)
  $pps = [math]::Round($r.prompt_eval_count / ($r.prompt_eval_duration / 1e9), 0)
  Add-Test "L01" "Langer Prompt 16K: Prefill + Nadel-Test" $(if ($ok -and $r.prompt_eval_count -lt 16384) { "PASS" } elseif ($ok) { "WARN" } else { "FAIL" }) ([ordered]@{ prompt_tokens = $r.prompt_eval_count; prefill_tps = $pps; total_s = [math]::Round($r.total_duration / 1e9, 1); answer = "$($r.response)".Trim() })
} catch { Add-Test "L01" "Langer Prompt 16K" "FAIL" @{ error = "$_" } }

# ---------- F: Funktionen (Tools, JSON, Thinking, Vision) ----------
try {
  $tool = @{ type = "function"; function = @{ name = "work_read"; description = "Liest eine Datei aus dem NEXUS-WORK-Ordner"; parameters = @{ type = "object"; properties = @{ path = @{ type = "string" } }; required = @("path") } } }
  $r = Post "/api/chat" @{ model = "nexus-q35-9b-16k"; stream = $false; think = $false; tools = @($tool); messages = @(@{ role = "user"; content = "Lies die Datei Folder.md im WORK-Ordner." }); options = @{ temperature = 0 } }
  $tc = $r.message.tool_calls
  $ok = $tc -and $tc[0].function.name -eq "work_read" -and "$($tc[0].function.arguments.path)" -match "Folder\.md"
  Add-Test "F01" "Tool-Calling (work_read)" $(if ($ok) { "PASS" } else { "FAIL" }) @{ tool_calls = ($tc | ConvertTo-Json -Depth 6 -Compress) }
} catch { Add-Test "F01" "Tool-Calling" "FAIL" @{ error = "$_" } }
try {
  $schema = @{ type = "object"; properties = @{ status = @{ type = "string"; enum = @("OK","FAIL") }; count = @{ type = "integer" } }; required = @("status","count") }
  $r = Post "/api/generate" @{ model = "nexus-q35-9b-16k"; prompt = "Gib status OK und count 3 als JSON aus."; stream = $false; think = $false; format = $schema; options = @{ temperature = 0 } }
  $j = $r.response | ConvertFrom-Json
  Add-Test "F02" "Strukturiertes JSON (Schema)" $(if ($j.status -eq "OK" -and $j.count -eq 3) { "PASS" } else { "FAIL" }) @{ response = $r.response }
} catch { Add-Test "F02" "Strukturiertes JSON" "FAIL" @{ error = "$_" } }
try {
  $r = Post "/api/generate" @{ model = "nexus-q35-9b-16k"; prompt = "Was ist 17*23? Antworte nur mit der Zahl."; stream = $false; think = $true; options = @{ temperature = 0; num_predict = 1024 } }
  $ok = "$($r.response)" -match "391"
  Add-Test "F03" "Thinking-Modus (17*23=391)" $(if ($ok) { "PASS" } else { "FAIL" }) @{ response = "$($r.response)".Trim(); think_chars = "$($r.thinking)".Length; total_s = [math]::Round($r.total_duration / 1e9, 1) }
} catch { Add-Test "F03" "Thinking-Modus" "FAIL" @{ error = "$_" } }
try {
  Add-Type -AssemblyName System.Drawing
  $bmp = New-Object Drawing.Bitmap 256, 96; $gr = [Drawing.Graphics]::FromImage($bmp); $gr.Clear([Drawing.Color]::White)
  $gr.DrawString("NEXUS 42", (New-Object Drawing.Font "Arial", 36), [Drawing.Brushes]::Black, 8, 18); $gr.Dispose()
  $msx = New-Object IO.MemoryStream; $bmp.Save($msx, [Drawing.Imaging.ImageFormat]::Png); $b64 = [Convert]::ToBase64String($msx.ToArray())
  $r = Post "/api/generate" @{ model = "nexus-q35-9b-16k"; prompt = "Welcher Text steht im Bild? Antworte nur mit dem Text."; images = @($b64); stream = $false; think = $false; options = @{ temperature = 0 } }
  $ok = "$($r.response)" -match "NEXUS" -and "$($r.response)" -match "42"
  Add-Test "F04" "Vision/OCR (Bildtext NEXUS 42)" $(if ($ok) { "PASS" } else { "FAIL" }) @{ response = "$($r.response)".Trim() }
} catch { Add-Test "F04" "Vision/OCR" "FAIL" @{ error = "$_" } }
try {
  $r = Post "/api/embed" @{ model = "nomic-embed-text"; input = @("Stahlbetonbalken Biegebemessung", "Brettsperrholz Decke") }
  Add-Test "F05" "Embeddings (nomic-embed-text)" $(if ($r.embeddings.Count -eq 2) { "PASS" } else { "FAIL" }) @{ dims = $r.embeddings[0].Count }
} catch { Add-Test "F05" "Embeddings" "FAIL" @{ error = "$_" } }

# ---------- S: Modellwechsel + Parallelbetrieb ----------
try {
  $sw = [Diagnostics.Stopwatch]::StartNew()
  Post "/api/embed" @{ model = "nomic-embed-text"; input = "test" } | Out-Null
  Post "/api/generate" @{ model = "nexus-q35-9b-16k"; prompt = "OK"; stream = $false; think = $false; options = @{ num_predict = 1 } } | Out-Null
  $sw.Stop()
  $loaded = @((Invoke-RestMethod "$Api/api/ps").models | ForEach-Object { "$($_.name) $([math]::Round(100*$_.size_vram/$_.size,0))%GPU" })
  Add-Test "S01" "Wechsel Embedding -> Chat-Modell" "INFO" @{ seconds = [math]::Round($sw.Elapsed.TotalSeconds, 1); loaded = ($loaded -join "; ") }
} catch { Add-Test "S01" "Modellwechsel" "FAIL" @{ error = "$_" } }

# ---------- Empfehlung ----------
$best = $rows | Where-Object { $_.gpu_pct -ge 100 -and $_.eval_tps -ge 15 -and $_.eval_tokens -ge 100 } | Sort-Object ctx -Descending | Select-Object -First 1
$REP.recommendation = [ordered]@{
  default_model = "nexus-q35-9b-16k"
  max_ctx_100pct_gpu = $(if ($best) { "$($best.model) ($($best.ctx))" } else { "keins" })
  note = "16K bleibt Standard (schnell, Reserve fuer Embedding). Groesster 100%-GPU-Kontext nur fuer lange Dokumente."
}
$REP.models = @((Invoke-RestMethod "$Api/api/tags").models | ForEach-Object { [ordered]@{ name = $_.name; size_gb = [math]::Round($_.size / 1e9, 2) } })

# ---------- Ausgabe ----------
$mdPath = "$out\hwbench_$ts.md"
$REP.state = "DONE"; Save
$md = @("# NEXUS Hardware-/Modell-Abnahme $ts", "", "| Variante | ctx | eval tok/s | prompt tok/s | GB | GPU % | VRAM MiB | CPU avg/max % | Laden s |", "|---|---|---|---|---|---|---|---|---|")
foreach ($x in $rows) { $md += "| $($x.model) | $($x.ctx) | $($x.eval_tps) | $($x.prompt_tps) | $($x.size_gb) | $($x.gpu_pct) | $($x.vram_used_mib) | $($x.cpu_avg_pct)/$($x.cpu_max_pct) | $($x.load_s) |" }
$md += ""; $md += "| ID | Test | Status |"; $md += "|---|---|---|"
foreach ($t in $REP.tests) { $md += "| $($t.id) | $($t.name) | $($t.status) |" }
$md | Set-Content -Encoding UTF8 $mdPath
Write-Host ""; $md | ForEach-Object { Write-Host $_ }
Write-Host "`nJSON: $jsonPath`nBitte Inhalt der JSON-Datei an ID05 senden:  Get-Content '$jsonPath' | Set-Clipboard" -ForegroundColor Green
