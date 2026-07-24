from pathlib import Path

from pipeline.extract.fetch_session import load_race
from pipeline.transform.transform_laps import transform_laps
from pipeline.transform.transform_results import transform_results
from pipeline.transform.validate import (
    raise_for_validation_errors,
    validate_laps,
    validate_results,
)


PROCESSED_DATA_DIR = Path("data/processed")


def main() -> None:
    """Extract, transform, validate and save one race."""

    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    raw_results, raw_laps, metadata = load_race(
        season=2025,
        event_name="Monza",
    )

    clean_results = transform_results(
        results=raw_results,
        metadata=metadata,
    )

    clean_laps = transform_laps(
        laps=raw_laps,
        metadata=metadata,
    )

    result_errors = validate_results(clean_results)
    lap_errors = validate_laps(clean_laps)

    raise_for_validation_errors(
        dataset_name="Results",
        errors=result_errors,
    )

    raise_for_validation_errors(
        dataset_name="Laps",
        errors=lap_errors,
    )

    results_path = (
        PROCESSED_DATA_DIR
        / "2025_monza_results.csv"
    )

    laps_path = (
        PROCESSED_DATA_DIR
        / "2025_monza_laps.csv"
    )

    clean_results.to_csv(
        results_path,
        index=False,
    )

    clean_laps.to_csv(
        laps_path,
        index=False,
    )

    print("\nTransformation completed successfully.")

    print(
        f"Results: {len(clean_results):,} rows "
        f"saved to {results_path}"
    )

    print(
        f"Laps: {len(clean_laps):,} rows "
        f"saved to {laps_path}"
    )

    print("\nClean results preview:")
    print(clean_results.head().to_string(index=False))

    print("\nClean laps preview:")
    print(clean_laps.head().to_string(index=False))

    print("\nClean lap column types:")
    print(clean_laps.dtypes)

    fastest_laps = (
        clean_laps
        .dropna(subset=["lap_time_ms"])
        .sort_values("lap_time_ms")
        .loc[
            :,
            [
                "driver_code",
                "lap_number",
                "lap_time_ms",
                "compound",
            ],
        ]
        .head(10)
    )

    print("\nTen fastest laps:")
    print(fastest_laps.to_string(index=False))

    average_driver_pace = (
        clean_laps
        .dropna(subset=["lap_time_ms"])
        .groupby("driver_code", as_index=False)
        .agg(
            average_lap_time_ms=(
                "lap_time_ms",
                "mean",
            ),
            completed_laps=(
                "lap_number",
                "count",
            ),
        )
        .sort_values("average_lap_time_ms")
    )

    print("\nAverage lap time by driver:")
    print(average_driver_pace.head(10).to_string(index=False))


if __name__ == "__main__":
    main()