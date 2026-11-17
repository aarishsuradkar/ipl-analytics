# IPL Performance Analytics Dashboard

An interactive, 3-page analytics application built with **Streamlit** and **Plotly** to visualize tournament trends, player milestones, and franchise dynamics from pre-aggregated MySQL query exports.

---

## 1. Project Overview & Architecture

This dashboard provides deep insights into the Indian Premier League (IPL) across tournament history without querying live databases or recalculating raw ball-by-ball logs. Every figure, metric, and insight displayed is computed directly from exported SQL result CSVs.

### Verified Tournament Coverage
- **Franchise & Match Records (`q6_team_win_pct.csv`):** 17 seasons, spanning from **2007/08** to **2024**.
- **Top Scorer Season Records (`q1_top_scorers.csv`):** 12 seasons, spanning from **2007/08** to **2019**.
- **Total Matches Recorded:** **1,076 matches** (verified identically in `q3_toss_impact.csv` and derived from `q6_team_win_pct.csv`).

---

## 2. Key Computed Findings (From CSVs Only)

All insights and summary statistics are programmatically evaluated from the dataset:

### Tab 1: Overview & Toss Impact
- **Total Matches Played:** **1,076 matches** across 17 tournaments.
- **Toss Impact:**
  - Toss winners won **50.9%** of all matches (548 wins in 1,076 matches).
  - Teams choosing to **field** won **54.0%** of matches (374 wins in 692 matches).
  - Teams choosing to **bat** won **45.3%** of matches (174 wins in 384 matches).
  - *Finding:* Electing to field granted an **8.7 percentage point** advantage over batting first.

### Tab 2: Player Milestones
- **All-Time Leading Batter (`q7`, min 500 balls):** **V Kohli** leads with **5,156 runs** (4,042 balls, batting average of 38.5, strike rate of 127.6).
- **Highest Strike Rate (`q7`):** **V Sehwag** achieved the highest strike rate of **148.8** (2,728 runs off 1,833 balls).
- **Top Cumulative Season Scorer (`q1`, 2007/08–2019):** **DA Warner** amassed **2,928 runs** appearing in season top-5 ranks, followed by **CH Gayle** (2,515 runs) and **SK Raina** (2,451 runs).
- **Death-Over Bowling Mastery (`q10`, overs 15–20, min 180 balls):** **DE Bollinger** achieved the lowest death economy at **7.36 RPO** (242 balls, 297 runs), followed by **SP Narine** at **7.38 RPO** (768 balls, 944 runs).

### Tab 3: Franchise & Venue Dynamics
- **Most Matches Played (`q6`):**
  1. **Mumbai Indians:** 257 games
  2. **Kolkata Knight Riders:** 247 games
  3. **Delhi Capitals:** 246 games
- **Venue Scoring Extremes (`q5`, min 10 matches):**
  - **Highest Scoring 1st Innings Venue:** **M.Chinnaswamy Stadium** with an average first-innings score of **182.6** (11 matches).
  - **Lowest Scoring 1st Innings Venue:** **Dr DY Patil Sports Academy** with an average first-innings score of **146.6** (17 matches).
- **Death Phase Acceleration (`q4`):** **Royal Challengers Bangalore** leads all franchises in death-over scoring with **10.00 RPO**, followed by **Chennai Super Kings** at **9.80 RPO**.

---

## 3. Data Sources & File Schema

Data files reside in `output/` (and fallback `question sql/`):

| File | Description | Key Fields & Types |
| :--- | :--- | :--- |
| `q1_top_scorers.csv` | Top 5 run scorers per season | `season` (Text), `batter` (Text), `runs` (Int), `rnk` (Int) |
| `q3_toss_impact.csv` | Toss decision win rates | `toss_decision` (Text), `matches_played` (Int), `toss_winner_won` (Int), `win_pct` (Float) |
| `q4_phase_run_rate.csv` | Run rate across match phases | `batting_team` (Text), `phase` (Text: Powerplay/Middle/Death), `run_rate` (Float) |
| `q5_venue_scores.csv` | Average 1st innings venue score | `venue` (Text), `matches_played` (Int), `avg_first_innings` (Float) |
| `q6_team_win_pct.csv` | Team game counts and win % per season | `season` (Text), `team` (Text), `games_played` (Int), `wins` (Int), `win_pct` (Float) |
| `q7_batters.csv` | Career metrics for top batters | `batter` (Text), `runs` (Int), `balls` (Int), `strike_rate` (Float), `batting_avg` (Float) |
| `q10_death_bowlers.csv` | Death over economy leaders | `bowler` (Text), `balls` (Int), `runs` (Int), `economy` (Float) |
| `q8_cumulative_runs.csv` | Cumulative runs progression | `match_date` (Date), `runs` (Int), `cumulative_runs` (Int) |
| `matches_summary.csv` | Season match counts | *(Optional/Missing; derived dynamically from `q6`)* |
| `total_runs_by_season.csv` | Total runs by season | *(Optional/Missing; gracefully omitted in dashboard)* |

---

## 4. Setup & How to Run

### 4.1 Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Git (optional)

### 4.2 Activate Virtual Environment & Run
```powershell
# Clone or navigate to the repository directory
git clone https://github.com/aarishsuradkar/ipl-analytics.git
cd ipl-analytics

# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# (Optional) Verify requirements
pip install -r requirements.txt

# Run the Streamlit application
streamlit run app.py
```

The application will launch in your default web browser at `http://localhost:8501`.

---

## 5. Verification & Mathematical Integrity
Run the built-in verification script to confirm calculation parity against the raw CSV files:
```powershell
python verify_dashboard.py
```
This script audits:
- Zero summing of rates or percentages (only `mean()` or exact rates are used).
- Parity of match counts: `1076` matches in `q3` matches `2152 games / 2` in `q6`.
- Categorical string sorting of `season` to prevent year summation.
- Exactness of strike rate, economy, and win percentages.

---

## 6. Project Structure
```text
ipl-analytics/
├── app.py                      # Main Streamlit + Plotly application
├── PROJECT_REPORT.md           # Comprehensive end-to-end report with screenshots
├── requirements.txt            # Dependency specification
├── verify_dashboard.py         # Automated verification script
├── README_dashboard.md         # Project documentation and findings
├── powerbi_build_guide.md      # Step-by-step Power BI Desktop guide
├── output/                     # Standardized CSV inputs
├── question sql/               # Original exported query CSVs
├── screenshots/                # Dashboard captures for portfolio/docs
└── venv/                       # Python virtual environment
```

---

## 7. Notes
- **Run Rate Calculation:** As noted in query source comments, run rate counts wides and no-balls as balls, representing an operational approximation.
- **Missing Files Handled:** The dashboard gracefully handles absent optional files (`matches_summary.csv`, `total_runs_by_season.csv`) by calculating matches from `q6` and alerting the user about total runs.
