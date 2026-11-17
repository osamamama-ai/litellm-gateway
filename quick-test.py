#!/usr/bin/env python3
"""
Quick Test - Greitas LiteLLM Gateway testas
Naudojimas: python quick-test.py
"""

from litellm_client import LiteLLMClient

def main():
    print("⚡ QUICK TEST - LiteLLM Gateway")
    print("=" * 60)

    client = LiteLLMClient()

    # Test 1: Health
    print("\n1️⃣ Health Check...")
    if client.health_check():
        print("   ✅ Gateway respond!")
    else:
        print("   ⚠️ Gateway offline or not responding")

    # Test 2: Simple question
    print("\n2️⃣ Simple Question (claude-sonnet-5)...")
    try:
        answer = client.ask(
            "Labas! Pavadink 3 AI modelius.",
            model="claude-sonnet-5"
        )
        print(f"   ✅ {answer[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")

    # Test 3: Cheap model
    print("\n3️⃣ Cheap Model Test (deepseek-flash)...")
    try:
        answer = client.ask(
            "Kas yra DeepSeek?",
            model="deepseek-flash"
        )
        print(f"   ✅ {answer[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")

    # Test 4: Chat
    print("\n4️⃣ Chat Completion (cheap-code)...")
    try:
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": "Tu esi helpful assistant."},
                {"role": "user", "content": "Pasakyk witty žokš."}
            ],
            model="cheap-code"
        )
        msg = response["choices"][0]["message"]["content"]
        print(f"   ✅ {msg[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")

    print("\n" + "=" * 60)
    print("✅ Quick test complete!")

if __name__ == "__main__":
    main()
