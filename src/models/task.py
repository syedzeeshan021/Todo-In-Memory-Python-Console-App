"""
Task dataclass representing a single todo item.

This module defines the Task dataclass with all required fields,
validation, and timestamp management for the console todo application.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """
    Represents a single todo item with all required fields.

    Attributes:
        id: Sequential identifier, immutable after creation
        title: Task title, 1-200 characters
        description: Task description, max 1000 characters
        completed: Completion status
        created_at: Creation timestamp
        updated_at: Last update timestamp
        completed_at: Completion timestamp (None if incomplete)
    """

    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Initialize timestamps if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

        # Validate field constraints
        self._validate_fields()

    def _validate_fields(self) -> None:
        """Validate field constraints."""
        # Validate title: 1-200 characters
        if not isinstance(self.title, str) or len(self.title.strip()) == 0:
            raise ValueError("Title must be a non-empty string")

        title_stripped = self.title.strip()
        if len(title_stripped) < 1 or len(title_stripped) > 200:
            raise ValueError(f"Title must be between 1 and 200 characters, got {len(title_stripped)}")

        # Validate description: max 1000 characters
        if not isinstance(self.description, str):
            raise ValueError("Description must be a string")

        if len(self.description) > 1000:
            raise ValueError(f"Description must be 1000 characters or less, got {len(self.description)}")

    def update_timestamps(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()

    def toggle_completion(self) -> None:
        """Toggle the completion status and update timestamps."""
        self.completed = not self.completed
        if self.completed:
            self.completed_at = datetime.now()
        else:
            self.completed_at = None
        self.update_timestamps()

    def __str__(self) -> str:
        """String representation of the task."""
        status = "[x]" if self.completed else "[ ]"
        return f"{status} [{self.id}] {self.title}"

    def to_dict(self) -> dict:
        """Convert task to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
