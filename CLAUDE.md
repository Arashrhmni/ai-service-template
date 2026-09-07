# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

This is an early-stage scaffold (day 1). The [README.md](README.md) describes an eventual goal of "async PostgreSQL, Redis caching, structured logging, Alembic migrations, and full Docker setup," but none of that exists yet — treat the README as an aspirational target, not a description of current code. Right now the repo is just a bare FastAPI app plus an unrelated packaging stub.

## Commands

Dependencies and the virtualenv are managed with [uv](https://docs.astral.sh/uv/) (see `uv.lock`, `.python-version` pinned to 3.12).

```bash
# install/sync dependencies
uv sync

# run the FastAPI app with auto-reload
uv run uvicorn app.main:app --reload
```

There is no test suite, linter, or type-checker configured yet — `pyproject.toml` has no `[tool.pytest]`, `[tool.ruff]`, or similar sections.

## Architecture

There are two independent, currently-unconnected pieces:

- **`app/main.py`** — the actual FastAPI application (`app = FastAPI()`), with routes defined directly on it. This is what `uvicorn app.main:app` serves.
- **`src/ai_service_template/`** — a separately packaged module exposing a `main()` function, wired up as the `ai-service-template` console script in `pyproject.toml` (`[project.scripts]`). It currently just prints a greeting and does not invoke the FastAPI app in `app/`.

When adding functionality, be aware these two entry points are not yet linked — decide whether new code belongs in the served app (`app/`) or the installable package (`src/ai_service_template/`), since routes added to one will not be reachable from the other.
