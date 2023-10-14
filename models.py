from database import Base
from sqlalchemy import  Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import  Date, Double
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

#User class
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique= True)
    password = Column(String, nullable=False)
    name = Column(String, nullable= False)
    url = Column(String, nullable=True)
    phone = Column(String, nullable=False)
    role = Column(String, nullable=False)


#Doctor AvailableOnlineTime
class availableOnlineTime(Base):
    __tablename__ = 'available_online_time'

    id = Column(Integer, primary_key=True,index=True)
    doctor = relationship("Doctor",back_populates="availableOnlineTimes")
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    date = Column(Date, nullable=False)
    day= Column(String, nullable=True)
    start_time = Column(Double, nullable=False)
    end_time = Column(Double, nullable=False)
    available_time = Column(Double, nullable=False)


#Doctor AvailableOfflineTime
class availableOfflineTime(Base):
    __tablename__ = 'available_offline_time'

    id = Column(Integer, primary_key=True,index=True)
    doctor = relationship("Doctor",back_populates="availableOfflineTimes")
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    date = Column(Date, nullable=False)
    day= Column(String, nullable=True)
    start_time = Column(Double, nullable=False)
    end_time = Column(Double, nullable=False)
    available_time = Column(Double, nullable=False)
    
#Doctor class
class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True,index=True)
    bmdc = Column(String, nullable=True)
    bio= Column(String, nullable=True)
    balance = Column(Integer, nullable=True)
    rating = Column(Double,nullable=True,default=0.0)
    expertise= Column(String, nullable=True)
    current_hospital= Column(String, nullable=True)
    place= Column(String, nullable=True)
    online_fee = Column(Integer, nullable=True)
    offline_fee = Column(Integer, nullable=True)
    degrees =Column(String, nullable=True)
    user = relationship("User")
    user_id = Column(Integer, ForeignKey('users.id'))
    availableOfflineTimes = relationship("availableOfflineTime",back_populates="doctor")
    availableOnlineTimes = relationship("availableOnlineTime",back_populates="doctor")

#Hospital Class
class Hospital(Base):
    __tablename__ = 'hospitals'
    id = Column(Integer, primary_key=True,index=True)
    user = relationship("User")
    user_id = Column(Integer, ForeignKey('users.id'))
    bio= Column(String, nullable=True)
    hospitalName= Column(String, nullable=True)
    place= Column(String, nullable=True)


#DoctorSerial class    
class DoctorSerial(Base):
    __tablename__ = "doctorserials"
    id =Column(Integer, primary_key=True,index=True)

    type = Column(String, nullable=False)

    price = Column(Integer, nullable=False)

    date = Column(Date, nullable=False)

    appointmentDate = Column(Date, nullable=False)

    time = Column(Double, nullable=False)

    reviewchecked = Column(Integer, nullable=False,default=None)

    checked = Column(Integer, nullable=False)

    prescription = Column(String, nullable=True,default=None)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User",foreign_keys=[user_id])
   

    doctor_id = Column(Integer, ForeignKey("users.id"))
    doctor = relationship("User",foreign_keys=[doctor_id])
    

#Review class
class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True,index=True)

    starCount = Column(Integer, nullable=False)

    review = Column(String, nullable=False)

    reviewer_id = Column(Integer, ForeignKey("users.id"))   
    reviewer =relationship("User", foreign_keys=[reviewer_id])
    

    subject_id = Column(Integer, ForeignKey("users.id"))
    subject =relationship("User", foreign_keys=[subject_id])
    

#MedicineReminder class
class MedicineReminder(Base):
    __tablename__ = 'medicine_reminders'
    id = Column(Integer, primary_key=True,index=True)
    description = Column(String, nullable=False)
    time = Column(String, nullable=False)
    days=Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")
  
#Diagnosis class
clas