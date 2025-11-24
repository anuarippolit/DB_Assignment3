from fastapi import APIRouter, Depends, HTTPException, Form, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import Address, Member
from app.schemas import AddressCreate, AddressUpdate, AddressResponse
from app.database import get_db

router = APIRouter(prefix="/addresses", tags=["addresses"])

#region create 
@router.post("/", response_model=AddressResponse, status_code=201)
def create_address(
    member_user_id: int = Form(...),
    house_number: str = Form(...),
    street: str = Form(...),
    town: str = Form(...),
    db: Session = Depends(get_db)
):
    member = db.query(Member).filter(Member.member_user_id == member_user_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    if db.query(Address).filter(Address.member_user_id == member_user_id).first():
        raise HTTPException(status_code=400, detail="Address already exists for this member")
    
    db_address = Address(
        member_user_id=member_user_id,
        house_number=house_number,
        street=street,
        town=town
    )

    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address
#endregion


#region get one 
@router.get("/{member_user_id}", response_model=AddressResponse)
def get_address(member_user_id: int, db: Session = Depends(get_db)):
    address = db.query(Address).filter(Address.member_user_id == member_user_id).first()
    
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    return address
#endregion

#region get all
@router.get("/", response_model=List[AddressResponse])
def get_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    addresses = db.query(Address).offset(skip).limit(limit).all()

    return addresses
#endregion

#region update
@router.put("/{member_user_id}", response_model=AddressResponse)
def update_address(
    member_user_id: int,
    house_number: Optional[str] = Query(None),
    street: Optional[str] = Query(None),
    town: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    db_address = db.query(Address).filter(Address.member_user_id == member_user_id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    if house_number is not None:
        db_address.house_number = house_number
    if street is not None:
        db_address.street = street
    if town is not None:
        db_address.town = town
    
    db.commit()
    db.refresh(db_address)
    return db_address
#endregion

#region delete
@router.delete("/{member_user_id}", status_code=204)
def delete_address(member_user_id: int, db: Session = Depends(get_db)):
    db_address = db.query(Address).filter(Address.member_user_id == member_user_id).first()
    
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    db.delete(db_address)
    db.commit()
    
    return None
#endregion