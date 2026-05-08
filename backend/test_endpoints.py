import requests
import json

BASE_URL = "http://localhost:8000/api"

print("--- 1. GET /api/health ---")
try:
    r = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {r.status_code}")
    print(r.json())
except Exception as e:
    print(f"Error: {e}")

print("\n--- 2. GET /api/models ---")
try:
    r = requests.get(f"{BASE_URL}/models")
    print(f"Status Code: {r.status_code}")
    models = r.json()
    print(f"Total models returned: {len(models)}")
    if models:
        print(f"First model example: {models[0]['name']} ({models[0]['provider']})")
except Exception as e:
    print(f"Error: {e}")

print("\n--- 3. GET /api/benchmarks ---")
try:
    r = requests.get(f"{BASE_URL}/benchmarks")
    print(f"Status Code: {r.status_code}")
    benches = r.json()
    print(f"Total benchmarks returned: {len(benches)}")
    if benches:
        print(f"First benchmark example: {benches[0]['name']} - {benches[0]['full_name']}")
except Exception as e:
    print(f"Error: {e}")

print("\n--- 4. GET /api/usecases ---")
try:
    r = requests.get(f"{BASE_URL}/usecases")
    print(f"Status Code: {r.status_code}")
    usecases = r.json()
    print(f"Total usecases returned: {len(usecases)}")
    if usecases:
        print(f"First usecase example: {usecases[0]['id']} ({usecases[0]['label']})")
except Exception as e:
    print(f"Error: {e}")

print("\n--- 5. POST /api/recommend ---")
try:
    payload = {"use_case_text": "I need a model for writing Python code", "top_n": 3}
    r = requests.post(f"{BASE_URL}/recommend", json=payload)
    print(f"Status Code: {r.status_code}")
    print("Full JSON Response:")
    print(json.dumps(r.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
