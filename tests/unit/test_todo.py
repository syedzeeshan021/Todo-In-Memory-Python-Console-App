"""
Unit tests for the Todo In-Memory Python Console App.

Tests for Task and TaskManager classes and their methods.
"""
import pytest
from src.main import Task, TaskManager, validate_title, validate_description


class TestTask:
    """Test cases for the Task class."""

    def test_task_creation(self):
        """Test creating a Task instance with valid parameters."""
        task = Task(1, "Test title", "Test description", False)
        assert task.id == 1
        assert task.title == "Test title"
        assert task.description == "Test description"
        assert task.status is False

    def test_task_creation_defaults(self):
        """Test creating a Task instance with default parameters."""
        task = Task(1, "Test title")
        assert task.id == 1
        assert task.title == "Test title"
        assert task.description == ""
        assert task.status is False

    def test_task_str_representation(self):
        """Test the string representation of a Task."""
        task = Task(1, "Test title", "Test description", False)
        expected = "[1] [ ] Test title - Test description"
        assert str(task) == expected

        # Test with complete status
        task.status = True
        expected = "[1] [X] Test title - Test description"
        assert str(task) == expected

    def test_task_to_dict(self):
        """Test converting a Task to dictionary representation."""
        task = Task(1, "Test title", "Test description", True)
        expected_dict = {
            "id": 1,
            "title": "Test title",
            "description": "Test description",
            "status": True
        }
        assert task.to_dict() == expected_dict


class TestTaskManager:
    """Test cases for the TaskManager class."""

    def test_task_manager_initialization(self):
        """Test initializing a TaskManager instance."""
        tm = TaskManager()
        assert tm.tasks == []
        assert tm.next_id == 1

    def test_add_task(self):
        """Test adding a task to the TaskManager."""
        tm = TaskManager()
        task = tm.add_task("Test title", "Test description")

        assert len(tm.tasks) == 1
        assert task.id == 1
        assert task.title == "Test title"
        assert task.description == "Test description"
        assert task.status is False
        assert tm.next_id == 2

    def test_add_task_without_description(self):
        """Test adding a task without description."""
        tm = TaskManager()
        task = tm.add_task("Test title")

        assert len(tm.tasks) == 1
        assert task.id == 1
        assert task.title == "Test title"
        assert task.description == ""
        assert task.status is False

    def test_list_tasks(self):
        """Test listing all tasks."""
        tm = TaskManager()
        tm.add_task("Task 1", "Description 1")
        tm.add_task("Task 2", "Description 2")

        tasks = tm.list_tasks()
        assert len(tasks) == 2
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"

    def test_get_task_by_id(self):
        """Test getting a task by its ID."""
        tm = TaskManager()
        task1 = tm.add_task("Task 1", "Description 1")
        task2 = tm.add_task("Task 2", "Description 2")

        # Test getting existing tasks
        retrieved_task = tm.get_task_by_id(1)
        assert retrieved_task is not None
        assert retrieved_task.id == 1
        assert retrieved_task.title == "Task 1"

        retrieved_task = tm.get_task_by_id(2)
        assert retrieved_task is not None
        assert retrieved_task.id == 2
        assert retrieved_task.title == "Task 2"

        # Test getting non-existing task
        retrieved_task = tm.get_task_by_id(999)
        assert retrieved_task is None

    def test_update_task(self):
        """Test updating a task's title and description."""
        tm = TaskManager()
        task = tm.add_task("Original title", "Original description")

        # Update both title and description
        result = tm.update_task(1, "New title", "New description")
        assert result is True
        assert task.title == "New title"
        assert task.description == "New description"

    def test_update_task_partial(self):
        """Test updating only title or only description."""
        tm = TaskManager()
        task = tm.add_task("Original title", "Original description")

        # Update only title
        result = tm.update_task(1, "Updated title", None)
        assert result is True
        assert task.title == "Updated title"
        assert task.description == "Original description"

        # Update only description
        tm.update_task(1, None, "Updated description")
        assert task.title == "Updated title"
        assert task.description == "Updated description"

    def test_update_nonexistent_task(self):
        """Test updating a non-existent task."""
        tm = TaskManager()
        result = tm.update_task(999, "New title", "New description")
        assert result is False

    def test_delete_task(self):
        """Test deleting a task."""
        tm = TaskManager()
        tm.add_task("Task 1", "Description 1")
        tm.add_task("Task 2", "Description 2")

        # Delete first task
        result = tm.delete_task(1)
        assert result is True
        assert len(tm.tasks) == 1
        assert tm.tasks[0].id == 2

    def test_delete_nonexistent_task(self):
        """Test deleting a non-existent task."""
        tm = TaskManager()
        tm.add_task("Task 1", "Description 1")
        result = tm.delete_task(999)
        assert result is False

    def test_complete_task(self):
        """Test marking a task as complete."""
        tm = TaskManager()
        tm.add_task("Task 1", "Description 1")

        # Verify initial status
        task = tm.get_task_by_id(1)
        assert task.status is False

        # Mark as complete
        result = tm.complete_task(1)
        assert result is True
        task = tm.get_task_by_id(1)
        assert task.status is True

    def test_complete_nonexistent_task(self):
        """Test marking a non-existent task as complete."""
        tm = TaskManager()
        result = tm.complete_task(999)
        assert result is False

    def test_incomplete_task(self):
        """Test marking a task as incomplete."""
        tm = TaskManager()
        tm.add_task("Task 1", "Description 1")

        # Mark as complete first
        tm.complete_task(1)
        task = tm.get_task_by_id(1)
        assert task.status is True

        # Mark as incomplete
        result = tm.incomplete_task(1)
        assert result is True
        task = tm.get_task_by_id(1)
        assert task.status is False

    def test_incomplete_nonexistent_task(self):
        """Test marking a non-existent task as incomplete."""
        tm = TaskManager()
        result = tm.incomplete_task(999)
        assert result is False


class TestValidation:
    """Test cases for validation functions."""

    def test_validate_title_success(self):
        """Test title validation with valid inputs."""
        # Valid title
        validate_title("Valid title")

        # Title at the limit
        validate_title("A" * 200)

    def test_validate_title_failure(self):
        """Test title validation with invalid inputs."""
        # Empty title
        with pytest.raises(ValueError, match="Title cannot be empty"):
            validate_title("")

        # Title with only spaces
        with pytest.raises(ValueError, match="Title cannot be empty"):
            validate_title("   ")

        # Title too long
        with pytest.raises(ValueError, match="Title too long"):
            validate_title("A" * 201)

    def test_validate_description_success(self):
        """Test description validation with valid inputs."""
        # Valid description
        validate_description("Valid description")

        # Empty description (should be allowed)
        validate_description("")

        # Description at the limit
        validate_description("A" * 1000)

    def test_validate_description_failure(self):
        """Test description validation with invalid inputs."""
        # Description too long
        with pytest.raises(ValueError, match="Description too long"):
            validate_description("A" * 1001)