# nlp/response_builder.py

def build_response(answer: str, intent: str):
    followups = {
        "emergency": "Do you want recovery steps or emergency helpline numbers?",
        "fir": "Do you want help filing an FIR or knowing the correct section?",
        "law": "Do you want punishment details or related sections?",
        "safety": "Want practical safety tips or recent scam examples?",
        "general": "Can you tell me a bit more?"
    }

    return {
        "reply": answer,
        "follow_up": followups.get(intent)
    }
