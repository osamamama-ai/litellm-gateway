import os
import json
import requests

BASE_URL = 'http://127.0.0.1:4000/v1'
ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')


def load_master_key():
    """Nuskaito LITELLM_MASTER_KEY iš .env (be išorinių priklausomybių)."""
    try:
        with open(ENV_FILE, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('LITELLM_MASTER_KEY='):
                    return line.split('=', 1)[1].strip()
    except OSError:
        pass
    return None


def main():
    key = load_master_key()
    headers = {}
    if key:
        headers['Authorization'] = f'Bearer {key}'
    else:
        print('⚠️  LITELLM_MASTER_KEY nerastas .env — bandau be autorizacijos.\n')

    try:
        print('🔍 Checking available models...\n')
        models_response = requests.get(f'{BASE_URL}/models', headers=headers, timeout=10)
        print(f'✅ Models endpoint - Status: {models_response.status_code}')
        models_data = models_response.json()
        print('Available Models:')
        if 'data' in models_data:
            for model in models_data['data']:
                print(f"  - {model.get('id', 'unknown')}")
        else:
            print(json.dumps(models_data, indent=2, ensure_ascii=False))

        print('\n' + '=' * 60)
        print('🧪 Testing chat completion...\n')

        data = {
            'model': 'deepseek-flash',
            'messages': [{'role': 'user', 'content': 'Sveikas! Kas tu esi?'}],
            'max_tokens': 100
        }

        response = requests.post(f'{BASE_URL}/chat/completions', json=data, headers=headers, timeout=15)
        print(f'✅ Chat endpoint - Status: {response.status_code}')
        print('\n📊 Response:')
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))

    except Exception as e:
        print(f'❌ Error: {e}')


if __name__ == '__main__':
    main()
