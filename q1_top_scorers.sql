-- =====================================================================
-- IPL Performance Analytics - 10 queries (MySQL 8.0+)
-- Assumes tables: matches(id, season, match_date, venue, team1, team2,
--   toss_winner, toss_decision, winner, player_of_match)
-- and deliveries(match_id, inning, batting_team, bowling_team, over_no,
--   batter, bowler, batsman_runs, total_runs, is_wicket,
--   player_dismissed, dismissal_kind)
-- If a column name differs in your data, change it here.
-- Run one query at a time (select it, then Ctrl+Enter).
-- =====================================================================
USE ipl;

-- ---------------------------------------------------------------------
-- 1. Top 5 run scorers per season  (CTE + RANK window function)
-- ---------------------------------------------------------------------
WITH season_runs AS (
  SELECT m.season, d.batter, SUM(d.batsman_runs) AS runs
  FROM deliveries d
  JOIN matches m ON d.match_id = m.id
  GROUP BY m.season, d.batter
), ranked AS (
  SELECT season, batter, runs,
         RANK() OVER (PARTITION BY season ORDER BY runs DESC) AS rnk
  FROM season_runs
)
SELECT * FROM ranked WHERE rnk <= 5 ORDER BY season, rnk;