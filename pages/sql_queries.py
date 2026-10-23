import streamlit as st
import pandas as pd
from utils.db_connection import fetch_data

st.set_page_config(page_title="SQL Analytics", page_icon="📊", layout="wide")

st.title("📊 SQL Analytics & Practice")
st.markdown("Execute and analyze the 25 practice SQL queries against the local database.")

# Dictionary containing all 25 queries spanning Beginner, Intermediate, and Advanced levels
queries = {
    # --- Beginner Level ---
    "Q1: Find all players who represent India": """
        SELECT full_name, playing_role, batting_style, bowling_style 
        FROM players 
        WHERE country = 'India';
    """,
    "Q2: Show all matches played in the last 30 days": """
        SELECT match_description, team1, team2, venue_name, venue_city, match_date 
        FROM matches 
        WHERE match_date >= date('now', '-30 days') 
        ORDER BY match_date DESC;
    """,
    "Q3: Top 10 highest run scorers in ODI cricket": """
        SELECT p.full_name, SUM(s.runs_scored) as total_runs
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        JOIN matches m ON s.match_id = m.match_id
        WHERE m.match_type = 'ODI'
        GROUP BY p.player_id
        ORDER BY total_runs DESC LIMIT 10;
    """,
    "Q4: Venues with capacity > 50,000": """
        SELECT venue_name, venue_city, venue_country, venue_capacity 
        FROM matches 
        WHERE venue_capacity > 50000 
        ORDER BY venue_capacity DESC;
    """,
    "Q5: Match wins per team": """
        SELECT winning_team, COUNT(*) as total_wins 
        FROM matches 
        WHERE winning_team IS NOT NULL 
        GROUP BY winning_team 
        ORDER BY total_wins DESC;
    """,
    "Q6: Count players by playing role": """
        SELECT playing_role, COUNT(*) as player_count 
        FROM players 
        GROUP BY playing_role;
    """,
    "Q7: Highest individual score per format": """
        SELECT m.match_type, MAX(s.runs_scored) as highest_score
        FROM player_match_stats s
        JOIN matches m ON s.match_id = m.match_id
        GROUP BY m.match_type;
    """,
    "Q8: Series starting in 2024": """
        SELECT series_name, venue_country as host, match_type, series_start_year 
        FROM matches 
        WHERE series_start_year = 2024;
    """,

    # --- Intermediate Level ---
    "Q9: All-rounders >1000 runs and >50 wickets": """
        SELECT p.full_name, SUM(s.runs_scored) as total_runs, SUM(s.wickets_taken) as total_wickets
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        WHERE p.playing_role = 'All-rounder'
        GROUP BY p.player_id
        HAVING total_runs > 1000 AND total_wickets > 50;
    """,
    "Q10: Details of last 20 completed matches": """
        SELECT match_description, team1, team2, winning_team, victory_margin, victory_type, venue_name
        FROM matches
        WHERE winning_team IS NOT NULL
        ORDER BY match_date DESC LIMIT 20;
    """,
    "Q11: Player performance across formats": """
        SELECT p.full_name, m.match_type, SUM(s.runs_scored) as total_runs
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        JOIN matches m ON s.match_id = m.match_id
        GROUP BY p.player_id, m.match_type;
    """,
    "Q12: Home vs Away performance (Wins)": """
        SELECT winning_team, 
               SUM(CASE WHEN winning_team = venue_country THEN 1 ELSE 0 END) as home_wins,
               SUM(CASE WHEN winning_team != venue_country THEN 1 ELSE 0 END) as away_wins
        FROM matches
        WHERE winning_team IS NOT NULL
        GROUP BY winning_team;
    """,
    "Q13: Consecutive batting partnerships > 100": """
        SELECT s1.match_id, p1.full_name as batter1, p2.full_name as batter2, 
               (s1.runs_scored + s2.runs_scored) as combined_runs
        FROM player_match_stats s1
        JOIN player_match_stats s2 ON s1.match_id = s2.match_id AND s1.innings = s2.innings 
             AND s2.batting_position = s1.batting_position + 1
        JOIN players p1 ON s1.player_id = p1.player_id
        JOIN players p2 ON s2.player_id = p2.player_id
        WHERE combined_runs >= 100;
    """,
    "Q14: Bowling average economy by venue (Min 3 matches)": """
        SELECT p.full_name, m.venue_name, 
               CAST(SUM(s.runs_conceded) AS FLOAT) / SUM(s.overs_bowled) as avg_economy,
               COUNT(DISTINCT m.match_id) as matches_played
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        JOIN matches m ON s.match_id = m.match_id
        WHERE s.overs_bowled >= 4
        GROUP BY p.player_id, m.venue_name
        HAVING matches_played >= 3;
    """,
    "Q15: Players in close matches (<50 runs or <5 wkts)": """
        SELECT p.full_name, COUNT(m.match_id) as close_matches, AVG(s.runs_scored) as avg_runs
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        JOIN matches m ON s.match_id = m.match_id
        WHERE (m.victory_type = 'runs' AND m.victory_margin < 50) 
           OR (m.victory_type = 'wickets' AND m.victory_margin < 5)
        GROUP BY p.player_id;
    """,
    "Q16: Batting strike rate trend by year (Since 2020)": """
        SELECT p.full_name, strftime('%Y', m.match_date) as play_year, 
               AVG(s.runs_scored) as avg_runs,
               (SUM(s.runs_scored) * 100.0 / SUM(s.balls_faced)) as strike_rate
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        JOIN matches m ON s.match_id = m.match_id
        WHERE m.match_date >= '2020-01-01' AND s.balls_faced > 0
        GROUP BY p.player_id, play_year;
    """,

    # --- Advanced Level ---
    "Q17: Toss advantage analysis": """
        SELECT toss_decision, 
               COUNT(*) as total_matches,
               SUM(CASE WHEN toss_winner = winning_team THEN 1 ELSE 0 END) as matches_won,
               (SUM(CASE WHEN toss_winner = winning_team THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as win_percentage
        FROM matches
        WHERE winning_team IS NOT NULL
        GROUP BY toss_decision;
    """,
    "Q18: Most economical bowlers in limited overs (Min 10 matches)": """
        SELECT p.full_name, SUM(s.wickets_taken) as total_wickets,
               CAST(SUM(s.runs_conceded) AS FLOAT) / SUM(s.overs_bowled) as economy_rate
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        JOIN matches m ON s.match_id = m.match_id
        WHERE m.match_type IN ('ODI', 'T20') AND s.overs_bowled > 0
        GROUP BY p.player_id
        HAVING COUNT(m.match_id) >= 10 AND AVG(s.overs_bowled) >= 2
        ORDER BY economy_rate ASC;
    """,
    "Q19: Batsman consistency (Standard deviation)": """
        -- SQLite lacks native STDEV, utilizing variance calculation workaround for demonstration
        SELECT p.full_name, AVG(s.runs_scored) as avg_runs,
               AVG(s.runs_scored * s.runs_scored) - (AVG(s.runs_scored) * AVG(s.runs_scored)) as run_variance
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        JOIN matches m ON s.match_id = m.match_id
        WHERE m.match_date >= '2022-01-01' AND s.balls_faced >= 10
        GROUP BY p.player_id
        ORDER BY run_variance ASC;
    """,
    "Q20: Match counts and averages across formats (Min 20 matches)": """
        SELECT p.full_name, 
               COUNT(m.match_id) as total_matches,
               SUM(CASE WHEN m.match_type = 'Test' THEN 1 ELSE 0 END) as test_matches,
               SUM(CASE WHEN m.match_type = 'ODI' THEN 1 ELSE 0 END) as odi_matches,
               SUM(CASE WHEN m.match_type = 'T20' THEN 1 ELSE 0 END) as t20_matches
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        JOIN matches m ON s.match_id = m.match_id
        GROUP BY p.player_id
        HAVING total_matches >= 20;
    """,
    "Q21: Comprehensive Weighted Performance Ranking": """
        SELECT p.full_name,
               SUM(s.runs_scored) * 0.01 + SUM(s.catches) * 3 as total_points
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        GROUP BY p.player_id
        ORDER BY total_points DESC LIMIT 10;
    """,
    "Q22: Head-to-Head Prediction (Last 3 years)": """
        SELECT team1, team2, COUNT(*) as matches_played,
               SUM(CASE WHEN winning_team = team1 THEN 1 ELSE 0 END) as team1_wins,
               SUM(CASE WHEN winning_team = team2 THEN 1 ELSE 0 END) as team2_wins
        FROM matches
        WHERE match_date >= date('now', '-3 years')
        GROUP BY team1, team2
        HAVING matches_played >= 1; 
    """,
    "Q23: Player Form & Momentum (Last 10 matches)": """
        SELECT p.full_name, SUM(s.runs_scored) as recent_runs, AVG(s.runs_scored) as form_avg
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        GROUP BY p.player_id
        ORDER BY recent_runs DESC LIMIT 10;
    """,
    "Q24: Most successful batting partnerships": """
        SELECT p1.full_name as batter1, p2.full_name as batter2, 
               AVG(s1.runs_scored + s2.runs_scored) as avg_partnership
        FROM player_match_stats s1
        JOIN player_match_stats s2 ON s1.match_id = s2.match_id AND s1.innings = s2.innings
             AND s2.batting_position = s1.batting_position + 1
        JOIN players p1 ON s1.player_id = p1.player_id
        JOIN players p2 ON s2.player_id = p2.player_id
        GROUP BY batter1, batter2
        ORDER BY avg_partnership DESC LIMIT 10;
    """,
    "Q25: Career Phase Trajectory Analysis": """
        SELECT p.full_name, strftime('%Y', m.match_date) as play_year, 
               AVG(s.runs_scored) as avg_runs
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        JOIN matches m ON s.match_id = m.match_id
        GROUP BY p.player_id, play_year
        ORDER BY p.full_name, play_year;
    """
}

selected_query_name = st.selectbox("Select a Practice Query", list(queries.keys()))
sql_statement = queries[selected_query_name]

st.markdown("### 📝 SQL Query")
st.code(sql_statement, language="sql")

if st.button("▶️ Execute Query", type="primary"):
    with st.spinner("Executing query..."):
        df = fetch_data(sql_statement)
        if not df.empty:
            st.success(f"Query returned {len(df)} rows.")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No data returned or query execution failed. Check if tables contain necessary sample data.")