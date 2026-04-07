"""CLI interface for Task Tracker."""

from __future__ import annotations

import sys

from task_tracker.store import TaskStore


def main() -> None:
    store = TaskStore()
    args = sys.argv[1:]

    if not args:
        print("Usage: task-tracker <command> [args]")
        print("Commands: add, list, done, remove, stats")
        sys.exit(1)

    cmd = args[0]

    if cmd == "add":
        if len(args) < 2:
            print("Usage: task-tracker add <title> [--priority low|medium|high]")
            sys.exit(1)
        priority = "medium"
        title_parts = []
        i = 1
        while i < len(args):
            if args[i] == "--priority" and i + 1 < len(args):
                priority = args[i + 1]
                i += 2
            else:
                title_parts.append(args[i])
                i += 1
        title = " ".join(title_parts)
        task = store.add(title, priority=priority)
        print(f"Added task #{task.id}: {task.title} [{task.priority}]")

    elif cmd == "list":
        show_done = "--all" in args
        tasks = store.list_all(show_done=show_done)
        if not tasks:
            print("No tasks.")
            return
        for t in tasks:
            status = "[x]" if t.done else "[ ]"
            print(f"  {status} #{t.id} {t.title} ({t.priority})")

    elif cmd == "done":
        if len(args) < 2:
            print("Usage: task-tracker done <id>")
            sys.exit(1)
        task = store.complete(int(args[1]))
        if task:
            print(f"Completed: #{task.id} {task.title}")
        else:
            print(f"Task #{args[1]} not found.")

    elif cmd == "remove":
        if len(args) < 2:
            print("Usage: task-tracker remove <id>")
            sys.exit(1)
        if store.remove(int(args[1])):
            print(f"Removed task #{args[1]}.")
        else:
            print(f"Task #{args[1]} not found.")

    elif cmd == "stats":
        s = store.stats()
        print(f"Total: {s['total']}  Done: {s['done']}  Pending: {s['pending']}")

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
