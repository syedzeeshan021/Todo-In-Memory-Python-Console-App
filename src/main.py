#!/usr/bin/env python3
"""
Todo In-Memory Python Console App

A command-line todo application that stores tasks in memory.
Provides functionality to add, view, update, delete, and mark tasks as complete/incomplete.
"""

import argparse
import sys
from typing import Dict, List, Optional, Callable
from enum import Enum


# ==================== CUSTOM EXCEPTIONS ====================


class TodoAppError(Exception):
    """Base exception for Todo application errors."""
    pass


class TaskNotFoundError(TodoAppError):
    """Raised when a task with given ID is not found."""
    pass


class ValidationError(ValueError, TodoAppError):
    """Raised when input validation fails."""
    pass


# ==================== ENUMERATIONS ====================


class TaskStatus(Enum):
    """Task completion status."""
    INCOMPLETE = False
    COMPLETE = True


# ==================== MODELS ====================


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

    def __repr__(self) -> str:
        """Return a developer-friendly representation of the task."""
        return f"Task(id={self.id}, title='{self.title}', status={'complete' if self.status else 'incomplete'})"

    def to_dict(self) -> dict:
        """Convert the task to a dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status
        }

    def set_status(self, status: bool) -> None:
        """Update task status."""
        self.status = status

    def update(self, title: Optional[str] = None, description: Optional[str] = None) -> None:
        """Update task fields."""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description


# ==================== VALIDATORS ====================


def validate_title(title: str) -> None:
    """
    Validate the title according to the specification.

    Args:
        title (str): The title to validate

    Raises:
        ValidationError: If title is empty or exceeds length limits
    """
    if not title or title.strip() == "":
        raise ValidationError("Title cannot be empty")

    if len(title) > 200:
        raise ValidationError(f"Title too long (max 200 characters, got {len(title)})")


def validate_description(description: str) -> None:
    """
    Validate the description according to the specification.

    Args:
        description (str): The description to validate

    Raises:
        ValidationError: If description exceeds length limits
    """
    if len(description) > 1000:
        raise ValidationError(f"Description too long (max 1000 characters, got {len(description)})")


# ==================== TASK MANAGER ====================


class TaskManager:
    """
    Manages the collection of Task objects and provides CRUD operations.

    Uses dictionary for O(1) task lookups and list for maintaining insertion order.

    Attributes:
        _tasks (Dict[int, Task]): Internal dictionary mapping task IDs to Task objects
        _tasks_list (List[Task]): List for maintaining task insertion order
        _next_id (int): Counter for generating unique IDs
    """

    def __init__(self):
        """Initialize the TaskManager with empty collections and ID counter."""
        self._tasks: Dict[int, Task] = {}
        self._tasks_list: List[Task] = []
        self._next_id = 1

    @property
    def tasks(self) -> List[Task]:
        """Return tasks list for backward compatibility."""
        return self._tasks_list

    @property
    def next_id(self) -> int:
        """Return the next task ID (for backward compatibility)."""
        return self._next_id

    def _add_to_storage(self, task: Task) -> None:
        """
        Add task to both storage structures.

        Args:
            task (Task): The task to add
        """
        self._tasks[task.id] = task
        self._tasks_list.append(task)

    def _remove_from_storage(self, task: Task) -> None:
        """
        Remove task from both storage structures.

        Args:
            task (Task): The task to remove
        """
        del self._tasks[task.id]
        self._tasks_list.remove(task)

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Create and add a new Task to the collection.

        Args:
            title (str): Title of the task (max 200 characters)
            description (str): Optional description of the task (max 1000 characters)

        Returns:
            Task: The newly created Task object

        Raises:
            ValidationError: If title is empty or exceeds length limits
        """
        # Validate input
        validate_title(title)
        validate_description(description)

        # Create and store the task
        task = Task(self._next_id, title, description, False)
        self._add_to_storage(task)
        self._next_id += 1

        return task

    def list_tasks(self) -> List[Task]:
        """
        Return all tasks in the collection.

        Returns:
            List[Task]: List of all tasks in insertion order
        """
        return self._tasks_list

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID with O(1) complexity.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Optional[Task]: The task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def _get_or_raise(self, task_id: int) -> Task:
        """
        Get a task by ID or raise an exception if not found.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Task: The task if found

        Raises:
            TaskNotFoundError: If task is not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        return task

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update an existing task's title and/or description with O(1) complexity.

        Args:
            task_id (int): The ID of the task to update
            title (Optional[str]): New title (if provided)
            description (Optional[str]): New description (if provided)

        Returns:
            bool: True if update was successful, False if task not found

        Raises:
            ValidationError: If provided title or description is invalid
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        # Validate and update fields
        if title is not None:
            validate_title(title)
        if description is not None:
            validate_description(description)

        task.update(title, description)
        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Remove a task by its ID with O(1) dictionary lookup.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if deletion was successful, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        self._remove_from_storage(task)
        return True

    def set_task_status(self, task_id: int, status: bool) -> bool:
        """
        Set task completion status with O(1) complexity.

        Consolidates complete_task and incomplete_task logic to avoid duplication.

        Args:
            task_id (int): The ID of the task to update
            status (bool): The new status (True = complete, False = incomplete)

        Returns:
            bool: True if operation was successful, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        task.set_status(status)
        return True

    def complete_task(self, task_id: int) -> bool:
        """
        Mark a task as complete.

        Args:
            task_id (int): The ID of the task to mark as complete

        Returns:
            bool: True if operation was successful, False if task not found
        """
        return self.set_task_status(task_id, True)

    def incomplete_task(self, task_id: int) -> bool:
        """
        Mark a task as incomplete.

        Args:
            task_id (int): The ID of the task to mark as incomplete

        Returns:
            bool: True if operation was successful, False if task not found
        """
        return self.set_task_status(task_id, False)

    def get_statistics(self) -> Dict[str, int | float]:
        """
        Calculate task statistics.

        Returns:
            Dict: Statistics including total, completed, incomplete, and completion rate
        """
        total = len(self._tasks_list)
        if total == 0:
            return {
                "total": 0,
                "completed": 0,
                "incomplete": 0,
                "completion_rate": 0.0
            }

        completed = sum(1 for task in self._tasks_list if task.status)
        incomplete = total - completed
        completion_rate = (completed / total * 100) if total > 0 else 0.0

        return {
            "total": total,
            "completed": completed,
            "incomplete": incomplete,
            "completion_rate": completion_rate
        }

    def search_tasks(self, keyword: str) -> List[Task]:
        """
        Search tasks by keyword in title or description.

        Args:
            keyword (str): The keyword to search for

        Returns:
            List[Task]: List of matching tasks
        """
        keyword_lower = keyword.lower()
        return [
            task for task in self._tasks_list
            if keyword_lower in task.title.lower() or keyword_lower in task.description.lower()
        ]

    def clear_all(self) -> int:
        """
        Clear all tasks and reset the ID counter.

        Returns:
            int: Number of tasks cleared
        """
        count = len(self._tasks_list)
        self._tasks.clear()
        self._tasks_list.clear()
        self._next_id = 1
        return count


# ==================== COMMAND HANDLERS ====================


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
    except ValidationError as e:
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
    except ValidationError as e:
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


# ==================== COMMAND-LINE PARSER ====================


def validate_title(title: str) -> None:
    """
    Validate the title according to the specification.

    Args:
        title (str): The title to validate

    Raises:
        ValidationError: If title is empty or exceeds length limits
    """
    if not title or title.strip() == "":
        raise ValidationError("Title cannot be empty")

    if len(title) > 200:
        raise ValidationError(f"Title too long (max 200 characters, got {len(title)})")


def validate_description(description: str) -> None:
    """
    Validate the description according to the specification.

    Args:
        description (str): The description to validate

    Raises:
        ValidationError: If description exceeds length limits
    """
    if len(description) > 1000:
        raise ValidationError(f"Description too long (max 1000 characters, got {len(description)})")


def parse_command_line_args():
    """
    Set up and parse command line arguments.

    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
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

    return parser


# ==================== UI COMPONENTS ====================


# ==================== UI COMPONENTS ====================


class UIFormatter:
    """Handles all UI display and formatting for the todo application."""

    @staticmethod
    def display_menu() -> None:
        """Display the main CRUD menu."""
        print("\n" + "=" * 70)
        print("╔" + "═" * 68 + "╗")
        print("║" + " " * 15 + "📝 TODO APPLICATION - CRUD MENU 📝" + " " * 16 + "║")
        print("╚" + "═" * 68 + "╝")
        print("\n📌 AVAILABLE OPERATIONS:")
        print("┌" + "─" * 68 + "┐")
        print("│ 🟢 CREATE    | add <title> [description]                         │")
        print("│ 🔵 READ      | list, ls, show <id>                              │")
        print("│ 🟡 UPDATE    | update <id> --title <text> --description <text>  │")
        print("│ 🔴 DELETE    | delete <id>, del <id>                            │")
        print("│ ✅ COMPLETE  | complete <id>, done <id>                         │")
        print("│ ❌ INCOMPLETE| incomplete <id>, undone <id>                      │")
        print("└" + "─" * 68 + "┘")
        print("\n🛠️  UTILITY COMMANDS:")
        print("┌" + "─" * 68 + "┐")
        print("│ 📊 stats                    - View task statistics              │")
        print("│ 🔍 search <keyword>         - Search tasks                      │")
        print("│ 🗑️  clear                    - Clear all tasks                   │")
        print("│ ❓ help, ?                   - Show detailed help               │")
        print("│ 🚪 quit, exit, q            - Exit application                  │")
        print("└" + "─" * 68 + "┘")
        print("=" * 70 + "\n")

    @staticmethod
    def display_help() -> None:
        """Display detailed help information."""
        print("\n" + "=" * 70)
        print("📖 DETAILED COMMAND GUIDE")
        print("=" * 70)
        print("\n✨ CREATE OPERATIONS:")
        print("  • add <title> [description]")
        print("    Example: add \"Buy groceries\" \"milk, eggs, bread\"\n")
        print("📖 READ OPERATIONS:")
        print("  • list or ls")
        print("    Display all tasks with their status")
        print("  • show <id>")
        print("    Display detailed information about a specific task\n")
        print("✏️  UPDATE OPERATIONS:")
        print("  • update <id> --title <text> --description <text>")
        print("    Example: update 1 --title \"New Title\" --description \"New Description\"\n")
        print("🗑️  DELETE OPERATIONS:")
        print("  • delete <id> or del <id>")
        print("    Permanently remove a task\n")
        print("✅ MARK COMPLETE:")
        print("  • complete <id> or done <id>")
        print("    Mark a task as completed [X]\n")
        print("❌ MARK INCOMPLETE:")
        print("  • incomplete <id> or undone <id>")
        print("    Mark a task as incomplete [ ]\n")
        print("🛠️  UTILITY COMMANDS:")
        print("  • stats - Show statistics (total, completed, incomplete, rate)")
        print("  • search <keyword> - Find tasks by title or description")
        print("  • clear - Remove all tasks and reset counter\n")
        print("=" * 70 + "\n")

    @staticmethod
    def display_tasks(tasks: List[Task]) -> None:
        """
        Display all tasks with statistics.

        Args:
            tasks (List[Task]): Tasks to display
        """
        if not tasks:
            print("\n📭 No tasks available. Start by adding one!")
            return

        print("\n" + "─" * 70)
        print("📋 YOUR TASKS:")
        print("─" * 70)
        for task in tasks:
            status_indicator = "✅" if task.status else "⭕"
            status_text = "Done" if task.status else "Pending"
            desc_text = f" | {task.description}" if task.description else ""
            print(f"  {status_indicator} [{task.id}] {task.title}{desc_text} ({status_text})")

        # Calculate and display statistics
        total = len(tasks)
        completed = sum(1 for t in tasks if t.status)
        incomplete = total - completed
        completion_rate = (completed / total * 100) if total > 0 else 0
        print("─" * 70)
        print(f"  📊 Total: {total} | ✅ Completed: {completed} | ⭕ Pending: {incomplete} | Rate: {completion_rate:.0f}%")
        print("─" * 70 + "\n")

    @staticmethod
    def display_task_detail(task: Task) -> None:
        """
        Display detailed information about a task.

        Args:
            task (Task): The task to display
        """
        status_text = "✅ Complete" if task.status else "⭕ Incomplete"
        print("\n" + "─" * 70)
        print(f"📝 TASK DETAILS (ID: {task.id})")
        print("─" * 70)
        print(f"  Title:       {task.title}")
        print(f"  Description: {task.description if task.description else '(No description)'}")
        print(f"  Status:      {status_text}")
        print("─" * 70 + "\n")

    @staticmethod
    def display_statistics(stats: Dict) -> None:
        """
        Display task statistics.

        Args:
            stats (Dict): Statistics dictionary
        """
        print("\n" + "─" * 70)
        print("📊 TASK STATISTICS")
        print("─" * 70)
        print(f"  Total Tasks:    {stats['total']}")
        print(f"  ✅ Completed:   {stats['completed']}")
        print(f"  ⭕ Incomplete:  {stats['incomplete']}")
        print(f"  📈 Completion Rate: {stats['completion_rate']:.1f}%")
        print("─" * 70 + "\n")

    @staticmethod
    def display_search_results(keyword: str, matches: List[Task]) -> None:
        """
        Display search results.

        Args:
            keyword (str): The search keyword
            matches (List[Task]): Matching tasks
        """
        if matches:
            print(f"\n🔍 Found {len(matches)} matching task(s):")
            print("─" * 70)
            for task in matches:
                status_indicator = "✅" if task.status else "⭕"
                desc_text = f" | {task.description}" if task.description else ""
                print(f"  {status_indicator} [{task.id}] {task.title}{desc_text}")
            print("─" * 70 + "\n")
        else:
            print("\n🔍 No matching tasks found\n")


# ==================== INTERACTIVE MODE ====================


class InteractiveCommandHandler:
    """Handles all interactive mode commands with O(1) lookups."""

    def __init__(self, task_manager: TaskManager):
        """Initialize the handler with a task manager instance."""
        self.task_manager = task_manager
        self.ui = UIFormatter()

    def handle_add(self, args: str) -> None:
        """Handle add command."""
        if not args.strip():
            print("Error: Title is required. Usage: add <title> [description]")
            return

        parts = self._parse_quoted_input(args)
        if not parts:
            print("Error: Title is required. Usage: add <title> [description]")
            return

        title = parts[0]
        description = parts[1] if len(parts) > 1 else ""

        try:
            task = self.task_manager.add_task(title, description)
            print(f"\n✨ Task added successfully!")
            print(f"   ID: {task.id} | Title: {task.title}")
            if description:
                print(f"   Description: {task.description}")
            print()
        except ValidationError as e:
            print(f"❌ Error: {e}\n")

    def handle_update(self, args: str) -> None:
        """Handle update command."""
        parts = args.split()
        if not parts:
            print("Usage: update <id> [--title <text>] [--description <text>]")
            return

        try:
            task_id = int(parts[0])
        except ValueError:
            print("Error: Task ID must be a number")
            return

        title = None
        description = None

        # Parse optional flags
        i = 1
        while i < len(parts):
            if parts[i] == '--title' and i + 1 < len(parts):
                title = parts[i + 1].strip('"')
                i += 2
            elif parts[i] == '--description' and i + 1 < len(parts):
                description = parts[i + 1].strip('"')
                i += 2
            else:
                i += 1

        try:
            success = self.task_manager.update_task(task_id, title, description)
            if success:
                task = self.task_manager.get_task_by_id(task_id)
                print(f"\n✏️  Task {task_id} updated successfully!")
                print(f"   Title: {task.title}")
                print(f"   Description: {task.description}\n")
            else:
                print(f"❌ Error: Task with ID {task_id} not found\n")
        except ValidationError as e:
            print(f"❌ Error: {e}\n")

    def handle_delete(self, args: str) -> None:
        """Handle delete command."""
        if not args.strip():
            print("Usage: delete <id> or del <id>")
            return

        try:
            task_id = int(args.strip())
        except ValueError:
            print("Error: Task ID must be a number")
            return

        task = self.task_manager.get_task_by_id(task_id)
        if task:
            success = self.task_manager.delete_task(task_id)
            if success:
                print(f"\n🗑️  Task {task_id} deleted successfully!")
                print(f"   Removed: {task.title}\n")
            else:
                print(f"❌ Error: Could not delete task {task_id}\n")
        else:
            print(f"❌ Error: Task with ID {task_id} not found\n")

    def handle_complete(self, args: str) -> None:
        """Handle complete command."""
        if not args.strip():
            print("Usage: complete <id> or done <id>")
            return

        try:
            task_id = int(args.strip())
        except ValueError:
            print("Error: Task ID must be a number")
            return

        task = self.task_manager.get_task_by_id(task_id)
        if task:
            success = self.task_manager.complete_task(task_id)
            if success:
                print(f"\n✅ Task {task_id} marked as complete!")
                print(f"   {task.title}\n")
            else:
                print(f"❌ Error: Could not mark task {task_id} as complete\n")
        else:
            print(f"❌ Error: Task with ID {task_id} not found\n")

    def handle_incomplete(self, args: str) -> None:
        """Handle incomplete command."""
        if not args.strip():
            print("Usage: incomplete <id> or undone <id>")
            return

        try:
            task_id = int(args.strip())
        except ValueError:
            print("Error: Task ID must be a number")
            return

        task = self.task_manager.get_task_by_id(task_id)
        if task:
            success = self.task_manager.incomplete_task(task_id)
            if success:
                print(f"\n⭕ Task {task_id} marked as incomplete!")
                print(f"   {task.title}\n")
            else:
                print(f"❌ Error: Could not mark task {task_id} as incomplete\n")
        else:
            print(f"❌ Error: Task with ID {task_id} not found\n")

    def handle_show(self, args: str) -> None:
        """Handle show command."""
        if not args.strip():
            print("Usage: show <id>")
            return

        try:
            task_id = int(args.strip())
        except ValueError:
            print("Error: Task ID must be a number")
            return

        task = self.task_manager.get_task_by_id(task_id)
        if task:
            self.ui.display_task_detail(task)
        else:
            print(f"❌ Error: Task with ID {task_id} not found\n")

    def handle_search(self, args: str) -> None:
        """Handle search command."""
        if not args.strip():
            print("Usage: search <keyword>")
            return

        keyword = args.strip()
        matches = self.task_manager.search_tasks(keyword)
        self.ui.display_search_results(keyword, matches)

    def handle_clear(self) -> None:
        """Handle clear command."""
        if not self.task_manager.tasks:
            print("\n📭 No tasks to clear\n")
        else:
            count = self.task_manager.clear_all()
            print(f"\n🗑️  Successfully cleared {count} task(s)!")
            print("   Task counter has been reset.\n")

    def handle_stats(self) -> None:
        """Handle stats command."""
        if not self.task_manager.tasks:
            print("\n📭 No tasks available\n")
        else:
            stats = self.task_manager.get_statistics()
            self.ui.display_statistics(stats)

    def handle_list(self) -> None:
        """Handle list command."""
        tasks = self.task_manager.list_tasks()
        self.ui.display_tasks(tasks)

    @staticmethod
    def _parse_quoted_input(text: str) -> List[str]:
        """
        Parse quoted strings from input.

        Args:
            text (str): Input text with potential quoted strings

        Returns:
            List[str]: List of parsed arguments
        """
        result = []
        current = ""
        in_quotes = False

        for char in text:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ' ' and not in_quotes:
                if current:
                    result.append(current)
                    current = ""
            else:
                current += char

        if current:
            result.append(current)

        return result


def run_interactive_mode(task_manager: TaskManager) -> None:
    """
    Run the interactive mode where users can enter commands continuously.

    Args:
        task_manager (TaskManager): The task manager instance
    """
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 10 + "🚀 Welcome to Todo Application - Interactive Mode 🚀" + " " * 5 + "║")
    print("╚" + "═" * 68 + "╝\n")

    formatter = UIFormatter()
    formatter.display_menu()

    print("💡 Type 'help' for detailed guide, 'quit' to exit")
    print("-" * 70)

    handler = InteractiveCommandHandler(task_manager)

    # Command dispatcher mapping
    command_dispatcher: Dict[str, Callable[[str], None]] = {
        'list': lambda args: handler.handle_list(),
        'ls': lambda args: handler.handle_list(),
        'add': handler.handle_add,
        'update': handler.handle_update,
        'delete': handler.handle_delete,
        'del': handler.handle_delete,
        'complete': handler.handle_complete,
        'done': handler.handle_complete,
        'incomplete': handler.handle_incomplete,
        'undone': handler.handle_incomplete,
        'show': handler.handle_show,
        'search': handler.handle_search,
        'stats': lambda args: handler.handle_stats(),
        'clear': lambda args: handler.handle_clear(),
        'help': lambda args: formatter.display_help(),
        '?': lambda args: formatter.display_help(),
        'menu': lambda args: formatter.display_menu(),
    }

    while True:
        try:
            user_input = input("todo> ").strip()

            if not user_input:
                continue

            # Handle quitting
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using Todo App. Goodbye!")
                break

            # Parse command and arguments
            command_parts = user_input.split(' ', 1)
            command = command_parts[0].lower()
            args = command_parts[1] if len(command_parts) > 1 else ""

            # Execute command
            if command in command_dispatcher:
                command_dispatcher[command](args)
            else:
                print(f"❌ Unknown command: '{command}'")
                print("💡 Type 'help' for detailed guide or 'menu' to see available operations\n")

        except KeyboardInterrupt:
            print("\n\n👋 Thank you for using Todo App. Goodbye!")
            break
        except EOFError:
            print("\n👋 Thank you for using Todo App. Goodbye!")
            break


# ==================== MAIN APPLICATION ====================


def main():
    """
    Main function to run the Todo application.

    Supports both command-line mode and interactive mode:
    - Interactive mode: Run without arguments
    - Command-line mode: Run with specific commands
    """
    task_manager = TaskManager()

    # Check if no arguments were provided (interactive mode)
    if len(sys.argv) == 1:
        run_interactive_mode(task_manager)
    else:
        # Command-line arguments provided, parse and execute
        parser = parse_command_line_args()
        args = parser.parse_args()

        # If no command is provided, show help
        if args.command is None:
            parser.print_help()
            return

        # Execute the appropriate function based on the command
        args.func(task_manager, args)


if __name__ == "__main__":
    main()
