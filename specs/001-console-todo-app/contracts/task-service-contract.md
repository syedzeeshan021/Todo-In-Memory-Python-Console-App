# API Contracts: Phase I - In-Memory Python Console Todo Application

## Task Service Interface

### Methods

#### add_task(title: str, description: str = "") -> Task
- **Purpose**: Creates a new task with the given title and optional description
- **Parameters**:
  - title (str): Task title (1-200 characters)
  - description (str, optional): Task description (max 1000 characters)
- **Returns**: Task object with assigned ID and timestamps
- **Raises**: ValueError if title validation fails
- **Side effects**: Increments global ID counter, adds task to in-memory storage

#### get_task(task_id: int) -> Task
- **Purpose**: Retrieves a task by its ID
- **Parameters**:
  - task_id (int): Unique identifier of the task
- **Returns**: Task object if found
- **Raises**: KeyError if task_id does not exist

#### list_tasks() -> List[Task]
- **Purpose**: Returns all tasks in the system
- **Parameters**: None
- **Returns**: List of all Task objects in creation order
- **Raises**: None

#### update_task(task_id: int, title: str = None, description: str = None) -> Task
- **Purpose**: Updates an existing task's title and/or description
- **Parameters**:
  - task_id (int): Unique identifier of the task to update
  - title (str, optional): New title (if provided)
  - description (str, optional): New description (if provided)
- **Returns**: Updated Task object
- **Raises**: KeyError if task_id does not exist, ValueError if validation fails
- **Side effects**: Updates updated_at timestamp

#### delete_task(task_id: int) -> bool
- **Purpose**: Removes a task from the system
- **Parameters**:
  - task_id (int): Unique identifier of the task to delete
- **Returns**: True if task was deleted, False if task did not exist
- **Raises**: None
- **Side effects**: Preserves ID to prevent reuse, removes from storage

#### toggle_task_completion(task_id: int) -> Task
- **Purpose**: Toggles the completion status of a task
- **Parameters**:
  - task_id (int): Unique identifier of the task to toggle
- **Returns**: Updated Task object with toggled completion status
- **Raises**: KeyError if task_id does not exist
- **Side effects**: Updates completed status and completed_at timestamp

## Task Model Contract

### Properties
- id (int): Sequential identifier, immutable after creation
- title (str): Task title, 1-200 characters
- description (str): Task description, max 1000 characters
- completed (bool): Completion status
- created_at (datetime): Creation timestamp
- updated_at (datetime): Last update timestamp
- completed_at (Optional[datetime]): Completion timestamp (None if incomplete)

### Validation
- title must be 1-200 characters when stripped of whitespace
- description must be ≤1000 characters if provided
- id must be positive integer
- timestamps must be valid datetime objects

