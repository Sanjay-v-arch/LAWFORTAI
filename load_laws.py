import json
from DataBase.mongo_models import collection

with open("data/laws.json", "r", encoding="utf-8") as f:
    laws = json.load(f)

collection.insert_many(laws)
print("✅ Laws loaded into MongoDB")
