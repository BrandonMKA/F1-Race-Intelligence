from collections.abc import Generator
from typing import Any

import psycopg

from pipeline.load.database import get_connection


def get_database_connection(
) -> Generator[
    psycopg.Connection[dict[str, Any]],
    None,
    None,
]:
    """
    Provide one PostgreSQL connection for an API request.

    FastAPI closes the connection after the request completes.
    """

    connection = get_connection()

    try:
        yield connection
    finally:
        connection.close()