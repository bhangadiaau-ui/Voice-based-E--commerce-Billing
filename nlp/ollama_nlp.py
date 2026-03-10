import json
import requests
from config import OLLAMA_URL, OLLAMA_MODEL
from logger import get_logger

log = get_logger("OllamaNLP")

SYSTEM_PROMPT = """
You are a billing NLP engine.
Extract structured items from user speech.

Rules:
- Output VALID JSON only
- Normalize item names
- Hindi and English words are allowed
- Convert Hindi product names to English
- Extract numeric quantities

Schema:
{
  "items": [
    {"name": "rice", "quantity": 2}
  ]
}
"""
# 🔤 Hindi → English product mapping
HINDI_TO_ENGLISH = {
    "केला": "banana",
    "केले": "banana",
    "सेब": "apple",
    "सेबों": "apple",
    "दूध": "milk",
    "चावल": "rice",
    "आटा": "atta",
    "गेहूं": "wheat",
    "चीनी": "sugar",
    "नमक": "salt",
    "तेल": "oil",
    "चॉकलेट": "chocolate",
    "बिस्कुट": "biscuit"
}

def extract_entities(text: str) -> dict:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": SYSTEM_PROMPT + "\nText: " + text,
        "stream": False
    }

    log.info("Sending text to Ollama")
    response = requests.post(OLLAMA_URL, json=payload, timeout=60)
    response.raise_for_status()

    raw = response.json()["response"]
    data = json.loads(raw)

    normalized_items = []

    for item in data.get("items", []):
        item_name = item.get("name", "").strip().lower()
        quantity = int(item.get("quantity", 1))

        # 🔥 Hindi → English normalization
        if item_name in HINDI_TO_ENGLISH:
            item_name = HINDI_TO_ENGLISH[item_name]

        # 🔁 plural normalization
        if item_name.endswith("s"):
            item_name = item_name[:-1]

        normalized_items.append({
            "name": item_name,
            "quantity": quantity
        })

    return {"items": normalized_items}