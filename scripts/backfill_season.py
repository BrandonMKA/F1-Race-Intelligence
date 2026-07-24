from __future__ import annotations

import argparse
import logging
import time

from pipeline.run_pipeline import run_pipeline
from scripts.race_schedule import (
    get_completed_races,
    get_loaded_rounds,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def backfill_season(
    season: int,
    start_round: int = 1,
    end_round: int | None = None,
    force: bool = False,
    delay_seconds: int = 2,
) -> None:
    """Load every completed race missing from a season."""

    completed_races = get_completed_races(
        season=season,
        start_round=start_round,
        end_round=end_round,
    )

    loaded_rounds = get_loaded_rounds(season)

    loaded_now: list[int] = []
    skipped: list[int] = []
    failed: list[tuple[int, str]] = []

    logger.info(
        "Found %s completed races in %s; %s are already loaded.",
        len(completed_races),
        season,
        len(loaded_rounds),
    )

    for race in completed_races:
        round_number = race["round_number"]
        event_name = race["event_name"]

        if round_number in loaded_rounds and not force:
            logger.info(
                "Skipping round %s (%s): already loaded.",
                round_number,
                event_name,
            )
            skipped.append(round_number)
            continue

        try:
            logger.info(
                "Loading round %s: %s",
                round_number,
                event_name,
            )

            run_pipeline(
                season=season,
                event=round_number,
            )

            loaded_now.append(round_number)

        except Exception as error:
            logger.exception(
                "Failed to load round %s: %s",
                round_number,
                event_name,
            )
            failed.append((round_number, str(error)))

        if delay_seconds > 0:
            time.sleep(delay_seconds)

    print("\nBackfill summary")
    print(f"Season: {season}")
    print(f"Loaded now: {len(loaded_now)}")
    print(f"Already loaded: {len(skipped)}")
    print(f"Failed: {len(failed)}")

    if loaded_now:
        print("Loaded rounds: " + ", ".join(map(str, loaded_now)))

    if failed:
        for round_number, error in failed:
            print(f"Round {round_number} failed: {error}")

        raise SystemExit(1)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Backfill completed races for an F1 season."
    )

    parser.add_argument("--season", type=int, required=True)
    parser.add_argument("--start-round", type=int, default=1)
    parser.add_argument("--end-round", type=int)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Reload races even when they are already in PostgreSQL.",
    )
    parser.add_argument("--delay-seconds", type=int, default=2)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    backfill_season(
        season=args.season,
        start_round=args.start_round,
        end_round=args.end_round,
        force=args.force,
        delay_seconds=args.delay_seconds,
    )
