import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables for API credentials
load_dotenv()
API_KEY = os.getenv("CRICBUZZ_API_KEY")
API_HOST = os.getenv("CRICBUZZ_API_HOST", "cricbuzz-cricket.p.rapidapi.com")

st.set_page_config(page_title="Live Matches", page_icon="🏏")
st.title("🏏 Live Match Updates")
st.markdown("Real-time match data pulled directly from the Cricbuzz API.")

def fetch_live_matches():
    """Fetches live matches from the Cricbuzz REST API."""
    url = f"https://{API_HOST}/matches/v1/live"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Connection Error: {e}")
        return None

if st.button("🔄 Refresh Live Scores", type="primary"):
    if not API_KEY or API_KEY == "your_api_key_here":
        st.warning("⚠️ Please configure your CRICBUZZ_API_KEY in the .env file.")
    else:
        with st.spinner("Fetching live data..."):
            data = fetch_live_matches()
            
            if data and "typeMatches" in data:
                for match_type in data["typeMatches"]:
                    st.subheader(f"🏆 {match_type.get('matchType', 'Unknown Format')} Matches")
                    
                    for series in match_type.get("seriesMatches", []):
                        # FIX: Extract the wrapper dict, then loop over its "matches" list
                        wrapper = series.get("seriesAdWrapper", {})
                        
                        for match in wrapper.get("matches", []):
                            match_info = match.get("matchInfo", {})
                            match_score = match.get("matchScore", {})
                            
                            if match_info:
                                team1 = match_info.get('team1', {}).get('teamName', 'Team 1')
                                team2 = match_info.get('team2', {}).get('teamName', 'Team 2')
                                
                                with st.expander(f"{team1} vs {team2} - {match_info.get('status', 'Status Unknown')}"):
                                    st.write(f"**Series:** {match_info.get('seriesName', wrapper.get('seriesName', 'N/A'))}")
                                    venue = match_info.get('venueInfo', {})
                                    st.write(f"**Venue:** {venue.get('ground', 'N/A')}, {venue.get('city', 'N/A')}")
                                    
                                    if match_score:
                                        t1_score = match_score.get('team1Score', {}).get('inngs1', {})
                                        st.write(f"**{team1} Score:** {t1_score.get('runs', 0)}/{t1_score.get('wickets', 0)} ({t1_score.get('overs', 0)} ov)")
            else:
                st.info("No live matches are currently underway, or the API structure has changed.")