import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# Create the Owner ONCE and keep it in the session "vault" so it survives reruns.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")
owner = st.session_state.owner

st.subheader("Owner")
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
st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    new_pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    new_pet_species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    if new_pet_name.strip():
        # This is the method from pawpal_system.py that handles the new pet.
        owner.add_pet(Pet(name=new_pet_name.strip(), breed=new_pet_species))
        st.success(f"Added {new_pet_name} to your pets.")
    else:
        st.error("Please enter a pet name first.")

if owner.pets:
    st.write("Your pets: " + ", ".join(pet.name for pet in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a Task (assigned to one of the owner's pets) ---
st.subheader("Add a Task")
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

    if st.button("Add task"):
        # Find the chosen pet, then use its add_task method from pawpal_system.py.
        pet = next(p for p in owner.pets if p.name == selected_pet_name)
        pet.add_task(
            Task(description=task_title, duration_minutes=int(duration), priority=priority)
        )
        st.success(f"Added '{task_title}' to {selected_pet_name}.")

# Show every task across all pets (read from the owner, which aggregates them).
all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "pet": task.pet.name if task.pet else "",
                "task": task.description,
                "minutes": task.duration_minutes,
                "priority": task.priority,
                "done": task.completed,
            }
            for task in all_tasks
        ]
    )

st.divider()

# --- Build Schedule ---
st.subheader("Build Schedule")
st.caption("Uses your Scheduler to fit the highest-priority tasks into the available time.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner=owner)
    plan = scheduler.generate_plan()
    if plan:
        st.success(f"Planned {len(plan)} task(s).")
        st.text(scheduler.explain_plan())
    else:
        st.warning(
            "No tasks fit in the available time. Add tasks or increase the available minutes."
        )
