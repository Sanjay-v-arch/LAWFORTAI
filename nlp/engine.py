from nlp.fuzzy_match import fuzzy_search
from nlp.semantic_match import semantic_search

def process_query(query: str):
    law, score = fuzzy_search(query)

    if law:
        return law, score / 100, "fuzzy"

    law, confidence = semantic_search(query)
    if law:
        return law, confidence, "semantic"

    return None, 0.0, "none"
