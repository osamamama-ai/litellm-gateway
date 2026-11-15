# Models Guide - LiteLLM Gateway

## Available Models (5 Tiers)

### 🚀 Tier 1: Ultra-Fast & Cheap
**Model ID**: `deepseek-flash`  
**Provider**: DeepSeek  
**Cost**: ~$0.014 per 1M tokens  
**Speed**: ⚡⚡⚡⚡⚡ (fastest)  
**Quality**: ⭐⭐⭐

**Best for**:
- Quick tasks
- Real-time responses
- Code completions
- High-volume cheap processing

**Example**:
```python
model = "deepseek-flash"  # Ultra cheap, very fast
```

---

### 💰 Tier 2: Budget-Friendly
**Model ID**: `cheap-code`  
**Provider**: Kimi K2.7  
**Cost**: ~$0.05 per 1M tokens  
**Speed**: ⚡⚡⚡⚡  
**Quality**: ⭐⭐⭐⭐

**Best for**:
- Code generation
- Documentation
- General tasks
- Budget-conscious teams

**Example**:
```python
model = "cheap-code"  # Good balance of price and quality
```

---

### 💚 Tier 3: Best Value Claude
**Model ID**: `claude-haiku-5-5`  
**Provider**: Anthropic  
**Cost**: ~$0.08 per 1M tokens  
**Speed**: ⚡⚡⚡  
**Quality**: ⭐⭐⭐⭐⭐

**Best for**:
- Production workloads
- Reliable responses
- Text analysis
- Customer-facing tasks

**Example**:
```python
model = "claude-haiku-5-5"  # Best Claude value
```

---

### 🎯 Tier 4: Powerful Processing
**Model ID**: `claude-sonnet-5`  
**Provider**: Anthropic  
**Cost**: ~$3 per 1M tokens  
**Speed**: ⚡⚡  
**Quality**: ⭐⭐⭐⭐⭐⭐

**Best for**:
- Complex reasoning
- Long-form content
- Fine-tuned responses
- Enterprise applications

**Example**:
```python
model = "claude-sonnet-5"  # Top-tier Claude
```

---

### 💪 Tier 5: Most Powerful
**Model ID**: `deepseek-pro`  
**Provider**: DeepSeek  
**Cost**: ~$0.27 per 1M tokens  
**Speed**: ⚡⚡  
**Quality**: ⭐⭐⭐⭐⭐⭐⭐

**Best for**:
- Advanced reasoning
- Code review
- Architecture design
- Complex problem solving

**Example**:
```python
model = "deepseek-pro"  # Most powerful
```

---

## Quick Comparison Table

| Model | Provider | Cost | Speed | Quality | Best For |
|-------|----------|------|-------|---------|----------|
| deepseek-flash | DeepSeek | 💰 | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | Quick tasks |
| cheap-code | Kimi K2.7 | 💰💰 | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Code & docs |
| claude-haiku-5-5 | Anthropic | 💰💰💰 | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Production |
| claude-sonnet-5 | Anthropic | 💰💰💰💰 | ⚡⚡ | ⭐⭐⭐⭐⭐⭐ | Complex work |
| deepseek-pro | DeepSeek | 💰💰💰💰 | ⚡⚡ | ⭐⭐⭐⭐⭐⭐⭐ | Reasoning |

---

## How to Switch Models

### Using Desktop GUI
1. Click the model dropdown in the GUI
2. Select a different model
3. Settings are automatically saved

### Using CLI
Set the model before running Claude Code:
```bash
$env:ANTHROPIC_MODEL = "deepseek-pro"
claude  # Uses deepseek-pro
```

### Using API
```python
import requests

response = requests.post(
    "http://127.0.0.1:4000/chat/completions",
    headers={"Authorization": "Bearer sk-a0a8e883..."},
    json={
        "model": "claude-sonnet-5",  # Switch here
        "messages": [{"role": "user", "content": "Hello!"}]
    }
)
```

---

## Pricing Breakdown

### Example: 1 Million Tokens

| Model | Input Cost | Output Cost | Total |
|-------|-----------|------------|-------|
| deepseek-flash | $0.007 | $0.007 | **$0.014** |
| cheap-code | $0.025 | $0.025 | **$0.050** |
| claude-haiku-5-5 | $0.040 | $0.040 | **$0.080** |
| claude-sonnet-5 | $1.500 | $1.500 | **$3.000** |
| deepseek-pro | $0.135 | $0.135 | **$0.270** |

### Monthly Estimate (1M tokens/day)

| Model | 1M/day | 10M/day | 100M/day |
|-------|--------|---------|----------|
| deepseek-flash | $0.42 | $4.20 | $42 |
| cheap-code | $1.50 | $15 | $150 |
| claude-haiku-5-5 | $2.40 | $24 | $240 |
| claude-sonnet-5 | $90 | $900 | $9,000 |
| deepseek-pro | $8.10 | $81 | $810 |

---

## Recommended Strategy

### Development
Use `deepseek-flash` or `cheap-code` - fast iteration, low cost

### Testing
Use `claude-haiku-5-5` - reliable quality, still affordable

### Production
Use `claude-sonnet-5` or context-dependent selection

### Complex Tasks
Use `deepseek-pro` - best reasoning capability

---

## Failover Chain

The gateway automatically falls back if a model fails:

```yaml
cheap-code → deepseek-flash → claude-haiku-5-5
deepseek-pro → deepseek-flash → claude-haiku-5-5
claude-sonnet-5 → claude-haiku-5-5 → deepseek-flash
```

---

## API Key Costs

All models use your **OpenRouter API key**.

✅ **Good news**: You pay OpenRouter directly  
✅ **No markup** from this gateway  
✅ **Full transparency** on costs  

---

## Need Help?

- 📖 See [Usage Guide](USAGE.md) for code examples
- 🔧 See [Setup Guide](SETUP.md) for configuration
- 💬 Ask in [GitHub Discussions](../../discussions)

---

**Last Updated**: November 2026  
**Version**: 1.0
