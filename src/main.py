"""Main entry point for the todo application."""

from src.services.task_service import TaskService
from src.ui.console_ui import ConsoleUI


def main() -> None:
    """Main function to run the todo application."""
    try:
        # Initialize the task service
        task_service = TaskService()

        # Initialize the console UI with the task service
        ui = ConsoleUI(task_service)

        # Run the application
        ui.run()

    except KeyboardInterrupt:
        print("\nApplication interrupted. Goodbye!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Please report this issue.")
    finally:
        print("Thank you for using the Todo Application!")


if __name__ == "__main__":
    main()
