"""
LiteLLM Gateway Client - Integration su Claude Code
"""

import os
import requests
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

# Load .env file at module level
load_dotenv()

class LiteLLMClient:
    """Client darbui su local LiteLLM Gateway"""

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:4000/v1",
        api_key: str = None,
    ):
        self.base_url = base_url
        self.api_key = api_key or os.getenv("LITELLM_MASTER_KEY", "sk-gateway-demo-key")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Chat completion su gateway

        Args:
            messages: Chat messages [{role, content}]
            model: Model name (gpt-3.5-turbo, claude-3-haiku, etc)
            temperature: Temperature (0-1)
            max_tokens: Max tokens

        Returns:
            Response JSON
        """
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }

        if max_tokens:
            payload["max_tokens"] = max_tokens

        response = requests.post(
            f"{self.base_url}/chat/completions",
            json=payload,
            headers=self.headers,
            timeout=30
        )

        response.raise_for_status()
        return response.json()

    def ask(self, question: str, model: str = "gpt-3.5-turbo") -> str:
        """Paprasta pagalba - paprastas klausimas"""
        response = self.chat_completion(
            messages=[{"role": "user", "content": question}],
            model=model
        )
        return response["choices"][0]["message"]["content"]

    def health_check(self) -> bool:
        """Patikrinti ar gateway veikia"""
        try:
            response = requests.get(
                f"{self.base_url.replace('/v1', '')}/health",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False


# Pavyzdžiai
if __name__ == "__main__":
    # Inicijalizacija
    client = LiteLLMClient()

    # 1. Health check
    print("🔍 Checking Gateway...")
    if client.health_check():
        print("✅ Gateway veikia!")
    else:
        print("❌ Gateway neveikia")

    # 2. Simple question
    print("\n📝 Paprastas klausimas:")
    answer = client.ask("Kas tu?")
    print(f"Atsakymas: {answer}")

    # 3. Chat completion
    print("\n💬 Chat completion:")
    response = client.chat_completion(
        messages=[
            {"role": "system", "content": "Tu esi helpful assistant"},
            {"role": "user", "content": "Paaiškink LiteLLM"}
        ],
        model="gpt-3.5-turbo"
    )
    print(f"Modelis: {response['model']}")
    print(f"Atsakymas: {response['choices'][0]['message']['content']}")
