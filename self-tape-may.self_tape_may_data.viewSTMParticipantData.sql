SELECT 
  max(stm._createdDate) as createdDate,
  LOWER(stm.email) AS email,
  CASE WHEN stm.instagram LIKE '@%' THEN LOWER(stm.instagram) ELSE CONCAT('@', LOWER(stm.instagram)) END as instagram, 
  stm.market,
  stm.name,
  stm.excludeFromLeaderboard,
  stm.numYearsParticipated,
  stm.participatedBefore,
  stm.numYearsSixteen,
  stm.recordedSixteen
FROM `self-tape-may.self_tape_may_data.tblSTMParticipantData` stm
JOIN (
  SELECT max(a._createdDate) as createdDate,
  CASE WHEN a.instagram LIKE '@%' THEN a.instagram ELSE CONCAT('@', a.instagram) END as instagram
  FROM `self-tape-may.self_tape_may_data.tblSTMParticipantData` a
  GROUP BY a.instagram
  ORDER BY max(a._createdDate) desc, a.instagram
) subQuery on subQuery.instagram = stm.instagram and subQuery.createdDate = stm._createdDate
GROUP BY
  stm.email,
  stm.instagram,
  stm.market,
  stm.name,
  stm.excludeFromLeaderboard,
  stm.numYearsParticipated,
  stm.participatedBefore,
  stm.numYearsSixteen,
  stm.recordedSixteen
  --createdDate
  --max(stm._createdDate)
ORDER BY max(stm._createdDate) DESC
