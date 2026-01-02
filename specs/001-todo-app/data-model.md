# Data Model: Todo In-Memory Python Console App

**Feature**: Todo In-Memory Python Console App
**Date**: 2026-01-03
**Status**: Complete

## Entities

### Task
Represents a single todo item with the following attributes:

- **id** (int): Auto-generated unique integer identifier
- **title** (str): Required string with maximum 200 characters
- **description** (str): Optional string with maximum 1000 characters
- **status** (bool): Boolean indicating completion status (True = complete, False = incomplete)

### TaskManager
Manages the collection of Task objects and provides operations:

- **tasks** (list): In-memory collection of Task objects
- **next_id** (int): Counter for generating unique IDs
- **add_task(title, description)**: Creates and adds a new Task
- **list_tasks()**: Returns all tasks for display
- **update_task(task_id, title, description)**: Updates an existing task
- **delete_task(task_id)**: Removes a task by ID
- **complete_task(task_id)**: Marks a task as complete
- **incomplete_task(task_id)**: Marks a task as incomplete

## Validation Rules

### Task Validation
- Title must not be empty
- Title must not exceed 200 characters
- Description may be empty but must not exceed 1000 characters
- ID must be unique within the TaskManager collection
- Status must be a boolean value

### Operation Validation
- All operations requiring a task ID must validate that the ID exists
- Update operations must validate that the ID exists before modification
- Delete operations must validate that the ID exists before removal
- Complete/incomplete operations must validate that the ID exists before status change

## State Transitions

### Task Status Transitions
- Initial state: status = False (incomplete)
- `complete_task()` → status = True (complete)
- `incomplete_task()` → status = False (incomplete)
- No other state transitions for the status attribute