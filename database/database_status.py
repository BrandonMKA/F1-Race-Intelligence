from pipeline.load.database import get_connection

TABLES = [
    "dim_event",
    "dim_driver",
    "dim_constructor",
    "fact_result",
    "fact_lap",
    "pipeline_run",
]


def main() -> None:
    with get_connection() as connection, connection.cursor() as cursor:
        print("F1 Race Intelligence Database")
        print("-" * 40)

        for table_name in TABLES:
            cursor.execute(f"SELECT COUNT(*) AS row_count FROM {table_name};")

            row = cursor.fetchone()

            if row is None:
                raise RuntimeError(f"Could not count rows in {table_name}.")

            print(f"{table_name:<20} " f"{row['row_count']:>10,} rows")


if __name__ == "__main__":
    main()
