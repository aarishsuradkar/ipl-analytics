USE ipl;
-- ---------------------------------------------------------------------
-- 7. Batter runs, strike rate and average (min 500 balls)
-- ---------------------------------------------------------------------
SELECT batter,
       SUM(batsman_runs) AS runs,
       COUNT(*) AS balls,
       ROUND(100.0 * SUM(batsman_runs) / COUNT(*), 2) AS strike_rate,
       ROUND(SUM(batsman_runs) /
             NULLIF(SUM(CASE WHEN player_dismissed = batter THEN 1 ELSE 0 END), 0), 2) AS batting_avg
FROM deliveries
GROUP BY batter
HAVING COUNT(*) >= 500
ORDER BY runs DESC
LIMIT 20;
