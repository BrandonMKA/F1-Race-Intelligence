from pipeline.load.database import get_connection


def main() -> None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    current_database() AS database_name,
                    current_user AS database_user,
                    version() AS postgres_version;
                """
            )

            result = cursor.fetchone()

    if result is None:
        raise RuntimeError("PostgreSQL returned no connection information.")

    print("Database connection successful.")
    print(f"Database: {result['database_name']}")
    print(f"User: {result['database_user']}")
    print(f"Version: {result['postgres_version']}")


if __name__ == "__main__":
    main()