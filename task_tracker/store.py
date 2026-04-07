"""JSON file-based task storage."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

DEFAULT_PATH = Path.home() / ".task_tracker.json"


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: str | None = None
    priority: str = "medium"  # low, medium, high


class TaskStore:
    """Persist tasks to a JSON file."""

    def __init__(self, path: Path = DEFAULT_PATH) -> None:
        self.path = path
        self._tasks: list[Task] = []
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            data = json.loads(self.path.read_text())
            self._tasks = [Task(**t) for t in data]
        else:
            self._tasks = []

    def _save(self) -> None:
        self.path.write_text(json.dumps([asdict(t) for t in self._tasks], indent=2))

    def _next_id(self) -> int:
        return max((t.id for t in self._tasks), default=0) + 1

    def add(self, title: str, priority: str = "medium") -> Task:
        task = Task(id=self._next_id(), title=title, priority=priority)
        self._tasks.append(task)
        self._save()
        return task

    def list_all(self, show_done: bool = False) -> list[Task]:
        if show_done:
            return list(self._tasks)
        return [t for t in self._tasks if not t.done]

    def get(self, task_id: int) -> Task | None:
        return next((t for t in self._tasks if t.id == task_id), None)

    def complete(self, task_id: int) -> Task | None:
        task = self.get(task_id)
        if task:
            task.done = True
            task.completed_at = datetime.now().isoformat()
            self._save()
        return task

    def remove(self, task_id: int) -> bool:
        before = len(self._tasks)
        self._tasks = [t for t in self._tasks if t.id != task_id]
        if len(self._tasks) < before:
            self._save()
            return True
        return False

    def stats(self) -> dict[str, int]:
        total = len(self._tasks)
        done = sum(1 for t in self._tasks if t.done)
        return {"total": total, "done": done, "pending": total - done}
