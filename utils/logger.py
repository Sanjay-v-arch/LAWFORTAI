import json
import os
from datetime import datetime

LOG_FILE = "logs/log.json"

def log_user_query(user_query, bot_response, method):
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_query": user_query,
        "bot_response": bot_response,
        "method": method
    }
    data.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)
