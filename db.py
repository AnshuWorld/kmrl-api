from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "kmrl")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def save_document(doc_data: dict):
    collection = db["documents"]
    result = collection.insert_one(doc_data)
    return str(result.inserted_id)

def get_documents(limit: int = 10):
    collection = db["documents"]
    return list(collection.find().sort("_id", -1).limit(limit))
def search_documents(query: str, category: str = None, limit: int = 10):
    collection = db["documents"]
    collection.create_index([("summary", "text"), ("full_text", "text")])
    
    filter_query = {"$text": {"$search": query}}
    if category:
        filter_query["category"] = category
    
    return list(collection.find(filter_query).limit(limit))

