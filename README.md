
# Database Queries Documentation

## Overview

`database_queries.py` is a Python script for executing SQL queries against a PostgreSQL database. It's divided into two main parts:
- **Part 1**: Initializes the database with schema and initial data
- **Part 2**: Executes various SQL queries (UPDATE, DELETE, SELECT, VIEW operations)

## Prerequisites

1. **PostgreSQL** database running
2. **Python 3** with required packages:
   ```bash
   pip install sqlalchemy psycopg2-binary python-dotenv
   ```

## Setup

1. **Create `.env` file** (copy from `.env.example`):
   ```env
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=caregivers_db
   ```

## Usage

### Run Part 1 (Initialize Database)

```bash
python3 -c "from database_queries import part_1; part_1()"
```

This will:
- Create all tables (USER, CAREGIVER, MEMBER, JOB, etc.)
- Insert initial data from `database.sql`

### Run Part 2 (Execute Queries)

```bash
python3 -c "from database_queries import part_2; part_2()"
```

This will:
- Executes all SQL queries (UPDATE, DELETE, SELECT, VIEW)
- Includes verification checks after UPDATE/DELETE operations
- Automatically disposes database connection when done

# Caregiver Management API

## Description

CSCI 341 Database Assignment 3 part #3

Stack: SQLAlchemy, FastAPI, uvicorn, pytest, Docker.

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
Made by: Pavel Kokoshko (web-app), Anuar Akimbekov (queries, structure)