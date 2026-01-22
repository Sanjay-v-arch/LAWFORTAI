# test_system.py

import json
from chatbot import chatbot_response
from presets import PRESET_RESPONSES
import os

# ---------------- Test Queries ----------------
test_queries = [
    "Hi",                                  # Preset
    "Hello there",                          # Preset variant
    "company leaking personal data",        # Fuzzy/semantic law match
    "unauthorized data collection",         # Semantic law match
    "Tell me a joke",                       # LLM fallback
    "How's your day?",                      # LLM fallback
    ""                                      # Empty query edge case
]

# ---------------- Log File Check ----------------
LOG_FILE = "logs/log.json"
if not os.path.exists("logs"):
    os.makedirs("logs")

# Initialize log file if missing
if not os.path.isfile(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        json.dump([], f)

# ---------------- Run Tests ----------------
print("🔹 Starting System Tests 🔹\n")

for query in test_queries:
    print(f"Query: {query}")
    response = chatbot_response(query)
    print(f"Response: {response}\n")

    # ---------------- Save log ----------------
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    log_entry = {
        "query": query,
        "response": response
    }
    logs.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

print("✅ All test queries processed.")
print(f"📄 Logs saved to {LOG_FILE}")
