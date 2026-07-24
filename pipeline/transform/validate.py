import pandas as pd


class DataValidationError(ValueError):
    """Raised when transformed data fails quality checks."""


def validate_results(
    results: pd.DataFrame,
) -> list[str]:
    """Return a list of validation errors for race results."""

    errors: list[str] = []

    if results.empty:
        errors.append("Results table is empty.")
        return errors

    required_columns = [
        "season",
        "round_number",
        "event_name",
        "driver_code",
        "finish_position",
    ]

    missing_columns = [
        column for column in required_columns if column not in results.columns
    ]

    if missing_columns:
        errors.append(f"Results table is missing columns: {missing_columns}")

        return errors

    if results["driver_code"].isna().any():
        errors.append("Results contain null driver codes.")

    duplicate_count = results.duplicated(
        subset=[
            "season",
            "round_number",
            "session_name",
            "driver_code",
        ]
    ).sum()

    if duplicate_count > 0:
        errors.append(f"Results contain {duplicate_count} duplicate driver records.")

    valid_positions = results["finish_position"].dropna()

    if (valid_positions <= 0).any():
        errors.append("Results contain invalid finish positions.")

    if (results["points"] < 0).any():
        errors.append("Results contain negative points.")

    return errors


def validate_laps(
    laps: pd.DataFrame,
) -> list[str]:
    """Return a list of validation errors for lap data."""

    errors: list[str] = []

    if laps.empty:
        errors.append("Laps table is empty.")
        return errors

    required_columns = [
        "season",
        "round_number",
        "event_name",
        "driver_code",
        "lap_number",
        "lap_time_ms",
    ]

    missing_columns = [
        column for column in required_columns if column not in laps.columns
    ]

    if missing_columns:
        errors.append(f"Laps table is missing columns: {missing_columns}")

        return errors

    if laps["driver_code"].isna().any():
        errors.append("Laps contain null driver codes.")

    if laps["lap_number"].isna().any():
        errors.append("Laps contain null lap numbers.")

    valid_lap_numbers = laps["lap_number"].dropna()

    if (valid_lap_numbers <= 0).any():
        errors.append("Laps contain non-positive lap numbers.")

    valid_lap_times = laps["lap_time_ms"].dropna()

    if (valid_lap_times <= 0).any():
        errors.append("Laps contain non-positive lap times.")

    duplicate_count = laps.duplicated(
        subset=[
            "season",
            "round_number",
            "session_name",
            "driver_code",
            "lap_number",
        ]
    ).sum()

    if duplicate_count > 0:
        errors.append(f"Laps contain {duplicate_count} duplicate driver-lap records.")

    return errors


def raise_for_validation_errors(
    dataset_name: str,
    errors: list[str],
) -> None:
    """Raise an exception if any validation errors exist."""

    if not errors:
        return

    formatted_errors = "\n".join(f"- {error}" for error in errors)

    raise DataValidationError(f"{dataset_name} failed validation:\n{formatted_errors}")
