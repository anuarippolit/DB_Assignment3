from fastapi import APIRouter, Depends, HTTPException, Form, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
import logging

from typing import List, Optional

from app.models import Address, Member
from app.schemas import AddressCreate, AddressUpdate, AddressResponse
from app.database import get_db

logger = logging.getLogger(__name__)

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
    try:
        m = db.query(Member).filter(Member.member_user_id == member_user_id).first()
        if not m:
            raise HTTPException(status_code=404, detail="Member not found")
        
        if db.query(Address).filter(Address.member_user_id == member_user_id).first():
            raise HTTPException(status_code=400, detail="Address already exists for this member")
        
        a = Address(
            member_user_id=member_user_id,
            house_number=house_number,
            street=street,
            town=town
        )

        db.add(a)
        db.commit()
        db.refresh(a)
        return a
    except OperationalError as e:
        logger.error(f"Database connection error in POST /addresses/: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database connection error. Please try again later."
        )
#endregion


#region get one 
@router.get("/{member_user_id}", response_model=AddressResponse)
def get_address(member_user_id: int, db: Session = Depends(get_db)):
    try:
        a = db.query(Address).filter(Address.member_user_id == member_user_id).first()
        
        if not a:
            raise HTTPException(status_code=404, detail="Address not found")

        return a
    except OperationalError as e:
        logger.error(f"Database connection error in GET /addresses/{member_user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database connection error. Please try again later."
        )
#endregion

#region get all
@router.get("/", response_model=List[AddressResponse])
def get_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        a = db.query(Address).offset(skip).limit(limit).all()
        return a
    except OperationalError as e:
        logger.error(f"Database connection error in GET /addresses/: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database connection error. Please try again later."
        )
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
    try:
        a = db.query(Address).filter(Address.member_user_id == member_user_id).first()
        if not a:
            raise HTTPException(status_code=404, detail="Address not found")
        
        if house_number is not None:
            a.house_number = house_number
        if street is not None:
            a.street = street
        if town is not None:
            a.town = town
        
        db.commit()
        db.refresh(a)
        return a
    except OperationalError as e:
        logger.error(f"Database connection error in PUT /addresses/{member_user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database connection error. Please try again later."
        )
#endregion

#region delete
@router.delete("/{member_user_id}", status_code=204)
def delete_address(member_user_id: int, db: Session = Depends(get_db)):
    try:
        a = db.query(Address).filter(Address.member_user_id == member_user_id).first()
        
        if not a:
            raise HTTPException(status_code=404, detail="Address not found")
        
        db.delete(a)
        db.commit()
        
        return None
    except OperationalError as e:
        logger.error(f"Database connection error in DELETE /addresses/{member_user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database connection error. Please try again later."
        )
#endregion