# Todo In-Memory Python Console App

A command-line todo application that stores tasks in memory. Provides functionality to add, view, update, delete, and mark tasks as complete/incomplete.

## Prerequisites

- Python 3.13+
- UV package manager (optional but recommended)

## Setup

1. Clone the repository
2. Navigate to the project directory
3. (Optional) Create a virtual environment:
   ```bash
   uv venv  # if using UV
   # or
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

## Usage

The application is run as a command-line tool with various subcommands:

### Add a Task
```bash
python src/main.py add "Task Title" "Task Description"
```
- Title is required (max 200 characters)
- Description is optional (max 1000 characters)
- Returns a unique ID for the created task

### List All Tasks
```bash
python src/main.py list
```
- Displays all tasks with ID, title, description, and status
- Status shown as [X] for complete, [ ] for incomplete

### Update a Task
```bash
python src/main.py update 1 --title "New Title" --description "New Description"
```
- Updates the title and description of task with specified ID
- Both title and description are optional (can update one or both)

### Mark Task Complete
```bash
python src/main.py complete 1
```
- Marks the task with specified ID as complete
- Status will show as [X]

### Mark Task Incomplete
```bash
python src/main.py incomplete 1
```
- Marks the task with specified ID as incomplete
- Status will show as [ ]

### Delete a Task
```bash
python src/main.py delete 1
```
- Removes the task with specified ID from the list

### Get Help
```bash
python src/main.py --help
python src/main.py add --help
python src/main.py list --help
# etc.
```

## Example Workflow

1. Add a task:
   ```bash
   python src/main.py add "Buy groceries" "Milk, eggs, bread"
   ```

2. List tasks:
   ```bash
   python src/main.py list
   ```

3. Mark task as complete:
   ```bash
   python src/main.py complete 1
   ```

4. Update a task:
   ```bash
   python src/main.py update 1 --title "Buy weekly groceries" --description "Milk, eggs, bread, fruits, vegetables"
   ```

## Features

- In-memory storage (no persistence to files or databases)
- Add tasks with title and optional description
- View all tasks with status indicators
- Update task details by ID
- Delete tasks by ID
- Mark tasks as complete/incomplete
- Input validation (title: max 200 chars, description: max 1000 chars)
- Error handling with specific messages

## Project Structure

```
src/
└── main.py              # Single file implementation with Task class, TaskManager class, CLI functions

tests/
├── unit/
│   └── test_todo.py     # Unit tests for Task, TaskManager, and CLI functions
└── integration/
    └── test_cli.py      # Integration tests for CLI commands
```