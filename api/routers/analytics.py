from typing import Any

import psycopg
from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies import get_database_connection
from api.schemas.analytics import (
    ConstructorPerformance,
    FastestLap,
    PositionGain,
    StintSummary,
)

router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"],
)


@router.get(
    "/events/{event_id}/fastest-laps",
    response_model=list[FastestLap],
)
def get_fastest_laps(
    event_id: int,
    limit: int = Query(
        default=10,
        ge=1,
        le=20,
        description="Number of drivers to return.",
    ),
    connection: psycopg.Connection[dict[str, Any]] = Depends(get_database_connection),
) -> list[dict[str, Any]]:
    """
    Return each driver's fastest valid lap, ordered fastest first.
    """

    verify_event_exists(connection, event_id)

    with connection.cursor() as cursor:
        cursor.execute(
            """
            WITH driver_fastest_laps AS (
                SELECT
                    lap.driver_id,
                    lap.lap_number,
                    lap.lap_time_ms,
                    lap.compound,
                    ROW_NUMBER() OVER (
                        PARTITION BY lap.driver_id
                        ORDER BY lap.lap_time_ms ASC
                    ) AS driver_lap_rank
                FROM fact_lap AS lap
                WHERE
                    lap.event_id = %s
                    AND lap.lap_time_ms IS NOT NULL
                    AND lap.pit_in = FALSE
                    AND lap.pit_out = FALSE
            )
            SELECT
                ROW_NUMBER() OVER (
                    ORDER BY fastest.lap_time_ms ASC
                ) AS position,
                driver.driver_id,
                driver.driver_code,
                driver.full_name,
                constructor.constructor_name,
                fastest.lap_number,
                fastest.lap_time_ms,
                fastest.compound
            FROM driver_fastest_laps AS fastest
            INNER JOIN dim_driver AS driver
                ON driver.driver_id = fastest.driver_id
            LEFT JOIN fact_result AS result
                ON result.event_id = %s
                AND result.driver_id = fastest.driver_id
            LEFT JOIN dim_constructor AS constructor
                ON constructor.constructor_id =
                    result.constructor_id
            WHERE fastest.driver_lap_rank = 1
            ORDER BY fastest.lap_time_ms ASC
            LIMIT %s;
            """,
            (
                event_id,
                event_id,
                limit,
            ),
        )

        rows = cursor.fetchall()

    return rows


@router.get(
    "/events/{event_id}/position-gains",
    response_model=list[PositionGain],
)
def get_position_gains(
    event_id: int,
    connection: psycopg.Connection[dict[str, Any]] = Depends(get_database_connection),
) -> list[dict[str, Any]]:
    """
    Compare each driver's starting and finishing positions.
    """

    verify_event_exists(connection, event_id)

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                driver.driver_id,
                driver.driver_code,
                driver.full_name,
                constructor.constructor_name,
                result.grid_position,
                result.finish_position,
                CASE
                    WHEN
                        result.grid_position IS NOT NULL
                        AND result.finish_position IS NOT NULL
                        AND result.grid_position > 0
                    THEN
                        result.grid_position
                        - result.finish_position
                    ELSE NULL
                END AS positions_gained
            FROM fact_result AS result
            INNER JOIN dim_driver AS driver
                ON driver.driver_id = result.driver_id
            LEFT JOIN dim_constructor AS constructor
                ON constructor.constructor_id =
                    result.constructor_id
            WHERE result.event_id = %s
            ORDER BY
                positions_gained DESC NULLS LAST,
                result.finish_position ASC NULLS LAST;
            """,
            (event_id,),
        )

        rows = cursor.fetchall()

    return rows


@router.get(
    "/events/{event_id}/constructors",
    response_model=list[ConstructorPerformance],
)
def get_constructor_performance(
    event_id: int,
    connection: psycopg.Connection[dict[str, Any]] = Depends(get_database_connection),
) -> list[dict[str, Any]]:
    """
    Summarize constructor results for one event.
    """

    verify_event_exists(connection, event_id)

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                constructor.constructor_id,
                constructor.constructor_name,
                COUNT(
                    DISTINCT result.driver_id
                ) AS driver_count,
                SUM(result.points) AS total_points,
                MIN(
                    result.finish_position
                ) AS best_finish,
                ROUND(
                    AVG(result.finish_position),
                    2
                ) AS average_finish
            FROM fact_result AS result
            INNER JOIN dim_constructor AS constructor
                ON constructor.constructor_id =
                    result.constructor_id
            WHERE result.event_id = %s
            GROUP BY
                constructor.constructor_id,
                constructor.constructor_name
            ORDER BY
                total_points DESC,
                best_finish ASC NULLS LAST;
            """,
            (event_id,),
        )

        rows = cursor.fetchall()

    return rows


@router.get(
    "/events/{event_id}/stints",
    response_model=list[StintSummary],
)
def get_stint_summaries(
    event_id: int,
    driver_code: str | None = Query(
        default=None,
        min_length=2,
        max_length=3,
        description="Optionally filter by driver code.",
    ),
    connection: psycopg.Connection[dict[str, Any]] = Depends(get_database_connection),
) -> list[dict[str, Any]]:
    """
    Summarize each driver's tire stints and lap pace.
    """

    verify_event_exists(connection, event_id)

    query = """
        SELECT
            driver.driver_id,
            driver.driver_code,
            driver.full_name,
            lap.stint_number,
            lap.compound,
            MIN(lap.lap_number) AS first_lap,
            MAX(lap.lap_number) AS last_lap,
            COUNT(*) AS lap_count,
            ROUND(
                AVG(lap.lap_time_ms),
                2
            ) AS average_lap_time_ms,
            MIN(
                lap.lap_time_ms
            ) AS fastest_lap_time_ms
        FROM fact_lap AS lap
        INNER JOIN dim_driver AS driver
            ON driver.driver_id = lap.driver_id
        WHERE
            lap.event_id = %s
            AND lap.stint_number IS NOT NULL
            AND lap.pit_in = FALSE
            AND lap.pit_out = FALSE
    """

    parameters: list[Any] = [event_id]

    if driver_code is not None:
        query += """
            AND UPPER(driver.driver_code) = UPPER(%s)
        """

        parameters.append(driver_code)

    query += """
        GROUP BY
            driver.driver_id,
            driver.driver_code,
            driver.full_name,
            lap.stint_number,
            lap.compound
        ORDER BY
            driver.driver_code ASC,
            lap.stint_number ASC;
    """

    with connection.cursor() as cursor:
        cursor.execute(
            query,
            tuple(parameters),
        )

        rows = cursor.fetchall()

    return rows


def verify_event_exists(
    connection: psycopg.Connection[dict[str, Any]],
    event_id: int,
) -> None:
    """Raise a 404 response when an event does not exist."""

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM dim_event
                WHERE event_id = %s
            ) AS event_exists;
            """,
            (event_id,),
        )

        row = cursor.fetchone()

    if row is None or not row["event_exists"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event {event_id} was not found.",
        )
