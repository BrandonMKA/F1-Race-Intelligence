CREATE INDEX IF NOT EXISTS idx_event_season_round
    ON dim_event (season, round_number);


CREATE INDEX IF NOT EXISTS idx_result_event
    ON fact_result (event_id);


CREATE INDEX IF NOT EXISTS idx_result_driver
    ON fact_result (driver_id);


CREATE INDEX IF NOT EXISTS idx_lap_event
    ON fact_lap (event_id);


CREATE INDEX IF NOT EXISTS idx_lap_driver
    ON fact_lap (driver_id);


CREATE INDEX IF NOT EXISTS idx_lap_event_driver
    ON fact_lap (event_id, driver_id);


CREATE INDEX IF NOT EXISTS idx_lap_event_number
    ON fact_lap (event_id, lap_number);


CREATE INDEX IF NOT EXISTS idx_pipeline_run_started
    ON pipeline_run (started_at DESC);