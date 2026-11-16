"""
Anthropic client wrapper for LiteLLM Gateway
Automatically adds master key authentication to all requests
"""

import os
from anthropic import Anthropic


class AnthropicGatewayClient(Anthropic):
    """
    Extended Anthropic client that works with LiteLLM Gateway.
    Automatically adds the master key authorization header.
    """

    def __init__(self, api_key=None, base_url=None, master_key=None, **kwargs):
        """
        Initialize the gateway client.

        Args:
            api_key: Anthropic API key (optional, can be from env)
            base_url: Gateway URL (default: http://127.0.0.1:4000/v1)
            master_key: LiteLLM master key (default: from LITELLM_MASTER_KEY env)
            **kwargs: Additional arguments to pass to Anthropic()
        """
        # Use gateway defaults
        if base_url is None:
            base_url = os.getenv("ANTHROPIC_BASE_URL", "http://127.0.0.1:4000/v1")

        if master_key is None:
            master_key = os.getenv("LITELLM_MASTER_KEY", "")

        self.master_key = master_key

        # Create httpx client with master key header
        default_headers = {}
        if self.master_key:
            default_headers["Authorization"] = f"Bearer {self.master_key}"

        # Initialize parent with gateway URL and custom headers
        super().__init__(
            api_key=api_key or os.getenv("ANTHROPIC_API_KEY", "sk-gateway-dummy"),
            base_url=base_url,
            default_headers=default_headers,
            **kwargs
        )


if __name__ == "__main__":
    # Test the wrapper
    print("Testing AnthropicGatewayClient...\n")

    client = AnthropicGatewayClient()

    print(f"Base URL: {client.base_url}")
    print(f"Master Key: {client.master_key[:20]}...\n")

    # Test with different models
    models_to_test = ["deepseek-flash", "deepseek-pro", "claude-haiku-5-5"]

    for model in models_to_test:
        print(f"Testing {model}...")
        try:
            response = client.messages.create(
                model=model,
                max_tokens=100,
                messages=[
                    {
                        "role": "user",
                        "content": "Say hello in one sentence."
                    }
                ]
            )
            print(f"  ✅ Success: {response.content[0].text[:80]}...\n")
        except Exception as e:
            print(f"  ❌ Failed: {str(e)}\n")
