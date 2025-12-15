from fuzzywuzzy import process
import json

with open("data/laws.json", "r", encoding="utf-8") as f:
    LAWS = json.load(f)

def fuzzy_search(query: str):
    choices = [law["summary"] for law in LAWS]
    best_match, score = process.extractOne(query, choices)

    if score < 60:
        return None, score

    for law in LAWS:
        if law["summary"] == best_match:
            return law, score

    return None, score
