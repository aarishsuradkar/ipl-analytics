USE ipl;
- ---------------------------------------------------------------------
-- 6. Team win % by season  (multiple CTEs, UNION ALL, LEFT JOIN)
-- ---------------------------------------------------------------------
WITH played AS (
  SELECT season, team1 AS team FROM matches
  UNION ALL
  SELECT season, team2 FROM matches
), games AS (
  SELECT season, team, COUNT(*) AS games_played
  FROM played
  GROUP BY season, team
), wins AS (
  SELECT season, winner AS team, COUNT(*) AS win_count
  FROM matches
  WHERE winner IS NOT NULL AND winner <> ''
  GROUP BY season, winner
)
SELECT g.season, g.team, g.games_played,
       COALESCE(w.win_count, 0) AS wins,
       ROUND(100.0 * COALESCE(w.win_count, 0) / g.games_played, 1) AS win_pct
FROM games g
LEFT JOIN wins w ON g.season = w.season AND g.team = w.team
ORDER BY g.season, win_pct DESC;
