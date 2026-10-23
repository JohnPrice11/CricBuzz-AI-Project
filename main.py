import streamlit as st
from utils.db_connection import initialize_database

# Configure the main page layout
st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize the database on startup
initialize_database()

st.title("🏏 Cricbuzz LiveStats Application")
st.sidebar.success("Select a page above to navigate.")

st.markdown("""
Welcome to the Cricbuzz LiveStats Dashboard! 

Please use the sidebar to navigate through the different modules of this application:
* **Home:** Project overview and instructions.
* **Live Matches:** Real-time data from the Cricbuzz API.
* **Top Stats:** Top batting and bowling performances.
* **SQL Queries:** Interactive analytics and practice questions.
* **CRUD Operations:** Manage player and match data.
""")