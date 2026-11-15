import requests
import json

base_url = 'http://localhost:4000/v1'

try:
    print('🔍 Checking available models...\n')
    models_response = requests.get(f'{base_url}/models', timeout=10)
    print(f'✅ Models endpoint - Status: {models_response.status_code}')
    models_data = models_response.json()
    print('Available Models:')
    if 'data' in models_data:
        for model in models_data['data']:
            print(f"  - {model.get('id', 'unknown')}")
    else:
        print(json.dumps(models_data, indent=2))

    print('\n' + '='*60)
    print('🧪 Testing chat completion...\n')

    # Try with deepseek-flash (the default configured model)
    data = {
        'model': 'deepseek-flash',
        'messages': [{'role': 'user', 'content': 'Sveikas! Kas tu esi?'}],
        'max_tokens': 100
    }

    response = requests.post(f'{base_url}/chat/completions', json=data, timeout=15)
    print(f'✅ Chat endpoint - Status: {response.status_code}')
    print('\n📊 Response:')
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

except Exception as e:
    print(f'❌ Error: {e}')
