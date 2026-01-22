"""Console user interface for the todo application."""

from typing import Optional

from src.services.task_service import TaskService


class ConsoleUI:
    """Console user interface for the todo application."""

    def __init__(self, task_service: TaskService) -> None:
        """Initialize the console UI with a task service.

        Args:
            task_service: The task service to interact with
        """
        self.task_service = task_service

    def display_menu(self) -> None:
        """Display the available commands to the user."""
        print("\n--- Todo Application ---")
        print("Available commands:")
        print("  add <title> [description] - Add a new task")
        print("  list - Show all tasks")
        print("  update <id> <title> [description] - Update a task")
        print("  complete <id> - Mark task as complete/incomplete")
        print("  delete <id> - Delete a task")
        print("  quit - Exit the application")
        print("  help - Show this menu")
        print("------------------------")

    def display_tasks(self) -> None:
        """Display all tasks in a formatted list."""
        tasks = self.task_service.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        print("\nYour tasks:")
        for task in tasks:
            completed_str = "COMPLETED" if task.completed else "PENDING"
            completed_at_str = f", Completed at: {task.completed_at}" if task.completed_at else ""
            created_at_str = task.created_at.strftime('%Y-%m-%d %H:%M:%S') if task.created_at else 'N/A'
            updated_at_str = task.updated_at.strftime('%Y-%m-%d %H:%M:%S') if task.updated_at else 'N/A'
            print(
                f"  {task} - {task.description} "
                f"(Created: {created_at_str}, "
                f"Updated: {updated_at_str}, "
                f"Status: {completed_str}{completed_at_str})"
            )

    def get_task_id_from_input(self, input_str: str, command_name: str) -> Optional[int]:
        """Extract and validate task ID from user input.

        Args:
            input_str: The user input string
            command_name: The name of the command for error messages

        Returns:
            The task ID if valid, None otherwise
        """
        try:
            task_id = int(input_str)
            if task_id <= 0:
                print(f"Error: Task ID must be a positive integer for '{command_name}' command")
                return None
            return task_id
        except ValueError:
            print(
                f"Error: Invalid task ID '{input_str}' for '{command_name}' command. "
                "Please enter a number."
            )
            return None

    def confirm_deletion(self, task_id: int) -> bool:
        """Ask user for confirmation before deleting a task.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if user confirms deletion, False otherwise
        """
        response = input(f"Are you sure you want to delete task {task_id}? (y/N): ").strip().lower()
        return response in ("y", "yes")

    def run(self) -> None:
        """Run the main interactive command loop."""
        print("Welcome to the Todo Application!")
        self.display_menu()

        while True:
            if self._handle_user_interaction():
                break

    def _handle_user_interaction(self) -> bool:
        """Handle a single user interaction cycle.

        Returns:
            True if the application should exit, False otherwise
        """
        try:
            user_input = input("\nEnter command: ").strip()

            if not user_input:
                print("Please enter a command. Type 'help' for available commands.")
                return False

            # Parse command and arguments
            parts = user_input.split(" ", 1)
            command = parts[0].lower()
            args_str = parts[1] if len(parts) > 1 else ""

            return self._execute_command(command, args_str)

        except KeyboardInterrupt:
            print("\n\nReceived interrupt signal. Goodbye!")
            return True
        except EOFError:
            print("\n\nEnd of input received. Goodbye!")
            return True

    def _execute_command(self, command: str, args_str: str) -> bool:
        """Execute the given command with arguments.

        Args:
            command: The command to execute
            args_str: Arguments for the command

        Returns:
            True if the application should exit, False otherwise
        """
        if command == "quit":
            print("Goodbye!")
            return True
        elif command == "help":
            self.display_menu()
        elif command == "list":
            self.display_tasks()
        elif command == "add":
            self.handle_add_command(args_str)
        elif command == "update":
            self.handle_update_command(args_str)
        elif command == "complete":
            self.handle_complete_command(args_str)
        elif command == "delete":
            self.handle_delete_command(args_str)
        else:
            print(f"Unknown command: '{command}'. Type 'help' for available commands.")

        return False

    def handle_add_command(self, args_str: str) -> None:
        """Handle the 'add' command to add a new task.

        Args:
            args_str: The arguments part of the command
        """
        if not args_str:
            print("Usage: add <title> [description]")
            return

        # Split title and description
        parts = args_str.split(" ", 1)
        title = parts[0]
        description = parts[1] if len(parts) > 1 else ""

        try:
            task = self.task_service.add_task(title, description)
            print(f"Task added successfully with ID {task.id}: {task.title}")
        except ValueError as e:
            print(f"Error adding task: {e}")

    def handle_update_command(self, args_str: str) -> None:
        """Handle the 'update' command to update an existing task.

        Args:
            args_str: The arguments part of the command
        """
        if not args_str:
            print("Usage: update <id> <title> [description]")
            return

        # Split ID, title, and description
        parts = args_str.split(" ", 2)
        if len(parts) < 2:
            print("Usage: update <id> <title> [description]")
            return

        task_id_str = parts[0]
        title = parts[1]
        description = parts[2] if len(parts) > 2 else ""

        # Validate task ID
        task_id = self.get_task_id_from_input(task_id_str, "update")
        if task_id is None:
            return

        try:
            updated_task = self.task_service.update_task(task_id, title, description)
            if updated_task:
                print(f"Task {task_id} updated successfully: {updated_task.title}")
            else:
                print(f"Task with ID {task_id} not found.")
        except ValueError as e:
            print(f"Error updating task: {e}")

    def handle_complete_command(self, args_str: str) -> None:
        """Handle the 'complete' command to toggle task completion.

        Args:
            args_str: The arguments part of the command
        """
        if not args_str:
            print("Usage: complete <id>")
            return

        task_id = self.get_task_id_from_input(args_str, "complete")
        if task_id is None:
            return

        task = self.task_service.toggle_complete(task_id)
        if task:
            status = "completed" if task.completed else "marked as incomplete"
            print(f"Task {task_id} {status}.")
        else:
            print(f"Task with ID {task_id} not found.")

    def handle_delete_command(self, args_str: str) -> None:
        """Handle the 'delete' command to delete a task.

        Args:
            args_str: The arguments part of the command
        """
        if not args_str:
            print("Usage: delete <id>")
            return

        task_id = self.get_task_id_from_input(args_str, "delete")
        if task_id is None:
            return

        # Confirm deletion
        if not self.confirm_deletion(task_id):
            print("Deletion cancelled.")
            return

        success = self.task_service.delete_task(task_id)
        if success:
            print(f"Task {task_id} deleted successfully.")
        else:
            print(f"Task with ID {task_id} not found.")
