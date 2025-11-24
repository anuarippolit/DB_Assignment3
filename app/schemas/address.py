from pydantic import BaseModel
from typing import Optional

class AddressBase(BaseModel):
    house_number: str
    street: str
    town: str

class AddressCreate(AddressBase):
    member_user_id: int

class AddressUpdate(BaseModel):
    house_number: Optional[str] = None
    street: Optional[str] = None
    town: Optional[str] = None

class AddressResponse(AddressBase):
    member_user_id: int

    class Config:
        from_attributes = True
