# LiteLLM Gateway - Easy Start Script
# Paleidžia gateway su 5 modeliais viena komanda

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "🚀 LiteLLM Gateway Startup" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Load environment variables from .env file
Write-Host "⚙️  Loading environment variables from .env..." -ForegroundColor Yellow

if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -and -not $_.StartsWith("#")) {
            $parts = $_ -split "=", 2
            if ($parts.Count -eq 2) {
                [Environment]::SetEnvironmentVariable($parts[0].Trim(), $parts[1].Trim())
            }
        }
    }
    Write-Host "✅ Environment variables loaded from .env" -ForegroundColor Green
} else {
    Write-Host "❌ ERROR: .env file not found!" -ForegroundColor Red
    Write-Host "Please create .env file with your API keys (see .env.example)" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Patikrinti ar litellm_proxy yra įdiegtas
Write-Host "📦 Checking litellm installation..." -ForegroundColor Yellow
try {
    litellm_proxy --help > $null 2>&1
    Write-Host "✅ litellm_proxy found" -ForegroundColor Green
} catch {
    Write-Host "⚠️  litellm_proxy not found. Installing..." -ForegroundColor Yellow
    pip install litellm -q
    Write-Host "✅ Installed litellm" -ForegroundColor Green
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "📡 Starting Gateway..." -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Gateway URL:    http://127.0.0.1:4000" -ForegroundColor Cyan
Write-Host "Master Key:     sk-gateway-..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Available Models:" -ForegroundColor Cyan
Write-Host "  • deepseek-flash    ($0.014/1M tokens)" -ForegroundColor Green
Write-Host "  • deepseek-pro      ($0.27/1M tokens)" -ForegroundColor Yellow
Write-Host "  • claude-haiku-5-5  ($0.08/1M tokens)" -ForegroundColor Yellow
Write-Host "  • cheap-code        ($0.05/1M tokens)" -ForegroundColor Yellow
Write-Host "  • claude-sonnet-5   ($3.00/1M tokens)" -ForegroundColor Red
Write-Host ""
Write-Host "Usage:" -ForegroundColor Cyan
Write-Host "  python gateway_client.py      (test all models)" -ForegroundColor Magenta
Write-Host "  curl http://127.0.0.1:4000/health  (health check)" -ForegroundColor Magenta
Write-Host ""
Write-Host "Press Ctrl+C to stop the gateway" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Paleisti gateway
litellm_proxy --config config.yaml
