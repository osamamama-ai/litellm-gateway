# LiteLLM - PAPRASTA NAUDOJIMO INSTRUKCIJA

## GREITAI - 3 ŽINGSNIAI

### 1️⃣ Darbalaukyje rask ir dublikliuok šias nuorodas:

```
Pradžia → C:\Users\osama\litellm-gateway\paprasta-start.cmd
```

Dublikliuok į darbalaukį kaip nuorodą ir pervadink į:
- **"LiteLLM - Paprasta"**

### 2️⃣ Spustelk nuorodą darbalaukyje

Atsidars meniu, pasirink:
- **5** - Pradėti abi (proxy + Claude Code automatiškai)

### 3️⃣ Darbas!

Proxy bėga fone, Claude Code atidaras su `cheap-code` modeliu. 
Naudokis normalia.

---

## MENIU PARINKTYS

| Pasirinkimas | Ką daro |
|---|---|
| **1** | Proxy (127.0.0.1:4000) – reikalingas visada |
| **2** | Claude Code + cheap-code (Kimi) |
| **3** | Claude Code + haiku (pigiausias Claude) |
| **4** | Claude Code + deepseek-flash (pigiausias iš viso) |
| **5** | Abi automatiškai (proxy + Claude Code) |
| **0** | Išeiti |

---

## MODELIAI - KURI PASIRINKTI?

### Pigiausias – **deepseek-flash** (option 4)
- Geri rezultatai, labai piga
- Puikus dienos darbams

### Geriausias Claude – **haiku** (option 3)
- Pigiausias Claude modelis
- Geras subalansavimas

### Lankstausias – **cheap-code** (option 2)
- Geriausias kodui
- Gerai skaito ir rašo LT

### Galingiausias – **sonnet-5** arba **deepseek-pro**
```powershell
cd "C:\Users\osama\litellm-gateway"
.\claude-llm.cmd --model claude-sonnet-5
```

---

## DAŽNOS PROBLEMOS

**P: Proxy neleidžia?**
A: Jis jau bėga. Tikrini: `netstat -ano | findstr ":4000"`

**P: "Claude Code doesn't recognize cheap-code"?**
A: Normalus įspėjimas, modelis veikia. Pasirink `/model` Claude Code'e.

**P: Kaip sustabdyti proxy?**
A: Spustelk proxy lango X arba Ctrl+C.

**P: Nuo kur žinoti, ar veikia?**
A: Jei Claude Code grąžina atsakymą – veikia! ✅

---

## RACIONALUS DARBO SRAUTAS

1. Spustelk **"LiteLLM - Paprasta"**
2. Pasirink **5** (abi)
3. Darbinkis Claude Code
4. Kai baigsi, uždaryk abi programas

**Baigtai!**

---

*Padaryta paprastai, kaip reikalavai. Nesutikslinti prasai "Try again"?*
