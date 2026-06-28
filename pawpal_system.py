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

    def mark_completed(self) -> None:
        self.completed = True


@dataclass
class Pet:
    """Represents a pet owned by the user."""

    pet_id: int
    name: str
    species: str
    breed: str = ""
    age: int = 0
    health_notes: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)


@dataclass
class Owner:
    """Represents the pet owner using the app."""

    owner_id: int
    name: str
    email: str
    pets: List[Pet] = field(default_factory=list)

    def create_account(self) -> None:
        pass

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)


@dataclass
class Scheduler:
    """Stores and organizes tasks for scheduling."""

    task_list: List[Task] = field(default_factory=list)

    def schedule_task(self, task: Task) -> None:
        self.task_list.append(task)

    def sort_by_priority(self) -> List[Task]:
        priority_order = {"low": 0, "medium": 1, "high": 2}
        return sorted(self.task_list, key=lambda task: priority_order.get(task.priority, 1), reverse=True)

    def display_schedule(self) -> List[Task]:
        return self.sort_by_priority()


if __name__ == "__main__":
    owner = Owner(owner_id=1, name="Jordan", email="jordan@example.com")
    pet = Pet(pet_id=1, name="Mochi", species="dog", breed="Shiba Inu", age=3)
    owner.add_pet(pet)

    task = Task(task_id=1, title="Morning walk", description="Walk for 20 minutes", priority="high")
    pet.add_task(task)
    scheduler = Scheduler()
    scheduler.schedule_task(task)

    print(f"Owner: {owner.name}")
    print(f"Pet: {pet.name}")
    print(f"Scheduled tasks: {[t.title for t in scheduler.display_schedule()]}")
