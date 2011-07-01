
-- Places
SELECT name, num_checkins, authentic, num_fans
FROM dim_location_places_and_page_names
    WHERE ds='2011-06-30'
ORDER BY num_checkins DESC
LIMIT 10000
;


-- People
SELECT dim_active_users.name
FROM (
    SELECT userid
    FROM tmp_davidma_eigenpoke_weights
    ORDER BY weight DESC
    LIMIT 10000
) u
JOIN dim_active_users
    ON u.userid=dim_active_users.userid
    AND dim_active_users.ds='2011-06-29'
;


-- Apps

SELECT appid.*, dim_application.application_name
FROM (
    SELECT *
    FROM dim_application_stats
        WHERE ds='2011-06-30'
    ORDER BY CAST(num_users_engaged_monthly AS INT) DESC
    LIMIT 10000
) appid
JOIN dim_application
    ON appid.application_id = dim_application.application_id
    AND dim_application.ds = '2011-06-29'
;



