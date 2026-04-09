"""Tests for PostgreSQL TaskStore.

These tests require a PostgreSQL instance to be available and configured.
They will be skipped if psycopg2 is not installed or if the database connection fails.
"""

from __future__ import annotations

import os
import pytest

# Try to import PostgreSQL dependencies
try:
    import psycopg2
    from task_tracker.postgres_store import PostgreSQLTaskStore
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False


@pytest.fixture
def postgres_store() -> PostgreSQLTaskStore:
    """Create a PostgreSQL store for testing.

    Requires environment variables:
    - POSTGRES_TEST_HOST (default: localhost)
    - POSTGRES_TEST_PORT (default: 5432)
    - POSTGRES_TEST_DB (default: task_tracker_test)
    - POSTGRES_TEST_USER (default: task_tracker_user)
    - POSTGRES_TEST_PASSWORD (default: empty)
    """
    if not POSTGRES_AVAILABLE:
        pytest.skip("psycopg2-binary not installed")

    host = os.getenv("POSTGRES_TEST_HOST", "localhost")
    port = int(os.getenv("POSTGRES_TEST_PORT", "5432"))
    database = os.getenv("POSTGRES_TEST_DB", "task_tracker_test")
    user = os.getenv("POSTGRES_TEST_USER", "task_tracker_user")
    password = os.getenv("POSTGRES_TEST_PASSWORD", "")

    try:
        store = PostgreSQLTaskStore(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        )

        # Clean up any existing test data
        with store.connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE tasks RESTART IDENTITY")

        yield store

        # Clean up after test
        with store.connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE tasks RESTART IDENTITY")

        store.close()

    except psycopg2.OperationalError as e:
        pytest.skip(f"PostgreSQL connection failed: {e}")


@pytest.mark.skipif(not POSTGRES_AVAILABLE, reason="psycopg2-binary not installed")
def test_add_task(postgres_store: PostgreSQLTaskStore) -> None:
    task = postgres_store.add("Buy milk")
    assert task.id == 1
    assert task.title == "Buy milk"
    assert task.done is False
    assert task.priority == "medium"


@pytest.mark.skipif(not POSTGRES_AVAILABLE, reason="psycopg2-binary not installed")
def test_add_with_priority(postgres_store: PostgreSQLTaskStore) -> None:
    task = postgres_store.add("Fix bug", priority="high")
    assert task.priority == "high"


@pytest.mark.skipif(not POSTGRES_AVAILABLE, reason="psycopg2-binary not installed")
def test_list_pending(postgres_store: PostgreSQLTaskStore) -> None:
    postgres_store.add("Task A")
    postgres_store.add("Task B")
    postgres_store.complete(1)
    pending = postgres_store.list_all(show_done=False)
    assert len(pending) == 1
    assert pending[0].title == "Task B"


@pytest.mark.skipif(not POSTGRES_AVAILABLE, reason="psycopg2-binary not installed")
def test_list_all(postgres_store: PostgreSQLTaskStore) -> None:
    postgres_store.add("Task A")
    postgres_store.add("Task B")
    postgres_store.complete(1)
    all_tasks = postgres_store.list_all(show_done=True)
    assert len(all_tasks) == 2


@pytest.mark.skipif(not POSTGRES_AVAILABLE, reason="psycopg2-binary not installed")
def test_complete_task(postgres_store: PostgreSQLTaskStore) -> None:
    postgres_store.add("Task A")
    task = postgres_store.complete(1)
    assert task is not None
    assert task.done is True
    assert task.completed_at is not None


@pytest.mark.skipif(not POSTGRES_AVAILABLE, reason="psycopg2-binary not installed")
def test_complete_nonexistent(postgres_store: PostgreSQLTaskStore) -> None:
    result = postgres_store.complete(999)
    assert result is None


@pytest.mark.skipif(not POSTGRES_AVAILABLE, reason="psycopg2-binary not installed")
def test_remove_task(postgres_store: PostgreSQLTaskStore) -> None:
    postgres_store.add("Task A")
    assert postgres_store.remove(1) is True
    assert postgres_store.list_all(show_done=True) == []


@pytest.mark.skipif(not POSTGRES_AVAILABLE, reason="psycopg2-binary not installed")
def test_remove_nonexistent(postgres_store: PostgreSQLTaskStore) -> None:
    assert postgres_store.remove(999) is False


@pytest.mark.skipif(not POSTGRES_AVAILABLE, reason="psycopg2-binary not installed")
def test_stats(postgres_store: PostgreSQLTaskStore) -> None:
    postgres_store.add("A")
    postgres_store.add("B")
    postgres_store.add("C")
    postgres_store.complete(1)
    s = postgres_store.stats()
    assert s == {"total": 3, "done": 1, "pending": 2}


@pytest.mark.skipif(not POSTGRES_AVAILABLE, reason="psycopg2-binary not installed")
def test_auto_increment_ids(postgres_store: PostgreSQLTaskStore) -> None:
    postgres_store.add("A")
    postgres_store.add("B")
    postgres_store.remove(1)
    task = postgres_store.add("C")
    assert task.id == 3  # PostgreSQL sequences continue incrementing


@pytest.mark.skipif(not POSTGRES_AVAILABLE, reason="psycopg2-binary not installed")
def test_get_task(postgres_store: PostgreSQLTaskStore) -> None:
    added_task = postgres_store.add("Test task")
    retrieved_task = postgres_store.get(added_task.id)
    assert retrieved_task is not None
    assert retrieved_task.id == added_task.id
    assert retrieved_task.title == "Test task"


@pytest.mark.skipif(not POSTGRES_AVAILABLE, reason="psycopg2-binary not installed")
def test_get_nonexistent_task(postgres_store: PostgreSQLTaskStore) -> None:
    task = postgres_store.get(999)
    assert task is None