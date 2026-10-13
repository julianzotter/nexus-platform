# NEXUS-AI Multi-LLM Orchestrator - Windows Setup (Keys nur als User-Env, nie im Repo)
python -m pip install -q pytest
foreach ($k in "PERPLEXITY_API_KEY","ANTHROPIC_API_KEY","OPENAI_API_KEY","GEMINI_API_KEY","GOOGLE_VISION_API_KEY") {
  if (-not [Environment]::GetEnvironmentVariable($k,"User")) {
    $v = Read-Host "$k (leer = ueberspringen)" -AsSecureString
    $p = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($v))
    if ($p) { [Environment]::SetEnvironmentVariable($k,$p,"User"); Set-Item "env:$k" $p }
  }
}
python -m pytest -q tests
python -m nexus_orch.cli status
