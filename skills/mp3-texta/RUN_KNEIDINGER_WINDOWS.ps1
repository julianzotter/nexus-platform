param([string]$Audio = "G:\Meine Ablage\AI-MP3-TEXTA\26_11_22_KNEIDINGER-WIGEBA.mp3", [string]$Out = "G:\Meine Ablage\AI-MP3-TEXTA\TRANSCRIPTS\KNEIDINGER-WIGEBA__SSOT_CANDIDATE")
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
if (!(Test-Path -LiteralPath $Audio)) { throw "BLOCKED_SOURCE: $Audio" }
foreach ($bin in @("ffprobe", "ffmpeg", "python")) { if (!(Get-Command $bin -ErrorAction SilentlyContinue)) { throw "BLOCKED_DEPENDENCY: $bin" } }
& python -c "from faster_whisper import WhisperModel; import yaml; print('ASR_DEPENDENCIES_OK')"
if ($LASTEXITCODE -ne 0) { throw "BLOCKED_DEPENDENCY: faster-whisper PyYAML. Install: pip install faster-whisper PyYAML" }
& python -c "from pathlib import Path; import hashlib; p=Path(r'$Audio'); h=hashlib.file_digest(p.open('rb'),'sha256').hexdigest(); print('SOURCE_SHA256',h); assert h=='b20818d7bdd83177a80749832963aad1220b9eec64c1f2759fb6275b1ea17434', 'SOURCE_HASH_MISMATCH'"
if ($LASTEXITCODE -ne 0) { throw "BLOCKED_SOURCE_HASH_MISMATCH" }
& python scripts/recursive_transcribe_v1.py $Audio --config scripts/config.yaml --output $Out
if ($LASTEXITCODE -ne 0) { throw "BLOCKED_ASR: see Python error; do not mark VALIDATED" }
Write-Host "SSOT_CANDIDATE: $Out"