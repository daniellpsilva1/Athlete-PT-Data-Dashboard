import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import streamlit as st

# Load .env file for local development
load_dotenv()

def get_db():
    try:
        # Check if running in Streamlit Cloud
        is_streamlit_cloud = os.getenv("STREAMLIT_CLOUD", "").lower() == "true"

        # Use Streamlit secrets in Cloud, .env locally
        MONGO_URI = (
            st.secrets.get("MONGO_URI") if is_streamlit_cloud
            else os.getenv("MONGO_URI")
        )
        DB_NAME = (
            st.secrets.get("DB_NAME", "athlete_db") if is_streamlit_cloud
            else os.getenv("DB_NAME", "athlete_db")
        )

        if not MONGO_URI:
            raise ValueError("MONGO_URI is not set in Streamlit secrets or .env file!")

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