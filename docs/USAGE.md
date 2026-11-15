# Usage Guide - LiteLLM Gateway

## Desktop GUI Usage

### Starting the Gateway

**Windows - Double-click**:
```
LiteLLM Gateway (desktop shortcut)
```

**Or run**:
```bash
python gateway-gui.py
```

### GUI Features

1. **Status Indicator** (top)
   - ✅ Green = Proxy running
   - ⛔ Red = Proxy stopped
   - ⚠️ Orange = Checking...

2. **Control Buttons**
   - ▶ Start Proxy - launches the local proxy
   - ⏹ Stop Proxy - shuts down cleanly
   - 🎯 Launch Both - starts proxy + Claude Code

3. **Model Dropdown**
   - Select any of 5 AI models
   - Changes apply immediately
   - Selection persists on restart

4. **Activity Logs**
   - Real-time actions
   - Status updates
   - Error messages
   - Timestamps for each event

---

## Claude Code Integration

### Using with Claude Code

Start the gateway and Claude Code together:

```bash
python gateway-gui.py
# Click "🎯 Paleidžiami abi (Proxy + Claude Code)"
```

Or manually:

```bash
# Terminal 1: Start proxy
python -m litellm --config config.yaml --port 4000

# Terminal 2: Run Claude Code
claude --model deepseek-flash
```

### Claude Code Configuration

The gateway exposes itself as a local model:

```bash
# Use any model through the gateway
claude --model cheap-code

# Switch models mid-session
claude --model claude-sonnet-5
```

---

## API Usage (Python)

### Basic Chat Request

```python
import requests
import json

def chat(model, message):
    response = requests.post(
        "http://127.0.0.1:4000/chat/completions",
        headers={
            "Authorization": "Bearer sk-a0a8e883e835a92b",
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "messages": [
                {"role": "user", "content": message}
            ]
        }
    )
    
    result = response.json()
    return result["choices"][0]["message"]["content"]

# Use it
answer = chat("deepseek-flash", "What is 2+2?")
print(answer)
```

### Streaming Response

```python
import requests

def chat_stream(model, message):
    response = requests.post(
        "http://127.0.0.1:4000/chat/completions",
        headers={
            "Authorization": "Bearer sk-a0a8e883e835a92b",
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": message}],
            "stream": True
        },
        stream=True
    )
    
    for line in response.iter_lines():
        if line:
            data = line.decode().replace("data: ", "")
            try:
                chunk = json.loads(data)
                if "choices" in chunk:
                    delta = chunk["choices"][0].get("delta", {})
                    content = delta.get("content", "")
                    print(content, end="", flush=True)
            except json.JSONDecodeError:
                pass

# Use it
chat_stream("claude-haiku-5-5", "Write a haiku about code")
```

---

## API Usage (cURL)

### Simple Request

```bash
curl -X POST http://127.0.0.1:4000/chat/completions \
  -H "Authorization: Bearer sk-a0a8e883e835a92b" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-flash",
    "messages": [
      {
        "role": "user",
        "content": "What is the capital of France?"
      }
    ]
  }'
```

### Streaming Response

```bash
curl -X POST http://127.0.0.1:4000/chat/completions \
  -H "Authorization: Bearer sk-a0a8e883e835a92b" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-5",
    "messages": [{"role": "user", "content": "Write a poem"}],
    "stream": true
  }'
```

---

## API Usage (JavaScript)

### Node.js Example

```javascript
const axios = require('axios');

async function chat(model, message) {
  try {
    const response = await axios.post(
      'http://127.0.0.1:4000/chat/completions',
      {
        model: model,
        messages: [{ role: 'user', content: message }]
      },
      {
        headers: {
          'Authorization': 'Bearer sk-a0a8e883e835a92b',
          'Content-Type': 'application/json'
        }
      }
    );
    
    return response.data.choices[0].message.content;
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// Use it
chat('cheap-code', 'Hello!').then(console.log);
```

### Browser/Fetch Example

```javascript
async function chat(model, message) {
  const response = await fetch('http://127.0.0.1:4000/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer sk-a0a8e883e835a92b',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: model,
      messages: [{ role: 'user', content: message }]
    })
  });
  
  const data = await response.json();
  return data.choices[0].message.content;
}
```

---

## Cost Optimization Tips

### 1. Model Selection Strategy
```
Quick tasks → deepseek-flash ($0.014/1M tokens)
Standard work → cheap-code ($0.050/1M tokens)
Important tasks → claude-haiku-5-5 ($0.080/1M tokens)
Complex reasoning → deepseek-pro ($0.270/1M tokens)
```

### 2. Batch Processing
Process multiple requests together instead of one-by-one to reduce overhead.

### 3. Prompt Engineering
Well-written prompts = faster responses = lower costs

```python
# ❌ Avoid vague prompts (requires more tokens to clarify)
"Tell me about Python"

# ✅ Use specific prompts (faster, cheaper)
"List 5 ways to optimize Python code for speed"
```

### 4. Token Counting
Use cheaper models to estimate token usage before running expensive ones.

```python
# Check token count first (cheap)
cheap_response = chat("cheap-code", "Summarize...what I'm about to ask")
# Then use expensive model if needed
```

---

## Environment Variables

### For Direct API Usage

```bash
# Windows PowerShell
$env:PROXY_URL = "http://127.0.0.1:4000"
$env:PROXY_KEY = "sk-a0a8e883e835a92b"

# Linux/Mac bash
export PROXY_URL="http://127.0.0.1:4000"
export PROXY_KEY="sk-a0a8e883e835a92b"
```

### For Claude Code Integration

```bash
# Select specific model
$env:ANTHROPIC_MODEL = "deepseek-pro"
claude

# Or with the launcher
claude-llm.ps1  # Windows
./claude-llm.ps1  # Mac/Linux
```

---

## Common Patterns

### Pattern 1: Cheapest Fast Answer
```python
response = chat("deepseek-flash", question)
```

### Pattern 2: Reliable Claude
```python
response = chat("claude-haiku-5-5", question)
```

### Pattern 3: Best Results (Any Cost)
```python
response = chat("deepseek-pro", question)
```

### Pattern 4: Fallback Strategy
```python
try:
    response = chat("deepseek-pro", question)
except:
    response = chat("claude-haiku-5-5", question)
```

---

## Troubleshooting

### Connection Refused
```
Error: Connection refused (127.0.0.1:4000)
```

**Solution**: 
1. Click "▶ Start Proxy" in GUI
2. Wait 3 seconds for startup
3. Try again

### 401 Unauthorized
```
Error: 401 - Unauthorized
```

**Solution**:
- Check `OPENROUTER_API_KEY` in `.env`
- Verify key format: `sk-or-v1-...`
- Restart proxy

### Model Not Found
```
Error: Model "deepseek-flash" not found
```

**Solution**:
- Use exact model names from [Models Guide](MODELS.md)
- Check spelling
- Restart proxy

### Timeout
```
Error: Request timed out after 30s
```

**Solution**:
- Try a faster model (deepseek-flash)
- Reduce message length
- Check internet connection

---

## Next Steps

- 📚 Read [Models Guide](MODELS.md) for details on each model
- ⚙️ See [Setup Guide](SETUP.md) for configuration
- 💬 Ask in [GitHub Discussions](../../discussions)

---

**Version**: 1.0  
**Last Updated**: November 2026
