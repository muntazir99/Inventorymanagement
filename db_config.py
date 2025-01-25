from pymongo import MongoClient

def get_db():
    client = MongoClient('mongodb+srv://muntazir9934:JZSN7jdZLUaHRyx3@main.taa62.mongodb.net/?retryWrites=true&w=majority&appName=main')
    db = client['inventoryESM']
    return db