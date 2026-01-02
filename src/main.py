#!/usr/bin/env python3
"""
Todo In-Memory Python Console App

A command-line todo application that stores tasks in memory.
Provides functionality to add, view, update, delete, and mark tasks as complete/incomplete.
"""

import argparse
import sys
from typing import List, Optional


class Task:
    """
    Represents a single todo item with attributes.

    Attributes:
        id (int): Auto-generated unique integer identifier
        title (str): Required string with maximum 200 characters
        description (str): Optional string with maximum 1000 characters
        status (bool): Boolean indicating completion status (True = complete, False = incomplete)
    """

    def __init__(self, task_id: int, title: str, description: str = "", status: bool = False):
        """
        Initialize a Task instance.

        Args:
            task_id (int): Unique identifier for the task
            title (str): Title of the task (max 200 characters)
            description (str): Optional description of the task (max 1000 characters)
            status (bool): Completion status (default: False)
        """
        self.id = task_id
        self.title = title
        self.description = description
        self.status = status  # False = incomplete, True = complete

    def __str__(self) -> str:
        """Return a string representation of the task for display."""
        status_indicator = "[X]" if self.status else "[ ]"
        return f"[{self.id}] {status_indicator} {self.title} - {self.description}"

    def to_dict(self) -> dict:
        """Convert the task to a dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status
        }


class TaskManager:
    """
    Manages the collection of Task objects and provides operations.

    Attributes:
        tasks (List[Task]): In-memory collection of Task objects
        next_id (int): Counter for generating unique IDs
    """

    def __init__(self):
        """Initialize the TaskManager with an empty task list and ID counter."""
        self.tasks: List[Task] = []
        self.next_id = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Create and add a new Task to the collection.

        Args:
            title (str): Title of the task (max 200 characters)
            description (str): Optional description of the task (max 1000 characters)

        Returns:
            Task: The newly created Task object

        Raises:
            ValueError: If title is empty or exceeds length limits
        """
        # Validate input
        validate_title(title)
        validate_description(description)

        # Create the task
        task = Task(self.next_id, title, description, False)
        self.tasks.append(task)

        # Increment the ID counter for the next task
        self.next_id += 1

        return task

    def list_tasks(self) -> List[Task]:
        """
        Return all tasks in the collection.

        Returns:
            List[Task]: List of all tasks
        """
        return self.tasks

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Optional[Task]: The task if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update an existing task's title and/or description.

        Args:
            task_id (int): The ID of the task to update
            title (Optional[str]): New title (if provided)
            description (Optional[str]): New description (if provided)

        Returns:
            bool: True if update was successful, False if task not found

        Raises:
            ValueError: If title is provided but is empty or exceeds length limits
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        # If title is provided, validate it
        if title is not None:
            validate_title(title)
            task.title = title

        # If description is provided, validate it
        if description is not None:
            validate_description(description)
            task.description = description

        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Remove a task by its ID.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if deletion was successful, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        self.tasks.remove(task)
        return True

    def complete_task(self, task_id: int) -> bool:
        """
        Mark a task as complete.

        Args:
            task_id (int): The ID of the task to mark as complete

        Returns:
            bool: True if operation was successful, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        task.status = True
        return True

    def incomplete_task(self, task_id: int) -> bool:
        """
        Mark a task as incomplete.

        Args:
            task_id (int): The ID of the task to mark as incomplete

        Returns:
            bool: True if operation was successful, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        task.status = False
        return True


def validate_title(title: str) -> None:
    """
    Validate the title according to the specification.

    Args:
        title (str): The title to validate

    Raises:
        ValueError: If title is empty or exceeds length limits
    """
    if not title or title.strip() == "":
        raise ValueError("Title cannot be empty")

    if len(title) > 200:
        raise ValueError(f"Title too long (max 200 characters, got {len(title)})")


def validate_description(description: str) -> None:
    """
    Validate the description according to the specification.

    Args:
        description (str): The description to validate

    Raises:
        ValueError: If description exceeds length limits
    """
    if len(description) > 1000:
        raise ValueError(f"Description too long (max 1000 characters, got {len(description)})")


def handle_add_command(task_manager: TaskManager, args) -> None:
    """
    Handle the 'add' command to create a new task.

    Args:
        task_manager (TaskManager): The task manager instance
        args: The parsed command-line arguments
    """
    try:
        task = task_manager.add_task(args.title, args.description or "")
        print(f"Task added with ID: {task.id}")
    except ValueError as e:
        print(f"Error: {e}")


def handle_list_command(task_manager: TaskManager, args) -> None:
    """
    Handle the 'list' command to display all tasks.

    Args:
        task_manager (TaskManager): The task manager instance
        args: The parsed command-line arguments
    """
    tasks = task_manager.list_tasks()

    if not tasks:
        print("No tasks available")
        return

    for task in tasks:
        status_indicator = "[X]" if task.status else "[ ]"
        if task.description:
            print(f"[{task.id}] {status_indicator} {task.title} - {task.description}")
        else:
            print(f"[{task.id}] {status_indicator} {task.title}")


def handle_update_command(task_manager: TaskManager, args) -> None:
    """
    Handle the 'update' command to modify a task.

    Args:
        task_manager (TaskManager): The task manager instance
        args: The parsed command-line arguments
    """
    # Determine which fields to update
    title = args.title if hasattr(args, 'title') and args.title is not None else None
    description = args.description if hasattr(args, 'description') and args.description is not None else None

    # At least one field must be provided for update
    if title is None and description is None:
        print("Error: Please provide at least a title or description to update")
        return

    try:
        success = task_manager.update_task(args.id, title, description)
        if success:
            print(f"Task {args.id} updated successfully")
        else:
            print(f"Error: Task with ID {args.id} not found")
    except ValueError as e:
        print(f"Error: {e}")


def handle_delete_command(task_manager: TaskManager, args) -> None:
    """
    Handle the 'delete' command to remove a task.

    Args:
        task_manager (TaskManager): The task manager instance
        args: The parsed command-line arguments
    """
    success = task_manager.delete_task(args.id)
    if success:
        print(f"Task {args.id} deleted successfully")
    else:
        print(f"Error: Task with ID {args.id} not found")


def handle_complete_command(task_manager: TaskManager, args) -> None:
    """
    Handle the 'complete' command to mark a task as complete.

    Args:
        task_manager (TaskManager): The task manager instance
        args: The parsed command-line arguments
    """
    success = task_manager.complete_task(args.id)
    if success:
        print(f"Task {args.id} marked as complete")
    else:
        print(f"Error: Task with ID {args.id} not found")


def handle_incomplete_command(task_manager: TaskManager, args) -> None:
    """
    Handle the 'incomplete' command to mark a task as incomplete.

    Args:
        task_manager (TaskManager): The task manager instance
        args: The parsed command-line arguments
    """
    success = task_manager.incomplete_task(args.id)
    if success:
        print(f"Task {args.id} marked as incomplete")
    else:
        print(f"Error: Task with ID {args.id} not found")


def main():
    """
    Main function to run the Todo application.
    Sets up the argument parser and handles commands.
    """
    # Create the task manager instance
    task_manager = TaskManager()

    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description="Todo In-Memory Python Console App",
        prog="todo"
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('title', help='Title of the task (max 200 characters)')
    add_parser.add_argument('description', nargs='?', default='', help='Description of the task (max 1000 characters)')
    add_parser.set_defaults(func=handle_add_command)

    # List command
    list_parser = subparsers.add_parser('list', help='List all tasks')
    list_parser.set_defaults(func=handle_list_command)

    # Update command
    update_parser = subparsers.add_parser('update', help='Update a task')
    update_parser.add_argument('id', type=int, help='ID of the task to update')
    update_parser.add_argument('--title', help='New title for the task (max 200 characters)')
    update_parser.add_argument('--description', help='New description for the task (max 1000 characters)')
    update_parser.set_defaults(func=handle_update_command)

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('id', type=int, help='ID of the task to delete')
    delete_parser.set_defaults(func=handle_delete_command)

    # Complete command
    complete_parser = subparsers.add_parser('complete', help='Mark a task as complete')
    complete_parser.add_argument('id', type=int, help='ID of the task to mark as complete')
    complete_parser.set_defaults(func=handle_complete_command)

    # Incomplete command
    incomplete_parser = subparsers.add_parser('incomplete', help='Mark a task as incomplete')
    incomplete_parser.add_argument('id', type=int, help='ID of the task to mark as incomplete')
    incomplete_parser.set_defaults(func=handle_incomplete_command)

    # Parse the arguments
    args = parser.parse_args()

    # If no command is provided, show help
    if args.command is None:
        parser.print_help()
        return

    # Execute the appropriate function based on the command
    args.func(task_manager, args)


if __name__ == "__main__":
    main()