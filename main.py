"""Demo script for PawPal+.

Builds an owner with a couple of pets and some tasks, then prints
today's schedule to the terminal. Run it with:  python main.py
"""

# 1. Import the classes from your logic layer.
from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    # 2. Create an owner and at least two pets.
    owner = Owner(name="Ishy", minutes_available=90)

    rex = Pet(name="Rex", breed="Labrador")
    mia = Pet(name="Mia", breed="Cat")

    owner.add_pet(rex)
    owner.add_pet(mia)

    # 3. Add at least three tasks (with different durations) to the pets.
    rex.add_task(Task("Morning walk", duration_minutes=30, priority="high"))
    rex.add_task(Task("Brush coat", duration_minutes=15, priority="low"))
    mia.add_task(Task("Give medication", duration_minutes=10, priority="high"))
    mia.add_task(Task("Play with feather toy", duration_minutes=20, priority="medium"))

    # 4. Build and print "Today's Schedule".
    scheduler = Scheduler(owner=owner)

    print("=" * 40)
    print("Today's Schedule")
    print("=" * 40)
    print(scheduler.explain_plan())


if __name__ == "__main__":
    main()
