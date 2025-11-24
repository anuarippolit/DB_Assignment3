import pytest
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.database import Base, get_db
from app.main import app

from app.models.user import User
from app.models.caregiver import Caregiver
from app.models.member import Member
from app.models.address import Address
from app.models.job import Job
from app.models.job_application import JobApplication
from app.models.appointment import Appointment


SQLALCHEMY_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/caregiver_test_db"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_test_db():
    sql_file_path = os.getenv("DATABASE_SQL_PATH", "database_app.sql")
    if not os.path.exists(sql_file_path):
        sql_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database_app.sql")
    
    with engine.begin() as conn:
        with open(sql_file_path, "r") as f:
            sql_script = f.read()
        
        for statement in sql_script.split(';'):
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                statement_upper = statement.upper()
                if 'INSERT' not in statement_upper:
                    try:
                        conn.execute(text(statement))
                    except Exception as e:
                        if 'DROP' not in statement_upper:
                            raise e


def drop_test_db():
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS APPOINTMENT CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS JOB_APPLICATION CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS JOB CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS ADDRESS CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS MEMBER CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS CAREGIVER CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS account CASCADE"))
        conn.execute(text("DROP TYPE IF EXISTS gender_enum CASCADE"))
        conn.execute(text("DROP TYPE IF EXISTS caregiving_type_enum CASCADE"))
        conn.execute(text("DROP TYPE IF EXISTS appointment_status_enum CASCADE"))


@pytest.fixture(scope="function")
def db():
    drop_test_db()
    init_test_db()
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        drop_test_db()


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

