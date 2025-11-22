from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Address(Base):
    __tablename__ = 'address'
    
    member_user_id = Column(Integer, ForeignKey('member.member_user_id', ondelete='CASCADE'), primary_key=True)
    house_number = Column(String, nullable=False)
    street = Column(String, nullable=False)
    town = Column(String, nullable=False)
    
    member = relationship("Member", back_populates="address")

