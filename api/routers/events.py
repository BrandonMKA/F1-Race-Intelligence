from typing import Any

import psycopg
from fastapi import APIRouter, Depends, HTTPException, Query, status


from api.dependencies import get_database_connection
from api.schemas.event import EventDetail, EventSummary
from api.schemas.lap import Lap
from api.schemas.result import RaceResult


router = APIRouter(
    prefix="/api/events",
    tags=["Events"],
)


@router.get(
    "",
    response_model=list[EventSummary],
)
def list_events(
    season: int | None = Query(
        default=None,
        ge=1950,
        le=2100,
        description="Optionally filter events by season.",
    ),
    connection: psycopg.Connection[dict[str, Any]] = Depends(
        get_database_connection
    ),
) -> list[dict[str, Any]]:
    """
    Return all loaded F1 events.

    Results can optionally be filtered by season.
    """

    query = """
        SELECT
            event_id,
            season,
            round_number,
            event_name,
            session_name,
            session_date
        FROM dim_event
    """

    parameters: tuple[Any, ...] = ()

    if season is not None:
        query += """
            WHERE season = %s
        """

        parameters = (season,)

    query += """
        ORDER BY
            season DESC,
            round_number ASC;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, parameters)
        rows = cursor.fetchall()

    return rows


@router.get(
    "/{event_id}",
    response_model=EventDetail,
)
def get_event(
    event_id: int,
    connection: psycopg.Connection[dict[str, Any]] = Depends(
        get_database_connection
    ),
) -> dict[str, Any]:
    """
    Return one event and its related row counts.
    """

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                event.event_id,
                event.season,
                event.round_number,
                event.event_name,
                event.session_name,
                event.session_date,
                (
                    SELECT COUNT(*)
                    FROM fact_result
                    WHERE fact_result.event_id = event.event_id
                ) AS result_count,
                (
                    SELECT COUNT(*)
                    FROM fact_lap
                    WHERE fact_lap.event_id = event.event_id
                ) AS lap_count
            FROM dim_event AS event
            WHERE event.event_id = %s;
            """,
            (event_id,),
        )

        row = cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event {event_id} was not found.",
        )

    return row


@router.get(
    "/{event_id}/results",
    response_model=list[RaceResult],
)
def get_event_results(
    event_id: int,
    connection: psycopg.Connection[dict[str, Any]] = Depends(
        get_database_connection
    ),
) -> list[dict[str, Any]]:
    """
    Return race results for one event.
    """

    verify_event_exists(
        connection=connection,
        event_id=event_id,
    )

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                driver.driver_id,
                driver.driver_number,
                driver.driver_code,
                driver.first_name,
                driver.last_name,
                driver.full_name,
                constructor.constructor_name,
                result.grid_position,
                result.finish_position,
                result.points,
                result.status
            FROM fact_result AS result
            INNER JOIN dim_driver AS driver
                ON driver.driver_id = result.driver_id
            LEFT JOIN dim_constructor AS constructor
                ON constructor.constructor_id =
                    result.constructor_id
            WHERE result.event_id = %s
            ORDER BY
                result.finish_position ASC NULLS LAST,
                result.points DESC,
                driver.driver_code ASC;
            """,
            (event_id,),
        )

        rows = cursor.fetchall()

    return rows


@router.get(
    "/{event_id}/laps",
    response_model=list[Lap],
)
def get_event_laps(
    event_id: int,
    driver_code: str | None = Query(
        default=None,
        min_length=2,
        max_length=3,
        description="Optionally filter by driver code.",
    ),
    limit: int = Query(
        default=500,
        ge=1,
        le=5000,
        description="Maximum number of lap rows to return.",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of lap rows to skip.",
    ),
    connection: psycopg.Connection[dict[str, Any]] = Depends(
        get_database_connection
    ),
) -> list[dict[str, Any]]:
    """
    Return lap data for an event.

    The response supports driver filtering and pagination.
    """

    verify_event_exists(
        connection=connection,
        event_id=event_id,
    )

    query = """
        SELECT
            driver.driver_id,
            driver.driver_code,
            driver.full_name,
            lap.lap_number,
            lap.stint_number,
            lap.compound,
            lap.tire_life,
            lap.position,
            lap.lap_time_ms,
            lap.sector_1_ms,
            lap.sector_2_ms,
            lap.sector_3_ms,
            lap.is_personal_best,
            lap.pit_in,
            lap.pit_out
        FROM fact_lap AS lap
        INNER JOIN dim_driver AS driver
            ON driver.driver_id = lap.driver_id
        WHERE lap.event_id = %s
    """

    parameters: list[Any] = [event_id]

    if driver_code is not None:
        query += """
            AND UPPER(driver.driver_code) = UPPER(%s)
        """

        parameters.append(driver_code)

    query += """
        ORDER BY
            lap.lap_number ASC,
            driver.driver_code ASC
        LIMIT %s
        OFFSET %s;
    """

    parameters.extend([limit, offset])

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
    """
    Raise a 404 response if an event does not exist.
    """

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