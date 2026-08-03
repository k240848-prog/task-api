from typing import Any

from fastapi import Body, FastAPI, Response, status
from fastapi.responses import JSONResponse

from database import (
    delete_task_from_database,
    fetch_all_tasks,
    fetch_task_by_id,
    initialize_database,
    insert_task,
    update_task_in_database,
)


app = FastAPI(
    title="Task API",
    description="A simple SQLite CRUD API for managing tasks.",
    version="1.0",
)


initialize_database()


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

    return insert_task(title.strip())


@app.put(
    "/tasks/{task_id}",
    summary="Update an existing task",
)
def update_task(
    task_id: int,
    payload: dict[str, Any] = Body(default={}),
):
    existing_task = fetch_task_by_id(task_id)

    if existing_task is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Task not found"},
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

    updated_title = existing_task["title"]
    updated_done = existing_task["done"]

    if "title" in payload:
        title = payload["title"]

        if not isinstance(title, str) or not title.strip():
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "Title must be a non-empty string"
                },
            )

        updated_title = title.strip()

    if "done" in payload:
        done = payload["done"]

        if not isinstance(done, bool):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Done must be true or false"},
            )

        updated_done = done

    updated_task = update_task_in_database(
        task_id=task_id,
        title=updated_title,
        done=updated_done,
    )

    if updated_task is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Task not found"},
        )

    return updated_task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
def delete_task(task_id: int):
    deleted = delete_task_from_database(task_id)

    if not deleted:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Task not found"},
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )