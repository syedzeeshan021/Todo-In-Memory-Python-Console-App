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

The application is run as a command-line tool with various subcommands. It supports both single command execution and interactive mode:

### Interactive Mode (Recommended)
```bash
python src/main.py
```
- Starts an interactive session where you can enter multiple commands
- Provides a `todo>` prompt for continuous command entry
- Type `help` to see all available commands

### Add a Task
```bash
python src/main.py add "Task Title" "Task Description"
# Or in interactive mode: add "Task Title" "Task Description"
```
- Title is required (max 200 characters)
- Description is optional (max 1000 characters)
- Returns a unique ID for the created task

### List All Tasks
```bash
python src/main.py list
# Or in interactive mode: list or ls
```
- Displays all tasks with ID, title, description, and status
- Status shown as [X] for complete, [ ] for incomplete
- Shows statistics (total, completed, incomplete) after listing

### Update a Task
```bash
python src/main.py update 1 --title "New Title" --description "New Description"
# Or in interactive mode: update 1 --title "New Title" --description "New Description"
```
- Updates the title and description of task with specified ID
- Both title and description are optional (can update one or both)

### Mark Task Complete
```bash
python src/main.py complete 1
# Or in interactive mode: complete 1 or done 1
```
- Marks the task with specified ID as complete
- Status will show as [X]

### Mark Task Incomplete
```bash
python src/main.py incomplete 1
# Or in interactive mode: incomplete 1 or undone 1
```
- Marks the task with specified ID as incomplete
- Status will show as [ ]

### Delete a Task
```bash
python src/main.py delete 1
# Or in interactive mode: delete 1 or del 1
```
- Removes the task with specified ID from the list

### Enhanced Interactive Commands

#### Show Task Details
```bash
# In interactive mode only:
show 1
```
- Displays detailed information about a specific task (ID, title, description, status)

#### View Statistics
```bash
# In interactive mode only:
stats
```
- Shows total tasks, completed tasks, incomplete tasks, and completion rate

#### Search Tasks
```bash
# In interactive mode only:
search keyword
```
- Finds and displays tasks containing the keyword in title or description

#### Clear All Tasks
```bash
# In interactive mode only:
clear
```
- Removes all tasks from the list and resets the task counter

#### Command Aliases
- `ls` → `list`
- `del` → `delete`
- `done` → `complete`
- `undone` → `incomplete`

### Get Help
```bash
python src/main.py --help
python src/main.py add --help
python src/main.py list --help
# etc.

# In interactive mode:
help
```

## Example Workflow

1. Start interactive mode:
   ```bash
   python src/main.py
   ```

2. Add a task:
   ```
   todo> add "Buy groceries" "Milk, eggs, bread"
   ```

3. List tasks:
   ```
   todo> list
   ```

4. Mark task as complete:
   ```
   todo> complete 1
   # or
   todo> done 1
   ```

5. Update a task:
   ```
   todo> update 1 --title "Buy weekly groceries" --description "Milk, eggs, bread, fruits, vegetables"
   ```

6. Search for tasks:
   ```
   todo> search groceries
   ```

7. View statistics:
   ```
   todo> stats
   ```

8. Exit the application:
   ```
   todo> quit
   # or
   todo> exit
   # or
   todo> q
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