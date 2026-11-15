$d = $PSScriptRoot
$key = $null
Get-Content (Join-Path $d '.env') | ForEach-Object { if ($_ -match '^\s*LITELLM_MASTER_KEY=(.+)$') { $key = $Matches[1].Trim() } }
if (-not $key) { $key = 'sk-local-gateway' }
$env:ANTHROPIC_BASE_URL = 'http://127.0.0.1:4000'
$env:ANTHROPIC_AUTH_TOKEN = $key
$env:CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY = '1'
$env:CLAUDE_CODE_MAX_OUTPUT_TOKENS = '8192'
$env:CLAUDE_CODE_DISABLE_1M_CONTEXT = '1'
$env:CLAUDE_CODE_MAX_CONTEXT_TOKENS = '262144'
claude @args
