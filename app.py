import streamlit as st

st.title("IPL Trading Engine 🔥")

team1 = st.selectbox("Batting Team", ["MI","CSK","RCB","KKR","SRH"])
team2 = st.selectbox("Bowling Team", ["MI","CSK","RCB","KKR","SRH"])

score = st.number_input("Score")
overs = st.number_input("Overs Completed")
wickets = st.number_input("Wickets Lost")

fours = st.number_input("Total Fours")
sixes = st.number_input("Total Sixes")

last_runs = st.number_input("Runs in last over")
last_boundaries = st.number_input("Boundaries in last over")

# Phase detection
if overs <= 6:
    phase = "Powerplay ⚡"
elif overs <= 15:
    phase = "Middle Overs ⚖️"
else:
    phase = "Death Overs 🔥"

st.subheader(f"Match Phase: {phase}")

# Core calculations
if overs > 0:
    run_rate = score / overs
    boundary_rate = (fours + sixes) / overs
else:
    run_rate = 0
    boundary_rate = 0

# Win probability
win_prob = min(100, (run_rate * 10) - (wickets * 5))
win_prob = max(0, win_prob)

st.subheader(f"Win Probability: {win_prob:.2f}%")

# Momentum
if last_runs > 15:
    momentum = "HIGH"
elif last_runs > 8:
    momentum = "NORMAL"
else:
    momentum = "LOW"

st.write(f"Momentum: {momentum}")

# Smart decision engine
st.subheader("Trading Signal 🎯")

if phase == "Death Overs 🔥":
    if momentum == "HIGH" and boundary_rate > 2:
        st.success("🚀 STRONG OVER (Death overs explosion)")
    elif momentum == "LOW":
        st.error("🛑 UNDER (batting collapse risk)")
    else:
        st.warning("⚠️ WAIT")

elif phase == "Powerplay ⚡":
    if boundary_rate > 2:
        st.success("⚡ OVER (field restrictions)")
    else:
        st.warning("⚠️ WAIT")

else:
    if momentum == "HIGH" and last_boundaries >= 2:
        st.success("📈 OVER (build-up phase)")
    elif momentum == "LOW":
        st.error("📉 UNDER (slow phase)")
    else:
        st.warning("⚠️ NO CLEAR EDGE")

# Entry timing
st.subheader("Entry Timing ⏱️")

if last_runs > 15 and last_boundaries >= 2:
    st.success("👉 ENTER NOW")
elif last_runs < 8:
    st.error("👉 AVOID / EXIT")
else:
    st.warning("👉 WAIT FOR NEXT OVER")
