# Task Tracker — Development Guide

## Project Structure
- `task_tracker/` — Main package
  - `store.py` — JSON file-based task storage (TaskStore class)
  - `cli.py` — CLI entry point
- `tests/` — pytest test suite

## Conventions
- Python 3.10+, type hints everywhere
- Use `from __future__ import annotations` in all files
- Tests use pytest with `tmp_path` fixtures for file isolation
- Keep it simple — no external dependencies beyond stdlib + pytest

## Running Tests
```bash
pytest -v
```

## Adding Features
- New commands go in `cli.py`, new storage logic in `store.py`
- Always add corresponding tests in `tests/test_store.py`
- Follow existing patterns for dataclass fields and serialization
