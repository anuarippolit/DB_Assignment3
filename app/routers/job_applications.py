from fastapi import APIRouter, Depends, HTTPException, Form, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.models import JobApplication, Caregiver, Job
from app.schemas import JobApplicationCreate, JobApplicationUpdate, JobApplicationResponse
from app.database import get_db

router = APIRouter(prefix="/job-applications", tags=["job-applications"])

#region create
@router.post("/", response_model=JobApplicationResponse, status_code=201)
def create_job_application(
    caregiver_user_id: int = Form(...),
    job_id: int = Form(...),
    date_applied: Optional[date] = Form(None),
    db: Session = Depends(get_db)
):
    #region validate request data
    caregiver = db.query(Caregiver).filter(
        Caregiver.caregiver_user_id == caregiver_user_id
    ).first()
    if not caregiver:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    
    job = db.query(Job).filter(Job.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    existing = db.query(JobApplication).filter(
        JobApplication.caregiver_user_id == caregiver_user_id,
        JobApplication.job_id == job_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Job application already exists")
    #endregion validate request data

    #auto-generate date
    if date_applied is None:
        date_applied = date.today()
    
    db_job_application = JobApplication(
        caregiver_user_id=caregiver_user_id,
        job_id=job_id,
        date_applied=date_applied
    )

    db.add(db_job_application)
    db.commit()
    db.refresh(db_job_application)
    return db_job_application
#endregion

#region get one
@router.get("/caregiver/{caregiver_user_id}/job/{job_id}", response_model=JobApplicationResponse)
def get_job_application(caregiver_user_id: int, job_id: int, db: Session = Depends(get_db)):
    job_application = db.query(JobApplication).filter(
        JobApplication.caregiver_user_id == caregiver_user_id,
        JobApplication.job_id == job_id
    ).first()

    if not job_application:
        raise HTTPException(status_code=404, detail="Job application not found")

    return job_application
#endregion

#region get all
@router.get("/", response_model=List[JobApplicationResponse])
def get_job_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    job_applications = db.query(JobApplication).offset(skip).limit(limit).all()
    return job_applications
#endregion

#region update
@router.put("/caregiver/{caregiver_user_id}/job/{job_id}", response_model=JobApplicationResponse)
def update_job_application(
    caregiver_user_id: int,
    job_id: int,
    date_applied: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    db_job_application = db.query(JobApplication).filter(
        JobApplication.caregiver_user_id == caregiver_user_id,
        JobApplication.job_id == job_id
    ).first()
    if not db_job_application:
        raise HTTPException(status_code=404, detail="Job application not found")
    
    if date_applied is not None:
        db_job_application.date_applied = date_applied
    
    db.commit()
    db.refresh(db_job_application)
    return db_job_application
#endregion

#region delete
@router.delete("/caregiver/{caregiver_user_id}/job/{job_id}", status_code=204)
def delete_job_application(caregiver_user_id: int, job_id: int, db: Session = Depends(get_db)):
    db_job_application = db.query(JobApplication).filter(
        JobApplication.caregiver_user_id == caregiver_user_id,
        JobApplication.job_id == job_id
    ).first()
    
    if not db_job_application:
        raise HTTPException(status_code=404, detail="Job application not found")
    
    db.delete(db_job_application)
    db.commit()
    return None
#endregion