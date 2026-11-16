"""
Routeris 5 DI modeliams per vietinį LiteLLM gateway (OpenAI-suderinamas API).

Modeliai (config.yaml):
  deepseek-flash    – pigiausias, greiti/paprasti darbai
  deepseek-pro      – analizė, ilgesni tekstai (pigesnė Sonnet alternatyva)
  claude-sonnet-5   – aukščiausia kokybė, sudėtingos užduotys
  claude-haiku-5-5  – pigus tikras Claude
  cheap-code        – Kimi K2.7 Code, programavimas

Naudojimas iš Python:
    from gateway_client import GatewayRouter
    r = GatewayRouter()
    print(r.ask("Kas yra LiteLLM?", task="quick").text)
    print(r.ask("Parašyk funkciją...", task="code").text)
    for res in r.ask_all("Pasisveikink vienu sakiniu."):
        print(res.model, res.ok, res.text)

Naudojimas iš komandinės eilutės:
    python gateway_client.py "Klausimas"                  # task=auto
    python gateway_client.py -t code "Parašyk regex..."
    python gateway_client.py -m claude-sonnet-5 "..."
    python gateway_client.py --all "Palygink atsakymus"
    python gateway_client.py --list | --check

Aplinkos kintamieji (arba .env šalia šio failo):
    GATEWAY_BASE_URL   (numatytas http://127.0.0.1:4000/v1)
    LITELLM_MASTER_KEY (arba GATEWAY_API_KEY)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_BASE_URL = "http://127.0.0.1:4000/v1"

MODELS: Dict[str, str] = {
    "deepseek-flash": "pigiausias, greiti/paprasti darbai",
    "deepseek-pro": "analizė, ilgesni tekstai",
    "claude-sonnet-5": "aukščiausia kokybė, sudėtingos užduotys",
    "claude-haiku-5-5": "pigus tikras Claude",
    "cheap-code": "programavimas (Kimi K2.7 Code)",
}

# Užduoties tipas -> modelių grandinė (pirmas – pagrindinis, kiti – atsarginiai).
ROUTES: Dict[str, List[str]] = {
    "quick": ["deepseek-flash", "claude-haiku-5-5"],
    "analysis": ["deepseek-pro", "deepseek-flash", "claude-haiku-5-5"],
    "quality": ["claude-sonnet-5", "deepseek-pro", "claude-haiku-5-5"],
    "claude": ["claude-haiku-5-5", "claude-sonnet-5"],
    "code": ["cheap-code", "deepseek-pro", "claude-haiku-5-5"],
}

# Lietuviški sinonimai
TASK_ALIASES: Dict[str, str] = {
    "greitas": "quick",
    "paprastas": "quick",
    "analize": "analysis",
    "analizė": "analysis",
    "kokybe": "quality",
    "kokybė": "quality",
    "sudetingas": "quality",
    "kodas": "code",
}

_CODE_HINTS = (
    "```", "def ", "class ", "function", "python", "javascript", "typescript",
    "sql", "regex", "kodas", "kodą", "funkcij", "skript", "bug", "klaida kode",
    "powershell", "bash", "html", "css", "json",
)
_QUALITY_HINTS = ("išsamiai", "detaliai", "kruopščiai", "strategij", "įvertink", "recenz")

# Klaidos, po kurių verta bandyti kitą modelį
_RETRYABLE_HTTP = {408, 409, 429, 500, 502, 503, 504}


class GatewayError(Exception):
    def __init__(self, message: str, status: Optional[int] = None):
        super().__init__(message)
        self.status = status


@dataclass
class RouteResult:
    model: str
    text: str = ""
    ok: bool = True
    error: str = ""
    seconds: float = 0.0
    usage: Dict[str, int] = field(default_factory=dict)
    tried: List[str] = field(default_factory=list)


def _load_dotenv(path: Path) -> Dict[str, str]:
    """Minimalus .env skaitytuvas (be priklausomybių). Reikšmės niekur nespausdinamos."""
    values: Dict[str, str] = {}
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip().removeprefix("export ").strip()
            values[key] = val.strip().strip('"').strip("'")
    except OSError:
        pass
    return values


def resolve_task(task: str, prompt: str) -> str:
    """Grąžina ROUTES raktą. 'auto' – paprasta euristika pagal užklausos turinį."""
    task = (task or "auto").strip().lower()
    task = TASK_ALIASES.get(task, task)
    if task != "auto":
        if task not in ROUTES:
            raise ValueError(f"Nežinomas užduoties tipas '{task}'. Galimi: auto, {', '.join(ROUTES)}")
        return task
    low = prompt.lower()
    if any(h in low for h in _CODE_HINTS):
        return "code"
    if any(h in low for h in _QUALITY_HINTS):
        return "quality"
    if len(prompt) > 1500:
        return "analysis"
    return "quick"


class GatewayRouter:
    """Routeris virš LiteLLM gateway su kliento pusės atsarginiais modeliais."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = 120.0,
    ):
        dotenv = _load_dotenv(Path(__file__).with_name(".env"))
        self.base_url = (
            base_url
            or os.getenv("GATEWAY_BASE_URL")
            or dotenv.get("GATEWAY_BASE_URL")
            or DEFAULT_BASE_URL
        ).rstrip("/")
        self._api_key = (
            api_key
            or os.getenv("GATEWAY_API_KEY")
            or os.getenv("LITELLM_MASTER_KEY")
            or dotenv.get("GATEWAY_API_KEY")
            or dotenv.get("LITELLM_MASTER_KEY")
            or "sk-gateway-dummy"
        )
        self.timeout = timeout

    def __repr__(self) -> str:  # raktas niekada nerodomas
        return f"GatewayRouter(base_url={self.base_url!r}, key={'set' if self._api_key else 'none'})"

    # ---- žemas lygis -------------------------------------------------------
    def _request(self, method: str, path: str, payload: Optional[dict] = None, timeout: Optional[float] = None) -> dict:
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        req = urllib.request.Request(
            f"{self.base_url}{path}",
            data=data,
            method=method,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._api_key}",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout or self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")[:500]
            raise GatewayError(f"HTTP {e.code}: {body}", status=e.code) from None
        except urllib.error.URLError as e:
            raise GatewayError(
                f"Gateway nepasiekiamas ({self.base_url}): {e.reason}. Ar paleistas start-proxy.ps1?"
            ) from None
        except TimeoutError:
            raise GatewayError(f"Baigėsi laikas ({timeout or self.timeout:.0f} s)", status=408) from None

    def chat_completion(
        self,
        model: str,
        messages: List[Dict[str, str]],
        max_tokens: int = 1024,
        temperature: float = 0.7,
    ) -> RouteResult:
        """Vienas kvietimas į konkretų modelį (be atsarginių)."""
        start = time.perf_counter()
        result = self._request(
            "POST",
            "/chat/completions",
            {"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": temperature},
        )
        choices = result.get("choices") or []
        if not choices:
            raise GatewayError(f"Netikėtas atsakymo formatas: {str(result)[:300]}")
        choice = choices[0]
        text = (choice.get("message") or {}).get("content") or choice.get("text") or ""
        return RouteResult(
            model=result.get("model") or model,
            text=text,
            seconds=time.perf_counter() - start,
            usage=result.get("usage") or {},
            tried=[model],
        )

    # ---- routeris ----------------------------------------------------------
    def ask(
        self,
        prompt: str,
        task: str = "auto",
        model: Optional[str] = None,
        system: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        fallback: bool = True,
    ) -> RouteResult:
        """
        Užklausa per routerį. Jei nurodytas `model` – naudojamas jis (atsarginiai
        imami iš jo užduoties grandinės); kitaip modelis parenkamas pagal `task`.
        """
        messages: List[Dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.extend(history or [])
        messages.append({"role": "user", "content": prompt})

        if model:
            chain = [model]
            if fallback:
                for route in ROUTES.values():
                    if route[0] == model:
                        chain += [m for m in route[1:] if m not in chain]
                        break
        else:
            chain = ROUTES[resolve_task(task, prompt)]
            if not fallback:
                chain = chain[:1]

        tried: List[str] = []
        errors: List[str] = []
        for m in chain:
            tried.append(m)
            try:
                res = self.chat_completion(m, messages, max_tokens=max_tokens, temperature=temperature)
                res.tried = tried
                return res
            except GatewayError as e:
                errors.append(f"{m}: {e}")
                # autentikacijos / užklausos klaidos – kitas modelis nepadės
                if e.status is not None and e.status not in _RETRYABLE_HTTP and e.status != 404:
                    break
                if e.status is None and "nepasiekiamas" in str(e):
                    break
        return RouteResult(model=tried[-1], ok=False, error=" | ".join(errors), tried=tried)

    def ask_all(self, prompt: str, models: Optional[List[str]] = None, **kwargs) -> List[RouteResult]:
        """Ta pati užklausa visiems (arba nurodytiems) modeliams lygiagrečiai – palyginimui."""
        models = models or list(MODELS)
        kwargs["fallback"] = False

        def one(m: str) -> RouteResult:
            return self.ask(prompt, model=m, **kwargs)

        with ThreadPoolExecutor(max_workers=len(models)) as pool:
            return list(pool.map(one, models))

    def list_models(self) -> List[str]:
        data = self._request("GET", "/models", timeout=10)
        return [m.get("id", "?") for m in data.get("data", [])]


# Suderinamumas su senu kodu
GatewayClient = GatewayRouter


def _print_result(res: RouteResult, show_meta: bool = True) -> None:
    if show_meta:
        tag = "OK" if res.ok else "KLAIDA"
        tokens = res.usage.get("total_tokens")
        extra = f", {tokens} tok." if tokens else ""
        via = f" (bandyta: {' -> '.join(res.tried)})" if len(res.tried) > 1 else ""
        print(f"[{tag}] {res.model} · {res.seconds:.1f} s{extra}{via}", file=sys.stderr)
    print(res.text if res.ok else res.error)


def main(argv: Optional[List[str]] = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except AttributeError:
            pass

    p = argparse.ArgumentParser(description="Routeris 5 DI modeliams per LiteLLM gateway")
    p.add_argument("prompt", nargs="*", help="Užklausa (jei nėra – skaitoma iš stdin)")
    p.add_argument("-t", "--task", default="auto",
                   help=f"auto | {' | '.join(ROUTES)} (arba LT: greitas, analize, kokybe, kodas)")
    p.add_argument("-m", "--model", choices=list(MODELS), help="Konkretus modelis")
    p.add_argument("-s", "--system", help="Sistemos instrukcija")
    p.add_argument("--all", action="store_true", help="Klausti visų 5 modelių ir palyginti")
    p.add_argument("--max-tokens", type=int, default=1024)
    p.add_argument("--temperature", type=float, default=0.7)
    p.add_argument("--timeout", type=float, default=120.0)
    p.add_argument("--no-fallback", action="store_true", help="Nebandyti atsarginių modelių")
    p.add_argument("--list", action="store_true", help="Parodyti modelius ir maršrutus")
    p.add_argument("--check", action="store_true", help="Patikrinti, ar gateway veikia")
    p.add_argument("-q", "--quiet", action="store_true", help="Spausdinti tik atsakymą")
    args = p.parse_args(argv)

    router = GatewayRouter(timeout=args.timeout)

    if args.list:
        print("Modeliai:")
        for name, desc in MODELS.items():
            print(f"  {name:<18} {desc}")
        print("\nMaršrutai (task -> grandinė):")
        for task, chain in ROUTES.items():
            print(f"  {task:<9} {' -> '.join(chain)}")
        return 0

    if args.check:
        try:
            available = router.list_models()
        except GatewayError as e:
            print(f"Gateway NEVEIKIA: {e}")
            return 1
        print(f"Gateway veikia: {router.base_url}")
        for name in MODELS:
            print(f"  {'✓' if name in available else '✗'} {name}")
        return 0 if all(n in available for n in MODELS) else 1

    prompt = " ".join(args.prompt).strip()
    if not prompt and not sys.stdin.isatty():
        prompt = sys.stdin.read().strip()
    if not prompt:
        p.error("nurodykite užklausą")

    common = dict(system=args.system, max_tokens=args.max_tokens, temperature=args.temperature)

    if args.all:
        results = router.ask_all(prompt, **common)
        for res in results:
            print("=" * 60)
            _print_result(res, show_meta=False)
            status = "OK" if res.ok else "KLAIDA"
            print(f"--- {res.model} · {status} · {res.seconds:.1f} s")
        return 0 if all(r.ok for r in results) else 1

    try:
        res = router.ask(prompt, task=args.task, model=args.model,
                         fallback=not args.no_fallback, **common)
    except ValueError as e:
        p.error(str(e))
    _print_result(res, show_meta=not args.quiet)
    return 0 if res.ok else 1


if __name__ == "__main__":
    sys.exit(main())
