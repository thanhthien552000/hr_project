# HR Management System — Backend API

FastAPI + SQLAlchemy 2.0 + PostgreSQL + Alembic

## Requirements
- Python 3.11+
- PostgreSQL 14+

## Setup

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy env file
copy .env.example .env
# Edit .env with your database credentials

# 4. Run migrations
alembic upgrade head

# 5. Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Docs
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure
```
app/
├── api/v1/          # Route handlers
├── core/            # Config, DB, security
├── common/          # Shared utilities
├── models/          # SQLAlchemy models
├── schemas/         # Pydantic schemas
├── services/        # Business logic
├── repositories/    # Data access layer
└── main.py          # App entry point
tests/               # Pytest test suite
alembic/             # DB migrations
```
