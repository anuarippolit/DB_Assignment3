# Caregiver Management API

## Run app:

```bash
docker-compose --profile app up --build
```

Available at: http://localhost:8000 - swagger UI

## Run tests

```bash
docker-compose --profile test up --build
```

## Stop:

```bash
docker-compose --profile app down
```

## Description

Stack: SQLAlchemy, FastAPI, uvicorn, pytest.

Database schema: `database_app.sql` creates the database. Models are 1:1 copies of database tables.

Structure:
```
app/
  models/ - SQLAlchemy ORM models
  routers/ - API endpoints
  schemas/ - Pydantic validation schemas
tests/ - pytest tests
database_app.sql - database initialization script
```

NOTE: Caregiver photos: saved in `/static`, separate endpoints for upload (`PUT /caregivers/{id}/photo`) and get (`GET /caregivers/{id}/photo`). 