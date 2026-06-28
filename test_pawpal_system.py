from datetime import datetime, timedelta

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


def test_scheduler_tracks_pending_tasks_and_filters_completed():
    owner = Owner(owner_id=1, name="Jordan", email="jordan@example.com")
    pet = Pet(pet_id=1, name="Mochi", species="dog")
    owner.add_pet(pet)

    now = datetime.now().replace(second=0, microsecond=0)
    pending_task = Task(task_id=1, title="Feed lunch", due_time=now, completed=False)
    done_task = Task(task_id=2, title="Brush coat", due_time=now + timedelta(hours=1), completed=True)

    pending_task.assign_to_pet(pet)
    done_task.assign_to_pet(pet)

    scheduler = Scheduler(owner=owner)
    scheduler.schedule_task(pending_task)
    scheduler.schedule_task(done_task)

    pending = scheduler.pending_tasks()
    assert pending == [pending_task]
    assert scheduler.filter_tasks(completed=False) == [pending_task]
    assert scheduler.filter_tasks(completed=True) == [done_task]


def test_scheduler_sorts_tasks_by_earliest_due_time():
    owner = Owner(owner_id=1, name="Jordan", email="jordan@example.com")
    pet = Pet(pet_id=1, name="Mochi", species="dog")
    owner.add_pet(pet)

    now = datetime.now().replace(second=0, microsecond=0)
    late_task = Task(task_id=1, title="Evening walk", due_time=now.replace(hour=18, minute=0))
    early_task = Task(task_id=2, title="Morning walk", due_time=now.replace(hour=8, minute=0))
    midday_task = Task(task_id=3, title="Feed lunch", due_time=now.replace(hour=12, minute=0))

    late_task.assign_to_pet(pet)
    early_task.assign_to_pet(pet)
    midday_task.assign_to_pet(pet)

    scheduler = Scheduler(owner=owner)
    scheduler.schedule_task(late_task)
    scheduler.schedule_task(early_task)
    scheduler.schedule_task(midday_task)

    sorted_titles = [task.title for task in scheduler.sort_by_time()]
    assert sorted_titles == ["Morning walk", "Feed lunch", "Evening walk"]


def test_scheduler_filters_tasks_by_pet_name():
    owner = Owner(owner_id=1, name="Jordan", email="jordan@example.com")
    pet_mochi = Pet(pet_id=1, name="Mochi", species="dog")
    pet_luna = Pet(pet_id=2, name="Luna", species="cat")
    owner.add_pet(pet_mochi)
    owner.add_pet(pet_luna)

    now = datetime.now().replace(second=0, microsecond=0)
    task_mochi = Task(task_id=1, title="Morning walk", due_time=now, completed=False)
    task_luna = Task(task_id=2, title="Feed lunch", due_time=now + timedelta(hours=1), completed=False)

    task_mochi.assign_to_pet(pet_mochi)
    task_luna.assign_to_pet(pet_luna)

    scheduler = Scheduler(owner=owner)
    scheduler.schedule_task(task_mochi)
    scheduler.schedule_task(task_luna)

    filtered = scheduler.filter_tasks(completed=False, pet_name="Mochi")
    assert filtered == [task_mochi]


def test_scheduler_creates_next_daily_recurring_task():
    owner = Owner(owner_id=1, name="Jordan", email="jordan@example.com")
    pet = Pet(pet_id=1, name="Mochi", species="dog")
    owner.add_pet(pet)

    now = datetime.now().replace(second=0, microsecond=0)
    recurring_task = Task(
        task_id=1,
        title="Morning walk",
        due_time=now,
        priority="high",
        duration_minutes=20,
        recurrence="daily",
    )
    recurring_task.assign_to_pet(pet)

    scheduler = Scheduler(owner=owner)
    scheduler.schedule_task(recurring_task)

    next_task = scheduler.mark_task_completed(recurring_task)

    assert recurring_task.completed is True
    assert next_task is not None
    assert next_task.title == recurring_task.title
    assert next_task.recurrence == "daily"
    assert next_task.due_time == now + timedelta(days=1)
    assert next_task.completed is False


def test_scheduler_detects_conflicting_task_times():
    owner = Owner(owner_id=1, name="Jordan", email="jordan@example.com")
    pet1 = Pet(pet_id=1, name="Mochi", species="dog")
    pet2 = Pet(pet_id=2, name="Luna", species="cat")
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    now = datetime.now().replace(second=0, microsecond=0)
    task1 = Task(task_id=1, title="Medication", due_time=now, duration_minutes=30)
    task2 = Task(task_id=2, title="Quick check-in", due_time=now, duration_minutes=15)

    task1.assign_to_pet(pet1)
    task2.assign_to_pet(pet2)

    scheduler = Scheduler(owner=owner)
    scheduler.schedule_task(task1)
    scheduler.schedule_task(task2)

    warnings = scheduler.detect_conflicts()
    assert any("Medication" in warning and "Quick check-in" in warning for warning in warnings)
    assert len(warnings) == 1
