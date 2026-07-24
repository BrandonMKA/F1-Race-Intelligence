from pipeline.load.database import get_connection


def main() -> None:
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
                SELECT
                    current_database() AS database_name,
                    current_user AS database_user,
                    version() AS postgres_version;
                """)

        row = cursor.fetchone()

    if row is None:
        raise RuntimeError("The connection test returned no data.")

    print("Database connection successful.")
    print(f"Database: {row['database_name']}")
    print(f"User: {row['database_user']}")
    print(f"Version: {row['postgres_version']}")


if __name__ == "__main__":
    main()
