from app.repositories.base import Task, TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    def check_health(self) -> None:
        self._repository.check_health()

    def get_all_tasks(self) -> list[Task]:
        return self._repository.get_all()

    def get_task(self, task_id: int) -> Task | None:
        return self._repository.get_by_id(task_id)

    def create_task(self, title: str) -> Task:
        return self._repository.create(title)

    def update_task(self, task_id: int, title: str, done: bool) -> Task | None:
        return self._repository.update(task_id, title, done)

    def delete_task(self, task_id: int) -> bool:
        return self._repository.delete(task_id)
