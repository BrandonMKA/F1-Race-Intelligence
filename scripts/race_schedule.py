from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

import fastf1
import pandas as pd

from pipeline.load.database import get_connection

logger = logging.getLogger(__name__)


def get_loaded_rounds(season: int) -> set[int]:
    """Return rounds that already have both results and laps."""

    query = """
        SELECT event.round_number
        FROM dim_event AS event
        WHERE event.season = %s
          AND EXISTS (
              SELECT 1
              FROM fact_result AS result
              WHERE result.event_id = event.event_id
          )
          AND EXISTS (
              SELECT 1
              FROM fact_lap AS lap
              WHERE lap.event_id = event.event_id
          )
        ORDER BY event.round_number;
    """

    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(query, (season,))
        rows = cursor.fetchall()

    return {int(row["round_number"]) for row in rows}


def get_race_start(event: pd.Series) -> pd.Timestamp | None:
    """Find the UTC start time of the Race session in a schedule row."""

    for session_number in range(1, 6):
        session_name = event.get(f"Session{session_number}")

        if not isinstance(session_name, str):
            continue

        if session_name.strip().lower() != "race":
            continue

        value = event.get(f"Session{session_number}DateUtc")

        if pd.isna(value):
            value = event.get(f"Session{session_number}Date")

        if pd.isna(value):
            return None

        timestamp = pd.Timestamp(value)

        if timestamp.tzinfo is None:
            return timestamp.tz_localize("UTC")

        return timestamp.tz_convert("UTC")

    return None


def get_completed_races(
    season: int,
    start_round: int = 1,
    end_round: int | None = None,
    availability_delay_hours: int = 6,
) -> list[dict[str, Any]]:
    """Return schedule entries whose race data should now be available."""

    schedule = fastf1.get_event_schedule(
        season,
        include_testing=False,
    )

    now = datetime.now(timezone.utc)
    delay = timedelta(hours=availability_delay_hours)
    races: list[dict[str, Any]] = []

    for _, event in schedule.iterrows():
        round_value = event.get("RoundNumber")

        if pd.isna(round_value):
            continue

        round_number = int(round_value)

        if round_number < start_round:
            continue

        if end_round is not None and round_number > end_round:
            continue

        race_start = get_race_start(event)

        if race_start is None:
            logger.warning(
                "Skipping round %s because its race time was unavailable.",
                round_number,
            )
            continue

        available_after = race_start.to_pydatetime() + delay

        if available_after > now:
            continue

        races.append(
            {
                "round_number": round_number,
                "event_name": str(event["EventName"]),
                "race_start": race_start,
            }
        )

    return races
