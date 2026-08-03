import sqlite3
from pathlib import Path


# Store tasks.db inside the project folder.
DATABASE_PATH = Path(__file__).resolve().parent / "tasks.db"


def initialize_database() -> None:
    """Create the tasks database, table, and initial sample data."""

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
                    CHECK (done IN (0, 1))
            )
            """
        )

        task_count = connection.execute(
            "SELECT COUNT(*) FROM tasks"
        ).fetchone()[0]

        # Seed the database only when the table is empty.
        if task_count == 0:
            example_tasks = [
                ("Learn FastAPI", 0),
                ("Build a CRUD API", 0),
                ("Upload project to GitHub", 1),
            ]

            connection.executemany(
                """
                INSERT INTO tasks (title, done)
                VALUES (?, ?)
                """,
                example_tasks,
            )

        connection.commit()

    finally:
        connection.close()