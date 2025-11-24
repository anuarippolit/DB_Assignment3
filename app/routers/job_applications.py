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
    c = db.query(Caregiver).filter(
        Caregiver.caregiver_user_id == caregiver_user_id
    ).first()
    if not c:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    
    j = db.query(Job).filter(Job.job_id == job_id).first()
    if not j:
        raise HTTPException(status_code=404, detail="Job not found")
    
    e = db.query(JobApplication).filter(
        JobApplication.caregiver_user_id == caregiver_user_id,
        JobApplication.job_id == job_id
    ).first()
    if e:
        raise HTTPException(status_code=400, detail="Job application already exists")
    #endregion validate request data

    #auto-generate date
    if date_applied is None:
        date_applied = date.today()
    
    ja = JobApplication(
        caregiver_user_id=caregiver_user_id,
        job_id=job_id,
        date_applied=date_applied
    )

    db.add(ja)
    db.commit()
    db.refresh(ja)
    return ja
#endregion

#region get one
@router.get("/caregiver/{caregiver_user_id}/job/{job_id}", response_model=JobApplicationResponse)
def get_job_application(caregiver_user_id: int, job_id: int, db: Session = Depends(get_db)):
    ja = db.query(JobApplication).filter(
        JobApplication.caregiver_user_id == caregiver_user_id,
        JobApplication.job_id == job_id
    ).first()

    if not ja:
        raise HTTPException(status_code=404, detail="Job application not found")

    return ja
#endregion

#region get all
@router.get("/", response_model=List[JobApplicationResponse])
def get_job_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ja = db.query(JobApplication).offset(skip).limit(limit).all()
    return ja
#endregion

#region update
@router.put("/caregiver/{caregiver_user_id}/job/{job_id}", response_model=JobApplicationResponse)
def update_job_application(
    caregiver_user_id: int,
    job_id: int,
    date_applied: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    ja = db.query(JobApplication).filter(
        JobApplication.caregiver_user_id == caregiver_user_id,
        JobApplication.job_id == job_id
    ).first()
    if not ja:
        raise HTTPException(status_code=404, detail="Job application not found")
    
    if date_applied is not None:
        ja.date_applied = date_applied
    
    db.commit()
    db.refresh(ja)
    return ja
#endregion

#region delete
@router.delete("/caregiver/{caregiver_user_id}/job/{job_id}", status_code=204)
def delete_job_application(caregiver_user_id: int, job_id: int, db: Session = Depends(get_db)):
    ja = db.query(JobApplication).filter(
        JobApplication.caregiver_user_id == caregiver_user_id,
        JobApplication.job_id == job_id
    ).first()
    
    if not ja:
        raise HTTPException(status_code=404, detail="Job application not found")
    
    db.delete(ja)
    db.commit()
    return None
#endregion