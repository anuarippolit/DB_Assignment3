from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr #out-of-box validation for emails. provides extensive errors' descriptions:) 
    given_name: str
    surname: str
    city: str
    phone_number: str #phone is not auto-validated, but made a validator functon in routers/users.py 
    profile_description: Optional[str] = None
    password: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    given_name: Optional[str] = None
    surname: Optional[str] = None
    city: Optional[str] = None
    phone_number: Optional[str] = None
    profile_description: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    user_id: int

    class Config:
        from_attributes = True
