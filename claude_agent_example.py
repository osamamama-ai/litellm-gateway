"""
Claude Agent example - naudoti LiteLLM Gateway
Šitas pavyzdys rodo kaip naudoti savo localų gateway su Claude kodu
"""

from litellm_client import LiteLLMClient

# Inicijalizuoti gateway client
gateway = LiteLLMClient(
    base_url="http://127.0.0.1:4000/v1",
    api_key="sk-gateway-demo-key"
)


def simple_agent():
    """Paprastas agent - klausti gateway"""
    print("🤖 Simple Agent - LiteLLM Gateway Integration")
    print("=" * 50)

    questions = [
        "Koks yra LiteLLM?",
        "Kaip naudoti LiteLLM Gateway?",
        "Koks yra skirtumas tarp Claude ir GPT?"
    ]

    for question in questions:
        print(f"\n❓ {question}")
        try:
            answer = gateway.ask(question, model="cheap-code")
            print(f"✅ Atsakymas: {answer[:200]}...")
        except Exception as e:
            print(f"❌ Klaida: {e}")


def chat_agent():
    """Chat agent - pokalbis"""
    print("\n\n💬 Chat Agent - Multi-turn conversation")
    print("=" * 50)

    messages = [
        {"role": "system", "content": "Tu esi helpful AI assistant. Tu kalbi lietuviškai."},
        {"role": "user", "content": "Paaiškink kas yra API gateway"},
        {"role": "assistant", "content": "API gateway yra..."},
        {"role": "user", "content": "O kaip jis naudojamas?"}
    ]

    try:
        response = gateway.chat_completion(
            messages=messages,
            model="claude-sonnet-5",
            temperature=0.7
        )

        print(f"Model: {response['model']}")
        print(f"Atsakymas: {response['choices'][0]['message']['content']}")
    except Exception as e:
        print(f"❌ Klaida: {e}")


def batch_processing():
    """Batch processing - daug užklausų"""
    print("\n\n📦 Batch Processing Agent")
    print("=" * 50)

    tasks = [
        "Sutrauk šį tekstą: LiteLLM Gateway yra proxy sistema...",
        "Vertimui į anglų: Sveiki, kaip laikaisi?",
        "Analitika: Ar 2025 bus geras metai technologijoms?",
    ]

    for i, task in enumerate(tasks, 1):
        print(f"\n[{i}/{len(tasks)}] {task[:50]}...")
        try:
            answer = gateway.ask(task, model="claude-sonnet-5")
            print(f"✅ {answer[:150]}...")
        except Exception as e:
            print(f"❌ {e}")


if __name__ == "__main__":
    # 1. Patikrinti connection
    print("🔌 Checking Gateway Connection...")
    if not gateway.health_check():
        print("⚠️  Gateway neatsakė, bet bandysim...")
    else:
        print("✅ Gateway veikia!")

    # 2. Run agents
    simple_agent()
    chat_agent()
    batch_processing()

    print("\n\n✅ Integration complete!")
    print("Naudokite LiteLLMClient iš savo Claude skriptų.")
