from typing import Any

import psycopg
from fastapi import APIRouter, Depends, HTTPException, status


from api.dependencies import get_database_connection


router = APIRouter(
    tags=["Health"],
)


@router.get("/health")
def health_check(
    connection: psycopg.Connection[dict[str, Any]] = Depends(
        get_database_connection
    ),
) -> dict[str, str]:
    """
    Confirm that the API and database are available.
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    current_database() AS database_name;
                """
            )

            row = cursor.fetchone()

        if row is None:
            raise RuntimeError(
                "Database health query returned no result."
            )

        return {
            "status": "healthy",
            "database": row["database_name"],
        }

    except psycopg.Error as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is unavailable.",
        ) from error