USE ipl;
-- ---------------------------------------------------------------------
-- 3. Does the toss matter?  (CTE)
-- ---------------------------------------------------------------------
WITH toss AS (
  SELECT toss_decision,
         COUNT(*) AS matches_played,
         SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS toss_winner_won
  FROM matches
  WHERE winner IS NOT NULL AND winner <> ''
  GROUP BY toss_decision
)
SELECT toss_decision, matches_played, toss_winner_won,
       ROUND(100.0 * toss_winner_won / matches_played, 1) AS win_pct
FROM toss;
