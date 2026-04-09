# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.0.0] - 2026-04-08

### Added
- Core task management functionality with create, list, complete, and remove operations
- Priority system supporting low, medium, and high priority levels
- Task completion tracking with creation and completion timestamps
- Statistics command to view total, completed, and pending task counts
- JSON file-based persistence to store tasks locally
- Command-line interface with intuitive commands:
  - `add <title> [--priority low|medium|high]` - Create new tasks
  - `list [--all]` - Show pending tasks or all tasks including completed
  - `done <id>` - Mark tasks as completed
  - `remove <id>` - Delete tasks
  - `stats` - Display task statistics
- Comprehensive test suite using pytest
- Type hints throughout codebase for better development experience

### Technical Details
- Python 3.10+ compatibility
- JSON-based task storage in `~/.task_tracker.json`
- Dataclass-based Task model with automatic ID generation
- CLI entry point via `task-tracker` command after installation

[v1.0.0]: https://github.com/JongoDB/test-repo/releases/tag/v1.0.0