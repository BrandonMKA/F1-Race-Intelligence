-- Available events
SELECT
    event_id,
    season,
    round_number,
    event_name,
    session_name
FROM dim_event
ORDER BY season DESC, round_number DESC;


-- Race results
SELECT
    e.season,
    e.event_name,
    r.finish_position,
    d.driver_code,
    c.constructor_name,
    r.grid_position,
    r.points,
    r.status
FROM fact_result AS r
JOIN dim_event AS e
    ON r.event_id = e.event_id
JOIN dim_driver AS d
    ON r.driver_id = d.driver_id
LEFT JOIN dim_constructor AS c
    ON r.constructor_id = c.constructor_id
ORDER BY
    e.season DESC,
    e.round_number DESC,
    r.finish_position;


-- Fastest laps
SELECT
    e.event_name,
    d.driver_code,
    l.lap_number,
    l.lap_time_ms,
    l.compound
FROM fact_lap AS l
JOIN dim_event AS e
    ON l.event_id = e.event_id
JOIN dim_driver AS d
    ON l.driver_id = d.driver_id
WHERE l.lap_time_ms IS NOT NULL
ORDER BY l.lap_time_ms
LIMIT 20;


-- Pipeline history
SELECT
    pipeline_run_id,
    season,
    event_name,
    status,
    started_at,
    completed_at,
    result_rows_loaded,
    lap_rows_loaded,
    error_message
FROM pipeline_run
ORDER BY started_at DESC;