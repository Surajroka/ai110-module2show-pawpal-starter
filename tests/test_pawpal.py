from pawpal_system import Owner, Pet, Task


def test_mark_completed_changes_task_status():
    task = Task(task_id=1, title="Morning walk", priority="high")

    assert task.completed is False

    task.mark_completed()

    assert task.completed is True


def test_adding_task_to_pet_increases_pet_task_count():
    owner = Owner(owner_id=1, name="Jordan", email="jordan@example.com")
    pet = Pet(pet_id=1, name="Mochi", species="dog")
    owner.add_pet(pet)

    initial_count = len(pet.tasks)

    task = Task(task_id=2, title="Feed dinner", priority="medium")
    task.assign_to_pet(pet)

    assert len(pet.tasks) == initial_count + 1
    assert task in pet.tasks
