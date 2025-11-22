from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from app.models.enums import CaregivingType

class JobBase(BaseModel):
    required_caregiving_type: CaregivingType
    other_requirements: Optional[str] = None
    date_posted: date

class JobCreate(BaseModel):
    job_id: Optional[int] = None
    member_user_id: int
    required_caregiving_type: CaregivingType
    other_requirements: Optional[str] = None
    date_posted: date = Field(default_factory=date.today) #auto-generated date 

class JobUpdate(BaseModel):
    member_user_id: Optional[int] = None
    required_caregiving_type: Optional[CaregivingType] = None
    other_requirements: Optional[str] = None
    date_posted: Optional[date] = None

class JobResponse(JobBase):
    job_id: int
    member_user_id: int

    class Config:
        from_attributes = True
