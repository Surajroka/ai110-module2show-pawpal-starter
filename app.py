import streamlit as st
from datetime import datetime

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_id=1, name="Jordan", email="jordan@example.com")
    default_pet = Pet(pet_id=1, name="Mochi", species="dog")
    st.session_state.owner.add_pet(default_pet)

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)

owner = st.session_state.owner
scheduler = st.session_state.scheduler

st.title(f"🐾 PawPal+ — {owner.name}")

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

st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value=owner.name, key="owner_name_input")
if owner_name != owner.name:
    owner.name = owner_name
    st.session_state.owner = owner

st.markdown("### Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", key="pet_name_input")
    species = st.selectbox("Species", ["dog", "cat", "other"], key="pet_species_input")
    add_pet_submitted = st.form_submit_button("Add pet")

    if add_pet_submitted:
        if pet_name.strip():
            new_pet = Pet(pet_id=len(owner.pets) + 1, name=pet_name.strip(), species=species)
            owner.add_pet(new_pet)
            st.session_state.owner = owner
            st.success(f"Added {new_pet.name} to {owner.name}.")
        else:
            st.warning("Please enter a pet name.")

st.write("Pets currently on record:")
if owner.pets:
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.species})")
else:
    st.info("No pets yet.")

st.markdown("### Schedule a Task")
with st.form("add_task_form", clear_on_submit=True):
    selected_pet_name = st.selectbox(
        "Assign to pet",
        [pet.name for pet in owner.pets],
        key="task_pet_select",
    )
    task_title = st.text_input("Task title", key="task_title_input")
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="task_duration_input")
    due_date = st.date_input("Due date", value=datetime.now().date(), key="task_due_date_input")
    due_time = st.time_input("Due time", value=datetime.now().time().replace(second=0, microsecond=0), key="task_due_time_input")
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="task_priority_input")
    recurrence = st.selectbox("Recurrence", ["none", "daily", "weekly"], key="task_recurrence_input")
    add_task_submitted = st.form_submit_button("Add task")

    if add_task_submitted:
        if task_title.strip() and owner.pets:
            selected_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)
            due_datetime = datetime.combine(due_date, due_time)
            recurrence_value = recurrence if recurrence != "none" else None
            task = Task(
                task_id=len(scheduler.task_list) + 1,
                title=task_title.strip(),
                priority=priority,
                duration_minutes=int(duration),
                due_time=due_datetime,
                recurrence=recurrence_value,
            )
            task.assign_to_pet(selected_pet)
            scheduler.schedule_task(task)
            st.session_state.scheduler = scheduler
            st.success(f"Added '{task.title}' for {selected_pet.name}.")
        else:
            st.warning("Please enter a task title and make sure at least one pet exists.")

st.write("Current tasks:")
if scheduler.display_schedule():
    for task in scheduler.display_schedule():
        pet_name = task.pet.name if task.pet else "Unknown"
        recurrence_text = f" | Recurrence: {task.recurrence}" if task.recurrence else ""
        due_text = task.due_time.strftime("%Y-%m-%d %H:%M") if task.due_time else "No due date"
        st.write(f"- {task.title} | Pet: {pet_name} | Due: {due_text} | Priority: {task.priority}{recurrence_text}")
else:
    st.info("No tasks yet. Add one above.")

st.markdown("### Complete a pending task")
pending_tasks = scheduler.filter_tasks(completed=False)
if pending_tasks:
    for task in pending_tasks:
        pet_name = task.pet.name if task.pet else "Unknown"
        due_text = task.due_time.strftime("%Y-%m-%d %H:%M") if task.due_time else "No due date"
        button_key = f"complete_task_{task.task_id}"
        if st.button(f"Complete {task.title} ({pet_name})", key=button_key):
            new_task = scheduler.mark_task_completed_by_id(task.task_id)
            st.session_state.scheduler = scheduler
            if new_task:
                new_due = new_task.due_time.strftime("%Y-%m-%d %H:%M") if new_task.due_time else "No due date"
                st.success(f"Completed '{task.title}' and created next occurrence for {new_due}.")
            else:
                st.success(f"Completed '{task.title}'.")
else:
    st.info("No pending tasks to complete.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.success(f"Using owner: {owner.name}")
    st.write("Pets currently on record:")
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.species})")

    st.write("Scheduled tasks:")
    for task in scheduler.display_schedule():
        pet_name = task.pet.name if task.pet else "Unknown"
        st.write(f"- {task.title} | Pet: {pet_name} | Priority: {task.priority}")
