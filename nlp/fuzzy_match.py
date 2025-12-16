from rapidfuzz import process, fuzz
import json

with open("data/laws.json", "r", encoding="utf-8") as f:
    LAWS = json.load(f)

def fuzzy_search(query: str):
    choices = [law["summary"] for law in LAWS]

    result = process.extractOne(
        query,
        choices,
        scorer=fuzz.token_set_ratio
    )

    if not result:
        return None, 0.0, "fuzzy_failed"

    best_match, score, index = result

    if score < 60:
        return None, score / 100, "fuzzy_failed"

    return LAWS[index], score / 100, "fuzzy"
