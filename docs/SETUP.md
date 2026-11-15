# Setup Guide - LiteLLM Gateway v1.0

## Prerequisites

- **Python 3.7+** - [Download here](https://python.org)
- **OpenRouter API Key** - [Get free key](https://openrouter.ai)
- **Windows 10+** or Linux/Mac (partial support)
- **Internet connection** for API calls to OpenRouter

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/osama/litellm-gateway.git
cd litellm-gateway
```

### Step 2: Install LiteLLM
```bash
pip install litellm==1.108.1
```

### Step 3: Configure API Keys
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your keys:
# - OPENROUTER_API_KEY=sk-or-v1-your_key_here
# - LITELLM_MASTER_KEY=sk-a0a8e883e835a92b (generate a random string)
```

### Step 4: Choose Your Setup

#### **Option A: Desktop GUI (Recommended for Windows users)**
```bash
python gateway-gui.py
```
- One-click UI
- Real-time proxy status
- Model switcher
- Live activity logs

#### **Option B: Command Line (Linux/Mac friendly)**
```bash
# Start proxy only
python -m litellm --config config.yaml --port 4000

# Or use the PowerShell script (Windows)
powershell -ExecutionPolicy Bypass -File start-proxy.ps1
```

#### **Option C: With Claude Code**
```bash
paprasta-start.cmd
# Select option 5 to launch both proxy and Claude Code
```

## Verification

### Check Proxy is Running
```bash
# Windows
netstat -ano | findstr ":4000"

# Linux/Mac
lsof -i :4000
```

Should show: `LISTENING` on `127.0.0.1:4000`

### Test API Call
```bash
curl -X POST http://127.0.0.1:4000/chat/completions \
  -H "Authorization: Bearer sk-a0a8e883..." \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-flash",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Troubleshooting

### "Port 4000 already in use"
```bash
# Windows - find and kill process
netstat -ano | findstr ":4000"
taskkill /F /PID <PID>

# Linux/Mac
lsof -i :4000 | grep LISTEN
kill <PID>
```

### "OPENROUTER_API_KEY not found"
- Ensure `.env` file exists in the gateway directory
- Check key is correctly formatted: `sk-or-v1-...`
- Restart proxy after editing `.env`

### "Module not found: litellm"
```bash
pip install --upgrade litellm
```

### GUI won't open
```bash
# Try running directly
python gateway-gui.py

# Check Python version
python --version  # Should be 3.7+

# Verify tkinter is available
python -m tkinter  # Should show a test window
```

## Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `OPENROUTER_API_KEY` | ✅ Yes | - | API key for OpenRouter |
| `LITELLM_MASTER_KEY` | ✅ Yes | - | Security key for proxy |
| `ANTHROPIC_BASE_URL` | Optional | - | Proxy URL for Claude Code |
| `ANTHROPIC_AUTH_TOKEN` | Optional | - | Auth token for proxy |

## Next Steps

- Read [Models Guide](MODELS.md) to learn about available models
- Check [Usage Guide](USAGE.md) for integration examples
- See [README](../README.md) for feature overview

## Support

- 🐛 **Bug Reports** - [GitHub Issues](../../issues)
- 💬 **Discussions** - [GitHub Discussions](../../discussions)
- 📧 **Email** - support@example.com

---

**Version**: 1.0  
**Last Updated**: November 2026  
**Status**: Production Ready ✅
