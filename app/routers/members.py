from fastapi import APIRouter, Depends, HTTPException, Form, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
import logging

from typing import List, Optional

from app.models import Member, User
from app.schemas import MemberCreate, MemberUpdate, MemberResponse
from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/members", tags=["members"])

#region create member
@router.post("/", response_model=MemberResponse, status_code=201)
def create_member(
    member_user_id: int = Form(...),
    house_rules: Optional[str] = Form(None),
    dependent_description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    try:
        u = db.query(User).filter(User.user_id == member_user_id).first()

        if not u:
            raise HTTPException(status_code=404, detail=f"User with id {member_user_id} not found. Please create the user first.")
        
        if db.query(Member).filter(Member.member_user_id == member_user_id).first():
            raise HTTPException(status_code=400, detail="Member already exists")
        
        m = Member(
            member_user_id=member_user_id,
            house_rules=house_rules,
            dependent_description=dependent_description
        )
        db.add(m)
        db.commit()
        db.refresh(m)
        return m
    except OperationalError as e:
        logger.error(f"Database connection error in POST /members/: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database connection error. Please try again later."
        )
#endregion create member

#region get all members
@router.get("/", response_model=List[MemberResponse])
def get_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        m = db.query(Member).offset(skip).limit(limit).all()
        return m
    except OperationalError as e:
        logger.error(f"Database connection error in GET /members/: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database connection error. Please try again later."
        )
#endregion get all members

#region get member
@router.get("/{member_user_id}", response_model=MemberResponse)
def get_member(member_user_id: int, db: Session = Depends(get_db)):
    try:
        m = db.query(Member).filter(Member.member_user_id == member_user_id).first()
        
        if not m:
            raise HTTPException(status_code=404, detail="Member not found")

        return m
    except OperationalError as e:
        logger.error(f"Database connection error in GET /members/{member_user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database connection error. Please try again later."
        )
#endregion get member

#region update member
@router.put("/{member_user_id}", response_model=MemberResponse)
def update_member(
    member_user_id: int,
    house_rules: Optional[str] = Query(None),
    dependent_description: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        m = db.query(Member).filter(Member.member_user_id == member_user_id).first()
        
        if not m:
            raise HTTPException(status_code=404, detail="Member not found")
        
        if house_rules is not None:
            m.house_rules = house_rules
        if dependent_description is not None:
            m.dependent_description = dependent_description
        
        db.commit()
        db.refresh(m)
        return m
    except OperationalError as e:
        logger.error(f"Database connection error in PUT /members/{member_user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database connection error. Please try again later."
        )
#endregion update member

#region delete member
@router.delete("/{member_user_id}", status_code=204)
def delete_member(member_user_id: int, db: Session = Depends(get_db)):
    try:
        m = db.query(Member).filter(Member.member_user_id == member_user_id).first()
        if not m:
            raise HTTPException(status_code=404, detail="Member not found")
        
        db.delete(m)
        db.commit()
        return None
    except OperationalError as e:
        logger.error(f"Database connection error in DELETE /members/{member_user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database connection error. Please try again later."
        )
#endregion delete member