"""
Task service for managing todo tasks in memory.

This module implements the business logic for task management operations
including adding, retrieving, updating, deleting, and toggling completion status.
"""

from typing import List, Optional

from src.models.task import Task


class TaskService:
    """
    Service class for managing tasks with in-memory storage.

    This class handles all business logic for task operations including:
    - Adding new tasks with sequential ID assignment
    - Retrieving tasks by ID or all tasks
    - Updating task details
    - Deleting tasks
    - Toggling task completion status
    """

    def __init__(self) -> None:
        """Initialize the task service with empty storage and ID counter."""
        self._tasks: dict[int, Task] = {}
        self.next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task to the service.

        Args:
            title: The task title (1-200 characters)
            description: Optional task description (max 1000 characters)

        Returns:
            The newly created Task object with assigned ID and timestamps

        Raises:
            ValueError: If title or description validation fails
        """
        # Validate title
        title_stripped = title.strip()
        if not title_stripped:
            raise ValueError("Task title cannot be empty")

        if len(title_stripped) > 200:
            raise ValueError("Task title must be between 1 and 200 characters")

        # Validate description
        if len(description) > 1000:
            raise ValueError("Task description cannot exceed 1000 characters")

        # Create task with the next available ID
        task = Task(
            id=self.next_id,
            title=title_stripped,
            description=description
        )

        # Store the task
        self._tasks[self.next_id] = task

        # Increment the ID counter for the next task
        self.next_id += 1

        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a specific task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks sorted by ID in ascending order.

        Returns:
            A list of all Task objects sorted by ID
        """
        # Return tasks sorted by ID
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """
        Update an existing task's title and/or description.

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            The updated Task object if successful, None if task doesn't exist

        Raises:
            ValueError: If title or description validation fails
        """
        task = self.get_task(task_id)
        if task is None:
            return None

        # Use current values if new values are not provided
        new_title = title if title is not None else task.title
        new_description = description if description is not None else task.description

        # Validate title if provided
        if title is not None:
            title_stripped = title.strip()
            if not title_stripped:
                raise ValueError("Task title cannot be empty")

            if len(title_stripped) > 200:
                raise ValueError("Task title must be between 1 and 200 characters")

            new_title = title_stripped

        # Validate description if provided
        if description is not None:
            if len(description) > 1000:
                raise ValueError("Task description cannot exceed 1000 characters")

            new_description = description

        # Update the task properties
        task.title = new_title
        task.description = new_description
        task.update_timestamps()

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was successfully deleted, False if it didn't exist
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def toggle_complete(self, task_id: int) -> Optional[Task]:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            The updated Task object if successful, None if task doesn't exist
        """
        task = self.get_task(task_id)
        if task is None:
            return None

        task.toggle_completion()
        return task