from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class JobApplication(Base):
    
    __tablename__ = 'job_application'
    
    caregiver_user_id = Column(Integer, ForeignKey('caregiver.caregiver_user_id', ondelete='CASCADE'), primary_key=True)
    job_id = Column(Integer, ForeignKey('job.job_id', ondelete='CASCADE'), primary_key=True)
    date_applied = Column(Date, nullable=False)
    
    caregiver = relationship("Caregiver", back_populates="job_applications")
    job = relationship("Job", back_populates="job_applications")

