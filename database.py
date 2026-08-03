import sqlite3
from pathlib import Path
from typing import Any


DATABASE_PATH = Path(__file__).resolve().parent / "tasks.db"


def get_connection() -> sqlite3.Connection:
    """Create and return a SQLite database connection."""

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    """Create the table and add sample tasks only when empty."""

    connection = get_connection()

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


def convert_row_to_task(row: sqlite3.Row) -> dict[str, Any]:
    """Convert a database row into the API task format."""

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"]),
    }


def fetch_all_tasks() -> list[dict[str, Any]]:
    """Return every task stored in SQLite."""

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT id, title, done
            FROM tasks
            ORDER BY id
            """
        ).fetchall()

        return [convert_row_to_task(row) for row in rows]

    finally:
        connection.close()


def fetch_task_by_id(task_id: int) -> dict[str, Any] | None:
    """Return one task by ID or None if it does not exist."""

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT id, title, done
            FROM tasks
            WHERE id = ?
            """,
            (task_id,),
        ).fetchone()

        if row is None:
            return None

        return convert_row_to_task(row)

    finally:
        connection.close()


def insert_task(title: str) -> dict[str, Any]:
    """Insert a new task and return the created database row."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO tasks (title, done)
            VALUES (?, ?)
            """,
            (title, 0),
        )

        connection.commit()

        new_task_id = cursor.lastrowid

        row = connection.execute(
            """
            SELECT id, title, done
            FROM tasks
            WHERE id = ?
            """,
            (new_task_id,),
        ).fetchone()

        return convert_row_to_task(row)

    finally:
        connection.close()