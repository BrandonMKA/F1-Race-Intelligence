from typing import Any

import pandas as pd


RESULT_COLUMN_MAP = {
    "DriverNumber": "driver_number",
    "Abbreviation": "driver_code",
    "FirstName": "first_name",
    "LastName": "last_name",
    "FullName": "full_name",
    "TeamName": "constructor_name",
    "GridPosition": "grid_position",
    "Position": "finish_position",
    "Points": "points",
    "Status": "status",
}


def transform_results(
    results: pd.DataFrame,
    metadata: dict[str, Any],
) -> pd.DataFrame:
    """
    Convert raw FastF1 race results into a clean database-ready table.
    """

    missing_columns = [
        column
        for column in RESULT_COLUMN_MAP
        if column not in results.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Results data is missing required columns: {missing_columns}"
        )

    clean_results = results[list(RESULT_COLUMN_MAP)].copy()

    clean_results = clean_results.rename(
        columns=RESULT_COLUMN_MAP
    )

    clean_results.insert(
        0,
        "season",
        metadata["season"],
    )

    clean_results.insert(
        1,
        "round_number",
        metadata["round_number"],
    )

    clean_results.insert(
        2,
        "event_name",
        metadata["event_name"],
    )

    clean_results.insert(
        3,
        "session_name",
        metadata["session_name"],
    )

    clean_results["driver_number"] = pd.to_numeric(
        clean_results["driver_number"],
        errors="coerce",
    ).astype("Int64")

    clean_results["grid_position"] = pd.to_numeric(
        clean_results["grid_position"],
        errors="coerce",
    ).astype("Int64")

    clean_results["finish_position"] = pd.to_numeric(
        clean_results["finish_position"],
        errors="coerce",
    ).astype("Int64")

    clean_results["points"] = pd.to_numeric(
        clean_results["points"],
        errors="coerce",
    ).fillna(0.0)

    text_columns = [
        "driver_code",
        "first_name",
        "last_name",
        "full_name",
        "constructor_name",
        "status",
    ]

    for column in text_columns:
        clean_results[column] = (
            clean_results[column]
            .astype("string")
            .str.strip()
        )

    clean_results["driver_code"] = (
        clean_results["driver_code"]
        .str.upper()
    )

    clean_results = clean_results.drop_duplicates(
        subset=[
            "season",
            "round_number",
            "session_name",
            "driver_code",
        ]
    )

    clean_results = clean_results.sort_values(
        by="finish_position",
        na_position="last",
    ).reset_index(drop=True)

    return clean_results