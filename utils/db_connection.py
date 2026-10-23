import sqlite3
import pandas as pd
from pathlib import Path
import random
from datetime import datetime, timedelta

# Resolve path relative to notebook or app location
DB_DIR = Path.cwd()
if DB_DIR.name == "notebooks":
    DB_DIR = DB_DIR.parent
DB_DIR = DB_DIR / "data"
DB_DIR.mkdir(exist_ok=True)

DB_PATH = DB_DIR / "livestats.db"

def get_connection():
    """Creates and returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

def initialize_database():
    """Creates tables and populates them with extensive synthetic data for analytics."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # --- TABLE CREATION ---
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        player_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        country TEXT NOT NULL,
        playing_role TEXT,
        batting_style TEXT,
        bowling_style TEXT
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS matches (
        match_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_description TEXT,
        team1 TEXT,
        team2 TEXT,
        venue_name TEXT,
        venue_city TEXT,
        venue_country TEXT,
        venue_capacity INTEGER,
        match_date DATE,
        match_type TEXT,
        series_name TEXT,
        series_start_year INTEGER,
        toss_winner TEXT,
        toss_decision TEXT,
        winning_team TEXT,
        victory_margin INTEGER,
        victory_type TEXT
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS player_match_stats (
        stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER,
        match_id INTEGER,
        runs_scored INTEGER DEFAULT 0,
        balls_faced INTEGER DEFAULT 0,
        fours INTEGER DEFAULT 0,
        sixes INTEGER DEFAULT 0,
        wickets_taken INTEGER DEFAULT 0,
        overs_bowled REAL DEFAULT 0.0,
        runs_conceded INTEGER DEFAULT 0,
        catches INTEGER DEFAULT 0,
        stumpings INTEGER DEFAULT 0,
        batting_position INTEGER,
        innings INTEGER,
        FOREIGN KEY (player_id) REFERENCES players(player_id),
        FOREIGN KEY (match_id) REFERENCES matches(match_id)
    )''')
    
    # --- SYNTHETIC DATA GENERATION ---
    cursor.execute("SELECT COUNT(*) FROM players")
    if cursor.fetchone()[0] == 0:
        
        # 1. Inject 10 Diverse Players
        sample_players = [
            ("Virat Kohli", "India", "Batsman", "Right Handed Bat", "Right-arm medium"),
            ("Rohit Sharma", "India", "Batsman", "Right Handed Bat", "Right-arm offbreak"),
            ("Jasprit Bumrah", "India", "Bowler", "Right Handed Bat", "Right-arm fast"),
            ("Ben Stokes", "England", "All-rounder", "Left Handed Bat", "Right-arm fast-medium"),
            ("Joe Root", "England", "Batsman", "Right Handed Bat", "Right-arm offbreak"),
            ("Jos Buttler", "England", "Wicket-keeper", "Right Handed Bat", "None"),
            ("Pat Cummins", "Australia", "Bowler", "Right Handed Bat", "Right-arm fast"),
            ("Steve Smith", "Australia", "Batsman", "Right Handed Bat", "Legbreak googly"),
            ("Mitchell Starc", "Australia", "Bowler", "Left Handed Bat", "Left-arm fast"),
            ("Hardik Pandya", "India", "All-rounder", "Right Handed Bat", "Right-arm fast-medium")
        ]
        cursor.executemany("INSERT INTO players (full_name, country, playing_role, batting_style, bowling_style) VALUES (?, ?, ?, ?, ?)", sample_players)

        # 2. Inject 50 Matches spanning 4 years (including the last 30 days)
        matches = []
        venues = [
            ("Narendra Modi Stadium", "Ahmedabad", "India", 132000),
            ("Wankhede Stadium", "Mumbai", "India", 33000),
            ("Lord's", "London", "England", 31000),
            ("MCG", "Melbourne", "Australia", 100024)
        ]
        teams = ["India", "England", "Australia"]
        formats = ["Test", "ODI", "T20"]
        
        today = datetime.today()
        base_date = today - timedelta(days=365*4)
        
        for i in range(1, 51):
            if i > 45:
                # Force last 5 matches into the "last 30 days" window
                m_date = today - timedelta(days=random.randint(1, 25))
            else:
                m_date = base_date + timedelta(days=i*25)
                
            t1, t2 = random.sample(teams, 2)
            venue = random.choice(venues)
            m_type = random.choice(formats)
            margin = random.choice([2, 4, 15, 60, 120]) # Ensures <5 and <50 criteria are met
            v_type = "wickets" if margin < 10 else "runs"
            
            matches.append((
                f"{t1} vs {t2} {m_type}", t1, t2, venue[0], venue[1], venue[2], venue[3],
                m_date.strftime("%Y-%m-%d"), m_type, f"International {m_type} Series", m_date.year,
                t1, random.choice(["Bat", "Bowl"]), random.choice([t1, t2]), margin, v_type
            ))
            
        cursor.executemany('''INSERT INTO matches (match_description, team1, team2, venue_name, venue_city, venue_country, venue_capacity, match_date, match_type, series_name, series_start_year, toss_winner, toss_decision, winning_team, victory_margin, victory_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', matches)

        # 3. Inject 300+ Player Match Stats (Ensuring 20+ matches per player and >100 run partnerships)
        stats = []
        for m_id in range(1, 51):
            # Batting Partnership: Kohli (1) and Rohit (2) batting consecutively at 1 and 2
            stats.append((1, m_id, random.randint(40, 130), random.randint(40, 100), 8, 2, 0, 0, 0, 1, 0, 1, 1))
            stats.append((2, m_id, random.randint(50, 140), random.randint(40, 90), 10, 4, 0, 0, 0, 0, 0, 2, 1))
            
            # All-Rounders: Stokes (4) and Pandya (10) getting >1000 aggregate runs & >50 wickets over 50 matches
            stats.append((4, m_id, random.randint(20, 80), random.randint(20, 70), 4, 1, random.randint(1, 4), 10.0, 45, 1, 0, 5, 1))
            stats.append((10, m_id, random.randint(20, 80), random.randint(20, 70), 4, 2, random.randint(1, 3), 8.0, 40, 0, 0, 6, 1))
            
            # Economical Bowlers: Bumrah (3) and Cummins (7)
            stats.append((3, m_id, random.randint(0, 10), random.randint(2, 15), 0, 0, random.randint(1, 5), 10.0, random.randint(30, 45), 0, 0, 10, 1))
            stats.append((7, m_id, random.randint(0, 15), random.randint(5, 20), 1, 0, random.randint(1, 4), 10.0, random.randint(35, 50), 1, 0, 9, 1))

        cursor.executemany('''INSERT INTO player_match_stats (player_id, match_id, runs_scored, balls_faced, fours, sixes, wickets_taken, overs_bowled, runs_conceded, catches, stumpings, batting_position, innings) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', stats)

    conn.commit()
    conn.close()

def execute_query(query, params=None):
    """Executes an INSERT/UPDATE/DELETE SQL query."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return True, "Success"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def fetch_data(query, params=None):
    """Executes a SELECT query and returns a pandas DataFrame for Streamlit rendering."""
    conn = get_connection()
    try:
        if params:
            df = pd.read_sql_query(query, conn, params=params)
        else:
            df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        print(f"Database Fetch Error: {e}")
        return pd.DataFrame()
    finally:
        conn.close()