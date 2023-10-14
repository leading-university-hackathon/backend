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
    bio= Column(String, nullable=True)
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
    
#Hospital class

class Hospital(Base):
    __tablename__ = 'hospitals'

    id = Column(Integer, primary_key=True,index=True)
    bio= Column(String, nullable=True)
    hospitalName = Column(String, nullable=False)
    place = Column(String, nullable=False)
    user = relationship("User")
    user_id = Column(Integer, ForeignKey('users.id'))

    
    
