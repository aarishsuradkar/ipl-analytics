USE ipl;
-- -----------------------------------------------------------------------
-- 9. Player of the match leaders
-- ---------------------------------------------------------------------
SELECT player_of_match, COUNT(*) AS awards
FROM matches
WHERE player_of_match IS NOT NULL AND player_of_match <> ''
GROUP BY player_of_match
ORDER BY awards DESC
LIMIT 10;
