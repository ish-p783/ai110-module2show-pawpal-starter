"""Tests for the PawPal+ logic layer."""

from pawpal_system import Pet, Task


def test_mark_complete_changes_status():
    """Calling mark_complete() should flip completed from False to True."""
    task = Task("Morning walk", duration_minutes=30, priority="high")

    assert task.completed is False  # starts incomplete
    task.mark_complete()
    assert task.completed is True   # now complete


def test_adding_task_increases_pet_task_count():
    """Adding a task to a Pet should increase that pet's task count by one."""
    pet = Pet(name="Rex", breed="Labrador")

    assert len(pet.tasks) == 0  # no tasks yet
    pet.add_task(Task("Feed dinner", duration_minutes=10, priority="medium"))
    assert len(pet.tasks) == 1  # one task after adding
