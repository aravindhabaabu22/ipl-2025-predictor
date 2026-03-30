import random
import pandas as pd

# -----------------------------
# TEAM DATA (Batting + Bowling)
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

    # Phase adjustments
    if phase == "powerplay":
        base_probs["4"] += 0.05
        base_probs["w"] += 0.02
    elif phase == "death":
        base_probs["6"] += 0.07
        base_probs["w"] += 0.03

    # Apply strengths
    base_probs["4"] *= bat_strength
    base_probs["6"] *= bat_strength * pitch_factor
    base_probs["w"] *= bowl_strength

    # Normalize
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

    total_runs = 0
    wickets = 0
    fours = 0
    sixes = 0

    for over in range(20):
        if wickets >= 10:
            break

        # Phase logic
        if over < 6:
            phase = "powerplay"
        elif over >= 16:
            phase = "death"
        else:
            phase = "middle"

        for ball in range(6):
            runs, wicket, f, s = simulate_ball(bat, bowl, phase, pitch_factor)

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
    score1, f1, s1 = simulate_innings(team1, team2, venue)
    score2, f2, s2 = simulate_innings(team2, team1, venue)

    winner = team1 if score1 > score2 else team2

    return {
        "score1": score1,
        "score2": score2,
        "fours_total": f1 + f2,
        "sixes_total": s1 + s2,
        "winner": winner
    }

# -----------------------------
# MONTE CARLO ENGINE
# -----------------------------
def monte_carlo(team1, team2, venue, sims=1000):
    results = []

    for _ in range(sims):
        results.append(simulate_match(team1, team2, venue))

    df = pd.DataFrame(results)

    summary = {
        "avg_total_runs": (df["score1"] + df["score2"]).mean(),
        "avg_fours": df["fours_total"].mean(),
        "avg_sixes": df["sixes_total"].mean(),
        "win_prob": df["winner"].value_counts(normalize=True) * 100
    }

    return summary, df

# -----------------------------
# RUN IT
# -----------------------------
summary, df = monte_carlo("MI", "CSK", "Mumbai", sims=2000)

print("\n🔥 ADVANCED SIMULATION RESULT")
print(summary)
