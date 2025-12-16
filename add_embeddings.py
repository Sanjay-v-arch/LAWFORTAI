from DataBase.mongo_models import collection
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

docs = collection.find({"embedding": {"$exists": False}})

count = 0
for doc in docs:
    text = (
        doc.get("title", "") + " " +
        doc.get("summary", "") + " " +
        " ".join(doc.get("keywords", []))
    )

    embedding = model.encode(text).tolist()

    collection.update_one(
        {"_id": doc["_id"]},
        {"$set": {"embedding": embedding}}
    )
    count += 1

print(f"🔥 Embeddings added to {count} laws")
