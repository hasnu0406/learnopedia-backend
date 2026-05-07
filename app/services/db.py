from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("✅ MongoDB connected successfully")
    db = client["learnopedia"]
except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    print(f"❌ MongoDB connection failed: {e}")
    client = None
    db = None

def get_collection():
    if db is None:
        raise Exception("Database not connected. Check MONGO_URL environment variable.")
    return db["users"]

def get_user_by_email(email: str):
    try:
        return get_collection().find_one({"email": email})
    except Exception as e:
        print(f"Error getting user: {e}")
        raise

def insert_user(user_data: dict):
    try:
        result = get_collection().insert_one(user_data)
        return str(result.inserted_id)
    except Exception as e:
        print(f"Error inserting user: {e}")
        raise