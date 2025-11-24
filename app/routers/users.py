from fastapi import APIRouter, Depends, HTTPException, Form, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import EmailStr
import re
from app.models import User
from app.schemas import UserCreate, UserUpdate, UserResponse
from app.database import get_db

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
    #region validation 
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    #email not validated, because Pydantic auto validates it
    
    if not validate_phone(phone_number):
        raise HTTPException(status_code=400, detail="Invalid phone number format. Expected format: +77071111111 or 87071111111")
    #endregion validation 

    #user_id is auto-generated. 
    max_user = db.query(User).order_by(User.user_id.desc()).first()
    new_user_id = (max_user.user_id + 1) if max_user else 1
    
    db_user = User(
        user_id=new_user_id,
        email=email,
        given_name=given_name,
        surname=surname,
        city=city,
        phone_number=phone_number,
        profile_description=profile_description,
        password=password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
#endregion create user

#region get user
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
#endregion get user

#region get all users
@router.get("/", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()

    return users
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
    db_user = db.query(User).filter(User.user_id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    #region validation
    if email is not None and email != db_user.email:
        if db.query(User).filter(User.email == email).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        db_user.email = email
    
    if phone_number is not None:
        if not validate_phone(phone_number):
            raise HTTPException(status_code=400, detail="Invalid phone number format. Expected format: +77071111111 or 87071111111")
        db_user.phone_number = phone_number
    #endregion validation

    if given_name is not None:
        db_user.given_name = given_name
    if surname is not None:
        db_user.surname = surname
    if city is not None:
        db_user.city = city
    if profile_description is not None:
        db_user.profile_description = profile_description
    if password is not None:
        db_user.password = password
    
    db.commit()
    db.refresh(db_user)
    return db_user
#endregion update user

#region delete user
@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()

    return None
#endregion delete user