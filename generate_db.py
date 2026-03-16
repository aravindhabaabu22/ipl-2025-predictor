import json
import os
import glob
import pandas as pd
import random

def generate_player_db(json_folder='.'):
    print(f"📂 Scanning '{json_folder}' to build the ultimate 2025 player registry...")
    all_files = glob.glob(os.path.join(json_folder, "*.json"))
    
    # Dictionary to track unique players and their teams: {"V Kohli": "Royal Challengers Bengaluru"}
    players_dict = {}
    
    for file in all_files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            info = data.get('info', {})
            
            # Filter for only 2025 matches
            season = str(info.get('season', ''))
            if season != '2025':
                continue
            
            # Extract every player listed in the match info
            registry = info.get('players', {})
            for team, player_list in registry.items():
                for player_name in player_list:
                    # If we haven't seen them before, add them to our dict!
                    if player_name not in players_dict:
                        players_dict[player_name] = team

    if not players_dict:
        print("❌ No players found. Check if the JSON files are in this folder and are from 2025.")
        return

    print(f"✅ Found {len(players_dict)} unique players across the 2025 season!")
    
    # Build the dataframe
    db_rows = []
    player_id_counter = 1001  # Start IDs at 1001 to keep it clean
    
    # We set a seed so the "random" stats stay exactly the same every time you run the script
    random.seed(42) 
    
    for player, team in players_dict.items():
        db_rows.append({
            'Player_ID': player_id_counter,
            'Player_Name': player,
            'Team': team,
            # Generating baseline attributes to test the model
            'Power': random.randint(40, 95),
            'Innovation': random.randint(40, 95),
            'Acceleration': random.randint(40, 95)
        })
        player_id_counter += 1
        
    df = pd.DataFrame(db_rows)
    
    # Save directly over your old file
    output_file = 'player_db.csv'
    df.to_csv(output_file, index=False)
    print(f"✅ Master database successfully generated and saved to '{output_file}'!")

if __name__ == "__main__":
    generate_player_db('.')