SELECT DISTINCT REPLACE(a.instagram, '@', '') AS instagram,
a.instagram as instaOrig,
'https://www.instagram.com/' || REPLACE(a.instagram, '@', '') as instagramURL
FROM `self-tape-may.self_tape_may_data.viewSTMParticipantData` a
ORDER BY a.instagram;
