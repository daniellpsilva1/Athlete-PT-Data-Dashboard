import pymongo
from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

def get_db():
    client = MongoClient(
        "MONGO_URI",
        tls=True,
        tlsAllowInvalidCertificates=True
    )
    return client.your_database_name