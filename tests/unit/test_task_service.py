"""Unit tests for the TaskService class."""

import pytest
from datetime import datetime

from src.models.task import Task
from src.services.task_service import TaskService


class TestTaskService:
    """Unit tests for the TaskService class."""

    def test_initial_state(self):
        """Test that TaskService initializes with empty storage and ID counter."""
        service = TaskService()

        assert len(service.get_all_tasks()) == 0
        assert service.next_id == 1

    def test_add_task_success(self):
        """Test adding a task successfully."""
        service = TaskService()

        task = service.add_task("Test Title", "Test Description")

        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description == "Test Description"
        assert task.completed is False
        assert task.created_at <= datetime.now()
        assert task.updated_at <= datetime.now()
        assert task.completed_at is None

        # Verify task is stored
        all_tasks = service.get_all_tasks()
        assert len(all_tasks) == 1
        assert all_tasks[0].id == 1

        # Verify next ID is incremented
        assert service.next_id == 2

    def test_add_task_without_description(self):
        """Test adding a task without description."""
        service = TaskService()

        task = service.add_task("Test Title")

        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description == ""
        assert task.completed is False

    def test_add_task_title_validation(self):
        """Test validation for task title."""
        service = TaskService()

        # Empty title
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.add_task("")

        # Whitespace-only title
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.add_task("   ")

        # Title too long
        with pytest.raises(ValueError, match="Task title must be between 1 and 200 characters"):
            service.add_task("a" * 201)

    def test_add_task_description_validation(self):
        """Test validation for task description."""
        service = TaskService()

        # Description too long
        with pytest.raises(ValueError, match="Task description cannot exceed 1000 characters"):
            service.add_task("Test Title", "a" * 1001)

    def test_delete_task_success(self):
        """Test deleting an existing task."""
        service = TaskService()
        task = service.add_task("Test Title")
        task_id = task.id

        result = service.delete_task(task_id)

        assert result is True
        assert service.get_task(task_id) is None
        assert len(service.get_all_tasks()) == 0

    def test_delete_task_not_exists(self):
        """Test deleting a non-existent task."""
        service = TaskService()

        result = service.delete_task(999)

        assert result is False

    def test_update_task_title_success(self):
        """Test updating a task's title."""
        service = TaskService()
        original_task = service.add_task("Original Title", "Original Description")
        task_id = original_task.id

        updated_task = service.update_task(task_id, "New Title")

        assert updated_task is not None
        assert updated_task.id == task_id
        assert updated_task.title == "New Title"
        assert updated_task.description == "Original Description"  # Should remain unchanged
        # The updated_at should be the same or later than original
        assert updated_task.updated_at >= original_task.updated_at

    def test_update_task_description_success(self):
        """Test updating a task's description."""
        service = TaskService()
        original_task = service.add_task("Original Title", "Original Description")
        task_id = original_task.id

        updated_task = service.update_task(task_id, description="New Description")

        assert updated_task is not None
        assert updated_task.id == task_id
        assert updated_task.title == "Original Title"  # Should remain unchanged
        assert updated_task.description == "New Description"
        # The updated_at should be the same or later than original
        assert updated_task.updated_at >= original_task.updated_at

    def test_update_task_both_fields_success(self):
        """Test updating both title and description."""
        service = TaskService()
        original_task = service.add_task("Original Title", "Original Description")
        task_id = original_task.id

        updated_task = service.update_task(task_id, "New Title", "New Description")

        assert updated_task is not None
        assert updated_task.id == task_id
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"
        # The updated_at should be the same or later than original
        assert updated_task.updated_at >= original_task.updated_at

    def test_update_task_not_exists(self):
        """Test updating a non-existent task."""
        service = TaskService()

        result = service.update_task(999, "New Title")

        assert result is None

    def test_update_task_validation(self):
        """Test validation during task update."""
        service = TaskService()
        original_task = service.add_task("Original Title")
        task_id = original_task.id

        # Empty title
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.update_task(task_id, "")

        # Title too long
        with pytest.raises(ValueError, match="Task title must be between 1 and 200 characters"):
            service.update_task(task_id, "a" * 201)

        # Description too long
        with pytest.raises(ValueError, match="Task description cannot exceed 1000 characters"):
            service.update_task(task_id, description="a" * 1001)

    def test_get_all_tasks_sorted(self):
        """Test that get_all_tasks returns tasks sorted by ID."""
        service = TaskService()
        task3 = service.add_task("Task 3")
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")

        all_tasks = service.get_all_tasks()

        assert len(all_tasks) == 3
        assert all_tasks[0].id == 1
        assert all_tasks[1].id == 2
        assert all_tasks[2].id == 3

    def test_get_task_success(self):
        """Test getting a specific task by ID."""
        service = TaskService()
        original_task = service.add_task("Test Title")
        task_id = original_task.id

        retrieved_task = service.get_task(task_id)

        assert retrieved_task is not None
        assert retrieved_task.id == task_id
        assert retrieved_task.title == "Test Title"

    def test_get_task_not_exists(self):
        """Test getting a non-existent task."""
        service = TaskService()

        result = service.get_task(999)

        assert result is None

    def test_toggle_complete_success(self):
        """Test toggling a task's completion status."""
        service = TaskService()
        original_task = service.add_task("Test Title")
        task_id = original_task.id

        # Toggle to complete
        completed_task = service.toggle_complete(task_id)

        assert completed_task is not None
        assert completed_task.completed is True
        assert completed_task.completed_at is not None
        # The updated_at should be the same or later than original
        assert completed_task.updated_at >= original_task.updated_at

        # Toggle back to incomplete
        incomplete_task = service.toggle_complete(task_id)

        assert incomplete_task is not None
        assert incomplete_task.completed is False
        assert incomplete_task.completed_at is None
        # The updated_at should be the same or later than previous
        assert incomplete_task.updated_at >= completed_task.updated_at

    def test_toggle_complete_not_exists(self):
        """Test toggling completion for a non-existent task."""
        service = TaskService()

        result = service.toggle_complete(999)

        assert result is None