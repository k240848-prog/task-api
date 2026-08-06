from typing import Any

from fastapi import Body, FastAPI, Response, status
from fastapi.responses import JSONResponse

from app.container import task_service

app = FastAPI(
    title="Task API",
    description="A PostgreSQL-backed CRUD API for managing tasks.",
    version="2.0",
)


@app.get("/", summary="View API information")
def root():
    return {
        "name": "Task API",
        "version": "2.0",
        "storage": "PostgreSQL",
        "endpoints": ["/tasks"],
    }


@app.get("/health", summary="Check API health")
def health():
    try:
        task_service.check_health()
        return {"status": "ok", "database": "connected"}
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "error", "database": "unavailable"},
        )


@app.get("/tasks", summary="Get all tasks")
def get_all_tasks():
    return task_service.get_all_tasks()


@app.get("/tasks/{task_id}", summary="Get a task by ID")
def get_task(task_id: int):
    task = task_service.get_task(task_id)

    if task is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Task {task_id} not found"},
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
            content={"error": "Title is required and must not be empty"},
        )

    return task_service.create_task(title.strip())


@app.put("/tasks/{task_id}", summary="Update an existing task")
def update_task(
    task_id: int,
    payload: dict[str, Any] = Body(default={}),
):
    existing_task = task_service.get_task(task_id)

    if existing_task is None:
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
            content={"error": "Provide title or done to update the task"},
        )

    updated_title = existing_task["title"]
    updated_done = existing_task["done"]

    if "title" in payload:
        title = payload["title"]
        if not isinstance(title, str) or not title.strip():
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Title must be a non-empty string"},
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

    updated_task = task_service.update_task(
        task_id=task_id,
        title=updated_title,
        done=updated_done,
    )

    if updated_task is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Task {task_id} not found"},
        )

    return updated_task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
def delete_task(task_id: int):
    deleted = task_service.delete_task(task_id)

    if not deleted:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Task {task_id} not found"},
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
