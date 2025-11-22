from pydantic import BaseModel
from typing import Optional
from app.models.enums import CaregivingType, Gender

class CaregiverBase(BaseModel):
    photo: Optional[str] = None
    gender: Gender
    caregiving_type: CaregivingType
    hourly_rate: int

class CaregiverCreate(CaregiverBase):
    caregiver_user_id: int

class CaregiverUpdate(BaseModel):
    photo: Optional[str] = None
    gender: Optional[Gender] = None
    caregiving_type: Optional[CaregivingType] = None
    hourly_rate: Optional[int] = None

class CaregiverResponse(CaregiverBase):
    caregiver_user_id: int

    class Config:
        from_attributes = True
