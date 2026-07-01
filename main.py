"""Demo script for PawPal+.

Builds an owner with a couple of pets and some tasks, then prints
today's schedule to the terminal. Run it with:  python main.py
"""

# 1. Import the classes from your logic layer.
from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    # 2. Create an owner and at least two pets.
    owner = Owner(name="Ishaan", minutes_available=90)

    rex = Pet(name="Rex", breed="Labrador")
    mia = Pet(name="Mia", breed="Cat")

    owner.add_pet(rex)
    owner.add_pet(mia)

    # 3. Add tasks OUT OF ORDER on purpose, so sorting has real work to do.
    #    Note the deliberately unpadded "9:00" to prove numeric time sorting.
    rex.add_task(Task("Evening walk", duration_minutes=30, priority="high", start_time="18:30"))
    rex.add_task(Task("Morning walk", duration_minutes=30, priority="high", start_time="9:00"))
    mia.add_task(Task("Give medication", duration_minutes=10, priority="high", start_time="08:00", frequency="once"))
    mia.add_task(Task("Play with feather toy", duration_minutes=20, priority="medium", start_time="12:15"))
    rex.add_task(Task("Brush coat", duration_minutes=15, priority="low", start_time="10:45"))
    # Deliberate clash: Mia's dinner is booked for 18:30, same as Rex's walk.
    mia.add_task(Task("Feed dinner", duration_minutes=10, priority="high", start_time="18:30"))

    # Mark one done so the status filter has something to separate out.
    mia.tasks[0].mark_complete()  # "Give medication"

    scheduler = Scheduler(owner=owner)

    # 4a. Sorting by time — added out of order, should print chronologically.
    print("=" * 40)
    print("All tasks, sorted by time")
    print("=" * 40)
    for task in scheduler.sort_by_time(owner.get_all_tasks()):
        pet_name = task.pet.name if task.pet else "unknown"
        print(f"  {task.start_time:>5}  {task.description} ({pet_name})")

    # 4b. Filtering by completion status.
    print("\n" + "=" * 40)
    print("Filter: pending vs. completed")
    print("=" * 40)
    print("  Pending:")
    for task in scheduler.filter_by_status(completed=False):
        print(f"    - {task.description}")
    print("  Completed:")
    for task in scheduler.filter_by_status(completed=True):
        print(f"    - {task.description}")

    # 4c. Filtering by pet name.
    print("\n" + "=" * 40)
    print("Filter: Rex's tasks only")
    print("=" * 40)
    for task in scheduler.filter_by_pet("Rex"):
        print(f"  - {task.description} [{task.start_time}]")

    # 4d. Conflict detection: warn about tasks booked at the same time.
    print("\n" + "=" * 40)
    print("Conflict detection")
    print("=" * 40)
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("  No scheduling conflicts found.")

    # 4e. Recurring tasks: completing a daily task auto-schedules tomorrow's.
    #     (label bumped from 4d after conflict detection was inserted above)
    print("\n" + "=" * 40)
    print("Recurring task rollover")
    print("=" * 40)
    morning_walk = next(t for t in rex.tasks if t.description == "Morning walk")
    print(f"  Before: Rex has {len(rex.tasks)} tasks. "
          f"'{morning_walk.description}' due {morning_walk.due_date}.")
    upcoming = morning_walk.mark_complete()  # daily -> spawns next occurrence
    print(f"  Completed '{morning_walk.description}'.")
    print(f"  After:  Rex has {len(rex.tasks)} tasks. "
          f"Next occurrence due {upcoming.due_date} (completed={upcoming.completed}).")

    # 4f. The daily plan / schedule.
    print("\n" + "=" * 40)
    print("Today's Schedule")
    print("=" * 40)
    print(scheduler.explain_plan())


if __name__ == "__main__":
    main()
