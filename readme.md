# Task API — FastAPI, PostgreSQL and Docker

This project runs a FastAPI CRUD service and PostgreSQL together with Docker Compose. Task data is stored in a named Docker volume, so it survives application and container restarts.

## Architecture

```text
HTTP routes (main.py)
        ↓
TaskService (app/service.py)
        ↓
TaskRepository interface (app/repositories/base.py)
        ↓
PostgresTaskRepository (app/repositories/postgres.py)
```

The in-memory repository is retained in `app/repositories/memory.py` and implements the same interface. Storage selection is isolated to `app/container.py`.

### Honest A2 note

The original A2 submission was a single-file in-memory API and did not already contain separate route, service and repository layers. For this task it was first refactored into those layers. The public API routes, request bodies, response shapes and status codes were preserved. After the refactor, PostgreSQL was introduced through the repository implementation and the storage wiring in `app/container.py`; `TaskService` contains no SQL and the routes do not import `psycopg`.

## Files

```text
app/
  container.py
  service.py
  repositories/
    base.py
    memory.py
    postgres.py
main.py
init.sql
Dockerfile
docker-compose.yml
.env.example
requirements.txt
```

## Start the complete stack

Create the local environment file:

```cmd
copy .env.example .env
```

Build and start the app and database:

```cmd
docker compose up --build
```

Open Swagger UI:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | App and database health |
| GET | `/tasks` | List tasks |
| GET | `/tasks/{task_id}` | Get one task |
| POST | `/tasks` | Create task |
| PUT | `/tasks/{task_id}` | Update task |
| DELETE | `/tasks/{task_id}` | Delete task |

## Database initialization

`init.sql` creates the `tasks` table and inserts three sample tasks only when the table is empty. PostgreSQL runs with the named volume `postgres_data`.

## Persistence proof

1. Start the stack with `docker compose up --build -d`.
2. Create a task in Swagger UI, for example `{"title": "Persistence test"}`.
3. Confirm it appears in `GET /tasks`.
4. Stop and remove the containers without deleting the volume:

```cmd
docker compose down
```

5. Start the stack again:

```cmd
docker compose up -d
```

6. Run `GET /tasks` again. The `Persistence test` row remains because PostgreSQL data is stored in the named volume.

Do not use `docker compose down -v` during the persistence test because `-v` intentionally deletes the named volume.

## Environment variables

`.env` is ignored by Git. `.env.example` is committed as the template.

```env
POSTGRES_DB=taskdb
POSTGRES_USER=taskuser
POSTGRES_PASSWORD=taskpass
DATABASE_URL=postgresql://taskuser:taskpass@db:5432/taskdb
```

## Useful commands

```cmd
docker compose up --build
docker compose ps
docker compose logs -f app
docker compose logs -f db
docker compose down
```
