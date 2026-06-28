from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import datetime, timedelta


def build_demo() -> Scheduler:
    owner = Owner(owner_id=1, name="Jordan", email="jordan@example.com")

    mochi = Pet(pet_id=1, name="Mochi", species="dog", breed="Shiba Inu", age=3)
    luna = Pet(pet_id=2, name="Luna", species="cat", breed="Siamese", age=2)

    owner.add_pet(mochi)
    owner.add_pet(luna)

    now = datetime.now().replace(second=0, microsecond=0)

    # Deliberately create tasks out of chronological order to test sorting
    tasks = [
        Task(task_id=1, title="Feed lunch", description="Feed Luna her wet food", due_time=now.replace(hour=12, minute=0), priority="medium", duration_minutes=10),
        Task(task_id=2, title="Play time", description="Play with Luna for a short session", due_time=now.replace(hour=15, minute=0), priority="low", duration_minutes=15),
        Task(task_id=3, title="Morning walk", description="Walk Mochi around the block", due_time=now.replace(hour=8, minute=0), priority="high", duration_minutes=20, recurrence="daily"),
        Task(task_id=4, title="Medication", description="Give Mochi his medicine", due_time=now.replace(hour=9, minute=30), priority="high", duration_minutes=5),
        Task(task_id=5, title="Quick check-in", description="Check Luna's water bowl", due_time=now.replace(hour=9, minute=30), priority="low", duration_minutes=10),
    ]

    tasks[0].assign_to_pet(mochi)
    tasks[1].assign_to_pet(luna)
    tasks[2].assign_to_pet(mochi)
    tasks[3].assign_to_pet(mochi)
    tasks[4].assign_to_pet(luna)

    scheduler = Scheduler(owner=owner)
    for task in tasks:
        scheduler.schedule_task(task)

    return scheduler


def main() -> None:
    scheduler = build_demo()
    print("Unsorted tasks (as added)")
    print("=========================")
    for task in scheduler.task_list:
        pet_name = task.pet.name if task.pet else "Unknown"
        due = task.due_time.strftime("%Y-%m-%d %H:%M") if task.due_time else "(no time)"
        print(f"- {task.title} | Pet: {pet_name} | Due: {due} | Priority: {task.priority}")

    print("\nSorted by time")
    print("==============")
    for task in scheduler.sort_by_time():
        pet_name = task.pet.name if task.pet else "Unknown"
        due = task.due_time.strftime("%Y-%m-%d %H:%M") if task.due_time else "(no time)"
        print(f"- {task.title} | Pet: {pet_name} | Due: {due} | Priority: {task.priority}")

    print("\nFiltered: pending tasks for Mochi")
    print("===============================")
    for task in scheduler.filter_tasks(completed=False, pet_name="Mochi"):
        due = task.due_time.strftime("%Y-%m-%d %H:%M") if task.due_time else "(no time)"
        print(f"- {task.title} | Due: {due} | Priority: {task.priority}")

    # Demonstrate recurring task automation
    print("\nMarking the daily recurring task complete...")
    recurring = next((t for t in scheduler.task_list if t.recurrence == "daily"), None)
    if recurring:
        new_task = scheduler.mark_task_completed(recurring)
        print(f"Completed: {recurring.title}")
        if new_task:
            due = new_task.due_time.strftime("%Y-%m-%d %H:%M") if new_task.due_time else "(no time)"
            print(f"New recurring task created: {new_task.title} | Due: {due} | ID: {new_task.task_id}")

    warnings = scheduler.detect_conflicts()
    if warnings:
        print("\nConflict warnings")
        print("=================")
        for warning in warnings:
            print(warning)
    else:
        print("\nNo schedule conflicts detected.")


if __name__ == "__main__":
    main()
