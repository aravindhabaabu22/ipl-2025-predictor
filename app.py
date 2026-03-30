import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="IPL Predictor", layout="centered")

st.title("🏏 IPL Advanced Monte Carlo Predictor")

# -----------------------------
# TEAM DATA
# -----------------------------
teams = {
    "MI": {"bat": 1.05, "bowl": 1.00},
    "CSK": {"bat": 1.00, "bowl": 1.05},
    "RCB": {"bat": 1.08, "bowl": 0.95},
    "KKR": {"bat": 1.02, "bowl": 1.02},
    "DC": {"bat": 0.95, "bowl": 0.97},
    "SRH": {"bat": 1.00, "bowl": 1.00},
    "LSG": {"bat": 1.01, "bowl": 1.02},
    "RR": {"bat": 1.04, "bowl": 1.01},
    "PBKS": {"bat": 1.03, "bowl": 0.96},
    "GT": {"bat": 1.02, "bowl": 1.05}
}

# -----------------------------
# PITCH CONDITIONS
# -----------------------------
pitch = {
    "Chennai": {"run_factor": 0.9, "six_factor": 0.8},
    "Mumbai": {"run_factor": 1.1, "six_factor": 1.2},
    "Bangalore": {"run_factor": 1.15, "six_factor": 1.3},
    "Delhi": {"run_factor": 1.05, "six_factor": 1.1},
    "Lucknow": {"run_factor": 0.95, "six_factor": 0.9}
}

# -----------------------------
# USER INPUT
# -----------------------------
team1 = st.selectbox("Select Team 1", list(teams.keys()))
team2 = st.selectbox("Select Team 2", list(teams.keys()))
venue = st.selectbox("Select Venue", list(pitch.keys()))
sims = st.slider("Simulations", 500, 5000, 2000)

if team1 == team2:
    st.error("❌ Select two different teams")
    st.stop()

# -----------------------------
# BALL SIMULATION
# -----------------------------
def simulate_ball(bat_strength, bowl_strength, phase, pitch_factor):
    base_probs = {
        "dot": 0.30,
        "1": 0.30,
        "2": 0.10,
        "4": 0.15,
        "6": 0.10,
        "w": 0.05
    }

    if phase == "powerplay":
        base_probs["4"] += 0.05
        base_probs["w"] += 0.02
    elif phase == "death":
        base_probs["6"] += 0.07
        base_probs["w"] += 0.03

    base_probs["4"] *= bat_strength
    base_probs["6"] *= bat_strength * pitch_factor
    base_probs["w"] *= bowl_strength

    total = sum(base_probs.values())
    probs = [v / total for v in base_probs.values()]
    outcomes = list(base_probs.keys())

    result = random.choices(outcomes, probs)[0]

    if result == "w":
        return 0, True, 0, 0
    elif result == "4":
        return 4, False, 1, 0
    elif result == "6":
        return 6, False, 0, 1
    elif result == "dot":
        return 0, False, 0, 0
    else:
        return int(result), False, 0, 0

# -----------------------------
# INNINGS SIMULATION
# -----------------------------
def simulate_innings(team_bat, team_bowl, venue):
    bat = teams[team_bat]["bat"]
    bowl = teams[team_bowl]["bowl"]
    pitch_factor = pitch[venue]["six_factor"]
    run_factor = pitch[venue]["run_factor"]

    total_runs = 0
    wickets = 0
    fours = 0
    sixes = 0

    for over in range(20):
        if wickets >= 10:
            break

        if over < 6:
            phase = "powerplay"
        elif over >= 16:
            phase = "death"
        else:
            phase = "middle"

        for ball in range(6):
            runs, wicket, f, s = simulate_ball(bat, bowl, phase, pitch_factor)

            runs = int(runs * run_factor)

            total_runs += runs
            fours += f
            sixes += s

            if wicket:
                wickets += 1
                if wickets >= 10:
                    break

    return total_runs, fours, sixes

# -----------------------------
# MATCH SIMULATION
# -----------------------------
def simulate_match(team1, team2, venue):
    try:
        s1, f1, x1 = simulate_innings(team1, team2, venue)
        s2, f2, x2 = simulate_innings(team2, team1, venue)

        return {
            "winner": team1 if s1 > s2 else team2,
            "total_runs": s1 + s2,
            "fours": f1 + f2,
            "sixes": x1 + x2
        }
    except:
        return {
            "winner": team1,
            "total_runs": 0,
            "fours": 0,
            "sixes": 0
        }

# -----------------------------
# RUN SIMULATION
# -----------------------------
if st.button("🔥 Run Simulation"):
    results = [simulate_match(team1, team2, venue) for _ in range(sims)]
    df = pd.DataFrame(results)

    st.subheader("📊 Results")

    win_prob = df["winner"].value_counts(normalize=True) * 100

    avg_runs = df["total_runs"].mean()
    avg_fours = df["fours"].mean()
    avg_sixes = df["sixes"].mean()

    st.write("🏆 Win Probability")
    st.write(win_prob)

    st.write(f"📈 Avg Total Runs: {avg_runs:.2f}")
    st.write(f"🏏 Avg Fours: {avg_fours:.2f}")
    st.write(f"💥 Avg Sixes: {avg_sixes:.2f}")

    # -----------------------------
    # BETTING INSIGHTS
    # -----------------------------
    st.subheader("💰 Betting Insights")

    if avg_fours > 30:
        st.success("✅ Likely OVER on Fours")
    else:
        st.warning("⚠️ Likely UNDER on Fours")

    if avg_sixes > 14:
        st.success("✅ Likely OVER on Sixes")
    else:
        st.warning("⚠️ Likely UNDER on Sixes")

    if avg_runs > 320:
        st.success("🔥 High scoring match (OVER runs)")
    else:
        st.warning("🧊 Low scoring match (UNDER runs)")
