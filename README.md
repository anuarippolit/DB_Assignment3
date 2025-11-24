# Caregiver Management API

## Description

CSCI 341 Database Assignment 3 part #3, made by Pavel Kokoshko. 
Team: Anuar Akimbekov, Pavel Kokoshko.

Stack: SQLAlchemy, FastAPI, uvicorn, pytest.

Database schema: `database_app.sql` creates the database. Models are 1:1 copies of database tables.

Structure:
```
app/
  models/ - SQLAlchemy ORM models
  routers/ - API endpoints
  schemas/ - validation schemas (DTOs)
templates/
  admin.html - main HTML
  css/ - static styles
  js/ - js module
tests/ - pytest (more or less integration tests)
static/ - Static files (caregiver photos only)
database_app.sql - database init. script. `database.sql` not used here due to adjustments made to schema. 
```

Several notes:
- I have deployed this to my personal server, w/o SSL as I have no free domen rn, maybe it may cause problems, but I hope no:)
- Caregiver photos:
  - saved in `/static` on server
  - Photo not retrieved automatically upon request for caregiver
  - in database only names are saved, but web-api has:
  - separate endpoints for update (`PUT /caregivers/{id}/photo`) and get (`GET /caregivers/{id}/photo`)
- "USER" database from Part II was re-named to "account" as it is reserved word, and I have experienced a range of problems with SQLAlchemy functions due to quotes needed for table "USER".

## Run app:

```bash
docker-compose --profile app up --build
```

Available at: 
1. http://localhost:8000 - admin panel
2. http://localhost:8000/docs - swagger 

## Run tests

```bash
docker-compose --profile test up --build
```

## Stop:

```bash
docker-compose --profile app down
```

---
Made by: Pavel Kokoshko
