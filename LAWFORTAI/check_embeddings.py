from DataBase.mongo_models import collection

total = collection.count_documents({})
with_embeddings = collection.count_documents({"embedding": {"$exists": True}})

print(f"Total laws: {total}")
print(f"Laws with embeddings: {with_embeddings}")
