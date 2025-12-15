from pymongo import MongoClient

# Replace <password> with your actual DB password
MONGO_URI = "mongodb+srv://sanjayofficial1302_db_user:y9WHTmkKdRkNytyk@lawfortai.jw3jj5k.mongodb.net/?appName=LAWFORTAI"
# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["LawFortAI"]
collection = db["queries"]

def save_query(user_query, answer, act, section):
    """Save conversation to MongoDB"""
    collection.insert_one({
        "query": user_query,
        "answer": answer,
        "act": act,
        "section": section
    })
