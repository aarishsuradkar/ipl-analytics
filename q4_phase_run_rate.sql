USE ipl;
-- ---------------------------------------------------------------------
-- 4. Run rate by phase: powerplay / middle / death  (CASE WHEN)
--    Overs assumed 0-19. If yours are 1-20, use <= 6 and <= 15 and >= 16.
--    Wides and no-balls count as balls here, so run rate is approximate.
-- ---------------------------------------------------------------------
SELECT batting_team,
       CASE WHEN over_no <= 5  THEN 'Powerplay'
            WHEN over_no <= 14 THEN 'Middle'
            ELSE 'Death' END AS phase,
       ROUND(6.0 * SUM(total_runs) / COUNT(*), 2) AS run_rate
FROM deliveries
WHERE inning IN (1, 2)
GROUP BY batting_team, phase
ORDER BY batting_team, phase;

