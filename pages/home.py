import streamlit as st

st.set_page_config(page_title="Home - Cricbuzz LiveStats", page_icon="🏠")

st.title("🏠 Project Overview: Cricbuzz LiveStats")

st.markdown("""
### 🎯 Problem Statement
Build a comprehensive cricket analytics dashboard that integrates live data from the Cricbuzz API with a SQL database to create an interactive web application.

### 💼 Business Use Cases
* **📺 Sports Media & Broadcasting:** Real-time match updates and player performance analysis.
* **🎮 Fantasy Cricket Platforms:** Player form analysis and recent performance tracking.
* **📈 Cricket Analytics Firms:** Advanced statistical modeling and data-driven insights.
* **🎓 Educational Institutions:** Teaching database operations and API integration.
* **🎲 Sports Betting & Prediction:** Historical performance analysis for odds calculation.

### 🛠️ Technology Stack
* **Frontend:** Python, Streamlit
* **Data Processing:** Pandas
* **Database:** SQL (SQLite)
* **API:** REST API (Cricbuzz via RapidAPI), Requests library

### 📁 Project Structure
The application is divided into four main modules accessible via the sidebar:
1. **Live Matches:** Fetches and displays ongoing match data.
2. **Top Stats:** Shows top batting and bowling statistics.
3. **SQL Queries:** An interface to run 25 advanced SQL analytics queries.
4. **CRUD Operations:** Create, Read, Update, and Delete records in the database.
""")