from __future__ import annotations

import argparse
import logging
from datetime import datetime, timezone

from scripts.backfill_season import backfill_season

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def update_season(season: int | None = None) -> None:
    """Load completed races missing from the selected or current season."""

    now = datetime.now(timezone.utc)
    target_season = season or now.year

    logger.info(
        "Starting race-data update for season %s at %s.",
        target_season,
        now.isoformat(),
    )

    backfill_season(
        season=target_season,
        force=False,
    )

    logger.info(
        "Finished race-data update for season %s.",
        target_season,
    )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ingest newly completed F1 races."
    )

    parser.add_argument(
        "--season",
        type=int,
        help="Optional season override. Defaults to the current year.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    try:
        update_season(args.season)
    except Exception:
        logger.exception("Race-data update failed.")
        raise