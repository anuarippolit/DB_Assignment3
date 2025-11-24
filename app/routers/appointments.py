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
    caregiver = db.query(Caregiver).filter(
        Caregiver.caregiver_user_id == caregiver_user_id
    ).first()
    if not caregiver:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    
    member = db.query(Member).filter(
        Member.member_user_id == member_user_id
    ).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    if appointment_id and db.query(Appointment).filter(
        Appointment.appointment_id == appointment_id
    ).first():
        raise HTTPException(status_code=400, detail="Appointment ID already exists")
    #endregion validate request data

    #auto-generate appointment_id if not provided in request
    if appointment_id is None:
        max_appointment = db.query(Appointment).order_by(Appointment.appointment_id.desc()).first()
        appointment_id = (max_appointment.appointment_id + 1) if max_appointment else 1
    
    db_appointment = Appointment(
        appointment_id=appointment_id,
        caregiver_user_id=caregiver_user_id,
        member_user_id=member_user_id,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        work_hours=work_hours,
        status=status
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment
#endregion

#region get one
@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(
        Appointment.appointment_id == appointment_id
    ).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment
#endregion

#region get all
@router.get("/", response_model=List[AppointmentResponse])
def get_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    appointments = db.query(Appointment).offset(skip).limit(limit).all()

    return appointments
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
    db_appointment = db.query(Appointment).filter(
        Appointment.appointment_id == appointment_id
    ).first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    if caregiver_user_id is not None and caregiver_user_id != db_appointment.caregiver_user_id:
        caregiver = db.query(Caregiver).filter(
            Caregiver.caregiver_user_id == caregiver_user_id
        ).first()
        if not caregiver:
            raise HTTPException(status_code=404, detail="Caregiver not found")
        db_appointment.caregiver_user_id = caregiver_user_id
    
    if member_user_id is not None and member_user_id != db_appointment.member_user_id:
        member = db.query(Member).filter(
            Member.member_user_id == member_user_id
        ).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        db_appointment.member_user_id = member_user_id
    
    if appointment_date is not None:
        if appointment_date < date.today():
            raise HTTPException(status_code=400, detail="Appointment date cannot be in the past")
        db_appointment.appointment_date = appointment_date
    
    if appointment_time is not None:
        if appointment_time.hour < 0 or appointment_time.hour > 23:
            raise HTTPException(status_code=400, detail="Hour must be between 0 and 23")
        if appointment_time.minute < 0 or appointment_time.minute > 59:
            raise HTTPException(status_code=400, detail="Minute must be between 0 and 59")
        if appointment_time.second is not None and (appointment_time.second < 0 or appointment_time.second > 59):
            raise HTTPException(status_code=400, detail="Second must be between 0 and 59")
        db_appointment.appointment_time = appointment_time
    
    if work_hours is not None:
        if work_hours <= 0:
            raise HTTPException(status_code=400, detail="Work hours must be greater than 0")
        db_appointment.work_hours = work_hours
    
    if status is not None:
        db_appointment.status = status
    #endregion validate request data

    db.commit()
    db.refresh(db_appointment)
    return db_appointment
#endregion update

#region delete

@router.delete("/{appointment_id}", status_code=204)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = db.query(Appointment).filter(
        Appointment.appointment_id == appointment_id
    ).first()
    
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    db.delete(db_appointment)
    db.commit()
    return None
#endregion