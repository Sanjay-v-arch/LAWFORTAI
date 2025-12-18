from nlp.fuzzy_match import fuzzy_search
from nlp.semantic_match import semantic_search

def process_query(query: str):

    # 1️⃣ FUZZY SEARCH
    law, confidence, method = fuzzy_search(query)
    if law:
        return law, confidence, method

    # 2️⃣ SEMANTIC SEARCH
    law, confidence, method = semantic_search(query)
    if law:
        return law, confidence, method

    # 3️⃣ FALLBACK
    return None, 0.0, "fallback"
