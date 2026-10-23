import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Must be the first Streamlit command
st.set_page_config(page_title="Top Player Stats", page_icon="🏆")

load_dotenv()
API_KEY = os.getenv("CRICBUZZ_API_KEY")
API_HOST = os.getenv("CRICBUZZ_API_HOST", "cricbuzz-cricket.p.rapidapi.com")

st.title("🏆 Top Player Statistics")
st.markdown("Explore historical top batting and bowling performances.")

stat_type = st.selectbox(
    "Select Statistic Category", 
    ["Most Runs", "Highest Score", "Most Wickets", "Best Bowling Figures"]
)

def get_mock_data(stat_category):
    """Provides fallback data if the API endpoint is unavailable or rate-limited."""
    if stat_category == "Most Runs":
        return [
            {"Rank": 1, "Player": "Sachin Tendulkar", "Matches": 463, "Runs": 18426, "Average": 44.83},
            {"Rank": 2, "Player": "Kumar Sangakkara", "Matches": 404, "Runs": 14234, "Average": 41.98},
            {"Rank": 3, "Player": "Virat Kohli", "Matches": 292, "Runs": 13848, "Average": 58.67}
        ]
    elif stat_category == "Highest Score":
        return [
            {"Rank": 1, "Player": "Brian Lara", "Format": "Test", "Highest Score": "400*", "Against": "England"},
            {"Rank": 2, "Player": "Matthew Hayden", "Format": "Test", "Highest Score": "380", "Against": "Zimbabwe"},
            {"Rank": 3, "Player": "Brian Lara", "Format": "Test", "Highest Score": "375", "Against": "England"}
        ]
    elif stat_category == "Most Wickets":
        return [
            {"Rank": 1, "Player": "Muttiah Muralitharan", "Matches": 350, "Wickets": 534, "Economy": 3.93},
            {"Rank": 2, "Player": "Wasim Akram", "Matches": 356, "Wickets": 502, "Economy": 3.89},
            {"Rank": 3, "Player": "Waqar Younis", "Matches": 262, "Wickets": 416, "Economy": 4.68}
        ]
    elif stat_category == "Best Bowling Figures":
        return [
            {"Rank": 1, "Player": "Jim Laker", "Format": "Test", "Figures": "10/53", "Against": "Australia"},
            {"Rank": 2, "Player": "Anil Kumble", "Format": "Test", "Figures": "10/74", "Against": "Pakistan"},
            {"Rank": 3, "Player": "Ajaz Patel", "Format": "Test", "Figures": "10/119", "Against": "India"}
        ]
    else:
        return [{"Status": "Data not available"}]

def fetch_top_stats(stat_category):
    """Fetches stats from the API, falling back to mock data on failure."""
    endpoint_map = {
        "Most Runs": "most-runs",
        "Highest Score": "highest-score",
        "Most Wickets": "most-wickets",
        "Best Bowling Figures": "best-bowling"
    }
    
    url = f"https://{API_HOST}/stats/v1/top/{endpoint_map.get(stat_category, 'most-runs')}"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # If API succeeds, return the JSON
            return response.json()
        else:
            # Fallback if rate limited or unauthorized
            return get_mock_data(stat_category)
    except Exception:
        return get_mock_data(stat_category)

with st.spinner(f"Loading {stat_type} data..."):
    stats_data = fetch_top_stats(stat_type)
    if stats_data:
        df = pd.DataFrame(stats_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("No data available.")