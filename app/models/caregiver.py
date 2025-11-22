from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.enums import CaregivingType, Gender

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

# class GenderEnum(TypeDecorator):
#     impl = String
#     cache_ok = True
    
#     def __init__(self):
#         super().__init__(length=50)
    
#     def process_bind_param(self, value, dialect):
#         if value is None:
#             return value
#         if isinstance(value, Gender):
#             return value.value
#         return value
    
#     def process_result_value(self, value, dialect):
#         if value is None:
#             return value
#         try:
#             return Gender(value)
#         except ValueError:
#             return value

class Caregiver(Base):
    __tablename__ = 'caregiver'
    __table_args__ = (
        CheckConstraint("hourly_rate >= 0"),
    )
    
    caregiver_user_id = Column(Integer, ForeignKey('account.user_id', ondelete='CASCADE'), primary_key=True)
    photo = Column(String)
    gender = Column(SQLEnum(Gender, native_enum=True), nullable=False)
    caregiving_type = Column(SQLEnum(CaregivingType, native_enum=True), nullable=False)
    hourly_rate = Column(Integer, nullable=False)
    
    user = relationship("User", back_populates="caregiver")
    job_applications = relationship("JobApplication", back_populates="caregiver", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="caregiver", cascade="all, delete-orphan")

