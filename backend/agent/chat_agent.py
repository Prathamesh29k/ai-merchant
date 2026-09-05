import json
import re

from config import settings


def _fallback_parse(message: str) -> dict[str, object]:
    normalized = message.lower()
    category = next((item for item in ("laptop", "phone", "accessory") if item in normalized), None)
    price_match = re.search(r"(?:under|below|less than)\s*[₹$]?\s*([\d,]+)", normalized)
    return {
        "category": category,
        "max_price": int(price_match.group(1).replace(",", "")) * 100 if price_match else None,
        "keywords": [word for word in re.findall(r"[a-z]+", normalized) if len(word) > 3][:5],
    }


def parse_query(message: str) -> dict[str, object]:
    """Parse shopping intent with Groq when configured, otherwise use a local fallback."""
    if not settings.groq_api_key:
        return _fallback_parse(message)
    from groq import Groq

    client = Groq(api_key=settings.groq_api_key)
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Return JSON only with category, max_price in paise, and keywords array."},
            {"role": "user", "content": message},
        ],
    )
    return json.loads(completion.choices[0].message.content)


def respond(message: str) -> dict[str, object]:
    intent = parse_query(message)
    return {
        "message": "I found the shopping intent. Choose a product below to prepare a test checkout.",
        "intent": intent,
    }
