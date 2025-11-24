from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, time
from app.models.enums import AppointmentStatus

class AppointmentBase(BaseModel):
    appointment_date: date
    appointment_time: time
    work_hours: int = Field(gt=0)
    status: AppointmentStatus
    
    #region validation methods
    @field_validator('appointment_date')
    @classmethod
    def validate_appointment_date(cls, v: date) -> date:
        if v < date.today():
            raise ValueError('Appointment date cannot be in the past')
        
        return v
    
    @field_validator('appointment_time')
    @classmethod
    def validate_appointment_time(cls, v: time) -> time:
        if v.hour < 0 or v.hour > 23:
            raise ValueError('Hour must be between 0 and 23')

        if v.minute < 0 or v.minute > 59:
            raise ValueError('Minute must be between 0 and 59')
        
        if v.second is not None and (v.second < 0 or v.second > 59):
            raise ValueError('Second must be between 0 and 59')

        return v
    #endregion validation methods

class AppointmentCreate(AppointmentBase):
    appointment_id: Optional[int] = None
    caregiver_user_id: int
    member_user_id: int

class AppointmentUpdate(BaseModel):
    caregiver_user_id: Optional[int] = None
    member_user_id: Optional[int] = None
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    work_hours: Optional[int] = Field(None, gt=0)
    status: Optional[AppointmentStatus] = None
    
    #region validation methods
    @field_validator('appointment_date')
    @classmethod
    def validate_appointment_date(cls, v: Optional[date]) -> Optional[date]:
        
        if v is not None and v < date.today():
            raise ValueError('Appointment date cannot be in the past')
        
        return v
    
    @field_validator('appointment_time')
    @classmethod
    def validate_appointment_time(cls, v: Optional[time]) -> Optional[time]:
        if v is not None:
            if v.hour < 0 or v.hour > 23:
                raise ValueError('Hour must be between 0 and 23')

            if v.minute < 0 or v.minute > 59:
                raise ValueError('Minute must be between 0 and 59')

            if v.second is not None and (v.second < 0 or v.second > 59):
                raise ValueError('Second must be between 0 and 59')
        return v
    #endregion validation methods

#class AppointmentResponse(AppointmentBase)
class AppointmentResponse(BaseModel):
    appointment_id: int
    caregiver_user_id: int
    member_user_id: int
    appointment_date: date
    appointment_time: time
    work_hours: int
    status: AppointmentStatus

    class Config:
        from_attributes = True
