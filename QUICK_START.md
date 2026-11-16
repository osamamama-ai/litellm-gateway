# ⚡ Quick Start - LiteLLM Gateway (5 AI Models)

## 🚀 Paleidimas (Startup)

### **Lengviausias būdas - Double-click:**
```
start-gateway.bat    (Windows - just double-click!)
```

### **Arba PowerShell:**
```powershell
.\start-gateway.ps1
```

### **Arba terminalas:**
```bash
cd C:\Users\osama\litellm-gateway
litellm_proxy --config config.yaml
```

---

## ✅ Patikrinti ar veikia

**Kai gateway palaistas, atidarykite naują terminalą:**

### 1️⃣ **Health Check**
```bash
curl http://127.0.0.1:4000/health
# Expected: 200 OK
```

### 2️⃣ **Test All Models**
```bash
cd C:\Users\osama\litellm-gateway
python gateway_client.py
```

### 3️⃣ **Direct Query**
```bash
curl -H "Authorization: Bearer sk-gateway-e2482150f273512c51ab807b7ae57a5cfb0824e8e13e4e60" \
  http://127.0.0.1:4000/v1/chat/completions \
  -d '{"model":"deepseek-flash","messages":[{"role":"user","content":"Hello"}],"max_tokens":50}'
```

---

## 🎯 5 Modeliai

| Modelis | Kaina | Naudoti kai |
|---------|-------|-----------|
| 🟢 **deepseek-flash** | $0.014 | Paprasti klausimai, brainstorming |
| 🟡 **deepseek-pro** | $0.27 | Sudėtinga analizė |
| 🟡 **claude-haiku-5-5** | $0.08 | Greitai santraukai |
| 🟡 **cheap-code** | $0.05 | Kodas, programavimas |
| 🔴 **claude-sonnet-5** | $3.00 | Backup (jei kiti nepavyksta) |

---

## 💻 Naudoti Python Code

```python
from gateway_client import GatewayClient

# Inicijuoti klientą
client = GatewayClient()

# Paklausti modelio
response = client.chat_completion(
    model="deepseek-flash",
    messages=[
        {"role": "user", "content": "Kas yra machine learning?"}
    ]
)

print(response)
```

---

## 📊 Kaip sutaupyti 94% 💰

**Originalus setup (tik Claude Sonnet):**
- 1M tokens/mėn = $3,000

**Su smart routing (5 modeliai):**
- 80% užduočių → DeepSeek Flash = $112
- 15% užduočių → DeepSeek Pro = $40.5
- 5% užduočių → Claude Sonnet = $150
- **TOTAL = $302.50 = 90% sutaupyti!** 🎉

---

## 🔧 Environment Variables (jei reikia keisti)

```bash
# Jei naudoji kitą komputerį:
export ANTHROPIC_BASE_URL="http://127.0.0.1:4000/v1"
export LITELLM_MASTER_KEY="sk-gateway-e2482150f273512c51ab807b7ae57a5cfb0824e8e13e4e60"
export OPENROUTER_API_KEY="sk-or-v1-..."
```

---

## 📁 Failai

| Failas | Naudojimas |
|--------|-----------|
| `start-gateway.bat` | 🟢 Lengviausias - tiesiog double-click! |
| `start-gateway.ps1` | PowerShell startup |
| `gateway_client.py` | Python klientas (NAUDOTI ŠIT!) |
| `config.yaml` | Gateway konfiguracija |
| `INTEGRATION_TEST_RESULTS.md` | Pilni test rezultatai |

---

## 🆘 Jei nesiveda

```bash
# 1. Patikrinti ar Python yra:
python --version

# 2. Patikrinti ar litellm įdiegtas:
pip install litellm

# 3. Patikrinti ar OpenRouter API raktas aktyvus:
# (Jei klaida 401 - nurodyti naują rakta config.yaml)

# 4. Jei 404 - gateway nėra palaistas
# Paleiskite start-gateway.bat
```

---

## 🎓 Šiapusės užduotys

✅ Setup baigtas  
✅ 5 modeliai veikia  
✅ Python klientas paruoštas  
✅ Cost tracking įjungtas  

**Sekantis žingsnis:**
- Naudoti `gateway_client.py` savo projektų
- Commit'inti setup'ą
- Ruoštis Product Hunt leidimui

---

**Sėkmės!** 🚀
