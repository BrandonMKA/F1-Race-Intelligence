from typing import Any

import pandas as pd
import psycopg

from pipeline.load.database import get_connection


def to_python_value(value: Any) -> Any:
    """
    Convert Pandas and NumPy null values into Python None.
    """

    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        return value.item()

    return value


def upsert_event(
    cursor: psycopg.Cursor[Any],
    metadata: dict[str, Any],
) -> int:
    """Insert or update an event and return its database ID."""

    cursor.execute(
        """
        INSERT INTO dim_event (
            season,
            round_number,
            event_name,
            session_name,
            session_date
        )
        VALUES (
            %(season)s,
            %(round_number)s,
            %(event_name)s,
            %(session_name)s,
            %(session_date)s
        )
        ON CONFLICT (
            season,
            round_number,
            session_name
        )
        DO UPDATE SET
            event_name = EXCLUDED.event_name,
            session_date = EXCLUDED.session_date
        RETURNING event_id;
        """,
        {
            "season": metadata["season"],
            "round_number": metadata["round_number"],
            "event_name": metadata["event_name"],
            "session_name": metadata["session_name"],
            "session_date": metadata.get("session_date"),
        },
    )

    row = cursor.fetchone()

    if row is None:
        raise RuntimeError("Failed to create or retrieve event.")

    return row["event_id"]


def upsert_driver(
    cursor: psycopg.Cursor[Any],
    result: pd.Series,
) -> int:
    """Insert or update a driver and return its database ID."""

    cursor.execute(
        """
        INSERT INTO dim_driver (
            driver_number,
            driver_code,
            first_name,
            last_name,
            full_name
        )
        VALUES (
            %(driver_number)s,
            %(driver_code)s,
            %(first_name)s,
            %(last_name)s,
            %(full_name)s
        )
        ON CONFLICT (driver_code)
        DO UPDATE SET
            driver_number = EXCLUDED.driver_number,
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            full_name = EXCLUDED.full_name
        RETURNING driver_id;
        """,
        {
            "driver_number": to_python_value(result["driver_number"]),
            "driver_code": result["driver_code"],
            "first_name": to_python_value(result["first_name"]),
            "last_name": to_python_value(result["last_name"]),
            "full_name": to_python_value(result["full_name"]),
        },
    )

    row = cursor.fetchone()

    if row is None:
        raise RuntimeError(f"Failed to create driver {result['driver_code']}.")

    return row["driver_id"]


def upsert_constructor(
    cursor: psycopg.Cursor[Any],
    constructor_name: str | None,
) -> int | None:
    """Insert a constructor and return its database ID."""

    if constructor_name is None or pd.isna(constructor_name):
        return None

    cursor.execute(
        """
        INSERT INTO dim_constructor (
            constructor_name
        )
        VALUES (%s)
        ON CONFLICT (constructor_name)
        DO UPDATE SET
            constructor_name = EXCLUDED.constructor_name
        RETURNING constructor_id;
        """,
        (constructor_name,),
    )

    row = cursor.fetchone()

    if row is None:
        raise RuntimeError(f"Failed to create constructor {constructor_name}.")

    return row["constructor_id"]


def upsert_result(
    cursor: psycopg.Cursor[Any],
    event_id: int,
    driver_id: int,
    constructor_id: int | None,
    result: pd.Series,
) -> None:
    """Insert or update one race result."""

    cursor.execute(
        """
        INSERT INTO fact_result (
            event_id,
            driver_id,
            constructor_id,
            grid_position,
            finish_position,
            points,
            status
        )
        VALUES (
            %(event_id)s,
            %(driver_id)s,
            %(constructor_id)s,
            %(grid_position)s,
            %(finish_position)s,
            %(points)s,
            %(status)s
        )
        ON CONFLICT (
            event_id,
            driver_id
        )
        DO UPDATE SET
            constructor_id = EXCLUDED.constructor_id,
            grid_position = EXCLUDED.grid_position,
            finish_position = EXCLUDED.finish_position,
            points = EXCLUDED.points,
            status = EXCLUDED.status;
        """,
        {
            "event_id": event_id,
            "driver_id": driver_id,
            "constructor_id": constructor_id,
            "grid_position": to_python_value(result["grid_position"]),
            "finish_position": to_python_value(result["finish_position"]),
            "points": to_python_value(result["points"]) or 0,
            "status": to_python_value(result["status"]),
        },
    )


def upsert_lap(
    cursor: psycopg.Cursor[Any],
    event_id: int,
    driver_id: int,
    lap: pd.Series,
) -> None:
    """Insert or update one driver-lap record."""

    cursor.execute(
        """
        INSERT INTO fact_lap (
            event_id,
            driver_id,
            lap_number,
            stint_number,
            compound,
            tire_life,
            position,
            lap_time_ms,
            sector_1_ms,
            sector_2_ms,
            sector_3_ms,
            is_personal_best,
            pit_in,
            pit_out
        )
        VALUES (
            %(event_id)s,
            %(driver_id)s,
            %(lap_number)s,
            %(stint_number)s,
            %(compound)s,
            %(tire_life)s,
            %(position)s,
            %(lap_time_ms)s,
            %(sector_1_ms)s,
            %(sector_2_ms)s,
            %(sector_3_ms)s,
            %(is_personal_best)s,
            %(pit_in)s,
            %(pit_out)s
        )
        ON CONFLICT (
            event_id,
            driver_id,
            lap_number
        )
        DO UPDATE SET
            stint_number = EXCLUDED.stint_number,
            compound = EXCLUDED.compound,
            tire_life = EXCLUDED.tire_life,
            position = EXCLUDED.position,
            lap_time_ms = EXCLUDED.lap_time_ms,
            sector_1_ms = EXCLUDED.sector_1_ms,
            sector_2_ms = EXCLUDED.sector_2_ms,
            sector_3_ms = EXCLUDED.sector_3_ms,
            is_personal_best = EXCLUDED.is_personal_best,
            pit_in = EXCLUDED.pit_in,
            pit_out = EXCLUDED.pit_out;
        """,
        {
            "event_id": event_id,
            "driver_id": driver_id,
            "lap_number": to_python_value(lap["lap_number"]),
            "stint_number": to_python_value(lap["stint_number"]),
            "compound": to_python_value(lap["compound"]),
            "tire_life": to_python_value(lap["tire_life"]),
            "position": to_python_value(lap["position"]),
            "lap_time_ms": to_python_value(lap["lap_time_ms"]),
            "sector_1_ms": to_python_value(lap["sector_1_ms"]),
            "sector_2_ms": to_python_value(lap["sector_2_ms"]),
            "sector_3_ms": to_python_value(lap["sector_3_ms"]),
            "is_personal_best": bool(to_python_value(lap["is_personal_best"])),
            "pit_in": bool(to_python_value(lap["pit_in"])),
            "pit_out": bool(to_python_value(lap["pit_out"])),
        },
    )


def start_pipeline_run(
    cursor: psycopg.Cursor[Any],
    metadata: dict[str, Any],
) -> int:
    """Create a running pipeline record."""

    cursor.execute(
        """
        INSERT INTO pipeline_run (
            season,
            round_number,
            event_name,
            session_name,
            status
        )
        VALUES (
            %(season)s,
            %(round_number)s,
            %(event_name)s,
            %(session_name)s,
            'running'
        )
        RETURNING pipeline_run_id;
        """,
        metadata,
    )

    row = cursor.fetchone()

    if row is None:
        raise RuntimeError("Failed to start pipeline run.")

    return row["pipeline_run_id"]


def complete_pipeline_run(
    cursor: psycopg.Cursor[Any],
    pipeline_run_id: int,
    result_count: int,
    lap_count: int,
) -> None:
    """Mark a pipeline run successful."""

    cursor.execute(
        """
        UPDATE pipeline_run
        SET
            status = 'successful',
            completed_at = CURRENT_TIMESTAMP,
            result_rows_loaded = %s,
            lap_rows_loaded = %s
        WHERE pipeline_run_id = %s;
        """,
        (
            result_count,
            lap_count,
            pipeline_run_id,
        ),
    )


def load_race_to_database(
    results: pd.DataFrame,
    laps: pd.DataFrame,
    metadata: dict[str, Any],
) -> None:
    """Load one transformed race into PostgreSQL."""

    with get_connection() as connection, connection.cursor() as cursor:
        pipeline_run_id = start_pipeline_run(
            cursor,
            metadata,
        )

        event_id = upsert_event(
            cursor,
            metadata,
        )

        driver_ids: dict[str, int] = {}

        for _, result in results.iterrows():
            driver_id = upsert_driver(cursor, result)

            constructor_id = upsert_constructor(
                cursor,
                to_python_value(result["constructor_name"]),
            )

            upsert_result(
                cursor=cursor,
                event_id=event_id,
                driver_id=driver_id,
                constructor_id=constructor_id,
                result=result,
            )

            driver_ids[result["driver_code"]] = driver_id

        for _, lap in laps.iterrows():
            driver_code = lap["driver_code"]
            driver_id = driver_ids.get(driver_code)

            if driver_id is None:
                raise ValueError(
                    "Lap data contains a driver that is not "
                    f"in the results table: {driver_code}"
                )

            upsert_lap(
                cursor=cursor,
                event_id=event_id,
                driver_id=driver_id,
                lap=lap,
            )

        complete_pipeline_run(
            cursor=cursor,
            pipeline_run_id=pipeline_run_id,
            result_count=len(results),
            lap_count=len(laps),
        )

    print("Database load completed successfully.")
    print(f"Results loaded: {len(results):,}")
    print(f"Laps loaded: {len(laps):,}")
