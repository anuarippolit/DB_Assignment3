from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = 'account'
    
    user_id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False) 
    given_name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    city = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    profile_description = Column(Text)
    password = Column(String, nullable=False)
    
    caregiver = relationship("Caregiver", back_populates="user", uselist=False, cascade="all, delete-orphan")
    member = relationship("Member", back_populates="user", uselist=False, cascade="all, delete-orphan")

