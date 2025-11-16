# Vexa REST API

Backend service built with **Python 3.12**, **FastAPI**, and **Tortoise ORM**. The application exposes endpoints, persists data in PostgreSQL, and ships with Docker assets for local development.

## Requirements

- [Python 3.12.12+](https://www.python.org/)
- [uv](https://github.com/astral-sh/uv) (recommended) or pip 24+
- [Docker](https://www.docker.com/) and Docker Compose (optional, for containers)
- `openssl` (used to generate secure local secrets)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/vemiliog/vexa-api.git
   cd vexa-api
   ```

2. **Install dependencies**

   Using **uv** (preferred):

   ```bash
   uv sync
   ```

   Or with `pip` inside a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Create the `.env` file**

   Define the database connection string used by Tortoise ORM and the credentials consumed by Docker Compose:

   ```bash
   cat <<'EOF' > .env
   DATABASE_URL=postgres://postgres:postgres@localhost:5432/vexa
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_NAME=vexa
   EOF
   ```

4. **Generate strong secrets**

   Update `DB_PASSWORD` (and any other sensitive value) with random data:

   ```bash
   openssl rand -base64 32
   ```

   Replace the placeholder values in `.env` with the generated secrets.

5. **Synchronize Docker credentials**

   Make sure the credentials you defined in `.env` match the `services.db.environment` block inside `compose.yaml`:

   ```yaml
   services:
     db:
       environment:
         POSTGRES_USER: ${DB_USER}
         POSTGRES_DB: ${DB_NAME}
         POSTGRES_PASSWORD: ${DB_PASSWORD}
   ```

   This ensures the API and the PostgreSQL container stay in sync.

6. **Start the local database (optional)**

   ```bash
   docker compose up -d db
   ```

   A local `postgresql/` directory is mounted as the container volume so your data persists between runs.

## Running the application

### Local development server

```bash
uv fastapi dev app/main.py
```

This command loads environment variables from `.env`, creates the FastAPI app, and Tortoise automatically creates tables defined in `app.models` (`generate_schemas=True` in `app/main.py`).

### Docker Compose

```bash
docker compose up --build
```

The `api` service uses the Dockerfile at the project root and connects to the `db` service defined in `compose.yaml`. Hot reload is handled by FastAPI inside the container when run in development mode.

## Available commands

- `uv run fastapi run app/main.py` – Run the API with auto-reload for development.
- `uv run black .` – Format the source code with Black.
- `uv run isort .` – Sort imports consistently across the project.

## Project structure

```plaintext
app/                         # FastAPI application package
  main.py                    # Application entrypoint, FastAPI + Tortoise setup
  controllers/               # HTTP controllers orchestrating services
  dtos/                      # Models used for request/response bodies
  models/                    # Tortoise ORM models (e.g., User)
  routes/                    # APIRouter instances (auth, health)
  services/                  # Business logic (auth, health)
  utils/                     # Helper utilities such as password hashing
compose.yaml                 # Docker Compose stack for the API and PostgreSQL
Dockerfile                   # Multi-stage build for the FastAPI service
postgresql/                  # Local volume to persist PostgreSQL data
pyproject.toml               # Project metadata and runtime dependencies
requirements.txt             # Locked dependency list exported by uv
uv.lock                      # uv lockfile for reproducible installs
README.md                    # Project documentation (this file)
```

---

FastAPI automatically generates interactive docs at `http://localhost:8000/docs` once the service is running. Use the `/health` endpoint to verify liveness and `/auth/register` to create users that are persisted via Tortoise ORM.
