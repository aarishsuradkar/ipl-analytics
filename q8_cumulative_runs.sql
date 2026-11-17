use ipl;
-- SELECT m.season, COUNT(DISTINCT d.match_id) AS matches_found
-- FROM deliveries d
-- JOIN matches m ON d.match_id = m.id
-- WHERE d.batting_team = 'Chennai Super Kings'
-- GROUP BY m.season
-- ORDER BY m.season;

-- - ---------------------------------------------------------------------
-- 8. Cumulative runs through a season for one team  (window SUM OVER)
--    Change the team and season. If season is stored as a number, use 2023 without quotes.
-- ---------------------------------------------------------------------
WITH match_runs AS (
  SELECT m.match_date, d.match_id, SUM(d.total_runs) AS runs
  FROM deliveries d
  JOIN matches m ON d.match_id = m.id
  WHERE d.batting_team = 'Chennai Super Kings'
    AND m.season = '2015'
  GROUP BY d.match_id, m.match_date
)
SELECT match_date, runs,
       SUM(runs) OVER (ORDER BY match_date) AS cumulative_runs
FROM match_runs
ORDER BY match_date;