"""Unit tests for the Task dataclass."""

import pytest
from datetime import datetime

from src.models.task import Task


class TestTask:
    """Unit tests for the Task dataclass."""

    def test_task_creation(self):
        """Test creating a task with all required fields."""
        task_id = 1
        title = "Test Task"
        description = "Test Description"
        completed = False
        created_at = datetime.now()
        updated_at = datetime.now()

        task = Task(
            id=task_id,
            title=title,
            description=description,
            completed=completed,
            created_at=created_at,
            updated_at=updated_at,
        )

        assert task.id == task_id
        assert task.title == title
        assert task.description == description
        assert task.completed == completed
        assert task.created_at == created_at
        assert task.updated_at == updated_at
        assert task.completed_at is None

    def test_task_creation_with_completed_at(self):
        """Test creating a task with completed_at."""
        task_id = 1
        title = "Test Task"
        description = "Test Description"
        completed = True
        created_at = datetime.now()
        updated_at = datetime.now()
        completed_at = datetime.now()

        task = Task(
            id=task_id,
            title=title,
            description=description,
            completed=completed,
            created_at=created_at,
            updated_at=updated_at,
            completed_at=completed_at,
        )

        assert task.completed_at == completed_at

    def test_task_str_representation(self):
        """Test the string representation of a task."""
        task = Task(
            id=1,
            title="Test Task",
            description="Test Description",
            completed=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        expected = "[ ] [1] Test Task"
        assert str(task) == expected

    def test_task_str_representation_completed(self):
        """Test the string representation of a completed task."""
        task = Task(
            id=1,
            title="Test Task",
            description="Test Description",
            completed=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        expected = "[x] [1] Test Task"
        assert str(task) == expected

    def test_task_repr_representation(self):
        """Test the detailed string representation of a task."""
        created_at = datetime.now()
        updated_at = datetime.now()
        task = Task(
            id=1,
            title="Test Task",
            description="Test Description",
            completed=False,
            created_at=created_at,
            updated_at=updated_at,
        )

        repr_str = repr(task)
        assert "Task(id=1" in repr_str
        assert "title='Test Task'" in repr_str
        assert "description='Test Description'" in repr_str
        assert "completed=False" in repr_str