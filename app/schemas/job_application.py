from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class JobApplicationBase(BaseModel):
    date_applied: date

class JobApplicationCreate(BaseModel):
    caregiver_user_id: int
    job_id: int
    date_applied: date = Field(default_factory=date.today) #auto-generated date


class JobApplicationUpdate(BaseModel):
    date_applied: Optional[date] = None

class JobApplicationResponse(JobApplicationBase):
    caregiver_user_id: int
    job_id: int

    class Config:
        from_attributes = True
