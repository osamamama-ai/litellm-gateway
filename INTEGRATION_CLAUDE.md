# 🔌 LiteLLM Gateway Integration su Claude Code

## Apžvalga

Šis projektas integruoja jūsų lokalų **LiteLLM Gateway** su **Claude Code**, kad galėtumėte:
- Naudoti pigiausius AI modelius (DeepSeek, Claude, GPT)
- Kurti savus agentus
- Testuoti AI integracijas lokaliai

---

## ✅ Setup (jau baigta)

### 1. Gateway veikia

```bash
# FastAPI:      http://localhost:8000
# Flask:        http://localhost:5000
# PostgreSQL:   localhost:5432
# Gateway:      http://localhost:4000
```

### 2. Python client paruoštas

```bash
litellm_client.py    # LiteLLMClient klasė
claude_agent_example.py  # Pavyzdžiai
```

---

## 🚀 Kaip naudoti

### Pavyzdys 1: Paprastas klausimas

```python
from litellm_client import LiteLLMClient

client = LiteLLMClient()

# Paprasta pagalba
answer = client.ask("Kas yra LiteLLM?")
print(answer)
```

### Pavyzdys 2: Chat completion

```python
response = client.chat_completion(
    messages=[
        {"role": "system", "content": "Tu esi helpful assistant"},
        {"role": "user", "content": "Paaiškink API"}
    ],
    model="gpt-3.5-turbo",
    temperature=0.7
)

print(response["choices"][0]["message"]["content"])
```

### Pavyzdys 3: Batch processing

```python
tasks = [
    "Sutrauk šį tekstą...",
    "Vertimui į anglų...",
    "Analitika..."
]

for task in tasks:
    answer = client.ask(task)
    print(answer)
```

---

## 🔧 Environment variables

Sukurkite `.env` failą:

```env
# Gateway
LITELLM_MASTER_KEY=sk-gateway-demo-key
LITELLM_GATEWAY_URL=http://127.0.0.1:4000/v1

# OpenRouter (kai bus API raktą)
OPENROUTER_API_KEY=sk-or-v1-your-key
```

---

## 📚 Modeliai

Gateway turi šiuos modelius:

```
✅ DeepSeek Flash    (pigiausias)
✅ DeepSeek Pro      (geriau)
✅ Claude Haiku      (greitas)
✅ Claude Sonnet     (intelligent)
✅ Kimi Code         (kodui)
```

**Pigiausias:** DeepSeek Flash  
**Rekomenduojamas:** Claude Haiku  
**Geriausias:** Claude Sonnet

---

## 🧪 Testavimai

### 1. Health check

```python
from litellm_client import LiteLLMClient

client = LiteLLMClient()
print(client.health_check())  # True/False
```

### 2. Greitas testas

```bash
python claude_agent_example.py
```

### 3. FastAPI Swagger UI

Atidaryk: http://localhost:8000/docs

---

## 📊 Kaina

**Claude Sonnet:** $15/mėn  
**DeepSeek Flash:** $0.55/mėn  
**Sutaupai:** ~94% su smart routing

---

## 🎯 Kito žingsniai

1. ✅ Paleisti Gateway
2. ✅ Setup Python client
3. ⏳ Gauti OpenRouter API raktą
4. ⏳ Integruoti su savo projektu

---

## ❓ Klausimai

**Q: Ar reikalingas internet?**  
A: Taip, kad paleisti OpenRouter API (reikia API rakto)

**Q: Ar gali naudoti offline?**  
A: Galite testinti LocalAI modeliais (reikia setup)

**Q: Ar saugus?**  
A: Taip, veikia lokaliai, API raktas jūsų

---

## 💡 Tips

1. Naudokite `DeepSeek Flash` testing
2. Naudokite `Claude Haiku` production
3. Cache requests jei galite
4. Monitor usage `LITELLM_LOG_LEVEL=INFO`

---

**Sėkmės! 🚀**
