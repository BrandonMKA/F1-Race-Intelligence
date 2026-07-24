from pathlib import Path

from pipeline.load.database import get_connection


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PROJECT_ROOT / "database" / "schema.sql"
INDEXES_PATH = PROJECT_ROOT / "database" / "indexes.sql"


def read_sql_file(path: Path) -> str:
    """Read and return a SQL file."""

    if not path.exists():
        raise FileNotFoundError(f"SQL file does not exist: {path}")

    return path.read_text(encoding="utf-8")


def create_database_schema() -> None:
    """Create database tables and indexes."""

    schema_sql = read_sql_file(SCHEMA_PATH)
    indexes_sql = read_sql_file(INDEXES_PATH)

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(schema_sql)
            cursor.execute(indexes_sql)

    print("Database tables and indexes created successfully.")


if __name__ == "__main__":
    create_database_schema()