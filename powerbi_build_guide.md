# Power BI Desktop Build Guide: IPL Performance Analytics Dashboard

This step-by-step guide walks you through building the exact 3-page interactive dashboard in **Power BI Desktop** using the CSV result files exported from MySQL.

---

## 1. Data Loading & Power Query Setup

### 1.1 Import CSV Files
In Power BI Desktop:
1. Click **Home > Get Data > Text/CSV**.
2. Navigate to your project folder (`ipl-analytics/output` or `ipl-analytics/question sql`).
3. Load the following files:
   - `q1_top_scorers.csv` (or `q1.csv`)
   - `q3_toss_impact.csv` (or `q3.csv`)
   - `q4_phase_run_rate.csv` (or `q4.csv`)
   - `q5_venue_scores.csv` (or `q5.csv`)
   - `q6_team_win_pct.csv` (or `q6.csv`)
   - `q7_batters.csv` (or `q7.csv`)
   - `q10_death_bowlers.csv` (or `q10.csv`)
   - *(Optional if exported)*: `matches_summary.csv`, `total_runs_by_season.csv`, `q8_cumulative_runs.csv`.

---

### 1.2 Set Explicit Data Types in Power Query
Open **Transform Data** (Power Query Editor) and verify/change the data types for each table:

| Table | Column | Required Data Type | Why? |
| :--- | :--- | :--- | :--- |
| **q1_top_scorers** | `season` | **Text** | Prevents numeric addition; preserves split seasons like `2007/08`. |
| | `batter` | **Text** | Categorical name. |
| | `runs` | **Whole Number** | Additive count. |
| | `rnk` | **Whole Number** | Ordinal rank. |
| **q3_toss_impact** | `toss_decision` | **Text** | Dimension (`field`, `bat`). |
| | `matches_played` | **Whole Number** | Additive count. |
| | `toss_winner_won` | **Whole Number** | Additive count. |
| | `win_pct` | **Decimal Number** | Rate / percentage. **Never sum!** |
| **q4_phase_run_rate** | `batting_team` | **Text** | Team dimension. |
| | `phase` | **Text** | Match phase (`Powerplay`, `Middle`, `Death`). |
| | `run_rate` | **Decimal Number** | Rate (RPO). **Never sum!** |
| **q5_venue_scores** | `venue` | **Text** | Venue name. |
| | `matches_played` | **Whole Number** | Additive count. |
| | `avg_first_innings` | **Decimal Number** | Continuous score average. **Never sum!** |
| **q6_team_win_pct** | `season` | **Text** | Prevents summation; preserves chronological labels. |
| | `team` | **Text** | Team dimension. |
| | `games_played` | **Whole Number** | Total games played by team. |
| | `wins` | **Whole Number** | Wins count. |
| | `win_pct` | **Decimal Number** | Win percentage. **Never sum!** |
| **q7_batters** | `batter` | **Text** | Player name. |
| | `runs`, `balls` | **Whole Number** | Counts. |
| | `strike_rate`, `batting_avg` | **Decimal Number** | Performance rates. **Never sum!** |
| **q10_death_bowlers** | `bowler` | **Text** | Player name. |
| | `balls`, `runs` | **Whole Number** | Counts. |
| | `economy` | **Decimal Number** | Economy rate (RPO). **Never sum!** |

Click **Close & Apply**.

---

### 1.3 Recommended DAX Measures
Create a dedicated table or add measures to respective tables:

```dax
// Total Matches from q3
Total Matches = SUM(q3_toss_impact[matches_played])

// Matches derived from q6 (since 2 teams play each match)
Matches from Teams = SUM(q6_team_win_pct[games_played]) / 2

// Distinct Seasons
Total Seasons = DISTINCTCOUNT(q6_team_win_pct[season])

// Toss Win Rate (Safe Average)
Avg Toss Win Pct = AVERAGE(q3_toss_impact[win_pct])

// Team Win Rate (Safe Average)
Avg Team Win Pct = AVERAGE(q6_team_win_pct[win_pct])

// Venue 1st Innings Average
Avg First Innings = AVERAGE(q5_venue_scores[avg_first_innings])

// Phase Run Rate
Avg Phase Run Rate = AVERAGE(q4_phase_run_rate[run_rate])

// Death Economy
Avg Death Economy = AVERAGE(q10_death_bowlers[economy])
```

---

## 2. Page 1: Overview

### 2.1 Header & Theme
- **Page Name:** `Overview`
- **Page Size:** 16:9 widescreen (1280 x 720).
- **Title Text Box:** `IPL Tournament Overview & Toss Impact Analysis`
- **Subtitle:** `High-level operational metrics and toss decision impact across tournament history.`

### 2.2 Visuals Configuration
1. **KPI Card 1 (Total Matches):**
   - **Visual:** Card.
   - **Field:** `Total Matches` (or `matches_played` from `q3_toss_impact`, Aggregation: **Sum**).
   - **Expected Value:** `1,076`.
   - **Label:** "Total Matches Played".
2. **KPI Card 2 (Total Tournament Runs):**
   - **Visual:** Card.
   - **Field:** If `total_runs_by_season.csv` is loaded: `SUM(total_runs_by_season[total_runs])`. Otherwise, place a card with text `Not in Exports` and a subtitle note.
3. **KPI Card 3 (Tournaments Covered):**
   - **Visual:** Card.
   - **Field:** `season` from `q6_team_win_pct`, Aggregation: **Distinct Count**.
   - **Expected Value:** `17`.
   - **Label:** "IPL Seasons".
4. **Visual 4 - Column Chart (Matches per Season):**
   - **Visual:** Clustered column chart.
   - **X-axis:** `q6_team_win_pct[season]`.
   - **Y-axis:** Measure `Matches from Teams` (or `games_played` divided by 2).
   - **Sort:** By `season` ascending.
   - **Data Labels:** On.
5. **Visual 5 - Column Chart (Toss Winner Match Win Rate):**
   - **Visual:** Clustered column chart.
   - **X-axis:** `q3_toss_impact[toss_decision]`.
   - **Y-axis:** `q3_toss_impact[win_pct]`, Aggregation: **Average** (Measure: `Avg Toss Win Pct`).
   - **Data Labels:** On (Display: `54.0%` for field, `45.3%` for bat).
   - **Y-axis limits:** Min 0, Max 100.
6. **Insight Box (Text Box):**
   - Place an Amber/Blue bordered callout text box:
   > **Key Insight:** Across 1,076 matches, toss winners won **50.9%** of games (548 wins). Choosing to **field** resulted in a significantly higher win rate (**54.0%**, 374 of 692 matches) compared to choosing to **bat** (**45.3%**, 174 of 384 matches).

---

## 3. Page 2: Players

### 3.1 Header
- **Page Name:** `Players`
- **Title Text Box:** `IPL Player Performance & Death Bowling Milestones`

### 3.2 Visuals Configuration
1. **Slicer 1 (Season Selector):**
   - **Visual:** Slicer.
   - **Field:** `q1_top_scorers[season]`.
   - **Format:** Dropdown style. Enable "Select All" option.
2. **Visual 2 - Horizontal Bar Chart (Top Run Scorers):**
   - **Visual:** Clustered bar chart.
   - **Y-axis:** `q1_top_scorers[batter]`.
   - **X-axis:** `q1_top_scorers[runs]`, Aggregation: **Sum**.
   - **Filters on Visual:** Top N filter -> Top 10 by `runs` (Sum).
   - **Sort:** By `runs` descending (highest at top).
   - **Data Labels:** On (Values formatted with `,` separator).
3. **Visual 3 - Performance Table (Leading All-Time Batters):**
   - **Visual:** Table.
   - **Columns:**
     - `q7_batters[batter]`
     - `q7_batters[runs]` (Aggregation: **Sum**, Format: `#,##0`)
     - `q7_batters[balls]` (Aggregation: **Sum**, Format: `#,##0`)
     - `q7_batters[strike_rate]` (Aggregation: **Average**, Format: `0.0`)
     - `q7_batters[batting_avg]` (Aggregation: **Average**, Format: `0.0`)
   - **Sort:** Click `runs` column header to sort descending.
4. **Visual 4 - Horizontal Bar Chart (Best Death Bowlers):**
   - **Visual:** Clustered bar chart.
   - **Y-axis:** `q10_death_bowlers[bowler]`.
   - **X-axis:** `q10_death_bowlers[economy]`, Aggregation: **Average**.
   - **Sort:** By `economy` **Ascending** (Lowest/best economy at top).
   - **Data Labels:** On (Format: `0.00`).
   - **Tooltip:** `balls` (Sum), `runs` (Sum).
5. **Insight Box (Text Box):**
   > **Player Insight:** Among listed top batters (min 500 balls), **V Sehwag** holds the highest strike rate at **148.8** (2,728 runs off 1,833 balls), while **V Kohli** leads in total runs with **5,156 runs** (avg 38.5). In death overs (15–20), **DE Bollinger** achieved the best economy rate at **7.36 RPO** across 242 balls.

---

## 4. Page 3: Teams & Venues

### 4.1 Header
- **Page Name:** `Teams & Venues`
- **Title Text Box:** `IPL Franchise Consistency & Venue Scoring Dynamics`

### 4.2 Visuals Configuration
1. **Slicer 1 (Team Selector):**
   - **Visual:** Slicer.
   - **Field:** `q6_team_win_pct[team]`.
   - **Selection:** Multi-select with Search. Pre-select: **Mumbai Indians**, **Kolkata Knight Riders**, **Delhi Capitals**.
2. **Visual 2 - Line Chart (Team Win % by Season):**
   - **Visual:** Line chart.
   - **X-axis:** `q6_team_win_pct[season]`.
   - **Y-axis:** `q6_team_win_pct[win_pct]`, Aggregation: **Average** (Measure: `Avg Team Win Pct`).
   - **Legend:** `q6_team_win_pct[team]`.
   - **Markers:** Turn ON.
   - **Y-axis bounds:** Min 0, Max 100.
3. **Visual 3 - Horizontal Bar Chart (Venue Scores):**
   - **Visual:** Clustered bar chart.
   - **Y-axis:** `q5_venue_scores[venue]`.
   - **X-axis:** `q5_venue_scores[avg_first_innings]`, Aggregation: **Average**.
   - **Filters on Visual:** Top N filter -> Top 10 by `avg_first_innings` (Average).
   - **Sort:** Descending (Highest score at top).
   - **Data Labels:** On (Format: `0.0`).
4. **Visual 4 - Clustered Column Chart (Run Rate by Phase):**
   - **Visual:** Clustered column chart.
   - **X-axis:** `q4_phase_run_rate[batting_team]`.
   - **Legend:** `q4_phase_run_rate[phase]`.
   - **Y-axis:** `q4_phase_run_rate[run_rate]`, Aggregation: **Average**.
   - **Slicer on Page:** `q4_phase_run_rate[batting_team]` to select teams.
5. **Insight Box (Text Box):**
   > **Venue & Phase Insight:** Across qualifying venues (min 10 matches), **M.Chinnaswamy Stadium** recorded the highest first innings average at **182.6**, whereas **Dr DY Patil Sports Academy** was the lowest at **146.6**. In the death overs, **Royal Challengers Bangalore** scored at the fastest clip with a **10.0 RPO** run rate.

---

## 5. Footer on Every Page
Add a text box at the bottom:
> *Built from SQL query outputs (MySQL). Run rate counts wides and no-balls as balls, so it is approximate.*

---

## 6. Pre-Screenshot Checklist
Before taking screenshots or publishing:
1. **Clear Slicers:** Reset slicers on Page 2 (`All seasons`) and Page 3 (to default 3 teams).
2. **Data Labels:** Ensure data labels are enabled and readable without clipping.
3. **Verify Aggregations:** Double check that **no** percentage or rate column is using `Sum`.
4. **Sort Orders:** Verify death bowlers are sorted **ascending** (lowest economy at top) and batters are sorted **descending** (highest runs at top).

---

## 7. Common Power BI Mistakes to Avoid
1. **Summing Percentages/Rates:** Defaulting to `SUM(win_pct)` will produce nonsensical values (e.g. 500%+). Always select **Average** or write an explicit measure.
2. **Season Stored as Number:** If `season` is imported as an integer, Power BI will attempt to sum the years (e.g., `40,000+`) and fail on split seasons like `2007/08`. Keep `season` as **Text**.
3. **Counting Matches from `games_played` Directly:** Each match has two participating teams, so `games_played` sums to 2,152. You must divide by 2 to get the actual 1,076 matches.
4. **Sorting Death Bowlers Incorrectly:** In bowling, a lower economy is better. Sorting descending puts the most expensive bowlers at the top. Sort **ascending**.
