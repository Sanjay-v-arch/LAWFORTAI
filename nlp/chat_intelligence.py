from typing import Dict

SESSION_MEMORY: Dict[str, Dict] = {}

FOLLOW_UP_KEYWORDS = [
    "explain", "what to do", "what todo", "steps",
    "next", "help", "guide", "recovery",
    "helpline", "call", "number",
    "fir", "complaint", "police"
]

def get_session(user_id="guest"):
    if user_id not in SESSION_MEMORY:
        SESSION_MEMORY[user_id] = {
            "last_answer": None,
            "last_topic": None
        }
    return SESSION_MEMORY[user_id]

def handle_followup(text: str, session: dict):
    t = text.lower()

    if not session.get("last_answer"):
        return None

    if "explain" in t:
        return f"Here’s a simple explanation:\n\n{session['last_answer']}"

    if any(x in t for x in ["what to do", "what todo", "steps", "next", "help", "guide"]):
        return (
            "Here’s what you should do now:\n\n"
            "1️⃣ Call 1930 immediately\n"
            "2️⃣ Freeze your bank / UPI\n"
            "3️⃣ Change all passwords\n"
            "4️⃣ Scan your device\n"
            "5️⃣ File complaint on cybercrime.gov.in\n\n"
            "Say **helpline** or **FIR** if you want."
        )

    if "helpline" in t:
        return "📞 Cyber Crime Helpline (India): **1930**\n🌐 https://cybercrime.gov.in"

    if "fir" in t or "complaint" in t:
        return "You can file FIR here: https://cybercrime.gov.in\nWant me to draft it?"

    return None
