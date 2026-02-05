# Costhook

A web application for monitoring costs across different providers. Built for developers, indie hackers, and vibe coders who want to keep track of their spending across multiple services.

## Tech Stack

- **Backend**: Python with FastAPI
- **Frontend**: React
- **Database**: PostgreSQL

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
- PostgreSQL 17+
- [uv](https://docs.astral.sh/uv/)

### Backend Setup

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Database

Create a PostgreSQL database and configure the connection string in your environment variables.

## Environment Variables

```
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/costhook
```

## License

Private project - All rights reserved.
