from DataBase.mongo_models import query_collection
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

SEMANTIC_THRESHOLD = 0.40


def semantic_search(query: str):
    """
    Semantic search over legal documents stored in MongoDB
    """

    # Encode user query
    query_vec = model.encode(query).reshape(1, -1)

    # Fetch documents with embeddings
    docs = list(
        query_collection.find(
            {
                "embedding": {"$exists": True},
                "summary": {"$exists": True}
            },
            {
                "_id": 0,
                "act": 1,
                "section": 1,
                "summary": 1,
                "full_text": 1,
                "embedding": 1
            }
        )
    )

    if not docs:
        return None, 0.0, "semantic"

    best_score = 0.0
    best_law = None

    for law in docs:
        law_vec = np.array(law["embedding"]).reshape(1, -1)
        score = cosine_similarity(query_vec, law_vec)[0][0]

        if score > best_score:
            best_score = score
            best_law = law

    if best_score < SEMANTIC_THRESHOLD:
        return None, best_score, "semantic"

    return best_law, best_score, "semantic"
