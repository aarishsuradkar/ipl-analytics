import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# Configuration and Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="IPL Performance Analytics Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling Palette (Deep IPL Navy, Cricket Gold, Royal Blue, Coral)
PRIMARY_COLOR = "#1E3A8A"
ACCENT_GOLD = "#F59E0B"
ACCENT_BLUE = "#3B82F6"
ACCENT_CORAL = "#EF4444"
CHART_PALETTE = ["#1E3A8A", "#3B82F6", "#F59E0B", "#10B981", "#8B5CF6", "#EC4899", "#6366F1"]

st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.0rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
        padding: 1.2rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .kpi-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        opacity: 0.9;
        margin-bottom: 0.3rem;
    }
    .kpi-value {
        font-size: 2.0rem;
        font-weight: 700;
    }
    .kpi-caption {
        font-size: 0.75rem;
        opacity: 0.8;
        margin-top: 0.3rem;
    }
    .insight-card {
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        padding: 1rem 1.25rem;
        border-radius: 6px;
        color: #92400E;
        font-size: 0.95rem;
        margin: 1.2rem 0;
        line-height: 1.5;
    }
    .footer-note {
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #E5E7EB;
        font-size: 0.85rem;
        color: #6B7280;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Data Loader Utilities
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def find_file(filename_variants):
    """Search for a file across output/, question sql/, and root directory."""
    search_dirs = [
        os.path.join(BASE_DIR, "output"),
        os.path.join(BASE_DIR, "question sql"),
        BASE_DIR
    ]
    for directory in search_dirs:
        for name in filename_variants:
            candidate = os.path.join(directory, name)
            if os.path.exists(candidate):
                return candidate
    return None

@st.cache_data
def load_all_data():
    """Load and normalize datasets from CSV outputs with robust error handling."""
    data = {}
    
    # 1. q1_top_scorers
    f_q1 = find_file(["q1_top_scorers.csv", "q1.csv"])
    if f_q1:
        df = pd.read_csv(f_q1, dtype={"season": str, "season_year": str})
        if "season_year" in df.columns and "season" not in df.columns:
            df.rename(columns={"season_year": "season"}, inplace=True)
        data["q1"] = df
    else:
        data["q1"] = None

    # 2. q3_toss_impact
    f_q3 = find_file(["q3_toss_impact.csv", "q3.csv"])
    if f_q3:
        data["q3"] = pd.read_csv(f_q3)
    else:
        data["q3"] = None

    # 3. q4_phase_run_rate
    f_q4 = find_file(["q4_phase_run_rate.csv", "q4.csv"])
    if f_q4:
        data["q4"] = pd.read_csv(f_q4)
    else:
        data["q4"] = None

    # 4. q5_venue_scores
    f_q5 = find_file(["q5_venue_scores.csv", "q5.csv"])
    if f_q5:
        data["q5"] = pd.read_csv(f_q5)
    else:
        data["q5"] = None

    # 5. q6_team_win_pct
    f_q6 = find_file(["q6_team_win_pct.csv", "q6.csv"])
    if f_q6:
        df = pd.read_csv(f_q6, dtype={"season": str, "season_year": str})
        if "season_year" in df.columns and "season" not in df.columns:
            df.rename(columns={"season_year": "season"}, inplace=True)
        data["q6"] = df
    else:
        data["q6"] = None

    # 6. q7_batters
    f_q7 = find_file(["q7_batters.csv", "q7.csv"])
    if f_q7:
        data["q7"] = pd.read_csv(f_q7)
    else:
        data["q7"] = None

    # 7. q10_death_bowlers
    f_q10 = find_file(["q10_death_bowlers.csv", "q10.csv"])
    if f_q10:
        data["q10"] = pd.read_csv(f_q10)
    else:
        data["q10"] = None

    # 8. matches_summary (Optional / Fallback)
    f_matches = find_file(["matches_summary.csv"])
    if f_matches:
        df = pd.read_csv(f_matches, dtype={"season_year": str, "season": str})
        if "season" in df.columns and "season_year" not in df.columns:
            df.rename(columns={"season": "season_year"}, inplace=True)
        data["matches_summary"] = df
    else:
        data["matches_summary"] = None

    # 9. total_runs_by_season (Optional / Fallback)
    f_runs = find_file(["total_runs_by_season.csv"])
    if f_runs:
        df = pd.read_csv(f_runs, dtype={"season_year": str, "season": str})
        if "season" in df.columns and "season_year" not in df.columns:
            df.rename(columns={"season": "season_year"}, inplace=True)
        data["total_runs_by_season"] = df
    else:
        data["total_runs_by_season"] = None

    # 10. q8_cumulative_runs (Optional)
    f_q8 = find_file(["q8_cumulative_runs.csv", "q8.csv"])
    if f_q8:
        data["q8"] = pd.read_csv(f_q8)
    else:
        data["q8"] = None

    return data

data = load_all_data()

# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------
st.markdown('<div class="main-title">🏏 IPL Performance Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Interactive analysis built directly from exported MySQL query results across IPL tournaments.</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 Overview", "👤 Players", "🏟️ Teams & Venues"])

# =============================================================================
# TAB 1: OVERVIEW
# =============================================================================
with tab1:
    st.subheader("Tournament Overview & Toss Impact")

    # Derived or loaded metrics
    matches_df = data["matches_summary"]
    runs_df = data["total_runs_by_season"]
    q6_df = data["q6"]
    q3_df = data["q3"]

    # Compute matches per season and total matches
    if matches_df is not None:
        total_matches = int(matches_df["matches_played"].sum())
        season_matches = matches_df.rename(columns={"season_year": "season"})
        matches_source_note = "matches_summary.csv"
    elif q6_df is not None:
        # Each match has 2 teams participating; sum(games_played) / 2 equals total matches
        season_matches = q6_df.groupby("season", as_index=False)["games_played"].sum()
        season_matches["matches_played"] = (season_matches["games_played"] // 2).astype(int)
        total_matches = int(season_matches["matches_played"].sum())
        matches_source_note = "Computed from q6 (games_played / 2)"
    elif q3_df is not None:
        total_matches = int(q3_df["matches_played"].sum())
        season_matches = None
        matches_source_note = "Computed from q3 (toss matches)"
    else:
        total_matches = 0
        season_matches = None
        matches_source_note = "Not available"

    # Total runs
    if runs_df is not None:
        total_runs_val = f"{int(runs_df['total_runs'].sum()):,}"
    else:
        total_runs_val = "Not exported"

    # Number of seasons
    if q6_df is not None:
        num_seasons = q6_df["season"].nunique()
    elif season_matches is not None:
        num_seasons = season_matches["season"].nunique()
    elif data["q1"] is not None:
        num_seasons = data["q1"]["season"].nunique()
    else:
        num_seasons = 0

    # KPI Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Matches Played</div>
            <div class="kpi-value">{total_matches:,}</div>
            <div class="kpi-caption">{matches_source_note}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Tournament Runs</div>
            <div class="kpi-value">{total_runs_val}</div>
            <div class="kpi-caption">{"From total_runs_by_season.csv" if runs_df is not None else "Requires total_runs_by_season.csv"}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Tournaments Covered</div>
            <div class="kpi-value">{num_seasons}</div>
            <div class="kpi-caption">Seasons recorded in dataset</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts Row: Matches per season & Total Runs per season
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        if season_matches is not None:
            # Sort seasons chronologically as string
            season_matches["season"] = season_matches["season"].astype(str)
            fig_m = px.bar(
                season_matches,
                x="season",
                y="matches_played",
                title="Matches Played per Season",
                labels={"season": "Season", "matches_played": "Matches Played"},
                text="matches_played",
                color_discrete_sequence=[PRIMARY_COLOR]
            )
            fig_m.update_traces(textposition="outside", cliponaxis=False)
            fig_m.update_layout(
                xaxis_type="category",
                margin=dict(t=40, b=40, l=40, r=20),
                hovermode="x unified",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_m, use_container_width=True)
        else:
            st.info("Matches per season dataset is not available.")

    with col_c2:
        if runs_df is not None:
            runs_df["season_year"] = runs_df["season_year"].astype(str)
            fig_r = px.bar(
                runs_df,
                x="season_year",
                y="total_runs",
                title="Total Runs Scored per Season",
                labels={"season_year": "Season", "total_runs": "Total Runs"},
                text="total_runs",
                color_discrete_sequence=[ACCENT_GOLD]
            )
            fig_r.update_traces(textposition="outside", cliponaxis=False)
            fig_r.update_layout(
                xaxis_type="category",
                margin=dict(t=40, b=40, l=40, r=20),
                hovermode="x unified",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_r, use_container_width=True)
        else:
            st.info("ℹ️ **Total Runs by Season**: The file `total_runs_by_season.csv` is not present among the exported query outputs. To display this chart, export `season_year, total_runs` to `output/total_runs_by_season.csv`.")

    # Toss Impact Analysis from q3
    st.markdown("---")
    st.subheader("Toss Impact Analysis")
    if q3_df is not None:
        # Use mean of win_pct (prompt rule: never sum percentage or rate)
        toss_summary = q3_df.groupby("toss_decision", as_index=False).agg({
            "matches_played": "sum",
            "toss_winner_won": "sum",
            "win_pct": "mean"
        })

        # Chart: Toss Decision vs Win %
        fig_toss = px.bar(
            toss_summary,
            x="toss_decision",
            y="win_pct",
            title="Toss Winner Match Win Rate by Decision",
            labels={"toss_decision": "Toss Decision", "win_pct": "Match Win Rate (%)"},
            text=toss_summary["win_pct"].apply(lambda v: f"{v:.1f}%"),
            color="toss_decision",
            color_discrete_map={"field": ACCENT_BLUE, "bat": PRIMARY_COLOR}
        )
        fig_toss.update_traces(
            textposition="outside",
            cliponaxis=False,
            hovertemplate="<b>Toss Decision: %{x}</b><br>Win Rate: %{y:.1f}%<extra></extra>"
        )
        fig_toss.update_layout(
            yaxis_range=[0, 100],
            showlegend=False,
            margin=dict(t=40, b=40, l=40, r=20),
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_toss, use_container_width=True)

        # Computed Insight Box
        total_toss_matches = int(q3_df["matches_played"].sum())
        total_toss_won = int(q3_df["toss_winner_won"].sum())
        overall_toss_win_pct = (total_toss_won / total_toss_matches * 100.0) if total_toss_matches > 0 else 0.0

        higher_row = toss_summary.loc[toss_summary["win_pct"].idxmax()]
        lower_row = toss_summary.loc[toss_summary["win_pct"].idxmin()]

        st.markdown(f"""
        <div class="insight-card">
            💡 <b>Key Finding:</b> Toss winners won <b>{overall_toss_win_pct:.1f}%</b> of matches ({total_toss_won:,} of {total_toss_matches:,} matches). 
            Teams had a markedly higher win rate when choosing to <b>{higher_row['toss_decision']}</b> (<b>{higher_row['win_pct']:.1f}%</b> win rate across {int(higher_row['matches_played']):,} matches) 
            compared to choosing to <b>{lower_row['toss_decision']}</b> (<b>{lower_row['win_pct']:.1f}%</b> across {int(lower_row['matches_played']):,} matches).
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("q3_toss_impact dataset not found.")

# =============================================================================
# TAB 2: PLAYERS
# =============================================================================
with tab2:
    st.subheader("Player Performance & Milestones")

    q1_df = data["q1"]
    q7_df = data["q7"]
    q10_df = data["q10"]

    col_p1, col_p2 = st.columns([1, 1])

    with col_p1:
        st.markdown("#### Top Run Scorers")
        if q1_df is not None:
            # Treat season as string
            q1_df["season"] = q1_df["season"].astype(str)
            seasons_available = sorted(q1_df["season"].unique().tolist())
            season_options = ["All seasons"] + seasons_available

            selected_season = st.selectbox(
                "Select Season:",
                options=season_options,
                index=0,
                key="player_season_select"
            )

            if selected_season == "All seasons":
                top_scorers = (
                    q1_df.groupby("batter", as_index=False)["runs"]
                    .sum()
                    .sort_values(by="runs", ascending=True)
                    .tail(10)
                )
                chart_title = "Top 10 Run Scorers (Cumulative Across All Recorded Seasons)"
            else:
                top_scorers = (
                    q1_df[q1_df["season"] == selected_season]
                    .sort_values(by="runs", ascending=True)
                )
                chart_title = f"Top Run Scorers in Season {selected_season}"

            fig_p = px.bar(
                top_scorers,
                x="runs",
                y="batter",
                orientation="h",
                title=chart_title,
                labels={"runs": "Runs Scored", "batter": "Batter"},
                text="runs",
                color_discrete_sequence=[ACCENT_BLUE]
            )
            fig_p.update_traces(
                textposition="outside",
                cliponaxis=False,
                hovertemplate="<b>%{y}</b><br>Runs: %{x:,}<extra></extra>"
            )
            fig_p.update_layout(
                margin=dict(t=40, b=40, l=100, r=40),
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_p, use_container_width=True)
        else:
            st.warning("q1_top_scorers dataset not found.")

    with col_p2:
        st.markdown("#### Best Death-Over Bowlers (Overs 15-20)")
        if q10_df is not None:
            # Sort ascending: lowest economy at the top (best at top)
            top10_bowlers = q10_df.sort_values(by="economy", ascending=False).tail(10)
            
            fig_b = px.bar(
                top10_bowlers,
                x="economy",
                y="bowler",
                orientation="h",
                title="Top 10 Death Bowlers by Economy Rate (Min 180 balls)",
                labels={"economy": "Economy Rate (Runs/Over)", "bowler": "Bowler"},
                text=top10_bowlers["economy"].apply(lambda v: f"{v:.2f}"),
                color_discrete_sequence=[PRIMARY_COLOR]
            )
            fig_b.update_traces(
                textposition="outside",
                cliponaxis=False,
                hovertemplate="<b>%{y}</b><br>Economy: %{x:.2f}<br>Balls: %{customdata[0]}<br>Runs Conceded: %{customdata[1]}<extra></extra>",
                customdata=top10_bowlers[["balls", "runs"]]
            )
            fig_b.update_layout(
                margin=dict(t=40, b=40, l=100, r=40),
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_b, use_container_width=True)
        else:
            st.warning("q10_death_bowlers dataset not found.")

    # Computed Insight Sentence for Players
    if q7_df is not None and q10_df is not None:
        best_sr_row = q7_df.loc[q7_df["strike_rate"].idxmax()]
        best_econ_row = q10_df.loc[q10_df["economy"].idxmin()]
        top_run_row = q7_df.loc[q7_df["runs"].idxmax()]

        st.markdown(f"""
        <div class="insight-card">
            💡 <b>Player Insight:</b> Among listed top batters (min 500 balls), <b>{best_sr_row['batter']}</b> holds the highest strike rate at <b>{best_sr_row['strike_rate']:.1f}</b> ({best_sr_row['runs']:,} runs off {best_sr_row['balls']:,} balls), 
            while <b>{top_run_row['batter']}</b> leads in total runs with <b>{top_run_row['runs']:,} runs</b> (avg {top_run_row['batting_avg']:.1f}). 
            In the death overs (overs 15–20), <b>{best_econ_row['bowler']}</b> delivered the best economy rate at <b>{best_econ_row['economy']:.2f} RPO</b> over {best_econ_row['balls']:,} balls.
        </div>
        """, unsafe_allow_html=True)

    # Detailed Table from q7
    st.markdown("---")
    st.markdown("#### All-Time Leading Batters Performance (Min 500 Balls)")
    if q7_df is not None:
        table_df = q7_df.sort_values(by="runs", ascending=False).copy()
        
        # Display with number formatting
        formatted_table = table_df.copy()
        formatted_table["runs"] = formatted_table["runs"].apply(lambda x: f"{x:,}")
        formatted_table["balls"] = formatted_table["balls"].apply(lambda x: f"{x:,}")
        formatted_table["strike_rate"] = formatted_table["strike_rate"].apply(lambda x: f"{x:.1f}")
        formatted_table["batting_avg"] = formatted_table["batting_avg"].apply(lambda x: f"{x:.1f}")
        
        formatted_table.rename(columns={
            "batter": "Batter",
            "runs": "Runs",
            "balls": "Balls Faced",
            "strike_rate": "Strike Rate",
            "batting_avg": "Batting Average"
        }, inplace=True)
        
        st.dataframe(formatted_table, use_container_width=True, hide_index=True)
    else:
        st.warning("q7_batters dataset not found.")

# =============================================================================
# TAB 3: TEAMS AND VENUES
# =============================================================================
with tab3:
    st.subheader("Team Consistency & Venue Scoring Dynamics")

    q4_df = data["q4"]
    q5_df = data["q5"]
    q6_df = data["q6"]

    # 1. Team Win % by Season
    st.markdown("#### Team Win Percentage Across Seasons")
    if q6_df is not None:
        q6_df["season"] = q6_df["season"].astype(str)
        # Compute default: 3 teams with most games played
        team_games_total = q6_df.groupby("team")["games_played"].sum().sort_values(ascending=False)
        default_teams = team_games_total.head(3).index.tolist()
        all_teams = sorted(q6_df["team"].unique().tolist())

        selected_teams = st.multiselect(
            "Select Teams to Compare:",
            options=all_teams,
            default=default_teams,
            key="team_multiselect"
        )

        if selected_teams:
            filtered_q6 = q6_df[q6_df["team"].isin(selected_teams)].copy()
            # Sort chronologically by season
            filtered_q6.sort_values(by=["team", "season"], inplace=True)

            fig_line = px.line(
                filtered_q6,
                x="season",
                y="win_pct",
                color="team",
                markers=True,
                title="Season-by-Season Match Win % by Team",
                labels={"season": "Season", "win_pct": "Win Percentage (%)", "team": "Team"},
                color_discrete_sequence=CHART_PALETTE
            )
            fig_line.update_traces(
                hovertemplate="<b>%{data.name}</b><br>Season: %{x}<br>Win Rate: %{y:.1f}%<extra></extra>"
            )
            fig_line.update_layout(
                xaxis_type="category",
                yaxis_range=[0, 100],
                hovermode="x unified",
                margin=dict(t=40, b=40, l=40, r=20),
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("Please select at least one team to display the trend line.")
    else:
        st.warning("q6_team_win_pct dataset not found.")

    st.markdown("---")
    col_t1, col_t2 = st.columns([1, 1])

    # 2. Venue Scores (q5)
    with col_t1:
        st.markdown("#### Venue Scoring Profile (1st Innings Average)")
        if q5_df is not None:
            view_mode = st.radio(
                "Filter Venues:",
                options=["Top 10 Highest Scoring", "Bottom 10 Lowest Scoring"],
                horizontal=True,
                key="venue_filter_mode"
            )

            if view_mode == "Top 10 Highest Scoring":
                venue_data = q5_df.sort_values(by="avg_first_innings", ascending=True).tail(10)
                venue_title = "Top 10 Highest Average 1st Innings Scores"
            else:
                venue_data = q5_df.sort_values(by="avg_first_innings", ascending=False).tail(10)
                venue_title = "Bottom 10 Lowest Average 1st Innings Scores"

            fig_v = px.bar(
                venue_data,
                x="avg_first_innings",
                y="venue",
                orientation="h",
                title=venue_title,
                labels={"avg_first_innings": "Avg 1st Innings Score", "venue": "Venue"},
                text=venue_data["avg_first_innings"].apply(lambda v: f"{v:.1f}"),
                color_discrete_sequence=[PRIMARY_COLOR]
            )
            fig_v.update_traces(
                textposition="outside",
                cliponaxis=False,
                hovertemplate="<b>%{y}</b><br>Avg 1st Innings: %{x:.1f}<br>Matches Played: %{customdata}<extra></extra>",
                customdata=venue_data["matches_played"]
            )
            fig_v.update_layout(
                margin=dict(t=40, b=40, l=140, r=40),
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_v, use_container_width=True)
        else:
            st.warning("q5_venue_scores dataset not found.")

    # 3. Phase Run Rate (q4)
    with col_t2:
        st.markdown("#### Run Rate by Match Phase")
        if q4_df is not None:
            # Multiselect for phase teams
            available_phase_teams = sorted(q4_df["batting_team"].unique().tolist())
            # Default to top teams from q6 or first 4
            default_phase_teams = available_phase_teams[:5]
            if q6_df is not None:
                q6_top5 = q6_df.groupby("team")["games_played"].sum().sort_values(ascending=False).head(5).index.tolist()
                default_phase_teams = [t for t in q6_top5 if t in available_phase_teams]

            selected_phase_teams = st.multiselect(
                "Filter Teams by Phase Run Rate:",
                options=available_phase_teams,
                default=default_phase_teams,
                key="phase_team_select"
            )

            if selected_phase_teams:
                filtered_q4 = q4_df[q4_df["batting_team"].isin(selected_phase_teams)].copy()
                
                # Order phases chronologically: Powerplay, Middle, Death
                phase_order = ["Powerplay", "Middle", "Death"]
                filtered_q4["phase"] = pd.Categorical(filtered_q4["phase"], categories=phase_order, ordered=True)
                filtered_q4.sort_values(by=["batting_team", "phase"], inplace=True)

                fig_phase = px.bar(
                    filtered_q4,
                    x="batting_team",
                    y="run_rate",
                    color="phase",
                    barmode="group",
                    title="Run Rate by Phase (Powerplay / Middle / Death)",
                    labels={"batting_team": "Team", "run_rate": "Run Rate (Runs/Over)", "phase": "Phase"},
                    category_orders={"phase": phase_order},
                    color_discrete_map={"Powerplay": ACCENT_BLUE, "Middle": PRIMARY_COLOR, "Death": ACCENT_GOLD}
                )
                fig_phase.update_traces(
                    hovertemplate="<b>%{x}</b><br>Phase: %{data.name}<br>Run Rate: %{y:.1f}<extra></extra>"
                )
                fig_phase.update_layout(
                    margin=dict(t=40, b=40, l=40, r=20),
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis_tickangle=-30
                )
                st.plotly_chart(fig_phase, use_container_width=True)
            else:
                st.info("Select at least one team to display phase run rates.")
        else:
            st.warning("q4_phase_run_rate dataset not found.")

    # Computed Insight Sentence for Teams & Venues
    if q5_df is not None and q4_df is not None:
        h_venue = q5_df.loc[q5_df["avg_first_innings"].idxmax()]
        l_venue = q5_df.loc[q5_df["avg_first_innings"].idxmin()]
        death_phases = q4_df[q4_df["phase"] == "Death"]
        h_death_team = death_phases.loc[death_phases["run_rate"].idxmax()]

        st.markdown(f"""
        <div class="insight-card">
            💡 <b>Venue & Phase Insight:</b> Across all venues (min 10 matches), <b>{h_venue['venue']}</b> recorded the highest scoring first innings at <b>{h_venue['avg_first_innings']:.1f}</b>, 
            while <b>{l_venue['venue']}</b> registered the lowest at <b>{l_venue['avg_first_innings']:.1f}</b>. 
            In the death overs, <b>{h_death_team['batting_team']}</b> accelerated with the highest death run rate at <b>{h_death_team['run_rate']:.1f} RPO</b>.
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Footer Note
# -----------------------------------------------------------------------------
st.markdown("""
<div class="footer-note">
    Built from SQL query outputs (MySQL). Run rate counts wides and no-balls as balls, so it is approximate.
</div>
""", unsafe_allow_html=True)
