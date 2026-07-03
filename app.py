import streamlit as st
from datetime import time

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A pet care planning assistant — track tasks, spot conflicts, and build a smart daily schedule.")

with st.expander("What PawPal+ does", expanded=False):
    st.markdown(
        """
- Track care tasks (walks, feeding, meds, grooming) per pet
- Sort tasks by **priority** or by **time of day**
- Filter by pet or completion status
- **Flag scheduling conflicts** when two tasks share the same time
- Build a daily plan that fits the highest-priority tasks into your available minutes
"""
    )

st.divider()

# Create the Owner ONCE and keep it in the session "vault" so it survives reruns.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")
owner = st.session_state.owner

# --- Owner ---
st.subheader("👤 Owner")
owner.name = st.text_input("Owner name", value=owner.name)
owner.minutes_available = st.number_input(
    "Time available today (minutes)",
    min_value=0,
    max_value=1440,
    value=owner.minutes_available or 90,
    step=15,
)

st.divider()

# --- Add a Pet ---
st.subheader("🐶 Add a Pet")
col1, col2 = st.columns(2)
with col1:
    new_pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    new_pet_species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    if new_pet_name.strip():
        owner.add_pet(Pet(name=new_pet_name.strip(), breed=new_pet_species))
        st.success(f"Added {new_pet_name} to your pets.")
    else:
        st.error("Please enter a pet name first.")

if owner.pets:
    st.write("Your pets: " + ", ".join(pet.name for pet in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a Task ---
st.subheader("📝 Add a Task")
if not owner.pets:
    st.caption("Add a pet first, then you can assign tasks to it.")
else:
    selected_pet_name = st.selectbox("Which pet?", [pet.name for pet in owner.pets])
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    col4, col5 = st.columns(2)
    with col4:
        start_time = st.time_input("Start time", value=time(8, 0))
    with col5:
        frequency = st.selectbox("Repeats", ["once", "daily", "weekly"], index=1)

    if st.button("Add task"):
        pet = next(p for p in owner.pets if p.name == selected_pet_name)
        pet.add_task(
            Task(
                description=task_title,
                duration_minutes=int(duration),
                priority=priority,
                frequency=frequency,
                start_time=start_time.strftime("%H:%M"),
            )
        )
        st.success(f"Added '{task_title}' to {selected_pet_name} at {start_time.strftime('%H:%M')}.")

st.divider()

# --- Task list: sorting, filtering, conflict detection ---
st.subheader("📋 Your Tasks")
scheduler = Scheduler(owner=owner)
all_tasks = owner.get_all_tasks()

if not all_tasks:
    st.info("No tasks yet. Add one above to get started.")
else:
    # Conflict warnings go at the TOP so the owner sees clashes before anything else.
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        st.warning(
            f"⚠️ {len(conflicts)} scheduling conflict(s) found — "
            "two or more tasks are booked for the same time:"
        )
        for warning in conflicts:
            # Strip the backend's "WARNING: " prefix; Streamlit already styles it.
            st.warning(warning.replace("WARNING: ", ""))
        st.caption("Tip: change one task's start time to resolve the clash.")
    else:
        st.success("✅ No scheduling conflicts — every task is at a distinct time.")

    # Sort + filter controls.
    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.selectbox("Sort by", ["Time of day", "Priority"])
    with col2:
        pet_options = ["All pets"] + [p.name for p in owner.pets]
        pet_filter = st.selectbox("Show", pet_options)

    status_filter = st.radio(
        "Status", ["All", "Pending", "Completed"], horizontal=True
    )

    # Apply filters using the Scheduler's methods.
    if pet_filter == "All pets":
        tasks = all_tasks
    else:
        tasks = scheduler.filter_by_pet(pet_filter)

    if status_filter == "Pending":
        tasks = [t for t in tasks if not t.completed]
    elif status_filter == "Completed":
        tasks = [t for t in tasks if t.completed]

    # Apply sorting using the Scheduler's methods.
    if sort_by == "Priority":
        tasks = scheduler.sort_by_priority(tasks)
    else:
        tasks = scheduler.sort_by_time(tasks)

    if tasks:
        st.table(
            [
                {
                    "Time": task.start_time or "—",
                    "Pet": task.pet.name if task.pet else "",
                    "Task": task.description,
                    "Priority": task.priority,
                    "Min": task.duration_minutes,
                    "Repeats": task.frequency,
                    "Done": "✅" if task.completed else "⏳",
                }
                for task in tasks
            ]
        )
    else:
        st.caption("No tasks match the current filter.")

    # Mark a task complete (demonstrates recurring-task spawning).
    pending = owner.get_pending_tasks()
    if pending:
        st.markdown("**Mark a task complete**")
        labels = {
            f"{t.description} ({t.pet.name if t.pet else '?'}) @ {t.start_time or '—'}": t
            for t in pending
        }
        choice = st.selectbox("Task", list(labels.keys()))
        if st.button("Mark complete"):
            task = labels[choice]
            upcoming = task.mark_complete()
            if upcoming is not None:
                st.success(
                    f"Completed '{task.description}'. A new **{task.frequency}** "
                    f"occurrence was scheduled for {upcoming.due_date}."
                )
            else:
                st.success(f"Completed '{task.description}'.")

st.divider()

# --- Build Schedule ---
st.subheader("📅 Build Today's Schedule")
st.caption("Fits the highest-priority pending tasks into your available time, ordered by time of day.")

if st.button("Generate schedule"):
    plan = scheduler.generate_plan()
    if plan:
        total = sum(t.duration_minutes for t in plan)
        st.success(
            f"Planned {len(plan)} task(s) using {total} of "
            f"{owner.minutes_available} available minutes."
        )
        st.table(
            [
                {
                    "Time": task.start_time or "—",
                    "Task": task.description,
                    "Pet": task.pet.name if task.pet else "",
                    "Priority": task.priority,
                    "Min": task.duration_minutes,
                }
                for task in plan
            ]
        )
    else:
        st.warning(
            "No tasks fit in the available time. Add tasks or increase the available minutes."
        )
