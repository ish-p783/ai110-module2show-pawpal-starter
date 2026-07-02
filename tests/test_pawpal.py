"""Tests for the PawPal+ logic layer."""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


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


def test_double_complete_does_not_spawn_duplicate():
    """Completing an already-done recurring task should be a no-op.

    The second mark_complete() must return None and not add a second copy,
    so a stray double-click can't flood the pet with duplicate tasks.
    """
    pet = Pet(name="Rex", breed="Labrador")
    pet.add_task(Task("Walk", frequency="daily"))

    pet.tasks[0].mark_complete()   # spawns one next-day copy -> 2 tasks
    result = pet.tasks[0].mark_complete()  # already done -> no-op

    assert result is None
    assert len(pet.tasks) == 2  # still original + the single spawned copy


def test_recurring_task_with_no_pet_does_not_crash():
    """A recurring task not attached to any pet still returns its next copy.

    Because self.pet is None, mark_complete() must skip the add_task() call
    (line 89 guard) instead of raising AttributeError.
    """
    task = Task("Walk", frequency="daily")  # never added to a Pet

    upcoming = task.mark_complete()

    assert task.completed is True
    assert upcoming is not None          # next occurrence still built
    assert upcoming.completed is False


def test_sort_by_time_handles_non_zero_padded_times():
    """'9:30' must sort before '10:00' (numeric parse, not string compare)."""
    owner = Owner(name="Sam")
    pet = Pet(name="Rex")
    owner.add_pet(pet)
    pet.add_task(Task("Late", start_time="10:00"))
    pet.add_task(Task("Early", start_time="9:30"))
    scheduler = Scheduler(owner=owner)

    ordered = scheduler.sort_by_time(owner.get_all_tasks())

    assert [t.description for t in ordered] == ["Early", "Late"]


def test_detect_conflicts_flags_same_time_tasks():
    """Two tasks at the same start time produce exactly one warning."""
    owner = Owner(name="Sam")
    pet = Pet(name="Rex")
    owner.add_pet(pet)
    pet.add_task(Task("Walk", start_time="08:00"))
    pet.add_task(Task("Feed", start_time="08:00"))
    scheduler = Scheduler(owner=owner)

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "08:00" in warnings[0]
    assert "Walk" in warnings[0] and "Feed" in warnings[0]


def test_empty_owner_generates_empty_plan():
    """An owner with no pets/tasks yields an empty plan and a clear message."""
    owner = Owner(name="Sam", minutes_available=60)
    scheduler = Scheduler(owner=owner)

    assert scheduler.generate_plan() == []
    assert scheduler.explain_plan() == "No tasks fit in the available time."
