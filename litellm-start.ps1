$d = $PSScriptRoot
Get-Content (Join-Path $d '.env') | ForEach-Object {
  if ($_ -match '^\s*([A-Za-z_][A-Za-z0-9_]*)=(.+)$') { [Environment]::SetEnvironmentVariable($Matches[1], $Matches[2].Trim(), 'Process') }
}
litellm --config (Join-Path $d 'config.yaml') --host 127.0.0.1 --port 4000
