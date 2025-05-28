import requests
import os

def chat_with_deepseek(prompt, context=""):
    api_key = os.getenv("DEEPSEEK_API_KEY")  # or hardcode if needed

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a Pokémon walkthrough writer."},
            {"role": "user", "content": f"{prompt}\n\n{context}"}
        ],
        "temperature": 0.3,
        "top_p": 0.9,
        "max_tokens": 1500
    }

    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json=payload
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
