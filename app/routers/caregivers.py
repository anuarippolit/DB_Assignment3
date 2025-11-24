from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import Caregiver, User
from app.models.enums import CaregivingType, Gender
from app.schemas import CaregiverCreate, CaregiverUpdate, CaregiverResponse
from app.database import get_db, STATIC_FOLDER
import os
import uuid
from pathlib import Path

router = APIRouter(prefix="/caregivers", tags=["caregivers"])

static_path = Path(STATIC_FOLDER)
static_path.mkdir(exist_ok=True)

#region caregiver entity routes

#region create
@router.post("/", response_model=CaregiverResponse, status_code=201)
async def create_caregiver(
    caregiver_user_id: int = Form(...),
    gender: Gender = Form(...),
    caregiving_type: CaregivingType = Form(...),
    hourly_rate: int = Form(...),
    photo: UploadFile = File(..., description="Photo file"),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.user_id == caregiver_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if db.query(Caregiver).filter(Caregiver.caregiver_user_id == caregiver_user_id).first():
        raise HTTPException(status_code=400, detail="Caregiver already exists")
    
    file_extension = os.path.splitext(photo.filename)[1] if photo.filename else ".jpg"
    photo_filename = f"{caregiver_user_id}_{uuid.uuid4().hex}{file_extension}"
    file_path = static_path / photo_filename
    
    with open(file_path, "wb") as buffer:
        content = await photo.read()
        buffer.write(content)
    
    db_caregiver = Caregiver(
        caregiver_user_id=caregiver_user_id,
        photo=photo_filename,
        gender=gender,
        caregiving_type=caregiving_type,
        hourly_rate=hourly_rate
    )
    db.add(db_caregiver)
    db.commit()
    db.refresh(db_caregiver)
    return db_caregiver
#endregion

#region get all
@router.get("/", response_model=List[CaregiverResponse])
def get_caregivers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    caregivers = db.query(Caregiver).offset(skip).limit(limit).all()
    return caregivers
#endregion

#region get one
@router.get("/{caregiver_user_id}", response_model=CaregiverResponse)
def get_caregiver(caregiver_user_id: int, db: Session = Depends(get_db)):
    caregiver = db.query(Caregiver).filter(Caregiver.caregiver_user_id == caregiver_user_id).first()
    if not caregiver:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    return caregiver
#endregion

#region update
@router.put("/{caregiver_user_id}", response_model=CaregiverResponse)
def update_caregiver(
    caregiver_user_id: int,
    gender: Optional[Gender] = Query(None, description="Gender of the caregiver. Possible values: MALE, FEMALE, OTHER"),
    caregiving_type: Optional[CaregivingType] = Query(None, description="Type of caregiving service. Possible values: BABYSITTER, ELDERLY_CARE, PLAYMATE_FOR_CHILDREN"),
    hourly_rate: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    db_caregiver = db.query(Caregiver).filter(Caregiver.caregiver_user_id == caregiver_user_id).first()
    if not db_caregiver:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    
    if gender is not None:
        db_caregiver.gender = gender
    if caregiving_type is not None:
        db_caregiver.caregiving_type = caregiving_type
    if hourly_rate is not None:
        db_caregiver.hourly_rate = hourly_rate
    
    db.commit()
    db.refresh(db_caregiver)
    return db_caregiver
#endregion

#region delete

@router.delete("/{caregiver_user_id}", status_code=204)
def delete_caregiver(caregiver_user_id: int, db: Session = Depends(get_db)):
    db_caregiver = db.query(Caregiver).filter(Caregiver.caregiver_user_id == caregiver_user_id).first()
    if not db_caregiver:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    
    if db_caregiver.photo:
        photo_path = static_path / db_caregiver.photo
        if photo_path.exists():
            photo_path.unlink()
    
    db.delete(db_caregiver)
    db.commit()
    return None
#endregion

#endregion

#region photo routes

#region get photo
@router.get("/{caregiver_user_id}/photo")
def get_caregiver_photo(caregiver_user_id: int, db: Session = Depends(get_db)):
    caregiver = db.query(Caregiver).filter(Caregiver.caregiver_user_id == caregiver_user_id).first()
    if not caregiver:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    
    if not caregiver.photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    photo_path = static_path / caregiver.photo
    if not photo_path.exists():
        raise HTTPException(status_code=404, detail="Photo file not found")
    
    return FileResponse(photo_path)
#endregion

#region update photo
@router.put("/{caregiver_user_id}/photo", response_model=CaregiverResponse)
async def update_caregiver_photo(
    caregiver_user_id: int,
    photo: UploadFile = File(..., description="Photo file"),
    db: Session = Depends(get_db)
):
    db_caregiver = db.query(Caregiver).filter(Caregiver.caregiver_user_id == caregiver_user_id).first()
    if not db_caregiver:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    
    #delete old photo 
    if db_caregiver.photo:
        old_photo_path = static_path / db_caregiver.photo
        if old_photo_path.exists():
            old_photo_path.unlink()
    
    #new photo
    file_extension = os.path.splitext(photo.filename)[1] if photo.filename else ".jpg"
    photo_filename = f"{caregiver_user_id}_{uuid.uuid4().hex}{file_extension}"
    file_path = static_path / photo_filename
    
    with open(file_path, "wb") as buffer:
        content = await photo.read()
        buffer.write(content)
    
    db_caregiver.photo = photo_filename
    db.commit()
    db.refresh(db_caregiver)
    return db_caregiver
#endregion  

#endregion
