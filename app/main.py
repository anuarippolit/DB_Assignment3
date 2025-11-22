from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, caregivers, members, addresses, jobs, job_applications, appointments
from app.models import User, Caregiver, Member, Address, Job, JobApplication, Appointment

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Caregiver Management API",
    version="1.0.3",
    docs_url="/",
    redoc_url="/redoc",
)

app.include_router(users.router)
app.include_router(caregivers.router)
app.include_router(members.router)
app.include_router(addresses.router)
app.include_router(jobs.router)
app.include_router(job_applications.router)
app.include_router(appointments.router)