import pandas as pd
import json
import os
import glob

def build_player_lookup(db_file):
    """Creates a dictionary to translate names (and Cricsheet aliases) to your custom IDs."""
    print("🔄 Loading Player ID dictionary...")
    try:
        df = pd.read_csv(db_file)
        lookup = {str(row['Player_Name']).strip().lower(): str(row['Player_ID']) for _, row in df.iterrows()}
        
        # The Alias Dictionary: Map Cricsheet's weird names to your database names
        aliases = {
            "v kohli": "virat kohli",
            "ybk jaiswal": "yashasvi jaiswal",
            "jr hazlewood": "josh hazlewood",
            "rjw topley": "reece topley",
            "vg arora": "vaibhav arora",
            "d brevis": "dewald brevis",
            "k khejroliya": "kulwant khejroliya",
            "arshad khan": "arshad khan", # (If missing, means he wasn't in our 150-player DB)
            "mustafizur rahman": "mustafizur rahman"
        }
        
        # Merge these aliases into our lookup brain
        for alias, full_name in aliases.items():
            if full_name in lookup:
                lookup[alias] = lookup[full_name]
                
        return lookup
    except FileNotFoundError:
        print(f"Error: Could not find '{db_file}'.")
        return {}

def process_cricsheet_json(json_folder, player_lookup):
    """Reads all JSON files and builds the match log."""
    print(f"📂 Scanning '{json_folder}' for match files...")
    all_files = glob.glob(os.path.join(json_folder, "*.json"))
    
    match_data_list = []
    missing_players = set() # Keep track of names we couldn't match
    match_counter = 1

    for file in all_files:
        with open(file, 'r') as f:
            data = json.load(f)
            
            info = data.get('info', {})
            
            # 1. Filter for the 2025 season
            season = str(info.get('season', ''))
            if season != '2025':
                continue
                
            teams = info.get('teams', [])
            if len(teams) != 2: continue
            
            team_a, team_b = teams[0], teams[1]
            
            # 2. Extract Match Conditions
            venue = info.get('venue', 'Unknown Stadium')
            toss_winner = info.get('toss', {}).get('winner', 'Unknown')
            toss_decision = info.get('toss', {}).get('decision', 'Unknown')
            actual_winner = info.get('outcome', {}).get('winner', 'Tie/No Result')
            
            # 3. Extract Playing XIs
            players_dict = info.get('players', {})
            team_a_names = players_dict.get(team_a, [])
            team_b_names = players_dict.get(team_b, [])
            
            # Helper function to convert a list of names to a comma-separated string of IDs
            def translate_to_ids(name_list):
                ids = []
                for name in name_list:
                    clean_name = name.strip().lower()
                    if clean_name in player_lookup:
                        ids.append(player_lookup[clean_name])
                    else:
                        missing_players.add(name) # Log it if we don't have an ID for them
                return ",".join(ids)

            team_a_ids = translate_to_ids(team_a_names)
            team_b_ids = translate_to_ids(team_b_names)
            
            # Note: Cricsheet stores Impact Players (substitutions) deep in the innings data.
            # For this MVP script, we leave Impact Player blank to be added manually if needed.
            impact_a = ""
            impact_b = ""

            # 4. Append to our master list
            match_data_list.append({
                'Match_ID': match_counter,
                'Venue': venue,
                'Team_A': team_a,
                'Team_B': team_b,
                'Toss_Winner': toss_winner,
                'Toss_Decision': toss_decision,
                'Team_A_XI': team_a_ids,
                'Team_A_Impact': impact_a,
                'Team_B_XI': team_b_ids,
                'Team_B_Impact': impact_b,
                'Actual_Winner': actual_winner
            })
            match_counter += 1

    # Convert the list of dictionaries to a DataFrame
    final_df = pd.DataFrame(match_data_list)
    return final_df, missing_players

# Execute the pipeline
if __name__ == "__main__":
    player_lookup = build_player_lookup('player_db.csv')
    
    if player_lookup:
        # Assuming you unzipped the Cricsheet JSONs into a folder called 'ipl_json_data'
        final_match_log, missing = process_cricsheet_json('.', player_lookup)
        
        if not final_match_log.empty:
            output_file = 'automated_matches_2025.csv'
            final_match_log.to_csv(output_file, index=False)
            print(f"✅ Success! Created {len(final_match_log)} matches and saved to '{output_file}'.")
            
            if missing:
                print("\n⚠️ WARNING: Could not find IDs for the following players in your players_db.csv:")
                for p in list(missing)[:10]: # Print first 10 missing
                    print(f"  - {p}")
                print("You may need to check spelling in players_db.csv!")
        else:
            print("❌ No 2025 matches found. Ensure the JSON folder contains 2025 data.")