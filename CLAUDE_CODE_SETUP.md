# CLAUDE_CODE_SETUP.md
# LiteLLM Gateway + Claude Code Integration

## Kaip naudoti gateway'ą su Claude Code

### 1. Paleidimas

Iš PowerShell:
```powershell
cd C:\Users\osama\litellm-gateway
.\start-workspace.ps1
```

### 2. Claude Code Configuration

#### A. Automatinis būdas (rekomenduojama):
```powershell
# Nustatyti aplinkos kintamuosius per PowerShell
$env:ANTHROPIC_BASE_URL = "http://127.0.0.1:4000/v1"
$env:ANTHROPIC_API_KEY = "sk-gateway"

# Palaidžiant Claude Code
claude code .
```

#### B. Claude Code settings.json:
Redaguokite ~/.claude/settings.json:
```json
{
  "anthropic_base_url": "http://127.0.0.1:4000/v1",
  "anthropic_api_key": "dummy-for-gateway"
}
```

### 3. Patikrinti, ar veikia

Iš Claude Code terminalo:
```bash
# Patikrinti gateway statusą
curl http://127.0.0.1:4000/health

# Bandyti API žaliasiomis
curl -X POST http://127.0.0.1:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-pro",
    "messages": [{"role": "user", "content": "Sveikas pasauli!"}]
  }'
```

### 4. Modeliai (iš gateway'o):
- `deepseek-flash` - greitas, pigas
- `deepseek-pro` - jėkingas
- `claude-haiku-5-5` - vidutinis
- `claude-sonnet-5` - stiprus (brangus)

### 5. Klaidos sprendimas

Jei gateway nepradeda:
1. Patikrinti: `python gateway-gui.py` rankiniu būdu
2. Patikrinti OpenRouter API raktą .env faile
3. Peržiūrėti logs: `Get-Content gateway.log`

Jei Claude Code nesikonektuoja:
1. Patikrinti: `netstat -ano | findstr :4000`
2. Nustatyti: `$env:ANTHROPIC_BASE_URL = "http://127.0.0.1:4000/v1"`
3. Atidaryti naują Claude Code procesą
