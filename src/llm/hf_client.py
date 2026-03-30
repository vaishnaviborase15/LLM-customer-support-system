import requests
import os

HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

def call_huggingface(prompt: str):
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 120,   # REDUCED (faster)
                    "temperature": 0.5       # more stable
                }
            },
            timeout=30   # reduced timeout
        )

        if response.status_code != 200:
            return fallback_response()

        data = response.json()

        if isinstance(data, dict) and "error" in data:
            return fallback_response()

        return data[0]["generated_text"]

    except:
        return fallback_response()


def fallback_response():
    return """Sentiment: Neutral
Priority: Medium
Response: Our support team will assist you shortly."""
