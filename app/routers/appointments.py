from fastapi import APIRouter, Depends, HTTPException, Form, Query
from sqlalchemy.orm import Session

from typing import List, Optional
from datetime import date, time

from app.models import Appointment, Caregiver, Member
from app.models.enums import AppointmentStatus
from app.schemas import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from app.database import get_db

router = APIRouter(prefix="/appointments", tags=["appointments"])

#region create
@router.post("/", response_model=AppointmentResponse, status_code=201)
def create_appointment(
    caregiver_user_id: int = Form(...),
    member_user_id: int = Form(...),
    appointment_date: date = Form(...),
    appointment_time: time = Form(...),
    work_hours: int = Form(...),
    status: AppointmentStatus = Form(...),
    appointment_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    #region validate request data
    c = db.query(Caregiver).filter(
        Caregiver.caregiver_user_id == caregiver_user_id
    ).first()
    if not c:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    
    m = db.query(Member).filter(
        Member.member_user_id == member_user_id
    ).first()
    if not m:
        raise HTTPException(status_code=404, detail="Member not found")
    
    if appointment_id and db.query(Appointment).filter(
        Appointment.appointment_id == appointment_id
    ).first():
        raise HTTPException(status_code=400, detail="Appointment ID already exists")
    #endregion validate request data

    #auto-generate appointment_id if not provided in request
    if appointment_id is None:
        max_a = db.query(Appointment).order_by(Appointment.appointment_id.desc()).first()
        appointment_id = (max_a.appointment_id + 1) if max_a else 1
    
    a = Appointment(
        appointment_id=appointment_id,
        caregiver_user_id=caregiver_user_id,
        member_user_id=member_user_id,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        work_hours=work_hours,
        status=status
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return a
#endregion

#region get one
@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    a = db.query(Appointment).filter(
        Appointment.appointment_id == appointment_id
    ).first()
    if not a:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return a
#endregion

#region get all
@router.get("/", response_model=List[AppointmentResponse])
def get_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    a = db.query(Appointment).offset(skip).limit(limit).all()

    return a
#endregion

#region update  
@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    caregiver_user_id: Optional[int] = Query(None),
    member_user_id: Optional[int] = Query(None),
    appointment_date: Optional[date] = Query(None),
    appointment_time: Optional[time] = Query(None),
    work_hours: Optional[int] = Query(None),
    status: Optional[AppointmentStatus] = Query(None, description="Status of the appointment. Possible values: PENDING, ACCEPTED, DECLINED"),
    db: Session = Depends(get_db)
):
    #region validate request data
    a = db.query(Appointment).filter(
        Appointment.appointment_id == appointment_id
    ).first()
    if not a:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    if caregiver_user_id is not None and caregiver_user_id != a.caregiver_user_id:
        c = db.query(Caregiver).filter(
            Caregiver.caregiver_user_id == caregiver_user_id
        ).first()
        if not c:
            raise HTTPException(status_code=404, detail="Caregiver not found")
        a.caregiver_user_id = caregiver_user_id
    
    if member_user_id is not None and member_user_id != a.member_user_id:
        m = db.query(Member).filter(
            Member.member_user_id == member_user_id
        ).first()
        if not m:
            raise HTTPException(status_code=404, detail="Member not found")
        a.member_user_id = member_user_id
    
    if appointment_date is not None:
        if appointment_date < date.today():
            raise HTTPException(status_code=400, detail="Appointment date cannot be in the past")
        a.appointment_date = appointment_date
    
    if appointment_time is not None:
        if appointment_time.hour < 0 or appointment_time.hour > 23:
            raise HTTPException(status_code=400, detail="Hour must be between 0 and 23")
        if appointment_time.minute < 0 or appointment_time.minute > 59:
            raise HTTPException(status_code=400, detail="Minute must be between 0 and 59")
        if appointment_time.second is not None and (appointment_time.second < 0 or appointment_time.second > 59):
            raise HTTPException(status_code=400, detail="Second must be between 0 and 59")
        a.appointment_time = appointment_time
    
    if work_hours is not None:
        if work_hours <= 0:
            raise HTTPException(status_code=400, detail="Work hours must be greater than 0")
        a.work_hours = work_hours
    
    if status is not None:
        a.status = status
    #endregion validate request data

    db.commit()
    db.refresh(a)
    return a
#endregion update

#region delete

@router.delete("/{appointment_id}", status_code=204)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    a = db.query(Appointment).filter(
        Appointment.appointment_id == appointment_id
    ).first()
    
    if not a:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    db.delete(a)
    db.commit()
    return None
#endregion