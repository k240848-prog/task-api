from copy import deepcopy

from app.repositories.base import Task, TaskRepository


class InMemoryTaskRepository(TaskRepository):
    def __init__(self) -> None:
        self._tasks: list[Task] = [
            {"id": 1, "title": "Learn FastAPI", "done": False},
            {"id": 2, "title": "Build a CRUD API", "done": False},
            {"id": 3, "title": "Upload project to GitHub", "done": True},
        ]

    def check_health(self) -> None:
        return None

    def get_all(self) -> list[Task]:
        return deepcopy(self._tasks)

    def get_by_id(self, task_id: int) -> Task | None:
        for task in self._tasks:
            if task["id"] == task_id:
                return deepcopy(task)
        return None

    def create(self, title: str) -> Task:
        next_id = max((task["id"] for task in self._tasks), default=0) + 1
        task = {"id": next_id, "title": title, "done": False}
        self._tasks.append(task)
        return deepcopy(task)

    def update(self, task_id: int, title: str, done: bool) -> Task | None:
        for task in self._tasks:
            if task["id"] == task_id:
                task["title"] = title
                task["done"] = done
                return deepcopy(task)
        return None

    def delete(self, task_id: int) -> bool:
        for index, task in enumerate(self._tasks):
            if task["id"] == task_id:
                self._tasks.pop(index)
                return True
        return False
