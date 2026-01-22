# Phase I - In-Memory Python Console Todo Application

A simple console-based todo application with in-memory storage, designed for learning spec-driven development.

## Features

- Add, list, update, delete, and toggle completion status of tasks
- Sequential ID assignment starting from 1
- Creation and modification timestamps
- Confirmation prompts for destructive operations
- Case-insensitive commands

## Prerequisites

- Python 3.13+
- UV package manager

## Setup

1. Clone the repository
2. Install dependencies: `uv sync` or `pip install -e .[dev]`
3. Run the application: `python -m src.cli.main`

## Usage

The application runs in an interactive console loop. Available commands:

- `add "task title" ["optional description"]` - Add a new task
- `list` - Show all tasks with status and timestamps
- `toggle <task_id>` - Mark task as complete/incomplete
- `update <task_id> "new title" ["new description"]` - Update task details
- `delete <task_id>` - Delete a task (with confirmation)
- `quit` - Exit the application

### Example Commands

```
add "Buy groceries" "Milk, bread, eggs"
list
toggle 1
update 1 "Updated title" "Updated description"
delete 1
quit
```

## Development

### Running Tests

```bash
# Run all tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=src --cov-report=html
```

### Code Quality

```bash
# Type checking
python -m mypy src/

# Linting
python -m ruff check src/
```
