USE ipl;
- ---------------------------------------------------------------------
-- 5. Average first-innings score by venue (min 10 matches)  (CTE + JOIN)
-- ---------------------------------------------------------------------
WITH inns AS (
  SELECT match_id, SUM(total_runs) AS score
  FROM deliveries
  WHERE inning = 1
  GROUP BY match_id
)
SELECT m.venue,
       COUNT(*) AS matches_played,
       ROUND(AVG(i.score), 1) AS avg_first_innings
FROM inns i
JOIN matches m ON i.match_id = m.id
GROUP BY m.venue
HAVING COUNT(*) >= 10
ORDER BY avg_first_innings DESC;
