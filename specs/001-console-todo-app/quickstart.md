# Quickstart Guide: Phase I - In-Memory Python Console Todo Application

## Prerequisites
- Python 3.13+ installed
- UV package manager installed

## Setup Instructions

### 1. Clone or Create Project Directory
```bash
mkdir phase1-console-todo
cd phase1-console-todo
```

### 2. Initialize UV Project
```bash
uv init
```

### 3. Create Project Structure
```bash
mkdir -p src/{models,services,ui}
mkdir -p tests/{unit,integration}
```

### 4. Install Dependencies
```bash
uv add pytest pytest-cov mypy ruff
```

### 5. Update pyproject.toml
```toml
[project]
name = "phase1-console-todo"
version = "0.1.0"
description = "Phase I - In-Memory Python Console Todo Application"
requires-python = ">=3.13"

dependencies = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "mypy>=1.0",
    "ruff>=0.0.270"
]

[tool.uv]
dev-dependencies = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "mypy>=1.0",
    "ruff>=0.0.270"
]
```

## File Structure Overview
```
phase1-console-todo/
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   └── task.py
│   ├── services/
│   │   └── task_service.py
│   └── ui/
│       └── console_ui.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_task.py
│   │   └── test_task_service.py
│   └── integration/
│       └── test_main_flow.py
├── README.md
├── CLAUDE.md
└── AGENTS.md
```

## Key Components

### 1. Task Model (`src/models/task.py`)
- Dataclass with type hints for all fields
- Immutable created_at timestamp
- Proper __str__ and __repr__ methods

### 2. Task Service (`src/services/task_service.py`)
- Core business logic implementation
- In-memory storage using dict[int, Task]
- Auto-incrementing ID management
- Input validation for all operations

### 3. Console UI (`src/ui/console_ui.py`)
- Interactive command loop
- Clear user prompts and error messages
- Confirmation for destructive actions

### 4. Main Application (`src/main.py`)
- Entry point for the application
- Wiring of UI and Service layers
- Graceful shutdown handling

## Running the Application
```bash
python -m src.main
```

## Testing
```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=html

# Run type checking
uv run mypy src/

# Run linting
uv run ruff check src/
```

## Available Commands in Console UI
- `add <title> [description]` - Add a new task
- `list` - Show all tasks
- `update <id> <title> [description]` - Update task
- `complete <id>` - Mark task as complete
- `delete <id>` - Delete a task
- `quit` - Exit the application
- `help` - Show available commands