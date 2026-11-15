# start-workspace.ps1
# Pradeda LiteLLM Gateway ir Claude Code

Write-Host "🚀 Pradedamas LiteLLM Gateway workspace..." -ForegroundColor Cyan

# Nustatyti aplinkos kintamuosius
$env:ANTHROPIC_BASE_URL = "http://127.0.0.1:4000"

# Perkelti į projektą
Set-Location "C:\Users\osama\litellm-gateway"

# Pradėti gateway GUI
Write-Host "📱 Pradedamas Gateway GUI..." -ForegroundColor Yellow
Start-Process python -ArgumentList "gateway-gui.py"

# Laukti, kol proxy susikurs
Start-Sleep -Seconds 5

# Patikrinti, ar proxy veikia
$proxyCheck = $false
for ($i = 0; $i -lt 10; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:4000/health" -TimeoutSec 2 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            $proxyCheck = $true
            Write-Host "✅ Proxy veikia!" -ForegroundColor Green
            break
        }
    } catch {
        Write-Host "⏳ Laukiama proxy... ($($i+1)/10)" -ForegroundColor Gray
        Start-Sleep -Seconds 1
    }
}

if ($proxyCheck) {
    # Atidaryti Claude Code
    Write-Host "🤖 Pradedamas Claude Code su gateway..." -ForegroundColor Cyan
    & claude code .
} else {
    Write-Host "⚠️  Proxy nesuaktyvėjo. Patikrinkite gateway-gui.py" -ForegroundColor Red
}
