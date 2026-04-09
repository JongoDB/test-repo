"""PostgreSQL-based task storage."""

from __future__ import annotations

import os
from datetime import datetime

from task_tracker.store import Task


class PostgreSQLTaskStore:
    """Persist tasks to a PostgreSQL database."""

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        database: str | None = None,
        user: str | None = None,
        password: str | None = None,
    ) -> None:
        # Import here to make psycopg2 optional
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
        except ImportError as e:
            raise ImportError(
                "psycopg2-binary is required for PostgreSQL support. "
                "Install with: pip install .[postgresql]"
            ) from e

        self.host = host or os.getenv("POSTGRES_HOST", "localhost")
        self.port = port or int(os.getenv("POSTGRES_PORT", "5432"))
        self.database = database or os.getenv("POSTGRES_DB", "task_tracker")
        self.user = user or os.getenv("POSTGRES_USER", "task_tracker_user")
        self.password = password or os.getenv("POSTGRES_PASSWORD", "")

        self.connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
        )
        self.connection.autocommit = True
        self.cursor_class = RealDictCursor
        self._initialize_schema()

    def _initialize_schema(self) -> None:
        """Create the tasks table if it doesn't exist."""
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(500) NOT NULL,
                    done BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP NULL,
                    priority VARCHAR(10) DEFAULT 'medium'
                )
            """)

    def _row_to_task(self, row: dict) -> Task:
        """Convert a database row to a Task object."""
        return Task(
            id=row["id"],
            title=row["title"],
            done=row["done"],
            created_at=row["created_at"].isoformat(),
            completed_at=row["completed_at"].isoformat() if row["completed_at"] else None,
            priority=row["priority"],
        )

    def add(self, title: str, priority: str = "medium") -> Task:
        """Add a new task."""
        with self.connection.cursor(cursor_factory=self.cursor_class) as cursor:
            cursor.execute(
                """
                INSERT INTO tasks (title, priority)
                VALUES (%s, %s)
                RETURNING id, title, done, created_at, completed_at, priority
                """,
                (title, priority),
            )
            row = cursor.fetchone()
            return self._row_to_task(row)

    def list_all(self, show_done: bool = False) -> list[Task]:
        """List all tasks, optionally filtering out completed ones."""
        with self.connection.cursor(cursor_factory=self.cursor_class) as cursor:
            if show_done:
                cursor.execute("SELECT * FROM tasks ORDER BY id")
            else:
                cursor.execute("SELECT * FROM tasks WHERE NOT done ORDER BY id")
            rows = cursor.fetchall()
            return [self._row_to_task(row) for row in rows]

    def get(self, task_id: int) -> Task | None:
        """Get a task by ID."""
        with self.connection.cursor(cursor_factory=self.cursor_class) as cursor:
            cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
            row = cursor.fetchone()
            return self._row_to_task(row) if row else None

    def complete(self, task_id: int) -> Task | None:
        """Mark a task as completed."""
        with self.connection.cursor(cursor_factory=self.cursor_class) as cursor:
            cursor.execute(
                """
                UPDATE tasks
                SET done = TRUE, completed_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING id, title, done, created_at, completed_at, priority
                """,
                (task_id,),
            )
            row = cursor.fetchone()
            return self._row_to_task(row) if row else None

    def remove(self, task_id: int) -> bool:
        """Remove a task by ID."""
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            return cursor.rowcount > 0

    def stats(self) -> dict[str, int]:
        """Get task statistics."""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as total FROM tasks")
            total = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) as done FROM tasks WHERE done = TRUE")
            done = cursor.fetchone()[0]

            return {"total": total, "done": done, "pending": total - done}

    def close(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()

    def __del__(self) -> None:
        """Ensure connection is closed when object is destroyed."""
        self.close()