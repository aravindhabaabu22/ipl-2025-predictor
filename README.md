# IPL 2025 Simulator & Predictor (85.1% Accuracy)

A personal project building an automated IPL season simulator and machine learning match predictor.

**Final accuracy:** 85.1% across all 74 IPL matches using player performance attributes and phase-level match data.

---

## Overview

This project simulates an IPL season and predicts match outcomes using structured player data and match phase statistics.

Key ideas used in the model:

- Player attributes (Power, Innovation, Acceleration)
- Team composition effects
- Phase-based match analysis (Powerplay, Middle overs, Death overs)
- Ball-by-ball data inspired by Cricsheet JSON structure

---

## Features

- Generated a database of **202 players** with performance attributes
- Simulated a full **74-match IPL season**
- Built and iterated through **three predictor versions**
- Integrated **phase-based match features** to significantly improve prediction accuracy

---

## Project Structure

```
data/                  # Input datasets
├── player_db.csv
├── automated_matches_2025.csv
├── automated_matches_2024.csv

scripts/               # Core code
├── ipl_predictor_v3.py
├── generate_db.py
├── build_match_log.py

outputs/               # Model results
├── predictions_2025_with_json.csv
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Claws333/ipl-2025-predictor.git
cd ipl-2025-predictor
```

Install dependencies:

```bash
pip install pandas numpy scikit-learn
```

---

## Running the Predictor

Execute the main prediction script:

```bash
python scripts/ipl_predictor_v3.py
```

The script will train the model and generate match predictions.

Results will be saved in:

```
outputs/predictions_2025_with_json.csv
```

---

## Accuracy Progression

| Version | Approach | Accuracy |
|-------|--------|--------|
| v1 | Basic team statistics | 52.7% |
| v2 | Player attribute features | 67.6% |
| v3 | Added phase-level match stats | **85.1%** |

---

## Extending the Model

To simulate or predict future seasons:

1. Update player data in

```
data/player_db.csv
```

2. Run the predictor again:

```bash
python scripts/ipl_predictor_v3.py
```

---

## Notes

This project was built for experimentation and learning in sports analytics and machine learning.

Contributions and improvements are welcome.
