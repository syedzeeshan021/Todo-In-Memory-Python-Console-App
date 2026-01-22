"""Integration tests for the main todo application flow."""

import pytest
from unittest.mock import Mock, patch

from src.models.task import Task
from src.services.task_service import TaskService
from src.ui.console_ui import ConsoleUI


class TestMainFlow:
    """Integration tests for the main todo application flow."""

    def test_full_crud_flow(self):
        """Test the complete CRUD flow of the application."""
        # Create service and UI
        service = TaskService()
        ui = ConsoleUI(service)

        # Add a task
        task = service.add_task("Test Task", "Test Description")
        assert len(service.get_all_tasks()) == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False

        # Update the task
        updated_task = service.update_task(task.id, "Updated Task", "Updated Description")
        assert updated_task is not None
        assert updated_task.title == "Updated Task"
        assert updated_task.description == "Updated Description"

        # Toggle completion
        completed_task = service.toggle_complete(task.id)
        assert completed_task is not None
        assert completed_task.completed is True
        assert completed_task.completed_at is not None

        # Toggle back to incomplete
        incomplete_task = service.toggle_complete(task.id)
        assert incomplete_task is not None
        assert incomplete_task.completed is False
        assert incomplete_task.completed_at is None

        # Delete the task
        success = service.delete_task(task.id)
        assert success is True
        assert len(service.get_all_tasks()) == 0

    def test_multiple_tasks_flow(self):
        """Test working with multiple tasks."""
        service = TaskService()
        ui = ConsoleUI(service)

        # Add multiple tasks
        task1 = service.add_task("Task 1", "First task")
        task2 = service.add_task("Task 2", "Second task")
        task3 = service.add_task("Task 3", "Third task")

        all_tasks = service.get_all_tasks()
        assert len(all_tasks) == 3

        # Verify tasks are sorted by ID
        assert all_tasks[0].id == 1
        assert all_tasks[1].id == 2
        assert all_tasks[2].id == 3

        # Update middle task
        updated_task = service.update_task(2, "Updated Task 2")
        assert updated_task is not None
        assert updated_task.title == "Updated Task 2"

        # Complete first task
        completed_task = service.toggle_complete(1)
        assert completed_task is not None
        assert completed_task.completed is True

        # Delete second task
        success = service.delete_task(2)
        assert success is True

        # Verify final state
        final_tasks = service.get_all_tasks()
        assert len(final_tasks) == 2
        task_ids = [task.id for task in final_tasks]
        assert 1 in task_ids
        assert 3 in task_ids
        assert 2 not in task_ids

    def test_task_service_validation(self):
        """Test that the service properly validates inputs."""
        service = TaskService()

        # Test title validation
        with pytest.raises(ValueError):
            service.add_task("")  # Empty title

        with pytest.raises(ValueError):
            service.add_task("   ")  # Whitespace-only title

        with pytest.raises(ValueError):
            service.add_task("a" * 201)  # Title too long

        # Test description validation
        with pytest.raises(ValueError):
            service.add_task("Valid Title", "a" * 1001)  # Description too long

        # Test update validation
        task = service.add_task("Valid Task")
        with pytest.raises(ValueError):
            service.update_task(task.id, "")  # Empty title in update