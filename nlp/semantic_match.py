from sentence_transformers import SentenceTransformer, util
import json

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("data/laws.json", "r", encoding="utf-8") as f:
    LAWS = json.load(f)

def semantic_search(query: str):
    query_emb = model.encode(query, convert_to_tensor=True)
    law_texts = [law["summary"] for law in LAWS]
    law_embs = model.encode(law_texts, convert_to_tensor=True)

    scores = util.cos_sim(query_emb, law_embs)[0]
    best_idx = scores.argmax().item()
    confidence = scores[best_idx].item()

    if confidence < 0.5:
        return None, confidence

    return LAWS[best_idx], confidence
