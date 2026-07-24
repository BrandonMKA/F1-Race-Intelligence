from __future__ import annotations

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

logger = logging.getLogger(__name__)


def run_pipeline(
    season: int,
    event: str | int,
) -> None:
    """Extract, transform, validate, and load one F1 race."""

    logger.info(
        "Starting pipeline for season=%s event=%s",
        season,
        event,
    )

    raw_results, raw_laps, metadata = load_race(
        season=season,
        event_name=event,
    )

    logger.info("Transforming data")

    clean_results = transform_results(
        results=raw_results,
        metadata=metadata,
    )

    clean_laps = transform_laps(
        laps=raw_laps,
        metadata=metadata,
    )

    logger.info("Validating data")

    raise_for_validation_errors(
        dataset_name="Results",
        errors=validate_results(clean_results),
    )

    raise_for_validation_errors(
        dataset_name="Laps",
        errors=validate_laps(clean_laps),
    )

    logger.info("Loading PostgreSQL")

    load_race_to_database(
        results=clean_results,
        laps=clean_laps,
        metadata=metadata,
    )

    logger.info(
        "Pipeline completed successfully for %s round %s: %s",
        metadata["season"],
        metadata["round_number"],
        metadata["event_name"],
    )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract, transform, validate, and load an F1 race."
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
        help='Event name or round number, such as "Monza" or "16".',
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    event: str | int

    event = int(args.event) if args.event.isdigit() else args.event

    try:
        run_pipeline(
            season=args.season,
            event=event,
        )
    except Exception:
        logger.exception("Pipeline failed")
        raise


if __name__ == "__main__":
    main()
