from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
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
