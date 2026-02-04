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


def parse_command_line_args():
    """
    Set up and parse command line arguments.
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


def display_menu():
    """
    Display an attractive CRUD menu for the todo application.
    """
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


def display_help():
    """
    Display detailed help information.
    """
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


def run_interactive_mode(task_manager):
    """
    Run the interactive mode where users can enter commands continuously.
    Enhanced with better parsing, command history, and user experience.
    """
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 10 + "🚀 Welcome to Todo Application - Interactive Mode 🚀" + " " * 5 + "║")
    print("╚" + "═" * 68 + "╝\n")
    
    # Display the menu immediately
    display_menu()
    
    print("💡 Type 'help' for detailed guide, 'quit' to exit")
    print("-" * 70)

    # Command history for reference (not actually storing but showing the concept)
    command_history = []

    while True:
        try:
            # Get user input
            user_input = input("todo> ").strip()

            # Add to command history if not empty
            if user_input:
                command_history.append(user_input)

            if not user_input:
                continue

            # Handle special commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using Todo App. Goodbye!")
                break
            elif user_input.lower() in ['help', '?']:
                display_help()
                continue
            elif user_input.lower() in ['menu']:
                display_menu()
                continue
            elif user_input.lower() in ['list', 'ls']:
                # Handle list command
                args = argparse.Namespace()
                tasks = task_manager.list_tasks()
                
                if not tasks:
                    print("\n📭 No tasks available. Start by adding one!")
                else:
                    print("\n" + "─" * 70)
                    print("📋 YOUR TASKS:")
                    print("─" * 70)
                    for task in tasks:
                        status_indicator = "✅" if task.status else "⭕"
                        status_text = "Done" if task.status else "Pending"
                        desc_text = f" | {task.description}" if task.description else ""
                        print(f"  {status_indicator} [{task.id}] {task.title}{desc_text} ({status_text})")
                    
                    # Show statistics after listing
                    total = len(tasks)
                    completed = len([t for t in tasks if t.status])
                    incomplete = total - completed
                    completion_rate = (completed / total * 100) if total > 0 else 0
                    print("─" * 70)
                    print(f"  📊 Total: {total} | ✅ Completed: {completed} | ⭕ Pending: {incomplete} | Rate: {completion_rate:.0f}%")
                    print("─" * 70 + "\n")
                continue
            elif user_input.lower().startswith('add '):
                # Handle add command - parse quoted strings properly
                command_part = user_input[4:]  # Remove 'add ' prefix
                title = ""
                description = ""

                # Parse quoted strings properly
                i = 0
                in_quotes = False
                current_string = ""

                while i < len(command_part):
                    if command_part[i] == '"':
                        if in_quotes:
                            # End of quoted string
                            title = current_string if not title else title
                            description = current_string if title else current_string
                            current_string = ""
                            in_quotes = False
                        else:
                            # Start of quoted string
                            in_quotes = True
                            current_string = ""
                        i += 1
                    elif command_part[i] == ' ' and not in_quotes:
                        if current_string:
                            if not title:
                                title = current_string
                            else:
                                # This should be part of description
                                if description:
                                    description += ' ' + current_string
                                else:
                                    description = current_string
                        elif not title and not current_string and not in_quotes:
                            # Skip multiple spaces before first word
                            pass
                        current_string = ""
                        i += 1
                    else:
                        current_string += command_part[i]
                        i += 1

                # Handle remaining text after loop
                if current_string:
                    if not title:
                        title = current_string
                    else:
                        if description:
                            description += ' ' + current_string
                        else:
                            description = current_string

                # If still empty, try simple split
                if not title and not description:
                    parts = command_part.strip().split(' ', 1)
                    if parts:
                        title = parts[0]
                        if len(parts) > 1:
                            description = parts[1]

                if not title:
                    print("Error: Title is required. Usage: add <title> [description]")
                    continue

                args = argparse.Namespace(title=title, description=description)
                try:
                    task = task_manager.add_task(title, description)
                    print(f"\n✨ Task added successfully!")
                    print(f"   ID: {task.id} | Title: {task.title}")
                    if description:
                        print(f"   Description: {task.description}")
                    print()
                except ValueError as e:
                    print(f"❌ Error: {e}\n")
                continue
            elif user_input.lower().startswith('update '):
                # Handle update command with improved parsing
                command_part = user_input[7:]  # Remove 'update ' prefix
                parts = command_part.split()

                if len(parts) < 1:
                    print("Usage: update <id> [--title <text>] [--description <text>]")
                    continue

                try:
                    task_id = int(parts[0])
                except ValueError:
                    print("Error: Task ID must be a number")
                    continue

                # Parse remaining arguments
                title = None
                description = None
                i = 1
                while i < len(parts):
                    if parts[i] == '--title' and i + 1 < len(parts):
                        title = parts[i + 1]
                        if title.startswith('"') and title.endswith('"'):
                            title = title[1:-1]
                        i += 2
                    elif parts[i] == '--description' and i + 1 < len(parts):
                        description = parts[i + 1]
                        if description.startswith('"') and description.endswith('"'):
                            description = description[1:-1]
                        i += 2
                    elif parts[i].startswith('--'):
                        print(f"Unknown option: {parts[i]}")
                        print("Usage: update <id> [--title <text>] [--description <text>]")
                        break
                    else:
                        i += 1
                else:
                    # Only proceed if no error occurred in the loop
                    try:
                        success = task_manager.update_task(task_id, title, description)
                        if success:
                            task = task_manager.get_task_by_id(task_id)
                            print(f"\n✏️  Task {task_id} updated successfully!")
                            print(f"   Title: {task.title}")
                            print(f"   Description: {task.description}\n")
                        else:
                            print(f"❌ Error: Task with ID {task_id} not found\n")
                    except ValueError as e:
                        print(f"❌ Error: {e}\n")
                continue
            elif user_input.lower().startswith(('delete ', 'del ')):
                # Handle delete command (support both 'delete' and 'del')
                command_part = user_input.split(' ', 1)
                if len(command_part) < 2:
                    print("Usage: delete <id> or del <id>")
                    continue

                try:
                    task_id = int(command_part[1])
                    task = task_manager.get_task_by_id(task_id)
                    if task:
                        success = task_manager.delete_task(task_id)
                        if success:
                            print(f"\n🗑️  Task {task_id} deleted successfully!")
                            print(f"   Removed: {task.title}\n")
                        else:
                            print(f"❌ Error: Could not delete task {task_id}\n")
                    else:
                        print(f"❌ Error: Task with ID {task_id} not found\n")
                except ValueError:
                    print("Error: Task ID must be a number\n")
                continue
            elif user_input.lower().startswith(('complete ', 'done ')):
                # Handle complete command (support both 'complete' and 'done')
                command_part = user_input.split(' ', 1)
                if len(command_part) < 2:
                    print("Usage: complete <id> or done <id>")
                    continue

                try:
                    task_id = int(command_part[1])
                    task = task_manager.get_task_by_id(task_id)
                    if task:
                        success = task_manager.complete_task(task_id)
                        if success:
                            print(f"\n✅ Task {task_id} marked as complete!")
                            print(f"   {task.title}\n")
                        else:
                            print(f"❌ Error: Could not mark task {task_id} as complete\n")
                    else:
                        print(f"❌ Error: Task with ID {task_id} not found\n")
                except ValueError:
                    print("Error: Task ID must be a number\n")
                continue
            elif user_input.lower().startswith(('incomplete ', 'undone ')):
                # Handle incomplete command (support 'incomplete' and 'undone')
                command_part = user_input.split(' ', 1)
                if len(command_part) < 2:
                    print("Usage: incomplete <id> or undone <id>")
                    continue

                try:
                    task_id = int(command_part[1])
                    task = task_manager.get_task_by_id(task_id)
                    if task:
                        success = task_manager.incomplete_task(task_id)
                        if success:
                            print(f"\n⭕ Task {task_id} marked as incomplete!")
                            print(f"   {task.title}\n")
                        else:
                            print(f"❌ Error: Could not mark task {task_id} as incomplete\n")
                    else:
                        print(f"❌ Error: Task with ID {task_id} not found\n")
                except ValueError:
                    print("Error: Task ID must be a number\n")
                continue
            elif user_input.lower().startswith('show '):
                # Show details of a specific task
                command_part = user_input.split(' ', 1)
                if len(command_part) < 2:
                    print("Usage: show <id>")
                    continue

                try:
                    task_id = int(command_part[1])
                    task = task_manager.get_task_by_id(task_id)
                    if task:
                        status_text = "✅ Complete" if task.status else "⭕ Incomplete"
                        print("\n" + "─" * 70)
                        print(f"📝 TASK DETAILS (ID: {task.id})")
                        print("─" * 70)
                        print(f"  Title:       {task.title}")
                        print(f"  Description: {task.description if task.description else '(No description)'}")
                        print(f"  Status:      {status_text}")
                        print("─" * 70 + "\n")
                    else:
                        print(f"❌ Error: Task with ID {task_id} not found\n")
                except ValueError:
                    print("Error: Task ID must be a number\n")
                continue
            elif user_input.lower() == 'clear':
                # Clear all tasks
                if not task_manager.tasks:
                    print("\n📭 No tasks to clear\n")
                else:
                    task_count = len(task_manager.tasks)
                    task_manager.tasks.clear()
                    task_manager.next_id = 1  # Reset ID counter
                    print(f"\n🗑️  Successfully cleared {task_count} task(s)!")
                    print("   Task counter has been reset.\n")
                continue
            elif user_input.lower() == 'stats':
                # Show statistics
                total = len(task_manager.tasks)
                if total == 0:
                    print("\n📭 No tasks available\n")
                else:
                    completed = len([t for t in task_manager.tasks if t.status])
                    incomplete = total - completed
                    completion_rate = (completed / total * 100) if total > 0 else 0

                    print("\n" + "─" * 70)
                    print("📊 TASK STATISTICS")
                    print("─" * 70)
                    print(f"  Total Tasks:    {total}")
                    print(f"  ✅ Completed:   {completed}")
                    print(f"  ⭕ Incomplete:  {incomplete}")
                    print(f"  📈 Completion Rate: {completion_rate:.1f}%")
                    print("─" * 70 + "\n")
                continue
            elif user_input.lower().startswith('search '):
                # Search tasks by keyword in title or description
                keyword = user_input[7:].strip().lower()
                if not keyword:
                    print("Usage: search <keyword>")
                    continue

                matches = []
                for task in task_manager.tasks:
                    if keyword in task.title.lower() or keyword in task.description.lower():
                        matches.append(task)

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
                continue
            else:
                print(f"❌ Unknown command: '{user_input}'")
                print("💡 Type 'help' for detailed guide or 'menu' to see available operations\n")

        except KeyboardInterrupt:
            print("\n\n👋 Thank you for using Todo App. Goodbye!")
            break
        except EOFError:
            print("\n👋 Thank you for using Todo App. Goodbye!")
            break


def main():
    """
    Main function to run the Todo application.
    Sets up the argument parser and handles commands.
    Supports both command-line mode and interactive mode.
    """
    # Create the task manager instance
    task_manager = TaskManager()

    # Check if no arguments were provided (interactive mode)
    if len(sys.argv) == 1:
        # No command-line arguments provided, start interactive mode
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