import os
from pathlib import Path
from typing import Any

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(ENV_PATH)


def get_database_url() -> str:
    """Return the configured PostgreSQL connection string."""

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not configured. "
            "Add it to the project's .env file."
        )

    return database_url


def get_connection() -> psycopg.Connection[dict[str, Any]]:
    """
    Open a PostgreSQL connection that returns query rows as dictionaries.
    """

    try:
        return psycopg.connect(
            get_database_url(),
            row_factory=dict_row,
            connect_timeout=15,
        )
    except psycopg.OperationalError as error:
        raise RuntimeError(
            "Could not connect to PostgreSQL. Check DATABASE_URL, "
            "network access, credentials, and database availability."
        ) from error