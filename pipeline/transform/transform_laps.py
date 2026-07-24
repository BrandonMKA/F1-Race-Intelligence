from typing import Any

import pandas as pd

LAP_COLUMN_MAP = {
    "Driver": "driver_code",
    "DriverNumber": "driver_number",
    "LapNumber": "lap_number",
    "LapTime": "lap_time",
    "Sector1Time": "sector_1_time",
    "Sector2Time": "sector_2_time",
    "Sector3Time": "sector_3_time",
    "Stint": "stint_number",
    "Compound": "compound",
    "TyreLife": "tire_life",
    "Position": "position",
    "PitInTime": "pit_in_time",
    "PitOutTime": "pit_out_time",
    "IsPersonalBest": "is_personal_best",
}


def timedelta_to_milliseconds(
    series: pd.Series,
) -> pd.Series:
    """
    Convert a Pandas timedelta Series into nullable integer milliseconds.
    """

    milliseconds = series.dt.total_seconds() * 1000

    return milliseconds.round().astype("Int64")


def transform_laps(
    laps: pd.DataFrame,
    metadata: dict[str, Any],
) -> pd.DataFrame:
    """
    Convert raw FastF1 lap data into a clean database-ready table.
    """

    missing_columns = [
        column for column in LAP_COLUMN_MAP if column not in laps.columns
    ]

    if missing_columns:
        raise ValueError(f"Lap data is missing required columns: {missing_columns}")

    clean_laps = laps[list(LAP_COLUMN_MAP)].copy()

    clean_laps = clean_laps.rename(columns=LAP_COLUMN_MAP)

    clean_laps.insert(
        0,
        "season",
        metadata["season"],
    )

    clean_laps.insert(
        1,
        "round_number",
        metadata["round_number"],
    )

    clean_laps.insert(
        2,
        "event_name",
        metadata["event_name"],
    )

    clean_laps.insert(
        3,
        "session_name",
        metadata["session_name"],
    )

    clean_laps["driver_code"] = (
        clean_laps["driver_code"].astype("string").str.strip().str.upper()
    )

    integer_columns = [
        "driver_number",
        "lap_number",
        "stint_number",
        "tire_life",
        "position",
    ]

    for column in integer_columns:
        clean_laps[column] = pd.to_numeric(
            clean_laps[column],
            errors="coerce",
        ).astype("Int64")

    clean_laps["lap_time_ms"] = timedelta_to_milliseconds(clean_laps["lap_time"])

    clean_laps["sector_1_ms"] = timedelta_to_milliseconds(clean_laps["sector_1_time"])

    clean_laps["sector_2_ms"] = timedelta_to_milliseconds(clean_laps["sector_2_time"])

    clean_laps["sector_3_ms"] = timedelta_to_milliseconds(clean_laps["sector_3_time"])

    clean_laps["compound"] = (
        clean_laps["compound"].astype("string").str.strip().str.upper()
    )

    clean_laps["is_personal_best"] = (
        clean_laps["is_personal_best"].fillna(False).astype(bool)
    )

    clean_laps["pit_in"] = clean_laps["pit_in_time"].notna()
    clean_laps["pit_out"] = clean_laps["pit_out_time"].notna()

    clean_laps = clean_laps.drop(
        columns=[
            "lap_time",
            "sector_1_time",
            "sector_2_time",
            "sector_3_time",
            "pit_in_time",
            "pit_out_time",
        ]
    )

    clean_laps = clean_laps.dropna(
        subset=[
            "driver_code",
            "lap_number",
        ]
    )

    clean_laps = clean_laps.drop_duplicates(
        subset=[
            "season",
            "round_number",
            "session_name",
            "driver_code",
            "lap_number",
        ],
        keep="last",
    )

    clean_laps = clean_laps.sort_values(
        by=[
            "lap_number",
            "position",
            "driver_code",
        ],
        na_position="last",
    ).reset_index(drop=True)

    return clean_laps
