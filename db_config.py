
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db():
    mongo_uri = os.getenv("MONGO_URI") 
    client = MongoClient(mongo_uri)
    db = client['inventoryESM']  
    return db
