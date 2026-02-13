import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('GOOGLE_API_KEY')
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"

try:
    resp = requests.get(url)
    if resp.status_code == 200:
        models = resp.json().get('models', [])
        print("Available Models:")
        for m in models:
            if 'generateContent' in m['supportedGenerationMethods']:
                print(f"- {m['name']}")
    else:
        print(f"Error: {resp.status_code} {resp.text}")
except Exception as e:
    print(f"Exception: {e}")
