SELECT ROW_NUMBER() OVER (ORDER BY count(stm.id) DESC, max(stm.timestamp) ASC) as user_rank, 
       stm.ownerUsername, count(stm.id) as num_selftapes, max(stm.timestamp) as max_timestamp, 
       sum(stm.videoDuration) as ttl_vid_minutes, CASE WHEN count(campflg.ownerUsername) > 0 THEN 'Y' ELSE 'N' END as campaignFlag
FROM `self-tape-may.self_tape_may_data.tbl-stm-clean-data` as stm 
LEFT OUTER JOIN (
    SELECT ownerUsername
    FROM `self-tape-may.self_tape_may_data.tbl-stm-clean-data` stm
    WHERE ownerUsername = stm.ownerUsername
    AND campaignFlag = 'Y'
    GROUP BY ownerUsername, campaignFlag
    HAVING COUNT(*) > 0
) AS campflg ON stm.ownerUsername = campflg.ownerUsername
WHERE stm.id is not null
GROUP BY stm.ownerUsername
ORDER BY count(stm.id) DESC, max(stm.timestamp) ASC;
