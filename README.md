\# IPL 2025 Simulator \& Predictor (85.1% Accuracy)



My personal project: Full automated IPL 2025 simulation + machine learning predictor.



\*\*Final accuracy:\*\* 85.1% on all 74 matches (using player stats + Cricsheet-style phase analysis).



\---



\## What I Built

\- Generated 202 players with Power, Innovation, Acceleration stats

\- Simulated full 74-match season

\- Built 3 versions of predictor (v1 → v3)

\- Used ball-by-ball JSON phase data (Powerplay, Death overs, extras) to reach 85%



\---



\## Project Structure



```

data/                  ← All input files

├── player\_db.csv

├── automated\_matches\_2025.csv

├── automated\_matches\_2024.csv



scripts/               ← All code

├── ipl\_predictor\_v3.py     ← Best version (run this!)

├── generate\_db.py

├── build\_match\_log.py



outputs/               ← Results

├── predictions\_2025\_with\_json.csv   ← Final predictions

```



\---



\## How to Run (for my friend)



\### 1. Clone



```bash

git clone https://github.com/Claws333/ipl-2025-predictor.git

cd ipl-2025-predictor

```



\### 2. Install dependencies



```bash

pip install pandas numpy scikit-learn

```



\### 3. Run the best model



```bash

python scripts/ipl\_predictor\_v3.py

```



You will see \*\*85% accuracy printed\*\* + new predictions generated.



\---



\## Accuracy Journey



\- v1: \*\*52.7%\*\*

\- v2: \*\*67.6%\*\*

\- v3: \*\*85.1%\*\* (added phase stats from JSONs)



\---



\## Extending to 2026



Want to see 2026 predictions?



Just add new players to:



```

data/player\_db.csv

```



Then run the same script.



\---



Made purely for learning. Feel free to fork!



Questions? DM me.

