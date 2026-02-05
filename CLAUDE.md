# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Costhook is a web application for monitoring costs across different providers. Target audience: developers, indie hackers, and vibe coders.

## Tech Stack

- **Backend**: Python 3.13+ with FastAPI
- **Frontend**: React 19 + TypeScript + Vite (Node.js 22+)
- **Database & Auth**: Supabase (PostgreSQL + Auth)
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
│   │   │   ├── deps.py      # Dependencies (SessionDep, CurrentUser, CurrentUserProfile)
│   │   │   └── routes/      # API route modules (users, providers, costs, health)
│   │   ├── core/
│   │   │   ├── config.py    # Settings (pydantic-settings)
│   │   │   ├── db.py        # SQLAlchemy engine and session
│   │   │   ├── security.py  # JWT verification
│   │   │   └── crypto.py    # Credentials encryption (Fernet)
│   │   ├── models/          # SQLAlchemy ORM models (UserProfile, Provider, CostRecord)
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
│   │   ├── App.tsx          # Root component with routing
│   │   ├── lib/
│   │   │   ├── supabase.ts  # Supabase client
│   │   │   └── api.ts       # Backend API client
│   │   ├── contexts/        # React contexts (AuthContext)
│   │   ├── components/      # Shared components (Layout, ProtectedRoute)
│   │   └── pages/           # Page components (Dashboard, Providers, Settings)
│   ├── public/
│   ├── index.html
│   ├── vite.config.ts       # Vite config (proxy to backend on /api)
│   └── package.json
└── README.md
```

## Data Models

- **UserProfile**: Extension of Supabase auth user (display_name, timezone)
- **Provider**: Connected service (type, name, encrypted credentials, status)
- **CostRecord**: Cost data from providers (amount, service, period)

## API Endpoints

- `GET/PATCH /api/v1/users/me` - User profile
- `GET/POST /api/v1/providers` - List/create providers
- `GET/PATCH/DELETE /api/v1/providers/{id}` - Provider operations
- `GET /api/v1/costs` - List costs (with filters)
- `GET /api/v1/health` - Health check

## Auth Flow

- Frontend handles auth via Supabase JS SDK (`@supabase/supabase-js`)
- Backend verifies Supabase JWT tokens using `pyjwt`
- Protected routes use `CurrentUserProfile` dependency from `app/api/deps.py`
- Provider credentials encrypted with Fernet (ENCRYPTION_KEY env var)
