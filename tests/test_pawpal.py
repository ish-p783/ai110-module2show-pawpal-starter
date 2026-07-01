"""Tests for the PawPal+ logic layer."""

from datetime import date, timedelta

from pawpal_system import Pet, Task


def test_mark_complete_changes_status():
    """Calling mark_complete() should flip completed from False to True."""
    task = Task("Morning walk", duration_minutes=30, priority="high")

    assert task.completed is False  # starts incomplete
    task.mark_complete()
    assert task.completed is True   # now complete


def test_completing_daily_task_spawns_next_day():
    """Finishing a daily task should add a fresh copy due one day later."""
    pet = Pet(name="Rex", breed="Labrador")
    today = date(2026, 7, 1)
    pet.add_task(Task("Walk", frequency="daily", due_date=today))

    pet.tasks[0].mark_complete()

    assert len(pet.tasks) == 2                      # original + next occurrence
    original, upcoming = pet.tasks
    assert original.completed is True               # the one we finished
    assert upcoming.completed is False              # the new one is fresh
    assert upcoming.due_date == today + timedelta(days=1)


def test_completing_weekly_task_spawns_next_week():
    """A weekly task should schedule its next occurrence 7 days out."""
    pet = Pet(name="Mia", breed="Cat")
    today = date(2026, 7, 1)
    pet.add_task(Task("Nail trim", frequency="weekly", due_date=today))

    pet.tasks[0].mark_complete()

    assert pet.tasks[1].due_date == today + timedelta(weeks=1)


def test_once_task_does_not_recur():
    """A one-off task should not create any follow-up when completed."""
    pet = Pet(name="Rex", breed="Labrador")
    pet.add_task(Task("Vet visit", frequency="once"))

    result = pet.tasks[0].mark_complete()

    assert result is None            # nothing spawned
    assert len(pet.tasks) == 1       # still just the original


def test_adding_task_increases_pet_task_count():
    """Adding a task to a Pet should increase that pet's task count by one."""
    pet = Pet(name="Rex", breed="Labrador")

    assert len(pet.tasks) == 0  # no tasks yet
    pet.add_task(Task("Feed dinner", duration_minutes=10, priority="medium"))
    assert len(pet.tasks) == 1  # one task after adding
