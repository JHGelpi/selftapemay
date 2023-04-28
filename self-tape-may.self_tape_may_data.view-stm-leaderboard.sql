SELECT ROW_NUMBER() OVER (ORDER BY count(stm.id) DESC, max(stm.timestamp) ASC) as userRank, 
       LOWER(stm.ownerUsername) as instagram, 
       count(stm.id) as numSelftapes, 
       --FORMAT_TIMESTAMP('%FT%T', TIMESTAMP(max(stm.timestamp))) as maxTimestamp,
        FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', TIMESTAMP(max(stm.timestamp))) as maxTimestamp,
       --sum(stm.videoDuration) as ttlVidMinutes, 
       CASE WHEN count(campflg.ownerUsername) > 0 THEN 'Y' ELSE 'N' END as campaignFlag, 
       partData.name, 
       LOWER(partData.email) as email,
       partData.market, 
       partData.participatedBefore, 
       partData.numYearsParticipated, 
       partData.recordedSixteen, 
       partData.numYearsSixteen, 
       partData.excludeFromLeaderboard, 
       stm.ownerUsername as _id, 
       max(stm.timestamp) as _createdDate, 
       max(stm.timestamp) as _updatedDate, 
       stm.ownerUsername as _owner
FROM `self-tape-may.self_tape_may_data.tblInstagramData` as stm
LEFT OUTER JOIN (
    SELECT ownerUsername
    FROM `self-tape-may.self_tape_may_data.tblInstagramData` stm
    WHERE ownerUsername = stm.ownerUsername
    AND campaignFlag = true
    GROUP BY ownerUsername, campaignFlag
    HAVING COUNT(*) > 0
) AS campflg ON stm.ownerUsername = campflg.ownerUsername
LEFT OUTER JOIN `self-tape-may.self_tape_may_data.viewSTMParticipantData` partData ON
partData.instagram = stm.ownerUsername
WHERE stm.id is not null AND (partData.excludeFromLeaderboard != TRUE OR partData.excludeFromLeaderboard IS NULL)
GROUP BY stm.ownerUsername, partData.name, partData.email, partData.market, partData.participatedBefore, partData.numYearsParticipated, partData.recordedSixteen, partData.numYearsSixteen, partData.excludeFromLeaderboard
ORDER BY max(stm.timestamp) DESC;
