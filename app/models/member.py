from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Member(Base):
    __tablename__ = 'member'
    
    member_user_id = Column(Integer, ForeignKey('account.user_id', ondelete='CASCADE'), primary_key=True)
    house_rules = Column(Text)
    dependent_description = Column(Text)
    
    user = relationship("User", back_populates="member")
    address = relationship("Address", back_populates="member", uselist=False, cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="member", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="member", cascade="all, delete-orphan")

