# Contributing to LiteLLM Gateway

Welcome! We're excited that you want to contribute to the LiteLLM Gateway project. This document will guide you through the process.

## Ways to Contribute

### 🐛 Report Bugs
- Check if the bug is already reported in [Issues](../../issues)
- Describe the bug clearly with steps to reproduce
- Include your OS, Python version, and environment details
- Add error messages and logs

### 💡 Suggest Features
- Open an issue with the label "enhancement"
- Describe the feature and why it would be useful
- Include examples if applicable
- Discuss implementation approaches

### 📚 Improve Documentation
- Fix typos or unclear explanations
- Add examples to existing docs
- Create new guides for common use cases
- Translate documentation

### 💻 Submit Code
- Fix bugs
- Add new features
- Optimize performance
- Improve code quality

## Getting Started

### 1. Fork the Repository
```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/litellm-gateway.git
cd litellm-gateway
```

### 2. Create a Branch
```bash
# Use descriptive branch names
git checkout -b feature/model-picker
git checkout -b fix/proxy-timeout
git checkout -b docs/setup-guide
```

### 3. Set Up Development Environment
```bash
# Create virtual environment
python -m venv venv

# Activate
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Make Your Changes
- Write clean, readable code
- Follow Python PEP 8 style guide
- Add comments for complex logic
- Test your changes thoroughly

### 5. Commit and Push
```bash
git add .
git commit -m "feat: add model comparison API"
git push origin feature/model-picker
```

### 6. Open a Pull Request
- Describe what your PR does
- Link related issues (Closes #123)
- Include screenshots for UI changes
- Explain your implementation approach

## Code Style

### Python
```python
# Good
def get_model_price(model_name: str) -> float:
    """Get the price per 1M tokens for a model."""
    prices = {
        "deepseek-flash": 0.014,
        "cheap-code": 0.050,
    }
    return prices.get(model_name, 0.0)

# Bad
def getPrice(m):
    return 0.05  # unclear which model
```

### Naming Conventions
- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private: `_leading_underscore`

### Documentation
- Docstrings for all functions
- Type hints for parameters
- Comments for non-obvious logic

## Testing

### Manual Testing
Before submitting:
1. Test your feature locally
2. Test with different models
3. Test error cases
4. Test on both Windows and Linux if possible

### What to Test
```bash
# Test the GUI
python gateway-gui.py

# Test the proxy
python -m litellm --config config.yaml --port 4000

# Test API calls
curl -X POST http://127.0.0.1:4000/chat/completions ...
```

## PR Guidelines

### Before Opening
- [ ] Tested locally
- [ ] No breaking changes (or justified)
- [ ] Documentation updated
- [ ] Commit message is clear
- [ ] No large unrelated changes

### PR Title Format
```
type(scope): short description

feat(gui): add dark mode toggle
fix(proxy): handle timeout errors gracefully
docs(setup): clarify Windows installation
```

### Types
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Code style/formatting
- `refactor` - Code reorganization
- `perf` - Performance improvement
- `test` - Test additions

## Commit Message Format

```
type(scope): subject line

Longer explanation of what and why, wrapped at 72 chars.
Can include multiple paragraphs.

Fixes #123
Relates to #456
```

Example:
```
feat(proxy): add request timeout configuration

Allow users to configure proxy request timeout via environment
variable PROXY_TIMEOUT_SECONDS. Defaults to 30 seconds.

Fixes #89
```

## Project Structure

```
litellm-gateway/
├── gateway-gui.py           # Desktop GUI
├── start-proxy.ps1          # Proxy launcher
├── config.yaml              # Proxy configuration
├── docs/                    # Documentation
├── .github/
│   └── workflows/           # CI/CD workflows
└── tests/                   # Test files (future)
```

## Areas for Contribution

### High Priority
- [ ] Linux/Mac GUI support
- [ ] Web dashboard alternative
- [ ] More model providers
- [ ] Comprehensive tests
- [ ] Docker support

### Medium Priority
- [ ] Performance optimization
- [ ] Better error messages
- [ ] Usage analytics
- [ ] Cost calculator
- [ ] Batch API support

### Nice to Have
- [ ] Alternative themes
- [ ] Language translations
- [ ] API rate limiting
- [ ] Request logging
- [ ] Health check endpoint

## Questions?

- 💬 Ask in [GitHub Discussions](../../discussions)
- 📧 Email: support@example.com
- 💬 Open an issue with "question" label

## Recognition

Contributors will be:
- Added to the CONTRIBUTORS.md file
- Mentioned in release notes
- Thanked in the README

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🙌

**Last Updated**: November 2026
