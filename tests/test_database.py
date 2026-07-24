from pipeline.load.database import get_connection


def test_database_connection() -> None:
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT 1 AS value;")
        result = cursor.fetchone()

    assert result is not None
    assert result["value"] == 1


def test_required_tables_exist() -> None:
    required_tables = {
        "dim_event",
        "dim_driver",
        "dim_constructor",
        "fact_result",
        "fact_lap",
        "pipeline_run",
    }

    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public';
                """)

        actual_tables = {row["table_name"] for row in cursor.fetchall()}

    assert required_tables.issubset(actual_tables)
