# Costhook

A web application for monitoring costs across different providers. Built for developers, indie hackers, and vibe coders who want to keep track of their spending across multiple services.

## Tech Stack

- **Backend**: Python with FastAPI
- **Frontend**: React + TypeScript + Vite
- **Database & Auth**: Supabase

## Project Structure

```
costhook/
├── backend/          # FastAPI application
├── frontend/         # React application
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.13+
- Node.js 22+
- [uv](https://docs.astral.sh/uv/)
- [Supabase](https://supabase.com/) account

### Supabase Setup

1. Create a new project at [supabase.com](https://supabase.com/)
2. Go to Settings > API to find your project URL, anon key, and JWT secret
3. Go to Settings > Database to find your connection string

### Backend Setup

```bash
cd backend
cp .env.example .env
# Edit .env with your Supabase credentials
uv sync
uv run uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
cp .env.example .env
# Edit .env with your Supabase credentials
npm install
npm run dev
```

## Environment Variables

### Backend (.env)

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_JWT_SECRET=your-jwt-secret
DATABASE_URL=postgresql+psycopg://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
```

### Frontend (.env)

```
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```

## License

Private project - All rights reserved.
