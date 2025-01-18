import streamlit as st
from pages import dashboard

# Set page config
st.set_page_config(
    page_title="Athlete Dashboard", 
    layout="wide",
    page_icon="🏃‍♀️"
)

# Directly show the dashboard
dashboard.show()