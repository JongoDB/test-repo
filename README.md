# Task Tracker CLI

A simple Python command-line task tracker for testing UKB pipeline integration.

## Usage

```bash
python -m task_tracker add "Buy groceries"
python -m task_tracker list
python -m task_tracker done 1
python -m task_tracker remove 1
python -m task_tracker stats
```

## Development

```bash
pip install -e ".[dev]"
pytest
```
