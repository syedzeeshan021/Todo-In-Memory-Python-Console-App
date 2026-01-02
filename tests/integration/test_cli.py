"""
Integration tests for the Todo In-Memory Python Console App CLI.

Tests for the command-line interface and integration between components.
"""
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from src.main import main, TaskManager, Task


def test_add_command():
    """Test the add command functionality."""
    # Capture stdout
    captured_output = io.StringIO()

    # Simulate command line arguments for adding a task
    sys.argv = ['todo', 'add', 'Test task', 'Test description']

    # We'll test this differently since the main function uses argparse
    # which expects sys.argv, but we can test the TaskManager functionality directly

    tm = TaskManager()

    # Test adding a task
    task = tm.add_task("Test task", "Test description")
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.status is False
    assert task.id == 1


def test_list_command():
    """Test the list command functionality."""
    tm = TaskManager()

    # Add some tasks
    tm.add_task("Task 1", "Description 1")
    tm.add_task("Task 2", "Description 2")

    # Test listing tasks
    tasks = tm.list_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"


def test_update_command():
    """Test the update command functionality."""
    tm = TaskManager()

    # Add a task
    task = tm.add_task("Original title", "Original description")
    assert task.title == "Original title"
    assert task.description == "Original description"

    # Update the task
    success = tm.update_task(task.id, "Updated title", "Updated description")
    assert success is True

    # Verify the update
    updated_task = tm.get_task_by_id(task.id)
    assert updated_task.title == "Updated title"
    assert updated_task.description == "Updated description"


def test_delete_command():
    """Test the delete command functionality."""
    tm = TaskManager()

    # Add some tasks
    tm.add_task("Task 1", "Description 1")
    tm.add_task("Task 2", "Description 2")

    # Verify we have 2 tasks
    assert len(tm.list_tasks()) == 2

    # Delete one task
    success = tm.delete_task(1)
    assert success is True

    # Verify we have 1 task left
    assert len(tm.list_tasks()) == 1

    # Verify the remaining task is the second one
    remaining_task = tm.list_tasks()[0]
    assert remaining_task.id == 2
    assert remaining_task.title == "Task 2"


def test_complete_command():
    """Test the complete command functionality."""
    tm = TaskManager()

    # Add a task
    task = tm.add_task("Test task", "Test description")
    assert task.status is False  # Should be incomplete initially

    # Mark as complete
    success = tm.complete_task(task.id)
    assert success is True

    # Verify the status changed
    completed_task = tm.get_task_by_id(task.id)
    assert completed_task.status is True


def test_incomplete_command():
    """Test the incomplete command functionality."""
    tm = TaskManager()

    # Add a task and mark as complete
    task = tm.add_task("Test task", "Test description")
    tm.complete_task(task.id)
    assert task.status is True  # Should be complete

    # Mark as incomplete
    success = tm.incomplete_task(task.id)
    assert success is True

    # Verify the status changed
    incomplete_task = tm.get_task_by_id(task.id)
    assert incomplete_task.status is False


def test_error_handling():
    """Test error handling for invalid operations."""
    tm = TaskManager()

    # Try to get a non-existent task
    task = tm.get_task_by_id(999)
    assert task is None

    # Try to update a non-existent task
    success = tm.update_task(999, "New title", "New description")
    assert success is False

    # Try to delete a non-existent task
    success = tm.delete_task(999)
    assert success is False

    # Try to complete a non-existent task
    success = tm.complete_task(999)
    assert success is False

    # Try to mark incomplete a non-existent task
    success = tm.incomplete_task(999)
    assert success is False


def test_input_validation():
    """Test input validation functionality."""
    tm = TaskManager()

    # Test that empty title is not allowed
    try:
        tm.add_task("", "Description")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Title cannot be empty" in str(e)

    # Test that long title is not allowed
    try:
        tm.add_task("A" * 201, "Description")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Title too long" in str(e)

    # Test that long description is not allowed
    try:
        tm.add_task("Title", "A" * 1001)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Description too long" in str(e)