import streamlit as st
import random

st.title("IPL Full Match Predictor 🔥")

teams = ["MI","CSK","RCB","KKR","SRH"]

team1 = st.selectbox("Team 1", teams)
team2 = st.selectbox("Team 2", teams)

st.subheader("Optional Live Inputs (can skip)")

score = st.number_input("Current Score", value=0)
overs = st.number_input("Overs", value=0)
wickets = st.number_input("Wickets", value=0)

# Team base strength (tuned realistic)
team_strength = {
    "MI": 170,
    "CSK": 175,
    "RCB": 180,
    "KKR": 172,
    "SRH": 168
}

# ✅ FIXED boundary prediction (realistic)
def predict_boundaries(score):
    fours = int(score / 10 + random.randint(-2, 3))   # ~15–22
    sixes = int(score / 18 + random.randint(-1, 2))   # ~6–12
    
    fours = max(10, min(fours, 25))
    sixes = max(3, min(sixes, 15))

    return fours, sixes


# 🔮 BUTTON TRIGGER
if st.button("Predict 🔮"):

    # Base scores
    base1 = team_strength[team1] + random.randint(-15, 15)
    base2 = team_strength[team2] + random.randint(-15, 15)

    # Adjust with live data (if given)
    if overs > 0:
        run_rate = score / overs
        base1 += run_rate * 5
        base1 -= wickets * 4

    # Final predicted scores
    score1 = int(base1)
    score2 = int(base2)

    # Boundary predictions
    fours1, sixes1 = predict_boundaries(score1)
    fours2, sixes2 = predict_boundaries(score2)

    # Winner
    if score1 > score2:
        winner = team1
    else:
        winner = team2

    # OUTPUT
    st.subheader("Match Prediction 🧠")

    st.write(f"🏏 {team1} Predicted Score: {score1}")
    st.write(f"📊 {team1} Fours: {fours1}")
    st.write(f"🚀 {team1} Sixes: {sixes1}")

    st.write("---")

    st.write(f"🏏 {team2} Predicted Score: {score2}")
    st.write(f"📊 {team2} Fours: {fours2}")
    st.write(f"🚀 {team2} Sixes: {sixes2}")

    st.subheader(f"🏆 Winner: {winner}")
