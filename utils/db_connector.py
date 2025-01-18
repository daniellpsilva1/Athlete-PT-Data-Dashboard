import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

def get_db():
    client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    return client['athlete_db']