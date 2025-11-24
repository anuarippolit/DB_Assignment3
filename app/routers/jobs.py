from fastapi import APIRouter, Depends, HTTPException, Form, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.models import Job, Member
from app.models.enums import CaregivingType
from app.schemas import JobCreate, JobUpdate, JobResponse
from app.database import get_db

router = APIRouter(prefix="/jobs", tags=["jobs"])

#region create
@router.post("/", response_model=JobResponse, status_code=201)
def create_job(
    member_user_id: int = Form(...),
    required_caregiving_type: CaregivingType = Form(...),
    other_requirements: Optional[str] = Form(None),
    date_posted: Optional[date] = Form(None, description="If empty it will insert todays date here"),
    job_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    member = db.query(Member).filter(Member.member_user_id == member_user_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    if job_id and db.query(Job).filter(Job.job_id == job_id).first():
        raise HTTPException(status_code=400, detail="Job ID already exists")
    
    if date_posted is None:
        date_posted = date.today()
    
    db_job = Job(
        job_id=job_id,
        member_user_id=member_user_id,
        required_caregiving_type=required_caregiving_type,
        other_requirements=other_requirements,
        date_posted=date_posted
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job
#endregion

#region get one

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
#endregion

#region get all

@router.get("/", response_model=List[JobResponse])
def get_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = db.query(Job).offset(skip).limit(limit).all()
    return jobs
#endregion

#region update
@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    member_user_id: Optional[int] = Query(None),
    required_caregiving_type: Optional[CaregivingType] = Query(None, description="Type of caregiving service required. Possible values: BABYSITTER, ELDERLY_CARE, PLAYMATE_FOR_CHILDREN"),
    other_requirements: Optional[str] = Query(None),
    date_posted: Optional[date] = Query(None, description="If empty it will insert todays date here"),
    db: Session = Depends(get_db)
):
    #region validate request 
    db_job = db.query(Job).filter(Job.job_id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if member_user_id is not None and member_user_id != db_job.member_user_id:
        member = db.query(Member).filter(Member.member_user_id == member_user_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        db_job.member_user_id = member_user_id
    
    if required_caregiving_type is not None:
        db_job.required_caregiving_type = required_caregiving_type
    if other_requirements is not None:
        db_job.other_requirements = other_requirements
    if date_posted is not None:
        db_job.date_posted = date_posted
    #endregion validate request 

    db.commit()
    db.refresh(db_job)
    return db_job
#endregion
#region delete

@router.delete("/{job_id}", status_code=204)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(Job).filter(Job.job_id == job_id).first()

    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db.delete(db_job)
    db.commit()
    return None
#endregion