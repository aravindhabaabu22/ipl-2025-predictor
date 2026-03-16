import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder

# ====================== LOAD DATA ======================
matches = pd.read_csv('automated_matches_2025.csv')
players = pd.read_csv('player_db.csv')

# ====================== HELPER FUNCTIONS ======================
def get_team_features(xi_str, players_df):
    if not isinstance(xi_str, str):
        return {k: 0 for k in ['avg_power', 'avg_innov', 'avg_accel', 'high_power', 
                               'high_accel', 'high_innov', 'batting_str', 'bowling_str']}
    ids = [int(x.strip()) for x in xi_str.split(',') if x.strip().isdigit()]
    df = players_df[players_df['Player_ID'].isin(ids)].copy()
    if len(df) == 0:
        return {k: 0 for k in ['avg_power', 'avg_innov', 'avg_accel', 'high_power', 
                               'high_accel', 'high_innov', 'batting_str', 'bowling_str']}
    
    feats = {
        'avg_power': df['Power'].mean(),
        'avg_innov': df['Innovation'].mean(),
        'avg_accel': df['Acceleration'].mean(),
        'high_power': (df['Power'] > 85).sum(),
        'high_accel': (df['Acceleration'] > 85).sum(),
        'high_innov': (df['Innovation'] > 80).sum(),
        'batting_str': df.iloc[:6]['Power'].mean() if len(df) >= 6 else df['Power'].mean(),   # top 6 = batters
        'bowling_str': df.iloc[-6:]['Acceleration'].mean() if len(df) >= 6 else df['Acceleration'].mean()  # last 6 = death/impact
    }
    return feats

# Pre-compute venue chase bias (exactly like Cricsheet venue stats)
venue_chase = matches.groupby('Venue').apply(
    lambda g: (g['Actual_Winner'] == g['Team_B']).mean() if len(g) > 0 else 0.5
).to_dict()

# ====================== BUILD FEATURE MATRIX ======================
features = []
targets = []

for _, row in matches.iterrows():
    a_feats = get_team_features(row['Team_A_XI'], players)
    b_feats = get_team_features(row['Team_B_XI'], players)
    
    # Venue bias
    chase_bias = venue_chase.get(row['Venue'], 0.5)
    
    # Toss bonus (Cricsheet-style)
    toss_bonus_a = 0
    if row['Toss_Winner'] == row['Team_A']:
        if row['Toss_Decision'] == 'field':
            toss_bonus_a = 3.8 + chase_bias * 2.0   # strong field-first at dew venues
        else:
            toss_bonus_a = 1.2 - chase_bias * 1.0
    else:
        toss_bonus_a = - (3.8 + chase_bias * 2.0) if row['Toss_Decision'] == 'field' else -1.2
    
    row_dict = {
        'power_diff': a_feats['avg_power'] - b_feats['avg_power'],
        'innov_diff': a_feats['avg_innov'] - b_feats['avg_innov'],
        'accel_diff': a_feats['avg_accel'] - b_feats['avg_accel'],
        'high_power_diff': a_feats['high_power'] - b_feats['high_power'],
        'high_accel_diff': a_feats['high_accel'] - b_feats['high_accel'],
        'high_innov_diff': a_feats['high_innov'] - b_feats['high_innov'],
        'batting_diff': a_feats['batting_str'] - b_feats['batting_str'],
        'bowling_diff': a_feats['bowling_str'] - b_feats['bowling_str'],
        'toss_bonus': toss_bonus_a,
        'chase_bias': chase_bias,
        'total_impact_a': a_feats['high_innov'],
        'total_impact_b': b_feats['high_innov']
    }
    features.append(row_dict)
    
    # Target: 1 if Team_A wins, 0 if Team_B wins (ignore Tie for simplicity)
    winner = row['Actual_Winner']
    if winner == row['Team_A']:
        targets.append(1)
    elif winner == row['Team_B']:
        targets.append(0)
    else:
        targets.append(1)  # rare Tie → treat as A win (only 4 cases)

X = pd.DataFrame(features)
y = np.array(targets)

# ====================== TRAIN & EVALUATE ======================
model = RandomForestClassifier(n_estimators=400, max_depth=12, random_state=42, class_weight='balanced')

# 5-fold CV accuracy
cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"5-Fold CV Accuracy: {cv_scores.mean():.1%} ± {cv_scores.std():.1%}")

# Final model on full data (for prediction table)
model.fit(X, y)
pred = model.predict(X)
accuracy = (pred == y).mean()
print(f"Full-dataset Backtest Accuracy: {accuracy:.1%}")

# ====================== PREDICTION TABLE (first 15 + last 5) ======================
matches['Predicted_Winner'] = ''
for i, p in enumerate(pred):
    if p == 1:
        matches.loc[i, 'Predicted_Winner'] = matches.loc[i, 'Team_A']
    else:
        matches.loc[i, 'Predicted_Winner'] = matches.loc[i, 'Team_B']

print("\nSample Predictions:")
print(matches[['Match_ID', 'Team_A', 'Team_B', 'Actual_Winner', 'Predicted_Winner']].head(15))
print("... (full table saved as 'predictions_2025.csv')")

matches.to_csv('predictions_2025.csv', index=False)
print("Full predictions saved to predictions_2025.csv")