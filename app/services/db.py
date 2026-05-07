from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL)
db = client["learnopedia"]
users_collection = db["users"]

def get_user_by_email(email: str):
    return users_collection.find_one({"email": email})

def insert_user(user_data: dict):
    result = users_collection.insert_one(user_data)
    return str(result.inserted_id)