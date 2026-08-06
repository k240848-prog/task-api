import psycopg
from psycopg.rows import dict_row

from app.repositories.base import Task, TaskRepository


class PostgresTaskRepository(TaskRepository):
    def __init__(self, database_url: str) -> None:
        if not database_url:
            raise ValueError("DATABASE_URL is required")
        self._database_url = database_url

    def _connect(self):
        return psycopg.connect(self._database_url, row_factory=dict_row)

    def check_health(self) -> None:
        with self._connect() as connection:
            connection.execute("SELECT 1")

    def get_all(self) -> list[Task]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT id, title, done FROM tasks ORDER BY id"
            ).fetchall()
            return [dict(row) for row in rows]

    def get_by_id(self, task_id: int) -> Task | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT id, title, done FROM tasks WHERE id = %s",
                (task_id,),
            ).fetchone()
            return dict(row) if row is not None else None

    def create(self, title: str) -> Task:
        with self._connect() as connection:
            row = connection.execute(
                """
                INSERT INTO tasks (title, done)
                VALUES (%s, FALSE)
                RETURNING id, title, done
                """,
                (title,),
            ).fetchone()
            return dict(row)

    def update(self, task_id: int, title: str, done: bool) -> Task | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                UPDATE tasks
                SET title = %s, done = %s
                WHERE id = %s
                RETURNING id, title, done
                """,
                (title, done, task_id),
            ).fetchone()
            return dict(row) if row is not None else None

    def delete(self, task_id: int) -> bool:
        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM tasks WHERE id = %s",
                (task_id,),
            )
            return cursor.rowcount > 0
