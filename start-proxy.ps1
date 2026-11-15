# Load .env file
$envFile = Join-Path $PSScriptRoot '.env'
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^\s*([^=]+)=(.*)$') {
            $name = $Matches[1].Trim()
            $value = $Matches[2].Trim()
            if ($name -and $value) {
                [Environment]::SetEnvironmentVariable($name, $value, 'Process')
            }
        }
    }
}

# Start proxy
Write-Host "Proxy paleidžiamas su OPENROUTER_API_KEY..." -ForegroundColor Green
cd $PSScriptRoot
& litellm --config config.yaml --host 127.0.0.1 --port 4000
