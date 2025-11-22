from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.enums import CaregivingType

#not valid, made enums in database.sql:
#in database it is TEXT, so I have to process enum to string
# class CaregivingTypeEnum(TypeDecorator):
#     impl = String
#     cache_ok = True
    
#     def __init__(self):
#         super().__init__(length=50)
    
#     def process_bind_param(self, value, dialect):
#         if value is None:
#             return value
#         if isinstance(value, CaregivingType):
#             return value.value
#         return value
    
#     def process_result_value(self, value, dialect):
#         if value is None:
#             return value
#         try:
#             return CaregivingType(value)
#         except ValueError:
#             return value

class Job(Base):
    __tablename__ = 'job'
    
    job_id = Column(Integer, primary_key=True)
    member_user_id = Column(Integer, ForeignKey('member.member_user_id', ondelete='CASCADE'), nullable=False)
    required_caregiving_type = Column(SQLEnum(CaregivingType, native_enum=True), nullable=False)
    other_requirements = Column(Text)
    date_posted = Column(Date, nullable=False)
    
    member = relationship("Member", back_populates="jobs")
    job_applications = relationship("JobApplication", back_populates="job", cascade="all, delete-orphan")

