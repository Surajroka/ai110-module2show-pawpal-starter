from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional


@dataclass
class Task:
    """Represents a single pet care task."""

    task_id: int
    title: str
    description: str = ""
    due_time: Optional[datetime] = None
    priority: str = "medium"
    completed: bool = False
    duration_minutes: int = 15
    pet: Optional["Pet"] = None
    recurrence: Optional[str] = None  # 'daily' or 'weekly'

    def mark_completed(self) -> None:
        """Mark the task as complete."""
        self.completed = True

    def assign_to_pet(self, pet: "Pet") -> None:
        """Attach this task to a pet."""
        self.pet = pet
        pet.add_task(self)


@dataclass
class Pet:
    """Represents a pet owned by the user."""

    pet_id: int
    name: str
    species: str
    breed: str = ""
    age: int = 0
    health_notes: str = ""
    owner: Optional["Owner"] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        if task not in self.tasks:
            self.tasks.append(task)
        if task.pet is None or task.pet != self:
            task.pet = self


@dataclass
class Owner:
    """Represents the pet owner using the app."""

    owner_id: int
    name: str
    email: str
    pets: List[Pet] = field(default_factory=list)

    def create_account(self) -> None:
        return None

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        if pet not in self.pets:
            self.pets.append(pet)
        if pet.owner is None or pet.owner != self:
            pet.owner = self

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks from this owner’s pets."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks


@dataclass
class Scheduler:
    """Stores and organizes tasks for scheduling."""

    owner: Optional[Owner] = None
    task_list: List[Task] = field(default_factory=list)

    def schedule_task(self, task: Task) -> None:
        """Add a task to the scheduler."""
        if task not in self.task_list:
            self.task_list.append(task)
        if task.pet is not None:
            task.pet.add_task(task)

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sort tasks by `due_time` (earliest first). Tasks without a due_time appear last.

        Example: to sort a list of time strings in "HH:MM" format you could use:
            sorted(times, key=lambda s: datetime.strptime(s, "%H:%M"))
        """
        source = tasks if tasks is not None else self.pending_tasks()

        def key_func(task: Task):
            if task.due_time is None:
                return (1, datetime.max)
            return (0, task.due_time)

        return sorted(source, key=key_func)

    def get_tasks_for_owner(self) -> List[Task]:
        """Return all tasks for the linked owner."""
        if self.owner is None:
            return []
        return self.owner.get_all_tasks()

    def pending_tasks(self) -> List[Task]:
        """Return unfinished tasks for the owner."""
        tasks = self.get_tasks_for_owner() if self.owner is not None else self.task_list
        return [task for task in tasks if not task.completed]

    def sort_by_priority(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sort tasks by priority level."""
        source = tasks if tasks is not None else self.pending_tasks()
        priority_order = {"low": 0, "medium": 1, "high": 2}
        return sorted(source, key=lambda task: priority_order.get(task.priority, 1), reverse=True)

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Filter tasks by completion status and/or pet name.

        - `completed`: True to return only completed tasks, False for pending, None for both.
        - `pet_name`: filter tasks assigned to a pet with this name.
        """
        tasks = self.get_tasks_for_owner() if self.owner is not None else list(self.task_list)
        if completed is not None:
            tasks = [t for t in tasks if t.completed is completed]
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet is not None and t.pet.name == pet_name]
        return tasks

    def detect_conflicts(self, tasks: Optional[List[Task]] = None) -> List[str]:
        """Detect overlapping task schedules and return warning strings.

        This method checks only tasks with explicit due times. It compares the
        time window of each task (due_time + duration_minutes) against later
        tasks and returns a lightweight warning list instead of raising an error.
        """
        tasks = tasks if tasks is not None else self.get_tasks_for_owner()
        timed_tasks = [task for task in tasks if task.due_time is not None]
        warnings: List[str] = []

        def overlaps(first: Task, second: Task) -> bool:
            first_start = first.due_time
            first_end = first.due_time + timedelta(minutes=first.duration_minutes)
            second_start = second.due_time
            second_end = second.due_time + timedelta(minutes=second.duration_minutes)
            return first_start < second_end and second_start < first_end

        sorted_tasks = sorted(timed_tasks, key=lambda task: task.due_time)
        for index, task in enumerate(sorted_tasks):
            for compare in sorted_tasks[index + 1 :]:
                if not overlaps(task, compare):
                    continue
                warnings.append(
                    f"Warning: '{task.title}' (pet: {task.pet.name if task.pet else 'Unknown'}) "
                    f"conflicts with '{compare.title}' (pet: {compare.pet.name if compare.pet else 'Unknown'}) at {task.due_time.strftime('%Y-%m-%d %H:%M')}"
                )
        return warnings

    def mark_task_completed(self, task: Task) -> Optional[Task]:
        """Mark a task completed and, if it is recurring, create the next occurrence.

        Returns the newly created Task if a recurrence was scheduled, otherwise None.
        """
        task.mark_completed()

        if not task.recurrence:
            return None

        if task.recurrence.lower() == "daily":
            delta = timedelta(days=1)
        elif task.recurrence.lower() == "weekly":
            delta = timedelta(weeks=1)
        else:
            return None

        next_due = (task.due_time + delta) if task.due_time is not None else (datetime.now() + delta)

        max_id = max([t.task_id for t in self.task_list], default=0)
        new_task = Task(
            task_id=max_id + 1,
            title=task.title,
            description=task.description,
            due_time=next_due,
            priority=task.priority,
            duration_minutes=task.duration_minutes,
            pet=task.pet,
            recurrence=task.recurrence,
        )

        self.schedule_task(new_task)
        return new_task

    def mark_task_completed_by_id(self, task_id: int) -> Optional[Task]:
        """Mark the task with the given ID complete and return the next recurring occurrence.

        This helper makes it easy for UI code to complete tasks by identifier and
        automatically handle recurrence if the task has `daily` or `weekly` set.
        """
        task = next((t for t in self.task_list if t.task_id == task_id), None)
        if task is None:
            return None
        return self.mark_task_completed(task)

    def display_schedule(self, pet: Optional[Pet] = None) -> List[Task]:
        """Display the scheduled tasks for a pet or all pets."""
        tasks = self.pending_tasks()
        if pet is not None:
            tasks = [task for task in tasks if task.pet == pet]
        return self.sort_by_priority(tasks)


if __name__ == "__main__":
    owner = Owner(owner_id=1, name="Jordan", email="jordan@example.com")
    pet = Pet(pet_id=1, name="Mochi", species="dog", breed="Shiba Inu", age=3)
    owner.add_pet(pet)

    task = Task(task_id=1, title="Morning walk", description="Walk for 20 minutes", priority="high", duration_minutes=20)
    task.assign_to_pet(pet)
    scheduler = Scheduler(owner=owner)
    scheduler.schedule_task(task)

    print(f"Owner: {owner.name}")
    print(f"Pet: {pet.name}")
    print(f"Scheduled tasks: {[t.title for t in scheduler.display_schedule(pet)]}")
