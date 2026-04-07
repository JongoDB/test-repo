"""Tests for TaskStore."""

from pathlib import Path

import pytest

from task_tracker.store import TaskStore


@pytest.fixture
def store(tmp_path: Path) -> TaskStore:
    return TaskStore(path=tmp_path / "tasks.json")


def test_add_task(store: TaskStore) -> None:
    task = store.add("Buy milk")
    assert task.id == 1
    assert task.title == "Buy milk"
    assert task.done is False
    assert task.priority == "medium"


def test_add_with_priority(store: TaskStore) -> None:
    task = store.add("Fix bug", priority="high")
    assert task.priority == "high"


def test_list_pending(store: TaskStore) -> None:
    store.add("Task A")
    store.add("Task B")
    store.complete(1)
    pending = store.list_all(show_done=False)
    assert len(pending) == 1
    assert pending[0].title == "Task B"


def test_list_all(store: TaskStore) -> None:
    store.add("Task A")
    store.add("Task B")
    store.complete(1)
    all_tasks = store.list_all(show_done=True)
    assert len(all_tasks) == 2


def test_complete_task(store: TaskStore) -> None:
    store.add("Task A")
    task = store.complete(1)
    assert task is not None
    assert task.done is True
    assert task.completed_at is not None


def test_complete_nonexistent(store: TaskStore) -> None:
    result = store.complete(999)
    assert result is None


def test_remove_task(store: TaskStore) -> None:
    store.add("Task A")
    assert store.remove(1) is True
    assert store.list_all(show_done=True) == []


def test_remove_nonexistent(store: TaskStore) -> None:
    assert store.remove(999) is False


def test_stats(store: TaskStore) -> None:
    store.add("A")
    store.add("B")
    store.add("C")
    store.complete(1)
    s = store.stats()
    assert s == {"total": 3, "done": 1, "pending": 2}


def test_persistence(tmp_path: Path) -> None:
    path = tmp_path / "tasks.json"
    s1 = TaskStore(path=path)
    s1.add("Persistent task")
    s2 = TaskStore(path=path)
    assert len(s2.list_all(show_done=True)) == 1
    assert s2.list_all(show_done=True)[0].title == "Persistent task"


def test_auto_increment_ids(store: TaskStore) -> None:
    store.add("A")
    store.add("B")
    store.remove(1)
    task = store.add("C")
    assert task.id == 3  # Should not reuse ID 1
