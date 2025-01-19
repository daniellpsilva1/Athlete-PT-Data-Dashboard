import pymongo
from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

def get_db():
    try:
        # Use environment variables for credentials
        MONGO_URI = os.getenv("MONGO_URI")  # Ensure this is set in your .env file
        DB_NAME = os.getenv("DB_NAME", "athlete_db")  # Default to 'athlete_db' if not set

        if not MONGO_URI:
            raise ValueError("MONGO_URI environment variable is not set!")

        client = MongoClient(
            MONGO_URI,
            tls=True,  # Enable TLS for secure connections
            tlsAllowInvalidCertificates=True,  # Only for development!
            retryWrites=True,
            w="majority",
            connectTimeoutMS=30000,
            socketTimeoutMS=30000
        )

        # Test the connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        return client[DB_NAME]

    except Exception as e:
        print(f"Failed to connect to MongoDB: {str(e)}")
        return None