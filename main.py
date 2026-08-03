from typing import Any
from database import (
    fetch_all_tasks,
    fetch_task_by_id,
    initialize_database,
)
from fastapi import Body, FastAPI, Response, status
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Task API",
    description="A simple in-memory CRUD API for managing tasks.",
    version="1.0",
)
initialize_database()


# Temporary in-memory storage.
# Data will reset whenever the server restarts.
tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False,
    },
    {
        "id": 2,
        "title": "Build a CRUD API",
        "done": False,
    },
    {
        "id": 3,
        "title": "Upload project to GitHub",
        "done": True,
    },
]


@app.get(
    "/",
    summary="View API information",
)
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"],
    }


@app.get(
    "/health",
    summary="Check API health",
)
def health():
    return {"status": "ok"}


@app.get(
    "/tasks",
    summary="Get all tasks",
)
def get_all_tasks():
    return fetch_all_tasks()

@app.get(
    "/tasks/{task_id}",
    summary="Get a task by ID",
)
def get_task(task_id: int):
    task = fetch_task_by_id(task_id)

    if task is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Task not found"},
        )

    return task

@app.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
)
def create_task(payload: dict[str, Any] = Body(default={})):
    title = payload.get("title")

    if not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Title is required and must not be empty"
            },
        )

    next_id = max(
        (task["id"] for task in tasks),
        default=0,
    ) + 1

    new_task = {
        "id": next_id,
        "title": title.strip(),
        "done": False,
    }

    tasks.append(new_task)

    return new_task


@app.put(
    "/tasks/{task_id}",
    summary="Update an existing task",
)
def update_task(
    task_id: int,
    payload: dict[str, Any] = Body(default={}),
):
    task_to_update = None

    for task in tasks:
        if task["id"] == task_id:
            task_to_update = task
            break

    if task_to_update is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Task {task_id} not found"},
        )

    if not payload:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Request body cannot be empty"},
        )

    if "title" not in payload and "done" not in payload:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Provide title or done to update the task"
            },
        )

    if "title" in payload:
        title = payload["title"]

        if not isinstance(title, str) or not title.strip():
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "Title must be a non-empty string"
                },
            )

        task_to_update["title"] = title.strip()

    if "done" in payload:
        done = payload["done"]

        if not isinstance(done, bool):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Done must be true or false"},
            )

        task_to_update["done"] = done

    return task_to_update


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)

            return Response(
                status_code=status.HTTP_204_NO_CONTENT
            )

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": f"Task {task_id} not found"},
    )