"""Unit tests for the main module."""

from unittest.mock import patch, MagicMock
import io
import sys

from src import main


class TestMain:
    """Unit tests for the main module."""

    @patch('src.main.ConsoleUI')
    @patch('src.main.TaskService')
    def test_main_function_runs_ui(self, mock_task_service_class, mock_console_ui_class):
        """Test that the main function initializes and runs the UI."""
        mock_task_service_instance = MagicMock()
        mock_task_service_class.return_value = mock_task_service_instance

        mock_ui_instance = MagicMock()
        mock_console_ui_class.return_value = mock_ui_instance

        # Run the main function
        main.main()

        # Verify that TaskService was initialized
        mock_task_service_class.assert_called_once()

        # Verify that ConsoleUI was initialized with the task service
        mock_console_ui_class.assert_called_once_with(mock_task_service_instance)

        # Verify that the UI run method was called
        mock_ui_instance.run.assert_called_once()

    @patch('src.main.ConsoleUI')
    @patch('src.main.TaskService')
    @patch('builtins.print')
    def test_main_keyboard_interrupt_handling(self, mock_print, mock_task_service_class, mock_console_ui_class):
        """Test that the main function handles KeyboardInterrupt gracefully."""
        mock_task_service_instance = MagicMock()
        mock_task_service_class.return_value = mock_task_service_instance

        mock_ui_instance = MagicMock()
        mock_console_ui_class.return_value = mock_ui_instance

        # Make the UI run method raise KeyboardInterrupt
        mock_ui_instance.run.side_effect = KeyboardInterrupt()

        # Run the main function
        main.main()

        # Verify that goodbye message was printed
        mock_print.assert_called()

    @patch('src.main.ConsoleUI')
    @patch('src.main.TaskService')
    @patch('builtins.print')
    def test_main_exception_handling(self, mock_print, mock_task_service_class, mock_console_ui_class):
        """Test that the main function handles general exceptions gracefully."""
        mock_task_service_instance = MagicMock()
        mock_task_service_class.return_value = mock_task_service_instance

        mock_ui_instance = MagicMock()
        mock_console_ui_class.return_value = mock_ui_instance

        # Make the UI run method raise a general exception
        mock_ui_instance.run.side_effect = RuntimeError("Test error")

        # Run the main function
        main.main()

        # Verify that error message was printed
        mock_print.assert_called()