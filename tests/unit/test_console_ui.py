"""Unit tests for the ConsoleUI class."""

from unittest.mock import Mock, patch, MagicMock
from io import StringIO
import sys

from src.models.task import Task
from src.services.task_service import TaskService
from src.ui.console_ui import ConsoleUI
from datetime import datetime


class TestConsoleUI:
    """Unit tests for the ConsoleUI class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.mock_service = Mock(spec=TaskService)
        self.ui = ConsoleUI(self.mock_service)

    @patch('builtins.input', side_effect=['quit'])
    @patch('builtins.print')
    def test_run_quit_command(self, mock_print, mock_input):
        """Test running the UI and quitting."""
        self.ui.run()
        mock_print.assert_any_call("Goodbye!")

    @patch('builtins.input', side_effect=['help', 'quit'])
    @patch('builtins.print')
    def test_run_help_command(self, mock_print, mock_input):
        """Test running the UI with help command."""
        self.ui.run()
        # Help menu should be displayed
        assert any(call.args and 'Available commands:' in str(call.args[0]) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['list', 'quit'])
    @patch('builtins.print')
    def test_run_list_command(self, mock_print, mock_input):
        """Test running the UI with list command."""
        # Mock the service to return some tasks
        mock_task = Task(1, "Test Task", "Description", False, datetime.now(), datetime.now())
        self.mock_service.get_all_tasks.return_value = [mock_task]

        self.ui.run()

        # Verify that the service method was called
        self.mock_service.get_all_tasks.assert_called_once()

    @patch('builtins.input', side_effect=['add Test Title Test Description', 'quit'])
    @patch('builtins.print')
    def test_run_add_command(self, mock_print, mock_input):
        """Test running the UI with add command."""
        # Mock the service to return a task when add_task is called
        mock_task = Task(1, "Test Title", "Test Description", False, datetime.now(), datetime.now())
        self.mock_service.add_task.return_value = mock_task

        self.ui.run()

        # Verify that the service method was called
        # Note: The first word is title, the rest is description
        self.mock_service.add_task.assert_called_once_with("Test", "Title Test Description")

    @patch('builtins.input', side_effect=['invalid_command', 'quit'])
    @patch('builtins.print')
    def test_run_invalid_command(self, mock_print, mock_input):
        """Test running the UI with an invalid command."""
        self.ui.run()

        # Verify that an unknown command message was printed
        assert any(
            call.args and 'Unknown command:' in str(call.args[0])
            for call in mock_print.call_args_list
        )

    def test_display_menu(self):
        """Test displaying the menu."""
        with patch('builtins.print') as mock_print:
            self.ui.display_menu()

            # Check that menu items are displayed
            assert any(
                call.args and 'Available commands:' in str(call.args[0])
                for call in mock_print.call_args_list
            )

    def test_get_task_id_from_input_valid(self):
        """Test getting a valid task ID from input."""
        result = self.ui.get_task_id_from_input("5", "test")
        assert result == 5

    def test_get_task_id_from_input_invalid(self):
        """Test getting an invalid task ID from input."""
        with patch('builtins.print'):
            result = self.ui.get_task_id_from_input("abc", "test")
            assert result is None

    def test_get_task_id_from_input_negative(self):
        """Test getting a negative task ID from input."""
        with patch('builtins.print'):
            result = self.ui.get_task_id_from_input("-5", "test")
            assert result is None

    @patch('builtins.input', return_value='y')
    def test_confirm_deletion_yes(self, mock_input):
        """Test confirming deletion with 'y'."""
        result = self.ui.confirm_deletion(1)
        assert result is True

    @patch('builtins.input', return_value='n')
    def test_confirm_deletion_no(self, mock_input):
        """Test confirming deletion with 'n'."""
        result = self.ui.confirm_deletion(1)
        assert result is False

    def test_handle_add_command(self):
        """Test handling the add command."""
        with patch('builtins.print'):
            self.ui.handle_add_command("Test Title Test Description")

        # Verify that add_task was called with the correct parameters
        # Note: The first word is title, the rest is description
        self.mock_service.add_task.assert_called_once_with("Test", "Title Test Description")

    def test_handle_update_command(self):
        """Test handling the update command."""
        with patch('builtins.print'):
            self.ui.handle_update_command("1 New Title New Description")

        # Verify that update_task was called with the correct parameters
        # Note: The first word is ID, second is title, the rest is description
        self.mock_service.update_task.assert_called_once_with(1, "New", "Title New Description")

    def test_handle_complete_command(self):
        """Test handling the complete command."""
        mock_task = Task(1, "Test", "", True, datetime.now(), datetime.now())
        self.mock_service.toggle_complete.return_value = mock_task

        with patch('builtins.print'):
            self.ui.handle_complete_command("1")

        # Verify that toggle_complete was called with the correct parameters
        self.mock_service.toggle_complete.assert_called_once_with(1)

    def test_handle_delete_command_confirmed(self):
        """Test handling the delete command with confirmation."""
        self.mock_service.delete_task.return_value = True

        with patch('builtins.input', return_value='y'), \
             patch('builtins.print'):
            self.ui.handle_delete_command("1")

        # Verify that delete_task was called
        self.mock_service.delete_task.assert_called_once_with(1)

    def test_display_tasks_empty(self):
        """Test displaying tasks when no tasks exist."""
        self.mock_service.get_all_tasks.return_value = []

        with patch('builtins.print'):
            self.ui.display_tasks()

        # Should print "No tasks found."
        self.mock_service.get_all_tasks.assert_called_once()