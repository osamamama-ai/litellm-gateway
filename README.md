# 🚀 LiteLLM Gateway

> **Unified AI Gateway with Cost Optimization & Desktop Control**

[![GitHub License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/osamamama-ai/litellm-gateway?style=social)](https://github.com/osamamama-ai/litellm-gateway)

---

## 🎯 What is LiteLLM Gateway?

A **lightweight, cost-optimized AI gateway** that routes your requests through multiple AI providers with:

- 💰 **91% Cost Savings** - Use cheaper models (DeepSeek, Kimi) instead of Claude
- 🖥️ **Desktop GUI** - Tkinter control panel for easy management
- 🔀 **Smart Routing** - Automatic failover chain
- 📊 **Real-time Billing** - Track your AI spending
- 🔌 **Claude Code Integration** - Use with Claude Code for development
- 🌐 **Local & Cloud** - Run locally or deploy to production

---

## 💡 The Problem

Organizations waste **90% of AI API spend** on suboptimal model selection:

- ❌ Every request goes to expensive Claude/GPT-4
- ❌ No visibility into costs
- ❌ No unified interface across providers

## ✅ The Solution

**LiteLLM Gateway** routes intelligently through a 5-tier model system:

| Tier | Model | Cost | Use Case |
|------|-------|------|----------|
| 1 | deepseek-flash | $0.014/1M | Simple tasks |
| 2 | cheap-code | $0.050/1M | Code generation |
| 3 | claude-haiku | $0.080/1M | Real Claude (fast) |
| 4 | claude-sonnet | $3.000/1M | Complex reasoning |
| 5 | deepseek-pro | $0.270/1M | Quality fallback |

---

## 💰 Cost Comparison

| | Direct Claude | With Gateway | Savings |
|---|---|---|---|
| **Cost/1M tokens** | $3.00 | $0.14 | **95%** ↓ |
| **Monthly coding** | ~$300 | ~$14 | **~$286** ↓ |

---

## 🚀 Quick Start

### 1. Prerequisites
```bash
python --version  # 3.7+
# OpenRouter API key: https://openrouter.ai/keys
```

### 2. Install
```bash
git clone https://github.com/osamamama-ai/litellm-gateway.git
cd litellm-gateway
pip install -r requirements.txt
```

### 3. Configure
```bash
# .env file
OPENROUTER_API_KEY=sk-or-v1-your-key-here
ANTHROPIC_BASE_URL=http://127.0.0.1:4000/v1
```

### 4. Run
```bash
# Start GUI + Proxy
python gateway-gui.py

# Or automated (Claude Code + Gateway)
.\start-workspace.ps1
```

---

## 🎮 Visual Tour

### Main Control Panel

![LiteLLM Gateway GUI](docs/images/gateway-gui-main.png)

**Live Gateway Manager Interface** — Shows proxy status, model selector, real-time cost tracking, and activity logs.

### ASCII Mockup Reference

```
╔════════════════════════════════════════════════╗
║  🚀 LiteLLM Gateway Manager                    ║
╠════════════════════════════════════════════════╣
║                                                ║
║  Proxy Status: ✅ Veikia (127.0.0.1:4000)     ║
║                                                ║
║  ┌─────────────────┬──────────────────┐       ║
║  │ ▶ Pradėti Proxy │ ⏹ Sustabdyti     │       ║
║  │                 │ Proxy            │       ║
║  └─────────────────┴──────────────────┘       ║
║                                                ║
║  Model: [deepseek-pro ▼]                      ║
║  Cost Today: $0.08                             ║
║  Requests: 45                                  ║
║                                                ║
║  [💻 Launch Claude Code + Gateway]            ║
║                                                ║
║  📋 Activity Logs:                             ║
║  ✅ 45 requests processed                      ║
║  💰 Total cost: $0.08                          ║
║                                                ║
╚════════════════════════════════════════════════╝
```

### Cost Savings in Real-Time
- 🔴 **Without Gateway**: $3.00 per 1M tokens
- 🟢 **With Gateway**: $0.14 per 1M tokens
- 💰 **Savings**: **95%** on every request!

---

## 🔌 Claude Code Integration

```powershell
# Set environment
$env:OPENROUTER_API_KEY = "sk-or-v1-your-key"
$env:ANTHROPIC_BASE_URL = "http://127.0.0.1:4000/v1"

# Launch Claude Code with gateway
claude code .
```

**Result**: All Claude Code operations now use **DeepSeek Pro** (91% cheaper)! 🎉

---

## 📸 Screenshots & Demo

See [Visual Guide](docs/VISUAL_GUIDE.md) for:
- ✅ Step-by-step screenshot instructions
- ✅ GIF creation tutorial
- ✅ ASCII mockups of each feature

### To Capture Your Own:
1. Run: `python gateway-gui.py`
2. Press: `Win + Shift + S` (Windows screenshot)
3. Save to: `docs/images/gateway-gui-main.png`

---

## 📚 Documentation

- **[Setup Guide](docs/SETUP.md)** - Installation & configuration
- **[Models Guide](docs/MODELS.md)** - Complete model comparison
- **[Usage Guide](docs/USAGE.md)** - Examples (Python, JS, cURL)
- **[Cloud Roadmap](docs/CLOUD_ROADMAP.md)** - v2.0 SaaS vision
- **[Visual Guide](docs/VISUAL_GUIDE.md)** - Screenshots & mockups
- **[Contributing](CONTRIBUTING.md)** - How to contribute
- **[Changelog](CHANGELOG.md)** - Version history

---

## 🛠️ Architecture

```
Your Application (Claude Code, Python, etc.)
         ↓
LiteLLM Gateway (127.0.0.1:4000)
  ├─ Smart routing
  ├─ Cost tracking
  └─ Failover chain
         ↓
OpenRouter API (Unified provider proxy)
         ↓
DeepSeek | Kimi | Claude | GPT-4 | Others
```

---

## 💬 FAQ

### Q: Is my API key safe?
**A**: Yes! Your OpenRouter key stays on your machine. The gateway is just a local proxy.

### Q: Can I use this in production?
**A**: Yes! v1.0 is stable. We recommend running on a private server with your own API key.

### Q: What if a model fails?
**A**: Automatic failover! If deepseek-pro times out, it tries claude-haiku, then deepseek-flash.

### Q: How much will I save?
**A**: Typical developer saves **$200-500/month** if using Claude directly.

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

Free for commercial and open-source use!

---

## 🌟 Show Your Support

If this project helped you save money:
- ⭐ **Star us on GitHub**
- 🐛 **Report bugs**
- 💡 **Share ideas**
- 🤝 **Contribute code**

---

**Built with ❤️ by the LiteLLM Gateway team**

*Last updated: November 2026*
