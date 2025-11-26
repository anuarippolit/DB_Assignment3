from fastapi import APIRouter, Depends, HTTPException, Form, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
import logging

from typing import List, Optional
from pydantic import EmailStr
import re

from app.models import User
from app.schemas import UserCreate, UserUpdate, UserResponse
from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])

#region validation methods
def validate_phone(phone: str) -> bool:
    #deleting all spaces, -, () and etc
    phone_clean = re.sub(r'[\s\-\(\)]', '', phone)
    
    #normalize 
    if phone_clean.startswith('8'):
        phone_clean = '7' + phone_clean[1:]
    elif phone_clean.startswith('+7'):
        phone_clean = '7' + phone_clean[2:]
    elif phone_clean.startswith('7'):
        pass
    else:
        return False
    
    if len(phone_clean) != 11:
        return False
    
    if not phone_clean.isdigit():
        return False
    
    if not phone_clean.startswith('7'):
        return False
    
    if len(phone_clean) > 1 and phone_clean[1] == '0':
        return False
    
    return True
#endregion validation methods

#region create user
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    email: EmailStr = Form(...),
    given_name: str = Form(...),
    surname: str = Form(...),
    city: str = Form(...),
    phone_number: str = Form(...),
    profile_description: Optional[str] = Form(None),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        #region validation 
        if db.query(User).filter(User.email == email).first():
            raise HTTPException(status_code=400, detail="Email already registered")

        #email not validated, because Pydantic auto validates it
        
        if not validate_phone(phone_number):
            raise HTTPException(status_code=400, detail="Invalid phone number format. Expected format: +77071111111 or 87071111111")
        #endregion validation 

        #user_id is auto-generated. 
        max_u = db.query(User).order_by(User.user_id.desc()).first()
        new_user_id = (max_u.user_id + 1) if max_u else 1
        
        u = User(
            user_id=new_user_id,
            email=email,
            given_name=given_name,
            surname=surname,
            city=city,
            phone_number=phone_number,
            profile_description=profile_description,
            password=password
        )

        db.add(u)
        db.commit()
        db.refresh(u)

        return u
    except OperationalError as e:
        logger.error(f"Database connection error in POST /users/: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database connection error. Please try again later."
        )
#endregion create user

#region get user
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        u = db.query(User).filter(User.user_id == user_id).first()

        if not u:
            raise HTTPException(status_code=404, detail="User not found")
        return u
    except OperationalError as e:
        logger.error(f"Database connection error in GET /users/{user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database connection error. Please try again later."
        )
#endregion get user

#region get all users
@router.get("/", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        u = db.query(User).offset(skip).limit(limit).all()
        return u
    except OperationalError as e:
        logger.error(f"Database connection error in GET /users/: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database connection error. Please try again later."
        )
#endregion get all users

#region update user
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    email: Optional[EmailStr] = Query(None),
    given_name: Optional[str] = Query(None),
    surname: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    phone_number: Optional[str] = Query(None),
    profile_description: Optional[str] = Query(None),
    password: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        u = db.query(User).filter(User.user_id == user_id).first()

        if not u:
            raise HTTPException(status_code=404, detail="User not found")
        
        #region validation
        if email is not None and email != u.email:
            if db.query(User).filter(User.email == email).first():
                raise HTTPException(status_code=400, detail="Email already registered")
            u.email = email
        
        if phone_number is not None:
            if not validate_phone(phone_number):
                raise HTTPException(status_code=400, detail="Invalid phone number format. Expected format: +77071111111 or 87071111111")
            u.phone_number = phone_number
        #endregion validation

        if given_name is not None:
            u.given_name = given_name
        if surname is not None:
            u.surname = surname
        if city is not None:
            u.city = city
        if profile_description is not None:
            u.profile_description = profile_description
        if password is not None:
            u.password = password
        
        db.commit()
        db.refresh(u)
        return u
    except OperationalError as e:
        logger.error(f"Database connection error in PUT /users/{user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database connection error. Please try again later."
        )
#endregion update user

#region delete user
@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        u = db.query(User).filter(User.user_id == user_id).first()

        if not u:
            raise HTTPException(status_code=404, detail="User not found")
        
        db.delete(u)
        db.commit()

        return None
    except OperationalError as e:
        logger.error(f"Database connection error in DELETE /users/{user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database connection error. Please try again later."
        )
#endregion delete user