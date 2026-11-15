# LiteLLM šliuzas Claude Code'ui (lokalus)

Lokalus LiteLLM proxy `http://127.0.0.1:4000`, per kurį `claude-llm` siunčia Claude Code užklausas.
Įprastas `claude` šio šliuzo **nenaudoja** – jo nustatymai nekeičiami.

## Įdiegta

- LiteLLM `1.108.1`, įdiegta per uv įrankį su priedais `proxy` ir `extra-proxy`
  (pastarasis atsineša `prisma 0.15.0`; be jo užklausa be rakto grąžindavo 500 vietoj 401):

  ```
  uv tool install "litellm[proxy,extra-proxy]==1.108.1"
  ```

## Paleidimas

1. Proxy (laikyti atidarytą atskirame lange):
   ```
   C:\Users\osama\litellm-gateway\litellm-start.cmd
   ```
   Klauso tik `127.0.0.1:4000` (ne LAN). Patikra: `http://127.0.0.1:4000/health/liveliness` → 200.
2. Claude Code per šliuzą (kitame lange):
   ```
   C:\Users\osama\litellm-gateway\claude-llm.cmd --model claude-sonnet-5
   ```
   `claude-llm` nustato `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN` (master raktas iš `.env`) ir
   `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` ir `CLAUDE_CODE_MAX_OUTPUT_TOKENS=8192` **tik savo procesui**.
   (8192 riba reikalinga, nes `max_tokens` iš `config.yaml` neperrašo Claude Code prašomų 32 000 tokenų,
   o OpenRouter tiek kreditų neužtenka.)
   Taip pat nustatomi `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` ir `CLAUDE_CODE_MAX_CONTEXT_TOKENS=262144`:
   Kimi K2.7 Code kontekstas yra 262 144 tokenai, o nepažįstamam modeliui Claude Code numato 1M.
   Įspėjimas „the 200K limit isn't enforced for cheap-code“ yra tikėtinas ir nekenkia.
   Pastaba: be `--model` Claude Code prašo savo numatytojo modelio (pvz. `claude-opus-5-5`), kurio šliuze nėra → klaida 400.
   Modelį galima pasirinkti ir per `/model` (šliuzo modeliai žymimi „From gateway“).

## Modeliai (visi per OpenRouter)

| Vardas šliuze | Tikrasis modelis | Atsarginis (fallback) |
|---|---|---|
| `claude-sonnet-5` | `anthropic/claude-sonnet-5` | `claude-haiku-5-5`, tada `cheap-code` |
| `claude-haiku-5-5` | `anthropic/claude-haiku-5.5` (pigiausias Claude) | `cheap-code` |
| `cheap-code` | `moonshotai/kimi-k2.7-code` | – |
| `deepseek-flash` | `deepseek/deepseek-v4.1-flash` (pigiausias) | `claude-haiku-5-5` |
| `deepseek-pro` | `deepseek/deepseek-v4-pro` | `deepseek-flash` |

Darbalaukio nuorodos: „LiteLLM proxy“, „Claude LLM (haiku)“, „Claude LLM (deepseek)“ (`deepseek-flash`),
„Claude LLM (cheap-code)“. `deepseek-pro` paleisti: `claude-llm.cmd --model deepseek-pro`.
Kimi, DeepSeek ir kiti ne Claude modeliai – jautrių dokumentų jiems nesiųsti.
Pakeitus `config.yaml`, proxy reikia perkrauti.

## Raktai

Visi raktai – tik faile `.env` (šablonas – `.env.example`). Niekur kitur jų nekopijuoti.

| Kintamasis | Paskirtis |
|---|---|
| `LITELLM_MASTER_KEY` | Prieigos prie proxy raktas (jį naudoja `claude-llm`) |
| `OPENROUTER_API_KEY` | Visiems modeliams (OpenRouter) |
| `ANTHROPIC_API_KEY` | Šiuo metu nenaudojamas |

Svarbu: jei `OPENROUTER_API_KEY` (ar kitas) nustatytas Windows naudotojo aplinkos kintamuosiuose,
proxy jį paims ir iš ten, net jei `.env` tuščias.

## Naujo modelio pridėjimas

Į `config.yaml` → `model_list` pridėti įrašą, pvz.:

```yaml
  - model_name: mano-modelis            # vardas, kurį matys Claude Code
    litellm_params:
      model: openrouter/tiekejas/modelis  # LiteLLM tiekėjo/modelio ID
      api_key: os.environ/OPENROUTER_API_KEY
      # max_tokens: 8192                 # pasirinktinai: riboti atsakymo ilgį (taupo kreditus)
```

Jei reikia naujo rakto – įrašyti jį į `.env` ir nurodyti `os.environ/VARDAS`.
Atsarginis modelis (fallback) – `router_settings.fallbacks`. Po pakeitimų proxy perkrauti.
Prieš keičiant – pasidaryti kopiją: `copy config.yaml config.yaml.bak`.

## Sustabdymas

Proxy lange paspausti `Ctrl+C` (arba uždaryti langą). Jei paleista fone:

```
powershell -Command "Get-NetTCPConnection -LocalPort 4000 -State Listen | % { Stop-Process -Id $_.OwningProcess }"
```

## Pašalinimas

```
uv tool uninstall litellm
```

Po to ištrinti aplanką `C:\Users\osama\litellm-gateway` (kartu su `.env`, kuriame yra raktai).
Įprasto `claude` nustatymų keisti nereikia – jie nebuvo liesti.
