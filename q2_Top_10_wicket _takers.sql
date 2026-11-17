USE ipl;
-- ---------------------------------------------------------------------
-- 2. Top 10 wicket takers (bowler wickets only)
-- ---------------------------------------------------------------------
SELECT bowler, COUNT(*) AS wickets
FROM deliveries
WHERE is_wicket = 1
  AND dismissal_kind NOT IN ('run out','retired hurt','retired out','obstructing the field')
GROUP BY bowler
ORDER BY wickets DESC
LIMIT 10;
