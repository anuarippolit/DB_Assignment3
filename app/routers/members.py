from fastapi import APIRouter, Depends, HTTPException, Form, Query
from sqlalchemy.orm import Session

from typing import List, Optional
from app.models import Member, User
from app.schemas import MemberCreate, MemberUpdate, MemberResponse
from app.database import get_db

router = APIRouter(prefix="/members", tags=["members"])

#region create member
@router.post("/", response_model=MemberResponse, status_code=201)
def create_member(
    member_user_id: int = Form(...),
    house_rules: Optional[str] = Form(None),
    dependent_description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.user_id == member_user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {member_user_id} not found. Please create the user first.")
    
    if db.query(Member).filter(Member.member_user_id == member_user_id).first():
        raise HTTPException(status_code=400, detail="Member already exists")
    
    db_member = Member(
        member_user_id=member_user_id,
        house_rules=house_rules,
        dependent_description=dependent_description
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member
#endregion create member

#region get all members
@router.get("/", response_model=List[MemberResponse])
def get_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    members = db.query(Member).offset(skip).limit(limit).all()
    return members
#endregion get all members

#region get member
@router.get("/{member_user_id}", response_model=MemberResponse)
def get_member(member_user_id: int, db: Session = Depends(get_db)):

    member = db.query(Member).filter(Member.member_user_id == member_user_id).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    return member
#endregion get member

#region update member
@router.put("/{member_user_id}", response_model=MemberResponse)
def update_member(
    member_user_id: int,
    house_rules: Optional[str] = Query(None),
    dependent_description: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    db_member = db.query(Member).filter(Member.member_user_id == member_user_id).first()
    
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    if house_rules is not None:
        db_member.house_rules = house_rules
    if dependent_description is not None:
        db_member.dependent_description = dependent_description
    
    db.commit()
    db.refresh(db_member)
    return db_member
#endregion update member

#region delete member
@router.delete("/{member_user_id}", status_code=204)
def delete_member(member_user_id: int, db: Session = Depends(get_db)):
    db_member = db.query(Member).filter(Member.member_user_id == member_user_id).first()
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    db.delete(db_member)
    db.commit()
    return None
#endregion delete member