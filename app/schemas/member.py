from pydantic import BaseModel
from typing import Optional

class MemberBase(BaseModel):
    house_rules: Optional[str] = None
    dependent_description: Optional[str] = None

class MemberCreate(MemberBase):
    member_user_id: int

class MemberUpdate(BaseModel):
    house_rules: Optional[str] = None
    dependent_description: Optional[str] = None

class MemberResponse(MemberBase):
    member_user_id: int

    class Config:
        from_attributes = True
