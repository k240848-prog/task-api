import os

from app.repositories.postgres import PostgresTaskRepository
from app.service import TaskService

DATABASE_URL = os.getenv("DATABASE_URL", "")

# Storage is selected here. Routes and TaskService do not know about SQL.
repository = PostgresTaskRepository(DATABASE_URL)
task_service = TaskService(repository)
