# Changelog

All notable changes to LiteLLM Gateway are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-11-15

### ✨ Added
- **Desktop Control Panel** - Tkinter GUI for managing the proxy
  - Real-time proxy status indicator
  - Start/Stop proxy buttons
  - Model selector dropdown
  - Live activity logs
  - Settings persistence

- **Local API Gateway** - LiteLLM proxy on 127.0.0.1:4000
  - 5 AI models from OpenRouter (cheap-code, deepseek-flash, haiku, sonnet, deepseek-pro)
  - Automatic failover chain
  - Request routing and rate limiting
  - JSON API compatible with OpenAI format

- **Claude Code Integration** - Seamless model switching
  - ANTHROPIC_BASE_URL configuration
  - Environment variable based model selection
  - Gateway model discovery via CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY

- **Documentation** - Comprehensive guides
  - Setup guide with Windows/Linux/Mac instructions
  - Models guide with pricing and comparisons
  - Usage guide with Python, JavaScript, cURL examples
  - Contributing guidelines

- **Windows Automation** - PowerShell scripts
  - start-proxy.ps1 - Proxy launcher
  - claude-llm.ps1 - Claude Code launcher
  - paprasta-start.cmd - Interactive menu
  - gateway-gui.cmd - GUI launcher

- **Configuration Management**
  - .env file for sensitive credentials
  - config.yaml for proxy settings
  - gateway-config.json for GUI preferences

### 🔧 Technical Details
- **Dependencies**: LiteLLM 1.108.1, Python 3.7+
- **License**: MIT (Commercial and open-source)
- **Platforms**: Windows 10+, Linux, macOS (GUI support TBD)
- **Architecture**: Local proxy + Tkinter GUI + PowerShell automation

### 📊 Cost Analysis
- deepseek-flash: $0.014/1M tokens (5-10x cheaper than Claude)
- cheap-code: $0.050/1M tokens
- claude-haiku-5-5: $0.080/1M tokens
- claude-sonnet-5: $3.00/1M tokens
- deepseek-pro: $0.270/1M tokens

---

## [1.1.0] - Planned

### 🎯 Planned Features
- [ ] Linux/Mac native desktop app
- [ ] Web dashboard (alternative to GUI)
- [ ] More model providers (Anthropic Direct, Azure)
- [ ] Batch API support for bulk requests
- [ ] Usage analytics and cost tracking
- [ ] API rate limiting per user/key
- [ ] Request/response logging
- [ ] Health check endpoint
- [ ] Docker containerization
- [ ] Kubernetes support

### 🔐 Security Improvements
- [ ] Request validation
- [ ] SSL/TLS support
- [ ] API key rotation
- [ ] Audit logging
- [ ] Rate limiting per API key

### 📈 Performance
- [ ] Request caching
- [ ] Connection pooling
- [ ] Async request handling
- [ ] Performance benchmarking

---

## [2.0.0] - Cloud Version (Roadmap)

### ☁️ Cloud Hosting
- Hosted LiteLLM Gateway in the cloud
- Team management & collaboration
- Advanced analytics dashboard
- Usage tracking and billing
- 24/7 support
- SLA guarantees
- Auto-scaling infrastructure

### 💼 Enterprise Features
- Custom model integrations
- SSO/SAML authentication
- VPC/Private deployment options
- Compliance certifications (SOC2, HIPAA)
- API key management
- Role-based access control

### 💰 Monetization
- Freemium SaaS model
- Pay-as-you-go pricing
- Enterprise contracts
- Consulting services
- Training & implementation

---

## [Unreleased]

### 🔄 In Progress
- Web UI redesign
- Performance optimizations
- Extended model support
- Better error handling

### 🤔 Under Discussion
- Mobile app
- VS Code extension
- Alternative authentication methods
- Custom model support

---

## Version Comparison

| Feature | 1.0 | 1.1 | 2.0 |
|---------|-----|-----|-----|
| Desktop GUI | ✅ | ✅ | ❌ |
| Local Proxy | ✅ | ✅ | ❌ |
| Web Dashboard | ❌ | ✅ | ✅ |
| Cloud Hosting | ❌ | ❌ | ✅ |
| Analytics | ❌ | ✅ | ✅ |
| Team Mgmt | ❌ | ❌ | ✅ |
| Enterprise | ❌ | ❌ | ✅ |

---

## Migration Guide

### From 1.0 to 1.1
- No breaking changes expected
- New features are opt-in
- Existing configs will continue to work

### From 1.x to 2.0
- Cloud version is separate service
- Local gateway continues to work
- API remains compatible

---

## Breaking Changes

None yet! We follow semantic versioning and will announce breaking changes in advance.

---

## Contributors

See [CONTRIBUTORS.md](CONTRIBUTORS.md) for the full list.

---

## Installation

### Latest Release (1.0.0)
```bash
git clone https://github.com/osama/litellm-gateway.git
cd litellm-gateway
pip install -r requirements.txt
```

### Development Version
```bash
git clone https://github.com/osama/litellm-gateway.git
git checkout develop
pip install -r requirements.txt
```

---

## Release Schedule

- **1.0.x** - Bug fixes and minor improvements
- **1.1** - Q1 2027 (estimated)
- **2.0** - Q3 2027 (estimated)

---

## Security Policy

### Reporting Security Issues
⚠️ **Do not open public issues for security vulnerabilities.**

Email: security@example.com

We will:
1. Acknowledge receipt within 24 hours
2. Investigate thoroughly
3. Release a patch within 7 days
4. Credit the reporter (optional)

---

**Last Updated**: November 15, 2026  
**Current Version**: 1.0.0  
**Status**: Stable ✅
