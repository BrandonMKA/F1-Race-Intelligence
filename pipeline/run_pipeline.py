import argparse
import logging

from pipeline.extract.fetch_session import load_race
from pipeline.load.load_race import load_race_to_database
from pipeline.transform.transform_laps import transform_laps
from pipeline.transform.transform_results import transform_results
from pipeline.transform.validate import (
    raise_for_validation_errors,
    validate_laps,
    validate_results,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Extract, transform, validate and load an F1 race."
        )
    )

    parser.add_argument(
        "--season",
        required=True,
        type=int,
        help="F1 season, such as 2025.",
    )

    parser.add_argument(
        "--event",
        required=True,
        type=str,
        help='Event identifier, such as "Monza".',
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    try:

        logging.info("Extracting FastF1 data")

        raw_results, raw_laps, metadata = load_race(
            season=args.season,
            event_name=args.event,
        )

        logging.info("Transforming data")

        clean_results = transform_results(
            results=raw_results,
            metadata=metadata,
        )

        clean_laps = transform_laps(
            laps=raw_laps,
            metadata=metadata,
        )

        logging.info("Validating data")

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

        logging.info("Validation passed.")

        logging.info("Loading PostgreSQL")

        load_race_to_database(
            results=clean_results,
            laps=clean_laps,
            metadata=metadata,
        )

        logging.info("Pipeline completed successfully.")

    except Exception as e:
        logging.exception("Pipeline failed")
        raise

if __name__ == "__main__":
    main()