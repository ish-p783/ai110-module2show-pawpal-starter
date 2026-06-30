"""PawPal+ logic layer.

This module holds all the backend classes for PawPal+:
Owner, Pet, Task, and Scheduler. The Streamlit UI (app.py)
will import and use these classes.

Skeleton generated from diagrams/uml.mmd. Methods are stubs
(no logic yet) -- fill them in step by step.
"""

from dataclasses import dataclass, field


@dataclass
class Pet:
    """A pet the owner cares for."""

    name: str
    breed: str = ""
    gender: str = ""
    weight: float = 0.0
    height: float = 0.0
    age: int = 0
    health_conditions: str = ""

    def update_info(self) -> None:
        """Update this pet's stored information."""
        raise NotImplementedError


@dataclass
class Task:
    """A single care task (walk, feed, meds, etc.)."""

    name: str
    duration_minutes: int
    priority: str  # e.g. "high", "medium", "low"
    pet: "Pet | None" = None

    def is_high_priority(self) -> bool:
        """Return True if this task is high priority."""
        raise NotImplementedError


@dataclass
class Owner:
    """The pet owner using the app."""

    name: str
    hours_available: float = 0.0
    preferences: str = ""
    pets: list[Pet] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        raise NotImplementedError

    def add_task(self, task: Task) -> None:
        """Add a care task for this owner."""
        raise NotImplementedError


@dataclass
class Scheduler:
    """Turns a list of tasks + available time into a daily plan."""

    tasks: list[Task] = field(default_factory=list)
    time_available: float = 0.0

    def sort_by_priority(self) -> list[Task]:
        """Return the tasks ordered by priority (highest first)."""
        raise NotImplementedError

    def generate_plan(self) -> list[Task]:
        """Build a daily plan that fits within the available time."""
        raise NotImplementedError
