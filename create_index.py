from DataBase.mongo_models import collection

collection.create_index([
    ("title", "text"),
    ("section", "text"),
    ("description", "text")
])

print("✅ Text index created")
