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

    target_season = season or datetime.now(timezone.utc).year

    logger.info(
        "Checking season %s for newly completed races.",
        target_season,
    )

    backfill_season(
        season=target_season,
        force=False,
    )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest newly completed F1 races.")

    parser.add_argument(
        "--season",
        type=int,
        help="Optional season override. Defaults to the current year.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    update_season(args.season)
