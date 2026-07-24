from pathlib import Path
from typing import Any

import fastf1
import pandas as pd

CACHE_DIR = Path("cache")


def load_race(
    season: int,
    event_name: str | int,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    """
    Download a Formula 1 race session.

    Returns:
        A tuple containing:
        1. Race results
        2. Lap-level data
        3. Session metadata
    """

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    fastf1.Cache.enable_cache(str(CACHE_DIR))

    session = fastf1.get_session(
        season,
        event_name,
        "R",
    )

    print(f"Loading {season}, event {event_name}...")

    session.load(
        telemetry=False,
        weather=False,
        messages=False,
    )

    results = session.results.copy()
    laps = session.laps.copy()

    if results.empty:
        raise ValueError("FastF1 returned no race results.")

    if laps.empty:
        raise ValueError("FastF1 returned no lap records.")

    metadata = {
        "season": season,
        "event_name": str(session.event["EventName"]),
        "round_number": int(session.event["RoundNumber"]),
        "session_name": str(session.name),
        "session_date": session.date,
    }

    return results, laps, metadata


def display_summary(
    results: pd.DataFrame,
    laps: pd.DataFrame,
    metadata: dict[str, Any],
) -> None:
    """Print a small summary of the extracted race."""

    print("\nSession metadata:")
    for key, value in metadata.items():
        print(f"{key}: {value}")

    result_columns = [
        "Position",
        "Abbreviation",
        "TeamName",
        "GridPosition",
        "Points",
        "Status",
    ]

    lap_columns = [
        "Driver",
        "LapNumber",
        "LapTime",
        "Compound",
        "TyreLife",
        "Position",
    ]

    print("\nRace results:")
    print(results[result_columns].head(10).to_string(index=False))

    print("\nSample lap records:")
    print(laps[lap_columns].head(10).to_string(index=False))

    print(f"\nDrivers returned: {len(results)}")
    print(f"Lap records returned: {len(laps)}")


if __name__ == "__main__":
    race_results, race_laps, race_metadata = load_race(
        season=2025,
        event_name="Monza",
    )

    display_summary(
        results=race_results,
        laps=race_laps,
        metadata=race_metadata,
    )
