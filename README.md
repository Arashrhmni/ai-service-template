# AI Service Template

![CI](https://github.com/Arashrhmni/ai-service-template/actions/workflows/ci.yml/badge.svg)

A production-style FastAPI boilerplate built as the foundation for a series of AI engineering projects — RAG systems, agentic workflows, and deployed cloud services. Every later project in this series starts from this template rather than rebuilding boilerplate from scratch.

This isn't a tutorial clone. It's built incrementally, with each piece added and verified independently: dependency-aware health checks, real database migrations, structured logging with request tracing, Redis-backed rate limiting, an isolated automated test suite, and a full CI pipeline gating every push.

## Stack

- **FastAPI** — async Python web framework
- **PostgreSQL 16** (async, via `asyncpg` + SQLAlchemy async engine)
- **SQLModel** — typed ORM models that double as Pydantic schemas
- **Alembic** — versioned database migrations
- **Redis 7** — caching / rate-limiting layer
- **structlog** — structured JSON logging with request-scoped context
- **pytest + pytest-asyncio** — async test suite with isolated, rolled-back DB transactions
- **ruff + mypy** — linting, formatting, and static type checking
- **GitHub Actions** — CI pipeline (lint, format check, type check, migrate, test)
- **Docker Compose** — full local stack (API + Postgres + Redis) with health-checked service dependencies
- **uv** — fast Python dependency management

## Architecture

```
Client
  |
  v
FastAPI app
  |
  +-- middleware   (request ID, structured logging, rate limiting)
  +-- routes/      (health, items)       - HTTP layer, request/response
  +-- services/    (business logic)      - orchestrates DB + Redis calls
  +-- schemas/     (Pydantic models)     - request/response validation
  +-- models/      (SQLModel + Postgres) - persisted data
        |
        +--> Postgres (asyncpg + SQLModel)
        +--> Redis (caching, rate-limiting)
```

Requests flow through a clear separation of concerns: **routes** handle HTTP and validation, **services** hold business logic, **models/schemas** define the data shape at the DB and API boundary respectively. This separation is what makes the codebase extensible — the `Item` resource is a placeholder for the `Document` resource that a future RAG pipeline will use, following the exact same pattern.

## Features

- Async FastAPI app with a clean routes -> services -> db layering
- Dependency-aware `/health` endpoint that independently checks Postgres and Redis, returning `200` only when both are reachable and `503` with a clear per-dependency error otherwise
- Typed configuration via `pydantic-settings`, driven by environment variables / `.env`
- Full CRUD example (`Item` resource) with Alembic-managed schema migrations
- Structured JSON logging via `structlog`, with a unique request ID attached to every log line for a given request and echoed back in the `X-Request-ID` response header
- Global exception handler — unhandled errors return a clean `500` JSON response to the client while the full traceback and a structured error log (with request ID) are captured server-side
- Redis-backed rate limiting (fixed window), fails open if Redis itself is unavailable so a caching-layer outage doesn't take the whole API down
- Automated test suite with real Postgres transactions rolled back after every test — fully isolated, no test pollution, no mocking the database
- CI pipeline on every push/PR: lint (ruff), format check (ruff), type check (mypy), migrations, and the full test suite against fresh Postgres/Redis service containers
- Fully Dockerized: `docker compose up --build` brings up the entire stack with health-checked startup ordering
- Live-reload for code changes without rebuilding the image

## Getting started

```bash
# Generate the lockfile (first time only)
uv lock

# Build and start everything
docker compose up --build
```

Once containers are healthy:

```bash
# Confirm the app is up
curl http://localhost:8000/

# Check dependency health
curl http://localhost:8000/health

# Apply database migrations
uv run alembic upgrade head

# Create an item
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "first item"}'

# Fetch it back
curl http://localhost:8000/items/1
```

**Note:** any time a new Python dependency is added (`uv add ...`), rebuild the image with `docker compose up --build` — the volume mount only syncs application code live, not dependencies.

## Development

```bash
make up          # start containers in the background
make down        # stop containers
make build       # rebuild and start
make test        # run the test suite
make lint        # ruff check
make format      # ruff format
make typecheck   # mypy
make migrate     # apply alembic migrations
make check       # lint + typecheck + test, the same gate CI runs
```

Run `make check` before pushing — it's the same set of checks the CI pipeline enforces, so failures get caught locally first.

## Project structure

```
app/
  main.py                 FastAPI app entrypoint, middleware, exception handler
  config.py                typed settings from env vars
  db.py                     async SQLAlchemy engine/session
  redis_client.py           async Redis client
  logging_conf.py           structlog configuration
  middleware.py             request ID + structured request/response logging
  rate_limit.py             Redis-backed fixed-window rate limiter
  models.py                 SQLModel table definitions
  schemas.py                Pydantic request/response models
  routes/
    health.py
    items.py
  services/
    items_service.py
tests/
  conftest.py               isolated DB session + test client fixtures
  test_health.py
  test_items.py
alembic/                  migration environment + versions
.github/workflows/ci.yml  CI pipeline definition
docker-compose.yml
Dockerfile
Makefile
```

## Roadmap

This template is Phase 1 of a larger build. Phase 1 is complete. Planned next:

- [ ] RAG pipeline built on top of this foundation (ingestion, chunking, embeddings, pgvector, hybrid retrieval, reranking, citation grounding, retrieval evaluation)
- [ ] Agent orchestration layer (LangGraph, tool schemas, human-approval steps, MCP)
- [ ] Observability (Langfuse/OpenTelemetry tracing for prompts, retrieval, and tool calls)
- [ ] Security layer (prompt-injection tests, tool authorization, secrets handling)
- [ ] Cloud deployment (Azure, Terraform, staging/prod environments, rollback)
- [ ] ML fundamentals project (baseline vs. classic ML vs. LLM comparison)

## Why this exists

Built as the first step of a structured path into applied AI engineering — favoring production fundamentals (typed config, health checks, migrations, observability, CI, containerization) before layering on LLM-specific components, rather than starting from an LLM demo with no engineering underneath it.