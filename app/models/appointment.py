from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, CheckConstraint, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.enums import AppointmentStatus

#not valid, made enums in database.sql:
#in database it is TEXT, so I have to process enum to string
# class AppointmentStatusEnum(TypeDecorator):
#     impl = String
#     cache_ok = True
    
#     def __init__(self):
#         super().__init__(length=50)
    
#     def process_bind_param(self, value, dialect):
#         if value is None:
#             return value
#         if isinstance(value, AppointmentStatus):
#             return value.value
#         return value
    
#     def process_result_value(self, value, dialect):
#         if value is None:
#             return value
#         try:
#             return AppointmentStatus(value)
#         except ValueError:
#             return value

class Appointment(Base):
    __tablename__ = 'appointment'
    __table_args__ = (
        CheckConstraint("work_hours > 0"),
    )
    
    appointment_id = Column(Integer, primary_key=True)
    caregiver_user_id = Column(Integer, ForeignKey('caregiver.caregiver_user_id', ondelete='CASCADE'), nullable=False)
    member_user_id = Column(Integer, ForeignKey('member.member_user_id', ondelete='CASCADE'), nullable=False)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    work_hours = Column(Integer, nullable=False)
    status = Column(SQLEnum(AppointmentStatus, native_enum=True), nullable=False) 
    
    caregiver = relationship("Caregiver", back_populates="appointments")
    member = relationship("Member", back_populates="appointments")