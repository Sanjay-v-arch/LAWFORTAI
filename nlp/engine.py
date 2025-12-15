from DataBase.mongo_models import collection
from rapidfuzz import fuzz, process

FUZZY_THRESHOLD = 70
FUZZY_CANDIDATES = 30

# ----- FUZZY SEARCH FUNCTION -----
def fuzzy_search(query: str):
    """
    Fuzzy search with MongoDB pre-filter + confidence guard
    """

    # 1️⃣ MongoDB text pre-filter (FAST)
    docs = list(collection.find(
        {"$text": {"$search": query}},
        {"_id": 0, "title": 1, "summary": 1, "keywords": 1, "act": 1, "section": 1}
    ).limit(FUZZY_CANDIDATES))

    if not docs:
        return None, 0.0, "fuzzy_failed"

    # 2️⃣ Prepare searchable strings
    searchable = []
    for law in docs:
        combined = (
            " ".join(law.get("keywords", [])) + " " +
            law.get("title", "") + " " +
            law.get("summary", "")
        )
        searchable.append(combined)

    # 3️⃣ RapidFuzz match
    match, score, index = process.extractOne(
        query,
        searchable,
        scorer=fuzz.token_set_ratio
    )

    # 4️⃣ Confidence guard
    if score < FUZZY_THRESHOLD:
        return None, score / 100, "fuzzy_failed"

    return docs[index], score / 100, "fuzzy"


# ----- PROCESS QUERY FUNCTION -----
def process_query(query: str):
    """
    Pipeline:
    1. Fuzzy search
    2. Semantic search (next)
    3. LLM fallback (last)
    """

    # 1️⃣ FUZZY
    law, confidence, method = fuzzy_search(query)

    if law:
        return law, confidence, method

    # 2️⃣ SEMANTIC (next step)
    # law, confidence = semantic_search(query)

    # 3️⃣ LLM fallback (future)
    return None, 0.0, "fallback"
