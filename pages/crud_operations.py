import streamlit as st
import pandas as pd
from utils.db_connection import fetch_data, execute_query

st.set_page_config(page_title="CRUD Operations", page_icon="⚙️", layout="wide")

st.title("⚙️ Database Management (CRUD)")
st.markdown("Add, update, or remove player records from the database.")

tab1, tab2, tab3 = st.tabs(["➕ Add Player", "📝 Update Player", "❌ Delete Player"])

# --- TAB 1: CREATE ---
with tab1:
    st.subheader("Add a New Player")
    with st.form("add_player_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            country = st.text_input("Country")
            role = st.selectbox("Playing Role", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
        with col2:
            batting_style = st.text_input("Batting Style", placeholder="e.g. Right Handed Bat")
            bowling_style = st.text_input("Bowling Style", placeholder="e.g. Right-arm fast")
        
        submitted = st.form_submit_button("Add Player")
        
        if submitted:
            if name and country:
                query = """
                    INSERT INTO players (full_name, country, playing_role, batting_style, bowling_style)
                    VALUES (?, ?, ?, ?, ?)
                """
                success, msg = execute_query(query, (name, country, role, batting_style, bowling_style))
                if success:
                    st.success(f"Player {name} added successfully!")
                else:
                    st.error(f"Error adding player: {msg}")
            else:
                st.warning("Full Name and Country are required.")

# --- TAB 2: UPDATE ---
with tab2:
    st.subheader("Update Existing Player")
    # Fetch current players to populate dropdown
    players_df = fetch_data("SELECT player_id, full_name, country FROM players")
    
    if not players_df.empty:
        player_options = dict(zip(players_df['player_id'], players_df['full_name'] + " (" + players_df['country'] + ")"))
        selected_player_id = st.selectbox("Select Player to Update", options=player_options.keys(), format_func=lambda x: player_options[x])
        
        with st.form("update_player_form"):
            new_role = st.selectbox("Update Playing Role", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
            update_submitted = st.form_submit_button("Update Player Role")
            
            if update_submitted:
                query = "UPDATE players SET playing_role = ? WHERE player_id = ?"
                success, msg = execute_query(query, (new_role, selected_player_id))
                if success:
                    st.success("Player updated successfully!")
                else:
                    st.error(f"Error updating player: {msg}")
    else:
        st.info("No players available to update.")

# --- TAB 3: DELETE ---
with tab3:
    st.subheader("Delete Player Record")
    if not players_df.empty:
        del_player_id = st.selectbox("Select Player to Delete", options=player_options.keys(), format_func=lambda x: player_options[x], key="del_select")
        
        # Requires confirmation to prevent accidental deletion
        confirm_delete = st.checkbox("I confirm I want to delete this record.")
        
        if st.button("Delete Player", type="primary"):
            if confirm_delete:
                # First delete related stats to maintain foreign key integrity
                execute_query("DELETE FROM player_match_stats WHERE player_id = ?", (del_player_id,))
                
                # Then delete the player
                query = "DELETE FROM players WHERE player_id = ?"
                success, msg = execute_query(query, (del_player_id,))
                if success:
                    st.success("Player record deleted permanently. Refresh page to update lists.")
                else:
                    st.error(f"Error deleting player: {msg}")
            else:
                st.warning("Please check the confirmation box before deleting.")
    else:
        st.info("No players available to delete.")

st.divider()
st.subheader("Current Player Roster")
st.dataframe(fetch_data("SELECT * FROM players"), use_container_width=True, hide_index=True)