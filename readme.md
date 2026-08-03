# Task API with SQLite

A simple CRUD API built with FastAPI and SQLite for creating, reading, updating, and deleting tasks.

The project originally stored tasks in an in-memory Python list. It was later migrated to SQLite so that task data remains available after the server restarts.

## Features

- Create a new task
- View all tasks
- View a task by ID
- Update a task
- Delete a task
- Persistent SQLite storage
- Automatic database and table creation
- Automatic sample-data seeding when the table is empty
- Input validation and appropriate HTTP status codes
- Interactive Swagger API documentation

## Technologies Used

- Python
- FastAPI
- SQLite
- Uvicorn
- DB Browser for SQLite
- Git and GitHub

## Project Structure

```text
task-api/
├── main.py
├── database.py
├── sql_queries.sql
├── database-viewer.png
├── requirements.txt
├── README.md
├── .gitignore
└── tasks.db
```

The `tasks.db` file is generated automatically and is excluded from Git.

## Database Structure

The application uses a SQLite database named:

```text
tasks.db
```

It contains a `tasks` table with the following columns:

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key with automatic increment |
| title | TEXT | Required task title |
| done | INTEGER | Completion status: `0` for false and `1` for true |

The table is created automatically when the application starts.

If the table is empty, the application inserts three sample tasks.

## Installation

Clone the repository:

```bash
git clone https://github.com/k240848-prog/task-api.git
```

Move into the project folder:

```bash
cd task-api
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows Command Prompt:

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI development server:

```bash
python -m uvicorn main:app --reload
```

Open the Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Open the API directly:

```text
http://127.0.0.1:8000
```

## API Endpoints

| Method | Endpoint | Description | Success Status |
|---|---|---|---|
| GET | `/` | Display API information | 200 |
| GET | `/health` | Check API health | 200 |
| GET | `/tasks` | Get all tasks | 200 |
| GET | `/tasks/{task_id}` | Get one task | 200 |
| POST | `/tasks` | Create a task | 201 |
| PUT | `/tasks/{task_id}` | Update a task | 200 |
| DELETE | `/tasks/{task_id}` | Delete a task | 204 |

Unknown task IDs return:

```text
404 Not Found
```

Invalid request data returns:

```text
400 Bad Request
```

## Example Requests

### Create a Task

```json
{
  "title": "Learn SQLite"
}
```

Example response:

```json
{
  "id": 4,
  "title": "Learn SQLite",
  "done": false
}
```

### Update a Task

```json
{
  "title": "Complete SQLite assignment",
  "done": true
}
```

### Delete a Task

```text
DELETE /tasks/4
```

A successful deletion returns:

```text
204 No Content
```

## SQL Queries

The `sql_queries.sql` file contains queries used to explore the database.

```sql
SELECT * FROM tasks;

SELECT * FROM tasks WHERE done = 1;

SELECT COUNT(*) AS total_tasks FROM tasks;

UPDATE tasks SET done = 1;

DELETE FROM tasks WHERE done = 1;
```

## Database Viewer

The SQLite database was opened and explored using DB Browser for SQLite.

![SQLite database displayed in DB Browser](database-viewer.png)

## Persistence

Tasks are stored inside the SQLite database instead of an in-memory Python list.

This means that created and updated tasks remain available after the FastAPI server is stopped and restarted.

## Development Stages

The project was completed through separate Git commits:

1. Stage 0 — Created the SQLite database
2. Stage 1 — Added database read endpoints
3. Stage 2 — Added database task insertion
4. Stage 3 — Added SQL update and delete operations
5. Stage 4 — Explored SQLite using SQL queries
6. Stage 5 — Added database documentation

## Author
Ali Safdar
