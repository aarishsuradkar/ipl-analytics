-- - ---------------------------------------------------------------------
-- 10. Best death-over bowlers by economy (min 180 balls = 30 overs)
--     Overs assumed 0-19 (death = over_no >= 15). Use >= 16 if overs are 1-20.
-- ---------------------------------------------------------------------
SELECT bowler,
       COUNT(*) AS balls,
       SUM(total_runs) AS runs,
       ROUND(6.0 * SUM(total_runs) / COUNT(*), 2) AS economy
FROM deliveries
WHERE over_no >= 15 AND inning IN (1, 2)
GROUP BY bowler
HAVING COUNT(*) >= 180
ORDER BY economy ASC
LIMIT 10;
