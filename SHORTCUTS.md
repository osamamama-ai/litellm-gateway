# ⚡ LiteLLM Gateway Shortcuts

Trys greitieji būdai paleisti agentus:

---

## 1️⃣ **Windows BAT Shortcut** (Paprasčiausias)

**Failas:** `run-agents.bat`

**Naudojimas:**
- Dukart spragtelkite `run-agents.bat` failą
- Arba iš cmd: `run-agents.bat`

**Daro:** Paleidžia `claude_agent_example.py` (3 agentai)

---

## 2️⃣ **Quick Test** (Greitas testas)

**Failas:** `quick-test.py`

**Naudojimas iš PowerShell:**
```powershell
python quick-test.py
```

**Naudojimas iš Claude Code terminal:**
```bash
python quick-test.py
```

**Daro:** 4 greiti testai:
- ✅ Health check
- ✅ Simple question
- ✅ Cheap model
- ✅ Chat completion

---

## 3️⃣ **PowerShell Launcher** (Poweringas)

**Failas:** `claude-quick-launch.ps1`

**Greita:**
```powershell
.\claude-quick-launch.ps1
```

**Visus agentus:**
```powershell
.\claude-quick-launch.ps1 -FullAgents
```

---

## 🎯 Recommended naudojimas:

| Tikslas | Failas | Komanda |
|---------|--------|---------|
| Greitai patikrinti | `quick-test.py` | `python quick-test.py` |
| Paleisti agentus | `run-agents.bat` | Dukart spragtelkite |
| Automation | `claude-quick-launch.ps1` | `.\claude-quick-launch.ps1` |

---

## 🔧 Setup (Claude Code)

Jei norite `/run-agents` komandą Claude Code:

Pridėkite į `.claude/settings.json`:
```json
{
  "hooks": {
    "pre-command": [
      {
        "command": "if ($_.Contains('run-agents')) { & .\\claude-quick-launch.ps1 -Quick }"
      }
    ]
  }
}
```

---

## ✅ All set!

Dabar galite greitai paleisti agentus! 🚀

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
