from pawpal_system import Owner, Pet, Task, Scheduler


def build_demo() -> Scheduler:
    owner = Owner(owner_id=1, name="Jordan", email="jordan@example.com")

    mochi = Pet(pet_id=1, name="Mochi", species="dog", breed="Shiba Inu", age=3)
    luna = Pet(pet_id=2, name="Luna", species="cat", breed="Siamese", age=2)

    owner.add_pet(mochi)
    owner.add_pet(luna)

    tasks = [
        Task(task_id=1, title="Morning walk", description="Walk Mochi around the block", priority="high", duration_minutes=20),
        Task(task_id=2, title="Feed lunch", description="Feed Luna her wet food", priority="medium", duration_minutes=10),
        Task(task_id=3, title="Medication", description="Give Mochi his medicine", priority="high", duration_minutes=5),
        Task(task_id=4, title="Play time", description="Play with Luna for a short session", priority="low", duration_minutes=15),
    ]

    tasks[0].assign_to_pet(mochi)
    tasks[1].assign_to_pet(luna)
    tasks[2].assign_to_pet(mochi)
    tasks[3].assign_to_pet(luna)

    scheduler = Scheduler(owner=owner)
    for task in tasks:
        scheduler.schedule_task(task)

    return scheduler


def main() -> None:
    scheduler = build_demo()
    print("Today’s schedule")
    print("================")
    for task in scheduler.display_schedule():
        pet_name = task.pet.name if task.pet else "Unknown"
        print(f"- {task.title} | Pet: {pet_name} | Priority: {task.priority} | Duration: {task.duration_minutes} min")


if __name__ == "__main__":
    main()
