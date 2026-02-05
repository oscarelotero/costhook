# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Costhook is a web application for monitoring costs across different providers. Target audience: developers, indie hackers, and vibe coders.

## Tech Stack

- **Backend**: Python 3.13+ with FastAPI
- **Frontend**: React 19 + TypeScript + Vite (Node.js 22+)
- **Database**: PostgreSQL 17+
- **Python Package Manager**: uv
- **Linting**: ruff (via pre-commit)
- **Migrations**: Alembic

## Common Commands

### Backend

```bash
cd backend
uv sync                                       # Install dependencies
uv run uvicorn app.main:app --reload          # Run dev server
uv run pytest                                 # Run tests
uv run pytest tests/test_file.py::test_name   # Run single test
uv run ruff check .                           # Lint code
uv run ruff format .                          # Format code
```

### Database Migrations

```bash
cd backend
uv run alembic upgrade head                   # Apply all migrations
uv run alembic downgrade -1                   # Rollback one migration
uv run alembic revision --autogenerate -m "description"  # Create migration
```

### Pre-commit

```bash
cd backend
uv run pre-commit install                     # Install hooks (one time)
uv run pre-commit run --all-files             # Run on all files
```

### Frontend

```bash
cd frontend
npm install                    # Install dependencies
npm run dev                    # Run dev server (port 3000)
npm test                       # Run tests with Vitest
npm run lint                   # Lint code
npm run format                 # Format code with Prettier
npm run build                  # Production build
```

## Architecture

```
costhook/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application factory
│   │   ├── api/
│   │   │   ├── deps.py      # Dependency injection (SessionDep, etc.)
│   │   │   └── routes/      # API route modules
│   │   ├── core/
│   │   │   ├── config.py    # Settings (pydantic-settings)
│   │   │   └── db.py        # SQLAlchemy engine and session
│   │   ├── models/          # SQLAlchemy ORM models
│   │   ├── schemas/         # Pydantic schemas (request/response)
│   │   └── crud/            # Database operations
│   ├── alembic/
│   │   ├── env.py           # Migration environment
│   │   └── versions/        # Migration files
│   ├── tests/
│   ├── pyproject.toml
│   └── .pre-commit-config.yaml
├── frontend/
│   ├── src/
│   │   ├── main.tsx         # React entry point
│   │   └── App.tsx          # Root component
│   ├── public/
│   ├── index.html
│   ├── vite.config.ts       # Vite config (proxy to backend on /api)
│   └── package.json
└── README.md
```

API routes are versioned under `/api/v1`. Health check: `GET /api/v1/health`
