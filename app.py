import streamlit as st
import random

st.title("IPL Smart Predictor 🔥")

teams = ["MI","CSK","RCB","KKR","SRH"]

team1 = st.selectbox("Team 1", teams)
team2 = st.selectbox("Team 2", teams)

st.subheader("Optional Match Inputs (can skip)")

score = st.number_input("Score", value=0)
overs = st.number_input("Overs", value=0)
wickets = st.number_input("Wickets", value=0)

fours = st.number_input("Fours", value=0)
sixes = st.number_input("Sixes", value=0)

last_runs = st.number_input("Last Over Runs", value=0)
last_boundaries = st.number_input("Last Over Boundaries", value=0)

# Base team strength (simple logic)
team_strength = {
    "MI": 85,
    "CSK": 88,
    "RCB": 82,
    "KKR": 84,
    "SRH": 80
}

if st.button("Predict 🔮"):

    # Base prediction using team strength
    strength1 = team_strength[team1] + random.randint(-5,5)
    strength2 = team_strength[team2] + random.randint(-5,5)

    # If match data available, adjust
    if overs > 0:
        run_rate = score / overs
        strength1 += run_rate * 2
        strength1 -= wickets * 3

    # Decide winner
    if strength1 > strength2:
        winner = team1
    else:
        winner = team2

    # Predict boundaries
    predicted_fours = random.randint(35, 70)
    predicted_sixes = random.randint(8, 25)

    # Results
    st.subheader("Prediction Result 🎯")

    st.success(f"🏆 Predicted Winner: {winner}")

    st.write(f"📊 Predicted Total Fours: {predicted_fours}")
    st.write(f"🚀 Predicted Total Sixes: {predicted_sixes}")

    # Basic signal
    if predicted_fours > 50:
        st.success("👉 HIGH boundary match (OVER likely)")
    else:
        st.warning("👉 Moderate/Low boundaries (UNDER possible)")
