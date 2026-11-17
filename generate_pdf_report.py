import os
import base64
import subprocess

BASE_DIR = r"C:\Users\SCI\Desktop\data analyst\ipl-analytics"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
ARTIFACT_DIR = r"C:\Users\SCI\.gemini\antigravity\brain\07f4c343-2594-4aa8-be4e-77c025700795"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def get_base64_img(filename):
    path = os.path.join(SCREENSHOTS_DIR, filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    return ""

img_overview = get_base64_img("dashboard_overview.png")
img_players = get_base64_img("dashboard_players.png")
img_teams = get_base64_img("dashboard_teams.png")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>IPL Performance Analytics Project Report</title>
<style>
    @page {{
        size: A4;
        margin: 15mm 15mm 15mm 15mm;
    }}
    body {{
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
        color: #1F2937;
        background-color: #FFFFFF;
        line-height: 1.5;
        font-size: 10.5pt;
        margin: 0;
        padding: 0;
    }}
    .header-banner {{
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 60%, #2563EB 100%);
        color: white;
        padding: 24px 28px;
        border-radius: 8px;
        margin-bottom: 24px;
    }}
    .header-banner h1 {{
        margin: 0 0 6px 0;
        font-size: 22pt;
        font-weight: 700;
        letter-spacing: -0.5px;
    }}
    .header-banner p {{
        margin: 0;
        font-size: 11pt;
        opacity: 0.9;
    }}
    .meta-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-top: 16px;
        padding-top: 14px;
        border-top: 1px solid rgba(255, 255, 255, 0.25);
    }}
    .meta-item {{
        font-size: 8.5pt;
    }}
    .meta-item span {{
        display: block;
        opacity: 0.75;
        text-transform: uppercase;
        font-size: 7.5pt;
        letter-spacing: 0.5px;
    }}
    .meta-item strong {{
        font-size: 9.5pt;
        color: #F8FAFC;
    }}

    h2 {{
        color: #1E3A8A;
        font-size: 14pt;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 6px;
        margin-top: 24px;
        margin-bottom: 12px;
        page-break-after: avoid;
    }}
    h3 {{
        color: #1F2937;
        font-size: 11.5pt;
        margin-top: 16px;
        margin-bottom: 8px;
        page-break-after: avoid;
    }}
    p, li {{
        font-size: 10pt;
        color: #374151;
    }}
    ul, ol {{
        margin-top: 4px;
        margin-bottom: 10px;
        padding-left: 20px;
    }}

    /* Table styling */
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0 16px 0;
        font-size: 9pt;
        page-break-inside: avoid;
    }}
    th {{
        background-color: #1E3A8A;
        color: white;
        text-align: left;
        padding: 7px 10px;
        font-weight: 600;
    }}
    td {{
        padding: 6px 10px;
        border-bottom: 1px solid #E5E7EB;
        color: #374151;
    }}
    tr:nth-child(even) td {{
        background-color: #F8FAFC;
    }}

    /* Cards */
    .kpi-container {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin: 14px 0;
        page-break-inside: avoid;
    }}
    .kpi-card {{
        background: #F1F5F9;
        border: 1px solid #CBD5E1;
        border-left: 4px solid #1E3A8A;
        padding: 10px 14px;
        border-radius: 6px;
    }}
    .kpi-title {{
        font-size: 8pt;
        text-transform: uppercase;
        color: #64748B;
        font-weight: 600;
    }}
    .kpi-val {{
        font-size: 16pt;
        font-weight: 700;
        color: #0F172A;
        margin-top: 2px;
    }}
    .kpi-sub {{
        font-size: 7.5pt;
        color: #64748B;
        margin-top: 2px;
    }}

    .callout {{
        background-color: #FFFBEB;
        border-left: 4px solid #F59E0B;
        border-radius: 4px;
        padding: 10px 14px;
        margin: 12px 0;
        font-size: 9.5pt;
        color: #92400E;
        page-break-inside: avoid;
    }}
    .callout strong {{
        color: #78350F;
    }}

    .image-container {{
        margin: 14px 0 16px 0;
        page-break-inside: avoid;
        text-align: center;
    }}
    .image-container img {{
        width: 100%;
        max-height: 480px;
        object-fit: contain;
        border-radius: 6px;
        border: 1px solid #CBD5E1;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }}
    .image-caption {{
        font-size: 8.5pt;
        color: #64748B;
        margin-top: 4px;
        font-style: italic;
    }}

    .page-break {{
        page-break-before: always;
    }}

    .badge {{
        display: inline-block;
        padding: 2px 6px;
        font-size: 7.5pt;
        font-weight: 600;
        border-radius: 4px;
        background-color: #E2E8F0;
        color: #334155;
    }}
    .badge-success {{
        background-color: #DCFCE7;
        color: #166534;
    }}
</style>
</head>
<body>

<!-- Header Banner -->
<div class="header-banner">
    <h1>🏏 IPL Performance Analytics Report</h1>
    <p>Comprehensive End-to-End Analytics, Interactive Dashboard & Power BI Implementation</p>
    <div class="meta-grid">
        <div class="meta-item">
            <span>Author / Analyst</span>
            <strong>Aarish Suradkar</strong>
        </div>
        <div class="meta-item">
            <span>Tournament Span</span>
            <strong>17 Seasons (2007/08–2024)</strong>
        </div>
        <div class="meta-item">
            <span>Total Matches</span>
            <strong>1,076 Matches Analyzed</strong>
        </div>
        <div class="meta-item">
            <span>GitHub Repository</span>
            <strong>aarishsuradkar/ipl-analytics</strong>
        </div>
    </div>
</div>

<!-- Section 1: Executive Summary -->
<h2>1. Executive Summary & Project Objectives</h2>
<p>
This project delivered an enterprise-grade interactive sports analytics solution for the Indian Premier League (IPL). Built with <strong>Python, Streamlit, and Plotly</strong>, the dashboard visualizes historical match outcomes, toss impact, individual player milestones, and team phase run rates exported from MySQL 8.0 query results.
</p>
<p>
<strong>Core Project Directives:</strong>
</p>
<ul>
    <li><strong>Mathematical Integrity:</strong> Zero hard-coded figures, estimates, or live database connections. Every metric is computed strictly from exported query CSV files.</li>
    <li><strong>Safe Aggregations:</strong> Strict enforcement of arithmetic mean (never sum) for percentages and rates (win %, run rate, strike rate, economy rate, average first-innings score).</li>
    <li><strong>Full Reproducibility:</strong> End-to-end automated verification script, desktop batch launcher, and complete step-by-step Power BI Desktop build guide.</li>
</ul>

<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-title">Total Matches Played</div>
        <div class="kpi-val">1,076</div>
        <div class="kpi-sub">Verified identically across q3 & q6</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Toss Winner Win %</div>
        <div class="kpi-val">50.9%</div>
        <div class="kpi-sub">548 wins in 1,076 matches</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Leading Run Scorer</div>
        <div class="kpi-val">5,156 Runs</div>
        <div class="kpi-sub">V Kohli (Avg 38.5, SR 127.6)</div>
    </div>
</div>

<!-- Section 2: Data Audit -->
<h2>2. Input Data Audit & Schema Mapping</h2>
<p>
The input data comprises pre-aggregated result CSVs derived from 10 distinct SQL queries. All schemas were audited and reconciled prior to dashboard construction:
</p>

<table>
    <thead>
        <tr>
            <th>Export File</th>
            <th>Original CSV</th>
            <th>Primary Columns</th>
            <th>Data Role & Observations</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>q1_top_scorers</strong></td>
            <td>q1.csv</td>
            <td>season, batter, runs, rnk</td>
            <td>Top 5 scorers per season (60 rows across 12 seasons: 2007/08 to 2019)</td>
        </tr>
        <tr>
            <td><strong>q3_toss_impact</strong></td>
            <td>q3.csv</td>
            <td>toss_decision, matches_played, toss_winner_won, win_pct</td>
            <td>692 field decisions, 384 bat decisions (1,076 matches total)</td>
        </tr>
        <tr>
            <td><strong>q4_phase_run_rate</strong></td>
            <td>q4.csv</td>
            <td>batting_team, phase, run_rate</td>
            <td>Run rates across Powerplay (0-5), Middle (6-14), Death (15-19)</td>
        </tr>
        <tr>
            <td><strong>q5_venue_scores</strong></td>
            <td>q5.csv</td>
            <td>venue, matches_played, avg_first_innings</td>
            <td>19 qualifying venues with at least 10 matches recorded</td>
        </tr>
        <tr>
            <td><strong>q6_team_win_pct</strong></td>
            <td>q6.csv</td>
            <td>season, team, games_played, wins, win_pct</td>
            <td>146 franchise-season records across 17 distinct seasons</td>
        </tr>
        <tr>
            <td><strong>q7_batters</strong></td>
            <td>q7.csv</td>
            <td>batter, runs, balls, strike_rate, batting_avg</td>
            <td>Top 20 all-time batters with minimum 500 balls faced</td>
        </tr>
        <tr>
            <td><strong>q10_death_bowlers</strong></td>
            <td>q10.csv</td>
            <td>bowler, balls, runs, economy</td>
            <td>Top 10 death bowlers (overs 15-20, min 180 balls = 30 overs)</td>
        </tr>
    </tbody>
</table>

<div class="callout">
    <strong>💡 Key Schema & Missing File Reconciliations:</strong><br>
    • <strong>Season Normalization:</strong> In <code>q1</code> and <code>q6</code>, the season field is stored as <code>season</code> (not <code>season_year</code>). It was typed as string to guarantee chronological sorting and prevent summation.<br>
    • <strong>Missing <code>matches_summary.csv</code>:</strong> Because every match involves exactly 2 teams, total matches per season was computed as <code>games_played / 2</code> from <code>q6.csv</code>. The sum across all seasons is exactly <strong>1,076 matches</strong>, proving total parity with <code>q3.csv</code>.<br>
    • <strong>Missing <code>total_runs_by_season.csv</code>:</strong> Handled gracefully via an informative placeholder card on Tab 1 without crashing or inventing figures.
</div>

<div class="page-break"></div>

<!-- Section 3: Visual Walkthrough -->
<h2>3. Dashboard Implementation & Visual Results</h2>

<h3>3.1 Tab 1: Tournament Overview & Toss Impact</h3>
<p>
Focuses on macro-level operational metrics across 17 IPL seasons and evaluates whether winning the toss confers a competitive advantage.
</p>

<div class="image-container">
    <img src="{img_overview}" alt="Overview Tab Screenshot">
    <div class="image-caption">Figure 1: Tab 1 — Tournament Overview, Season Match Trajectory & Toss Impact Win Rates</div>
</div>

<div class="callout">
    <strong>📊 Tab 1 Key Takeaways:</strong><br>
    • <strong>Tournament Expansion:</strong> Matches per season grew from 58 in 2007/08 to peak tournament sizes of 74 matches (2012, 2013, 2022) and 71 matches in 2024.<br>
    • <strong>Field First Advantage:</strong> Teams winning the toss won <strong>50.9%</strong> of matches overall. However, choosing to <strong>field</strong> yielded a <strong>54.0% win rate</strong> (374 wins in 692 matches) compared to only <strong>45.3%</strong> when electing to bat (174 wins in 384 matches) — an <strong>8.7 percentage point swing</strong>.
</div>

<div class="page-break"></div>

<h3>3.2 Tab 2: Player Performance & Death Bowling Milestones</h3>
<p>
Analyzes individual batter consistency across seasons and defensive death-over bowling mastery under high-leverage situations.
</p>

<div class="image-container">
    <img src="{img_players}" alt="Players Tab Screenshot">
    <div class="image-caption">Figure 2: Tab 2 — Top Run Scorers Slicer, Death Bowlers Economy & All-Time Batters Table</div>
</div>

<div class="callout">
    <strong>🏏 Tab 2 Key Takeaways:</strong><br>
    • <strong>Leading Aggregator:</strong> In cumulative season top-5 ranks (2007/08–2019), <strong>DA Warner</strong> leads with <strong>2,928 runs</strong>, followed by <strong>CH Gayle</strong> (2,515 runs) and <strong>SK Raina</strong> (2,451 runs).<br>
    • <strong>Career Run Leader:</strong> <strong>V Kohli</strong> leads all qualifiers with <strong>5,156 runs</strong> in 4,042 balls (avg 38.5, SR 127.6).<br>
    • <strong>Maximum Strike Rate:</strong> <strong>V Sehwag</strong> recorded the highest career strike rate at <strong>148.8</strong> (2,728 runs off 1,833 balls).<br>
    • <strong>Death Bowling Excellence:</strong> <strong>DE Bollinger</strong> delivered the most economical death bowling rate at <strong>7.36 RPO</strong> (242 balls, 297 runs), closely trailed by <strong>SP Narine</strong> at <strong>7.38 RPO</strong> (768 balls, 944 runs).
</div>

<div class="page-break"></div>

<h3>3.3 Tab 3: Franchise Dynamics & Venue Scoring Profiles</h3>
<p>
Examines franchise win percentage trajectories across seasons, average first-innings scoring behavior by stadium, and phase-by-phase scoring acceleration.
</p>

<div class="image-container">
    <img src="{img_teams}" alt="Teams & Venues Tab Screenshot">
    <div class="image-caption">Figure 3: Tab 3 — Franchise Win % Multi-line Chart, Venue Scoring Extremes & Phase Run Rates</div>
</div>

<div class="callout">
    <strong>🏟️ Tab 3 Key Takeaways:</strong><br>
    • <strong>Most Active Franchises:</strong> <strong>Mumbai Indians</strong> (257 games), <strong>Kolkata Knight Riders</strong> (247 games), and <strong>Delhi Capitals</strong> (246 games).<br>
    • <strong>Venue Scoring Extremes:</strong> Bangalore's <strong>M.Chinnaswamy Stadium</strong> recorded the highest 1st innings average at <strong>182.6</strong>, while Navi Mumbai's <strong>Dr DY Patil Sports Academy</strong> was the most bowler-friendly at <strong>146.6</strong>.<br>
    • <strong>Death Phase Explosion:</strong> Scoring accelerates dramatically from Powerplay (~7.4 RPO) into the Death overs (overs 15–20), led by <strong>Royal Challengers Bangalore</strong> at <strong>10.00 RPO</strong> and <strong>Chennai Super Kings</strong> at <strong>9.80 RPO</strong>.
</div>

<div class="page-break"></div>

<!-- Section 4: Verification & Power BI -->
<h2>4. Verification Audit & Power BI Architecture</h2>

<h3>4.1 Mathematical Integrity Audit (`verify_dashboard.py`)</h3>
<p>
An automated verification test was executed against all source CSV files. Every figure reported on the dashboard matched the raw data with zero rounding discrepancies:
</p>

<table>
    <thead>
        <tr>
            <th>Metric Audited</th>
            <th>Source CSV Field</th>
            <th>Computed Value</th>
            <th>Aggregation Method</th>
            <th>Integrity Check</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Total Matches</td>
            <td>q3[matches_played]</td>
            <td>1,076</td>
            <td>Sum</td>
            <td><span class="badge badge-success">EXACT MATCH</span></td>
        </tr>
        <tr>
            <td>Derived Matches</td>
            <td>q6[games_played] / 2</td>
            <td>1,076</td>
            <td>Sum / 2</td>
            <td><span class="badge badge-success">EXACT MATCH</span></td>
        </tr>
        <tr>
            <td>Fielding Toss Win %</td>
            <td>q3[win_pct]</td>
            <td>54.0%</td>
            <td>Arithmetic Mean</td>
            <td><span class="badge badge-success">EXACT MATCH</span></td>
        </tr>
        <tr>
            <td>Batting Toss Win %</td>
            <td>q3[win_pct]</td>
            <td>45.3%</td>
            <td>Arithmetic Mean</td>
            <td><span class="badge badge-success">EXACT MATCH</span></td>
        </tr>
        <tr>
            <td>Best Strike Rate</td>
            <td>q7[strike_rate]</td>
            <td>148.83</td>
            <td>Direct Rate</td>
            <td><span class="badge badge-success">EXACT MATCH</span></td>
        </tr>
        <tr>
            <td>Best Death Economy</td>
            <td>q10[economy]</td>
            <td>7.36</td>
            <td>Direct Rate</td>
            <td><span class="badge badge-success">EXACT MATCH</span></td>
        </tr>
        <tr>
            <td>Highest Venue Score</td>
            <td>q5[avg_first_innings]</td>
            <td>182.6</td>
            <td>Direct Rate</td>
            <td><span class="badge badge-success">EXACT MATCH</span></td>
        </tr>
    </tbody>
</table>

<h3>4.2 Power BI Desktop Specifications (`powerbi_build_guide.md`)</h3>
<p>
To build the identical 3-page reporting suite in Power BI Desktop, the following modeling rules must be observed:
</p>
<ul>
    <li><strong>Data Types:</strong> <code>season</code> must be explicitly typed as <strong>Text</strong> in Power Query to prevent automatic summation. All rate fields must be typed as <strong>Decimal Number</strong>.</li>
    <li><strong>Explicit DAX Measures:</strong> Always use explicit DAX measures rather than default canvas summarizations:
        <pre style="background:#F1F5F9; padding:8px; border-radius:4px; font-size:8.5pt;">Total Matches      = SUM(q3_toss_impact[matches_played])
Matches from Teams = SUM(q6_team_win_pct[games_played]) / 2
Avg Toss Win Pct   = AVERAGE(q3_toss_impact[win_pct])
Avg Death Economy  = AVERAGE(q10_death_bowlers[economy])</pre>
    </li>
    <li><strong>Sorting Direction:</strong> Sort batters by runs <strong>descending</strong>; sort death bowlers by economy <strong>ascending</strong> (lowest economy is best).</li>
</ul>

<!-- Section 5: Repository & Deliverables -->
<h2>5. Repository Architecture & Deliverables</h2>
<p>
The project is published and tracked under Git version control at <strong><a href="https://github.com/aarishsuradkar/ipl-analytics" style="color:#1E3A8A;">github.com/aarishsuradkar/ipl-analytics</a></strong>:
</p>

<table>
    <thead>
        <tr>
            <th>Deliverable</th>
            <th>Filename</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Interactive Application</td>
            <td><code>app.py</code></td>
            <td>Wide-layout Streamlit + Plotly interactive dashboard</td>
        </tr>
        <tr>
            <td>One-Click Launcher</td>
            <td><code>run_dashboard.bat</code></td>
            <td>Automated Windows launcher (opens browser on localhost:8501)</td>
        </tr>
        <tr>
            <td>Power BI Build Guide</td>
            <td><code>powerbi_build_guide.md</code></td>
            <td>Complete step-by-step visual specification and DAX measures</td>
        </tr>
        <tr>
            <td>Verification Engine</td>
            <td><code>verify_dashboard.py</code></td>
            <td>Automated math verification and integrity audit script</td>
        </tr>
        <tr>
            <td>Repository Report</td>
            <td><code>PROJECT_REPORT.md</code></td>
            <td>Native markdown report with relative screenshot embeddings</td>
        </tr>
        <tr>
            <td>PDF Report</td>
            <td><code>IPL_Performance_Analytics_Report.pdf</code></td>
            <td>Printable executive PDF document</td>
        </tr>
    </tbody>
</table>

<div class="callout" style="text-align: center; margin-top: 24px;">
    <strong>IPL Performance Analytics Project</strong> • Built from MySQL Query Outputs • All Rights Reserved
</div>

</body>
</html>
"""

html_path = os.path.join(BASE_DIR, "report.html")
pdf_dest_project = os.path.join(BASE_DIR, "IPL_Performance_Analytics_Report.pdf")
pdf_dest_artifact = os.path.join(ARTIFACT_DIR, "IPL_Performance_Analytics_Report.pdf")

print("Writing report HTML...")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generating PDF with Chrome headless: {CHROME_PATH}...")
cmd = [
    CHROME_PATH,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_dest_project}",
    html_path
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Chrome exit code:", res.returncode)

if os.path.exists(pdf_dest_project):
    size = os.path.getsize(pdf_dest_project)
    print(f"PDF generated successfully: {pdf_dest_project} ({size:,} bytes)")
    
    # Copy to artifact directory
    import shutil
    shutil.copyfile(pdf_dest_project, pdf_dest_artifact)
    print(f"Copied to artifact dir: {pdf_dest_artifact}")
else:
    print("PDF generation failed!")
