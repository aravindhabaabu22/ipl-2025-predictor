import pandas as pd

def calculate_team_score(xi_string, impact_id, players_df):
    """Averages the attributes of the Playing XI + Impact Player."""
    try:
        player_ids = [int(pid.strip()) for pid in str(xi_string).split(',') if pid.strip()]
        if pd.notna(impact_id) and str(impact_id).strip() != '':
            player_ids.append(int(float(impact_id)))
    except ValueError:
        return 0
    
    team_squad = players_df[players_df['Player_ID'].isin(player_ids)]
    if team_squad.empty:
        return 0
        
    avg_power = team_squad['Power'].mean()
    avg_innovation = team_squad['Innovation'].mean()
    avg_acceleration = team_squad['Acceleration'].mean()
    
    return round(avg_power + avg_innovation + avg_acceleration, 2)

def run_hybrid_predictions():
    db_file = 'player_db.csv'
    match_file = 'automated_matches_2025.csv'
    
    print("🏏 FIRING UP THE HYBRID PREDICTION ENGINE 🏏\n" + "="*65)
    try:
        players_df = pd.read_csv(db_file)
        matches_df = pd.read_csv(match_file)
    except FileNotFoundError as e:
        print(f"Error: Ensure both files exist. {e}")
        return

    correct = 0
    total = 0
    
    # Venue Bias Dictionary
    chasing_venues = ['Wankhede Stadium', 'M. Chinnaswamy Stadium', 'Eden Gardens', 'Narendra Modi Stadium']
    defending_venues = ['M.A. Chidambaram Stadium', 'Ekana Stadium', 'Sawai Mansingh Stadium']
    
    for index, match in matches_df.iterrows():
        team_a = match['Team_A']
        team_b = match['Team_B']
        venue = match['Venue']
        toss_winner = match['Toss_Winner']
        toss_decision = str(match['Toss_Decision']).lower().strip()
        
        # 1. Get Base Micro-Stat Scores
        base_score_a = calculate_team_score(match['Team_A_XI'], match.get('Team_A_Impact', ''), players_df)
        base_score_b = calculate_team_score(match['Team_B_XI'], match.get('Team_B_Impact', ''), players_df)
        
        if base_score_a + base_score_b == 0:
            continue

        # 2. Apply Context Multipliers (The Magic Sauce)
        multiplier_a = 1.0
        multiplier_b = 1.0
        
        team_a_chasing = (toss_winner == team_a and toss_decision == 'bowl') or \
                         (toss_winner == team_b and toss_decision == 'bat')

        if venue in chasing_venues:
            if team_a_chasing:
                multiplier_a += 0.05  # 5% boost for chasing here
                multiplier_b -= 0.02
            else:
                multiplier_b += 0.05
                multiplier_a -= 0.02
        elif venue in defending_venues:
            if team_a_chasing:
                multiplier_b += 0.05  # 5% boost for defending here
                multiplier_a -= 0.02
            else:
                multiplier_a += 0.05
                multiplier_b -= 0.02
                
        # Calculate Final Adjusted Scores
        final_score_a = base_score_a * multiplier_a
        final_score_b = base_score_b * multiplier_b
            
        if final_score_a > final_score_b:
            favorite = team_a
        else:
            favorite = team_b
            
        actual = match.get('Actual_Winner', 'Unknown')
        
        if actual != 'Unknown' and actual != 'Tie/No Result':
            total += 1
            if favorite == actual:
                correct += 1
                marker = "✅ CORRECT"
            else:
                marker = "❌ INCORRECT"

    if total > 0:
        accuracy = (correct / total) * 100
        print("\n" + "*"*65)
        print(" 📊 FINAL HYBRID BACKTESTING RESULTS 📊")
        print("*"*65)
        print(f"Total Matches Analyzed: {total}")
        print(f"Correct Predictions: {correct}")
        print(f"Model Accuracy: {accuracy:.2f}%")
        print("*"*65 + "\n")

if __name__ == "__main__":
    run_hybrid_predictions()