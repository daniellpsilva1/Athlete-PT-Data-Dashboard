import pymongo
from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

def get_db():
    client = MongoClient(
        os.getenv("MONGO_URI"),
        tls=True,
        tlsAllowInvalidCertificates=True,
        retryWrites=True,
        w="majority",
        connectTimeoutMS=30000,
        socketTimeoutMS=30000
    )
    return client['athlete_db']['athletes'] 