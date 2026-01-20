# nlp/intent.py

INTENTS = {
    "greeting": ["hi", "hello", "hey", "good morning", "good evening"],
    "emergency": ["scam", "fraud", "money lost", "upi fraud", "account hacked"],
    "fir": ["fir", "complaint", "police", "report crime"],
    "law": ["section", "act", "punishment", "legal", "law"],
    "safety": ["safe", "protect", "avoid scam", "precautions"],
}

def detect_intent(text: str) -> str:
    text = text.lower()
    for intent, keywords in INTENTS.items():
        for k in keywords:
            if k in text:
                return intent
    return "general"
