from pawpal_system import Owner, Pet, Task, Scheduler


def test_scheduler_collects_tasks_from_owner_pets():
    owner = Owner(owner_id=1, name="Jordan", email="jordan@example.com")
    pet = Pet(pet_id=1, name="Mochi", species="dog")
    owner.add_pet(pet)

    walk_task = Task(task_id=1, title="Morning walk", priority="high", duration_minutes=20)
    feed_task = Task(task_id=2, title="Feed dinner", priority="medium", duration_minutes=10)

    walk_task.assign_to_pet(pet)
    feed_task.assign_to_pet(pet)

    scheduler = Scheduler(owner=owner)
    scheduled_tasks = scheduler.get_tasks_for_owner()

    assert len(scheduled_tasks) == 2
    assert [task.title for task in scheduled_tasks] == ["Morning walk", "Feed dinner"]
