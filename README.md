# AI Service Template

A production-style FastAPI boilerplate built as the foundation for a series of AI engineering projects — RAG systems, agentic workflows, and deployed cloud services. Every later project in this series starts from this template rather than rebuilding boilerplate from scratch.

This isn't a tutorial clone. It's built incrementally, with each piece added and verified independently: dependency-aware health checks, real database migrations, a proper service-layer architecture, and a fully containerized local dev environment.

## Stack

- **FastAPI** — async Python web framework
- **PostgreSQL 16** (async, via `asyncpg` + SQLAlchemy async engine)
- **SQLModel** — typed ORM models that double as Pydantic schemas
- **Alembic** — versioned database migrations
- **Redis 7** — caching / rate-limiting layer
- **Docker Compose** — full local stack (API + Postgres + Redis) with health-checked service dependencies
- **uv** — fast Python dependency management

## Architecture

┌─────────────────────────────────────────┐
│ FastAPI app │
│ ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│ │ routes │ │ services │ │ schemas │ │
│ │ (health, │ │ (business│ │(Pydantic│ │
│ │ items) │ │ logic) │ │ models) │ │
│ └──────────┘ └──────────┘ └─────────┘ │
│ │ │ │
│ ┌────▼────┐ ┌─────▼─────┐ │
│ │ Postgres│ │ Redis │ │
│ │ (asyncpg│ │ (caching, │ │
│ │+SQLModel)│ │ rate-limit│ │
│ └─────────┘ └───────────┘ │
└─────────────────────────────────────────┘

Requests flow through a clear separation of concerns: **routes** handle HTTP and validation, **services** hold business logic, **models/schemas** define the data shape at the DB and API boundary respectively. This separation is what makes the codebase extensible — the `Item` resource below is a placeholder for the `Document` resource that a future RAG pipeline will use, following the exact same pattern.

## Features so far

- ✅ Async FastAPI app with a clean routes → services → db layering
- ✅ Dependency-aware `/health` endpoint that independently checks Postgres and Redis, returning `200` only when both are reachable and `503` with a clear per-dependency error otherwise
- ✅ Typed configuration via `pydantic-settings`, driven by environment variables / `.env`
- ✅ Full CRUD example (`Item` resource) with Alembic-managed schema migrations
- ✅ Fully Dockerized: `docker compose up --build` brings up the entire stack with health-checked startup ordering
- ✅ Live-reload for code changes without rebuilding the image

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

## Project structure

app/
├── main.py # FastAPI app entrypoint
├── config.py # typed settings from env vars
├── db.py # async SQLAlchemy engine/session
├── redis_client.py # async Redis client
├── models.py # SQLModel table definitions
├── schemas.py # Pydantic request/response models
├── routes/
│ ├── health.py
│ └── items.py
└── services/
└── items_service.py
alembic/ # migration environment + versions
docker-compose.yml
Dockerfile


## Roadmap

This template is Phase 1 of a larger build. Planned next:

- [ ] Automated test suite (pytest + throwaway test database)
- [ ] Structured logging + request IDs + rate limiting
- [ ] CI pipeline (lint, type-check, test on every push)
- [ ] RAG pipeline built on top of this foundation (ingestion, embeddings, hybrid retrieval, evaluation)
- [ ] Agent orchestration layer (LangGraph, MCP)
- [ ] Observability (Langfuse/OpenTelemetry tracing)
- [ ] Cloud deployment (Azure, Terraform, CI/CD)

## Why this exists

Built as the first step of a structured path into applied AI engineering — favoring production fundamentals (typed config, health checks, migrations, containerization) before layering on LLM-specific components, rather than starting from an LLM demo with no engineering underneath it.