CREATE TABLE IF NOT EXISTS dim_event (
    event_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    season INTEGER NOT NULL,
    round_number INTEGER NOT NULL,
    event_name VARCHAR(150) NOT NULL,
    session_name VARCHAR(50) NOT NULL,
    session_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_event_session
        UNIQUE (season, round_number, session_name),

    CONSTRAINT chk_event_season
        CHECK (season >= 1950),

    CONSTRAINT chk_round_number
        CHECK (round_number > 0)
);


CREATE TABLE IF NOT EXISTS dim_driver (
    driver_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    driver_number INTEGER,
    driver_code VARCHAR(3) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    full_name VARCHAR(200),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_driver_code
        UNIQUE (driver_code),

    CONSTRAINT chk_driver_code_length
        CHECK (char_length(driver_code) = 3)
);


CREATE TABLE IF NOT EXISTS dim_constructor (
    constructor_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    constructor_name VARCHAR(150) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_constructor_name
        UNIQUE (constructor_name)
);


CREATE TABLE IF NOT EXISTS fact_result (
    result_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    event_id BIGINT NOT NULL,
    driver_id BIGINT NOT NULL,
    constructor_id BIGINT,
    grid_position INTEGER,
    finish_position INTEGER,
    points NUMERIC(6, 2) NOT NULL DEFAULT 0,
    status VARCHAR(150),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_result_event
        FOREIGN KEY (event_id)
        REFERENCES dim_event(event_id),

    CONSTRAINT fk_result_driver
        FOREIGN KEY (driver_id)
        REFERENCES dim_driver(driver_id),

    CONSTRAINT fk_result_constructor
        FOREIGN KEY (constructor_id)
        REFERENCES dim_constructor(constructor_id),

    CONSTRAINT uq_result_event_driver
        UNIQUE (event_id, driver_id),

    CONSTRAINT chk_grid_position
        CHECK (grid_position IS NULL OR grid_position >= 0),

    CONSTRAINT chk_finish_position
        CHECK (finish_position IS NULL OR finish_position > 0),

    CONSTRAINT chk_points
        CHECK (points >= 0)
);


CREATE TABLE IF NOT EXISTS fact_lap (
    lap_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    event_id BIGINT NOT NULL,
    driver_id BIGINT NOT NULL,
    lap_number INTEGER NOT NULL,
    stint_number INTEGER,
    compound VARCHAR(30),
    tire_life INTEGER,
    position INTEGER,
    lap_time_ms INTEGER,
    sector_1_ms INTEGER,
    sector_2_ms INTEGER,
    sector_3_ms INTEGER,
    is_personal_best BOOLEAN NOT NULL DEFAULT FALSE,
    pit_in BOOLEAN NOT NULL DEFAULT FALSE,
    pit_out BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_lap_event
        FOREIGN KEY (event_id)
        REFERENCES dim_event(event_id),

    CONSTRAINT fk_lap_driver
        FOREIGN KEY (driver_id)
        REFERENCES dim_driver(driver_id),

    CONSTRAINT uq_lap_event_driver_number
        UNIQUE (event_id, driver_id, lap_number),

    CONSTRAINT chk_lap_number
        CHECK (lap_number > 0),

    CONSTRAINT chk_stint_number
        CHECK (stint_number IS NULL OR stint_number > 0),

    CONSTRAINT chk_tire_life
        CHECK (tire_life IS NULL OR tire_life >= 0),

    CONSTRAINT chk_lap_position
        CHECK (position IS NULL OR position > 0),

    CONSTRAINT chk_lap_time
        CHECK (lap_time_ms IS NULL OR lap_time_ms > 0),

    CONSTRAINT chk_sector_1
        CHECK (sector_1_ms IS NULL OR sector_1_ms > 0),

    CONSTRAINT chk_sector_2
        CHECK (sector_2_ms IS NULL OR sector_2_ms > 0),

    CONSTRAINT chk_sector_3
        CHECK (sector_3_ms IS NULL OR sector_3_ms > 0)
);


CREATE TABLE IF NOT EXISTS pipeline_run (
    pipeline_run_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    season INTEGER NOT NULL,
    round_number INTEGER,
    event_name VARCHAR(150) NOT NULL,
    session_name VARCHAR(50) NOT NULL,
    status VARCHAR(30) NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ,
    result_rows_loaded INTEGER NOT NULL DEFAULT 0,
    lap_rows_loaded INTEGER NOT NULL DEFAULT 0,
    error_message TEXT,

    CONSTRAINT chk_pipeline_status
        CHECK (
            status IN (
                'running',
                'successful',
                'failed'
            )
        )
);