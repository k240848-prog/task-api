from abc import ABC, abstractmethod
from typing import Any

Task = dict[str, Any]


class TaskRepository(ABC):
    @abstractmethod
    def check_health(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, task_id: int) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    def create(self, title: str) -> Task:
        raise NotImplementedError

    @abstractmethod
    def update(self, task_id: int, title: str, done: bool) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        raise NotImplementedError
