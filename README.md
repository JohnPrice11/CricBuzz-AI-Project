# 🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics

## 🎯 Problem Statement
A comprehensive cricket analytics dashboard that integrates live data from the Cricbuzz API with a SQL database to create an interactive web application. This platform delivers real-time match updates, detailed player statistics, SQL-driven analytics, and full CRUD operations for data management.

## 💼 Business Use Cases
1. **📺 Sports Media & Broadcasting:** Real-time match updates and player performance analysis for commentary teams.
2. **🎮 Fantasy Cricket Platforms:** Player form analysis, head-to-head statistics, and real-time score updates.
3. **📈 Cricket Analytics Firms:** Advanced statistical modeling and data-driven insights for team management.
4. **🎓 Educational Institutions:** Teaching database operations, SQL practice, and API integration with real-world datasets.
5. **🎲 Sports Betting & Prediction:** Historical performance analysis, player form tracking, and venue-specific insights.

## 🛠️ Technology Stack & Tags
* **Frontend/Web Development:** Python, Streamlit
* **Data Processing & Analytics:** Pandas
* **Database Management:** SQL (SQLite)
* **API Integration:** REST API (Cricbuzz via RapidAPI), Requests library
* **Technical Tags:** Python, Streamlit, SQL, Database, REST API, Database Connector, pandas, requests, Data Analytics, Web Development, Sports Technology

## 📌 Page-wise Features
1. **Home Page:** Describes the project, tools used, instructions, and navigation structure.
2. **Live Match Page:** Fetches ongoing matches from the Cricbuzz API, displaying real-time scorecards, match status, and venue details.
3. **Top Player Stats Page:** Displays top batting and bowling leaderboards (most runs, highest score, most wickets) fetched via the Cricbuzz API.
4. **SQL Queries & Analytics Page:** Integrates 25 advanced SQL practice queries (Beginner to Advanced) executed against a local database, rendering tabular outputs directly in Streamlit.
5. **CRUD Operations Page:** Full Create, Read, Update, and Delete operations on player and match statistics using a form-based UI.

## 📁 Project Structure
```text
cricbuzz_livestats/
├── main.py                     # Main Streamlit application entry point
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API credentials)
├── README.md                   # Project documentation
├── pages/                      # Streamlit dashboard modules
│   ├── 1_🏏_Live_Matches.py    # Real-time Cricbuzz API integration
│   ├── 2_🏆_Top_Player_Stats.py# API-fetched batting/bowling leaderboards
│   ├── 3_📊_SQL_Analytics.py   # 25 interactive SQL practice questions
│   └── 4_⚙️_CRUD_Operations.py # Database management interface
├── utils/                      # Backend logic
│   └── db_connection.py        # SQLite connection & sample data initialization
├── notebooks/                  # Jupyter notebooks for testing
│   └── data_fetching.ipynb     # API and DB connection testing sandbox
└── data/                       # Local database directory
    └── livestats.db            # Auto-generated SQLite database
```

## 🚀 Setup & Installation Instructions

**1. Clone the repository**
```bash
git clone https://github.com/JohnPrice11/cricbuzz_livestats.git
cd cricbuzz_livestats
```

**2. Create a virtual environment (Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure API Keys**
You need a Cricbuzz API key from RapidAPI to fetch live scores.
* Sign up at [RapidAPI](https://rapidapi.com/) and subscribe to a Cricbuzz Cricket API.
* Create a file named `.env` in the root directory.
* Add your credentials:
```env
CRICBUZZ_API_KEY=your_actual_api_key_here
CRICBUZZ_API_HOST=cricbuzz-cricket.p.rapidapi.com
```

**5. Run the Application**
```bash
streamlit run main.py
```
*Note: The SQLite database (`data/livestats.db`) and the comprehensive sample data required for the advanced SQL analytics module will automatically initialize upon the first run.*

---
**Developer:** Dhruv Singh Yadav | B.Tech Data Science and Engineering