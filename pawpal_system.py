"""PawPal+ logic layer.

This module holds all the backend classes for PawPal+:
Task, Pet, Owner, and Scheduler. The Streamlit UI (app.py)
will import and use these classes.

Data ownership (how the pieces relate):
    Owner  has many  Pet
    Pet    has many  Task
    Scheduler reads tasks THROUGH the Owner (owner.get_all_tasks()),
    so it never reaches into a Pet directly.
"""

from dataclasses import dataclass, field

# Ranking so priorities sort correctly (higher number = more important).
# Use this instead of sorting priority strings, which would sort alphabetically.
PRIORITY_ORDER = {"high": 3, "medium": 2, "low": 1}


@dataclass
class Task:
    """A single care activity (a walk, a feeding, a dose of meds...)."""

    description: str
    duration_minutes: int = 0
    priority: str = "medium"  # "high", "medium", or "low"
    frequency: str = "daily"  # e.g. "daily", "weekly", "once"
    completed: bool = False
    pet: "Pet | None" = None  # back-reference, set when added to a Pet

    def is_high_priority(self) -> bool:
        """Return True if this task is high priority."""
        return self.priority == "high"

    def priority_rank(self) -> int:
        """Numeric rank for sorting (unknown priorities rank lowest)."""
        return PRIORITY_ORDER.get(self.priority, 0)

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark this task as not done."""
        self.completed = False


@dataclass
class Pet:
    """Stores a pet's details and the tasks that belong to it."""

    name: str
    breed: str = ""
    gender: str = ""
    weight: float = 0.0
    height: float = 0.0
    age: int = 0
    health_conditions: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        task.pet = self  # so the task knows which pet it belongs to
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet (safe if it's not present)."""
        if task in self.tasks:
            self.tasks.remove(task)
            task.pet = None

    def pending_tasks(self) -> list[Task]:
        """Return this pet's tasks that aren't completed yet."""
        return [t for t in self.tasks if not t.completed]


@dataclass
class Owner:
    """Manages multiple pets and gives access to all their tasks."""

    name: str
    minutes_available: int = 0  # daily care time, same unit as Task.duration_minutes
    preferences: str = ""
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet (safe if it's not present)."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_all_tasks(self) -> list[Task]:
        """Flatten every task across all of this owner's pets."""
        all_tasks: list[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_pending_tasks(self) -> list[Task]:
        """All not-yet-completed tasks across every pet."""
        return [t for t in self.get_all_tasks() if not t.completed]


@dataclass
class Scheduler:
    """The 'brain': retrieves, organizes, and plans tasks across pets."""

    owner: Owner

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered highest priority first."""
        return sorted(tasks, key=lambda t: t.priority_rank(), reverse=True)

    def generate_plan(self) -> list[Task]:
        """Build a daily plan of pending tasks that fits the available time.

        Greedy strategy: take the highest-priority pending tasks first and
        keep adding them until the owner's available minutes run out.
        """
        pending = self.owner.get_pending_tasks()
        ordered = self.sort_by_priority(pending)

        plan: list[Task] = []
        minutes_used = 0
        for task in ordered:
            if minutes_used + task.duration_minutes <= self.owner.minutes_available:
                plan.append(task)
                minutes_used += task.duration_minutes
        return plan

    def explain_plan(self) -> str:
        """Human-readable summary of the generated plan and why."""
        plan = self.generate_plan()
        if not plan:
            return "No tasks fit in the available time."

        total = sum(t.duration_minutes for t in plan)
        lines = [
            f"Planned {len(plan)} task(s) using {total} of "
            f"{self.owner.minutes_available} available minutes:"
        ]
        for task in plan:
            pet_name = task.pet.name if task.pet else "unknown pet"
            lines.append(
                f"  - {task.description} ({pet_name}) "
                f"[{task.priority}, {task.duration_minutes} min]"
            )
        return "\n".join(lines)
